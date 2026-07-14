"""CLI entrypoint. Commands: check-config, list-labs, list-cases, run, validate.

Exit codes (see specs/.../contracts/cli-contract.md):
  0 success | 1 usage error | 2 config error | 3 model error | 4 validation failure
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

from .cases import find_case, load_cases
from .client import ModelClient, ModelError
from .config import ConfigError, load_config
from .prompts import PromptError, build_prompt, load_manifest
from .results import save_result
from .validate import load_schema, validate_structured

EXIT_OK, EXIT_USAGE, EXIT_CONFIG, EXIT_MODEL, EXIT_VALIDATION = 0, 1, 2, 3, 4


def repo_root() -> Path:
    override = os.environ.get("WORKSHOP_REPO_ROOT")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[4]


def _iter_manifests(root: Path):
    for mf in sorted((root / "prompts").rglob("*.manifest.yaml")):
        try:
            yield load_manifest(mf)
        except PromptError:
            continue


def _find_manifest(root: Path, lab: str, variant: str):
    for m in _iter_manifests(root):
        if m.lab == lab and m.variant == variant:
            return m
    return None


def cmd_check_config(_args) -> int:
    try:
        cfg = load_config()
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return EXIT_CONFIG
    print("Config OK:", cfg.redacted())
    return EXIT_OK


def cmd_list_labs(_args) -> int:
    root = repo_root()
    labs = sorted({m.lab for m in _iter_manifests(root)})
    if not labs:
        print("No prompt manifests found under prompts/.", file=sys.stderr)
    for lab in labs:
        print(lab)
    return EXIT_OK


def cmd_list_cases(args) -> int:
    root = repo_root()
    manifests = [m for m in _iter_manifests(root) if m.lab == args.lab]
    if not manifests:
        print(f"No manifests for lab '{args.lab}'.", file=sys.stderr)
        return EXIT_USAGE
    test_set = next((m.test_set for m in manifests if m.test_set), None)
    if not test_set:
        print(f"No test_set declared for lab '{args.lab}'.", file=sys.stderr)
        return EXIT_USAGE
    for case in load_cases((manifests[0]._dir / test_set).resolve()):
        print(f"{case.id}\t{case.scenario_type}")
    return EXIT_OK


def cmd_run(args) -> int:
    root = repo_root()
    try:
        cfg = load_config()
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return EXIT_CONFIG

    manifest = _find_manifest(root, args.lab, args.variant)
    if manifest is None:
        print(f"No manifest for lab '{args.lab}' variant '{args.variant}'.", file=sys.stderr)
        return EXIT_USAGE
    if not manifest.test_set:
        print(f"Manifest {manifest.id} has no test_set.", file=sys.stderr)
        return EXIT_USAGE

    try:
        case = find_case((manifest._dir / manifest.test_set).resolve(), args.case)
        prompt = build_prompt(manifest, case.input)
    except (PromptError, Exception) as exc:  # noqa: BLE001
        print(f"Load error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    print(f"Lab={manifest.lab} case={case.id} variant={manifest.variant} prompt={manifest.id}@{manifest.version}")
    if not args.quiet:
        if prompt.system:
            print("\n--- SYSTEM ---\n" + prompt.system)
        print("\n--- USER ---\n" + prompt.user)

    schema = None
    if manifest.output_schema:
        schema = load_schema((manifest._dir / manifest.output_schema).resolve())

    client = ModelClient(cfg)
    started = time.time()
    try:
        resp = client.respond(system=prompt.system, user=prompt.user, output_schema=schema)
    except ModelError as exc:
        print(f"Model error: {exc}", file=sys.stderr)
        return EXIT_MODEL
    duration_ms = int((time.time() - started) * 1000)

    print("\n--- RESPONSE ---\n" + resp.text)

    exit_code = EXIT_OK
    validation = None
    if schema is not None:
        validation = validate_structured(resp.text)
        print("\n" + validation.summary_line())
        for err in validation.errors:
            print(f"  - {err}", file=sys.stderr)
        if not validation.passed:
            exit_code = EXIT_VALIDATION

    if cfg.save_results or args.save:
        from .validate import ValidationResult
        vr = validation or ValidationResult(True, [], None)
        path = save_result(
            cfg, prompt_id=manifest.id, prompt_version=manifest.version, test_case_id=case.id,
            response_text=resp.text, validation=vr, duration_ms=duration_ms,
            input_tokens=resp.input_tokens, output_tokens=resp.output_tokens,
        )
        print(f"\nSaved sanitized result: {path}")

    return exit_code


def cmd_chain(args) -> int:
    root = repo_root()
    try:
        cfg = load_config()
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return EXIT_CONFIG

    stages = sorted(
        (m for m in _iter_manifests(root) if m.lab == args.lab and m.variant == "stage"),
        key=lambda m: m.id,
    )
    if not stages:
        print(f"No stage manifests for lab '{args.lab}'.", file=sys.stderr)
        return EXIT_USAGE

    test_set = next((m.test_set for m in stages if m.test_set), None)
    if not test_set:
        print(f"No test_set declared for lab '{args.lab}' stages.", file=sys.stderr)
        return EXIT_USAGE
    try:
        case = find_case((stages[0]._dir / test_set).resolve(), args.case)
    except Exception as exc:  # noqa: BLE001
        print(f"Load error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    from .chain import run_chain

    client = ModelClient(cfg)

    def respond(system, user):
        return client.respond(system=system, user=user)

    try:
        result = run_chain(stages, case.input, respond)
    except ModelError as exc:
        print(f"Model error: {exc}", file=sys.stderr)
        return EXIT_MODEL

    for s in result.stages:
        status = "PASS" if s.validated else "FAIL"
        print(f"\n--- STAGE {s.stage_id}: {status} ---\n{s.output}")
        for err in s.errors:
            print(f"  - {err}", file=sys.stderr)

    if not result.completed:
        print(f"\nChain stopped at stage: {result.stopped_at}", file=sys.stderr)
        return EXIT_VALIDATION
    print("\nChain completed.")
    return EXIT_OK


def cmd_validate(args) -> int:
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    # Accept either a raw triage JSON or a saved run-result wrapper.
    import json
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "parsed_output" in data:
            text = json.dumps(data["parsed_output"])
    except json.JSONDecodeError:
        pass
    result = validate_structured(text)
    print(result.summary_line())
    for err in result.errors:
        print(f"  - {err}", file=sys.stderr)
    return EXIT_OK if result.passed else EXIT_VALIDATION


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="workshop_runner", description="Advanced Prompt Engineering Workshop runner")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("check-config").set_defaults(func=cmd_check_config)
    sub.add_parser("list-labs").set_defaults(func=cmd_list_labs)

    lc = sub.add_parser("list-cases")
    lc.add_argument("--lab", required=True)
    lc.set_defaults(func=cmd_list_cases)

    run = sub.add_parser("run")
    run.add_argument("--lab", required=True)
    run.add_argument("--case", required=True)
    run.add_argument("--variant", required=True, choices=["baseline", "improved", "stage", "reference"])
    run.add_argument("--save", action="store_true")
    run.add_argument("--quiet", action="store_true", help="Do not print the rendered prompt")
    run.set_defaults(func=cmd_run)

    val = sub.add_parser("validate")
    val.add_argument("--file", default=None)
    val.set_defaults(func=cmd_validate)

    chain = sub.add_parser("chain")
    chain.add_argument("--lab", required=True)
    chain.add_argument("--case", required=True)
    chain.set_defaults(func=cmd_chain)

    return p

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse exits 2 on usage error; normalize to our code 1
        return EXIT_USAGE if exc.code else EXIT_OK
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
