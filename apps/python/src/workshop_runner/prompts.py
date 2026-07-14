"""Prompt manifest loading and simple, safe variable rendering.

The renderer uses named ``{{placeholders}}`` only. It rejects missing and undeclared variables,
preserves source text exactly, and never evaluates expressions.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

try:  # PyYAML is a common transitive dependency; fall back to a tiny parser if absent.
    import yaml  # type: ignore
    _HAS_YAML = True
except Exception:  # pragma: no cover - exercised only when PyYAML missing
    _HAS_YAML = False

_PLACEHOLDER = re.compile(r"\{\{\s*([a-z0-9_]+)\s*\}\}")


class PromptError(Exception):
    """Raised for manifest/render problems."""


@dataclass
class PromptManifest:
    id: str
    version: str
    lab: str
    variant: str
    purpose: str
    user_prompt: str
    variables: list[str]
    model: dict
    system_prompt: str | None = None
    output_schema: str | None = None
    test_set: str | None = None
    known_limitations: list[str] = field(default_factory=list)
    change_notes: str | None = None
    _dir: Path = field(default=Path("."), repr=False)


def _load_yaml(text: str) -> dict:
    if _HAS_YAML:
        return yaml.safe_load(text)
    raise PromptError("PyYAML is required to parse prompt manifests. Install it with `pip install pyyaml`.")


def load_manifest(path: str | Path) -> PromptManifest:
    p = Path(path)
    if not p.exists():
        raise PromptError(f"Manifest not found: {p}")
    data = _load_yaml(p.read_text(encoding="utf-8"))
    required = ["id", "version", "lab", "variant", "purpose", "user_prompt", "variables", "model"]
    missing = [k for k in required if k not in data]
    if missing:
        raise PromptError(f"Manifest {p} missing keys: {', '.join(missing)}")
    return PromptManifest(
        id=data["id"], version=data["version"], lab=data["lab"], variant=data["variant"],
        purpose=data["purpose"], user_prompt=data["user_prompt"], variables=list(data["variables"]),
        model=dict(data["model"]), system_prompt=data.get("system_prompt"),
        output_schema=data.get("output_schema"), test_set=data.get("test_set"),
        known_limitations=list(data.get("known_limitations", [])),
        change_notes=data.get("change_notes"), _dir=p.parent,
    )


def _read(dir_: Path, rel: str) -> str:
    fp = (dir_ / rel).resolve()
    if not fp.exists():
        raise PromptError(f"Referenced prompt file not found: {fp}")
    return fp.read_text(encoding="utf-8")


def render(template: str, values: dict, declared: list[str]) -> str:
    """Render ``{{var}}`` placeholders. Reject undeclared and missing variables."""
    used = set(_PLACEHOLDER.findall(template))
    undeclared = used - set(declared)
    if undeclared:
        raise PromptError(f"Prompt uses undeclared variable(s): {', '.join(sorted(undeclared))}")

    def sub(match: re.Match) -> str:
        name = match.group(1)
        if name not in values:
            raise PromptError(f"Missing value for variable: {name}")
        return str(values[name])

    return _PLACEHOLDER.sub(sub, template)


@dataclass
class RenderedPrompt:
    system: str | None
    user: str


def build_prompt(manifest: PromptManifest, values: dict) -> RenderedPrompt:
    """Load prompt files and render them with the supplied values."""
    system_text = None
    if manifest.system_prompt:
        system_text = _read(manifest._dir, manifest.system_prompt)
        system_text = render(system_text, values, manifest.variables)
    user_text = render(_read(manifest._dir, manifest.user_prompt), values, manifest.variables)
    return RenderedPrompt(system=system_text, user=user_text)
