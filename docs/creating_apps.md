# Adding New Apps

Copy `apps/app_template` or create a folder under `apps/` containing everything that app needs:

```text
app.py
requirements.txt
README.md
assets/icon.svg
```

Then register it in `apps/apps.json`.

Example folder:

```text
apps/11_ab1file_process/
  app.py
  requirements.txt
  README.md
  assets/icon.svg
```

Example `apps/apps.json` entry:

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

Most fields such as app type, Python version, wheelhouse, and launch settings come from the `defaults` section of `apps/apps.json`.

Restart the launcher. No Python list and no launcher code needs editing.

The same pattern works after building the `.exe`: add the app folder under `build/Unified-Streamlit-Launcher/apps/`, update `build/Unified-Streamlit-Launcher/apps/apps.json`, then restart `launcher.exe`.
