from __future__ import annotations

from launcher.app_discovery import discover_apps
from launcher.environment_manager import EnvironmentManager, RuntimeResolver


def test_calculates_deterministic_environment_path(temp_config, repo_root):
    app = discover_apps(repo_root / "apps")[0]
    manager = EnvironmentManager(temp_config, repo_root / "fake-python.exe")
    assert manager.environment_path_for(app) == temp_config.paths.local_cache_directory / "environments" / app.id / app.version


def test_detects_ready_marker(temp_config, repo_root):
    app = discover_apps(repo_root / "apps")[0]
    manager = EnvironmentManager(temp_config, repo_root / "fake-python.exe")
    env_path = manager.environment_path_for(app)
    python_path = manager.venv_python_for(env_path)
    python_path.parent.mkdir(parents=True, exist_ok=True)
    python_path.write_text("", encoding="utf-8")
    marker = manager.marker_path_for(env_path)
    marker.write_text(
        '{"app_id":"hello-pipeline","app_version":"1.0.0","requirements_sha256":"' + manager.requirements_hash(app.requirements) + '"}',
        encoding="utf-8",
    )
    assert manager.is_ready(app)


def test_detects_changed_requirements_hash(temp_config, repo_root, tmp_path):
    app = discover_apps(repo_root / "apps")[0]
    manager = EnvironmentManager(temp_config, repo_root / "fake-python.exe")
    env_path = manager.environment_path_for(app)
    python_path = manager.venv_python_for(env_path)
    python_path.parent.mkdir(parents=True, exist_ok=True)
    python_path.write_text("", encoding="utf-8")
    manager.marker_path_for(env_path).write_text(
        '{"app_id":"hello-pipeline","app_version":"1.0.0","requirements_sha256":"wrong"}',
        encoding="utf-8",
    )
    assert not manager.is_ready(app)


def test_builds_correct_pip_command(temp_config, repo_root):
    app = discover_apps(repo_root / "apps")[0]
    manager = EnvironmentManager(temp_config, repo_root / "fake-python.exe")
    command = manager.pip_install_command(app, repo_root / ".venv" / "Scripts" / "python.exe")
    assert command[:4][-3:] == ["-m", "pip", "install"]
    assert "-r" in command


def test_chooses_offline_wheelhouse_when_available(temp_config, copied_apps):
    wheelhouse = copied_apps / "01_hello_pipeline" / "wheelhouse"
    wheelhouse.mkdir()
    (wheelhouse / "placeholder.whl").write_text("", encoding="utf-8")
    app = discover_apps(copied_apps)[0]
    manager = EnvironmentManager(temp_config, copied_apps / "fake-python.exe")
    command = manager.pip_install_command(app, copied_apps / "venv-python.exe")
    assert "--no-index" in command
    assert "--find-links" in command


def test_runtime_resolver_can_skip_validation_before_local_sync(temp_config, tmp_path, monkeypatch):
    runtime_python = tmp_path / "network_runtime" / "python.exe"
    runtime_python.parent.mkdir()
    runtime_python.write_text("placeholder", encoding="utf-8")
    object.__setattr__(temp_config.paths, "runtime_python", runtime_python)

    def fail_validate(_python_path):
        raise AssertionError("network runtime should not be executed before local sync")

    resolver = RuntimeResolver(temp_config, development_mode=False)
    monkeypatch.setattr(resolver, "validate", fail_validate)

    assert resolver.resolve(validate=False) == runtime_python
