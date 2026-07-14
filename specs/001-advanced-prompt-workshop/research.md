# Phase 0 Research: Advanced Prompt Engineering Hands-On Workshop

**Feature**: `001-advanced-prompt-workshop` | **Date**: 2026-07-13

Each research item below records a Decision, Rationale, Alternatives considered, Verification evidence (how it will be confirmed), Verification status, and Owner. Items marked **OPEN** must be resolved and confirmed against the live workshop environment before Phase 1 implementation of the affected component is approved. Design decisions that do not depend on the live environment are marked **RESOLVED**.

---

## R-001 — GPT-5.4 Deployment

- **Decision**: Target a single Microsoft Foundry GPT-5.4 deployment addressed by its deployment name (not the model family name), accessed via the Azure OpenAI v1 Responses API with `reasoning_effort` defaulting to `low` and bounded `max_output_tokens`.
- **Rationale**: A single named deployment keeps configuration uniform across all tracks and matches the operational constraint that the deployment name may differ from the model name.
- **Alternatives considered**: Hard-coding a model identifier (rejected — deployment name varies per resource); multiple model families (rejected — increases quota and parity complexity).
- **Verification evidence**: Confirm exact deployment name, region, deployment type, Responses API availability, structured-output support, available quota, valid `reasoning_effort` values, and expected latency against the provisioned resource.
- **Verification status**: OPEN — requires provisioned Foundry resource.
- **Owner**: Workshop technical lead.

## R-002 — SDK Compatibility

- **Decision**: Use the official OpenAI SDKs — `openai` (Python), `OpenAI` (.NET), `com.openai:openai-java` — for the Responses API on Python 3.10+, .NET 8, JDK 17.
- **Rationale**: One current interface across all three languages minimizes divergence and instructional overhead.
- **Alternatives considered**: Community SDKs (rejected — inconsistent maintenance); raw REST (kept only as a troubleshooting reference).
- **Verification evidence**: Execute one minimal Responses API call per language and record the exact tested package versions; pin them after the end-to-end compatibility test.
- **Verification status**: OPEN — pending compatibility run.
- **Owner**: Each track maintainer.

## R-003 — Structured-Output Parity

- **Decision**: Define one shared strict JSON Schema (`triage-output.schema.json`) with all fields required, null-capable types for optional values, and `additionalProperties: false`; enforce it in all three coding tracks and via the portal checklist.
- **Rationale**: Microsoft Foundry structured outputs support a defined JSON Schema subset; a single strict schema guarantees identical contracts across tracks.
- **Alternatives considered**: Per-language schemas (rejected — divergence); free-text "JSON-like" output (rejected — violates constitution Gate 5 and FR-037).
- **Verification evidence**: Verify strict structured output through all three coding paths; where an SDK lacks a convenient typed surface, document the smallest supported protocol-level fallback without changing the shared contract.
- **Verification status**: OPEN — pending per-SDK structured-output test.
- **Owner**: Each track maintainer.

## R-004 — Portal Workflow

- **Decision**: Document the portal path using textual navigation (model selection, system/developer instruction entry, user-input entry, structured-output configuration, output copying, access permissions) with dated screenshots as secondary aids.
- **Rationale**: Portal labels change; text-first instructions age better and satisfy Risk 3 mitigation.
- **Alternatives considered**: Screenshot-only walkthroughs (rejected — brittle to UI changes).
- **Verification evidence**: Verify current portal labels and each step immediately before the workshop; record any changed labels.
- **Verification status**: OPEN — verify near delivery date.
- **Owner**: Portal-track author.

## R-005 — Authentication

- **Decision**: Use temporary API-key authentication for coding exercises, read exclusively from environment variables; document Microsoft Entra ID (managed identity, least privilege, managed secret storage) as the production pattern.
- **Rationale**: Microsoft documents both API-key and Entra ID support for the Responses API and recommends Entra ID; API keys minimize cross-org onboarding friction in a 75-minute session.
- **Alternatives considered**: Entra ID for the live workshop (rejected — tenant/consent friction for transient cross-org attendees); keys in config files (rejected — leakage risk).
- **Verification evidence**: Confirm temporary API-key workflow, env-var setup, key revocation procedure, and the Entra ID production reference.
- **Verification status**: RESOLVED (design) / OPEN (revocation procedure confirmation with the resource owner).
- **Owner**: Workshop organizer.

## R-006 — Quota and Concurrency

- **Decision**: Design for up to 50 concurrent request makers with staggered exercises, short inputs/outputs, and retry-with-jitter; hold a backup GPT-5.4 deployment as contingency.
- **Rationale**: Microsoft recommends retry logic and gradual workload changes to manage Azure OpenAI rate limits; a live cohort can exceed per-deployment throughput.
- **Alternatives considered**: Uncontrolled concurrent runs (rejected — rate-limit failures); no backup deployment (rejected — single point of failure).
- **Verification evidence**: Load-test a controlled number of simultaneous calls to determine safe attendee batch size, call staggering, retry guidance, and whether a second deployment is needed.
- **Verification status**: OPEN — pending load test.
- **Owner**: Workshop technical lead.

## R-007 — Evaluation

- **Decision**: Three-layer evaluation — deterministic validation (all tracks), human rubric (all tracks), and an optional facilitator-only Python AI-assisted runner using Microsoft Foundry evaluators.
- **Rationale**: No single technique is sufficient; deterministic checks catch contract violations while human/AI-assisted evaluation address qualitative behavior. Microsoft Foundry supports built-in and custom evaluators.
- **Alternatives considered**: Human-only evaluation (rejected — misses objective contract failures); AI-only evaluation (rejected — parity and cost concerns, not an attendee learning outcome).
- **Verification evidence**: Verify the deterministic runner, Microsoft Foundry evaluation SDK compatibility, required dataset fields, and cost/latency of AI-assisted evaluation.
- **Verification status**: OPEN — pending evaluator compatibility test.
- **Owner**: Evaluation maintainer.

## R-008 — Cross-Platform Setup

- **Decision**: Provide `setup.ps1` (Windows PowerShell) and `setup.sh` (macOS/Linux) with a configuration checker, minimal dependencies, and a portal fallback for restricted workstations.
- **Rationale**: Attendees run varied OSes and corporate restrictions; setup must not block participation (Risk 6).
- **Alternatives considered**: Single-OS instructions (rejected — excludes attendees); container-only setup (rejected — corporate restrictions may block).
- **Verification evidence**: Test on Windows PowerShell, macOS shell, Linux shell, and under common corporate restrictions.
- **Verification status**: OPEN — pending multi-platform test.
- **Owner**: Setup-script maintainer.

## R-009 — Workshop Timing

- **Decision**: Validate the 75-minute agenda through a rehearsal with one non-coder, one Python attendee, one C#/Java attendee, and one facilitator who did not author the lab.
- **Rationale**: Timing risk (Risk 7) can only be confirmed empirically; the facilitator path must fit the session.
- **Alternatives considered**: Estimating timing without rehearsal (rejected — unreliable for a fixed session length).
- **Verification evidence**: Conduct the rehearsal and record per-segment timings; adjust required vs. take-home scope accordingly.
- **Verification status**: OPEN — pending rehearsal.
- **Owner**: Facilitator.

---

## Resolved Design Decisions (no live-environment dependency)

These are captured in [plan.md](plan.md) Architecture Decisions AD-001 through AD-010 and are **RESOLVED**:

- Content-first repository with shared assets (AD-001)
- Thin CLI applications (AD-002)
- v1 Responses API as the primary interface (AD-003)
- Stateless requests with `store=false` (AD-004)
- Shared prompt manifest format and validation rules (AD-005)
- Simple named-placeholder rendering (AD-006)
- Shared synthetic triage scenario (AD-007)
- Layered evaluation model (AD-008)
- No exact golden-text assertions (AD-009)
- Portal/code parity (AD-010)

## Exit Criteria for Phase 0

All OPEN items (R-001, R-002, R-003, R-004, R-006, R-007, R-008, R-009, and the R-005 revocation confirmation) MUST be verified against the actual workshop environment before the affected component is implemented, and MUST all be resolved before the full package is declared release-ready (Increment 8). Phase 1 design artifacts below do not depend on these confirmations and proceed in parallel.
