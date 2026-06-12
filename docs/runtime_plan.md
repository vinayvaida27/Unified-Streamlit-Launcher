# Python Runtime Plan

Goal: one installation for non-technical users. The launcher always runs apps on
its **own private Python**. It must **never** use a Python already installed on
the user's machine, even if one exists.

## Runtime resolution order (production)

1. **Bundled runtime (preferred)** — `runtime/python.exe` shipped inside the
   release folder. Copied to the user's local cache on first start. Works
   offline, deterministic, no admin rights.
2. **Auto-download (fallback)** — if `runtime/` is missing or invalid, the
   launcher downloads a **pinned official CPython release** from the internet,
   verifies its SHA-256, extracts it into the per-user cache, validates it
   (venv + pip + ssl), and uses it. The download is per-user, needs no admin
   rights, and does not register itself in PATH or the registry.
3. **System Python — never.** No PATH lookup, no `py` launcher, no registry
   detection. The development-interpreter fallback is disabled in production
   builds (`allow_development_interpreter_fallback: false` in the release
   config).

## Download source (fallback)

- Use the official **python.org / PSF "python" NuGet package** (full portable
  CPython with pip and venv) or an official python.org build — pinned exact
  version (3.11.x or 3.12.x) and SHA-256 in `config/launcher_config.json`:

```json
"runtime": {
  "download": {
    "enabled": true,
    "version": "3.11.9",
    "url": "https://globalcdn.nuget.org/packages/python.3.11.9.nupkg",
    "sha256": "<pinned-hash>"
  }
}
```

- Note: the plain "embeddable zip" from python.org is NOT suitable (no venv,
  no pip). The NuGet package layout is suitable.
- Download goes to `%LOCALAPPDATA%\...\runtime\downloads\<version>\`, with a
  progress dialog in the launcher UI and a clear error message (with retry)
  if the machine is offline.

## Isolation guarantees (no system-Python contamination)

- Subprocesses already run with `PYTHONNOUSERSITE=1`; additionally scrub
  `PYTHONPATH`, `PYTHONHOME`, and `PYTHONSTARTUP` from the child environment.
- Runtime validation (version window 3.11–3.12, ssl/venv/pip import check)
  runs against the cached private runtime only, fail-closed.
- Per-app venvs are always created from the private runtime; the venv marker
  records the runtime fingerprint so venvs rebuild automatically when the
  runtime is updated.

## Phases

1. **Code fixes (in progress)** — config-path anchoring (done), clean stop of
   starting apps (done), crash detection (done), runtime fingerprint in venv
   markers, pip output streamed to app logs with timeout, dynamic category
   filter, tests.
2. **Runtime downloader module** — `launcher/runtime_downloader.py` +
   config schema + progress UI + tests (mocked download).
3. **Prepare bundled runtime** — run `scripts\prepare_runtime.ps1` against an
   official portable CPython 3.11; verify `runtime/python.exe -m venv` works.
4. **Build & verify** — `scripts\build_exe.ps1`; test the release folder on a
   clean Windows machine/VM **without Python installed**: double-click
   `launcher.exe`, open two apps, stop, restart, view logs.
5. **Distribute** — copy folder to network share (read-only for users) or
   build the NSIS one-click installer; optional code signing.

## Acceptance criteria

- A machine with no Python: launcher starts and runs apps (bundled runtime),
  or downloads its own runtime if the bundle is absent.
- A machine **with** Python installed: launcher demonstrably never invokes it
  (verify via Process Explorer: all `python.exe` paths are under the launcher
  cache).
- Two apps run side by side on different ports; Stop/Restart/View Log work;
  closing the launcher stops all apps.
