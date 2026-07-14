"""Secret redaction helpers shared across output paths."""
from __future__ import annotations

import re

# Patterns that look like keys/tokens. Conservative; aims to avoid ever printing a secret.
_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{16,}", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9]{32,}"),  # long opaque strings (e.g. API keys)
]


def redact(text: str, extra: list[str] | None = None) -> str:
    """Return text with known secret patterns and any provided literals masked."""
    if text is None:
        return text
    result = text
    for literal in (extra or []):
        if literal:
            result = result.replace(literal, "***redacted***")
    for pattern in _PATTERNS:
        result = pattern.sub("***redacted***", result)
    return result
