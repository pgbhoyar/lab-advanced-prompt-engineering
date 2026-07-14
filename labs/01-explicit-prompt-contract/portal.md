# Lab 01 — Portal Instructions

## Baseline

1. In the playground for the workshop deployment, clear system instructions.
2. Paste the baseline user message with `normal-01` substituted:

   ```
   Please triage this support request and make it better.

   My work laptop is about 5 years old and the battery now lasts only 20 minutes. I have to
   stay plugged in all day. Can I get a replacement? - Priya, Finance
   ```
3. Run once. Note the weaknesses.

## Improved

1. Paste the contents of `prompts/01-explicit-contract/system.md` into the **system /
   developer instructions** field.
2. In the user message, paste:

   ```
   Triage the following service request according to your instructions.

   Service request:
   My work laptop is about 5 years old and the battery now lasts only 20 minutes. I have to
   stay plugged in all day. Can I get a replacement? - Priya, Finance
   ```
3. Run once with the **same** input as the baseline.

## Compare

Score both with the [standard rubric](../../rubrics/standard-rubric.md). The improved response
should follow the labeled output structure and stay under 150 words.

## Fallback

Switched from a coding track? Restart this lab here using the same prompt and input. See
[../../docs/pre-workshop-setup.md](../../docs/pre-workshop-setup.md).
