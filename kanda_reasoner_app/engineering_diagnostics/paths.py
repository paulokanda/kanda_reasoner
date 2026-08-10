# project-path: kanda_reasoner_app/engineering_diagnostics/paths.py
"""Project-owned durable paths for Engineering Diagnostics."""

from __future__ import annotations

import os
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    ProjectToolBoundaryIdentity,
    canonical_project_support_root,
    project_support_root_blockers,
)

from .models import DiagnosticBoundaryError

__all__ = [
    "ENGINEERING_DIAGNOSTICS_DATABASE_NAME",
    "ENGINEERING_DIAGNOSTICS_SUPPORT_DIR",
    "engineering_diagnostics_database_path",
    "engineering_diagnostics_support_root",
]

ENGINEERING_DIAGNOSTICS_SUPPORT_DIR = "project_engineering_diagnostics"
ENGINEERING_DIAGNOSTICS_DATABASE_NAME = "engineering_diagnostics.sqlite3"


def _path_key(path: str | Path) -> str:
    value = Path(path).expanduser().resolve(strict=False)
    return os.path.normcase(str(value))


def engineering_diagnostics_support_root(
    boundary: ProjectToolBoundaryIdentity,
) -> Path:
    """Return canonical external Project Support storage for this box."""
    project_root = boundary.active_project_root.resolve(strict=False)
    canonical_support = canonical_project_support_root(project_root)
    supplied_support = boundary.active_project_support_root.resolve(strict=False)
    if _path_key(canonical_support) != _path_key(supplied_support):
        raise DiagnosticBoundaryError(
            "ENGINEERING_DIAGNOSTICS_SUPPORT_ROOT_MISMATCH"
        )
    blockers = project_support_root_blockers(project_root, supplied_support)
    if blockers:
        raise DiagnosticBoundaryError(
            "ENGINEERING_DIAGNOSTICS_SUPPORT_ROOT_BLOCKED:" + ",".join(blockers)
        )
    owner_root = (supplied_support / ENGINEERING_DIAGNOSTICS_SUPPORT_DIR).resolve(
        strict=False
    )
    try:
        owner_root.relative_to(project_root)
    except ValueError:
        pass
    else:
        raise DiagnosticBoundaryError(
            "ENGINEERING_DIAGNOSTICS_STORAGE_INSIDE_PROJECT_SOURCE"
        )
    return owner_root


def engineering_diagnostics_database_path(
    boundary: ProjectToolBoundaryIdentity,
) -> Path:
    """Return the sole SQLite file owned by Engineering Diagnostics."""
    return engineering_diagnostics_support_root(boundary) / (
        ENGINEERING_DIAGNOSTICS_DATABASE_NAME
    )
