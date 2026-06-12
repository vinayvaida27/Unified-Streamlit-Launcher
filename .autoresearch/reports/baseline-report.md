# Baseline Report

## Metadata

- UTC timestamp: 2026-06-12T13:48:02.4898746Z
- Branch: autoresearch/unified-launcher-20260612-baseline
- Commit: 69a7277
- Repository: Unified-Streamlit-Launcher

## Baseline Commands

- python -m pytest
- python -m compileall launcher build_scripts
- powershell -ExecutionPolicy Bypass -File .\scripts\build_exe.ps1

## Results

| Check | Status | Evidence |
|---|---|---|
| Repository clean at start | PASS | .autoresearch/evidence/commands/git-status-baseline.txt |
| Pytest suite | PASS | .autoresearch/evidence/logs/baseline-tests.log |
| Compile launcher/build scripts | PASS | .autoresearch/evidence/logs/baseline-compileall.log |
| Preferred build command | FAIL | .autoresearch/evidence/logs/baseline-build.log |
| Release folder created | FAIL | .autoresearch/evidence/artifacts/baseline-release-tree.txt |
| launcher.exe hash captured | FAIL | launcher.exe was not created |

## Observed Build Failure

PyInstaller failed while processing `assets/launcher/launcher.ico` because the file is a placeholder text file, not a valid ICO. The PowerShell wrapper still printed a completion message and returned success-like control flow in this capture path, so build failure reporting also needs hardening.

## Release Readiness

NOT APPROVED FOR RELEASE. The preferred build does not currently produce `build/Unified-Streamlit-Launcher/launcher.exe`.

## Next Highest-Value Experiment

Hypothesis: if the spec generator validates the launcher icon before including it and the PowerShell wrappers propagate Python build failures, the preferred build will fail honestly or proceed past the placeholder icon issue.
