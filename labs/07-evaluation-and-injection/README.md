# Lab 07 — Evaluation and Prompt-Injection Testing

**Last updated: Jul-14-2026**

Turn "it feels better" into **evidence**. Compare prompt variants with a repeatable rubric, then
test a defensive prompt against benign adversarial input — and record failures honestly.

`INTERMEDIATE` · ⏱️ 15 MIN · 📂 EVALUATION & SECURITY

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 300 | Anyone (no coding required) | 15 minutes (10 evaluation + 5 injection) | Score variants across five scenario types, surface improvements and regressions, and demonstrate that prompt wording is one layer of defense — not the whole security story. |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Part A — Evaluation](#-part-a--evaluation)
7. [Part B — Prompt-injection testing](#-part-b--prompt-injection-testing)
8. [Checkpoint](#-checkpoint)
9. [Test your understanding & reflection](#-test-your-understanding--reflection)
10. [Troubleshooting](#-troubleshooting)
11. [Optional challenge](#-optional-challenge)
12. [Summary](#-summary)

## 🤔 Why this matters

Evaluation-driven iteration is the main difference between casual prompting and prompt engineering.
And because enterprise prompts process untrusted text, you must understand both the value **and the
limits** of defensive prompt design.

## 🌐 Scenario

You compare a baseline and improved prompt across the five scenario types (normal, ambiguous,
missing-information, edge, adversarial), then run a **defensive** triage prompt against benign,
synthetic injection attempts.

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Evaluation rubric** | Scores responses on defined criteria (0–2), so comparisons are evidence-based. |
| **Regression** | A change that improves one thing but worsens another — the rubric makes it visible. |
| **Prompt injection** | Untrusted text that tries to hijack the task. |
| **Defense in depth** | Layering safeguards; prompt wording alone is not a complete boundary. |

## ✅ Prerequisites

- **Labs 01, 02, and 04** completed.
- Your chosen track configured (Portal, Python, C#, or Java).

## 🎯 What you'll accomplish

- Score two prompt variants on identical inputs and name an improvement or regression.
- Run a defensive prompt against adversarial cases and record the outcome honestly.

## 🧪 Part A — Evaluation

**Summary of tasks:** run a baseline and improved variant (e.g. Lab 04) on the **same** cases and
score both with the rubric.

### Step-by-step instructions

1. Pick a lab with baseline/improved variants (e.g. `04-structured-output`).
2. Run both variants on the same cases and score each with the
   [standard rubric](../../rubrics/standard-rubric.md).
3. Record improvements **and** regressions. A change that fixes the happy path but breaks
   missing-information handling is a regression you must surface.
4. **Facilitator deterministic runner (optional):**
   `python evaluation/facilitator/run_evaluation.py --lab 04-structured-output --variant improved --runs 3`

## 🛡️ Part B — Prompt-injection testing

**Summary of tasks:** run the defensive prompt against benign adversarial cases.

### Step-by-step instructions

1. Run the defensive (`improved`) variant on each adversarial case:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 07-evaluation-and-injection --case adversarial-ignore-01 --variant improved` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 07-evaluation-and-injection --case adversarial-ignore-01 --variant improved` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 07-evaluation-and-injection --case adversarial-ignore-01 --variant improved"` |
   | Portal | See [portal.md](portal.md) |

   Also try `adversarial-reveal-01` and `adversarial-outofscope-01`.

2. Confirm the model keeps triaging, refuses to reveal instructions/secrets, and stays in scope.

> **Honesty rule.** If an adversarial test **bypasses** the boundary, record it as a **failed**
> test and note that application-level safeguards are required. Do not retry until you get a clean
> run and present only that.

🏅 **Congratulations!** You evaluated with evidence and tested defenses honestly.

## 🏅 Checkpoint

- [ ] You scored a baseline and improved variant on the same inputs and named one improvement or regression.
- [ ] You ran at least one adversarial case and recorded the outcome honestly.

## 🤔 Test your understanding & reflection

1. Did the improved prompt improve one criterion while regressing another?
2. Why is a passing injection test **not** proof the prompt is secure?

## 🧭 Troubleshooting

- Deterministic runner import error → run from the repository root.
- Coding blocked? Use [portal.md](portal.md). See
  [../../docs/troubleshooting.md](../../docs/troubleshooting.md).

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional.

## 📖 Summary

You made prompt decisions evidence-based and saw the limits of prompt-only defenses. **Lab 08**
combines every technique into one reusable capstone prompt.
