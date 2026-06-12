# Deployment

The recommended deployment is a portable folder:

```text
Unified-Streamlit-Launcher/
  launcher.exe
  apps/
  config/
  runtime/
  docs/
```

Users run `launcher.exe`. They do not install Python.

## Distribution Options

- Copy the folder to a local machine.
- Publish the folder to a read-only network share.
- Wrap the folder with an installer later using `build_scripts/installer.nsis`.

## Updating Apps After Build

Apps are not sealed inside `launcher.exe`.

To add an app after a build:

1. Copy a new app folder into `apps/`.
2. Add the app to `apps/apps.json`.
3. Restart `launcher.exe`.

The launcher will create or reuse that app's per-user virtual environment when the app is opened.

## Production Runtime

Production releases should include a complete portable Python runtime under `runtime/`.

The runtime must support:

- `python.exe`
- `venv`
- `pip`
- SSL
- subprocesses

The CPython embeddable ZIP is not enough unless customized to support `venv` and `pip`.

## Build Pipeline

The release folder is produced by:

```powershell
.\scripts\build_exe.ps1
```

Internally this calls `build_scripts/build.py`, which generates a PyInstaller spec, builds `launcher.exe`, copies external app/config/runtime folders, writes checksums, and verifies the release structure.
