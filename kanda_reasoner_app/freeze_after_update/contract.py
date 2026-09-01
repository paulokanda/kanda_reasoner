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
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_first_prompt_files_dir,
    project_analysis_evidence_root,
)

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
from .freeze_entry_contract import (
    _contract_error,
    _preview_root_binding_error,
    preview_freeze_entry,
    validate_freeze_entry_preview,
    write_confirmed_freeze_entry,
)

FreezeAfterUpdateResult = _FreezeAfterUpdateResult
FreezeAfterUpdateStatus = _FreezeAfterUpdateStatus

# Split-module invariant: explicit write authorization remains fail-closed when
# confirmation is not True; root checks remain owned by _preview_root_binding_error.


def inspect_freeze_after_update_box(project_root: str | Path) -> FreezeAfterUpdateResult:
    """Inspect the selected project external support box."""
    return _inspect_freeze_after_update_box(project_root)


def ensure_freeze_after_update_box(project_root: str | Path) -> FreezeAfterUpdateResult:
    """Create or repair the selected project external support box."""
    return _ensure_freeze_after_update_box(project_root)


def generate_freeze_after_update_ai_files(project_root: str | Path) -> FreezeAfterUpdateResult:
    """Build or refresh Freeze Feature After Update AI-send files."""
    return _generate_freeze_after_update_ai_files(project_root)


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
    """Refresh generated AI-visible context after a local freeze write."""

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
            timeout=300,
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
