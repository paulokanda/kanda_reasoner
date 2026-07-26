# project-path: kanda_reasoner_app/manage_architecture/architecture_review_card_lifecycle.py
"""Own Architecture Review card identity, invalidation, and release lifecycle."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_background_cancel import (
    cancel_planner_background_work as _cancel_planner_background_work,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
    selected_planner_version,
)

__all__ = [
    "bind_architecture_review_card_lifecycle",
    "clear_architecture_review_card_state",
    "handle_planner_target_selection",
    "release_completed_architecture_review_card",
    "tool_source_root",
]

_PLANNER_RESULT_ATTRS = (
    "_large_file_refactor_last_analysis",
    "_large_file_refactor_last_plan",
    "_large_file_refactor_llm_result",
    "_large_file_refactor_plan_ai_review_result",
    "_large_file_refactor_web_ai_proposal",
    "_large_file_refactor_preview_bundle",
    "_large_file_refactor_preview_write_result",
    "_large_file_refactor_import_migration_preview",
    "_large_file_refactor_preview_validation",
    "_large_file_refactor_patch_gate_result",
    "_large_file_refactor_project_patch_payload_result",
    "_large_file_refactor_payload_apply_gate_result",
    "_large_file_refactor_heuristic_version",
    "_large_file_refactor_local_ai_version",
    "_large_file_refactor_web_ai_version",
    "_large_file_refactor_last_generated_native_version",
)

_WORKBENCH_RESULT_ATTRS = (
    "_large_file_refactor_workbench_plan_snapshot",
    "_large_file_refactor_workbench_intake",
    "_large_file_refactor_workbench_dependency_readiness",
    "_large_file_refactor_workbench_real_preview",
    "_large_file_refactor_workbench_structural_validation",
    "_large_file_refactor_workbench_preflight_backup",
    "_large_file_refactor_workbench_source_payload",
    "_large_file_refactor_workbench_guarded_apply",
    "_large_file_refactor_workbench_post_apply_validation",
    "_large_file_refactor_workbench_rollback",
    "_large_file_refactor_workbench_behavior_validation",
    "_large_file_refactor_workbench_completion_evidence",
    "_large_file_refactor_workbench_completion_transaction",
    "_large_file_refactor_workbench_completion_apply_outcome",
    "_large_file_refactor_workbench_completion_rollback_result",
)

_WORKBENCH_BUTTON_ATTRS = (
    "_large_file_refactor_workbench_dependency_button",
    "_large_file_refactor_workbench_real_preview_button",
    "_large_file_refactor_workbench_validate_button",
    "_large_file_refactor_workbench_preflight_button",
    "_large_file_refactor_workbench_source_payload_button",
    "_large_file_refactor_workbench_completion_prepare_button",
    "_large_file_refactor_workbench_transaction_prepare_button",
    "_large_file_refactor_workbench_refactor_large_module_button",
    "_large_file_refactor_workbench_transaction_rollback_button",
)


def tool_source_root() -> Path:
    """Return reusable KANDA Reasoner Tool source root from this installed module."""
    return Path(__file__).resolve().parents[2]


def bind_architecture_review_card_lifecycle(window: object) -> None:
    """Bind project-root and AST-target changes to one fail-closed card lifecycle."""
    if bool(getattr(window, "_architecture_review_card_lifecycle_bound", False)):
        return
    root_edit = getattr(window, "_root_path_edit", None)
    target_edit = getattr(window, "_large_module_target_edit", None)
    root_text = _widget_text(root_edit)
    target_text = _widget_text(target_edit)
    window._architecture_review_card_project_key = _path_key(root_text)
    window._architecture_review_card_project_text = root_text
    window._architecture_review_card_target_key = _target_key(root_text, target_text)
    window._architecture_review_card_target_text = target_text
    window._architecture_review_lifecycle_resetting = False
    if root_edit is not None:
        root_edit.textChanged.connect(
            lambda text="": _project_root_changed(window, str(text))
        )
    if target_edit is not None:
        target_edit.textChanged.connect(
            lambda text="": _ast_target_changed(window, str(text))
        )
    window._architecture_review_card_lifecycle_bound = True


def handle_planner_target_selection(window: object, selected_path: str) -> bool:
    """Accept one Planner target only after unloading stale downstream card state."""
    root_text = _root_text(window)
    new_key = _target_key(root_text, selected_path)
    current_key = str(getattr(window, "_architecture_review_card_target_key", ""))
    if new_key == current_key:
        return True
    if _architecture_operation_open(window):
        _status(window, "Target change blocked: Architecture operation is still reading the current card.")
        return False
    if _transaction_open(window):
        _status(window, "Target change blocked: current refactor transaction still owns the card.")
        return False
    _cancel_planner_background_work(window)
    _clear_planner_results(window, clear_candidates=False)
    _clear_workbench_results(window)
    window._architecture_review_card_target_key = new_key
    window._architecture_review_card_target_text = str(selected_path)
    return True


def clear_architecture_review_card_state(
    window: object,
    *,
    include_ast: bool,
    clear_planner_candidates: bool,
    reason: str,
) -> None:
    """Forget one loaded card from Tool GUI memory without deleting project-owned truth."""
    if bool(getattr(window, "_architecture_review_lifecycle_resetting", False)):
        return
    window._architecture_review_lifecycle_resetting = True
    try:
        _cancel_planner_background_work(window)
        if include_ast:
            _clear_ast_state(window)
        _clear_planner_results(window, clear_candidates=clear_planner_candidates)
        _clear_workbench_results(window)
        _status(window, reason)
    finally:
        window._architecture_review_lifecycle_resetting = False


def release_completed_architecture_review_card(window: object) -> None:
    """Eject a completed refactor card while preserving durable project artifacts."""
    outcome = getattr(
        window,
        "_large_file_refactor_workbench_completion_apply_outcome",
        None,
    )
    final_state = str(getattr(outcome, "final_transaction_state", ""))
    if not final_state.startswith("COMPLETED_"):
        return
    evidence = getattr(
        window,
        "_large_file_refactor_workbench_completion_evidence",
        None,
    )
    contract = getattr(evidence, "contract", None)
    target_text = str(getattr(contract, "target_file", "") or "")
    if not target_text:
        target_text = _widget_text(getattr(window, "_large_module_target_edit", None))
    clear_architecture_review_card_state(
        window,
        include_ast=False,
        clear_planner_candidates=True,
        reason=(
            "Refactor completed. Card released from Architecture Review memory; "
            "project source, Preview evidence, transaction receipt, and help files "
            "remain owned by the active project."
        ),
    )
    _remove_completed_ast_target(window, target_text)
    next_text = _widget_text(getattr(window, "_large_module_target_edit", None))
    window._architecture_review_card_target_key = _target_key(_root_text(window), next_text)
    window._architecture_review_card_target_text = next_text


def _project_root_changed(window: object, new_text: str) -> None:
    if bool(getattr(window, "_architecture_review_lifecycle_resetting", False)):
        return
    new_key = _path_key(new_text)
    old_key = str(getattr(window, "_architecture_review_card_project_key", ""))
    if new_key == old_key:
        return
    if _architecture_operation_open(window):
        _restore_edit_text(
            window,
            "_root_path_edit",
            str(getattr(window, "_architecture_review_card_project_text", "")),
        )
        _status(window, "Project Root change blocked: Architecture operation is still reading the current card.")
        return
    if _transaction_open(window):
        _restore_edit_text(
            window,
            "_root_path_edit",
            str(getattr(window, "_architecture_review_card_project_text", "")),
        )
        _status(window, "Project Root change blocked: current refactor transaction still owns the card.")
        return
    window._architecture_review_card_project_key = new_key
    window._architecture_review_card_project_text = new_text
    window._architecture_review_card_target_key = ""
    window._architecture_review_card_target_text = ""
    clear_architecture_review_card_state(
        window,
        include_ast=True,
        clear_planner_candidates=True,
        reason="Project Root changed. Architecture Review unloaded the previous project card.",
    )


def _ast_target_changed(window: object, new_text: str) -> None:
    if bool(getattr(window, "_architecture_review_lifecycle_resetting", False)):
        return
    root_text = _root_text(window)
    new_key = _target_key(root_text, new_text)
    old_key = str(getattr(window, "_architecture_review_card_target_key", ""))
    if new_key == old_key:
        return
    if _architecture_operation_open(window):
        _restore_edit_text(
            window,
            "_large_module_target_edit",
            str(getattr(window, "_architecture_review_card_target_text", "")),
        )
        _status(window, "AST target change blocked: Architecture operation is still reading the current card.")
        return
    if _transaction_open(window):
        _restore_edit_text(
            window,
            "_large_module_target_edit",
            str(getattr(window, "_architecture_review_card_target_text", "")),
        )
        _status(window, "AST target change blocked: current refactor transaction still owns the card.")
        return
    window._architecture_review_card_target_key = new_key
    window._architecture_review_card_target_text = new_text
    _cancel_planner_background_work(window)
    _clear_planner_results(window, clear_candidates=False)
    _clear_workbench_results(window)



def _clear_ast_state(window: object) -> None:
    window._large_module_targets = []
    window._large_module_target_index = -1
    window._large_module_target_source = "none"
    window._last_large_module_split_handoff = ""
    target_edit = getattr(window, "_large_module_target_edit", None)
    if target_edit is not None:
        target_edit.clear()
        target_edit.setPlaceholderText("Run Validate to load a project-owned large-module card")
    output = getattr(window, "_large_module_split_output", None)
    if output is not None:
        output.setPlainText("No large-module card loaded for the current Project Root.")
    sync = getattr(window, "_sync_large_module_target_controls", None)
    if callable(sync):
        sync()


def _clear_planner_results(window: object, *, clear_candidates: bool) -> None:
    selected_version = selected_planner_version(window)
    if clear_candidates:
        window._large_file_refactor_planner_candidates = []
        window._large_file_refactor_warning_targets = []
        window._large_file_refactor_warning_input_gate_open = False
    window._large_file_refactor_planner_selected_path = ""
    window._large_file_refactor_planner_state = "IDLE"
    window._large_file_refactor_docstring_proposals = []
    window._large_file_refactor_selected_version = selected_version
    window._large_file_refactor_web_ai_proposal_applied = False
    for attr_name in _PLANNER_RESULT_ATTRS:
        setattr(window, attr_name, None)
    target_edit = getattr(window, "_large_file_refactor_target_edit", None)
    if target_edit is not None:
        target_edit.clear()
    evidence = getattr(window, "_large_file_refactor_evidence_output", None)
    if evidence is not None:
        evidence.setPlainText("No card loaded. Select a project-owned large module and analyze it.")
    plan_output = getattr(window, "_large_file_refactor_plan_output", None)
    if plan_output is not None:
        plan_output.setPlainText("No split plan is owned by the Planner for the current card.")


def _clear_workbench_results(window: object) -> None:
    window._large_file_refactor_workbench_state = "IDLE"
    window._large_file_refactor_workbench_transaction_apply_executor_proven = False
    for attr_name in _WORKBENCH_RESULT_ATTRS:
        setattr(window, attr_name, None)
    for attr_name in _WORKBENCH_BUTTON_ATTRS:
        button = getattr(window, attr_name, None)
        if button is not None and hasattr(button, "setEnabled"):
            button.setEnabled(False)
    for attr_name in (
        "_large_file_refactor_workbench_semantic_review_check",
        "_large_file_refactor_workbench_warning_ack_check",
        "_large_file_refactor_workbench_transaction_confirm_check",
    ):
        checkbox = getattr(window, attr_name, None)
        if checkbox is not None:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)
    intake_output = getattr(window, "_large_file_refactor_workbench_intake_output", None)
    if intake_output is not None:
        intake_output.setPlainText("No Planner card loaded into Workbench.")
    completion_output = getattr(
        window,
        "_large_file_refactor_workbench_completion_status_output",
        None,
    )
    if completion_output is not None:
        completion_output.setPlainText("No completion transaction is loaded for the current card.")


def _remove_completed_ast_target(window: object, target_text: str) -> None:
    targets = list(getattr(window, "_large_module_targets", []) or [])
    root_text = _root_text(window)
    completed_key = _target_key(root_text, target_text)
    remaining = [
        item for item in targets
        if _target_key(root_text, str(getattr(item, "path", ""))) != completed_key
    ]
    window._large_module_targets = remaining
    window._large_module_target_index = 0 if remaining else -1
    window._last_large_module_split_handoff = ""
    edit = getattr(window, "_large_module_target_edit", None)
    if edit is not None:
        if remaining:
            edit.setText(str(getattr(remaining[0], "path", "")))
        else:
            edit.clear()
            edit.setPlaceholderText("Completed card ejected; select the next project module")
    sync = getattr(window, "_sync_large_module_target_controls", None)
    if callable(sync):
        sync()


def _architecture_operation_open(window: object) -> bool:
    """Return whether a top-level Architecture worker still owns the current card."""
    for attr_name in ("_worker_thread", "_ai_review_thread"):
        thread = getattr(window, attr_name, None)
        if thread is not None and hasattr(thread, "isRunning") and thread.isRunning():
            return True
    return False


def _transaction_open(window: object) -> bool:
    rollback = getattr(
        window,
        "_large_file_refactor_workbench_completion_rollback_result",
        None,
    )
    if str(getattr(rollback, "status", "")) == "rollback_verified":
        return False
    outcome = getattr(
        window,
        "_large_file_refactor_workbench_completion_apply_outcome",
        None,
    )
    final_state = str(getattr(outcome, "final_transaction_state", ""))
    if final_state.startswith("COMPLETED_") or final_state == "ROLLBACK_VERIFIED":
        return False
    completion = getattr(
        window,
        "_large_file_refactor_workbench_completion_transaction",
        None,
    )
    if completion is not None:
        return True
    apply_result = getattr(window, "_large_file_refactor_workbench_guarded_apply", None)
    legacy_rollback = getattr(window, "_large_file_refactor_workbench_rollback", None)
    applied = str(getattr(apply_result, "status", "")) == "applied"
    rolled_back = str(getattr(legacy_rollback, "status", "")) == "rollback_completed"
    return applied and not rolled_back


def _restore_edit_text(window: object, attr_name: str, text: str) -> None:
    edit = getattr(window, attr_name, None)
    if edit is None:
        return
    window._architecture_review_lifecycle_resetting = True
    try:
        edit.setText(text)
    finally:
        window._architecture_review_lifecycle_resetting = False


def _root_text(window: object) -> str:
    return _widget_text(getattr(window, "_root_path_edit", None)) or str(Path.cwd())


def _widget_text(widget: Any) -> str:
    return str(widget.text()).strip() if widget is not None and hasattr(widget, "text") else ""


def _path_key(path_text: str) -> str:
    text = str(path_text).strip()
    if not text:
        return ""
    try:
        return str(Path(text).resolve()).casefold()
    except OSError:
        return text.replace("\\", "/").rstrip("/").casefold()


def _target_key(root_text: str, target_text: str) -> str:
    target = str(target_text).strip()
    if not target:
        return ""
    try:
        path = Path(target)
        resolved = path.resolve() if path.is_absolute() else (Path(root_text).resolve() / path).resolve()
        return str(resolved).casefold()
    except OSError:
        return target.replace("\\", "/").rstrip("/").casefold()


def _status(window: object, message: str) -> None:
    status_bar_method = getattr(window, "statusBar", None)
    if callable(status_bar_method):
        bar = status_bar_method()
        if bar is not None:
            bar.showMessage(message)
