# Deployment

Publish the portable release folder from `build/Unified-Streamlit-Launcher` to a read-only network location such as `\\server\shared\UnifiedStreamlitPlatform\Published`. Application code and environments should be synchronized to `%LOCALAPPDATA%\OrganizationName\UnifiedStreamlitPlatform` before execution.

Prepare a runtime with `scripts/prepare_runtime.ps1`. Validate on a clean Windows machine without Python installed.

Code sign `launcher.exe` and document the certificate chain. Test antivirus behavior before broad rollout and add allow-list rules only for the signed release path and local cache paths approved by IT.

Never overwrite a running launcher executable in place. Use a bootstrapper/updater pattern for future production self-updates.
