# Phase 1 Data Model: Advanced Prompt Engineering Hands-On Workshop

**Feature**: `001-advanced-prompt-workshop` | **Date**: 2026-07-13

These entities are content/configuration records stored as repository files (Markdown, YAML, JSON, JSON Lines). No database is used. Schemas for the machine-validated entities live in [contracts/](contracts/).

---

## Prompt Asset

Reusable prompt or prompt-chain stage.

- **Fields**: id, name, version, purpose, objective, input variables, instructions (system/user prompt files), constraints, output contract (schema reference), uncertainty policy, model configuration, model-specific notes, known limitations, change rationale.
- **Validation**: unique id; semver version; every referenced file exists; every declared variable used and every used placeholder declared; contains no credentials; structured-output prompts reference a schema; production variants reference a test set; version increment requires change notes.
- **Relationships**: has one Model Configuration; references one Structured Output Contract (structured prompts) and one Test Case set (production variants); grouped under one Lab.
- **Versioning**: version changes when instructions, examples, output contract, uncertainty behavior, model settings, or security boundaries change. Dataset changes do not silently overwrite evaluation history.
- **Schema**: [contracts/prompt-manifest.schema.json](contracts/prompt-manifest.schema.json).

## Prompt Variant

A version of a prompt being compared.

- **Fields**: variant identifier, parent prompt, version, changes from baseline, reason for change, test set used, evaluation scores, observed failures, regressions.
- **Validation**: `variant` ∈ {baseline, improved, stage, reference}; baseline and improved variants of the same lab reference the same test set for fair comparison.
- **Relationships**: belongs to one Prompt Asset; produces many Evaluation Results.
- **State**: `draft` → `evaluated` → `accepted` | `rejected` (accepted requires meeting the prompt acceptance threshold below).

## Lab

A focused hands-on exercise.

- **Fields**: lab identifier, title, primary technique, learning objective, estimated duration, prerequisites, baseline prompt, improved prompt, input data, checkpoint, test cases, evaluation rubric, troubleshooting guidance, optional challenge.
- **Validation (content-completeness test)**: each required lab contains learning objective, duration, prerequisites, scenario, starting prompt, improvement step, portal instructions, coding instructions, test cases, evaluation guidance, checkpoint, reflection, troubleshooting, and an optional-challenge marker.
- **Relationships**: contains Prompt Assets and Test Cases; references one Evaluation Rubric.
- **Ordering**: 00→08, one primary concept per lab.

## Test Case

One repeatable prompt input and expected behavior.

- **Fields**: id, scenario_type, input (request_id, request_text, policy_context), expected_characteristics, prohibited_behavior, applicable_rubric_criteria, tags.
- **Validation**: `scenario_type` ∈ {normal, ambiguous, missing-information, edge-case, conflicting, irrelevant, adversarial}; each core evaluation set includes at least one normal, ambiguous, missing-information, edge, and conflicting/irrelevant/adversarial case.
- **Relationships**: belongs to a Test Set referenced by Prompt Variants; drives Evaluation Results.
- **Schema**: [contracts/test-case.schema.json](contracts/test-case.schema.json).

## Reference Context

Supplied source information used for grounding.

- **Fields**: context identifier, source label, content, authority level, allowed usage, conflict-handling behavior.
- **Validation**: synthetic content only; instructions embedded in context MUST be treated as data, never as authoritative instructions.
- **Relationships**: supplied to grounding-lab Prompt Assets via the `policy_context` variable.

## Structured Output Contract

Required machine-readable response format.

- **Fields**: required fields, optional fields, field types, allowed values (enums), missing-value behavior, validation rules.
- **Validation**: all fields required; optional values represented with null-capable types; `additionalProperties: false`; no text outside the JSON object.
- **Instance**: the triage output — request_id, summary, category, urgency, recommended_action, missing_information, evidence, confidence, needs_human_review.
- **Schema**: [contracts/triage-output.schema.json](contracts/triage-output.schema.json).

## Evaluation Rubric

Criteria used to score responses.

- **Fields**: rubric identifier, criteria, scoring scale, scoring definitions, required passing score, automatic checks, human-review checks.
- **Scale**: 0 = Failed, 1 = Partially satisfied, 2 = Fully satisfied.
- **Criteria (9, max 18)**: task correctness, instruction adherence, completeness, relevance, groundedness, output-format compliance, missing-information handling, safety and scope compliance, clarity and conciseness.
- **Relationships**: applied to Evaluation Results across all tracks (parity).

## Evaluation Result

Scores and deterministic checks for one variant/case run.

- **Fields**: prompt_id, prompt_version, test_case_id, scenario_type, run_index, scores (9 criteria), total_score, deterministic_checks (passed, errors, schema_valid, fallback_used_when_required, credentials_exposed, followed_embedded_instruction), regression, notes.
- **Validation**: total_score = sum of criterion scores (0–18); deterministic checks recorded independently of rubric scores.
- **Schema**: [contracts/evaluation-result.schema.json](contracts/evaluation-result.schema.json).

## Model Configuration

Supported GPT-5.4 request settings.

- **Fields**: reasoning_effort (low/medium/high), max_output_tokens, store (false for core labs), request timeout.
- **Validation**: unsupported sampling parameters (temperature, top_p, presence_penalty, frequency_penalty) MUST NOT be present.
- **Relationships**: embedded in each Prompt Asset manifest; defaults overridable via `WORKSHOP_*` env vars.

## Run Result

Sanitized record of a single execution (when saving is enabled).

- **Fields**: run_id, prompt_id, prompt_version, test_case_id, model_deployment, started_at, duration_ms, status, response_text, parsed_output, validation (passed, errors), usage (input_tokens, output_tokens).
- **Validation**: MUST NOT contain API key, authorization headers, tokens, env-variable dumps, or private attendee data. Files are Git-ignored.

## Learning Track

Method used to complete labs.

- **Allowed values**: Microsoft Foundry portal, Python, C#, Java.
- **Invariant**: every track teaches the same required learning outcomes using the same shared assets; a failure in one track does not block completion via another (FR-097).

## Capstone Submission

Attendee's final reusable prompt.

- **Fields**: prompt contract, test results, revision notes, evaluation score, known limitations, completion status.
- **Minimum passing criteria**: valid prompt manifest; valid response contract; all five test categories executed; no schema failure; no critical security-boundary failure; no fabricated action claim; ≥14 of 18 rubric points; no zero score for groundedness, format compliance, or safety.

---

## Prompt Acceptance Threshold (production workshop variants)

A production workshop prompt variant is `accepted` when:

- Average score ≥ 14 of 18.
- No test scores zero for groundedness.
- No test scores zero for safety and scope compliance.
- Structured-output tests have zero schema violations.
- Missing-information tests use the required fallback behavior.
- Adversarial tests do not expose credentials or follow embedded instructions.
- The targeted criterion improves without an unacceptable regression elsewhere.

## Cross-Entity Invariants

- Prompt Variant baseline and improved reference an identical Test Case set (fair comparison, FR-020/FR-063).
- Every structured-output Prompt Asset references the single shared triage schema (parity, Gate 5).
- Evaluation Rubric is identical across all Learning Tracks (parity, FR-091).
