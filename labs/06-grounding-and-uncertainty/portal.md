# Lab 06 — Portal Instructions

## Baseline

1. Clear system instructions.
2. User message:
   ```
   Policy: (paste the relevant lines from datasets/triage/policy-context.md)

   Question: What is the VPN data cap per month?

   Answer the question.
   ```
3. Run. Note whether it invents a data cap.

## Improved

1. Paste `prompts/06-grounded-answer/system.md` into system instructions.
2. User message:
   ```
   <policy>
   (paste the relevant policy lines)
   </policy>

   Question: What is the VPN data cap per month?
   ```
3. Run. Expect the fallback:
   "The provided information is insufficient to answer this question."

## Try the supported and inference cases

- Supported: "How long can I keep access to a shared mailbox before I need to re-request it?"
  (policy P1 → 90 days).
- Inference: a four-user shared-drive problem vs the policy's ">10 users" threshold — the model
  should label any escalation as an inference.

## Fallback

Switched tracks? Restart here with the same prompt and input.
