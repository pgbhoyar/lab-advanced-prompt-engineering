# Lab 06 — Grounding and Uncertainty

**Last updated: Jul-14-2026**

Make the model answer **only from supplied context** and acknowledge when it can't — so it never
invents enterprise rules, numbers, or citations.

`INTERMEDIATE` · ⏱️ 12 MIN · 📂 GROUNDING & UNCERTAINTY

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 300 | Anyone (no coding required) | 12 minutes | Answer supported questions from a synthetic policy, return a defined fallback for unsupported questions, and clearly label inferences versus stated facts. |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Exercise: Observe the ungrounded baseline](#-exercise-observe-the-ungrounded-baseline)
7. [Exercise: Ground and add a fallback](#-exercise-ground-and-add-a-fallback)
8. [Test & evaluate](#-test--evaluate)
9. [Checkpoint](#-checkpoint)
10. [Test your understanding & reflection](#-test-your-understanding--reflection)
11. [Troubleshooting](#-troubleshooting)
12. [Optional challenge](#-optional-challenge)
13. [Summary](#-summary)

## 🤔 Why this matters

An assistant that invents a policy number is worse than one that says "I don't know." Grounding and
explicit uncertainty handling are what make an enterprise assistant **trustworthy**.

## 🌐 Scenario

You answer IT service-policy questions using only the synthetic
[`policy-context.md`](../../datasets/triage/policy-context.md). Some questions are answered by the
policy; some are not; some conflict.

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Grounding** | Basing answers only on supplied source material. |
| **Fallback** | The defined response when the source cannot answer ("The provided information is insufficient…"). |
| **Inference** | A reasonable conclusion not directly stated — it must be labeled as such, never presented as policy fact. |

## ✅ Prerequisites

- **Lab 01** completed.
- Your chosen track configured (Portal, Python, C#, or Java).

## 🎯 What you'll accomplish

- Answer a supported question with policy evidence.
- Return the required fallback for an unsupported question.
- Distinguish facts, inferences, and unknowns.

## 🚀 Exercise: Observe the ungrounded baseline

**Summary of tasks:** run the baseline on `grounding-unsupported-01` (asks a VPN data cap the policy
does not cover) and note whether it invents a number.

### Step-by-step instructions

1. Run the **baseline** variant:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 06-grounding-and-uncertainty --case grounding-unsupported-01 --variant baseline` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 06-grounding-and-uncertainty --case grounding-unsupported-01 --variant baseline` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 06-grounding-and-uncertainty --case grounding-unsupported-01 --variant baseline"` |
   | Portal | See [portal.md](portal.md) |

## 🔧 Exercise: Ground and add a fallback

**Summary of tasks:** run the improved variant, which restricts answers to the supplied policy and
requires a fallback for unsupported questions.

### Step-by-step instructions

1. Run the **improved** variant on the same case (swap to `--variant improved`). Expect the exact
   fallback: *"The provided information is insufficient to answer this question."*
2. Also try `grounding-supported-01` (answers **90 days** with policy evidence) and
   `grounding-inference-01` (labels an escalation as an **inference**, not a policy fact).

🏅 **Congratulations!** You grounded responses and handled missing evidence.

## 🧮 Test & evaluate

Run the improved prompt on the supported, unsupported, and inference cases. Score with the
[standard rubric](../../rubrics/standard-rubric.md), focusing on **groundedness** and
**missing-information handling**.

## 🏅 Checkpoint

- [ ] The supported question is answered with policy evidence.
- [ ] The unsupported question returns the exact fallback sentence.

## 🤔 Test your understanding & reflection

1. What did the fallback rule prevent on the unsupported question?
2. How did the improved prompt separate a fact from an inference?

## 🧭 Troubleshooting

- If the model still invents a number, confirm the grounding system prompt was applied and the
  policy is inside the `<policy>` delimiters.
- Coding blocked? Use [portal.md](portal.md). See
  [../../docs/troubleshooting.md](../../docs/troubleshooting.md).

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional.

## 📖 Summary

You made the assistant answer only from evidence and admit uncertainty. **Lab 07** compares prompt
variants with a rubric and tests them against benign adversarial input.
