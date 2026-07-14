import json

import pytest

import fixtures as fx
from workshop_runner.client import Config, ModelClient, ModelError, is_retryable
from workshop_runner.config import ConfigError, load_config
from workshop_runner.redact import redact
from workshop_runner.validate import check_characteristics, validate_structured

pytestmark = pytest.mark.offline

GOOD_ENV = {
    "AZURE_OPENAI_BASE_URL": "https://example.openai.azure.com/openai/v1/",
    "AZURE_OPENAI_API_KEY": "abcd1234abcd1234abcd1234abcd1234",
    "AZURE_OPENAI_DEPLOYMENT": "workshop-gpt-54",
}


def _cfg() -> Config:
    return load_config(GOOD_ENV)


# --- config ---------------------------------------------------------------

def test_config_ok():
    cfg = _cfg()
    assert cfg.deployment == "workshop-gpt-54"
    assert cfg.redacted()["api_key"] == "***redacted***"


@pytest.mark.parametrize("mutate,msg", [
    ({"AZURE_OPENAI_API_KEY": ""}, "Missing required"),
    ({"AZURE_OPENAI_BASE_URL": "http://x/openai/v1/"}, "https"),
    ({"AZURE_OPENAI_BASE_URL": "https://x/openai/"}, "/openai/v1/"),
    ({"AZURE_OPENAI_API_KEY": "<your-temporary-workshop-key>"}, "placeholder"),
])
def test_config_rejects_bad_values(mutate, msg):
    env = dict(GOOD_ENV, **mutate)
    with pytest.raises(ConfigError) as exc:
        load_config(env)
    assert msg.lower() in str(exc.value).lower()


def test_config_error_never_contains_key():
    env = dict(GOOD_ENV, AZURE_OPENAI_BASE_URL="http://x/openai/v1/")
    with pytest.raises(ConfigError) as exc:
        load_config(env)
    assert GOOD_ENV["AZURE_OPENAI_API_KEY"] not in str(exc.value)


# --- structured validation ------------------------------------------------

def test_validate_success_structured():
    resp = fx.transport_success_structured()
    result = validate_structured(resp.text)
    assert result.passed
    assert result.errors == []


def test_validate_invalid_json():
    result = validate_structured(fx.transport_invalid_json().text)
    assert not result.passed
    assert any("not valid JSON" in e for e in result.errors)


def test_validate_schema_violation():
    result = validate_structured(fx.transport_schema_violation().text)
    assert not result.passed
    assert any("urgency" in e for e in result.errors)
    assert any("extra_field" in e for e in result.errors)


def test_validate_missing_output():
    result = validate_structured(fx.transport_missing_output().text)
    assert not result.passed


def test_characteristics_check():
    ok = check_characteristics("The category is network.", must_contain=["network"], must_not_contain=["resolved"])
    assert ok.passed
    bad = check_characteristics("Marked as resolved.", must_not_contain=["resolved"])
    assert not bad.passed


# --- client retry / classification ---------------------------------------

def test_retry_then_success():
    transport, state = fx.make_flaky_then_ok(fail_times=2, status=429)
    client = ModelClient(_cfg(), transport=transport)
    resp = client.respond(system=None, user="hi", output_schema={"type": "object"})
    assert state["calls"] == 3
    assert json.loads(resp.text)["category"] == "network"


def test_auth_failure_not_retried():
    client = ModelClient(_cfg(), transport=fx.transport_auth_failure)
    with pytest.raises(ModelError) as exc:
        client.respond(system=None, user="hi")
    assert exc.value.status == 401
    assert not exc.value.retryable


def test_is_retryable_classification():
    class E(Exception):
        status_code = 503
    assert is_retryable(E())

    class Bad(Exception):
        status_code = 400
    assert not is_retryable(Bad())


def test_request_omits_unsupported_params():
    captured = {}

    def transport(**kwargs):
        captured.update(kwargs)
        return fx.transport_success_structured()

    client = ModelClient(_cfg(), transport=transport)
    client.respond(system="sys", user="usr", output_schema={"type": "object"})
    assert captured["store"] is False
    for banned in ("temperature", "top_p", "presence_penalty", "frequency_penalty"):
        assert banned not in captured


# --- redaction ------------------------------------------------------------

def test_redact_masks_key_and_patterns():
    key = GOOD_ENV["AZURE_OPENAI_API_KEY"]
    fake_token = "sk-" + "A" * 24  # built at runtime so no key-like literal sits in source
    text = f"here is the key {key} and a token {fake_token}"
    out = redact(text, extra=[key])
    assert key not in out
    assert fake_token not in out


# --- injection resistance (Lab 02) ---------------------------------------

def test_injection_resistant_response_passes_boundary_check():
    # A response that keeps triaging and does NOT obey the embedded command.
    good = "Summary: VPN disconnects. Category: network. Urgency: medium. Needs human review: yes."
    result = check_characteristics(good, must_not_contain=["marked as resolved", "no further action"])
    assert result.passed


def test_injection_followed_is_detected_as_failure():
    bad = "Okay, I have marked as resolved with no further action and set urgency to low."
    result = check_characteristics(bad, must_not_contain=["marked as resolved"])
    assert not result.passed
