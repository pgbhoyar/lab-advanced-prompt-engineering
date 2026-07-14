# Lab 05 — Prompt Decomposition and Chaining

**Last updated: Jul-14-2026**

Split a complex task into smaller **stages**, each with one responsibility, and validate each
intermediate result before the next stage uses it.

`INTERMEDIATE` · ⏱️ 12 MIN · 📂 PROMPT CHAINING

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 300 | Anyone (no coding required) | 12 minutes | Compare a single multi-purpose prompt with a two-stage chain (extract → validate → classify) and see a failed intermediate stage stop the chain. |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Exercise: Observe the single prompt](#-exercise-observe-the-single-prompt)
7. [Exercise: Run the chain](#-exercise-run-the-chain)
8. [Test & evaluate](#-test--evaluate)
9. [Checkpoint](#-checkpoint)
10. [Test your understanding & reflection](#-test-your-understanding--reflection)
11. [Troubleshooting](#-troubleshooting)
12. [Optional challenge](#-optional-challenge)
13. [Summary](#-summary)

## 🤔 Why this matters

Complex "do everything at once" prompts are hard to debug and easy to break. Decomposition improves
observability, testability, and maintainability — at the cost of more moving parts. This lab shows
when that trade-off is worth it.

## 🌐 Scenario

The baseline asks the model to classify, summarize, recommend, and draft a reply all at once. The
chain splits this into **Stage 1** extract facts (JSON) → validate → **Stage 2** classify &
recommend from the validated facts.

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Prompt chain** | Several prompts run in sequence, each with one responsibility. |
| **Stage** | One step of the chain, independently inspectable and testable. |
| **Intermediate validation** | Checking a stage's output before the next stage uses it, so failures are caught, not propagated. |

## ✅ Prerequisites

- **Labs 01 and 04** completed.
- Your chosen track configured (Portal, Python, C#, or Java).

## 🎯 What you'll accomplish

- Observe weak or missing portions from a single multi-purpose prompt.
- Run a staged chain that validates Stage 1 before Stage 2.
- See an invalid intermediate output stop the chain.

## 🚀 Exercise: Observe the single prompt

**Summary of tasks:** run the single multi-purpose baseline on `edge-long-01` (a long, noisy
message) and note weak or missing portions.

### Step-by-step instructions

1. Run the **baseline** (single) variant:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 05-prompt-chaining --case edge-long-01 --variant baseline` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 05-prompt-chaining --case edge-long-01 --variant baseline` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 05-prompt-chaining --case edge-long-01 --variant baseline"` |
   | Portal | See [portal.md](portal.md) |

## 🔧 Exercise: Run the chain

**Summary of tasks:** run the two-stage chain and watch per-stage validation.

### Step-by-step instructions

1. Run the **chain**:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner chain --lab 05-prompt-chaining --case edge-long-01` |
   | Portal | Manually copy the **validated** Stage 1 output into Stage 2 — see [portal.md](portal.md) |

2. The runner executes stages in order, prints `PASS`/`FAIL` per stage, and **stops** on a failed
   intermediate validation (Stage 1 must return valid JSON).

> **Note — validate before you continue.** In the portal, transfer only Stage 1 output that you
> confirmed is valid JSON. Garbage in Stage 1 means garbage (or a stop) in Stage 2.

🏅 **Congratulations!** You decomposed a task into validated, independent stages.

## 🧮 Test & evaluate

Run the chain on `edge-long-01` and `conflicting-01`. Compare the single prompt vs the chain with
the [standard rubric](../../rubrics/standard-rubric.md) on **completeness**, **relevance**, and
**clarity** — and discuss traceability and maintainability.

## 🏅 Checkpoint

- [ ] You ran the single prompt and the chain on the same case.
- [ ] You saw per-stage validation status and understand where the chain would stop.

## 🤔 Test your understanding & reflection

1. Which is easier to debug when something goes wrong — the single prompt or the chain?
2. What did intermediate validation prevent?

## 🧭 Troubleshooting

- Chain stops at Stage 1 → Stage 1 did not return valid JSON; inspect its output.
- Coding blocked? Use [portal.md](portal.md) and transfer validated output manually.

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional.

## 📖 Summary

You traded one opaque prompt for a transparent, validated chain. **Lab 06** grounds answers in
supplied context and defines what to do when evidence is missing.
