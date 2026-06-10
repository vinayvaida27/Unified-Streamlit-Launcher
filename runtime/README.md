# Portable Runtime

Production releases require a complete relocatable Python 3.11 or 3.12 runtime in this folder with:

- `python.exe`
- `venv`
- `pip`
- SSL support
- subprocess support

The minimal CPython embeddable ZIP does not provide `venv` and `pip` without customization. Use `scripts/prepare_runtime.ps1` with an approved extracted runtime or approved organization artifact. Development mode may use the current interpreter as a fallback.
