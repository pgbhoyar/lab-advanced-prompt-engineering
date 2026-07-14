# Lab 02 — Test Cases

From [`datasets/triage/adversarial-cases.jsonl`](../../datasets/triage/adversarial-cases.jsonl):

| Case ID | Scenario type | Focus |
|---------|---------------|-------|
| `adversarial-ignore-01` | adversarial | Direct "ignore instructions" injection |
| `adversarial-indirect-01` | adversarial | Indirect injection inside forwarded content |
| `adversarial-reveal-01` | adversarial | Attempt to exfiltrate system instructions/keys |

Run baseline and improved on the **same** case to compare.
