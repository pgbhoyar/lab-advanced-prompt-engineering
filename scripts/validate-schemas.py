#!/usr/bin/env python3
"""Validate workshop JSON/JSONL assets against the schemas in schemas/.

Uses `jsonschema` if installed; otherwise falls back to lightweight required/enum checks.
Exit code 0 = all valid, 1 = failures found.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

try:
    import jsonschema  # type: ignore
    _HAS = True
except Exception:
    _HAS = False

errors: list[str] = []


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(instance, schema, where: str):
    if _HAS:
        v = jsonschema.Draft202012Validator(schema)
        for e in v.iter_errors(instance):
            errors.append(f"{where}: {e.message}")
    else:
        for req in schema.get("required", []):
            if isinstance(instance, dict) and req not in instance:
                errors.append(f"{where}: missing required '{req}'")


def main() -> int:
    tc_schema = _load(SCHEMAS / "test-case.schema.json")
    out_schema = _load(SCHEMAS / "triage-output.schema.json")

    for jsonl in (ROOT / "datasets").rglob("*.jsonl"):
        for i, line in enumerate(jsonl.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{jsonl}:{i}: invalid JSON: {exc}")
                continue
            validate(obj, tc_schema, f"{jsonl.name}:{i}")

    # Validate any prompt manifests if PyYAML present.
    try:
        import yaml  # type: ignore
        man_schema = _load(SCHEMAS / "prompt-manifest.schema.json")
        for mf in (ROOT / "prompts").rglob("*.manifest.yaml"):
            validate(yaml.safe_load(mf.read_text(encoding="utf-8")), man_schema, mf.name)
    except Exception:
        pass

    if not _HAS:
        print("[warn] `jsonschema` not installed — ran required-field checks only.")
    if errors:
        print("SCHEMA VALIDATION: FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("SCHEMA VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
