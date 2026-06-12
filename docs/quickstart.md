# Quickstart

## For Developers

```powershell
git clone https://github.com/vinayvaida27/Unified-Streamlit-Launcher.git
cd Unified-Streamlit-Launcher
.\scripts\setup_dev.ps1
.\scripts\run_launcher_dev.ps1
```

## Build A Release

```powershell
.\scripts\prepare_runtime.ps1 -RuntimeSource C:\ApprovedPythonRuntime
.\scripts\build_exe.ps1
```

The release is created at:

```text
build/Unified-Streamlit-Launcher
```

Run:

```text
build/Unified-Streamlit-Launcher/launcher.exe
```

## Add A New App

1. Copy `apps/app_template` to a new folder.
2. Edit `app.py` and `requirements.txt`.
3. Add one entry to `apps/apps.json`.
4. Restart the launcher.
