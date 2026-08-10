# project-path: tools/fire_shield_validation_fixtures.py
"""Cross-platform archive fixtures for Fire Shield validation."""

from __future__ import annotations

import zipfile
from pathlib import Path


__all__ = ("fire_shield_raw_backslash_zip", "fire_shield_zip")


def fire_shield_zip(path: Path, entries: list[tuple[str, bytes]]) -> None:
    """Create one ordinary synthetic ZIP fixture."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, raw in entries:
            archive.writestr(name, raw)


def fire_shield_raw_backslash_zip(
    path: Path,
    forward_name: str,
    backslash_name: str,
    raw: bytes,
) -> int:
    """Create a ZIP whose local and central headers contain backslashes."""
    if len(forward_name.encode("utf-8")) != len(backslash_name.encode("utf-8")):
        raise RuntimeError("FIRE_SHIELD_RAW_ZIP_NAME_LENGTH_MISMATCH")
    fire_shield_zip(path, [(forward_name, raw)])
    payload = path.read_bytes()
    forward = forward_name.encode("utf-8")
    backslash = backslash_name.encode("utf-8")
    count = payload.count(forward)
    if count != 2:
        raise RuntimeError(
            "FIRE_SHIELD_RAW_ZIP_HEADER_COUNT_INVALID:" + str(count)
        )
    path.write_bytes(payload.replace(forward, backslash))
    return count
