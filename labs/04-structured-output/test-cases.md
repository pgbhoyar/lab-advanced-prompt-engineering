# Lab 04 — Test Cases

From [`datasets/triage/core-test-cases.jsonl`](../../datasets/triage/core-test-cases.jsonl):

| Case ID | Scenario type | Focus |
|---------|---------------|-------|
| `normal-01` | normal | All fields, valid enums |
| `missing-information-01` | missing-information | Non-empty `missing_information`, `needs_human_review: true` |
| `conflicting-01` | conflicting | Policy urgency overrides reporter opinion |

Coding tracks validate automatically; portal track uses the manual checklist.
