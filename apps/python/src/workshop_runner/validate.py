"""Response validation: strict structured output + free-text characteristics."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

_ALLOWED = {
    "category": {"access", "hardware", "software", "network", "security", "other"},
    "urgency": {"low", "medium", "high", "critical"},
    "confidence": {"low", "medium", "high"},
}
_REQUIRED_FIELDS = [
    "request_id", "summary", "category", "urgency", "recommended_action",
    "missing_information", "evidence", "confidence", "needs_human_review",
]


@dataclass
class ValidationResult:
    passed: bool
    errors: list[str] = field(default_factory=list)
    parsed: dict | None = None

    def summary_line(self) -> str:
        return "VALIDATION: PASS" if self.passed else "VALIDATION: FAIL"


def validate_structured(response_text: str) -> ValidationResult:
    """Validate a triage JSON response against the shared output contract."""
    errors: list[str] = []
    text = (response_text or "").strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return ValidationResult(False, [f"Response is not valid JSON: {exc}"])

    if not isinstance(parsed, dict):
        return ValidationResult(False, ["Root of the response must be a JSON object."], None)

    for f in _REQUIRED_FIELDS:
        if f not in parsed:
            errors.append(f"Missing required field: {f}")

    extra = [k for k in parsed if k not in _REQUIRED_FIELDS]
    for k in extra:
        errors.append(f"Unexpected field not in contract: {k}")

    for f, allowed in _ALLOWED.items():
        if f in parsed and parsed[f] not in allowed:
            errors.append(f"Field '{f}' has invalid value '{parsed[f]}' (allowed: {sorted(allowed)})")

    for f in ("missing_information", "evidence"):
        if f in parsed and not isinstance(parsed[f], list):
            errors.append(f"Field '{f}' must be an array.")

    if "needs_human_review" in parsed and not isinstance(parsed["needs_human_review"], bool):
        errors.append("Field 'needs_human_review' must be a boolean.")

    return ValidationResult(len(errors) == 0, errors, parsed)


def check_characteristics(response_text: str, *, must_contain: list[str] | None = None,
                          must_not_contain: list[str] | None = None) -> ValidationResult:
    """Lightweight free-text validation for non-structured labs (case-insensitive substring checks)."""
    errors: list[str] = []
    hay = (response_text or "").lower()
    for needle in (must_contain or []):
        if needle.lower() not in hay:
            errors.append(f"Expected text not found: {needle!r}")
    for needle in (must_not_contain or []):
        if needle.lower() in hay:
            errors.append(f"Prohibited text present: {needle!r}")
    return ValidationResult(len(errors) == 0, errors, None)


def load_schema(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
