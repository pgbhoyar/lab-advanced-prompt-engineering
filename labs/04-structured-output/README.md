# Lab 04 — Structured Output

**Last updated: Jul-14-2026**

Move from conversational replies to a **strict, machine-readable output contract**. You'll compare
a loose "reply in JSON" prompt with a schema-enforced prompt and validate the result.

`INTERMEDIATE` · ⏱️ 15 MIN · 📂 STRUCTURED OUTPUT

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 300 | Anyone (no coding required) | 15 minutes | Produce a triage object with all required fields and valid enum values, and validate it programmatically (coding) or with a manual checklist (portal). |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Exercise: Observe loose "JSON"](#-exercise-observe-loose-json)
7. [Exercise: Enforce a strict schema](#-exercise-enforce-a-strict-schema)
8. [Test & evaluate](#-test--evaluate)
9. [Checkpoint](#-checkpoint)
10. [Test your understanding & reflection](#-test-your-understanding--reflection)
11. [Troubleshooting](#-troubleshooting)
12. [Optional challenge](#-optional-challenge)
13. [Summary](#-summary)

## 🤔 Why this matters

Real applications consume model output as data, not prose. A fluent answer that breaks the schema
is a **failed** result — it can't be parsed downstream. Structured output is the transition from
chatting with a model to building on it.

## 🌐 Scenario

A downstream system needs a machine-readable triage object. You compare a loose "reply in JSON"
prompt with a strict schema-enforced prompt using
[`schemas/triage-output.schema.json`](../../schemas/triage-output.schema.json).

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Schema** | Defines the exact shape of a response — fields, types, allowed values. |
| **Enum** | A fixed set of allowed values (e.g. urgency ∈ {low, medium, high, critical}). |
| **Strict structured output** | The model must return valid JSON matching the schema, with no extra text or fields. |
| **Failed structured output** | A fluent response that violates the contract — scored as a failure. |

## ✅ Prerequisites

- **Lab 01** completed.
- Your chosen track configured (Portal, Python, C#, or Java).

## 🎯 What you'll accomplish

- Produce a single JSON object with all nine required fields and valid enums.
- Validate it automatically (coding) or with the portal checklist.
- Recognize that a fluent but non-compliant response is a failure.

## 🚀 Exercise: Observe loose "JSON"

**Summary of tasks:** run the baseline "reply in JSON" prompt on `normal-01` and note contract
issues.

### Step-by-step instructions

1. Run the **baseline** variant:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 04-structured-output --case normal-01 --variant baseline` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 04-structured-output --case normal-01 --variant baseline` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 04-structured-output --case normal-01 --variant baseline"` |
   | Portal | See [portal.md](portal.md) |

2. Note issues: prose around the JSON, wrong field names (`priority` vs `urgency`), invalid enum
   values, or missing fields.

## 🔧 Exercise: Enforce a strict schema

**Summary of tasks:** run the improved prompt, which sends the strict schema (all fields required,
enums constrained, `additionalProperties: false`).

### Step-by-step instructions

1. Run the **improved** variant on the same case (swap to `--variant improved`). The runner
   **automatically validates** the response and prints `VALIDATION: PASS` / `FAIL` (exit code 4 on
   failure).
2. Try `missing-information-01`: confirm `missing_information` is a non-empty array and
   `needs_human_review` is `true`.

> **Note — portal validation.** If the portal exposes a JSON-schema option, attach the shared
> schema; otherwise validate by hand with the
> [structured-output checklist](../../rubrics/structured-output-checklist.md).

🏅 **Congratulations!** You produced and validated a strict structured output.

## 🧮 Test & evaluate

Run the improved prompt on `normal-01` and `missing-information-01`. Score with the
[standard rubric](../../rubrics/standard-rubric.md), focusing on **output-format compliance**.

## 🏅 Checkpoint

- [ ] Improved response contains all nine required fields with valid enum values.
- [ ] You validated it (runner `VALIDATION: PASS`, or the portal checklist).

## 🤔 Test your understanding & reflection

1. What did the strict schema fix that "reply in JSON" did not?
2. How is the missing-information case represented in the structured output?

## 🧭 Troubleshooting

- `VALIDATION: FAIL — Unexpected field` → the model added a key not in the contract; rely on
  schema-enforced mode or tighten the instruction.
- Portal has no schema option? Request the schema in the prompt and use the checklist.
- See [../../docs/troubleshooting.md](../../docs/troubleshooting.md).

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional.

## 📖 Summary

You enforced and validated a strict output contract. **Lab 05** breaks a complex task into
independently testable stages.
