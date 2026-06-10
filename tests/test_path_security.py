from __future__ import annotations

import json
from pathlib import Path

from launcher.app_discovery import discover_apps


def _mutate_manifest(app_dir: Path, **updates):
    manifest = app_dir / "app_manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data.update(updates)
    manifest.write_text(json.dumps(data), encoding="utf-8")


def test_rejects_parent_traversal(copied_apps):
    _mutate_manifest(copied_apps / "01_hello_pipeline", entrypoint="../app.py")
    apps = discover_apps(copied_apps)
    assert all(app.id != "hello-pipeline" for app in apps)


def test_rejects_absolute_entrypoint_outside_app_root(copied_apps, tmp_path):
    outside = tmp_path / "outside.py"
    outside.write_text("", encoding="utf-8")
    _mutate_manifest(copied_apps / "01_hello_pipeline", entrypoint=str(outside))
    apps = discover_apps(copied_apps)
    assert all(app.id != "hello-pipeline" for app in apps)


def test_rejects_command_injection_fields(copied_apps):
    _mutate_manifest(copied_apps / "01_hello_pipeline", command="calc.exe")
    apps = discover_apps(copied_apps)
    assert all(app.id != "hello-pipeline" for app in apps)


def test_rejects_invalid_app_ids(copied_apps):
    _mutate_manifest(copied_apps / "01_hello_pipeline", id="Hello Pipeline; calc")
    apps = discover_apps(copied_apps)
    assert all(app.name != "Hello Pipeline" for app in apps)
