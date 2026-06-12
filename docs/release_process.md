# Release Process

1. Run `scripts/setup_dev.ps1`.
2. Prepare or validate `runtime/`.
3. Run `scripts/build_exe.ps1`.
4. Review `build/Unified-Streamlit-Launcher/checksums.sha256`.
5. Code sign `launcher.exe`.
6. Copy the release to a read-only network publishing folder.
7. Validate on a clean Windows VM.

## Clean Windows Verification Checklist

1. Copy the release folder locally.
2. Run `launcher.exe`.
3. Confirm no Python installation prompt appears.
4. Confirm 10 apps are visible.
5. Open Hello Pipeline.
6. Confirm environment creation succeeds.
7. Confirm browser opens a localhost URL.
8. Confirm the page displays `Hello`.
9. Open three apps simultaneously.
10. Confirm they use different ports.
11. Stop one app.
12. Confirm the other apps continue running.
13. Close the launcher.
14. Confirm all child Streamlit processes stop.
15. Disconnect the network drive.
16. Confirm the last local version still launches.
17. Corrupt one staged update file.
18. Confirm checksum verification rejects it.
19. Confirm logs contain useful technical details.
20. Confirm no sensitive user data appears in logs.
