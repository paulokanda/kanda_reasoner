"""Canonical maintenance subfolder policy for KANDA storage helpers.

This module is intentionally side-effect free on import.  It only returns paths
or creates folders when an explicit ``ensure_*`` function is called.
"""

from __future__ import annotations

__all__ = []


from pathlib import Path
from typing import Iterable

from kanda_reasoner_app.storage_policy.maintenance_root_resolver import get_maintenance_root

MAINTENANCE_SUBFOLDER_PARTS: dict[str, tuple[str, ...]] = {
    "patch_backups": ("patch_backups",),
    "restore_points": ("restore_points",),
    "audit_logs": ("audit_logs",),
    "quarantine_manual": ("quarantine_manual",),
    "packaging_exclusion": ("packaging_exclusion",),
    "evidence_relocation": ("evidence_relocation",),
    "compilation_readiness": ("compilation_readiness",),
}
MAINTENANCE_SUBFOLDER_NAMES: tuple[str, ...] = tuple(sorted(MAINTENANCE_SUBFOLDER_PARTS))


def _normalize_name(name: str) -> str:
    cleaned = str(name or "").strip().replace("\\", "/").strip("/")
    if not cleaned:
        raise ValueError("maintenance subfolder name must not be empty")
    return cleaned


def relative_maintenance_subfolder_parts(name: str) -> tuple[str, ...]:
    """Return canonical relative parts for a maintenance subfolder name."""
    cleaned = _normalize_name(name)
    if cleaned in MAINTENANCE_SUBFOLDER_PARTS:
        return MAINTENANCE_SUBFOLDER_PARTS[cleaned]
    # Allow future explicit subfolder names while preventing path traversal.
    parts = tuple(part for part in cleaned.split("/") if part and part not in {".", ".."})
    if not parts or len(parts) != len(cleaned.split("/")):
        raise ValueError("maintenance subfolder path is unsafe: " + str(name))
    return parts


def get_maintenance_subfolder(
    name: str,
    maintenance_root: str | Path | None = None,
) -> Path:
    """Return a maintenance subfolder path without creating it."""
    root = Path(maintenance_root).expanduser().resolve(strict=False) if maintenance_root is not None else get_maintenance_root()
    result = root
    for part in relative_maintenance_subfolder_parts(name):
        result = result / part
    return result


def ensure_maintenance_subfolder(
    name: str,
    maintenance_root: str | Path | None = None,
) -> Path:
    """Create and return one canonical maintenance subfolder."""
    path = get_maintenance_subfolder(name, maintenance_root=maintenance_root)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_all_maintenance_subfolders(
    maintenance_root: str | Path | None = None,
) -> dict[str, Path]:
    """Return all named maintenance subfolder paths without creating them."""
    return {
        name: get_maintenance_subfolder(name, maintenance_root=maintenance_root)
        for name in MAINTENANCE_SUBFOLDER_NAMES
    }


def ensure_maintenance_structure(
    maintenance_root: str | Path | None = None,
    names: Iterable[str] | None = None,
) -> dict[str, Path]:
    """Create a named maintenance folder set and return paths by name."""
    selected = tuple(names) if names is not None else MAINTENANCE_SUBFOLDER_NAMES
    return {
        name: ensure_maintenance_subfolder(name, maintenance_root=maintenance_root)
        for name in selected
    }


def describe_maintenance_subfolder_policy() -> dict[str, object]:
    """Return a serializable summary of the maintenance subfolder policy."""
    return {
        "schema_version": "1.0",
        "subfolder_names": list(MAINTENANCE_SUBFOLDER_NAMES),
        "subfolder_parts": {key: list(value) for key, value in MAINTENANCE_SUBFOLDER_PARTS.items()},
        "side_effect_free_on_import": True,
    }
