# project-path: kanda_reasoner_app/_project_support_path_contracts.py
"""Neutral Project support-path contracts shared by root and boundary owners."""

from __future__ import annotations

from pathlib import Path
from typing import TypeVar

from kanda_reasoner_app.portable_smoke_isolation import (
    resolve_portable_smoke_isolation,
)

__all__: list[str] = []

_SHOW_PROJECT_TO_AI_SUFFIX = "_show_project_to_AI"
_DELETE_AFTER_DAILY_WORK_SUFFIX = "_delete_after_daily_work"

_ExceptionT = TypeVar("_ExceptionT", bound=Exception)


def _normalize_project_source_root(
    active_project_root: str | Path,
    *,
    error_type: type[_ExceptionT] = RuntimeError,
) -> Path:
    """Return a normalized Project source root or raise the requested error."""
    root = Path(active_project_root).expanduser().resolve(strict=False)
    if root.name.endswith(_SHOW_PROJECT_TO_AI_SUFFIX):
        raise error_type(
            "ACTIVE_PROJECT_ROOT_IS_PROJECT_SUPPORT_ROOT:" + str(root)
        )
    if root.name.endswith(_DELETE_AFTER_DAILY_WORK_SUFFIX):
        raise error_type(
            "ACTIVE_PROJECT_ROOT_IS_TRANSIENT_GARBAGE_ROOT:" + str(root)
        )
    return root


def _canonical_transient_garbage_root(
    active_project_root: str | Path,
    *,
    error_type: type[_ExceptionT] = RuntimeError,
) -> Path:
    """Return canonical transient storage or a token-bound smoke override."""
    root = _normalize_project_source_root(
        active_project_root,
        error_type=error_type,
    )
    smoke = resolve_portable_smoke_isolation()
    if smoke is not None:
        return smoke.transient_root(root)
    folder_name = root.name + _DELETE_AFTER_DAILY_WORK_SUFFIX
    base = Path(root.anchor) if root.drive else root.parent
    return (base / folder_name).resolve(strict=False)
