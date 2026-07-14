# Lab 04 — Expected Observations

Judge by characteristics; wording varies but the **structure** must be exact.

## Baseline — typical weaknesses

- Prose before/after the JSON ("Here is the triage: { ... } Hope this helps!").
- Field names differ from the contract (e.g. `priority` instead of `urgency`).
- Values outside the allowed set (e.g. `urgency: "urgent"`).
- Missing fields (no `needs_human_review`, no `evidence`).

## Improved — expected characteristics

- A single JSON object, nothing outside it.
- All nine fields present: `request_id, summary, category, urgency, recommended_action,
  missing_information, evidence, confidence, needs_human_review`.
- `category`, `urgency`, `confidence` use only allowed enum values.
- `normal-01`: category `hardware`, `request_id` = `SR-1001`, empty `missing_information` (or a
  minor item), `needs_human_review` likely `false`.
- `missing-information-01`: non-empty `missing_information`, `needs_human_review: true`.

## Teaching point

A fluent, confident response that breaks the schema is a **failed** structured output. The runner
scores it exit code 4 / `VALIDATION: FAIL`; the portal checklist marks it FAIL.
