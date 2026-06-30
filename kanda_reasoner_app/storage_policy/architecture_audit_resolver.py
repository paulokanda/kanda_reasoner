# project-path: kanda_reasoner_app/storage_policy/architecture_audit_resolver.py
"""External architecture audit path resolver for Kanda Reasoner.

This module resolves where generated architecture audit evidence should live
for the selected/analyzed project. It is side-effect free on import: importing
it must not create folders, move files, delete files, scan the source tree, or
change any existing evidence behavior.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from kanda_reasoner_app.storage_policy.path_resolver import (
    get_app_root,
    get_app_slug,
    get_app_drive_or_anchor,
    is_path_same_or_inside,
    make_safe_slug,
    normalize_path,
)

ARCHITECTURE_AUDIT_DOMAIN = "architecture_audit"
ARCHITECTURE_AUDIT_CURRENT_FOLDER = "current"
ARCHITECTURE_AUDIT_RUNS_FOLDER = "runs"
ARCHITECTURE_AUDIT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER = "json_complete"
ARCHITECTURE_AUDIT_SUBFOLDER_NAMES = (
    "json_complete",
    "bundle_manifest",
    "file_manifest",
    "reports",
)
ARCHITECTURE_AUDIT_ARTIFACT_SUFFIXES = (
    "active_snapshot",
    "bundle_manifest",
    "complete",
    "complete_runtime_trace",
    "exclusion_rules",
    "file_manifest",
    "reconstruction_payload",
    "validation_state",
)


def build_architecture_audit_root_from_drive_or_anchor(
    drive_or_anchor: str,
    project_slug: str,
) -> Path:
    """Build an external architecture audit root from drive/anchor and slug."""
    anchor = str(drive_or_anchor).strip()
    slug = make_safe_slug(project_slug)

    if not anchor:
        raise ValueError("drive_or_anchor must not be empty.")

    folder_name = f"{slug}_{ARCHITECTURE_AUDIT_DOMAIN}"

    if anchor.endswith(":"):
        return Path(f"{anchor}\\{folder_name}")

    return Path(anchor) / folder_name


def get_project_slug(project_root: str | Path | None = None) -> str:
    """Return a safe slug for the selected/analyzed project root."""
    if project_root is None:
        return get_app_slug()

    root = normalize_path(project_root)
    return make_safe_slug(root.name)


def get_architecture_audit_root(project_root: str | Path | None = None) -> Path:
    """Return the external architecture audit root for a selected project."""
    if project_root is None:
        root = get_app_root()
        drive_or_anchor = get_app_drive_or_anchor(root)
        slug = get_app_slug(root)
    else:
        root = normalize_path(project_root)
        drive_or_anchor = get_app_drive_or_anchor(root)
        slug = make_safe_slug(root.name)

    return build_architecture_audit_root_from_drive_or_anchor(drive_or_anchor, slug)


def get_architecture_audit_current_root(
    project_root: str | Path | None = None,
) -> Path:
    """Return the current audit output root without creating it."""
    return get_architecture_audit_root(project_root) / ARCHITECTURE_AUDIT_CURRENT_FOLDER


def build_architecture_audit_run_id(
    timestamp: datetime | None = None,
) -> str:
    """Return a Windows filename-safe run id."""
    value = datetime.now() if timestamp is None else timestamp
    return value.strftime(ARCHITECTURE_AUDIT_TIMESTAMP_FORMAT)


def get_architecture_audit_run_root(
    project_root: str | Path | None = None,
    run_id: str | None = None,
) -> Path:
    """Return a timestamped audit run root without creating it."""
    safe_run_id = make_safe_slug(run_id) if run_id else build_architecture_audit_run_id()
    return (
        get_architecture_audit_root(project_root)
        / ARCHITECTURE_AUDIT_RUNS_FOLDER
        / safe_run_id
    )


def _validate_audit_subfolder_name(subfolder_name: str) -> str:
    """Return a valid audit subfolder name or raise ValueError."""
    name = str(subfolder_name).strip()
    if name not in ARCHITECTURE_AUDIT_SUBFOLDER_NAMES:
        raise ValueError(
            f"Unknown architecture audit subfolder {name!r}. "
            f"Allowed values: {ARCHITECTURE_AUDIT_SUBFOLDER_NAMES!r}."
        )
    return name


def _validate_artifact_suffix(suffix: str) -> str:
    """Return a valid artifact suffix or raise ValueError."""
    value = str(suffix).strip()
    if value not in ARCHITECTURE_AUDIT_ARTIFACT_SUFFIXES:
        raise ValueError(
            f"Unknown architecture audit artifact suffix {value!r}. "
            f"Allowed values: {ARCHITECTURE_AUDIT_ARTIFACT_SUFFIXES!r}."
        )
    return value


def get_architecture_audit_subfolder(
    project_root: str | Path | None = None,
    subfolder_name: str = ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER,
    use_run: bool = False,
    run_id: str | None = None,
) -> Path:
    """Return a canonical audit subfolder without creating it."""
    name = _validate_audit_subfolder_name(subfolder_name)
    parent = (
        get_architecture_audit_run_root(project_root, run_id=run_id)
        if use_run
        else get_architecture_audit_current_root(project_root)
    )
    return parent / name


def get_architecture_audit_artifact_path(
    project_root: str | Path | None = None,
    suffix: str = "complete",
    use_run: bool = False,
    run_id: str | None = None,
    subfolder_name: str = ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER,
) -> Path:
    """Return a generated audit artifact path without creating it."""
    artifact_suffix = _validate_artifact_suffix(suffix)
    project_slug = get_project_slug(project_root)
    folder = get_architecture_audit_subfolder(
        project_root,
        subfolder_name=subfolder_name,
        use_run=use_run,
        run_id=run_id,
    )
    return folder / f"{project_slug}__{artifact_suffix}.json"


def get_architecture_audit_current_subfolders(
    project_root: str | Path | None = None,
) -> dict[str, Path]:
    """Return every canonical current audit subfolder without creating it."""
    return {
        name: get_architecture_audit_subfolder(project_root, name)
        for name in ARCHITECTURE_AUDIT_SUBFOLDER_NAMES
    }


def assert_architecture_audit_root_outside_project(
    architecture_audit_root: str | Path,
    project_root: str | Path,
) -> Path:
    """Return audit root, raising ValueError if it is inside project root."""
    audit_root = normalize_path(architecture_audit_root)
    root = normalize_path(project_root)

    if is_path_same_or_inside(audit_root, root):
        raise ValueError(
            "Architecture audit root must be outside the selected project "
            "source tree. "
            f"architecture_audit_root={str(audit_root)!r}, "
            f"project_root={str(root)!r}."
        )

    return audit_root


def ensure_architecture_audit_current_structure(
    project_root: str | Path | None = None,
) -> dict[str, Path]:
    """Create and return the current audit folder structure explicitly."""
    folders = get_architecture_audit_current_subfolders(project_root)
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    return folders


__all__ = [
    "ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER",
    "ARCHITECTURE_AUDIT_ARTIFACT_SUFFIXES",
    "ARCHITECTURE_AUDIT_CURRENT_FOLDER",
    "ARCHITECTURE_AUDIT_DOMAIN",
    "ARCHITECTURE_AUDIT_RUNS_FOLDER",
    "ARCHITECTURE_AUDIT_SUBFOLDER_NAMES",
    "ARCHITECTURE_AUDIT_TIMESTAMP_FORMAT",
    "assert_architecture_audit_root_outside_project",
    "build_architecture_audit_root_from_drive_or_anchor",
    "build_architecture_audit_run_id",
    "ensure_architecture_audit_current_structure",
    "get_architecture_audit_artifact_path",
    "get_architecture_audit_current_root",
    "get_architecture_audit_current_subfolders",
    "get_architecture_audit_root",
    "get_architecture_audit_run_root",
    "get_architecture_audit_subfolder",
    "get_project_slug",
]
