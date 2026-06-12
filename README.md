# Unified Streamlit Launcher

Production-oriented Windows desktop launcher for multiple Python/Streamlit applications.

![Screenshot placeholder](assets/launcher/launcher.png)

The launcher is a PySide6 desktop wrapper and process manager. It reads one simple registry file, `apps/apps.json`, prepares isolated virtual environments in a per-user local cache, starts Streamlit on dynamic `127.0.0.1` ports, waits for readiness, then opens the default browser.

## Simple Project Layout

```text
Unified-Streamlit-Launcher/
  apps/
    apps.json                  # one place to register apps
    01_hello_pipeline/         # one self-contained Streamlit app
      app.py
      requirements.txt
      README.md
      assets/icon.svg
  launcher/                    # desktop launcher framework
  build/                       # generated builds/releases go here
  scripts/
  documentation/
```

New people only need to understand:

- Put Streamlit apps in `apps/<app_folder>/`.
- Register each app in `apps/apps.json`.
- Run the launcher in development mode or build a release into `build/`.

## Development Setup

```powershell
.\scripts\setup_dev.ps1
.\scripts\run_launcher_dev.ps1
```

Development mode may fall back to the current Python interpreter when `runtime/python.exe` is not present. Production releases must include a validated portable runtime.

## Build Release

```powershell
.\scripts\prepare_runtime.ps1 -RuntimeSource C:\ApprovedPythonRuntime
.\scripts\build_release.ps1
```

The build uses PyInstaller `--onedir` and produces `build/Unified-Streamlit-Launcher`.

## Architecture

See [documentation/architecture.md](documentation/architecture.md).

## Adding Apps

See [documentation/adding_new_apps.md](documentation/adding_new_apps.md). Apps are registered in `apps/apps.json`; no launcher Python code needs editing.

## Troubleshooting

See [documentation/troubleshooting.md](documentation/troubleshooting.md).

## Icon Licensing

Demo SVG icons are locally generated placeholders. See `assets/licenses/`.

## Production Cautions

Code signing, antivirus allow-list testing, checksum verification, and clean-machine validation are required before broad stakeholder deployment.
