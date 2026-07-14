# Lab 04 — Portal Instructions

## Baseline (loose JSON)

1. System instructions: `Triage the request and reply in JSON with the summary, category,
   urgency, and what to do next.`
2. User message:
   ```
   Request ID: SR-1001
   Service request:
   My work laptop is about 5 years old and the battery now lasts only 20 minutes. I have to stay
   plugged in all day. Can I get a replacement? - Priya, Finance
   ```
3. Run. Note any prose around the JSON, wrong field names, or invalid values.

## Improved (strict schema)

1. If the portal exposes a **structured output / JSON schema** option, enable it and paste the
   contents of [`schemas/triage-output.schema.json`](../../schemas/triage-output.schema.json).
   If it does not, paste `prompts/04-structured-output/strict-system.md` into system instructions
   (it describes the exact contract).
2. Use the **same** user message.
3. Run once.

## Validate (manual checklist)

Work through [`rubrics/structured-output-checklist.md`](../../rubrics/structured-output-checklist.md).
The response is a **PASS** only if every box is checked (single JSON object, all nine fields,
valid enums, arrays for the list fields, no extra keys, no secrets).

## Fallback

Switched tracks? Restart here with the same prompt and input.
