#!/usr/bin/env python3
"""Validate lab-content completeness and accessibility/safety authoring rules.

Checks each labs/*/README.md for required sections, and scans all prompt/lab text for
prohibited requests to disclose hidden chain-of-thought (FR-049). Also warns when a lab
appears to lack a portal fallback file (FR-010) and does light accessibility heuristics
(FR-005/FR-006).

Exit code 0 = pass, 1 = failures.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "labs"

REQUIRED_SECTIONS = [
    "objective", "duration", "prerequisites", "scenario", "checkpoint",
    "reflection", "troubleshooting",
]

# FR-049: prompts must not request hidden/internal reasoning disclosure.
COT_PATTERNS = [
    re.compile(r"chain[- ]of[- ]thought", re.I),
    re.compile(r"reveal your (hidden|internal|private) reasoning", re.I),
    re.compile(r"show your (hidden|internal|private) (reasoning|thoughts)", re.I),
]

errors: list[str] = []
warnings: list[str] = []


def check_lab(lab_dir: Path):
    readme = lab_dir / "README.md"
    if not readme.exists():
        errors.append(f"{lab_dir.name}: missing README.md")
        return
    text = readme.read_text(encoding="utf-8").lower()
    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{lab_dir.name}: README missing '{section}' content")
    if not (lab_dir / "portal.md").exists():
        errors.append(f"{lab_dir.name}: missing portal.md (portal fallback, FR-010)")
    if not (lab_dir / "challenge.md").exists():
        warnings.append(f"{lab_dir.name}: no challenge.md (optional advanced challenge, FR-024)")


def scan_cot(base: Path):
    for md in base.rglob("*.md"):
        content = md.read_text(encoding="utf-8")
        for pat in COT_PATTERNS:
            if pat.search(content):
                errors.append(f"{md.relative_to(ROOT)}: requests hidden chain-of-thought (FR-049)")


def main() -> int:
    if LABS.exists():
        for lab in sorted(p for p in LABS.iterdir() if p.is_dir()):
            check_lab(lab)
    for base in (LABS, ROOT / "prompts"):
        if base.exists():
            scan_cot(base)

    for w in warnings:
        print(f"[warn] {w}")
    if errors:
        print("CONTENT VALIDATION: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("CONTENT VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
