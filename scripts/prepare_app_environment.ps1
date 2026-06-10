param([Parameter(Mandatory=$true)][string]$AppId)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) { throw "Run scripts/setup_dev.ps1 first." }
& $Python -c "print('Prepare individual app environments through the launcher UI, or call EnvironmentManager from a small maintenance command. Requested app: $AppId')"
