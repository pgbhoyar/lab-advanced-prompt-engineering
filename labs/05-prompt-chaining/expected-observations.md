# Lab 05 — Expected Observations

Judge by characteristics; responses vary.

## Single prompt — typical weaknesses

- One or more of the four sub-tasks is thin, missing, or blended into another.
- On the long/noisy `edge-long-01`, irrelevant details (coffee machine, desk moves) may leak in.
- Hard to tell which step failed.

## Chain — expected characteristics

- **Stage 1** returns a clean JSON object of extracted facts; irrelevant noise is dropped.
- If Stage 1 output is not valid JSON, the chain **stops** and reports it (no garbage into Stage 2).
- **Stage 2** classifies/recommends using only the validated facts.
- Each stage is independently inspectable and testable.

## Teaching point

Decomposition improves observability and maintainability. The trade-off is more calls and more
moving parts — worth it when reliability and traceability matter.
