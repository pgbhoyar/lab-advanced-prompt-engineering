"""Recorded, API-shaped fixtures and fake transports for offline tests (no network)."""
from __future__ import annotations

import json

from workshop_runner.client import ModelResponse

VALID_TRIAGE = {
    "request_id": "SR-0001",
    "summary": "User cannot connect to office WiFi; single-user issue.",
    "category": "network",
    "urgency": "high",
    "recommended_action": "Have the user forget and rejoin the WiFi network; if unresolved, check the device WiFi adapter.",
    "missing_information": [],
    "evidence": ["Everyone else on the team is fine", "Restart already attempted"],
    "confidence": "medium",
    "needs_human_review": False,
}

SUCCESS_TEXT = "This request looks like a network connectivity problem. I'd suggest rejoining the WiFi."


def transport_success_text(**_kwargs) -> ModelResponse:
    return ModelResponse(text=SUCCESS_TEXT, input_tokens=120, output_tokens=30, request_id="resp_text_1")


def transport_success_structured(**_kwargs) -> ModelResponse:
    return ModelResponse(text=json.dumps(VALID_TRIAGE), input_tokens=200, output_tokens=90, request_id="resp_json_1")


def transport_invalid_json(**_kwargs) -> ModelResponse:
    return ModelResponse(text="Sure! Here is the triage: category is network, urgency high.")


def transport_schema_violation(**_kwargs) -> ModelResponse:
    bad = dict(VALID_TRIAGE)
    bad["urgency"] = "urgent"  # not an allowed enum
    bad["extra_field"] = "nope"
    return ModelResponse(text=json.dumps(bad))


def transport_missing_output(**_kwargs) -> ModelResponse:
    return ModelResponse(text="")


class _HttpError(Exception):
    def __init__(self, status: int):
        super().__init__(f"HTTP {status}")
        self.status_code = status


def make_flaky_then_ok(fail_times: int, status: int = 429):
    """A transport that fails `fail_times` with `status`, then returns a valid structured response."""
    state = {"calls": 0}

    def transport(**_kwargs) -> ModelResponse:
        state["calls"] += 1
        if state["calls"] <= fail_times:
            raise _HttpError(status)
        return transport_success_structured()

    return transport, state


def transport_auth_failure(**_kwargs) -> ModelResponse:
    raise _HttpError(401)


def transport_timeout(**_kwargs) -> ModelResponse:
    class _Timeout(Exception):
        pass
    raise _Timeout("request timeout")


def transport_content_filter(**_kwargs) -> ModelResponse:
    raise _HttpError(400)
