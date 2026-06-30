# project-path: kanda_reasoner_app/storage_policy/path_resolver.py
"""Path resolution helpers for the Kanda Reasoner storage policy box.

This module owns side-effect-free path helpers used by later storage policy
modules. Importing it must not create folders, move files, delete files, scan
the live source tree, or read user-specific configuration.
"""

from __future__ import annotations

import re
from pathlib import Path

APP_PACKAGE_NAME = "kanda_reasoner_app"
DEFAULT_SLUG_FALLBACK = "project"
_SAFE_SLUG_PATTERN = re.compile(r"[^a-z0-9_]+")
_REPEATED_UNDERSCORE_PATTERN = re.compile(r"_+")


def normalize_path(path: str | Path) -> Path:
    """Return an absolute, normalized Path without creating it."""
    return Path(path).expanduser().resolve()


def find_parent_named(start_path: str | Path, folder_name: str) -> Path:
    """Return the nearest parent path with the requested folder name.

    The search includes start_path itself. A ValueError is raised when the
    requested folder is not found in the path ancestry.
    """
    current = normalize_path(start_path)

    for candidate in (current, *current.parents):
        if candidate.name == folder_name:
            return candidate

    raise ValueError(
        "Could not find parent folder named "
        f"{folder_name!r} from path {str(current)!r}."
    )


def get_storage_policy_package_root() -> Path:
    """Return the storage_policy package folder."""
    return Path(__file__).resolve().parent


def get_app_package_root() -> Path:
    """Return the canonical Kanda Reasoner application package folder."""
    return find_parent_named(__file__, APP_PACKAGE_NAME)


def get_app_root() -> Path:
    """Return the Kanda Reasoner application source root folder."""
    return get_app_package_root().parent


def make_safe_slug(name: str, fallback: str = DEFAULT_SLUG_FALLBACK) -> str:
    """Return a lowercase ASCII-safe slug for file and folder names."""
    stripped = str(name).strip().lower()
    slug = _SAFE_SLUG_PATTERN.sub("_", stripped)
    slug = _REPEATED_UNDERSCORE_PATTERN.sub("_", slug).strip("_")

    if slug:
        return slug

    return fallback


def get_app_slug(app_root: str | Path | None = None) -> str:
    """Return a safe slug derived from the app root folder name."""
    root = normalize_path(app_root) if app_root is not None else get_app_root()
    return make_safe_slug(root.name)


def get_app_drive_or_anchor(app_root: str | Path | None = None) -> str:
    """Return the filesystem drive on Windows or anchor on POSIX systems.

    On Windows this returns values such as "C:" or "E:". On POSIX systems,
    where Path.drive is empty, it returns the path anchor such as "/".
    """
    root = normalize_path(app_root) if app_root is not None else get_app_root()

    if root.drive:
        return root.drive

    return root.anchor


def is_path_inside(path: str | Path, parent: str | Path) -> bool:
    """Return True when path is strictly inside parent."""
    child_path = normalize_path(path)
    parent_path = normalize_path(parent)

    if child_path == parent_path:
        return False

    try:
        child_path.relative_to(parent_path)
    except ValueError:
        return False

    return True


def is_path_same_or_inside(path: str | Path, parent: str | Path) -> bool:
    """Return True when path equals parent or is inside parent."""
    child_path = normalize_path(path)
    parent_path = normalize_path(parent)

    if child_path == parent_path:
        return True

    try:
        child_path.relative_to(parent_path)
    except ValueError:
        return False

    return True


__all__ = [
    "APP_PACKAGE_NAME",
    "DEFAULT_SLUG_FALLBACK",
    "find_parent_named",
    "get_app_drive_or_anchor",
    "get_app_package_root",
    "get_app_root",
    "get_app_slug",
    "get_storage_policy_package_root",
    "is_path_inside",
    "is_path_same_or_inside",
    "make_safe_slug",
    "normalize_path",
]
