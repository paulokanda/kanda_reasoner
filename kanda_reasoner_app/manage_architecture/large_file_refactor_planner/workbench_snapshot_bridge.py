# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_snapshot_bridge.py
"""Explicit Planner-to-Workbench bridge and snapshot state ownership."""

from __future__ import annotations

import json
from typing import Any

from .planner_workbench_handoff import export_latest_planner_workbench_handoff
from .workbench_aqr_snapshot_lifecycle import retire_aqr_for_snapshot_replacement
from .workbench_plan_intake import (
    WorkbenchPlanIntakeResult,
    build_workbench_plan_intake,
    recheck_workbench_source_hash,
)
from .workbench_plan_snapshot import (
    build_workbench_plan_snapshot,
)

__all__ = [
    "load_latest_snapshot_into_workbench",
    "materialize_workbench_owned_plan",
    "recheck_owned_snapshot_intake",
    "workbench_source_transaction_open",
]


_DOWNSTREAM_ATTRS = (
    "_large_file_refactor_workbench_dependency_readiness",
    "_large_file_refactor_workbench_real_preview",
    "_large_file_refactor_workbench_structural_validation",
    "_large_file_refactor_workbench_advanced_quality_review",
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

_OUTPUT_MESSAGES = {
    "_large_file_refactor_workbench_dependency_output":
        "Snapshot changed. Run Dependency Readiness for the owned snapshot.",
    "_large_file_refactor_workbench_real_preview_output":
        "Snapshot changed. Generate a new real preview after readiness.",
    "_large_file_refactor_workbench_validation_output":
        "Snapshot changed. Validate the new real preview before continuing.",
    "_large_file_refactor_workbench_aqr_output":
        "Snapshot changed. Run a fresh Advanced Quality Review after Structural Validation passes.",
    "_large_file_refactor_workbench_preflight_output":
        "Snapshot changed. Prepare new preflight backup readiness evidence.",
    "_large_file_refactor_workbench_source_payload_output":
        "Snapshot changed. Build a new source apply payload.",
    "_large_file_refactor_workbench_apply_output":
        "Snapshot changed. No guarded apply result exists for this snapshot.",
    "_large_file_refactor_workbench_rollback_output":
        "Snapshot changed. No rollback result exists for this snapshot.",
}


def load_latest_snapshot_into_workbench(
    window: object,
    active_project_root: str,
) -> tuple[WorkbenchPlanIntakeResult | None, str]:
    """Capture once through public Planner export and assume Workbench ownership."""

    if workbench_source_transaction_open(window):
        return None, (
            "Load blocked: a source apply transaction is still open. "
            "Complete rollback or preserve the current Workbench transaction."
        )

    try:
        handoff = export_latest_planner_workbench_handoff(window)
        snapshot = build_workbench_plan_snapshot(handoff)
        result = build_workbench_plan_intake(
            snapshot=snapshot,
            active_project_root=active_project_root,
        )
    except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result = build_workbench_plan_intake(
            snapshot=None,
            active_project_root=active_project_root,
        )
        return result, "Planner handoff blocked without changing Workbench state: " + str(exc)

    if not result.workbench_snapshot_owned:
        blocker_text = ", ".join(result.blockers) or "UNKNOWN_INTAKE_BLOCKER"
        return result, (
            "Planner handoff rejected without changing Workbench state. Blockers: "
            + blocker_text
        )
    _reset_downstream_results(window)
    window._large_file_refactor_workbench_plan_snapshot = snapshot
    return result, ""


def recheck_owned_snapshot_intake(
    window: object,
) -> WorkbenchPlanIntakeResult | None:
    """Recheck source freshness without reading Planner state."""

    intake = getattr(window, "_large_file_refactor_workbench_intake", None)
    if intake is None:
        return None
    result = recheck_workbench_source_hash(intake)
    if not result.ready_for_real_preview:
        _reset_downstream_results(window)
    return result


def materialize_workbench_owned_plan(window: object) -> Any:
    """Return fresh typed plan from Workbench snapshot only."""

    snapshot = getattr(
        window,
        "_large_file_refactor_workbench_plan_snapshot",
        None,
    )
    if snapshot is None:
        return None
    try:
        return snapshot.materialize_plan()
    except (TypeError, ValueError, KeyError):
        return None


def workbench_source_transaction_open(window: object) -> bool:
    """Block snapshot replacement while any mutation transaction owns the card."""

    completion_rollback = getattr(
        window,
        "_large_file_refactor_workbench_completion_rollback_result",
        None,
    )
    if getattr(completion_rollback, "status", "") == "rollback_verified":
        return False
    outcome = getattr(
        window,
        "_large_file_refactor_workbench_completion_apply_outcome",
        None,
    )
    final_state = str(getattr(outcome, "final_transaction_state", ""))
    if final_state.startswith("COMPLETED_") or final_state == "ROLLBACK_VERIFIED":
        return False
    completion_transaction = getattr(
        window,
        "_large_file_refactor_workbench_completion_transaction",
        None,
    )
    if completion_transaction is not None:
        return True

    apply_result = getattr(
        window,
        "_large_file_refactor_workbench_guarded_apply",
        None,
    )
    rollback_result = getattr(
        window,
        "_large_file_refactor_workbench_rollback",
        None,
    )
    applied = bool(
        apply_result and getattr(apply_result, "status", "") == "applied"
    )
    rolled_back = bool(
        rollback_result
        and getattr(rollback_result, "status", "") == "rollback_completed"
    )
    return applied and not rolled_back


def _reset_downstream_results(window: object) -> None:
    """Invalidate all Workbench outputs owned by a previous snapshot."""

    retire_aqr_for_snapshot_replacement(window)

    for attr_name in _DOWNSTREAM_ATTRS:
        setattr(window, attr_name, None)
    for attr_name, message in _OUTPUT_MESSAGES.items():
        widget = getattr(window, attr_name, None)
        if widget is not None:
            widget.setPlainText(message)
    window._large_file_refactor_workbench_aqr_identity_hash = ""
    window._large_file_refactor_workbench_aqr_context = None
    window._large_file_refactor_workbench_aqr_stage_states = {}
    window._large_file_refactor_workbench_aqr_terminal_status = ""
    window._large_file_refactor_workbench_aqr_terminal_diagnostic = ""
    for attr_name in (
        "_large_file_refactor_workbench_apply_token_edit",
        "_large_file_refactor_workbench_rollback_token_edit",
    ):
        edit = getattr(window, attr_name, None)
        if edit is not None:
            edit.clear()
    window._large_file_refactor_workbench_transaction_apply_executor_proven = False
    for attr_name in (
        "_large_file_refactor_workbench_semantic_review_check",
        "_large_file_refactor_workbench_warning_ack_check",
        "_large_file_refactor_workbench_transaction_confirm_check",
    ):
        checkbox = getattr(window, attr_name, None)
        if checkbox is not None:
            checkbox.setChecked(False)
            checkbox.setEnabled(False)
    for attr_name in (
        "_large_file_refactor_workbench_transaction_prepare_button",
        "_large_file_refactor_workbench_refactor_large_module_button",
        "_large_file_refactor_workbench_transaction_rollback_button",
    ):
        button = getattr(window, attr_name, None)
        if button is not None:
            button.setEnabled(False)
