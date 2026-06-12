# Build EXE

This project builds a portable Windows folder, not a fragile single-file bundle.

```text
build/Unified-Streamlit-Launcher/
  launcher.exe
  config/
  apps/
  assets/
  runtime/
  docs/
```

`launcher.exe` is the desktop process manager. The apps remain external so teams can add or update apps later without rebuilding launcher code.

## Prerequisites

- Windows
- Python 3.11 or 3.12 for development
- A validated portable Python runtime under `runtime/` for production distribution

## Setup

```powershell
.\scripts\setup_dev.ps1
```

## Build

```powershell
.\scripts\build_exe.ps1
```

Equivalent Python command:

```powershell
.\.venv\Scripts\python.exe build_scripts\build.py
```

## Build Steps

The builder performs:

1. clean previous build output;
2. run tests;
3. generate `build/launcher.spec`;
4. run PyInstaller;
5. copy `apps/`, `config/`, `assets/`, `runtime/`, and `docs/`;
6. generate `checksums.sha256`;
7. verify the release structure.

## Output

```text
build/Unified-Streamlit-Launcher/launcher.exe
```

Double-click `launcher.exe` to run the launcher.

## Optional Signing

Use `build_scripts/sign_exe.py` as a hook for organization code signing:

```powershell
python build_scripts\sign_exe.py --signtool C:\Path\signtool.exe --cert-subject "Your Certificate"
```
