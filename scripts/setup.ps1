#requires -Version 5.1
<#
.SYNOPSIS
    Workshop setup + configuration checker for the coding tracks.
.DESCRIPTION
    Verifies runtime availability and validates that required environment variables are set
    without printing secret values. Points to the portal fallback if a coding runtime is missing.
#>

$ErrorActionPreference = 'Stop'

Write-Host "== Advanced Prompt Engineering Workshop setup ==" -ForegroundColor Cyan

function Test-EnvVar {
    param([string]$Name)
    $value = [Environment]::GetEnvironmentVariable($Name)
    if ([string]::IsNullOrWhiteSpace($value)) {
        Write-Host ("  [MISSING] {0}" -f $Name) -ForegroundColor Yellow
        return $false
    }
    if ($value -like '*<*>*') {
        Write-Host ("  [PLACEHOLDER] {0} still contains a placeholder value" -f $Name) -ForegroundColor Yellow
        return $false
    }
    Write-Host ("  [OK] {0} is set" -f $Name) -ForegroundColor Green
    return $true
}

# Load .env if present (coding tracks)
if (Test-Path ".env") {
    Get-Content ".env" | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
        $pair = $_ -split '=', 2
        [Environment]::SetEnvironmentVariable($pair[0].Trim(), $pair[1].Trim())
    }
    Write-Host "Loaded .env" -ForegroundColor DarkGray
} else {
    Write-Host "No .env found. Copy .env.example to .env and fill in workshop values." -ForegroundColor Yellow
}

$ok = $true
$ok = (Test-EnvVar 'AZURE_OPENAI_BASE_URL') -and $ok
$ok = (Test-EnvVar 'AZURE_OPENAI_API_KEY') -and $ok
$ok = (Test-EnvVar 'AZURE_OPENAI_DEPLOYMENT') -and $ok

$base = [Environment]::GetEnvironmentVariable('AZURE_OPENAI_BASE_URL')
if ($base -and ($base -notmatch '^https://')) { Write-Host "  [WARN] BASE_URL must use https://" -ForegroundColor Yellow; $ok = $false }
if ($base -and ($base -notmatch '/openai/v1/?$')) { Write-Host "  [WARN] BASE_URL should end in /openai/v1/" -ForegroundColor Yellow; $ok = $false }

Write-Host ""
Write-Host "Detected runtimes:" -ForegroundColor Cyan
foreach ($cmd in @('python','dotnet','java')) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) { Write-Host ("  [OK] {0}" -f $cmd) -ForegroundColor Green }
    else { Write-Host ("  [not found] {0}" -f $cmd) -ForegroundColor DarkGray }
}

Write-Host ""
if ($ok) {
    Write-Host "Configuration looks good. You can run a coding track or the portal." -ForegroundColor Green
} else {
    Write-Host "Configuration incomplete. If you cannot fix the coding setup, use the portal track:" -ForegroundColor Yellow
    Write-Host "  docs/portal-setup.md" -ForegroundColor Yellow
    Write-Host "You can complete every required lab through the portal (no local code needed)." -ForegroundColor Yellow
}
