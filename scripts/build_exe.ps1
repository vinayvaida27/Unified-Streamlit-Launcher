param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host "Building Unified Streamlit Launcher EXE release..."
& (Join-Path $Root "scripts\build_release.ps1")

Write-Host ""
Write-Host "Done. Release folder:"
Write-Host (Join-Path $Root "build\Unified-Streamlit-Launcher")
