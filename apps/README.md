# Apps Folder

This folder is the app-maintenance area.

```text
apps/
  apps.json
  app_template/
  my_new_app/
    app.py
    requirements.txt
    README.md
    assets/icon.svg
```

To add a new app:

1. Copy `app_template` or create a new folder.
2. Put the Streamlit entry file and dependency files inside that folder.
3. Add one entry to `apps/apps.json`.
4. Restart the launcher.

The launcher does not need Python code changes when apps are added. In a built release, edit the release folder's `apps/` directory the same way and restart `launcher.exe`.
