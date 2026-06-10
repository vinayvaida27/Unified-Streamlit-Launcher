from __future__ import annotations

import json
import shutil

from launcher.app_discovery import discover_apps


def test_discovers_all_10_apps(repo_root):
    apps = discover_apps(repo_root / "apps")
    assert len(apps) == 10


def test_sorts_by_display_order(repo_root):
    apps = discover_apps(repo_root / "apps")
    assert [app.display_order for app in apps] == list(range(1, 11))


def test_rejects_duplicate_ids(copied_apps):
    first = copied_apps / "01_hello_pipeline" / "app_manifest.json"
    second = copied_apps / "02_second_app" / "app_manifest.json"
    data = json.loads(second.read_text(encoding="utf-8"))
    data["id"] = "hello-pipeline"
    second.write_text(json.dumps(data), encoding="utf-8")
    apps = discover_apps(copied_apps)
    assert len(apps) == 9


def test_handles_missing_icon(copied_apps):
    (copied_apps / "01_hello_pipeline" / "assets" / "icon.svg").unlink()
    apps = discover_apps(copied_apps)
    assert all(app.id != "hello-pipeline" for app in apps)


def test_rejects_path_traversal(copied_apps):
    manifest = copied_apps / "01_hello_pipeline" / "app_manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["entrypoint"] = "../../malicious.py"
    manifest.write_text(json.dumps(data), encoding="utf-8")
    apps = discover_apps(copied_apps)
    assert all(app.id != "hello-pipeline" for app in apps)


def test_skips_disabled_apps(copied_apps):
    manifest = copied_apps / "01_hello_pipeline" / "app_manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["enabled"] = False
    manifest.write_text(json.dumps(data), encoding="utf-8")
    apps = discover_apps(copied_apps)
    assert len(apps) == 9
