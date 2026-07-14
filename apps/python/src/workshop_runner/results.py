"""Sanitized result recorder. Never writes secrets or private data. Files are Git-ignored."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import Config
from .redact import redact
from .validate import ValidationResult


def save_result(config: Config, *, prompt_id: str, prompt_version: str, test_case_id: str,
                response_text: str, validation: ValidationResult, duration_ms: int,
                input_tokens: int | None, output_tokens: int | None) -> Path:
    """Write a sanitized run result and return its path."""
    out_dir = Path(config.results_directory)
    out_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "run_id": str(uuid.uuid4()),
        "prompt_id": prompt_id,
        "prompt_version": prompt_version,
        "test_case_id": test_case_id,
        "model_deployment": config.deployment,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "duration_ms": duration_ms,
        "status": "success" if validation.passed else "validation_failed",
        "response_text": redact(response_text, extra=[config.api_key]),
        "parsed_output": validation.parsed if validation.parsed is not None else {},
        "validation": {"passed": validation.passed, "errors": validation.errors},
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
    }

    path = out_dir / f"{prompt_id}__{test_case_id}__{record['run_id'][:8]}.json"
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return path
