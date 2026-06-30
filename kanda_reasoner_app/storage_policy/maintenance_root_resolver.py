# project-path: kanda_reasoner_app/storage_policy/maintenance_root_resolver.py
"""Maintenance root resolution for the Kanda Reasoner storage policy box.

This module resolves the application-owned maintenance root used for backups,
restore points, quarantine, scratch data, logs, and build outputs. It is
side-effect free: importing this module must not create folders, move files,
delete files, or scan the source tree.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path

from kanda_reasoner_app.storage_policy.path_resolver import (
    get_app_drive_or_anchor,
    get_app_root,
    is_path_same_or_inside,
    normalize_path,
)

MAINTENANCE_ROOT_FOLDER_NAME = "_kanda_reasoner_temp"
MAINTENANCE_ROOT_ENV_VARS = (
    "kanda_reasoner_maintenance_root",
    "KANDA_REASONER_MAINTENANCE_ROOT",
)


def _first_configured_root(
    environment: Mapping[str, str] | None = None,
) -> Path | None:
    """Return the first configured maintenance root from environment values."""
    source = os.environ if environment is None else environment

    for name in MAINTENANCE_ROOT_ENV_VARS:
        value = str(source.get(name, "")).strip()
        if value:
            return normalize_path(value)

    return None


def build_maintenance_root_from_drive_or_anchor(
    drive_or_anchor: str,
    folder_name: str = MAINTENANCE_ROOT_FOLDER_NAME,
) -> Path:
    """Build a maintenance root from a Windows drive or POSIX anchor."""
    anchor = str(drive_or_anchor).strip()

    if not anchor:
        raise ValueError("drive_or_anchor must not be empty.")

    if anchor.endswith(":"):
        return Path(f"{anchor}\\{folder_name}")

    return Path(anchor) / folder_name


def get_default_maintenance_root(app_root: str | Path | None = None) -> Path:
    """Return the default app-owned maintenance root without creating it."""
    root = normalize_path(app_root) if app_root is not None else get_app_root()
    drive_or_anchor = get_app_drive_or_anchor(root)
    return build_maintenance_root_from_drive_or_anchor(drive_or_anchor)


def get_maintenance_root(
    app_root: str | Path | None = None,
    environment: Mapping[str, str] | None = None,
) -> Path:
    """Return the configured maintenance root or the default root.

    The default follows the Kanda Reasoner application drive or filesystem
    anchor. It does not follow the selected project being analyzed.
    """
    configured_root = _first_configured_root(environment)
    if configured_root is not None:
        return configured_root

    return get_default_maintenance_root(app_root)


def is_maintenance_root_inside_app(
    maintenance_root: str | Path,
    app_root: str | Path | None = None,
) -> bool:
    """Return True when the maintenance root is inside the app source tree."""
    root = normalize_path(app_root) if app_root is not None else get_app_root()
    return is_path_same_or_inside(maintenance_root, root)


def assert_maintenance_root_outside_app(
    maintenance_root: str | Path,
    app_root: str | Path | None = None,
) -> Path:
    """Return maintenance_root, raising ValueError if it is inside app root."""
    root = normalize_path(app_root) if app_root is not None else get_app_root()
    resolved_root = normalize_path(maintenance_root)

    if is_maintenance_root_inside_app(resolved_root, root):
        raise ValueError(
            "Maintenance root must be outside the Kanda Reasoner source tree. "
            f"maintenance_root={str(resolved_root)!r}, app_root={str(root)!r}."
        )

    return resolved_root


__all__ = [
    "MAINTENANCE_ROOT_ENV_VARS",
    "MAINTENANCE_ROOT_FOLDER_NAME",
    "assert_maintenance_root_outside_app",
    "build_maintenance_root_from_drive_or_anchor",
    "get_default_maintenance_root",
    "get_maintenance_root",
    "is_maintenance_root_inside_app",
]
