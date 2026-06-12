from __future__ import annotations

from launcher.app_discovery import discover_apps
from launcher.local_cache import LocalCacheManager


def test_syncs_app_source_to_local_cache(tmp_path, repo_root):
    app = discover_apps(repo_root / "apps")[0]
    cache = LocalCacheManager(tmp_path / "cache")
    cache.ensure_directories()

    cached_app = cache.sync_app_to_local_cache(app)

    assert cached_app.app_dir != app.app_dir
    assert cached_app.app_dir == (tmp_path / "cache" / "apps" / app.id / app.version).resolve()
    assert cached_app.entrypoint.exists()
    assert cached_app.entrypoint.parent == cached_app.app_dir
    assert cached_app.icon.exists()
    assert cached_app.requirements.exists()


def test_sync_refreshes_when_source_changes(tmp_path, copied_apps):
    app = discover_apps(copied_apps)[0]
    cache = LocalCacheManager(tmp_path / "cache")
    cache.ensure_directories()

    first_cached = cache.sync_app_to_local_cache(app)
    original_text = first_cached.entrypoint.read_text(encoding="utf-8")
    app.entrypoint.write_text(original_text + "\n# changed\n", encoding="utf-8")

    refreshed = cache.sync_app_to_local_cache(app)

    assert "# changed" in refreshed.entrypoint.read_text(encoding="utf-8")
