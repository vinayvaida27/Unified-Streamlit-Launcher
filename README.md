# Unified Streamlit Launcher

Windows desktop launcher for many independent Streamlit apps.

The important idea is simple:

- `launcher/` is the reusable desktop framework.
- `apps/` contains Streamlit applications.
- `apps/apps.json` is the only app registry people normally edit.
- `build/Unified-Streamlit-Launcher/` is the generated folder you give to users.

Nontechnical users should run the built `launcher.exe`. They should not install Python, run PowerShell, or edit launcher code.

## Repository Layout

```text
Unified-Streamlit-Launcher/
  launcher/                 # Core PySide6 launcher framework
  apps/                     # Streamlit apps and central registry
    apps.json
    app_template/
    01_hello_pipeline/
    02_second_app/
  config/                   # Global launcher config
    launcher_config.json
    platform_manifest.json
  runtime/                  # Portable Python runtime for production builds
  scripts/                  # Setup/build/release scripts
  build/                    # Generated releases
  docs/                     # User and deployment documentation
  tests/
```

## Developer Quickstart

Use Windows PowerShell:

```powershell
.\scripts\setup_dev.ps1
.\scripts\run_launcher_dev.ps1
```

Development requires Python 3.11 or 3.12. The dev launcher can use the local interpreter while production builds use `runtime/python.exe`.

## Build The EXE Release

1. Prepare or copy an approved portable Python runtime into `runtime/`.
2. Run:

```powershell
.\scripts\build_release.ps1
```

Shortcut:

```powershell
.\scripts\build_exe.ps1
```

Output:

```text
build/Unified-Streamlit-Launcher/
  launcher.exe
  config/
  apps/
  assets/
  runtime/
  docs/
```

Users can copy that folder and double-click `launcher.exe`.

## Add Apps After Building

The apps are external to the executable. After a release is built, you can add or replace apps in the release folder:

```text
build/Unified-Streamlit-Launcher/apps/
  apps.json
  my_new_app/
    app.py
    requirements.txt
    README.md
    assets/icon.svg
```

Then add the app to `apps/apps.json` and restart `launcher.exe`.

## Documentation

- [Quickstart](docs/quickstart.md)
- [Creating apps](docs/creating_apps.md)
- [Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Architecture](docs/architecture.md)

## Validation

```powershell
python -m pytest
```

The framework includes tests for config loading, app registry validation, path security, environment paths, process launch commands, health checks, and updates.
