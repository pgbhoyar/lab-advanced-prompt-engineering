"""Test-case (.jsonl) loading."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


class CaseError(Exception):
    """Raised for test-case loading problems."""


@dataclass
class TestCase:
    id: str
    scenario_type: str
    input: dict
    expected_characteristics: list[str]
    prohibited_behavior: list[str]
    applicable_rubric_criteria: list[str]
    tags: list[str]

    @classmethod
    def from_dict(cls, d: dict) -> "TestCase":
        return cls(
            id=d["id"], scenario_type=d["scenario_type"], input=dict(d["input"]),
            expected_characteristics=list(d.get("expected_characteristics", [])),
            prohibited_behavior=list(d.get("prohibited_behavior", [])),
            applicable_rubric_criteria=list(d.get("applicable_rubric_criteria", [])),
            tags=list(d.get("tags", [])),
        )


def load_cases(path: str | Path) -> list[TestCase]:
    p = Path(path)
    if not p.exists():
        raise CaseError(f"Test set not found: {p}")
    cases: list[TestCase] = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            cases.append(TestCase.from_dict(json.loads(line)))
        except json.JSONDecodeError as exc:
            raise CaseError(f"Invalid JSON on line {i} of {p}: {exc}") from exc
    return cases


def find_case(path: str | Path, case_id: str) -> TestCase:
    for case in load_cases(path):
        if case.id == case_id:
            return case
    raise CaseError(f"Test case '{case_id}' not found in {path}")
