# Iteration 0001 Report

## Metadata

- UTC timestamp: 2026-06-12T14:02:00Z
- Branch: autoresearch/unified-launcher-20260612-baseline
- Baseline commit: 69a7277
- Area: EXE build and release verification

## Hypothesis

If the PyInstaller spec generator ignores an invalid placeholder icon and the PowerShell build wrappers propagate nonzero Python exits, the documented build command will produce a release folder instead of failing during icon conversion.

## Changes

- `build_scripts/create_pyinstaller_spec.py` now validates the `.ico` file header before passing it to PyInstaller.
- `scripts/build_exe.ps1` and `scripts/build_release.ps1` now exit with the Python build exit code when the build fails.
- `scripts/verify_release.ps1` now validates registered apps from `apps/apps.json` instead of hard-coding a directory count.
- Added regression coverage in `tests/test_build_scripts.py`.

## Evidence

| Check | Result | Evidence |
|---|---|---|
| `python -m pytest` | PASS, 44 tests | terminal run after change |
| `python -m compileall launcher build_scripts` | PASS | terminal run after change |
| `scripts/build_exe.ps1` | PASS | `.autoresearch/evidence/logs/iteration-0001-build.log` |
| `scripts/verify_release.ps1` | PASS | `.autoresearch/evidence/logs/iteration-0001-verify-release.log` |

## Release Artifact

- `build/Unified-Streamlit-Launcher/launcher.exe` exists.
- SHA256: `F7BDC9D3E42884EA18C2A2F2DDC0E5CAC530ECC49D06B034A0538E2B6FA61DC9`
- `checksums.sha256` exists.
- `release_info.json` exists.

## Decision

KEEP. The preferred local build and release verifier now pass.

## Remaining Gaps

External validation is still required on a clean Windows machine with no Python installed and on a representative read-only network share with multiple users.
