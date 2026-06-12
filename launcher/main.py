"""Launcher application entrypoint."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .app_discovery import discover_apps
from .config_loader import load_platform_config
from .environment_manager import EnvironmentManager, RuntimeResolver
from .local_cache import LocalCacheManager
from .logging_setup import configure_logging
from .process_manager import ProcessManager

LOG = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Run the desktop launcher."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/launcher_config.json")
    parser.add_argument("--development", action="store_true")
    args = parser.parse_args(argv)

    config = load_platform_config(Path(args.config))
    cache = LocalCacheManager(config.paths.local_cache_directory)
    cache.ensure_directories()
    configure_logging(config.paths.local_cache_directory, config.logging)
    apps = cache.sync_apps_to_local_cache(discover_apps(config.paths.apps_directory))
    runtime_python = RuntimeResolver(config, development_mode=args.development).resolve()
    env_manager = EnvironmentManager(config, runtime_python)
    process_manager = ProcessManager(cache.logs_dir)

    from PySide6.QtWidgets import QApplication

    from .ui.main_window import MainWindow

    qt_app = QApplication(sys.argv[:1])
    window = MainWindow(config, apps, env_manager, process_manager)
    window.show()
    result = qt_app.exec()
    if config.launcher.stop_apps_on_exit:
        process_manager.stop_all()
    LOG.info("Launcher exited with code %s", result)
    return int(result)
