param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) { throw "Run scripts/setup_dev.ps1 first." }

& $Python (Join-Path $Root "build_scripts\build.py")
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}
