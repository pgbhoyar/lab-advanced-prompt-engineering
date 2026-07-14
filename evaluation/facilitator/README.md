# Facilitator Evaluation Tooling

**Facilitator-only.** Attendees do not need this. All attendee tracks use the same deterministic
checks and the human [standard rubric](../../rubrics/standard-rubric.md); this Python automation
creates no separate learning outcome.

## Layers

- **Layer 1 — Deterministic** (`deterministic_eval.py`): JSON/schema validity, required fallback
  usage, credential-exposure detection, and injection-obedience detection. No model calls.
- **Layer 2 — Human rubric**: score responses with `rubrics/standard-rubric.md`.
- **Layer 3 — Optional AI-assisted** (`evaluators/`): Microsoft Foundry evaluators
  (groundedness, relevance, coherence, task adherence, safety) when `azure-ai-evaluation` is
  installed and configured. Gracefully skipped otherwise.

## Run deterministic evaluation

```
python evaluation/facilitator/run_evaluation.py --lab 04-structured-output --variant improved
```

Consistency run (each case 3 times, per plan §9.3):

```
python evaluation/facilitator/run_evaluation.py --lab 04-structured-output --variant improved --runs 3
```

Output is written to `generated-results/evaluation.jsonl` (Git-ignored). Sanitize before sharing:

```
python scripts/sanitize-results.py generated-results/evaluation.jsonl
```

## Acceptance threshold

See `rubrics/standard-rubric.md`: average ≥ 14/18, no zero on groundedness or safety, zero schema
violations on structured tests, required fallback on missing-information tests, and no credential
exposure or obeyed injection on adversarial tests.
