#!/usr/bin/env python3
"""Strip secret-looking patterns from saved result files before sharing.

Usage: python scripts/sanitize-results.py [path-or-dir]
Rewrites files in place (they are Git-ignored). Exit 0 always unless a path is invalid.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{16,}", re.I),
    re.compile(r"\"api_key\"\s*:\s*\"[^\"]+\""),
    re.compile(r"[A-Za-z0-9]{40,}"),
]


def sanitize_text(text: str) -> str:
    for pat in PATTERNS:
        text = pat.sub("***redacted***", text)
    return text


def main(argv: list[str]) -> int:
    target = Path(argv[1]) if len(argv) > 1 else (ROOT / "generated-results")
    if not target.exists():
        print(f"Path not found: {target}", file=sys.stderr)
        return 1
    files = [target] if target.is_file() else list(target.rglob("*.json"))
    for f in files:
        original = f.read_text(encoding="utf-8")
        cleaned = sanitize_text(original)
        if cleaned != original:
            f.write_text(cleaned, encoding="utf-8")
            print(f"sanitized: {f}")
    print(f"Done. Scanned {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
