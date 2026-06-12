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

## Network Drive Deployment

The release folder can live on a network drive, for example:

```text
\\server\shared\Unified-Streamlit-Launcher\
  launcher.exe
  apps/
  config/
  runtime/
```

Users who have access to the share can double-click `launcher.exe`.

On startup, the launcher:

1. reads `apps/apps.json` from the release folder;
2. copies the bundled `runtime/` folder into the user's local cache;
3. copies each registered app folder into the user's local cache;
4. creates or reuses per-app virtual environments under the local cache;
5. runs Streamlit from local cached runtime and app source, not directly from the network app folder.

Default local cache:

```text
%LOCALAPPDATA%\OrganizationName\UnifiedStreamlitPlatform
```

This keeps the shared network folder as the distribution source while avoiding slow or fragile Python execution from the network drive. Fifteen users can open the same shared `launcher.exe`; each user gets separate local runtime, app, environment, log, and state folders.

## Distribution Options

- Copy the folder to a local machine.
- Publish the folder to a read-only network share.
- Wrap the folder with an installer later using `build_scripts/installer.nsis`.

## Updating Apps After Build

Apps are not sealed inside `launcher.exe`.

To add an app after a build on the network share:

1. Copy a new app folder into `\\server\shared\Unified-Streamlit-Launcher\apps\`.
2. Add the app to `\\server\shared\Unified-Streamlit-Launcher\apps\apps.json`.
3. Ask users to restart `launcher.exe`.

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
