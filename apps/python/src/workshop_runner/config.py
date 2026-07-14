"""Configuration loading and validation.

Fails BEFORE any request is sent when configuration is invalid, and never prints the API key.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigError(Exception):
    """Raised when configuration is missing or invalid. Message never contains the key."""


_REQUIRED = ("AZURE_OPENAI_BASE_URL", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT")


@dataclass(frozen=True)
class Config:
    base_url: str
    api_key: str
    deployment: str
    reasoning_effort: str = "low"
    max_output_tokens: int = 800
    request_timeout_seconds: int = 90
    save_results: bool = False
    results_directory: str = "generated-results"

    def redacted(self) -> dict:
        """A dict safe to print/log — the key is masked."""
        return {
            "base_url": self.base_url,
            "api_key": "***redacted***",
            "deployment": self.deployment,
            "reasoning_effort": self.reasoning_effort,
            "max_output_tokens": self.max_output_tokens,
            "request_timeout_seconds": self.request_timeout_seconds,
        }


def _to_int(name: str, value: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ConfigError(f"{name} must be an integer, got a non-numeric value.")
    if parsed <= 0:
        raise ConfigError(f"{name} must be a positive integer.")
    return parsed


def load_config(env: dict | None = None) -> Config:
    """Load and validate configuration from environment variables.

    Raises ConfigError (without exposing the key) on any problem.
    """
    env = dict(os.environ if env is None else env)

    missing = [name for name in _REQUIRED if not (env.get(name) or "").strip()]
    if missing:
        raise ConfigError(
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in the workshop values."
        )

    base_url = env["AZURE_OPENAI_BASE_URL"].strip()
    api_key = env["AZURE_OPENAI_API_KEY"].strip()
    deployment = env["AZURE_OPENAI_DEPLOYMENT"].strip()

    if "<" in api_key and ">" in api_key:
        raise ConfigError("AZURE_OPENAI_API_KEY still contains a placeholder. Paste the real workshop key.")
    if not base_url.startswith("https://"):
        raise ConfigError("AZURE_OPENAI_BASE_URL must use https://.")
    if not base_url.rstrip("/").endswith("/openai/v1"):
        raise ConfigError("AZURE_OPENAI_BASE_URL must end in /openai/v1/ (the v1 Responses API base).")
    if not deployment:
        raise ConfigError("AZURE_OPENAI_DEPLOYMENT must not be blank.")

    return Config(
        base_url=base_url,
        api_key=api_key,
        deployment=deployment,
        reasoning_effort=(env.get("WORKSHOP_REASONING_EFFORT") or "low").strip(),
        max_output_tokens=_to_int("WORKSHOP_MAX_OUTPUT_TOKENS", env.get("WORKSHOP_MAX_OUTPUT_TOKENS", "800")),
        request_timeout_seconds=_to_int(
            "WORKSHOP_REQUEST_TIMEOUT_SECONDS", env.get("WORKSHOP_REQUEST_TIMEOUT_SECONDS", "90")
        ),
        save_results=(env.get("WORKSHOP_SAVE_RESULTS", "false").strip().lower() == "true"),
        results_directory=(env.get("WORKSHOP_RESULTS_DIRECTORY") or "generated-results").strip(),
    )
