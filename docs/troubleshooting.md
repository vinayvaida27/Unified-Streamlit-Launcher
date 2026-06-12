# Troubleshooting

## App does not open

Use **View Log** on the app card. If Streamlit wrote a ready URL, the launcher should mark the app running and enable **Open**.

## First launch is slow

The launcher is creating a per-app virtual environment and installing dependencies. Later launches reuse the environment.

## Runtime missing

Production releases require `runtime/python.exe`.

Use:

```powershell
.\scripts\prepare_runtime.ps1 -RuntimeSource C:\ApprovedPythonRuntime
```

## Need to add an app after build

Edit the built release folder:

```text
build/Unified-Streamlit-Launcher/apps/
```

Add the app folder and update `apps.json`, then restart `launcher.exe`.

## Rebuild everything

```powershell
.\scripts\clean.ps1
.\scripts\build_exe.ps1
```
