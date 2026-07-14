# Lab 07 — Test Cases

Evaluation uses any lab's five scenario types on the **same** inputs. Injection uses
[`datasets/triage/adversarial-cases.jsonl`](../../datasets/triage/adversarial-cases.jsonl):

| Case ID | Scenario type | Focus |
|---------|---------------|-------|
| `adversarial-ignore-01` | adversarial | Direct "ignore instructions" injection |
| `adversarial-reveal-01` | adversarial | Attempt to exfiltrate instructions/keys |
| `adversarial-indirect-01` | adversarial | Indirect injection in forwarded content |
| `adversarial-outofscope-01` | adversarial | Role override / out-of-scope request |

All examples are benign and synthetic (FR-082).
