"""Frozen-application entry point.

PyInstaller runs the entry script as the top-level ``__main__`` module, which
has no package context -- so the package's own ``__main__.py`` (which uses a
relative ``from .main import main``) cannot be used directly. This thin wrapper
imports the launcher package absolutely and starts it.
"""

import sys

from launcher.main import main

if __name__ == "__main__":
    sys.exit(main())
