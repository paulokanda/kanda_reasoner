# project-path: tools/validate_project_web_ai_governed_apply_cycle_reset_v1.py
"""Validate terminal Governed Apply cycle reset and truthful Preview state."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace


def require(condition: bool, message: str) -> None:
    """Raise one deterministic assertion when a gate fails."""
    if not condition:
        raise AssertionError(message)


def _receipt(status: str, project_id: str = "project-1") -> object:
    """Return one synthetic terminal apply receipt."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts import (
        ProjectWebAIApplyReceipt,
    )

    return ProjectWebAIApplyReceipt(
        schema_version="1.0",
        transaction_id="a" * 32,
        authorization_id="b" * 32,
        operation_id="c" * 32,
        status=status,
        operation_class="EXTERNAL_PROJECT_CHANGE",
        project_id=project_id,
        project_root="C:/fixture",
        project_root_fingerprint="f" * 64,
        project_epoch=1,
        snapshot_id="snapshot-1",
        preview_fingerprint="d" * 64,
        changed_files=("sample.py",),
        source_sha256=("1" * 64,),
        installed_sha256=("2" * 64,),
        backup_root="C:/fixture_daily/backups",
        validation_markers=("PASS",),
        started_at_utc="2026-07-22T00:00:00+00:00",
        completed_at_utc="2026-07-22T00:00:01+00:00",
        error="",
        receipt_path="C:/fixture_support/receipt.json",
    )


def validate_receipt_cycle_contracts() -> None:
    """Prove captions and retry/refresh decisions for terminal outcomes."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts import (
        apply_preview_caption,
        receipt_allows_retry_after_shadow_delete,
        receipt_matches_fresh_project_context,
    )

    success = _receipt("APPLIED_SOURCE_VERIFIED")
    rollback = _receipt("ROLLED_BACK")
    unresolved = _receipt("UNRESOLVED")
    require(apply_preview_caption(None) == "View Shadow Preview", "base caption drift")
    require(
        apply_preview_caption(success) == "View Applied Preview",
        "success caption drift",
    )
    require(
        apply_preview_caption(rollback) == "View Rolled-Back Preview",
        "rollback caption overstates success",
    )
    require(
        apply_preview_caption(unresolved) == "View Unresolved Preview",
        "unresolved caption drift",
    )
    require(
        receipt_allows_retry_after_shadow_delete(rollback),
        "rolled-back receipt did not reopen retry after Shadow deletion",
    )
    require(
        not receipt_allows_retry_after_shadow_delete(success),
        "successful receipt cleared before fresh handoff",
    )
    require(
        not receipt_allows_retry_after_shadow_delete(unresolved),
        "unresolved receipt was cleared",
    )
    require(
        receipt_matches_fresh_project_context(
            success,
            project_id="project-1",
            project_root_fingerprint="f" * 64,
        ),
        "successful receipt did not match fresh Project context",
    )
    require(
        not receipt_matches_fresh_project_context(
            success,
            project_id="project-2",
            project_root_fingerprint="f" * 64,
        ),
        "cross-Project receipt was retired",
    )
    require(
        not receipt_matches_fresh_project_context(
            rollback,
            project_id="project-1",
            project_root_fingerprint="f" * 64,
        ),
        "rolled-back receipt used fresh-handoff retirement",
    )
    print("TERMINAL_APPLY_PREVIEW_CAPTIONS_TRUTHFUL: PASS")
    print("ROLLED_BACK_SHADOW_DELETE_REOPENS_RETRY: PASS")
    print("SUCCESSFUL_APPLY_REQUIRES_FRESH_CONTEXT_RESET: PASS")
    print("CROSS_PROJECT_RECEIPT_RESET_REJECTED: PASS")


def validate_source_integration(root: Path) -> None:
    """Require host lifecycle integration without weakening apply authority."""
    engine = root / "kanda_reasoner_app" / "reasoner_engine"
    receipts = (engine / "project_web_ai_apply_receipts.py").read_text(
        encoding="utf-8"
    )
    workflow = (engine / "project_web_ai_apply_workflow.py").read_text(
        encoding="utf-8"
    )
    preparation = (engine / "project_web_ai_change_preparation.py").read_text(
        encoding="utf-8"
    )
    tab = (engine / "project_web_ai_tab.py").read_text(encoding="utf-8")
    require(
        '"ROLLED_BACK": "View Rolled-Back Preview"' in receipts,
        "rolled-back caption contract missing",
    )
    require(
        "receipt_matches_fresh_project_context" in workflow,
        "fresh-context apply retirement owner missing",
    )
    require(
        "self._release_rolled_back_apply_receipt()" in preparation,
        "Shadow deletion does not release rolled-back retry authority",
    )
    require(
        "self.new_chat()" in preparation,
        "fresh source generation can reuse stale advisory exchange",
    )
    require(
        "_retire_change_cycle_after_context_refresh(snapshot)" in tab,
        "context reload does not retire the successful apply cycle",
    )
    require(
        "execute_project_web_ai_apply" not in tab,
        "tab gained direct write-broker execution authority",
    )
    print("HOST_LIFECYCLE_APPLY_CYCLE_RESET_WIRED: PASS")
    print("FRESH_SOURCE_REQUIRES_NEW_ADVISORY_CHAT: PASS")
    print("REMOTE_AI_WRITE_AUTHORITY_UNCHANGED: PASS")


def _preview(root: Path) -> object:
    """Return one synthetic Shadow Preview rooted in a disposable folder."""
    from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
        ProjectWebAIShadowPreview,
        ShadowTargetPreview,
    )

    shadow = root / "operation" / "shadow"
    shadow.mkdir(parents=True)
    target = shadow / "sample.py"
    target.write_text("value = 2\n", encoding="utf-8")
    return ProjectWebAIShadowPreview(
        operation_id="c" * 32,
        shadow_root=str(shadow),
        summary="summary",
        targets=(
            ShadowTargetPreview(
                relative_path="sample.py",
                original_sha256="1" * 64,
                proposed_sha256="2" * 64,
                shadow_path=str(target),
                unified_diff=(
                    "--- a/sample.py\n+++ b/sample.py\n"
                    "@@ -1 +1 @@\n-value = 1\n+value = 2\n"
                ),
                python_syntax_status="PASS",
            ),
        ),
        affected_public_contracts=(),
        required_validators=(),
        known_risks=(),
        validation_markers=("PASS",),
    )


def validate_real_widget() -> None:
    """Prove terminal cycle projection on the real Project Web AI widget."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("REAL_QT_APPLY_CYCLE_RESET: NOT_APPLICABLE")
        return

    from kanda_reasoner_app.reasoner_engine.project_web_ai_tab import (
        ProjectWebAITab,
    )

    app = QApplication.instance() or QApplication([])
    widget = ProjectWebAITab()
    with tempfile.TemporaryDirectory(prefix="kanda_apply_cycle_") as temp:
        temp_root = Path(temp)
        rollback_preview = _preview(temp_root / "rollback")
        widget._change_preview = rollback_preview
        widget._change_operation = object()
        widget._apply_receipt = _receipt("ROLLED_BACK")
        widget._update_change_preparation_state(False)
        require(
            widget.prepare_changes_button.text() == "View Rolled-Back Preview",
            "real widget overstates rolled-back Preview",
        )
        widget._delete_current_shadow_preview()
        require(widget._apply_receipt is None, "rollback retry receipt not released")
        require(widget._change_preview is None, "rolled-back Shadow not deleted")

        success_preview = _preview(temp_root / "success")
        old_chat_id = widget._active_chat_id
        widget._history[:] = [
            {"role": "user", "content": "old question"},
            {"role": "assistant", "content": "old answer"},
        ]
        widget._change_preview = success_preview
        widget._change_operation = object()
        widget._apply_receipt = _receipt("APPLIED_SOURCE_VERIFIED")
        snapshot = SimpleNamespace(
            project_id="project-1",
            project_root_fingerprint="f" * 64,
        )
        require(
            widget._retire_change_cycle_after_context_refresh(snapshot),
            "fresh context did not retire successful cycle",
        )
        require(widget._apply_receipt is None, "successful receipt remained in memory")
        require(widget._change_preview is None, "successful Shadow remained in memory")
        require(widget._change_operation is None, "successful operation remained active")
        require(widget._active_chat_id != old_chat_id, "new advisory chat not created")
        require(widget._history == [], "stale advisory exchange remained active")
        require(
            widget._chat_store.get(old_chat_id) is not None,
            "prior memory-only chat was destructively removed",
        )
    widget.close()
    app.processEvents()
    print("REAL_QT_APPLY_CYCLE_RESET: PASS")
    print("REAL_QT_FRESH_CONTEXT_STARTS_NEW_ADVISORY_CHAT: PASS")


def validate_module_sizes(root: Path) -> None:
    """Require all touched Python modules to remain within the hard limit."""
    paths = (
        "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_receipts.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py",
        "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
        "tools/validate_project_web_ai_governed_apply_cycle_reset_v1.py",
    )
    for relative in paths:
        count = len((root / relative).read_text(encoding="utf-8").splitlines())
        require(count <= 500, relative + " exceeds 500 physical lines")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    """Run deterministic cycle-reset and optional real-widget validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    sys.path.insert(0, str(root))
    validate_receipt_cycle_contracts()
    validate_source_integration(root)
    validate_real_widget()
    validate_module_sizes(root)
    print("VALIDATION OK: project-web-ai-governed-apply-cycle-reset-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
