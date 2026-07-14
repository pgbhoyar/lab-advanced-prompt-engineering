# Hands-On: Advanced Prompt Engineering

A hands-on workshop that teaches how to design, test, evaluate, and improve prompts as
**version-controlled engineering assets** — using OpenAI GPT-5.4 in Microsoft Foundry.

Every required lab can be completed through **four equivalent tracks**:

1. **Microsoft Foundry portal** (no coding)
2. **Python**
3. **C#**
4. **Java**

All tracks share the same scenario, prompts, inputs, output contract, test cases, and rubric.

> **👉 Easiest way to follow the labs:** open the browsable site — [site/index.html](site/index.html) —
> in your web browser. It's a click-through experience with a lab landing page, badges, a table of
> contents, Python/C#/Java code tabs, and Next/Previous navigation. No server needed: just
> double-click the file. (Prefer plain text? Each lab also has a `README.md`.)

## Scenario

> Build an **Enterprise Service Request Triage Assistant** that reads synthetic IT support
> requests, identifies category and urgency, summarizes the problem, recommends the next
> action, and explains when the available information is insufficient.

## Getting Started

1. Read [docs/workshop-overview.md](docs/workshop-overview.md).
2. Follow [docs/pre-workshop-setup.md](docs/pre-workshop-setup.md) (coding tracks) or
   [docs/portal-setup.md](docs/portal-setup.md) (portal track).
3. Review [docs/credential-safety.md](docs/credential-safety.md) — **read this before using any key**.
4. Start with [labs/00-access-and-baseline/README.md](labs/00-access-and-baseline/README.md).

## Lab Index

| Lab | Technique |
|-----|-----------|
| [00 — Access & Baseline](labs/00-access-and-baseline/) | Environment + unoptimized baseline |
| [01 — Explicit Prompt Contract](labs/01-explicit-prompt-contract/) | Objective, audience, constraints, output |
| [02 — Instruction Hierarchy](labs/02-instruction-hierarchy/) | System/user/data separation + delimiters |
| [03 — Few-Shot Prompting](labs/03-few-shot-prompting/) | Representative examples |
| [04 — Structured Output](labs/04-structured-output/) | Strict JSON schema + validation |
| [05 — Prompt Chaining](labs/05-prompt-chaining/) | Task decomposition + stage validation |
| [06 — Grounding & Uncertainty](labs/06-grounding-and-uncertainty/) | Answer from context, fallback |
| [07 — Evaluation & Injection](labs/07-evaluation-and-injection/) | Rubric comparison + defensive testing |
| [08 — Capstone](labs/08-capstone/) | Reusable enterprise prompt |

## Repository Layout

- `prompts/` — shared prompt manifests + text (source of truth)
- `datasets/` — synthetic triage data and test cases
- `schemas/` — JSON schemas (output, manifest, test case, evaluation result)
- `rubrics/` — evaluation rubric + portal validation checklist
- `apps/{python,csharp,java}/` — thin CLI reference runners
- `evaluation/` — deterministic + optional AI-assisted evaluators (facilitator)
- `docs/` — setup, portal, credential safety, troubleshooting, facilitator guide
- `solutions/` — reference solutions (separate from attendee instructions)

## Safety

Temporary keys only, read from environment variables. **Never** commit secrets or enter
confidential data into prompts. See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE).
