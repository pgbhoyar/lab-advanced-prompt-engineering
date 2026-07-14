# Lab 04 — Challenge (Optional)

> Optional. Does not block later labs.

1. Feed the runner a deliberately broken response via `validate`:
   ```
   echo '{"category":"urgent"}' | python -m workshop_runner validate
   ```
   Observe the specific validation errors and exit code 4.
2. Add `confidence` reasoning: ask the model to set `confidence: low` whenever
   `needs_human_review` is true. Re-run `ambiguous-01` and check consistency.
