# Contributing

Thank you for improving the Advanced Prompt Engineering Workshop.

## Principles

This repository follows the workshop constitution
([.specify/memory/constitution.md](.specify/memory/constitution.md)). All contributions
MUST comply with it. Key rules:

- **Shared assets are the source of truth.** Prompts, datasets, schemas, and rubrics live in
  `prompts/`, `datasets/`, `schemas/`, and `rubrics/`. Do **not** copy prompt content into a
  language project — all tracks load the shared files.
- **Parity.** Portal, Python, C#, and Java tracks must teach the same technique with the same
  scenario, inputs, output contract, test cases, and rubric.
- **No secrets.** Never commit credentials. Use `.env` (ignored) and `.env.example`
  (placeholders only).
- **Synthetic data only.** No real customer, employee, or company data.
- **Evaluation-driven.** Prompt changes must reference a failure mode or evaluation result and
  update the prompt version + change notes.

## Before opening a PR

1. Run the validators: `python scripts/validate-schemas.py`, `python scripts/validate-content.py`,
   `python scripts/validate-parity.py`.
2. Run offline tests for any coding track you changed.
3. Confirm no secret patterns are present.

## Prompt changes

Increment the prompt `version` (semver) and add `change_notes` describing what changed, why,
which failure motivated it, which tests ran, and whether scores improved.
