#!/usr/bin/env bash
# Workshop setup + configuration checker for the coding tracks (macOS / Linux).
# Validates required environment variables without printing secret values and
# points to the portal fallback if a coding runtime is missing.
set -euo pipefail

echo "== Advanced Prompt Engineering Workshop setup =="

# Load .env if present
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
  echo "Loaded .env"
else
  echo "No .env found. Copy .env.example to .env and fill in workshop values."
fi

ok=1
check_var() {
  local name="$1"
  local value="${!name:-}"
  if [ -z "$value" ]; then
    echo "  [MISSING] $name"; ok=0
  elif [[ "$value" == *"<"*">"* ]]; then
    echo "  [PLACEHOLDER] $name still contains a placeholder value"; ok=0
  else
    echo "  [OK] $name is set"
  fi
}

check_var AZURE_OPENAI_BASE_URL
check_var AZURE_OPENAI_API_KEY
check_var AZURE_OPENAI_DEPLOYMENT

base="${AZURE_OPENAI_BASE_URL:-}"
if [ -n "$base" ] && [[ "$base" != https://* ]]; then echo "  [WARN] BASE_URL must use https://"; ok=0; fi
if [ -n "$base" ] && [[ "$base" != */openai/v1/ && "$base" != */openai/v1 ]]; then echo "  [WARN] BASE_URL should end in /openai/v1/"; ok=0; fi

echo ""
echo "Detected runtimes:"
for cmd in python3 dotnet java; do
  if command -v "$cmd" >/dev/null 2>&1; then echo "  [OK] $cmd"; else echo "  [not found] $cmd"; fi
done

echo ""
if [ "$ok" -eq 1 ]; then
  echo "Configuration looks good. You can run a coding track or the portal."
else
  echo "Configuration incomplete. If you cannot fix the coding setup, use the portal track:"
  echo "  docs/portal-setup.md"
  echo "You can complete every required lab through the portal (no local code needed)."
fi
