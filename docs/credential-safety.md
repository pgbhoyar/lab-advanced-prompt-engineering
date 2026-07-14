# Credential Safety

**Read this before using any workshop key.**

## The key is a temporary secret

Workshop keys are short-lived and shared only through the facilitator's controlled channel.
Treat the key like a password.

**Never**:

- Put the key in source code, prompts, screenshots, logs, chat, or lab submissions.
- Commit the key. `.env` is Git-ignored; example files use placeholders only.

**Always**:

- Store the key in environment variables (`.env` locally). All coding tracks read it from there.
- Use the setup checker to confirm configuration without printing the key.

## Data handling — do not paste sensitive information

Use only the **synthetic** workshop data provided. Do **not** enter confidential, regulated,
proprietary, or personal information (real customer names, account numbers, tickets, employee
data) into any workshop prompt — on any track. The triage assistant is a teaching example, not an
approved system for real data.

## After the workshop

The facilitator **rotates or revokes** the temporary keys within the defined post-workshop
window. Your local `.env` key will stop working after that — this is expected. Delete your local
`.env` when you are done.

## Production guidance (not used in this workshop)

For real systems, prefer **Microsoft Entra ID** (managed identity), least-privilege role
assignments, auditable permissions, and managed secret storage over API keys.
