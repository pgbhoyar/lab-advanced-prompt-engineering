# Facilitator Solutions

**Do not distribute to attendees before they attempt the labs.** These solutions live in a
separate directory to avoid accidental disclosure (FR-126).

## Reference prompts

The canonical "improved"/"reference" prompt for each lab already lives under `prompts/` as the
source of truth. Facilitators can demonstrate them directly:

| Lab | Reference prompt |
|-----|------------------|
| 01 | `prompts/01-explicit-contract/improved.manifest.yaml` |
| 02 | `prompts/02-instruction-hierarchy/improved.manifest.yaml` |
| 03 | `prompts/03-few-shot/fewshot.manifest.yaml` |
| 04 | `prompts/04-structured-output/improved.manifest.yaml` |
| 05 | `prompts/05-prompt-chain/stage*.manifest.yaml` |
| 06 | `prompts/06-grounded-answer/improved.manifest.yaml` |
| 07 | `prompts/07-defensive-prompt/defensive.manifest.yaml` |
| 08 | `prompts/08-capstone-reference/reference.manifest.yaml` |

## Capstone reference

`prompts/08-capstone-reference/` is a complete, passing capstone. Use it to show a model answer
after attendees have attempted their own. It combines explicit contract, instruction/data
separation, strict structured output, grounding + fallback, and injection-resistant scope rules.

## Expected deterministic outcomes

See `evaluation/expected-observations/README.md` and `evaluation/sample-results/`.
