# Lab 08 — Capstone: Enterprise Triage Prompt

**Last updated: Jul-14-2026**

Combine everything you've learned into one **reusable, tested** enterprise triage prompt — and
leave the workshop with a practical artifact you can keep improving.

`INTERMEDIATE–ADVANCED` · ⏱️ REMAINING TIME (finishable afterward) · 📂 CAPSTONE

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 300 | Anyone (no coding required) | Remaining session time | Build a prompt that produces strict structured output, grounded in a supplied policy, resistant to embedded instructions, with a defined uncertainty policy — and pass the capstone quality gates. |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Requirements](#-requirements)
7. [Exercise: Build and test your capstone](#-exercise-build-and-test-your-capstone)
8. [Passing criteria](#-passing-criteria)
9. [Checkpoint](#-checkpoint)
10. [Test your understanding & reflection](#-test-your-understanding--reflection)
11. [Troubleshooting](#-troubleshooting)
12. [Optional challenge](#-optional-challenge)
13. [Summary](#-summary)

## 🤔 Why this matters

Individual techniques are useful; combining them into one reliable, versioned prompt is what
real work looks like. The capstone proves you can assemble a prompt that is structured, grounded,
safe, and honest about uncertainty — all at once.

## 🌐 Scenario

Build one prompt that triages a service request into the strict triage schema, grounded in a
supplied policy, resistant to embedded instructions, with a defined uncertainty policy.

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Reusable prompt asset** | A versioned prompt with manifest, text, test set, rubric, and change notes. |
| **Quality gate** | A defined bar (schema-valid, grounded, safe, ≥ 14/18) a prompt must clear to ship. |
| **Composition** | Layering contract + hierarchy + structured output + grounding + defense in one prompt. |

## ✅ Prerequisites

- **Labs 01, 02, 04, and 06** completed (contract, hierarchy, structured output, grounding).
  Lab 07 (evaluation) recommended.
- Your chosen track configured (Portal, Python, C#, or Java).

## 🎯 What you'll accomplish

- Create (or start) a reusable triage prompt that passes the four provided capstone cases.
- Explain which workshop technique each part of your prompt applies.

## 📐 Requirements

Your prompt must define: prompt id, version, objective, input variables, constraints, output
contract, and uncertainty policy. It must:

- Produce structured output conforming to
  [`schemas/triage-output.schema.json`](../../schemas/triage-output.schema.json).
- **Ground** answers in the supplied `<policy>` with a fallback when unsupported.
- **Separate** instructions from `<source_data>` (treat it as untrusted).
- Be tested across normal, ambiguous, missing-information, an edge case (add your own), and
  adversarial inputs.

Start from the reference prompt (`prompts/08-capstone-reference/`) or write your own. Keep prompt
text in files; never hard-code secrets.

## 🚀 Exercise: Build and test your capstone

**Summary of tasks:** build the prompt, run the capstone cases, and score against the capstone
rubric.

### Step-by-step instructions

1. Run the reference (or your prompt) on the capstone cases:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 08-capstone --case cap-normal-01 --variant reference` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 08-capstone --case cap-adversarial-01 --variant reference` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 08-capstone --case cap-normal-01 --variant reference"` |
   | Portal | See [portal.md](portal.md) |

2. Run all four cases (`cap-normal-01`, `cap-ambiguous-01`, `cap-missing-01`,
   `cap-adversarial-01`) and add one edge case of your own. Structured output is validated
   automatically on coding tracks.
3. Score with the [capstone rubric](../../rubrics/capstone-rubric.md).

🏅 **Congratulations!** You built a reusable, tested enterprise prompt.

## 🎯 Passing criteria

See the [capstone rubric](../../rubrics/capstone-rubric.md): valid manifest and response contract,
all five categories executed, no schema failure, no security-boundary failure, no fabricated
action, **≥ 14/18**, and no zero on groundedness, format, or safety.

## 🏅 Checkpoint

- [ ] Your prompt passes the four provided cases (structured, grounded, injection-resistant).
- [ ] You can name which workshop technique each part of your prompt applies.

## 🤔 Test your understanding & reflection

1. Which technique was hardest to combine with the others, and why?
2. If you had one more revision, what failure would you target first?

## 🧭 Troubleshooting

- Schema failures → check field names/enums against the triage schema.
- Coding blocked? Use [portal.md](portal.md).
- Didn't finish? The reference prompt, test set, and rubric stay in the repo — continue after the
  session using [../../docs/post-workshop-next-steps.md](../../docs/post-workshop-next-steps.md).

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional.

## 📖 Summary

You assembled a structured, grounded, safe, uncertainty-aware prompt and measured it against a
quality gate — a reusable asset and a complete picture of enterprise prompt engineering.
