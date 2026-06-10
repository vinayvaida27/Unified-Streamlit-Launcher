"""Local cache and platform state management."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .constants import STATE_SCHEMA_VERSION
from .path_utils import atomic_write_json, read_json


class LocalCacheManager:
    """Manages local cache folders and state files."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.environments_dir = base_dir / "environments"
        self.logs_dir = base_dir / "logs"
        self.state_dir = base_dir / "state"
        self.staging_dir = base_dir / "staging"

    def ensure_directories(self) -> None:
        """Create expected local cache directories."""

        for path in (self.base_dir, self.environments_dir, self.logs_dir, self.state_dir, self.staging_dir):
            path.mkdir(parents=True, exist_ok=True)

    @property
    def state_path(self) -> Path:
        return self.state_dir / "platform_state.json"

    def load_state(self) -> dict:
        """Load platform state or return an empty state."""

        if not self.state_path.exists():
            return {"schema_version": STATE_SCHEMA_VERSION, "active_platform_version": "1.0.0", "applications": {}}
        return read_json(self.state_path)

    def update_app_state(self, app_id: str, installed_version: str, last_exit_code: int | None = None) -> None:
        """Atomically update one application's state."""

        state = self.load_state()
        apps = state.setdefault("applications", {})
        entry = apps.setdefault(app_id, {})
        entry["installed_version"] = installed_version
        entry["last_started_at"] = datetime.now(timezone.utc).isoformat()
        if last_exit_code is not None:
            entry["last_exit_code"] = last_exit_code
        atomic_write_json(self.state_path, state)
