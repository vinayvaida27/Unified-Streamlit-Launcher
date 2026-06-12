param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) { throw "Run scripts/setup_dev.ps1 first." }

Write-Host "Building Unified Streamlit Launcher EXE release..."
& $Python (Join-Path $Root "build_scripts\build.py")

Write-Host ""
Write-Host "Done. Release folder:"
Write-Host (Join-Path $Root "build\Unified-Streamlit-Launcher")
