param()

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (!(Test-Path $Python)) { throw "Run scripts/setup_dev.ps1 first." }
& $Python -m PyInstaller --clean --noconsole --onedir --name launcher --distpath (Join-Path $Root "build\pyinstaller") (Join-Path $Root "launcher\__main__.py")
