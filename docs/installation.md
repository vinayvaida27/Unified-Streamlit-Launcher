# Installation

## Developer Machine

Install Python 3.11 or 3.12, then run:

```powershell
.\scripts\setup_dev.ps1
```

## End User Machine

End users do not install Python. They receive the built folder:

```text
build/Unified-Streamlit-Launcher/
```

They run:

```text
launcher.exe
```

Production releases must include a validated portable Python runtime under `runtime/`.
