# Lab 01 — Explicit Prompt Contract

**Last updated: Jul-14-2026**

Turn a vague request into an **explicit prompt contract** — objective, audience, context,
instructions, constraints, output format, and an uncertainty policy — and watch model behavior
become measurable and consistent.

`BEGINNER` · ⏱️ 10 MIN · 📂 PROMPT CONTRACTS

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 200 | Anyone (no coding required) | 10 minutes | Replace subjective wording ("make it better") with observable requirements, then compare a baseline and improved prompt on the same input using the standard rubric. |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Exercise: Observe the vague baseline](#-exercise-observe-the-vague-baseline)
7. [Exercise: Apply an explicit contract](#-exercise-apply-an-explicit-contract)
8. [Test & evaluate](#-test--evaluate)
9. [Checkpoint](#-checkpoint)
10. [Test your understanding & reflection](#-test-your-understanding--reflection)
11. [Troubleshooting](#-troubleshooting)
12. [Optional challenge](#-optional-challenge)
13. [Summary](#-summary)

## 🤔 Why this matters

"Make it better" is not a specification. When expectations are vague, results vary and you can't
tell whether a change helped. An explicit contract makes the model's job — and your evaluation —
**observable**. This is the foundation every later lab builds on.

## 🌐 Scenario

Same Enterprise Service Request Triage scenario. You compare two prompts on the **same input**, so
the only thing that changes is the prompt itself.

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Prompt contract** | The explicit expectations you give the model: what to do, for whom, with what limits, and in what format. |
| **Constraint** | A hard rule (e.g. "under 150 words") the response must respect. |
| **Uncertainty policy** | What the model should do when information is missing (say so, don't guess). |
| **Observable criteria** | Requirements you can check — audience, tone, length, required content — instead of "professional" or "better". |

## ✅ Prerequisites

- **Lab 00** completed — you have a baseline response and a working track.
- Your chosen track configured (Portal, Python, C#, or Java).

## 🎯 What you'll accomplish

- Identify at least two weaknesses in a vague prompt's output.
- Write an explicit contract with objective, constraints, output format, and uncertainty policy.
- Show, with the rubric, which contract element caused the improvement.

## 🚀 Exercise: Observe the vague baseline

**Summary of tasks:** run the vague baseline on `normal-01` and note its weaknesses.

**Baseline prompt** ([`prompts/01-explicit-contract/user.md`](../../prompts/01-explicit-contract/user.md)):

```text
Please triage this support request and make it better.

{{request_text}}
```

### Step-by-step instructions

1. Run the **baseline** variant:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 01-explicit-prompt-contract --case normal-01 --variant baseline` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 01-explicit-prompt-contract --case normal-01 --variant baseline` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 01-explicit-prompt-contract --case normal-01 --variant baseline"` |
   | Portal | See [portal.md](portal.md) |

2. Note weaknesses: "better" is subjective, no category/urgency vocabulary, no output structure,
   no rule for missing information.

## 🔧 Exercise: Apply an explicit contract

**Summary of tasks:** run the improved prompt (with a system contract) on the **same** case.

The improved prompt ([`prompts/01-explicit-contract/system.md`](../../prompts/01-explicit-contract/system.md))
defines a Job, Audience, numbered Instructions, Constraints, a labeled output structure, and an
Uncertainty policy.

### Step-by-step instructions

1. Run the **improved** variant on the same case:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 01-explicit-prompt-contract --case normal-01 --variant improved` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 01-explicit-prompt-contract --case normal-01 --variant improved` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 01-explicit-prompt-contract --case normal-01 --variant improved"` |
   | Portal | See [portal.md](portal.md) |

🏅 **Congratulations!** You turned a vague request into a testable prompt contract.

## 🧮 Test & evaluate

Run both variants against the **same** input (also try `ambiguous-01` and `missing-information-01`).
Score each with the [standard rubric](../../rubrics/standard-rubric.md). Expect the improved prompt
to score higher on **instruction adherence**, **completeness**, and **output-format compliance**.

## 🏅 Checkpoint

- [ ] You ran the baseline and improved prompts on the **same** input.
- [ ] You scored both with the rubric and can name which contract element caused the improvement.

## 🤔 Test your understanding & reflection

1. Which specific contract element caused the biggest improvement?
2. How did the uncertainty policy change the response on `missing-information-01`?

## 🧭 Troubleshooting

- If the improved response ignores a rule, confirm you selected `--variant improved` and the
  **same** case as the baseline.
- Coding blocked? Switch to [portal.md](portal.md). See
  [../../docs/troubleshooting.md](../../docs/troubleshooting.md).

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional — does not block later labs.

## 📖 Summary

You replaced vague wording with an explicit, observable contract and proved the improvement with a
rubric. Next, **Lab 02** separates your stable instructions from untrusted input.
