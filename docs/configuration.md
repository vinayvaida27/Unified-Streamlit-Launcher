# Configuration

Global launcher configuration lives in:

```text
config/launcher_config.json
```

Application registration lives in:

```text
apps/apps.json
```

`apps/apps.json` has:

- `defaults`: common settings for all apps.
- `applications`: one entry per Streamlit app.

Each app entry points to files inside that app folder. Absolute paths and `..` path traversal are rejected.
