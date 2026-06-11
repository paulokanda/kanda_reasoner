"""Backup path resolver helpers for the Kanda Reasoner storage policy box.

This module returns canonical patch backup paths for future patch installers
and searches existing backup locations for restore workflows. It is side-effect
free on import: importing it must not create folders, move files, delete files,
or scan the live source tree.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from kanda_reasoner_app.storage_policy.historical_debris_report import (
    build_legacy_debris_path,
)
from kanda_reasoner_app.storage_policy.maintenance_subfolder_policy import (
    get_maintenance_subfolder,
)
from kanda_reasoner_app.storage_policy.path_resolver import (
    get_app_drive_or_anchor,
    make_safe_slug,
)

PATCH_BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
BACKUP_RESTORE_SEARCH_SUBFOLDERS = (
    "patch_backups",
    "restore_points",
)
_LEGACY_BACKUP_FOLDER_NAMES = (
    "_kanda_patch_backups",
    "_kanda_restore_points",
)


@dataclass(frozen=True)
class PatchBackupCandidate:
    """Candidate backup folder found during restore lookup."""

    path: str
    source_name: str
    exists: bool
    modified_timestamp: float | None


def _current_timestamp() -> str:
    """Return a timestamp for patch backup folder names."""
    return datetime.now().strftime(PATCH_BACKUP_TIMESTAMP_FORMAT)


def build_patch_backup_folder_name(
    patch_name: str,
    timestamp: str | None = None,
) -> str:
    """Return a safe patch backup folder name.

    The result is deterministic when timestamp is provided. When timestamp is
    omitted, the current local timestamp is used.
    """
    safe_patch_name = make_safe_slug(patch_name, fallback="")
    if not safe_patch_name:
        raise ValueError("patch_name must produce a non-empty safe slug.")

    backup_timestamp = timestamp if timestamp is not None else _current_timestamp()
    cleaned_timestamp = str(backup_timestamp).strip()
    if not cleaned_timestamp:
        raise ValueError("timestamp must not be empty.")

    return f"{safe_patch_name}_{cleaned_timestamp}"


def get_patch_backup_path(
    patch_name: str,
    timestamp: str | None = None,
    maintenance_root: str | Path | None = None,
) -> Path:
    """Return the canonical patch backup path without creating it."""
    folder_name = build_patch_backup_folder_name(
        patch_name,
        timestamp=timestamp,
    )
    return get_maintenance_subfolder(
        "patch_backups",
        maintenance_root=maintenance_root,
    ) / folder_name


def ensure_patch_backup_path(
    patch_name: str,
    timestamp: str | None = None,
    maintenance_root: str | Path | None = None,
) -> Path:
    """Create and return the canonical patch backup path.

    This is the only function in this module that creates a folder, and it does
    so only when called explicitly by an installer or test.
    """
    backup_path = get_patch_backup_path(
        patch_name,
        timestamp=timestamp,
        maintenance_root=maintenance_root,
    )
    backup_path.mkdir(parents=True, exist_ok=True)
    return backup_path


def get_backup_restore_search_roots(
    maintenance_root: str | Path | None = None,
    drive_or_anchor: str | None = None,
) -> tuple[Path, ...]:
    """Return restore search roots in canonical order.

    New storage-policy paths are searched first. Historical top-level backup
    folders are searched as fallback locations for older patch installers.
    """
    anchor = drive_or_anchor if drive_or_anchor is not None else get_app_drive_or_anchor()

    roots = [
        get_maintenance_subfolder(
            subfolder_name,
            maintenance_root=maintenance_root,
        )
        for subfolder_name in BACKUP_RESTORE_SEARCH_SUBFOLDERS
    ]
    roots.extend(
        build_legacy_debris_path(legacy_name, drive_or_anchor=anchor)
        for legacy_name in _LEGACY_BACKUP_FOLDER_NAMES
    )
    return tuple(roots)


def _candidate_from_path(path: Path, source_name: str) -> PatchBackupCandidate:
    """Build a candidate data object for an existing backup path."""
    try:
        modified_timestamp = float(path.stat().st_mtime)
    except OSError:
        modified_timestamp = None

    return PatchBackupCandidate(
        path=str(path),
        source_name=source_name,
        exists=path.exists(),
        modified_timestamp=modified_timestamp,
    )


def _matching_candidates(
    patch_name: str,
    maintenance_root: str | Path | None = None,
    drive_or_anchor: str | None = None,
) -> tuple[PatchBackupCandidate, ...]:
    """Return existing backup candidates for patch_name."""
    safe_patch_name = make_safe_slug(patch_name, fallback="")
    if not safe_patch_name:
        raise ValueError("patch_name must produce a non-empty safe slug.")

    candidates: list[PatchBackupCandidate] = []
    search_roots = get_backup_restore_search_roots(
        maintenance_root=maintenance_root,
        drive_or_anchor=drive_or_anchor,
    )

    for root in search_roots:
        if not root.exists() or not root.is_dir():
            continue

        for match in root.glob(f"{safe_patch_name}_*"):
            if not match.is_dir():
                continue
            candidates.append(
                _candidate_from_path(match, source_name=root.name),
            )

    return tuple(candidates)


def find_latest_patch_backup(
    patch_name: str,
    maintenance_root: str | Path | None = None,
    drive_or_anchor: str | None = None,
) -> PatchBackupCandidate | None:
    """Return the newest matching backup candidate, or None if absent."""
    candidates = _matching_candidates(
        patch_name,
        maintenance_root=maintenance_root,
        drive_or_anchor=drive_or_anchor,
    )
    if not candidates:
        return None

    return sorted(
        candidates,
        key=lambda candidate: (
            candidate.modified_timestamp is not None,
            candidate.modified_timestamp or 0.0,
            candidate.path,
        ),
        reverse=True,
    )[0]


__all__ = [
    "BACKUP_RESTORE_SEARCH_SUBFOLDERS",
    "PATCH_BACKUP_TIMESTAMP_FORMAT",
    "PatchBackupCandidate",
    "build_patch_backup_folder_name",
    "ensure_patch_backup_path",
    "find_latest_patch_backup",
    "get_backup_restore_search_roots",
    "get_patch_backup_path",
]
