"""Generate the PyInstaller spec used by the release builder."""

from __future__ import annotations

from pathlib import Path


def generate_spec(project_root: Path | None = None) -> Path:
    """Write and return the launcher spec path."""

    root = (project_root or Path(__file__).resolve().parent.parent).resolve()
    spec_path = root / "build" / "launcher.spec"
    entrypoint = (root / "launcher" / "__main__.py").as_posix()
    pathex = root.as_posix()
    icon_path = (root / "assets" / "launcher" / "launcher.ico").as_posix()
    icon_line = f"    icon=r'{icon_path}'," if Path(icon_path).exists() else "    icon=None,"

    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(
        f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{entrypoint}'],
    pathex=[r'{pathex}'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
{icon_line}
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='launcher',
)
""",
        encoding="utf-8",
    )
    return spec_path


if __name__ == "__main__":
    print(generate_spec())
