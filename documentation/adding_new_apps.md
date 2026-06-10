# Adding New Apps

Create a folder under `apps/` containing:

```text
app.py
app_manifest.json
requirements.txt
README.md
assets/icon.svg
```

Example manifest:

```json
{
  "schema_version": 1,
  "id": "eleventh-app",
  "name": "Eleventh App",
  "version": "1.0.0",
  "description": "A new Streamlit application.",
  "category": "Demonstration",
  "type": "streamlit",
  "entrypoint": "app.py",
  "icon": "assets/icon.svg",
  "requirements": "requirements.txt",
  "wheelhouse": "wheelhouse",
  "python_version": "3.11",
  "enabled": true,
  "display_order": 11,
  "launch": {
    "address": "127.0.0.1",
    "port": "dynamic",
    "headless": true,
    "file_watcher_type": "none",
    "gather_usage_stats": false,
    "startup_timeout_seconds": 60
  }
}
```

Restart the launcher or add a future refresh action. No Python list needs editing.
