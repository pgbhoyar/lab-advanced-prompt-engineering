# Lab 05 — Portal Instructions

You will run two stages by hand, validating between them.

## Stage 1 — Extract (validate before continuing)

1. System instructions: paste `prompts/05-prompt-chain/stage1-system.md`.
2. User message:
   ```
   Request:
   (paste the edge-long-01 request text from datasets/triage/edge-cases.jsonl)
   ```
3. Run. **Validate**: is the output a single JSON object with the four keys? If not, **stop** —
   fix the prompt or input rather than continuing.

## Stage 2 — Classify & recommend

1. Replace system instructions with `prompts/05-prompt-chain/stage2-system.md`.
2. User message:
   ```
   Extracted facts (validated JSON from stage 1):
   (paste ONLY the validated JSON from Stage 1)
   ```
3. Run.

## Compare

Now run the single baseline prompt (`prompts/05-prompt-chain/system.md`) on the same request and
compare quality, traceability, and how easy each is to debug.

## Fallback

Switched tracks? Restart here; copy only validated Stage 1 output into Stage 2.
