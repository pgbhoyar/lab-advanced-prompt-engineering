# Portal Parity Contract

**Feature**: `001-advanced-prompt-workshop`

This contract maps every automated coding action to the equivalent Microsoft Foundry portal action so that portal and coding tracks teach identical behavior (constitution Gate 1, Gate 10; FR-088 through FR-097). Both tracks use the same system instructions, user prompt, input data, output contract, test cases, rubric, and expected observations.

## Action Mapping

| # | Coding-track action (CLI) | Portal-track equivalent |
|---|---------------------------|-------------------------|
| 1 | `check-config` validates env vars and base URL | Attendee confirms they are in the correct Foundry project and have the target deployment selected |
| 2 | Loader reads the shared system prompt (`system.md`) | Attendee pastes the same system/developer instructions into the portal system-instruction field |
| 3 | Loader renders the user prompt with case variables | Attendee pastes the rendered user prompt into the user-input field |
| 4 | Delimited source data injected into the prompt | Attendee pastes source data inside the same delimiters shown in the lab |
| 5 | Model client sets deployment, `reasoning_effort`, `max_output_tokens`, `store=false` | Attendee selects the same deployment and configures equivalent output settings; response storage left off |
| 6 | Structured-output schema applied | Attendee enables the portal structured-output/JSON-schema option using the shared schema, or requests the schema in-prompt where schema entry is unavailable |
| 7 | Runner submits one request | Attendee runs the prompt once |
| 8 | Response validator checks JSON parse, required fields, enums, no extra fields, null/empty-list behavior | Attendee applies the manual structured-output checklist (`rubrics/structured-output-checklist.md`) |
| 9 | Result recorder saves sanitized result (when enabled) | Attendee copies the output into the lab worksheet |
| 10 | Exit code / `VALIDATION: PASS`/`FAIL` | Checklist pass/fail outcome |

## Equivalence Rules

- The same test-case inputs (`datasets/triage/*.jsonl`) are used in both tracks.
- The same rubric (`rubrics/standard-rubric.md`) scores both tracks.
- Portal instructions may describe manual steps; coding tracks automate loading and validation, but the observed behavior and pass/fail outcome MUST match.
- When a portal capability is unavailable (e.g. strict schema entry), the lab documents the smallest in-prompt fallback without changing the shared output contract.

## Fallback Continuity

A blocked coding attendee resumes at the same lab number, with the same prompt and input data, on the portal track within five minutes (SC-002). No portal step requires locally installed software (FR-003, operational constraints).
