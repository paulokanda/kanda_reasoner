# project-path: kanda_reasoner_app/freeze_after_update/contract.py
"""Public contract for the Freeze Feature After Update box.

This module is the only public bridge the GUI and other app code should use
for Freeze Feature After Update operations.  It intentionally keeps GUI code
away from reusable freeze-engine internals.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping

from .box_bootstrapper import (
    ensure_freeze_after_update_box as _ensure_freeze_after_update_box,
    inspect_freeze_after_update_box as _inspect_freeze_after_update_box,
)
from .result import (
    FreezeAfterUpdateResult as _FreezeAfterUpdateResult,
    FreezeAfterUpdateStatus as _FreezeAfterUpdateStatus,
)
from .send_pack_builder import (
    generate_freeze_after_update_ai_files as _generate_freeze_after_update_ai_files,
)

FreezeAfterUpdateResult = _FreezeAfterUpdateResult
FreezeAfterUpdateStatus = _FreezeAfterUpdateStatus


def inspect_freeze_after_update_box(project_root: str | Path) -> FreezeAfterUpdateResult:
    """Inspect the selected project external support box."""
    return _inspect_freeze_after_update_box(project_root)


def ensure_freeze_after_update_box(project_root: str | Path) -> FreezeAfterUpdateResult:
    """Create or repair the selected project external support box."""
    return _ensure_freeze_after_update_box(project_root)


def generate_freeze_after_update_ai_files(project_root: str | Path) -> FreezeAfterUpdateResult:
    """Build or refresh Freeze Feature After Update AI-send files."""
    return _generate_freeze_after_update_ai_files(project_root)
from kanda_reasoner_app.project_analysis_evidence_paths import project_analysis_evidence_root

__all__ = [
    "FreezeAfterUpdateResult",
    "FreezeAfterUpdateStatus",
    "ensure_freeze_after_update_box",
    "generate_freeze_after_update_ai_files",
    "inspect_freeze_after_update_box",
    "preview_freeze_entry",
    "validate_freeze_entry_preview",
    "write_confirmed_freeze_entry",
    "refresh_freeze_exposure",
    "refresh_ai_compliance_context",
]



def _resolved_project_root(project_root: str | Path) -> Path:
    """Return the real selected project root used for user-facing metadata."""
    return Path(project_root).expanduser().resolve(strict=False)


def _freeze_state_owner_root(project_root: str | Path) -> Path:
    """Return the external freeze-state owner root used by the ledger engine."""
    return project_analysis_evidence_root(project_root)


def _preview_for_ledger_engine(preview: Mapping[str, Any], owner_root: Path) -> dict[str, Any]:
    """Return an engine-facing preview with the owner root as project_root.

    The reusable local freeze writer from project_freeze_ledger validates that
    the preview was produced for the same active root passed to validation and
    write calls. After the external-root migration, that engine root is the
    external project-support root, while the public contract still reports the
    real selected project source root to the GUI. This adapter keeps both
    boundaries true without mutating the read-only preview shown to the user.
    """
    engine_preview = dict(preview)
    engine_preview["project_root"] = str(owner_root)
    engine_preview["freeze_state_owner_root"] = str(owner_root)
    return engine_preview

def preview_freeze_entry(project_root: str | Path, inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Return a local freeze-entry preview without writing project memory.

    The deterministic engine lives in ``project_freeze_ledger/freeze_tools``.
    The Freeze Feature After Update tab must call this public contract instead
    of importing the engine module directly.
    """

    try:
        from project_freeze_ledger.freeze_tools.local_freeze_writer import (
            preview_freeze_entry as _engine_preview_freeze_entry,
        )

        resolved_project_root = _resolved_project_root(project_root)
        owner_root = _freeze_state_owner_root(resolved_project_root)
        preview = _engine_preview_freeze_entry(owner_root, inputs)
        result = _with_contract_status(preview, operation="preview_freeze_entry")
        # Project root is an engine-facing contract field. After the external-root
        # migration it must equal the freeze-state owner root, while the selected
        # source project remains available through explicit display/provenance fields.
        result["project_root"] = str(owner_root)
        result["freeze_state_owner_root"] = str(owner_root)
        result["selected_project_root"] = str(resolved_project_root)
        result["display_project_root"] = str(resolved_project_root)
        return result
    except Exception as exc:
        return _contract_error(
            operation="preview_freeze_entry",
            project_root=project_root,
            message=str(exc),
        )


def validate_freeze_entry_preview(
    project_root: str | Path,
    preview: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate a freeze-entry preview without writing files."""

    try:
        from project_freeze_ledger.freeze_tools.local_freeze_writer import (
            validate_freeze_entry_preview as _engine_validate_freeze_entry_preview,
        )

        resolved_project_root = _resolved_project_root(project_root)
        owner_root = _freeze_state_owner_root(resolved_project_root)
        engine_preview = _preview_for_ledger_engine(preview, owner_root)
        validation = _engine_validate_freeze_entry_preview(owner_root, engine_preview)
        result = dict(validation)
        result.setdefault("ok", bool(result.get("ok")))
        result.setdefault("errors", [])
        result.setdefault("warnings", [])
        result["operation"] = "validate_freeze_entry_preview"
        result["project_root"] = str(owner_root)
        result["freeze_state_owner_root"] = str(owner_root)
        result["selected_project_root"] = str(resolved_project_root)
        result["display_project_root"] = str(resolved_project_root)
        return result
    except Exception as exc:
        return _contract_error(
            operation="validate_freeze_entry_preview",
            project_root=project_root,
            message=str(exc),
        )


def write_confirmed_freeze_entry(
    project_root: str | Path,
    preview: Mapping[str, Any],
    *,
    confirmation: bool = False,
) -> dict[str, Any]:
    """Write a confirmed local freeze entry through the deterministic engine.

    This is the only contract write path for the future tab workflow.  It
    refuses to write unless ``confirmation`` is exactly ``True``; the engine
    performs the final safety checks and atomic writes.
    """

    try:
        from project_freeze_ledger.freeze_tools.local_freeze_writer import (
            write_confirmed_freeze_entry as _engine_write_confirmed_freeze_entry,
        )

        resolved_project_root = _resolved_project_root(project_root)
        owner_root = _freeze_state_owner_root(resolved_project_root)
        engine_preview = _preview_for_ledger_engine(preview, owner_root)
        result = _engine_write_confirmed_freeze_entry(
            owner_root,
            engine_preview,
            confirmation=confirmation,
        )
        output = dict(result)
        output.setdefault("ok", bool(output.get("ok")))
        output.setdefault("errors", [])
        output.setdefault("warnings", [])
        output["operation"] = "write_confirmed_freeze_entry"
        output["project_root"] = str(owner_root)
        output["freeze_state_owner_root"] = str(owner_root)
        output["selected_project_root"] = str(resolved_project_root)
        output["display_project_root"] = str(resolved_project_root)
        return output
    except Exception as exc:
        return _contract_error(
            operation="write_confirmed_freeze_entry",
            project_root=project_root,
            message=str(exc),
        )

from kanda_reasoner_app.project_analysis_evidence_paths import analysis_first_prompt_files_dir


def refresh_freeze_exposure(project_root: str | Path, *, max_items: int = 40) -> dict[str, Any]:
    """Return current freeze-memory exposure for the active project.

    This is intentionally read-only in v1.1.  It wraps the existing frozen
    memory exposure engine so later GUI code has a stable public access point.
    """

    try:
        from project_freeze_ledger.freeze_tools.expose_freeze_memory import (
            audit_freeze_memory,
            render_text_report,
        )

        owner_root = project_analysis_evidence_root(project_root)
        audit = audit_freeze_memory(str(owner_root))
        report = render_text_report(audit, max_items=max(1, int(max_items)))
        return {
            "ok": audit.status in {"OK", "STALE_EXPOSURE", "INDEX_MISMATCH"},
            "operation": "refresh_freeze_exposure",
            "project_root": str(Path(project_root).expanduser().resolve()),
            "freeze_state_owner_root": str(owner_root),
            "status": audit.status,
            "report": report,
            "audit": audit.to_dict(),
            "errors": list(audit.errors),
            "warnings": list(audit.warnings),
        }
    except Exception as exc:
        return _contract_error(
            operation="refresh_freeze_exposure",
            project_root=project_root,
            message=str(exc),
        )


def refresh_ai_compliance_context(project_root: str | Path, *, max_items: int = 40) -> dict[str, Any]:
    """Refresh all AI-visible freeze context after a local freeze write.

    The canonical freeze memory remains in the selected project external support root.
    This function refreshes the generated AI-send pack and the startup upload
    channel that the external AI reads at the beginning of a programming
    session.  It does not write project-specific memory into
    ``project_freeze_ledger``.
    """

    resolved_project_root = Path(project_root).expanduser().resolve()
    ai_send_result = None
    startup_ok = False
    completed_stdout = ""
    completed_stderr = ""
    completed_returncode = -1

    try:
        app_root = Path(__file__).resolve().parents[2]
        workspace_root = app_root / "kanda_prompt_workspace"
        script = workspace_root / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
        startup_delivery_dir = analysis_first_prompt_files_dir(resolved_project_root)
        startup_zip = startup_delivery_dir / "first_prompts_to_ai.zip"
        read_before_all = startup_delivery_dir / "tell_AI_read_before_all.md"
        prompt_library_zip = startup_delivery_dir / "prompt_library.zip"

        # Deprecated project-local files_to_send_ai ZIPs are cleaned, not regenerated.
        # Freeze context now travels through the external Show Project to AI startup
        # and source-archive delivery.
        ai_send_result = generate_freeze_after_update_ai_files(resolved_project_root)

        if not script.is_file():
            raise FileNotFoundError(f"Missing startup sync tool: {script}")

        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--sync",
                "--yes",
                "--project-root",
                str(resolved_project_root),
            ],
            cwd=str(workspace_root),
            text=True,
            capture_output=True,
        )

        startup_ok = completed.returncode == 0
        completed_stdout = completed.stdout
        completed_stderr = completed.stderr
        completed_returncode = completed.returncode

        # Audit after both generated exposure channels have been refreshed.
        exposure = refresh_freeze_exposure(resolved_project_root, max_items=max_items)
        errors = list(exposure.get("errors", []))
        warnings = list(exposure.get("warnings", []))

        ai_send_ok = bool(getattr(ai_send_result, "ok", False))
        if not ai_send_ok:
            errors.append("AI-send exposure refresh failed.")
            if getattr(ai_send_result, "message", ""):
                errors.append(str(ai_send_result.message))

        if not startup_ok:
            errors.append("Startup freeze context refresh failed.")
            if completed.stderr:
                errors.append(completed.stderr.strip())

        return {
            "ok": bool(exposure.get("ok")) and ai_send_ok and startup_ok and not errors,
            "operation": "refresh_ai_compliance_context",
            "project_root": str(resolved_project_root),
            "freeze_exposure": exposure,
            "freeze_status": exposure.get("status"),
            "report": exposure.get("report", ""),
            "ai_send_refreshed": ai_send_ok,
            "ai_send_status": getattr(getattr(ai_send_result, "status", None), "value", str(getattr(ai_send_result, "status", ""))),
            "ai_send_message": str(getattr(ai_send_result, "message", "")),
            "ai_send_zip": "",
            "ai_send_instruction": "",
            "startup_context_refreshed": startup_ok,
            "startup_sync_stdout": completed_stdout,
            "startup_sync_stderr": completed_stderr,
            "startup_sync_returncode": completed_returncode,
            "startup_zip": str(startup_zip),
            "read_before_all_instruction": str(read_before_all),
            "paste_after_uploading": str(read_before_all),  # Backward-compatible key; active file is tell_AI_read_before_all.md.
            "prompt_library_zip": str(prompt_library_zip),
            "project_local_ai_send_generation_deprecated": True,
            "generated_context_filename": "09_active_project_freeze_context.md",
            "errors": errors,
            "warnings": warnings,
        }
    except Exception as exc:
        exposure = refresh_freeze_exposure(resolved_project_root, max_items=max_items)
        result = _contract_error(
            operation="refresh_ai_compliance_context",
            project_root=resolved_project_root,
            message=str(exc),
        )
        result["freeze_exposure"] = exposure
        result["report"] = exposure.get("report", "")
        result["ai_send_refreshed"] = bool(getattr(ai_send_result, "ok", False)) if ai_send_result is not None else False
        result["ai_send_status"] = getattr(getattr(ai_send_result, "status", None), "value", str(getattr(ai_send_result, "status", ""))) if ai_send_result is not None else ""
        result["ai_send_message"] = str(getattr(ai_send_result, "message", "")) if ai_send_result is not None else ""
        result["ai_send_zip"] = str(getattr(ai_send_result, "output_zip", "") or "") if ai_send_result is not None else ""
        result["ai_send_instruction"] = str(getattr(ai_send_result, "output_instruction", "") or "") if ai_send_result is not None else ""
        result["startup_context_refreshed"] = startup_ok
        result["startup_sync_stdout"] = completed_stdout
        result["startup_sync_stderr"] = completed_stderr
        result["startup_sync_returncode"] = completed_returncode
        try:
            app_root = Path(__file__).resolve().parents[2]
            workspace_root = app_root / "kanda_prompt_workspace"
            startup_delivery_dir = analysis_first_prompt_files_dir(resolved_project_root)
            result["startup_zip"] = str(startup_delivery_dir / "first_prompts_to_ai.zip")
            result["read_before_all_instruction"] = str(startup_delivery_dir / "tell_AI_read_before_all.md")
            result["paste_after_uploading"] = str(startup_delivery_dir / "tell_AI_read_before_all.md")
            result["prompt_library_zip"] = str(startup_delivery_dir / "prompt_library.zip")
            result["generated_context_filename"] = "09_active_project_freeze_context.md"
        except Exception:
            pass
        return result


def _with_contract_status(preview: Mapping[str, Any], *, operation: str) -> dict[str, Any]:
    """Support with contract status behavior.
    
    Parameters
    ----------
    preview : Mapping[str, Any]
        The preview value.
    operation : str
        The operation value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    result = dict(preview)
    result.setdefault("errors", [])
    result.setdefault("warnings", [])
    result["operation"] = operation
    result["ok"] = bool(result.get("is_writable")) and not result.get("errors")
    return result


def _contract_error(*, operation: str, project_root: str | Path, message: str) -> dict[str, Any]:
    """Support contract error behavior.
    
    Parameters
    ----------
    operation : str
        The operation value.
    project_root : str | Path
        The project root path.
    message : str
        The message text.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    try:
        resolved_root = str(Path(project_root).expanduser().resolve())
    except Exception:
        resolved_root = str(project_root)
    return {
        "ok": False,
        "operation": operation,
        "project_root": resolved_root,
        "errors": [message],
        "warnings": [],
        "message": message,
    }
