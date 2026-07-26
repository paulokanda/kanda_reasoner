"""Private validation helpers for handoff_zip_exporter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .bundle_checker import check_ai_context_bundle
from .handoff_zip_exporter_support import _BYTES_PER_MB, _EXPORT_KIND, _is_destination_inside_project_root
from .schema_models import ProjectContext

__all__: list[str] = []

def _part_size_error(context: ProjectContext, message: str) -> dict[str, Any]:
    """Support part size error behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    message : str
        The message text.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "ok": False,
        "kind": _EXPORT_KIND,
        "project_slug": context.project_slug,
        "failures": [message],
    }

def _validate_destination(context: ProjectContext, destination: Path) -> dict[str, Any] | None:
    """Support validate destination behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    destination : Path
        The destination path.
    
    Returns
    -------
    dict[str, Any] | None
        The mapped values.
    """
    
    if not destination.exists() or not destination.is_dir():
        return _part_size_error(context, "Destination folder does not exist: " + str(destination))
    if _is_destination_inside_project_root(context.root, destination):
        return _part_size_error(
            context,
            "Destination folder is inside the active project root. "
            "Choose a folder outside: " + str(context.root),
        )
    return None


def _resolve_part_size(
    context: ProjectContext,
    part_size_mb: int,
    part_size_bytes: int | None,
    allowed_part_size_mb_options: tuple[int, ...],
) -> tuple[int | None, dict[str, Any] | None]:
    """Support resolve part size behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    part_size_mb : int
        The part size mb value.
    part_size_bytes : int | None
        The part size bytes value.
    
    Returns
    -------
    tuple[int | None, dict[str, Any] | None]
        The tuple of values.
    """
    
    if part_size_bytes is None:
        if part_size_mb not in allowed_part_size_mb_options:
            return None, _part_size_error(
                context,
                "part_size_mb must be one of " + ", ".join(str(item) for item in allowed_part_size_mb_options),
            )
        part_size_bytes = part_size_mb * _BYTES_PER_MB
    if part_size_bytes <= 0:
        return None, _part_size_error(context, "part_size_bytes must be positive")
    return int(part_size_bytes), None


def _check_bundle_if_requested(context: ProjectContext, check_bundle: bool) -> dict[str, Any] | None:
    """Support check bundle if requested behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    check_bundle : bool
        The check bundle value.
    
    Returns
    -------
    dict[str, Any] | None
        The mapped values.
    """
    
    if not check_bundle:
        return None
    check_result = check_ai_context_bundle(context)
    if bool(check_result.get("ok", False)):
        return None
    failures = check_result.get("failures", [])
    if not isinstance(failures, list):
        failures = ["Unknown bundle checker failure"]
    return {
        "ok": False,
        "kind": _EXPORT_KIND,
        "project_slug": context.project_slug,
        "failures": [str(item) for item in failures],
        "check_result": check_result,
    }
