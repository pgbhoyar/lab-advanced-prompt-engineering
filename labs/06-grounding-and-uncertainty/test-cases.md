# Lab 06 — Test Cases

From [`datasets/triage/edge-cases.jsonl`](../../datasets/triage/edge-cases.jsonl):

| Case ID | Scenario type | Focus |
|---------|---------------|-------|
| `grounding-supported-01` | normal | Answer supported by policy (90 days) |
| `grounding-unsupported-01` | missing-information | Requires the insufficient-information fallback |
| `grounding-inference-01` | edge-case | Distinguish inference from stated policy |

Run baseline and improved on the **same** case to compare.
