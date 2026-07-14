# Lab 08 — Portal Instructions

## Build your capstone prompt

1. Paste `prompts/08-capstone-reference/system.md` into the **system instructions** field (or
   write your own combining: strict schema, grounding, `<source_data>` separation, uncertainty
   policy). If the portal supports structured output, attach
   [`schemas/triage-output.schema.json`](../../schemas/triage-output.schema.json).
2. For each capstone case, paste the user message:
   ```
   Request ID: CAP-001

   <policy>
   (paste the case policy_context)
   </policy>

   <source_data>
   (paste the case request_text)
   </source_data>
   ```

## Test

Run all four capstone cases (`cap-normal-01`, `cap-ambiguous-01`, `cap-missing-01`,
`cap-adversarial-01`) and add one edge case of your own.

## Validate & score

- Use the [structured-output checklist](../../rubrics/structured-output-checklist.md) for each
  response.
- Score with the [capstone rubric](../../rubrics/capstone-rubric.md).

## Fallback

Switched tracks? Restart here with the same prompt and inputs.
