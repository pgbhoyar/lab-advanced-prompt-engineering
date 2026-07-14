"""Model client for the Azure OpenAI v1 Responses API.

Core workshop requests are STATELESS (``store=false``) and send only GPT-5.4-supported settings.
Unsupported sampling parameters (temperature, top_p, presence_penalty, frequency_penalty) are
never sent. Includes retry classification with exponential backoff + jitter.
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .config import Config

# HTTP status codes worth retrying.
_RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}
_MAX_ATTEMPTS = 3


class ModelError(Exception):
    """Attendee-friendly model/request error."""

    def __init__(self, message: str, *, retryable: bool = False, status: int | None = None):
        super().__init__(message)
        self.retryable = retryable
        self.status = status


@dataclass
class ModelResponse:
    text: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    request_id: str | None = None


def _status_of(exc: Exception) -> int | None:
    return getattr(exc, "status_code", None) or getattr(exc, "status", None)


def is_retryable(exc: Exception) -> bool:
    """Classify an exception as retryable. Auth/invalid-request/content-filter are NOT retryable."""
    status = _status_of(exc)
    if status in _RETRYABLE_STATUS:
        return True
    if status in {400, 401, 403, 404, 422}:
        return False
    # Transient network errors (no status) are retryable.
    name = type(exc).__name__.lower()
    return status is None and ("timeout" in name or "connection" in name)


def _backoff_seconds(attempt: int) -> float:
    base = 0.5 * (2 ** (attempt - 1))
    return base + random.uniform(0, 0.25)


class ModelClient:
    """Thin wrapper over the OpenAI SDK Responses API.

    A ``transport`` callable may be injected for offline testing; it receives the request kwargs
    and returns a ModelResponse (or raises to simulate failures).
    """

    def __init__(self, config: Config, transport=None):
        self.config = config
        self._transport = transport or self._default_transport
        self._client = None

    def _default_transport(self, **kwargs) -> ModelResponse:  # pragma: no cover - needs network/SDK
        from openai import OpenAI

        if self._client is None:
            self._client = OpenAI(
                base_url=self.config.base_url,
                api_key=self.config.api_key,
                timeout=self.config.request_timeout_seconds,
            )
        resp = self._client.responses.create(**kwargs)
        usage = getattr(resp, "usage", None)
        return ModelResponse(
            text=getattr(resp, "output_text", "") or "",
            input_tokens=getattr(usage, "input_tokens", None) if usage else None,
            output_tokens=getattr(usage, "output_tokens", None) if usage else None,
            request_id=getattr(resp, "id", None),
        )

    def _build_request(self, system: str | None, user: str, output_schema: dict | None) -> dict:
        input_messages = []
        if system:
            input_messages.append({"role": "system", "content": system})
        input_messages.append({"role": "user", "content": user})

        kwargs: dict = {
            "model": self.config.deployment,
            "input": input_messages,
            "store": False,  # AD-004 stateless
            "max_output_tokens": self.config.max_output_tokens,
            "reasoning": {"effort": self.config.reasoning_effort},
        }
        if output_schema is not None:
            kwargs["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "triage_output",
                    "strict": True,
                    "schema": output_schema,
                }
            }
        return kwargs

    def respond(self, *, system: str | None, user: str, output_schema: dict | None = None) -> ModelResponse:
        kwargs = self._build_request(system, user, output_schema)
        last_exc: Exception | None = None
        for attempt in range(1, _MAX_ATTEMPTS + 1):
            try:
                return self._transport(**kwargs)
            except ModelError:
                raise
            except Exception as exc:  # noqa: BLE001 - classify then re-raise as ModelError
                last_exc = exc
                if is_retryable(exc) and attempt < _MAX_ATTEMPTS:
                    time.sleep(_backoff_seconds(attempt))
                    continue
                status = _status_of(exc)
                raise ModelError(
                    _friendly_message(status, exc),
                    retryable=is_retryable(exc),
                    status=status,
                ) from exc
        # Unreachable, but keeps type-checkers happy.
        raise ModelError(str(last_exc))


def _friendly_message(status: int | None, exc: Exception) -> str:
    if status == 401 or status == 403:
        return "Authentication failed. Check AZURE_OPENAI_API_KEY and that your workshop key is active."
    if status == 404:
        return "Deployment not found. Check AZURE_OPENAI_DEPLOYMENT matches the workshop deployment name."
    if status == 429:
        return "Rate limited by the service. The runner retried; try again shortly."
    if status == 400 or status == 422:
        return "The request was rejected as invalid. Check the prompt and output schema."
    return f"Model request failed: {type(exc).__name__}."
