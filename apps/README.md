# Apps Folder

This folder is the app-maintenance area.

```text
apps/
  apps.json
  my_new_app/
    app.py
    requirements.txt
    README.md
    assets/icon.svg
```

To add a new app:

1. Copy an existing app folder or create a new folder.
2. Put the Streamlit entry file and dependency files inside that folder.
3. Add one entry to `apps/apps.json`.
4. Restart the launcher.

The launcher does not need Python code changes when apps are added.
