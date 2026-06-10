"""Virtual environment management for applications."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from .exceptions import DependencyInstallationError, EnvironmentCreationError, RuntimeNotFoundError, RuntimeValidationError
from .models import ApplicationManifest, EnvironmentState, PlatformConfig
from .path_utils import atomic_write_json


class RuntimeResolver:
    """Resolves and validates the Python runtime."""

    def __init__(self, config: PlatformConfig, development_mode: bool = False) -> None:
        self.config = config
        self.development_mode = development_mode

    def resolve(self) -> Path:
        """Resolve the runtime path according to production/development rules."""

        runtime_python = self.config.paths.runtime_python
        if runtime_python.exists():
            self.validate(runtime_python)
            return runtime_python
        if self.development_mode and self.config.runtime.allow_development_interpreter_fallback:
            fallback = Path(sys.executable)
            self.validate(fallback)
            return fallback
        raise RuntimeNotFoundError(f"Bundled runtime is missing: {runtime_python}")

    def validate(self, python_path: Path) -> None:
        """Validate Python version, venv, pip, SSL, and subprocess support."""

        if not python_path.exists():
            raise RuntimeNotFoundError(str(python_path))
        script = "import ssl, subprocess, venv, pip, sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
        result = subprocess.run([str(python_path), "-c", script], capture_output=True, text=True, timeout=20)
        if result.returncode != 0:
            raise RuntimeValidationError(result.stderr.strip() or "Runtime validation failed")
        major, minor, *_ = result.stdout.strip().split(".")
        if (int(major), int(minor)) < (3, 11) or (int(major), int(minor)) >= (3, 13):
            raise RuntimeValidationError(f"Unsupported Python version: {result.stdout.strip()}")


class EnvironmentManager:
    """Creates and validates per-app/per-version virtual environments."""

    def __init__(self, config: PlatformConfig, runtime_python: Path) -> None:
        self.config = config
        self.runtime_python = runtime_python
        self.environments_dir = config.paths.local_cache_directory / "environments"

    def environment_path_for(self, app: ApplicationManifest) -> Path:
        """Return deterministic environment path for an app version."""

        return self.environments_dir / app.id / app.version

    def venv_python_for(self, environment_path: Path) -> Path:
        """Return the Python executable path inside a Windows venv."""

        if sys.platform == "win32":
            return environment_path / "Scripts" / "python.exe"
        return environment_path / "bin" / "python"

    def marker_path_for(self, environment_path: Path) -> Path:
        return environment_path / ".environment_ready.json"

    def requirements_hash(self, requirements_path: Path) -> str:
        """Return SHA-256 for requirements file."""

        digest = hashlib.sha256()
        digest.update(requirements_path.read_bytes())
        return digest.hexdigest()

    def is_ready(self, app: ApplicationManifest) -> bool:
        """Return whether an environment marker matches current inputs."""

        env_path = self.environment_path_for(app)
        marker = self.marker_path_for(env_path)
        python_path = self.venv_python_for(env_path)
        if not marker.exists() or not python_path.exists():
            return False
        try:
            data = json.loads(marker.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return False
        return (
            data.get("app_id") == app.id
            and data.get("app_version") == app.version
            and data.get("requirements_sha256") == self.requirements_hash(app.requirements)
        )

    def pip_install_command(self, app: ApplicationManifest, venv_python: Path) -> list[str]:
        """Build the dependency installation command."""

        command = [str(venv_python), "-m", "pip", "install"]
        if self.config.runtime.offline_install_preferred and app.wheelhouse.exists() and any(app.wheelhouse.iterdir()):
            command.extend(["--no-index", "--find-links", str(app.wheelhouse)])
        command.extend(["-r", str(app.requirements)])
        return command

    def ensure_environment(self, app: ApplicationManifest, progress=None) -> EnvironmentState:
        """Create or reuse an app environment."""

        env_path = self.environment_path_for(app)
        venv_python = self.venv_python_for(env_path)
        marker_path = self.marker_path_for(env_path)
        if progress:
            progress("Checking environment")
        if self.is_ready(app):
            return EnvironmentState(app.id, app.version, env_path, venv_python, True, marker_path)
        env_path.parent.mkdir(parents=True, exist_ok=True)
        if progress:
            progress("Creating virtual environment")
        result = subprocess.run([str(self.runtime_python), "-m", "venv", str(env_path)], capture_output=True, text=True)
        if result.returncode != 0:
            raise EnvironmentCreationError(result.stderr.strip() or "Virtual environment creation failed")
        if progress:
            progress("Installing dependencies")
        pip_cmd = self.pip_install_command(app, venv_python)
        result = subprocess.run(pip_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise DependencyInstallationError(result.stderr.strip() or "Dependency installation failed")
        if progress:
            progress("Validating environment")
        result = subprocess.run([str(venv_python), "-c", "import streamlit"], capture_output=True, text=True)
        if result.returncode != 0:
            raise DependencyInstallationError(result.stderr.strip() or "Streamlit validation import failed")
        atomic_write_json(
            marker_path,
            {
                "app_id": app.id,
                "app_version": app.version,
                "python_version": subprocess.check_output([str(venv_python), "--version"], text=True).strip(),
                "requirements_sha256": self.requirements_hash(app.requirements),
                "installed_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        return EnvironmentState(app.id, app.version, env_path, venv_python, True, marker_path)
