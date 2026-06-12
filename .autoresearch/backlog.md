# Autoresearch Backlog

### Issue ID: UDL-001

**Title:** Preferred EXE build fails on invalid placeholder launcher icon  
**Severity:** CRITICAL  
**Status:** RESOLVED IN ITERATION 0001  
**Related tests:** preferred build, release verifier  
**Affected modules:** `build_scripts/create_pyinstaller_spec.py`, `assets/launcher/launcher.ico`, `scripts/build_exe.ps1`  
**User-visible impact:** New developers cannot build the release EXE reliably.  
**Observed behavior:** PyInstaller fails with UnidentifiedImageError for `assets/launcher/launcher.ico`.  
**Expected behavior:** Build either uses a valid icon or omits the invalid icon and completes release assembly.  
**Evidence paths:** .autoresearch/evidence/logs/baseline-build.log  
**Proposed next experiment:** Validate icon before including it in generated spec; harden PowerShell wrapper failure propagation.

**Resolution:** The spec generator now ignores invalid placeholder ICO files, and build wrappers propagate failed Python build exit codes. The preferred build now creates `launcher.exe`, `checksums.sha256`, and `release_info.json`.

### Issue ID: UDL-002

**Title:** Release verifier hard-codes app directory count  
**Severity:** MEDIUM  
**Status:** RESOLVED IN ITERATION 0001  
**Related tests:** release verifier  
**Affected modules:** `scripts/verify_release.ps1`  
**User-visible impact:** Valid releases with `apps/app_template` fail verification even when all registered apps are present.  
**Observed behavior:** Verifier expected exactly 10 directories under `apps`, but the framework structure also includes `app_template`.  
**Expected behavior:** Verifier reads `apps/apps.json`, validates registered app folders and entrypoints, and ignores template/support folders.  
**Evidence paths:** `.autoresearch/evidence/logs/iteration-0001-verify-release.log`

### Blocked Test: B1 - Clean machine without Python

**Missing prerequisite:** Clean Windows machine or VM with no Python installed.  
**Why current evidence is insufficient:** Development machine has Python installed.  
**Exact external procedure:** Copy built release to clean VM, confirm Python absent, run launcher.exe, open Hello Pipeline, inspect process paths.  
**Pass criteria:** No Python prompt; child process uses local cached portable runtime; app opens.  
**Release risk if skipped:** No-Python end-user claim remains unverified.

### Blocked Test: B2 - Representative multi-user network-share test

**Missing prerequisite:** Read-only UNC share and at least two Windows users or machines.  
**Why current evidence is insufficient:** Unit tests simulate local cache behavior but not share permissions or concurrent users.  
**Exact external procedure:** Publish release to read-only share, run from two standard-user machines, open apps, inspect local cache/log paths.  
**Pass criteria:** No writes to share; each user has independent local runtime/apps/env/logs.  
**Release risk if skipped:** Multi-user network deployment remains partially unverified.
