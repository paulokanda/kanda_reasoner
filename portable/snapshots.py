"""Metadata snapshots proving source and Project Support immutability."""

from __future__ import annotations

import hashlib
from pathlib import Path

from portable.constants import PROJECT_SNAPSHOT_IGNORES
from portable.errors import PortableBuildError


def metadata_snapshot(
    root: Path,
    *,
    ignored_names: set[str] | None = None,
) -> dict[str, object]:
    """Create a deterministic metadata-only tree fingerprint."""

    if not root.exists():
        return {
            "exists": False,
            "digest": "",
            "files": 0,
            "directories": 0,
        }

    ignored = {
        item.casefold()
        for item in (ignored_names or set())
    }
    digest = hashlib.sha256()
    files = 0
    directories = 0

    entries = sorted(
        root.rglob("*"),
        key=lambda item: item.relative_to(root).as_posix().casefold(),
    )
    for entry in entries:
        relative = entry.relative_to(root)
        if any(part.casefold() in ignored for part in relative.parts):
            continue

        stat = entry.lstat()
        if entry.is_symlink():
            kind = "L"
            size = 0
        elif entry.is_dir():
            kind = "D"
            size = 0
            directories += 1
        else:
            kind = "F"
            size = stat.st_size
            files += 1

        record = (
            f"{kind}\0{relative.as_posix()}\0"
            f"{size}\0{stat.st_mtime_ns}\n"
        )
        digest.update(record.encode("utf-8"))

    return {
        "exists": True,
        "digest": digest.hexdigest(),
        "files": files,
        "directories": directories,
    }


def project_snapshot(root: Path) -> dict[str, object]:
    """Snapshot source while ignoring developer-owned caches."""

    return metadata_snapshot(
        root,
        ignored_names=PROJECT_SNAPSHOT_IGNORES,
    )


def assert_unchanged(
    label: str,
    before: dict[str, object],
    after: dict[str, object],
) -> None:
    """Block publication when a protected tree changed."""

    if before != after:
        raise PortableBuildError(
            f"{label} changed; Portable publication was blocked."
        )
    print(f"{label}: PASS")
