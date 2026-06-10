param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Release = Join-Path $Root "build\release\UnifiedStreamlitPlatform"
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) { throw "Run scripts/setup_dev.ps1 first." }

Remove-Item -Recurse -Force (Join-Path $Root "build\release") -ErrorAction SilentlyContinue
& $Python -m pytest
& (Join-Path $PSScriptRoot "build_launcher.ps1")

New-Item -ItemType Directory -Force -Path $Release | Out-Null
Copy-Item -Recurse -Force (Join-Path $Root "build\pyinstaller\launcher\*") $Release
Copy-Item -Force (Join-Path $Root "launcher_config.json") $Release
Copy-Item -Force (Join-Path $Root "platform_manifest.json") $Release
Copy-Item -Recurse -Force (Join-Path $Root "apps") $Release
Copy-Item -Recurse -Force (Join-Path $Root "assets") $Release
Copy-Item -Recurse -Force (Join-Path $Root "documentation") $Release
Copy-Item -Recurse -Force (Join-Path $Root "runtime") $Release
& (Join-Path $PSScriptRoot "generate_checksums.ps1") -Path $Release
& (Join-Path $PSScriptRoot "verify_release.ps1") -Path $Release
Write-Host "Release created at $Release"
