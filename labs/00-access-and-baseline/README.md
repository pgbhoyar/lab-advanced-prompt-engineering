# Lab 00 — Access and Baseline

**Last updated: Jul-14-2026**

Get your workshop environment working and capture your first, **unoptimized** model response.
This baseline is the "before" picture you will improve throughout the rest of the workshop.

`BEGINNER` · ⏱️ 8 MIN · 📂 SETUP & BASELINE

| Level | Persona | Duration | Learning objective |
|-------|---------|----------|---------|
| 100 | Anyone (no coding required) | 8 minutes | Confirm you can reach the workshop model on your chosen track, run a prompt, and save a baseline response with two observable weaknesses to compare against later. |

## 📋 Contents

1. [Why this matters](#-why-this-matters)
2. [Scenario](#-scenario)
3. [Core concepts](#-core-concepts)
4. [Prerequisites](#-prerequisites)
5. [What you'll accomplish](#-what-youll-accomplish)
6. [Choose your track](#-choose-your-track)
7. [Exercise: Run the baseline prompt](#-exercise-run-the-baseline-prompt)
8. [Checkpoint](#-checkpoint)
9. [Test your understanding & reflection](#-test-your-understanding--reflection)
10. [Troubleshooting](#-troubleshooting)
11. [Optional challenge](#-optional-challenge)
12. [Summary](#-summary)

## 🤔 Why this matters

No learning can happen until you can reach the model. A fast, reliable start means you spend the
session on **prompt engineering**, not setup. Capturing a baseline now also gives you an honest
measuring stick: every later lab is judged by how much it improves on this first attempt.

## 🌐 Scenario

You are triaging **synthetic** IT support requests for the **Enterprise Service Request Triage
Assistant** used throughout the workshop. The starter request `SR-0001` (in
[`datasets/triage/starter-cases.jsonl`](../../datasets/triage/starter-cases.jsonl)) describes a
user who cannot connect to office WiFi before a client demo.

## 🎓 Core concepts

| Concept | Why it matters |
|---------|----------------|
| **Prompt** | The text you send to the model. Everything you do in this workshop is shaping prompts. |
| **Baseline** | A first, unoptimized attempt you keep for comparison. Improvement is only meaningful against a baseline. |
| **Model deployment** | The named instance of GPT-5.4 in Microsoft Foundry. Its name may differ from "GPT-5.4" — use the exact name you were given. |

## ✅ Prerequisites

- Workshop access instructions from the facilitator.
- **Coding tracks only:** a prepared runtime (Python 3.10+, .NET 8+, or JDK 17+).
- No prior AI, SDK, command-line, or prompt-engineering experience required.
- You have read [credential-safety.md](../../docs/credential-safety.md) — **never** paste a key
  into code, prompts, or chat, and use only synthetic data.

## 🎯 What you'll accomplish

- Reach the workshop model on the Portal, Python, C#, or Java track.
- Run the baseline prompt against the starter request.
- Record two observable weaknesses to improve in Lab 01.

## 🧪 Choose your track

Both tracks teach the same thing and use the same prompt and input — pick the one that fits you.

| Track | Best for | How you run it |
|-------|----------|----------------|
| **Portal** | No coding | Microsoft Foundry portal — see [portal.md](portal.md) |
| **Developer** | Python / C# / Java | The workshop runner CLI (below) |

## 🚀 Exercise: Run the baseline prompt

**Summary of tasks:** choose a track, confirm connectivity, run the baseline prompt on
`starter-01`, and record the response.

**Starting prompt** (deliberately vague — see [`prompts/00-baseline/user.md`](../../prompts/00-baseline/user.md)):

```text
Look at this IT support message and tell me what to do about it.

{{request_text}}
```

### Step-by-step instructions

1. **Pick your track** — Portal ([portal.md](portal.md)) or a coding language below.
2. **Check connectivity.** Coding tracks: run the config checker (it never prints your key).
   - Windows: `pwsh scripts/setup.ps1`
   - macOS / Linux: `bash scripts/setup.sh`
3. **Run the baseline** on case `starter-01`:

   | Track | Command |
   |-------|---------|
   | Python | `python -m workshop_runner run --lab 00-access-and-baseline --case starter-01 --variant baseline` |
   | C# | `dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 00-access-and-baseline --case starter-01 --variant baseline` |
   | Java | `./mvnw -q exec:java -Dexec.args="run --lab 00-access-and-baseline --case starter-01 --variant baseline"` |

4. **Record** the response and two weaknesses in
   [expected-observations.md](expected-observations.md).

> **Note — configure credentials via environment variables only.** See
> [credential-safety.md](../../docs/credential-safety.md). Never place a key in code.

🏅 **Congratulations!** You reached the model and captured a baseline.

## 🏅 Checkpoint

You have completed this lab when:

- [ ] You received a response from the workshop model.
- [ ] You recorded **two observable weaknesses** in the baseline response.

## 🤔 Test your understanding & reflection

1. What did the baseline prompt leave undefined (format, urgency criteria, missing-information behavior)?
2. If two people ran this prompt, would they get comparably structured answers? Why or why not?

## 🧭 Troubleshooting

- **Missing/placeholder credentials:** run `scripts/setup.ps1` / `setup.sh` to check configuration.
- **Coding setup blocked:** switch to [portal.md](portal.md) and continue this same lab.
- **No/slow response:** see [../../docs/troubleshooting.md](../../docs/troubleshooting.md) and the
  offline sample in [../../offline-fallback/baseline-output.md](../../offline-fallback/baseline-output.md).

## 🏆 Optional challenge

See [challenge.md](challenge.md). Optional — it does not block later labs.

## 📖 Summary

You confirmed access, ran an intentionally vague prompt, and captured a baseline with observable
weaknesses. In **Lab 01** you'll turn that vague prompt into an explicit, testable prompt contract.
