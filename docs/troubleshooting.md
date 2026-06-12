# Troubleshooting

## Runtime Missing

Production requires `runtime/python.exe`. Run `scripts/prepare_runtime.ps1` with an approved runtime.

## Environment Creation Failed

Open the launcher log and app log under the local cache. Check write permissions and venv support.

## Pip Installation Failed

Use a populated app `wheelhouse` for offline installs or enable network access for development dependency installation.

## Network Share Unavailable

The launcher should continue using the last valid local version when update checks cannot reach the network share.

## Port Conflict

Ports are dynamic. Restart the app if a selected port becomes unavailable before launch.

## Startup Timeout

Open the app log. Streamlit may have crashed during import or dependency loading.

## Browser Did Not Open

Use Open again on the running card. The launcher stores the app URL after health succeeds.

## Streamlit Process Crashed

View the app log. The process manager marks crashed apps failed and clears stale state.

## Icon Missing

Invalid manifests with missing icons are skipped and logged. Add `assets/icon.svg`.

## Network Share Unavailable

Confirm the UNC path and user read permissions.
