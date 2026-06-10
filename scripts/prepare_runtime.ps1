param([string]$RuntimeSource)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$RuntimeDir = Join-Path $Root "runtime"
if (!$RuntimeSource) { throw "Provide -RuntimeSource pointing to an approved extracted Python runtime directory." }
if (!(Test-Path $RuntimeSource)) { throw "Runtime source does not exist: $RuntimeSource" }

Get-ChildItem $RuntimeDir -Force | Where-Object { $_.Name -notin @("README.md", ".gitkeep") } | Remove-Item -Recurse -Force
Copy-Item -Recurse -Force (Join-Path $RuntimeSource "*") $RuntimeDir
$Python = Join-Path $RuntimeDir "python.exe"
if (!(Test-Path $Python)) { throw "Copied runtime does not contain python.exe" }

& $Python -c "import ssl, subprocess, venv, pip, platform, json, pathlib, datetime; p=pathlib.Path('runtime/runtime_info.json'); p.write_text(json.dumps({'python_version': platform.python_version(), 'architecture': platform.architecture()[0], 'validated': True, 'validated_at': datetime.datetime.utcnow().isoformat() + 'Z'}, indent=2), encoding='utf-8')"
$TestVenv = Join-Path $RuntimeDir "_venv_validation"
& $Python -m venv $TestVenv
Remove-Item -Recurse -Force $TestVenv
Write-Host "Runtime validated at $RuntimeDir"
