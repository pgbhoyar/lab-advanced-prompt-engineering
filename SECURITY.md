# Security Policy

## Workshop Credential Handling

This repository is a teaching package. It contains **no secrets** and MUST never contain any.

Workshop credentials (Microsoft Foundry endpoint, deployment name, API key) are **temporary**
and are distributed only through a controlled channel by the facilitator.

API keys MUST NOT be:

- Added to source code
- Included in prompts
- Committed to Git
- Added to screenshots
- Shared in public chat
- Printed in logs
- Stored in sample output
- Included in lab submissions

All coding tracks read the endpoint, deployment name, and key from environment variables
(`AZURE_OPENAI_BASE_URL`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_DEPLOYMENT`). Example
configuration files (`.env.example`) contain placeholders only. Local secret files (`.env`)
are excluded via [.gitignore](.gitignore).

Temporary workshop keys are **rotated or revoked** by the facilitator within the defined
post-workshop window. See [docs/credential-safety.md](docs/credential-safety.md).

## Production Guidance

For production systems, use Microsoft Entra ID (managed identity), least-privilege role
assignments, auditable permissions, and managed secret storage rather than API keys.

## Data Handling

Use only synthetic or approved public data. Do **not** enter confidential, regulated,
proprietary, or personal information into any workshop prompt.

## Reporting

If you discover a credential accidentally committed, or a security issue in these materials,
notify the workshop organizer immediately and open a private report rather than a public issue.
Rotate any exposed key without delay.
