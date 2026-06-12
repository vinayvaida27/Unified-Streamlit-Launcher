# Project Context: Unified Streamlit Launcher

Use this file as context for ChatGPT or another assistant when asking questions about this repository, build errors, deployment, adding apps, or troubleshooting.

## What This Project Is

`Unified-Streamlit-Launcher` is a Windows desktop launcher for multiple independent Streamlit applications.

The intended nontechnical-user experience is:

1. A user opens a shared network drive or copied release folder.
2. The user double-clicks `launcher.exe`.
3. A Windows desktop launcher window opens.
4. The launcher shows app cards from `apps/apps.json`.
5. The user clicks **Open**, **Open All**, **Stop**, **Restart**, or **View Log**.
6. The launcher creates/reuses each app's isolated virtual environment.
7. Streamlit starts on a dynamic `127.0.0.1` port.
8. The browser opens to the running Streamlit app.

The launcher itself is a PySide6 desktop app. It is not a Streamlit app.

## Repository URL

GitHub:

```text
https://github.com/vinayvaida27/Unified-Streamlit-Launcher
```

## Current Architecture

```text
Unified-Streamlit-Launcher/
├── launcher/                  # Core PySide6 launcher framework
│   ├── main.py
│   ├── app_discovery.py
│   ├── config_loader.py
│   ├── environment_manager.py
│   ├── process_manager.py
│   ├── health_checker.py
│   ├── local_cache.py
│   ├── models.py
│   └── ui/
│       ├── main_window.py
│       ├── app_card.py
│       ├── log_dialog.py
│       └── styles.py
│
├── apps/                      # Streamlit apps and central app registry
│   ├── apps.json              # Main app registry
│   ├── app_template/          # Copy this to create a new app
│   ├── 01_hello_pipeline/
│   ├── 02_second_app/
│   └── ...
│
├── config/
│   ├── launcher_config.json   # Global launcher configuration
│   └── platform_manifest.json
│
├── runtime/                   # Portable Python runtime for production
│   └── README.md
│
├── build/                     # Generated build output
│   └── Unified-Streamlit-Launcher/
│       └── launcher.exe
│
├── build_scripts/             # Python build pipeline
│   ├── build.py
│   ├── create_pyinstaller_spec.py
│   ├── bundle_venvs.py
│   ├── sign_exe.py
│   └── installer.nsis
│
├── scripts/                   # PowerShell wrapper scripts
│   ├── setup_dev.ps1
│   ├── run_launcher_dev.ps1
│   ├── build_exe.ps1
│   ├── build_release.ps1
│   ├── prepare_runtime.ps1
│   └── verify_release.ps1
│
├── docs/
├── tests/
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── requirements-build.txt
└── README.md
```

## Key Design Decisions

### Portable Folder, Not Single-File EXE

The production output is a portable folder:

```text
build/Unified-Streamlit-Launcher/
  launcher.exe
  apps/
  config/
  runtime/
  docs/
```

This is intentional. Apps are external to `launcher.exe`, so new apps can be added later without rebuilding launcher code.

### Network Drive Distribution

The release folder may live on a network drive:

```text
\\server\shared\Unified-Streamlit-Launcher\
  launcher.exe
  apps/
  config/
  runtime/
```

Multiple users can double-click the same shared `launcher.exe`.

### Local Per-User Execution

Even if `launcher.exe` is opened from a network share, Python and Streamlit should not run directly from the network folder.

At startup, the launcher copies the runtime and app source folders into each user's local cache:

```text
%LOCALAPPDATA%\OrganizationName\UnifiedStreamlitPlatform\
  runtime\current\python.exe
  apps\<app_id>\<version>\
  environments\<app_id>\<version>\
  logs\
  state\
```

Each user gets separate local runtime, apps, virtual environments, logs, and state.

### No Python Required For End Users

Production users should not install Python. A production release must include a portable Python runtime under:

```text
runtime/python.exe
```

The runtime must support:

- `python.exe`
- `venv`
- `pip`
- SSL
- subprocesses

The minimal CPython embeddable ZIP is not enough unless customized for `venv` and `pip`.

## Development Commands

From PowerShell in the repo root:

```powershell
.\scripts\setup_dev.ps1
.\scripts\run_launcher_dev.ps1
```

If script execution is blocked:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_dev.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\run_launcher_dev.ps1
```

Development requires Python 3.11 or 3.12.

## Build Commands

Preferred build command:

```powershell
.\scripts\build_exe.ps1
```

Equivalent Python command:

```powershell
.\.venv\Scripts\python.exe build_scripts\build.py
```

The builder:

1. Cleans previous build output.
2. Runs tests.
3. Generates `build/launcher.spec`.
4. Runs PyInstaller.
5. Copies `apps/`, `config/`, `assets/`, `runtime/`, and `docs/`.
6. Generates `checksums.sha256`.
7. Verifies release structure.

Output:

```text
build/Unified-Streamlit-Launcher/launcher.exe
```

## App Registry

Apps are registered in:

```text
apps/apps.json
```

There are defaults:

```json
{
  "type": "streamlit",
  "entrypoint": "app.py",
  "icon": "assets/icon.svg",
  "requirements": "requirements.txt",
  "wheelhouse": "wheelhouse",
  "python_version": "3.11",
  "enabled": true
}
```

Each app entry looks like:

```json
{
  "id": "hello-pipeline",
  "folder": "01_hello_pipeline",
  "name": "Hello Pipeline",
  "version": "1.0.0",
  "description": "A minimal Streamlit application that displays a hello message.",
  "category": "Demonstration",
  "display_order": 1
}
```

The launcher rejects unsafe paths such as absolute paths or `..` traversal.

## Adding A New App

1. Copy:

```text
apps/app_template/
```

2. Rename the copied folder, for example:

```text
apps/11_ab1file_process/
```

3. Edit:

```text
apps/11_ab1file_process/app.py
apps/11_ab1file_process/requirements.txt
apps/11_ab1file_process/README.md
apps/11_ab1file_process/assets/icon.svg
```

4. Add an entry to `apps/apps.json`:

```json
{
  "id": "ab1file-process",
  "folder": "11_ab1file_process",
  "name": "AB1 File Process",
  "version": "1.0.0",
  "description": "Process AB1 files with a Streamlit interface.",
  "category": "Bioinformatics",
  "display_order": 11,
  "entrypoint": "app.py",
  "icon": "assets/icon.svg",
  "requirements": "requirements.txt"
}
```

5. Restart the launcher.

After building, the same pattern works inside:

```text
build/Unified-Streamlit-Launcher/apps/
```

That means apps can be added after building once, as long as the new app folder and `apps/apps.json` are updated in the release folder or network share.

## Important Runtime Flow

On launcher startup:

1. Load `config/launcher_config.json`.
2. Create local cache folders under `%LOCALAPPDATA%`.
3. Discover apps from `apps/apps.json`.
4. Copy app folders into local cache.
5. Resolve `runtime/python.exe`.
6. In production, copy the runtime into local cache and validate the local copy.
7. Show PySide6 desktop UI.

When user opens an app:

1. Check app-specific environment marker.
2. Create venv if needed.
3. Install dependencies from app `requirements.txt`.
4. Start Streamlit with:

```text
python -m streamlit run app.py --server.address 127.0.0.1 --server.port <dynamic>
```

5. Poll Streamlit health and watch log for ready URL.
6. Open browser only after app is ready.
7. Track process for Stop, Restart, Open, and View Log.

## Core Files To Inspect For Bugs

- App discovery: `launcher/app_discovery.py`
- Config loading: `launcher/config_loader.py`
- Runtime and venv creation: `launcher/environment_manager.py`
- Network/local cache sync: `launcher/local_cache.py`
- Process launch/stop/restart: `launcher/process_manager.py`
- Streamlit readiness: `launcher/health_checker.py`
- Main UI: `launcher/ui/main_window.py`
- App card UI: `launcher/ui/app_card.py`
- Build pipeline: `build_scripts/build.py`

## Logs

Logs are written under the local cache:

```text
%LOCALAPPDATA%\OrganizationName\UnifiedStreamlitPlatform\logs\
```

Each app has an app-specific log, for example:

```text
hello-pipeline.log
```

The launcher UI has a **View Log** button per app.

## Common Problems And What To Check

### Launcher says runtime missing

Production needs:

```text
runtime/python.exe
```

Run:

```powershell
.\scripts\prepare_runtime.ps1 -RuntimeSource C:\ApprovedPythonRuntime
```

### User machine has no Python

That is expected. End users do not need Python. The built release must include `runtime/`.

### App first launch is slow

The launcher is creating a local venv and installing dependencies. Later launches reuse the environment.

### App opens in browser but card still says starting

Check:

- `launcher/health_checker.py`
- app log ready URL
- `launcher/ui/main_window.py`, especially the timer that syncs ready logs

### App works for one user but not another

Each user has a separate local cache. Check that user's:

```text
%LOCALAPPDATA%\OrganizationName\UnifiedStreamlitPlatform\
```

Also check network permissions and app log files.

### Adding app does not show in launcher

Check:

- app folder exists under `apps/`
- app entry exists in `apps/apps.json`
- `enabled` is not false
- `id` is lowercase kebab-case, like `ab1file-process`
- `entrypoint`, `requirements`, and `icon` exist inside the app folder

### App dependency install fails

Check the app-specific log and the app's `requirements.txt`.

For offline production, add wheel files under the app's `wheelhouse/` folder and keep `offline_install_preferred` enabled in config.

## Testing

Run:

```powershell
python -m pytest
```

Current test coverage includes:

- configuration loading
- app registry discovery
- path security
- port allocation
- environment path and marker behavior
- process command building
- health checks
- update/checksum logic
- local app/runtime cache sync

## Current Expected Test Count

At the time this context file was created, the suite had 42 tests passing.

## Build Output Should Contain

```text
build/Unified-Streamlit-Launcher/
  launcher.exe
  config/launcher_config.json
  config/platform_manifest.json
  apps/apps.json
  apps/app_template/app.py
  assets/
  runtime/
  docs/
  checksums.sha256
  release_info.json
```

## Important Deployment Advice

For a network drive with many users:

- Make the network release folder read-only for normal users.
- Let app maintainers update `apps/` and `apps/apps.json`.
- Users only double-click `launcher.exe`.
- Each user gets independent local cache and venvs.
- Do not ask users to install Python.
- Code signing is recommended before broad distribution.

