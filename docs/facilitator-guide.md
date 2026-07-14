# Facilitator Guide

End-to-end guide for delivering the 75-minute workshop. A facilitator who did not author the labs
should be able to run the session from this document (SC-019).

## Before the session

- [ ] Provision the GPT-5.4 Foundry deployment; confirm quota (see [timing-guide.md](timing-guide.md)
      and research R-001/R-006).
- [ ] Prepare temporary keys and the controlled distribution channel
      ([credential-safety.md](credential-safety.md)).
- [ ] Rehearse end-to-end (one non-coder, one Python, one C#/Java, one non-author facilitator).
- [ ] Pre-run each improved prompt so you have live examples if the network is slow.
- [ ] Have the offline fallback pack ready (`offline-fallback/`).

## Required vs optional labs

| Lab | Status in a 75-min session |
|-----|----------------------------|
| 00 Access & Baseline | Required |
| 01 Explicit Contract | Required |
| 02 Instruction Hierarchy | Required |
| 03 Few-Shot | Required |
| 04 Structured Output | Required |
| 05 Chaining | Demo / take-home |
| 06 Grounding | Demo / take-home |
| 07 Evaluation & Injection | Demo (short) + take-home |
| 08 Capstone | Intro + take-home |

See [timing-guide.md](timing-guide.md) for the minute-by-minute agenda and the accelerated/
take-home paths.

## Per-segment structure

For each lab: state the **objective**, show the **baseline weakness** (demo cue), introduce the
**one technique**, run the **improved** prompt on the same input, and confirm the **checkpoint**
before moving on. Expected observations are in each lab's `expected-observations.md`.

## Managing different speeds

- Slower attendees: point to the reference prompt (`prompts/.../improved*`) and the portal
  fallback so they can catch up without blocking.
- Faster attendees: the optional `challenge.md` in each lab.
- Whole-group code failure: switch everyone to the portal at the same lab number
  ([pre-workshop-setup.md](pre-workshop-setup.md) §4).

## Common questions

- *"My deployment name isn't GPT-5.4."* Correct — use the exact deployment name you were given.
- *"Can I use my own data?"* No — synthetic only; never paste confidential/personal data.
- *"The model gave a different answer than the example."* Expected. Judge by characteristics, not
  exact text (AD-009).
- *"Why did the injection sometimes work?"* Prompt wording is one layer; that is the Lab 07 lesson.

## Troubleshooting & recovery

See [troubleshooting.md](troubleshooting.md) for setup, authentication, dependency, rate-limit,
schema, and output problems. If model access fails entirely, run the segment from the
`offline-fallback/` pack and the pre-run examples.

## Contingency (quota / availability / network)

- Stagger exercises so not all attendees call at once; keep inputs/outputs short (low reasoning
  effort, bounded tokens).
- Keep a **backup** GPT-5.4 deployment configured (R-006). Switch by changing the shared
  `AZURE_OPENAI_*` values.
- If the network is down, use the offline fallback pack and demonstrate from your pre-runs.

## Credentials: distribution and revocation

- Distribute keys only through the controlled channel; never in slides or chat.
- After the session, **rotate or revoke** all temporary keys within the defined window (SC-024).
  Confirm revocation with the resource owner.
