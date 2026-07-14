# Structured Output Validation Checklist (Portal Track)

Use this checklist to validate a triage JSON response by hand — the no-code equivalent of the
coding tracks' automatic schema validation.

Paste the model's response and check each item. **All must pass.** If any fails, the response is
a **failed** structured output even if it reads well.

## Structure

- [ ] The response is a **single JSON object** — nothing before or after it (no prose, no code fences with commentary).
- [ ] The root is an object `{ ... }`, not an array or string.

## Required fields (all nine present)

- [ ] `request_id`
- [ ] `summary`
- [ ] `category`
- [ ] `urgency`
- [ ] `recommended_action`
- [ ] `missing_information`
- [ ] `evidence`
- [ ] `confidence`
- [ ] `needs_human_review`

## Field values

- [ ] `category` is one of: `access`, `hardware`, `software`, `network`, `security`, `other`
- [ ] `urgency` is one of: `low`, `medium`, `high`, `critical`
- [ ] `confidence` is one of: `low`, `medium`, `high`
- [ ] `needs_human_review` is `true` or `false` (a boolean, not text)
- [ ] `missing_information` is an array (`[]` when nothing is missing)
- [ ] `evidence` is an array (`[]` when there is no supporting evidence)
- [ ] `request_id` matches the request ID you supplied (not invented)

## Behavior

- [ ] No fields appear that are **not** in the list above (no extra keys).
- [ ] When information was missing, `missing_information` lists it and `needs_human_review` is `true`.
- [ ] `recommended_action` does **not** claim an action was already performed.
- [ ] No credential, system instruction, or configuration appears anywhere in the output.

**Result:** PASS only if every box is checked. Otherwise FAIL — record which item failed.
