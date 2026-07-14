# Lab 03 — Few-Shot Prompting

**Last updated: Jul-14-2026**

When instructions alone are ambiguous, a few **representative examples** can sharpen the model's
decisions. You'll improve a tricky classification with a small, consistent example set.

`BEGINNER–INTERMEDIATE` · ⏱️ 10 MIN · 📂 FEW-SHOT PROMPTING

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 200 | Anyone (no coding required) | 10 minutes | Compare zero-shot vs few-shot classification on a boundary case (a phishing link that should be **security**, not **software**) and see the pattern applied to new input. |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Exercise: Observe zero-shot](#-exercise-observe-zero-shot)
7. [Exercise: Add few-shot examples](#-exercise-add-few-shot-examples)
8. [Test & evaluate](#-test--evaluate)
9. [Checkpoint](#-checkpoint)
10. [Test your understanding & reflection](#-test-your-understanding--reflection)
11. [Troubleshooting](#-troubleshooting)
12. [Optional challenge](#-optional-challenge)
13. [Summary](#-summary)

## 🤔 Why this matters

Some boundaries are hard to describe in words but easy to show. Few-shot prompting is a widely
applicable technique that produces an easily observable before-and-after — as long as the examples
are accurate and consistent.

## 🌐 Scenario

Classify triage categories. The boundary between **security** and **software** is easy to get wrong
without examples (a clicked phishing link looks like a "pop-up" problem).

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Zero-shot** | Instructions only, no examples. |
| **Few-shot** | A handful of example input/output pairs that demonstrate the desired behavior. |
| **Boundary case** | An input near the line between two categories, where examples help most. |
| **Consistency** | Examples must be accurate and internally consistent — a wrong example teaches wrong behavior. |

## ✅ Prerequisites

- **Lab 01** completed.
- Your chosen track configured (Portal, Python, C#, or Java).

## 🎯 What you'll accomplish

- Record a zero-shot classification and its rationale.
- Add representative, consistent examples covering multiple categories.
- Observe the few-shot prompt apply the demonstrated pattern to a new case.

## 🚀 Exercise: Observe zero-shot

**Summary of tasks:** run the zero-shot prompt on `few-shot-boundary-01` (a clicked phishing link)
and record the category.

### Step-by-step instructions

1. Run the **baseline** (zero-shot) variant:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 03-few-shot-prompting --case few-shot-boundary-01 --variant baseline` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 03-few-shot-prompting --case few-shot-boundary-01 --variant baseline` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 03-few-shot-prompting --case few-shot-boundary-01 --variant baseline"` |
   | Portal | See [portal.md](portal.md) |

2. Zero-shot may mislabel it as **software**. Record the category and reason.

## 🔧 Exercise: Add few-shot examples

**Summary of tasks:** run the few-shot variant, which adds three consistent examples including a
boundary example mapping a phishing link to **security**.

### Step-by-step instructions

1. Run the **improved** (few-shot) variant on the same case (swap to `--variant improved`).
2. Confirm it now classifies the boundary case as **security** and applies the pattern rather than
   copying an example verbatim.

🏅 **Congratulations!** You improved an ambiguous classification with few-shot examples.

## 🧮 Test & evaluate

Run both on `few-shot-boundary-01`. Optionally add `irrelevant-01` (should stay out of scope) to
confirm the examples don't cause over-triage. Score with the
[standard rubric](../../rubrics/standard-rubric.md), focusing on **task correctness**.

## 🏅 Checkpoint

- [ ] You ran zero-shot and few-shot on the same case.
- [ ] The few-shot variant applied the demonstrated pattern (not a copied example).

## 🤔 Test your understanding & reflection

1. Did the model copy an example literally, or apply the pattern to new input?
2. What would happen if one example were inconsistent or wrong?

## 🧭 Troubleshooting

- If few-shot performs worse, check the examples are accurate and consistent — a bad example
  teaches bad behavior.
- Coding blocked? Use [portal.md](portal.md). See
  [../../docs/troubleshooting.md](../../docs/troubleshooting.md).

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional.

## 📖 Summary

You used a small, consistent example set to sharpen an ambiguous decision. **Lab 04** locks the
response into a strict, machine-readable structure.
