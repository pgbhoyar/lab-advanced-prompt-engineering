"""Prompt-chain orchestration.

Runs stage manifests in order. Each stage's raw text output is validated (as JSON by default)
before being passed to the next stage as the ``previous_output`` variable. A failed intermediate
validation STOPS the chain rather than silently continuing.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

from .prompts import PromptManifest, build_prompt


@dataclass
class StageResult:
    stage_id: str
    output: str
    validated: bool
    errors: list[str] = field(default_factory=list)


@dataclass
class ChainResult:
    stages: list[StageResult]
    completed: bool

    @property
    def stopped_at(self) -> str | None:
        for s in self.stages:
            if not s.validated:
                return s.stage_id
        return None


def _is_json_object(text: str) -> tuple[bool, list[str]]:
    try:
        data = json.loads(text.strip())
    except json.JSONDecodeError as exc:
        return False, [f"stage output is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return False, ["stage output JSON root must be an object"]
    return True, []


def run_chain(stages: list[PromptManifest], initial_values: dict, respond,
              validate_stage=None) -> ChainResult:
    """Execute stages sequentially.

    ``respond(system, user)`` returns a response object with a ``.text`` attribute (injectable for
    offline tests). ``validate_stage(index, text)`` returns (ok, errors); defaults to JSON-object
    validation for every stage except the last.
    """
    results: list[StageResult] = []
    values = dict(initial_values)

    for i, manifest in enumerate(stages):
        prompt = build_prompt(manifest, values)
        resp = respond(system=prompt.system, user=prompt.user)
        text = getattr(resp, "text", str(resp))

        is_last = i == len(stages) - 1
        if validate_stage is not None:
            ok, errors = validate_stage(i, text)
        elif not is_last:
            ok, errors = _is_json_object(text)
        else:
            ok, errors = True, []

        results.append(StageResult(stage_id=manifest.id, output=text, validated=ok, errors=errors))
        if not ok:
            return ChainResult(stages=results, completed=False)

        values["previous_output"] = text

    return ChainResult(stages=results, completed=True)
