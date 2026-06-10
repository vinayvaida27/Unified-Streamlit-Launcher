param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$VenvDir = Join-Path $Root ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

if (!(Test-Path $VenvPython)) {
  $Created = $false
  foreach ($Version in @("3.12", "3.11")) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
      cmd /c "py -$Version -m venv ""$VenvDir"" >nul 2>nul"
      if ($LASTEXITCODE -eq 0 -and (Test-Path $VenvPython)) {
        $Created = $true
        break
      }
      Write-Host "Python $Version was not available for dev venv creation."
    }
  }

  if (!$Created) {
    throw @"
No Python 3.11 or 3.12 interpreter was found.

Install one, then rerun this script. For example:
  winget install --id Python.Python.3.12 -e

From cmd.exe, use:
  powershell -ExecutionPolicy Bypass -File .\scripts\setup_dev.ps1
"@
  }
}

& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r (Join-Path $Root "requirements-dev.txt")
& $VenvPython -c "import PySide6, streamlit; print('PySide6 and Streamlit validated')"

Write-Host "Development environment ready."
Write-Host "Run: powershell -ExecutionPolicy Bypass -File .\scripts\run_launcher_dev.ps1"
