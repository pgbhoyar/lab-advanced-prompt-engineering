# Troubleshooting

Common setup, authentication, dependency, rate-limit, schema, and output problems.

## Setup & configuration

| Symptom | Fix |
|---------|-----|
| `Missing required environment variable(s)` | Copy `.env.example` to `.env` and fill the three required values. Run `scripts/setup.ps1` / `setup.sh`. |
| `BASE_URL must use https://` | Ensure the endpoint starts with `https://`. |
| `BASE_URL must end in /openai/v1/` | Append `/openai/v1/` to the resource endpoint. |
| `... still contains a placeholder` | You pasted the `<...>` placeholder; paste the real key. |
| `No module named workshop_runner` | `python -m pip install -e apps/python` from the repo root. |

## Authentication

| Symptom | Fix |
|---------|-----|
| `Authentication failed` (401/403) | Key is wrong or expired. Re-copy it (watch for trailing spaces). Keys may be rotated after the workshop. |
| `Deployment not found` (404) | `AZURE_OPENAI_DEPLOYMENT` must be the **deployment name**, which may differ from "GPT-5.4". |

## Dependencies / runtime

| Symptom | Fix |
|---------|-----|
| Cannot install packages / corporate restrictions | Use the **portal** track — every required lab works with no local code. |
| Wrong Python/.NET/JDK version | Python 3.10+, .NET 8+, JDK 17+. If unavailable, use the portal. |

## Rate limits & slow responses

| Symptom | Fix |
|---------|-----|
| `429` / rate limited | The runner retries with backoff. Wait a moment; the facilitator may stagger exercises. |
| Very slow response | Reasoning effort is already `low` and tokens are bounded. Use the facilitator's pre-run example or the `offline-fallback/` pack. |

## Structured output / schema

| Symptom | Fix |
|---------|-----|
| `VALIDATION: FAIL — Unexpected field` | The model added a key not in the contract. Rely on schema-enforced mode or tighten the instruction. |
| `VALIDATION: FAIL — invalid value` | An enum value is out of range (e.g. `urgency: urgent`). |
| Portal has no schema option | Request the schema in the prompt and validate with `rubrics/structured-output-checklist.md`. |

## Output variance

Model responses vary between runs. Judge by required **characteristics**, not exact text. When
assessing consistency, run more than once and record variation rather than keeping only the best
result.

## Switching tracks

If a coding track breaks, switch to the portal at the **same lab number** using the same prompt
and input (see [pre-workshop-setup.md](pre-workshop-setup.md) §4). Target: under five minutes.
