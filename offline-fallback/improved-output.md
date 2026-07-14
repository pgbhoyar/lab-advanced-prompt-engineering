# Offline Fallback — Improved Response Sample (Lab 04 Structured Output)

Use if the network/model is unavailable. Sanitized, synthetic example of a **schema-valid**
structured triage for `normal-01`. Actual responses vary but must match the schema.

## Input (SR-1001)

> My work laptop is about 5 years old and the battery now lasts only 20 minutes. I have to stay
> plugged in all day. Can I get a replacement? - Priya, Finance

## Example improved (strict schema) response

```json
{
  "request_id": "SR-1001",
  "summary": "A ~5-year-old work laptop has poor battery life (about 20 minutes) and must stay plugged in.",
  "category": "hardware",
  "urgency": "medium",
  "recommended_action": "Verify device age and battery health, then process a laptop replacement per the 4-year policy.",
  "missing_information": [],
  "evidence": ["Laptop is about 5 years old", "Battery lasts only ~20 minutes"],
  "confidence": "high",
  "needs_human_review": false
}
```

## Why it passes

Single JSON object, all nine fields, valid enums, arrays for the list fields, no extra keys, no
secrets, `request_id` echoed. Contrast with the baseline "reply in JSON" which often adds prose or
a `priority` field — a **failed** structured output.
