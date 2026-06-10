"""Application manifest discovery and validation."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from .constants import DEFAULT_ADDRESS, SUPPORTED_APP_TYPES, SUPPORTED_SCHEMA_VERSION
from .exceptions import ManifestValidationError, SecurityValidationError
from .models import ApplicationManifest, LaunchSettings
from .path_utils import ensure_within_directory, read_json, reject_path_traversal
from .security import reject_command_injection_fields, validate_app_id

LOG = logging.getLogger(__name__)
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")


def _required(data: dict, key: str):
    if key not in data:
        raise ManifestValidationError(f"Missing required manifest field: {key}")
    return data[key]


def load_app_manifest(app_dir: Path) -> ApplicationManifest:
    """Load and strictly validate an application manifest."""

    manifest_path = app_dir / "app_manifest.json"
    data = read_json(manifest_path)
    reject_command_injection_fields(data)

    if data.get("schema_version") != SUPPORTED_SCHEMA_VERSION:
        raise ManifestValidationError("Unsupported application manifest schema version")
    app_id = str(_required(data, "id"))
    validate_app_id(app_id)
    version = str(_required(data, "version"))
    if not SEMVER.match(version):
        raise ManifestValidationError(f"Invalid semantic version: {version}")
    app_type = str(_required(data, "type"))
    if app_type not in SUPPORTED_APP_TYPES:
        raise ManifestValidationError(f"Unsupported app type: {app_type}")

    entrypoint_raw = str(_required(data, "entrypoint"))
    icon_raw = str(_required(data, "icon"))
    requirements_raw = str(_required(data, "requirements"))
    wheelhouse_raw = str(data.get("wheelhouse", "wheelhouse"))
    for value in (entrypoint_raw, icon_raw, requirements_raw, wheelhouse_raw):
        reject_path_traversal(value)

    entrypoint = ensure_within_directory(app_dir / entrypoint_raw, app_dir)
    icon = ensure_within_directory(app_dir / icon_raw, app_dir)
    requirements = ensure_within_directory(app_dir / requirements_raw, app_dir)
    wheelhouse = ensure_within_directory(app_dir / wheelhouse_raw, app_dir)

    if not entrypoint.is_file():
        raise ManifestValidationError(f"Entrypoint does not exist: {entrypoint}")
    if not icon.is_file():
        raise ManifestValidationError(f"Icon does not exist: {icon}")
    if not requirements.is_file():
        raise ManifestValidationError(f"Requirements file does not exist: {requirements}")
    display_order = int(_required(data, "display_order"))
    if display_order < 1:
        raise ManifestValidationError("display_order must be positive")

    launch_data = _required(data, "launch")
    address = str(launch_data.get("address", DEFAULT_ADDRESS))
    if address != DEFAULT_ADDRESS:
        raise ManifestValidationError("Streamlit apps must bind to 127.0.0.1")

    return ApplicationManifest(
        schema_version=data["schema_version"],
        id=app_id,
        name=str(_required(data, "name")),
        version=version,
        description=str(_required(data, "description")),
        category=str(_required(data, "category")),
        type=app_type,
        entrypoint=entrypoint,
        icon=icon,
        requirements=requirements,
        wheelhouse=wheelhouse,
        python_version=str(_required(data, "python_version")),
        enabled=bool(_required(data, "enabled")),
        display_order=display_order,
        launch=LaunchSettings(
            address=address,
            port=str(launch_data.get("port", "dynamic")),
            headless=bool(launch_data.get("headless", True)),
            file_watcher_type=str(launch_data.get("file_watcher_type", "none")),
            gather_usage_stats=bool(launch_data.get("gather_usage_stats", False)),
            startup_timeout_seconds=int(launch_data.get("startup_timeout_seconds", 60)),
        ),
        app_dir=app_dir.resolve(),
    )


def discover_apps(apps_directory: Path, include_disabled: bool = False) -> list[ApplicationManifest]:
    """Discover valid application manifests."""

    if not apps_directory.exists():
        LOG.warning("Applications directory does not exist: %s", apps_directory)
        return []
    discovered: list[ApplicationManifest] = []
    seen_ids: set[str] = set()
    for manifest_path in sorted(apps_directory.glob("*/app_manifest.json")):
        try:
            app = load_app_manifest(manifest_path.parent.resolve())
            if app.id in seen_ids:
                raise ManifestValidationError(f"Duplicate application ID: {app.id}")
            seen_ids.add(app.id)
            if app.enabled or include_disabled:
                discovered.append(app)
        except (ManifestValidationError, SecurityValidationError, ValueError) as exc:
            LOG.exception("Skipping invalid application manifest at %s: %s", manifest_path, exc)
    return sorted(discovered, key=lambda app: (app.display_order, app.name.lower()))
