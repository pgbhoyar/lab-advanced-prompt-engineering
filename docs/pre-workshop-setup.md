# Pre-Workshop Setup Guide

Complete this **before** the workshop. Everything here uses **synthetic** data and a
**temporary** workshop key. You can complete every required lab through the portal if you cannot
run code.

## 0. Get the workshop files

**How you "get" the workshop depends on your track:**

- **Portal track (no code):** you do **not** need to clone anything. Just open the workshop
  site in your browser and follow the **Portal** steps in each lab. The site has everything you
  paste into the Foundry portal. (Your facilitator will share the site link, or open
  `site/index.html` if you were given the files.)
- **Coding track (Python / C# / Java):** you **do** need the repository locally — the runner
  loads the shared prompts, datasets, and schemas from it. Clone it (or download the ZIP) and
  work from the repository root:

  ```
  git clone <workshop-repo-url>
  cd lab-advanced-prompt-engineering
  ```

  > No Git? Download the repository ZIP from the workshop page and extract it, then open a
  > terminal in the extracted folder. Everything else is the same.

You will still receive the **temporary credentials** from the facilitator's controlled channel —
they are never stored in the repository.

## 1. Choose your track

| Track | You need | Notes |
|-------|----------|-------|
| Microsoft Foundry portal | A browser + workshop account | No local install, no clone |
| Python | Python 3.10+, the repo cloned | `pip install -e apps/python` |
| C# | .NET SDK 8.0+, the repo cloned | `dotnet restore` in `apps/csharp` |
| Java | JDK 17+, the repo cloned | Maven Wrapper included |

## 2. Get and configure credentials

1. Receive the temporary endpoint, deployment name, and key from the facilitator's controlled
   channel. **Never** paste the key into code, prompts, screenshots, or chat.
2. Copy `.env.example` to `.env` and fill in the three required values.
3. Run the checker (it never prints your key):
   - Windows: `pwsh scripts/setup.ps1`
   - macOS/Linux: `bash scripts/setup.sh`

Read [credential-safety.md](credential-safety.md) before using any key.

## 3. Verify your track

- **Python:** `python -m workshop_runner check-config`
- **C#:** `dotnet run --project apps/csharp/src/WorkshopRunner -- check-config`
- **Java:** `./mvnw -q exec:java -Dexec.args="check-config"`
- **Portal:** open the project and confirm you can select the workshop deployment
  (see [portal-setup.md](portal-setup.md)).

Full per-language commands are in [coding-tracks.md](coding-tracks.md).

## Cross-platform notes

- **Windows:** run `pwsh scripts/setup.ps1`. Use `dotnet` / `java` / `python` from a terminal.
- **macOS / Linux:** run `bash scripts/setup.sh`. Use `python3`, `dotnet`, `java`.
- **Corporate-restricted machines:** if you cannot install packages or run local code, use the
  **portal** track — every required lab works with no local software. The Java runner core also
  runs with only the JDK (no Maven) if package downloads are blocked (see
  [coding-tracks.md](coding-tracks.md)).

## 4. Switching tracks mid-workshop (fallback)

If your coding setup breaks at any point, you can switch to the **portal** without losing your
place:

1. Note the **lab number** you are on (e.g. Lab 03).
2. Open that lab's `portal.md`.
3. Restart the **same lab** from its beginning using the **same shared prompt and input** — labs
   are stateless, so no mid-lab progress needs to be preserved.
4. This switch is designed to take **under five minutes**.

The reverse (portal → coding) works the same way. A failure in one track never blocks another.

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for authentication, dependency, rate-limit, and
output problems.
