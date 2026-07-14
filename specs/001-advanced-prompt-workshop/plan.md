# Implementation Plan: Advanced Prompt Engineering Hands-On Workshop

**Branch**: `001-advanced-prompt-workshop` | **Date**: 2026-07-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-advanced-prompt-workshop/spec.md`

## Summary

Implement a content-first, multi-language workshop package that teaches advanced prompt engineering through a consistent **Enterprise Service Request Triage** scenario. Attendees complete equivalent exercises through four tracks: Microsoft Foundry portal, Python, C#, and Java.

The implementation uses shared prompt assets as the single source of truth, shared synthetic datasets and test cases, shared JSON output contracts, thin language-specific command-line applications, Microsoft Foundry's Azure OpenAI v1 Responses API, stateless requests, deterministic validation plus human evaluation rubrics, optional Microsoft Foundry AI-assisted evaluation for facilitators, environment-based configuration for temporary credentials, and automated content/schema/build/contract/secret-scanning checks. No database, hosted application, custom backend, agent framework, or external tool execution is required.

Priorities: beginner accessibility, track parity, prompt visibility, minimal code, repeatability, credential safety, evaluation-driven prompt development, and reliable delivery within 75 minutes.

## Technical Context

**Language/Version**:
- Content: Markdown, JSON, JSON Lines, YAML, PowerShell + shell setup scripts
- Python 3.10+ (`openai`, `pydantic`, `pytest`, `azure-ai-evaluation`, `azure-identity`)
- C# / .NET SDK 8.0+ (`OpenAI`, `Azure.Identity`, `System.Text.Json`, xUnit)
- Java / JDK 17+ (`com.openai:openai-java`, `com.azure:azure-identity`, Jackson, JUnit 5, Maven Wrapper)
- Portal: Microsoft Foundry portal (no local runtime)

**Primary Dependencies**: Microsoft Foundry GPT-5.4 deployment; Azure OpenAI v1 Responses API; official OpenAI SDKs (Python/.NET/Java); JSON Schema-compatible structured-output contract; Git + GitHub. Dependency versions MUST be pinned in the applicable lockfile/build file after all three coding tracks pass an end-to-end compatibility test.

**Storage**: No database. Repository files store prompt definitions/metadata, synthetic datasets, JSON schemas, rubrics, expected observations, facilitator solutions, and sanitized example outputs. Generated attendee outputs are printed to terminal by default, optionally written to a local Git-ignored directory, and excluded from version control.

**Testing**: Content-completeness, schema-validation, unit, contract, cross-track parity, offline integration (recorded fixtures), opt-in live Microsoft Foundry integration, manual portal validation, end-to-end facilitator rehearsal, and credential/secret scanning.

**Target Platform**: Coding tracks on Windows 10/11, macOS, common desktop Linux; portal track on a current desktop browser supported by Microsoft Foundry; CI on GitHub-hosted runners (Linux primary, Windows smoke tests for setup scripts where practical).

**Project Type**: Content-first multi-language workshop monorepository (workshop docs, prompt assets, synthetic evaluation data, three small CLI reference apps, shared contracts, automated quality checks). Not a production web app; exposes no custom HTTP API.

**Performance Goals**: Local app startup <10s after dependency restore; config validation <2s; one model request per exercise step unless a lab demonstrates chaining; default request timeout 90s; max three retries for retryable failures; output capped to lab need; rerun a changed prompt without rebuilding unrelated components; blocked coding attendee can move to portal within 5 minutes.

**Constraints**:
- Live workshop duration is 75 minutes.
- Temporary API-key auth permitted for coding exercises; production guidance uses Microsoft Entra ID.
- No credential committed to the repository; no real customer/employee data.
- No required portal exercise depends on local software.
- Model deployment name may differ from the model name; model output is nondeterministic.
- Live-model tests must not run automatically on every pull request.
- Workshop must remain usable after temporary credentials expire, and completable if attendees skip coding.
- GPT-5.4 reasoning-model unsupported sampling parameters (`temperature`, `top_p`, `presence_penalty`, `frequency_penalty`) MUST be omitted, not tuned.

**Scale/Scope**: Up to 60 attendees; up to 50 concurrent request makers per exercise window; ~5–10 model calls per attendee live, plus facilitator/demo calls; package supports independent post-workshop use. Capacity MUST be validated against the actual deployment quota before the workshop.

## Architecture Decisions

- **AD-001 — Content-First Repository**: Prompt files, datasets, schemas, and rubrics are the authoritative assets; language apps load them at runtime. Prevents track divergence. Rejected: per-project prompt duplication (divergence risk); doc generation tooling (unneeded complexity for v1).
- **AD-002 — Thin CLI Applications**: Each coding track provides a small CLI that validates config, loads a prompt/test case, renders variables, submits, displays, validates structured output, and optionally saves a sanitized result. Rejected: web app, shared backend, agent framework (all add scope unrelated to learning).
- **AD-003 — Microsoft Foundry v1 Responses API**: Coding tracks use the Azure OpenAI v1 Responses API through official SDKs; base URL `https://<resource-name>.openai.azure.com/openai/v1/`; configured model value is the deployment name. Rejected as primary: Chat Completions (kept as reference), raw REST only (kept as troubleshooting reference).
- **AD-004 — Stateless Requests**: Core requests use `store=false`; chaining passes validated stage output explicitly rather than server-side state. Improves reproducibility and fair comparison. Rejected: `previous_response_id` chaining for required labs.
- **AD-005 — Shared Prompt Manifest**: Every reusable prompt has a YAML manifest + one or more Markdown prompt files, with validation rules (unique ID, semver, referenced files exist, declared==used variables, no credentials, schema for structured prompts, test set for production variants, change notes on version change).
- **AD-006 — Simple Prompt Rendering**: Named placeholders (`{{request_text}}`); renderer rejects missing/undeclared variables, preserves text exactly, no expression execution or template logic.
- **AD-007 — Shared Synthetic Scenario**: All labs use Enterprise Service Request Triage with a consistent entity set (service request, requester details, service policy, category, urgency, recommended action, missing information, evidence, human-review decision).
- **AD-008 — Layered Evaluation**: Layer 1 deterministic validation, Layer 2 human rubric, Layer 3 optional AI-assisted evaluation (facilitator-only Python runner using Microsoft Foundry evaluators).
- **AD-009 — No Exact Golden-Text Assertions**: Tests validate required characteristics; exact assertions only for JSON field names, enum values, required fallback phrases, static schema rules, fixed identifiers.
- **AD-010 — Portal and Code Parity**: Portal and coding tracks share system instructions, user prompt, input data, output contract, test cases, rubric, and expected observations.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Gate | Status | Evidence |
|---|------|--------|----------|
| 1 | Accessible Dual-Path Learning | PASS | Every required lab includes `portal.md` and a common `README.md`; code tracks use shared assets; coding failure has portal fallback; advanced challenges separated from required steps. |
| 2 | Progressive Learning (one concept per lab) | PASS | Lab progression isolates one primary concept: access/baseline → contract → hierarchy/delimiters → few-shot → structured output → chaining → grounding → evaluation/injection → capstone. |
| 3 | Explicit Prompt Contracts | PASS | Prompt manifests + templates require objective, input, constraints, output, and uncertainty behavior. |
| 4 | Responsible Advanced Techniques | PASS | Demonstrates decomposition, concise rationale, evidence, verification without requesting hidden chain-of-thought (FR-049). |
| 5 | Structured Output Validation | PASS | Shared JSON schemas + track-specific parsers enforce the same contract; `additionalProperties:false`. |
| 6 | Evaluation Before Optimization | PASS | Each revised prompt references a test set and rubric; baseline and improved prompts use identical inputs. |
| 7 | Grounding & Uncertainty | PASS | Grounding labs include source-authority rules, insufficient-evidence fallback, conflicting-source handling. |
| 8 | Security & Privacy | PASS (documented workshop exception) | Temporary API keys used for simple onboarding; env vars only, no committed secrets, controlled distribution, synthetic data, local-only config, secret scanning, post-workshop rotation, Entra ID documented as production pattern. See Complexity Tracking. |
| 9 | Reproducibility & Versioning | PASS | Prompt manifests include IDs, versions, model settings, schemas, datasets, change notes. |
| 10 | Workshop Definition of Done | PASS | Automated content checks + facilitator rehearsal validate constitutional requirements. |

All ten gates pass. The single exception (temporary API-key authentication) is documented in Complexity Tracking with compensating controls.

## Project Structure

### Documentation (this feature)

```text
specs/001-advanced-prompt-workshop/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── prompt-manifest.schema.json
│   ├── triage-output.schema.json
│   ├── test-case.schema.json
│   ├── evaluation-result.schema.json
│   ├── cli-contract.md
│   └── portal-parity-contract.md
└── tasks.md             # /speckit.tasks output (NOT created here)
```

### Source Code (repository root)

```text
.
├── .github/workflows/            # content-quality, build-and-test, secret-scan, live-integration
├── .specify/                     # constitution, scripts, templates
├── specs/001-advanced-prompt-workshop/
├── docs/                         # overview, setup, portal-setup, credential-safety, troubleshooting,
│                                 #   facilitator-guide, timing-guide, post-workshop-next-steps
├── labs/                         # 00-access-and-baseline … 08-capstone
├── prompts/                      # 00-baseline … 08-capstone-reference (manifests + prompt md)
├── datasets/triage/              # starter/core/edge/adversarial cases (.jsonl) + policy-context.md
├── schemas/                      # prompt-manifest, triage-output, test-case, evaluation-result
├── rubrics/                      # standard-rubric(.md/.json), structured-output-checklist, capstone-rubric
├── apps/
│   ├── python/                   # pyproject.toml, requirements.lock, src/workshop_runner/, tests/
│   ├── csharp/                   # WorkshopRunner.sln, src/WorkshopRunner/, tests/WorkshopRunner.Tests/
│   └── java/                     # pom.xml, mvnw/mvnw.cmd, src/main/java, src/test/java
├── evaluation/                   # facilitator/ (run_evaluation.py, evaluators/), expected-observations/, sample-results/
├── solutions/                    # facilitator/, attendee-reference/
├── scripts/                      # setup.ps1/.sh, validate-content.py, validate-parity.py, validate-schemas.py, sanitize-results.py
├── offline-fallback/             # baseline-output.md, improved-output.md, evaluation-exercise.md
├── generated-results/.gitkeep    # Git-ignored runtime outputs
├── .env.example, .gitignore, .gitattributes
├── SECURITY.md, CONTRIBUTING.md, LICENSE, README.md
```

**Structure Decision**: A monorepository is selected because all tracks must share prompts, datasets, schemas, and workshop documentation. Language projects remain independent build units but load common assets from repository-root directories. Only API connection, response extraction, and local validation are language-specific.

> Note: The constitution's *recommended* repository organization uses an advisory `01`–`10` lab numbering and lists evaluation and prompt-injection as separate labs. This plan adopts a `00`–`08` numbering with a combined Lab 07 (evaluation + injection); the constitution layout is explicitly advisory ("SHOULD", "MAY be removed").

## Implementation Sequence (Increments)

1. **Repository Foundation** — directory structure, constitution/spec references, shared config contract, shared schemas, synthetic starter dataset, content validation scripts, CI foundations, security files.
2. **Portal + Python Vertical Slice** — Lab 00, Lab 01, portal instructions, Python runner, shared prompt manifest, one test case, offline tests, one live integration test (validates architecture before duplicating adapters).
3. **C# + Java Parity** — C# and Java runners, shared contract tests, cross-track parity checks, platform setup docs.
4. **Core Workshop Labs** — instruction hierarchy, few-shot, structured output; portal + coding paths; rubrics; troubleshooting.
5. **Advanced Labs** — prompt chaining, grounding/uncertainty, prompt-injection testing, advanced test data, facilitator demonstrations.
6. **Evaluation System** — deterministic evaluator, human rubric workflow, optional Foundry evaluation runner, comparison reports, pre-workshop consistency suite.
7. **Capstone + Facilitation** — capstone, reference solution, facilitator guide, timing guide, offline fallback, credential operations guide.
8. **Release Readiness** — full rehearsal, quota validation, cross-platform checks, portal review, secret scan, accessibility review, link validation, backup deployment test, release tag.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because | Control |
|-----------|------------|--------------------------------------|---------|
| Multi-language duplication (Python/C#/Java runners) | Three coding tracks are an explicit workshop requirement | A single language would exclude required attendee audiences | Only API connection, response extraction, and local validation are language-specific; prompts, schemas, datasets, rubrics remain shared and parity-tested |
| Temporary API-key authentication | Attendees span unrelated organizations/devices and need simple onboarding within a 75-minute session (Gate 8 exception) | Entra ID onboarding for transient cross-org attendees adds tenant/consent friction that would consume session time | Short-lived credentials, env vars only, synthetic data, controlled distribution, secret scanning, immediate post-workshop rotation; Entra ID documented as production pattern |
| Python-only AI-assisted evaluator | AI-assisted evaluation is facilitator tooling, not an attendee learning outcome | Reimplementing evaluator tooling in all three languages adds maintenance with no learning benefit | All attendee tracks use the same deterministic checks + human rubric; Python automation creates no separate learning outcome |
| Full package larger than live agenda | Repository supports both the 75-minute live meeting and take-home learning | Trimming to only live content removes required completed-package deliverables | Required live path clearly identified; advanced material marked as demonstration/optional/take-home |

## Post-Design Constitution Re-Check

After Phase 1 artifacts (`research.md`, `data-model.md`, `contracts/`, `quickstart.md`) were generated, all ten gates were re-evaluated and continue to PASS. The shared contracts (prompt manifest, triage output, test case, evaluation result) enforce structured-output validation (Gate 5), reproducibility/versioning (Gate 9), and explicit prompt contracts (Gate 3) at schema level. The CLI and portal-parity contracts document Gate 1 accessibility and Gate 10 parity. No new violations were introduced; the temporary API-key exception remains the only tracked deviation.
