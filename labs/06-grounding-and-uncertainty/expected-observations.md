# Lab 06 — Expected Observations

Judge by characteristics; responses vary.

## Baseline — typical weakness

- Invents a VPN data cap or answers from general knowledge not in the policy.

## Improved — expected characteristics

- `grounding-supported-01`: answers **90 days**, citing policy P1 as evidence.
- `grounding-unsupported-01`: returns exactly
  "The provided information is insufficient to answer this question."
- `grounding-inference-01`: notes the reported four users is below the policy's >10 threshold and
  labels any escalation suggestion as an **Inference:**, not a stated policy fact.
- Never invents numbers, sources, citations, or URLs.

## Teaching point

Groundedness and an explicit uncertainty policy are what make an enterprise assistant
trustworthy. A fluent but ungrounded answer scores **0** on groundedness — fluency does not
compensate.
