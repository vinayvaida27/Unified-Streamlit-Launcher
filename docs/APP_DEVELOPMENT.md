# App Development

Each Streamlit app is self-contained:

```text
apps/my_app/
  app.py
  requirements.txt
  README.md
  assets/icon.svg
```

Register the app in:

```text
apps/apps.json
```

Example:

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

The launcher rejects absolute paths and `..` traversal.

## Template

Copy:

```text
apps/app_template/
```

Then edit `app.py`, `requirements.txt`, `README.md`, and `assets/icon.svg`.

## Dependency Isolation

Every app version gets its own virtual environment:

```text
%LOCALAPPDATA%/OrganizationName/UnifiedStreamlitPlatform/environments/<app_id>/<version>/
```

Changing `requirements.txt` causes the environment to rebuild.
