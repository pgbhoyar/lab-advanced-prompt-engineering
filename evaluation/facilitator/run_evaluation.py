#!/usr/bin/env python3
"""Facilitator evaluation runner (deterministic Layer 1, plus optional AI-assisted Layer 3).

Runs a prompt variant across its test set, records deterministic checks per case, and writes
sanitized evaluation-result records. AI-assisted evaluation via `azure-ai-evaluation` is optional
and only used when the package is installed and --ai is passed.

Usage:
    python evaluation/facilitator/run_evaluation.py --lab 04-structured-output --variant improved
    python evaluation/facilitator/run_evaluation.py --lab 04-structured-output --variant improved --runs 3

This is FACILITATOR tooling. It is not part of any attendee learning track.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps" / "python" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from workshop_runner.cases import load_cases  # noqa: E402
from workshop_runner.client import ModelClient, ModelError  # noqa: E402
from workshop_runner.config import ConfigError, load_config  # noqa: E402
from workshop_runner.prompts import build_prompt, load_manifest  # noqa: E402
from workshop_runner.validate import load_schema  # noqa: E402
from deterministic_eval import evaluate_response  # noqa: E402


def _find_manifest(lab: str, variant: str):
    for mf in sorted((ROOT / "prompts").rglob("*.manifest.yaml")):
        m = load_manifest(mf)
        if m.lab == lab and m.variant == variant:
            return m
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab", required=True)
    ap.add_argument("--variant", default="improved")
    ap.add_argument("--runs", type=int, default=1, help="Repeat each case N times (consistency).")
    ap.add_argument("--out", default=str(ROOT / "generated-results" / "evaluation.jsonl"))
    args = ap.parse_args()

    manifest = _find_manifest(args.lab, args.variant)
    if manifest is None:
        print(f"No manifest for lab '{args.lab}' variant '{args.variant}'.", file=sys.stderr)
        return 1
    try:
        cfg = load_config()
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 2

    cases = load_cases((manifest._dir / manifest.test_set).resolve())
    schema = load_schema((manifest._dir / manifest.output_schema).resolve()) if manifest.output_schema else None
    client = ModelClient(cfg)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    records = []

    for case in cases:
        for run_index in range(1, args.runs + 1):
            prompt = build_prompt(manifest, case.input)
            try:
                resp = client.respond(system=prompt.system, user=prompt.user, output_schema=schema)
            except ModelError as exc:
                print(f"[{case.id} run {run_index}] model error: {exc}", file=sys.stderr)
                continue
            checks = evaluate_response(
                resp.text,
                scenario_type=case.scenario_type,
                structured=schema is not None,
                requires_fallback=(case.scenario_type == "missing-information"),
            )
            record = {
                "prompt_id": manifest.id,
                "prompt_version": manifest.version,
                "test_case_id": case.id,
                "scenario_type": case.scenario_type,
                "run_index": run_index,
                "deterministic_checks": checks,
            }
            records.append(record)
            status = "PASS" if checks["passed"] else "FAIL"
            print(f"{case.id} run {run_index}: {status}")

    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"\nWrote {len(records)} evaluation record(s) to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
