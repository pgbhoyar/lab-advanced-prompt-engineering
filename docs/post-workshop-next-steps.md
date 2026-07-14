# Post-Workshop Next Steps

The temporary workshop keys will be rotated or revoked, but everything in this repository stays
usable — you only need model access to make live calls.

## Finish what you started

- Complete the **capstone** ([labs/08-capstone](../labs/08-capstone/README.md)) using the
  reference prompt, capstone test set, and [capstone rubric](../rubrics/capstone-rubric.md).
- Try the labs you skipped live: **05 chaining**, **06 grounding**, **07 evaluation & injection**.

## Reuse the pattern in your own work

- Treat prompts as versioned assets: manifest + system/user text + test set + rubric + change notes.
- Keep prompt content separate from application code (see the thin runners in `apps/`).
- Validate structured output programmatically; keep a small five-category test set.

## Take it to production (beyond this workshop)

- Replace API keys with **Microsoft Entra ID** (managed identity), least privilege, and managed
  secret storage.
- Add application-level safeguards on top of prompt design: input validation, output validation,
  human confirmation for consequential actions, and content-safety / prompt-protection tooling.
- Add evaluation to CI: deterministic checks on every change, plus periodic human/AI-assisted
  review.

## Where to look

- Techniques and rules: [.specify/memory/constitution.md](../.specify/memory/constitution.md)
- Shared assets: `prompts/`, `datasets/`, `schemas/`, `rubrics/`
- Evaluation tooling: `evaluation/facilitator/`
