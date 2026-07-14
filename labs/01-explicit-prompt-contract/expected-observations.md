# Lab 01 — Expected Observations

Judge by *characteristics*, not exact wording. Responses vary between runs.

## Baseline (vague) — typical weaknesses

- Interprets "better" inconsistently (rewrites the message, or replies conversationally).
- No fixed category/urgency vocabulary.
- No structured output; missing-information handling undefined.

## Improved (explicit contract) — expected characteristics

- Uses the labeled output structure (Summary / Category / Urgency / Recommended action /
  Missing information / Needs human review).
- Category from the allowed set; urgency reflects impact.
- On `normal-01` (5-year-old laptop): category **hardware**, a concrete next action, low/medium
  urgency, "Needs human review: no" (or yes if it notes a missing detail).
- On `missing-information-01`: lists what is missing and sets "Needs human review: yes".

## Rubric expectation

Improved should score higher on instruction adherence, completeness, and output-format
compliance while remaining grounded (no invented policy or IDs).
