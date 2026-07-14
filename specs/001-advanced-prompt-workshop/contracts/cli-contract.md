# CLI Contract

**Feature**: `001-advanced-prompt-workshop` | **Applies to**: Python, C#, and Java runners

All three coding-track runners MUST expose the same command surface, argument names, exit codes, and console-output semantics. Language-specific differences are limited to the invocation prefix (e.g. `python -m workshop_runner`, `dotnet run --`, `java -jar workshop-runner.jar` or `./mvnw -q exec:java`).

## Commands

| Command | Purpose |
|---------|---------|
| `check-config` | Validate environment configuration without contacting the model. |
| `list-labs` | List available lab identifiers. |
| `list-cases --lab <lab-id>` | List test-case identifiers for a lab. |
| `run --lab <lab-id> --case <case-id> --variant <variant>` | Render the prompt for the case, submit one request, display the response, and validate structured output when applicable. |
| `validate --file <result-file>` | Validate a saved result file (or piped JSON) against the applicable schema without contacting the model. |

## Arguments

- `--lab <lab-id>`: Lab identifier matching a directory under `labs/` (e.g. `04-structured-output`). Required for `run`, `list-cases`.
- `--case <case-id>`: Test-case identifier from the lab's test set. Required for `run`.
- `--variant <variant>`: One of `baseline`, `improved`, `stage`, `reference`. Required for `run`. Defaults are not assumed.
- `--file <path>`: Path to a result JSON file for `validate`. When omitted, read JSON from standard input.
- `--save` (optional flag): Persist a sanitized result to the results directory (equivalent to `WORKSHOP_SAVE_RESULTS=true` for this invocation).

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success. For `run`, a response was received and (if applicable) passed structured-output validation. |
| `1` | Usage error (unknown command, missing/invalid argument). |
| `2` | Configuration error (missing/invalid env var, non-HTTPS base URL, base URL not ending in `/openai/v1/`, blank deployment, placeholder API key, invalid numeric setting). |
| `3` | Model/request error after retries (authentication failure, invalid request, content-filter rejection, invalid deployment, timeout, transient failures exhausted). |
| `4` | Validation failure (response received but structured output failed schema/contract validation, or `validate` found errors). |

## Console-Output Expectations

- `run` prints, in order: resolved lab/case/variant identifiers, the rendered prompt sections (system, user, delimited input) when a `--show-prompt` style verbosity is enabled by default for teaching, the model response, and a validation summary line.
- Validation summary uses a stable prefix: `VALIDATION: PASS` or `VALIDATION: FAIL` followed by an error list.
- Errors are written to standard error; primary output to standard output.
- No credential value is ever printed. Known secret patterns are redacted in all output.
- Output is capped to the amount required by the lab.

## Error Semantics

- Configuration problems fail before any request is sent, with a message explaining how to fix the problem (without printing the credential).
- Retryable failures (HTTP 429/408/500/502/503/504, transient network) are retried up to three attempts total: attempt 1 immediate, attempt 2 exponential delay with jitter, attempt 3 larger exponential delay with jitter; service-provided retry headers are respected.
- Non-retryable failures (authentication, invalid request, content-filter, invalid deployment, schema-definition errors) are reported immediately without retry.

## Parity Requirement

Cross-track parity tests assert that all three runners: load the same prompt files, datasets, and schema; accept equivalent arguments; produce equivalent pass/fail validation semantics; and use identical exit codes for equivalent conditions. No language project may contain a divergent copy of a shared prompt.
