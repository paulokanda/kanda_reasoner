"""Content-hash snapshots proving project and Project Support immutability."""

from __future__ import annotations

import hashlib
from pathlib import Path

from portable.constants import PROJECT_SNAPSHOT_IGNORES
from portable.errors import PortableBuildError


_BLOCK_SIZE = 1024 * 1024


def _update_file_content(
    digest: "hashlib._Hash",
    path: Path,
) -> None:
    """Add a file's exact bytes to a tree digest."""

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(_BLOCK_SIZE),
            b"",
        ):
            digest.update(block)


def content_snapshot(
    root: Path,
    *,
    ignored_names: set[str] | None = None,
) -> dict[str, object]:
    """Create a deterministic path-and-content tree fingerprint."""

    if not root.exists():
        return {
            "exists": False,
            "digest": "",
            "files": 0,
            "directories": 0,
            "symlinks": 0,
        }

    ignored = {
        item.casefold()
        for item in (ignored_names or set())
    }
    digest = hashlib.sha256()
    files = 0
    directories = 0
    symlinks = 0

    entries = sorted(
        root.rglob("*"),
        key=lambda item: item.relative_to(root).as_posix().casefold(),
    )
    for entry in entries:
        relative = entry.relative_to(root)
        if any(
            part.casefold() in ignored
            for part in relative.parts
        ):
            continue

        relative_text = relative.as_posix()
        if entry.is_symlink():
            symlinks += 1
            digest.update(
                f"L\0{relative_text}\0".encode("utf-8")
            )
            digest.update(
                str(entry.readlink()).encode("utf-8")
            )
            digest.update(b"\n")
            continue

        if entry.is_dir():
            directories += 1
            digest.update(
                f"D\0{relative_text}\n".encode("utf-8")
            )
            continue

        files += 1
        digest.update(
            f"F\0{relative_text}\0".encode("utf-8")
        )
        _update_file_content(digest, entry)
        digest.update(b"\n")

    return {
        "exists": True,
        "digest": digest.hexdigest(),
        "files": files,
        "directories": directories,
        "symlinks": symlinks,
    }


def metadata_snapshot(
    root: Path,
    *,
    ignored_names: set[str] | None = None,
) -> dict[str, object]:
    """Compatibility alias now backed by exact content hashes."""

    return content_snapshot(
        root,
        ignored_names=ignored_names,
    )


def project_snapshot(root: Path) -> dict[str, object]:
    """Hash project contents while ignoring developer-owned caches."""

    return content_snapshot(
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
