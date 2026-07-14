import pytest

from workshop_runner.chain import run_chain
from workshop_runner.prompts import PromptManifest
from workshop_runner.client import ModelResponse

pytestmark = pytest.mark.offline


def _stage(id_, tmp_path, sys_text, user_text, variables):
    (tmp_path / f"{id_}-sys.md").write_text(sys_text, encoding="utf-8")
    (tmp_path / f"{id_}-user.md").write_text(user_text, encoding="utf-8")
    return PromptManifest(
        id=id_, version="1.0.0", lab="05-prompt-chaining", variant="stage",
        purpose="test", user_prompt=f"{id_}-user.md", variables=variables,
        model={"reasoning_effort": "low", "max_output_tokens": 100, "store": False},
        system_prompt=f"{id_}-sys.md", _dir=tmp_path,
    )


def test_chain_completes_when_stages_valid(tmp_path):
    s1 = _stage("s1", tmp_path, "extract", "req {{request_text}}", ["request_text"])
    s2 = _stage("s2", tmp_path, "classify", "facts {{previous_output}}", ["previous_output"])

    outputs = iter(['{"reported_issue": "wifi"}', "Category: network"])

    def respond(system, user):
        return ModelResponse(text=next(outputs))

    result = run_chain([s1, s2], {"request_text": "wifi down"}, respond)
    assert result.completed
    assert len(result.stages) == 2
    assert result.stopped_at is None


def test_chain_stops_on_invalid_intermediate(tmp_path):
    s1 = _stage("s1", tmp_path, "extract", "req {{request_text}}", ["request_text"])
    s2 = _stage("s2", tmp_path, "classify", "facts {{previous_output}}", ["previous_output"])

    # Stage 1 returns non-JSON -> chain must stop before stage 2.
    outputs = iter(["not json at all", "should never run"])

    def respond(system, user):
        return ModelResponse(text=next(outputs))

    result = run_chain([s1, s2], {"request_text": "wifi down"}, respond)
    assert not result.completed
    assert result.stopped_at == "s1"
    assert len(result.stages) == 1  # stage 2 never executed
