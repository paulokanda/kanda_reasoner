"""Build uploadable AI-send files for Freeze Feature After Update.

This app-facing module delegates generation to the blueprint freeze generator
under project_freeze_ledger/freeze_tools. It exists so GUI code can keep using
the public app contract while generator logic remains in its own box.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .blueprint_adapter import generate_ai_send_files
from .result import FreezeAfterUpdateResult, FreezeAfterUpdateStatus


_STATUS_MAP = {
    "valid": FreezeAfterUpdateStatus.VALID,
    "created": FreezeAfterUpdateStatus.CREATED,
    "updated": FreezeAfterUpdateStatus.UPDATED,
    "pack_created": FreezeAfterUpdateStatus.PACK_CREATED,
    "incomplete": FreezeAfterUpdateStatus.INCOMPLETE,
    "invalid_project_root": FreezeAfterUpdateStatus.INVALID_PROJECT_ROOT,
    "invalid_box_path": FreezeAfterUpdateStatus.INVALID_BOX_PATH,
    "error": FreezeAfterUpdateStatus.ERROR,
}


def _optional_path(value: Any) -> Path | None:
    if value in (None, ""):
        return None
    return Path(str(value))


def _path_tuple(values: Any) -> tuple[Path, ...]:
    if not isinstance(values, list):
        return ()
    return tuple(Path(str(item)) for item in values)


def _from_payload(payload: dict[str, Any]) -> FreezeAfterUpdateResult:
    status_text = str(payload.get("status") or "error")
    status = _STATUS_MAP.get(status_text, FreezeAfterUpdateStatus.ERROR)
    return FreezeAfterUpdateResult(
        status=status,
        project_root=_optional_path(payload.get("project_root")),
        box_root=_optional_path(payload.get("box_root")),
        message=str(payload.get("message") or ""),
        missing_paths=_path_tuple(payload.get("missing_paths")),
        created_paths=_path_tuple(payload.get("created_paths")),
        output_zip=_optional_path(payload.get("output_zip")),
        output_instruction=_optional_path(payload.get("output_instruction")),
        freeze_count=int(payload.get("freeze_count") or 0),
    )


def generate_freeze_after_update_ai_files(project_root: Path | str) -> FreezeAfterUpdateResult:
    """Return a deprecated no-op result for legacy AI-send generation.

    Freeze memory is now exposed through the Show Project to AI first/second
    prompt files and the source archive project ZIPs.  The old
    project_freeze_after_update/files_to_send_ai ZIP pack lived inside the
    project source tree and polluted source archives, so this public function no
    longer creates that folder or ZIP.  It also removes any stale project-local
    files_to_send_ai folder if present.
    """
    root = Path(project_root).expanduser().resolve(strict=False)
    try:
        from kanda_reasoner_app.generated_artifact_hygiene import cleanup_project_generated_zip_noise

        cleanup = cleanup_project_generated_zip_noise(root)
        if cleanup.get("errors"):
            return FreezeAfterUpdateResult(
                status=FreezeAfterUpdateStatus.ERROR,
                project_root=root,
                box_root=root / "project_freeze_after_update",
                message="Failed to clean deprecated AI-send files: " + str(cleanup.get("errors")),
            )
        return FreezeAfterUpdateResult(
            status=FreezeAfterUpdateStatus.VALID,
            project_root=root,
            box_root=root / "project_freeze_after_update",
            message=(
                "Deprecated project-local files_to_send_ai ZIP generation skipped. "
                "Freeze context is delivered through Show Project to AI first_prompt_files "
                "and second_prompt_files/source_archive artifacts."
            ),
            output_zip=None,
            output_instruction=None,
        )
    except Exception as exc:
        return FreezeAfterUpdateResult(
            status=FreezeAfterUpdateStatus.ERROR,
            project_root=root,
            box_root=root / "project_freeze_after_update",
            message="Failed to clean deprecated files_to_send_ai output: " + str(exc),
        )
