# Workshop Datasets

All data in this directory is **synthetic** and created for teaching. It contains no real
customer, employee, or company information, and no personally identifiable information.

## Files

- `policy-context.md` — a fictional IT service policy used as the authoritative grounding source
  (Lab 06).
- `starter-cases.jsonl` — one normal request for Lab 00.
- `core-test-cases.jsonl` — the five core scenario types (normal, ambiguous, missing-information,
  edge, conflicting) used across Labs 01–07.
- `edge-cases.jsonl` — additional edge, irrelevant, and grounding cases.
- `adversarial-cases.jsonl` — benign, synthetic prompt-injection and out-of-scope cases (Labs 02, 07).

## Format

Each `.jsonl` file has one JSON object per line conforming to
[`schemas/test-case.schema.json`](../schemas/test-case.schema.json). Validate with:

```
python scripts/validate-schemas.py
```

## Safety

Do not add real data. Do not add harmful prompt-injection payloads — injection examples must
remain benign and demonstrate defensive behavior only.
