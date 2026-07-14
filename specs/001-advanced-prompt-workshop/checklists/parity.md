# Cross-Track Parity & Accessibility Requirements Checklist: Advanced Prompt Engineering Hands-On Workshop

**Purpose**: Validate the quality (completeness, clarity, consistency, measurability, coverage) of the requirements governing dual-path accessibility and Portal/Python/C#/Java parity — before implementation.
**Created**: 2026-07-13
**Feature**: [spec.md](../spec.md)
**Audience & Timing**: Reviewer / facilitator — PR review and pre-delivery gate
**Depth**: Standard review gate

> This checklist tests whether the *requirements are well written* — not whether the workshop works. Each item asks whether a parity/accessibility requirement is complete, clear, consistent, and measurable.

## Requirement Completeness

- [ ] CHK001 Are requirements defined for every track (Portal, Python, C#, Java) at each required lab, rather than only for the coding tracks collectively? [Completeness, Spec §FR-002, §FR-003]
- [ ] CHK002 Is a requirement present that specifies what "equivalent" means across tracks in observable terms (same scenario, prompt, input, output contract, evaluation)? [Completeness, Spec §FR-088–§FR-092]
- [ ] CHK003 Are requirements defined for the track-switch/resume behavior (which lab, prompt, and input an attendee resumes with) beyond stating that resumption is possible? [Completeness, Spec §FR-012]
- [ ] CHK004 Is the portal fallback requirement specified for *every* coding lab, and is a way to confirm coverage across all labs documented? [Completeness, Spec §FR-010, §FR-107]
- [ ] CHK005 Are requirements defined for what constitutes a "completion checkpoint" consistently enough to apply identically on all four tracks? [Completeness, Spec §FR-009]
- [ ] CHK006 Are requirements present for how unfamiliar technical terms are introduced identically across portal and coding instructions? [Completeness, Spec §FR-005]
- [ ] CHK007 Is there a requirement covering equivalence of expected-observation content between portal and coding tracks (not just prompts and inputs)? [Gap, Spec §FR-014]
- [ ] CHK008 Are requirements defined for the manual portal validation checklist as the parity equivalent of programmatic validation? [Completeness, Spec §FR-073, contracts/portal-parity-contract.md]

## Requirement Clarity

- [ ] CHK009 Is "the same prompt-engineering technique" quantified or defined so reviewers can objectively confirm portal and coding paths teach it? [Clarity, Spec §FR-004]
- [ ] CHK010 Is "plain language and short, numbered steps" specified with observable criteria (e.g., step granularity, term-explanation trigger) rather than left subjective? [Ambiguity, Spec §FR-006]
- [ ] CHK011 Is "equivalent prompt content" (§FR-089) distinguished clearly from "the same prompt content," so reviewers know whether wording may differ between tracks? [Ambiguity, Spec §FR-089]
- [ ] CHK012 Is the boundary of "language-specific differences ... limited to what is necessary to connect to and invoke the model" defined precisely enough to adjudicate a disputed difference? [Clarity, Spec §FR-093]
- [ ] CHK013 Is "prompt text easy to locate and modify" expressed with checkable criteria rather than as a subjective quality? [Ambiguity, Spec §FR-094]
- [ ] CHK014 Is "only the complexity required to demonstrate the lab" defined with an observable test a reviewer can apply to each code sample? [Ambiguity, Spec §FR-095]
- [ ] CHK015 Is the phrase "resume at the current lab after switching tracks" clarified as to whether prior in-lab progress is preserved or the lab restarts? [Clarity, Spec §FR-012]

## Requirement Consistency

- [ ] CHK016 Do the accessibility requirements (§FR-001–§FR-014) and parity requirements (§FR-088–§FR-097) use consistent track terminology matching the Learning Track entity's allowed values? [Consistency, Spec §FR-002, Key Entities: Learning Track]
- [ ] CHK017 Are the "same core test inputs" (§FR-090) and "same evaluation rubric" (§FR-091) requirements consistent with the evaluation requirements that also mandate identical comparison inputs (§FR-063)? [Consistency, Spec §FR-090, §FR-091, §FR-063]
- [ ] CHK018 Is the portal no-code requirement (§FR-003) consistent with any requirement that could implicitly assume local tooling in a "required" lab? [Consistency, Spec §FR-003, §FR-010]
- [ ] CHK019 Do the CLI contract command/argument requirements align with the spec's parity requirements without introducing track-specific behavior the spec forbids? [Consistency, contracts/cli-contract.md, Spec §FR-093]
- [ ] CHK020 Are the portal-parity action mappings consistent with the requirement that all tracks target the same required output behavior? [Consistency, contracts/portal-parity-contract.md, Spec §FR-092]
- [ ] CHK021 Is "required learning MUST NOT depend on an optional challenge" (§FR-011) consistent across all track descriptions and the facilitator required/optional labeling (§FR-100)? [Consistency, Spec §FR-011, §FR-100]

## Measurability & Acceptance Criteria

- [ ] CHK022 Can parity be objectively verified — is there a requirement establishing an evidence mechanism (e.g., shared-asset loading, parity checks) rather than only asserting parity? [Measurability, Spec §FR-089–§FR-091, plan.md AD-001]
- [ ] CHK023 Is the five-minute track-switch expectation (SC-002) traceable to a requirement that makes the switch procedure observable and timeable? [Measurability, Spec §SC-002, §FR-010]
- [ ] CHK024 Are the parity success criteria (SC-015) expressed so a reviewer can confirm "same core prompts, test cases, and evaluation criteria" against concrete artifacts? [Measurability, Spec §SC-015]
- [ ] CHK025 Do accessibility outcome targets (e.g., SC-001, SC-018) map to per-lab requirements a reviewer can check rather than aggregate-only metrics? [Measurability, Spec §SC-001, §SC-018]

## Scenario & Edge-Case Coverage

- [ ] CHK026 Are requirements defined for the case where an entire cohort is switched from code to the portal mid-session (not just an individual attendee)? [Coverage, Edge Case, Spec Edge Cases; §FR-097]
- [ ] CHK027 Are requirements defined for a coding attendee whose runtime/SDK is unavailable, specifying continuation without loss of lab position? [Coverage, Spec Edge Cases, §FR-010, §FR-012]
- [ ] CHK028 Are requirements defined for how portal-label drift or stale screenshots are handled so portal instructions remain usable? [Coverage, Gap, Spec Edge Cases]
- [ ] CHK029 Is there a requirement addressing divergence detection — how the workshop prevents one track from silently holding a different prompt/schema/dataset copy? [Coverage, Gap, plan.md §11.6; Spec §FR-089]

## Dependencies, Assumptions & Traceability

- [ ] CHK030 Is the assumption that "the same underlying prompt concepts apply across all supported tracks" validated or flagged, given it underpins all parity requirements? [Assumption, Spec Assumptions]
- [ ] CHK031 Are cross-track parity requirements traceable to at least one measurable success criterion, and each accessibility requirement to a verification method? [Traceability, Spec §FR-088–§FR-097, §SC-015]

## Notes

- Check items off as validated: `[x]`. A checked item means the *requirement* is complete/clear/consistent/measurable — not that the feature is built.
- Record findings inline (e.g., cite the ambiguous phrase or the missing requirement).
- `[Gap]` items indicate a requirement that appears missing from spec/plan/contracts and may need to be added before implementation.
- Focus scope: Cross-track parity & accessibility only. Other dimensions (evaluation, security, structured-output, content/facilitation) are out of scope for this checklist and may be generated separately.
