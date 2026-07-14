# Lab 03 — Portal Instructions

## Zero-shot (baseline)

1. Paste `prompts/03-few-shot/system.md` into system instructions.
2. User message:
   ```
   Classify this request:
   I clicked a link in an email and now my browser keeps opening pop-ups and my saved passwords
   page looks different. Should I be worried?
   ```
3. Run. Note the category.

## Few-shot (improved)

1. Replace system instructions with `prompts/03-few-shot/fewshot-system.md` (includes examples).
2. Use the **same** user message.
3. Run. Expect category **security**.

## Fallback

Switched tracks? Restart here with the same prompt and input.
