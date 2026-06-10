# Unified Streamlit Launcher

Production-oriented Windows desktop launcher for multiple Python/Streamlit applications.

![Screenshot placeholder](assets/launcher/launcher.png)

The launcher is a PySide6 desktop wrapper and process manager. It discovers app manifests under `apps/`, prepares isolated virtual environments in a per-user local cache, starts Streamlit on dynamic `127.0.0.1` ports, waits for health, then opens the default browser.

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

The build uses PyInstaller `--onedir` and produces `build/release/UnifiedStreamlitPlatform`.

## Architecture

See [documentation/architecture.md](documentation/architecture.md).

## Adding Apps

See [documentation/adding_new_apps.md](documentation/adding_new_apps.md). Apps are discovered dynamically; no Python app list needs editing.

## Troubleshooting

See [documentation/troubleshooting.md](documentation/troubleshooting.md).

## Icon Licensing

Demo SVG icons are locally generated placeholders. See `assets/licenses/`.

## Production Cautions

Code signing, antivirus allow-list testing, checksum verification, and clean-machine validation are required before broad stakeholder deployment.
