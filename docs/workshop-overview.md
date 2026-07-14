# Workshop Overview

## What this is

A 75-minute hands-on workshop that treats prompts as **testable, reusable, version-controlled
engineering assets**, using OpenAI GPT-5.4 in Microsoft Foundry. Every required lab works on the
**Microsoft Foundry portal** (no code) or via **Python, C#, or Java** — all sharing the same
prompts, inputs, output contract, test cases, and rubric.

## The scenario

> Build an **Enterprise Service Request Triage Assistant** that reads synthetic IT support
> requests, identifies category and urgency, summarizes the problem, recommends the next action,
> and explains when information is insufficient.

One scenario throughout lets you focus on technique, not domain.

## What you'll learn

Zero-shot baseline → explicit prompt contract → instruction hierarchy & delimited data → few-shot
→ structured output → prompt chaining → grounding & uncertainty → evaluation & injection testing →
a reusable capstone prompt.

## Ground rules

- **Synthetic data only.** Never enter confidential, regulated, proprietary, or personal
  information into any prompt.
- **Keep secrets safe.** Temporary keys live in environment variables, never in code, prompts,
  screenshots, or chat. See [credential-safety.md](credential-safety.md).

## How to start

1. [pre-workshop-setup.md](pre-workshop-setup.md) (coding) or [portal-setup.md](portal-setup.md)
   (portal).
2. [labs/00-access-and-baseline/README.md](../labs/00-access-and-baseline/README.md).

## After the workshop

Temporary keys are rotated/revoked, but all assets remain usable for continued learning. See
[post-workshop-next-steps.md](post-workshop-next-steps.md).
