"""Maintenance subfolder policy for the Kanda Reasoner storage policy box.

This module declares the canonical subfolders under the application-owned
maintenance root. It is side-effect free on import: it must not create folders,
move files, delete files, or scan the source tree unless an explicit ensure
function is called by the caller.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from kanda_reasoner_app.storage_policy.maintenance_root_resolver import (
    get_maintenance_root,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path

MAINTENANCE_SUBFOLDER_PARTS: dict[str, tuple[str, ...]] = {
    "patch_backups": ("backups", "patches"),
    "restore_points": ("backups", "restore"),
    "pre_commit_backups": ("backups", "pre_commit"),
    "failed_patch_payloads": ("backups", "failed_patches"),
    "scratch_extracts": ("scratch", "extracts"),
    "scratch_cache": ("scratch", "cache"),
    "scratch_temp_work": ("scratch", "temp_work"),
    "scratch_downloads": ("scratch", "downloads"),
    "quarantine_manual": ("quarantine", "manual"),
    "quarantine_autodelete": ("quarantine", "autodelete"),
    "install_logs": ("logs", "install"),
    "runtime_logs": ("logs", "runtime"),
    "audit_logs": ("logs", "audit"),
    "migration_logs": ("logs", "migration"),
    "build_outputs": ("build",),
    "release_outputs": ("releases",),
    "legacy_absorbed": ("migration", "legacy_absorbed"),
    "migrated_evidence": ("migration", "migrated_evidence"),
    "crash_dumps": ("diagnostics", "crash_dumps"),
    "diagnostic_screenshots": ("diagnostics", "screenshots"),
    "staging": ("staging",),
}

MAINTENANCE_SUBFOLDER_NAMES = tuple(MAINTENANCE_SUBFOLDER_PARTS.keys())


def get_maintenance_subfolder(
    name: str,
    maintenance_root: str | Path | None = None,
) -> Path:
    """Return a canonical maintenance subfolder path without creating it."""
    if name not in MAINTENANCE_SUBFOLDER_PARTS:
        allowed = ", ".join(MAINTENANCE_SUBFOLDER_NAMES)
        raise ValueError(
            f"Unknown maintenance subfolder {name!r}. "
            f"Allowed values: {allowed}."
        )

    root = (
        normalize_path(maintenance_root)
        if maintenance_root is not None
        else get_maintenance_root()
    )

    folder = root
    for part in MAINTENANCE_SUBFOLDER_PARTS[name]:
        folder = folder / part

    return folder


def get_all_maintenance_subfolders(
    maintenance_root: str | Path | None = None,
) -> dict[str, Path]:
    """Return all canonical maintenance subfolders without creating them."""
    return {
        name: get_maintenance_subfolder(name, maintenance_root)
        for name in MAINTENANCE_SUBFOLDER_NAMES
    }


def ensure_maintenance_subfolder(
    name: str,
    maintenance_root: str | Path | None = None,
) -> Path:
    """Create and return one canonical maintenance subfolder."""
    folder = get_maintenance_subfolder(name, maintenance_root)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def ensure_maintenance_structure(
    maintenance_root: str | Path | None = None,
) -> dict[str, Path]:
    """Create and return all canonical maintenance subfolders."""
    folders = get_all_maintenance_subfolders(maintenance_root)

    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)

    return folders


def relative_maintenance_subfolder_parts(name: str) -> tuple[str, ...]:
    """Return the relative path parts for a canonical maintenance subfolder."""
    if name not in MAINTENANCE_SUBFOLDER_PARTS:
        allowed = ", ".join(MAINTENANCE_SUBFOLDER_NAMES)
        raise ValueError(
            f"Unknown maintenance subfolder {name!r}. "
            f"Allowed values: {allowed}."
        )

    return MAINTENANCE_SUBFOLDER_PARTS[name]


def describe_maintenance_subfolder_policy() -> Mapping[str, tuple[str, ...]]:
    """Return a copy of the canonical subfolder policy."""
    return dict(MAINTENANCE_SUBFOLDER_PARTS)


__all__ = [
    "MAINTENANCE_SUBFOLDER_NAMES",
    "MAINTENANCE_SUBFOLDER_PARTS",
    "describe_maintenance_subfolder_policy",
    "ensure_maintenance_structure",
    "ensure_maintenance_subfolder",
    "get_all_maintenance_subfolders",
    "get_maintenance_subfolder",
    "relative_maintenance_subfolder_parts",
]
