"""Verify that a built wheel contains only the supported package architecture."""

from pathlib import Path
from sys import argv
from zipfile import ZipFile


def check_wheel(path: Path) -> None:
    """Validate required typing metadata and reject deleted legacy modules.

    Args:
        path: Wheel archive produced by ``uv build``.

    Raises:
        RuntimeError: If required metadata is absent or legacy code is present.
    """
    with ZipFile(path) as archive:
        names = set(archive.namelist())

    if "syntiq_mt5/py.typed" not in names:
        raise RuntimeError("wheel does not contain syntiq_mt5/py.typed")

    forbidden = {
        name
        for name in names
        if name.startswith("syntiq_mt5/_core/")
        or name.endswith("/service.py")
        or name == "syntiq_mt5/client.py"
    }
    if forbidden:
        rendered = ", ".join(sorted(forbidden))
        raise RuntimeError(f"wheel contains removed legacy modules: {rendered}")


if __name__ == "__main__":
    check_wheel(Path(argv[1]))
