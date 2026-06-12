param([string]$Config = "config\launcher_config.json")

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) {
  $Python = (Get-Command python).Source
}
& $Python -m launcher --development --config (Join-Path $Root $Config)
