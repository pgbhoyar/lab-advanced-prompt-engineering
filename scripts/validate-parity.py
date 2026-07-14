#!/usr/bin/env python3
"""Cross-track parity / divergence detection.

Ensures the coding tracks do NOT hold their own copies of prompt text, and that shared assets
are referenced from the canonical locations (prompts/, datasets/, schemas/, rubrics/).

Heuristic: no *.md prompt-like file or *.json schema copy should live under apps/. Prompt content
must live only under prompts/. Exit 0 = no divergence, 1 = divergence found.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / "apps"

errors: list[str] = []


def main() -> int:
    if APPS.exists():
        # Flag prompt/schema duplicates checked into language projects.
        for suspicious in list(APPS.rglob("*.manifest.yaml")) + list(APPS.rglob("system.md")) + list(APPS.rglob("user.md")):
            errors.append(f"Prompt asset must not live under apps/: {suspicious.relative_to(ROOT)}")
        for schema in APPS.rglob("*.schema.json"):
            errors.append(f"Schema copy must not live under apps/: {schema.relative_to(ROOT)}")

    # Confirm canonical shared dirs exist.
    for required in ("prompts", "datasets", "schemas", "rubrics"):
        if not (ROOT / required).exists():
            errors.append(f"Missing canonical shared directory: {required}/")

    if errors:
        print("PARITY VALIDATION: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PARITY VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
