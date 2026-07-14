# Coding Tracks — Starter Instructions

All three coding tracks are **thin CLI runners** that load the same shared prompts, datasets, and
schemas from the repository root. Only how they connect to the model differs. Prompt content lives
in `prompts/` — never inside a language project.

Every runner exposes the same commands (see
[contracts/cli-contract.md](../specs/001-advanced-prompt-workshop/contracts/cli-contract.md)):
`check-config`, `list-labs`, `list-cases --lab <id>`, `run --lab <id> --case <id> --variant <v>`,
`validate [--file <f>]`. Exit codes: `0` ok, `1` usage, `2` config, `3` model, `4` validation.

Configure credentials via environment variables only (see [credential-safety.md](credential-safety.md)).

## How a run works (where `{{request_text}}` comes from)

You will see placeholders like `{{request_text}}` in the prompt files. **You never type these.**
The runner fills them in automatically. Every `run` does the same four things:

1. **Loads the prompt** for the lab + variant, e.g. `prompts/01-explicit-contract/user.md`, which
   contains the placeholder `{{request_text}}`.
2. **Loads the test case** you chose with `--case`. Cases live in `datasets/triage/*.jsonl`. For
   `--case normal-01`, the input `request_text` is *"My work laptop is about 5 years old…"*.
3. **Renders** the prompt by substituting each `{{placeholder}}` with the matching value from the
   case's `input` (so `{{request_text}}` becomes the case text). The runner prints the rendered
   prompt so you can see exactly what was sent.
4. **Sends** the request and prints the response (and `VALIDATION: PASS/FAIL` for structured labs).

So the whole job of the attendee is: **pick a `--lab`, a `--case`, and a `--variant`.** You do not
paste input or fill in the placeholder. To use different input, choose a different `--case`:

```
python -m workshop_runner list-cases --lab 01-explicit-prompt-contract
```

To change the *wording* of the prompt, edit the file under `prompts/<lab>/` — no code change, and
all three languages (and the portal) pick up the same edit.

> **Run from the repository root.** The runner walks up the folder tree to find the shared
> `prompts/`, `datasets/`, and `schemas/` directories. If you see "No manifest for lab…", you are
> probably not at the repo root, or you passed a `--lab`/`--case` id that doesn't exist
> (use `list-labs` and `list-cases`).

## Python (3.10+)

```
python -m pip install -e apps/python
python -m workshop_runner check-config
python -m workshop_runner run --lab 01-explicit-prompt-contract --case normal-01 --variant improved
python -m workshop_runner chain --lab 05-prompt-chaining --case edge-long-01
```

## C# (.NET 8+)

**Expectations:** .NET 8 SDK installed; a `.env` (or environment variables) with your
credentials; and you run **from the repository root** so the runner finds the shared assets. The
first `dotnet run` automatically restores packages and builds — allow a little extra time.

```
# from the repository root
dotnet run --project apps/csharp/src/WorkshopRunner -- check-config
dotnet run --project apps/csharp/src/WorkshopRunner -- list-cases --lab 01-explicit-prompt-contract
dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 01-explicit-prompt-contract --case normal-01 --variant baseline
dotnet run --project apps/csharp/src/WorkshopRunner -- run --lab 01-explicit-prompt-contract --case normal-01 --variant improved
```

The `--` separates `dotnet` options from the runner's arguments. You do **not** edit any C# code or
supply `{{request_text}}` — the runner renders it from the `--case` you chose (see
[How a run works](#how-a-run-works-where-request_text-comes-from)). Run the offline tests with:

```
dotnet test apps/csharp/tests/WorkshopRunner.Tests --filter Category=Offline
```

## Java (JDK 17+)

Using the Maven Wrapper (recommended):

```
cd apps/java
./mvnw -q compile
./mvnw -q exec:java -Dexec.args="check-config"
./mvnw -q exec:java -Dexec.args="run --lab 04-structured-output --case normal-01 --variant improved"
./mvnw -q test -Dgroups=offline
```

Or with the JDK directly (no Maven needed — the runner core uses only `java.base`):

```
cd apps/java
javac -d target/classes (all files under src/main/java)
java -cp target/classes com.workshop.runner.Main list-labs
```

## Editing prompts

Change a prompt by editing files under `prompts/<lab>/` — no code change is required. Re-run the
same command to see the effect. All tracks pick up the same edit.

## Switching to the portal

If a coding track breaks, switch to the portal at the same lab number using the same prompt and
input — see [pre-workshop-setup.md](pre-workshop-setup.md) §4.
