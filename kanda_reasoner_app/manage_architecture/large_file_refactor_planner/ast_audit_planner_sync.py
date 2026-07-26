# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ast_audit_planner_sync.py
"""Sync the AST Split Audit target into the Large File Refactor Planner."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from kanda_reasoner_app.manage_architecture.large_module_target_queue import (
    normalize_target_text,
)

from .analysis_formatting import format_analysis_report
from .ast_analysis import analyze_python_file
from .docstring_formatting import format_docstring_proposals
from .docstring_planner import build_docstring_proposals
from .gui_warning_input_gate import (
    refresh_warning_input_gate,
    sync_warning_input_selection,
)
from .models import PlannerSettings, PlannerState
from .split_formatting import format_split_plan
from .split_planner import build_split_plan

__all__ = ["PlannerAstTargetSyncResult", "sync_planner_from_ast_audit_target"]


@dataclass(frozen=True)
class PlannerAstTargetSyncResult:
    """Describe one AST-audit-to-planner synchronization attempt."""

    status: str
    requested_target: str
    selected_path: str
    candidate_index: int
    message: str


def sync_planner_from_ast_audit_target(window: object) -> PlannerAstTargetSyncResult:
    """Load the current AST audit target into Planner and populate read-only fields."""
    requested_target = _ast_target_text(window)
    refresh_warning_input_gate(window)
    if not requested_target:
        message = "AST Split Audit has no Target .py selected."
        _show_blocked_message(window, message)
        return PlannerAstTargetSyncResult(
            status="no_target",
            requested_target="",
            selected_path="",
            candidate_index=-1,
            message=message,
        )

    candidates = list(
        getattr(window, "_large_file_refactor_planner_candidates", []) or []
    )
    root_text = _root_text(window)
    normalized_target = normalize_target_text(root_text, requested_target)
    candidate_index = _match_candidate_index(
        candidates,
        normalized_target,
        requested_target,
    )
    if candidate_index < 0:
        message = (
            "Planner sync blocked. The AST Split Audit target is not in the current "
            "WARNING MODULE_TOO_LARGE candidate queue. Run Validate again or choose "
            "a current oversized warning target."
        )
        _clear_planner_selection(window, requested_target)
        _show_blocked_message(window, message)
        return PlannerAstTargetSyncResult(
            status="blocked_not_warning_candidate",
            requested_target=requested_target,
            selected_path="",
            candidate_index=-1,
            message=message,
        )

    table = getattr(window, "_large_file_refactor_candidate_table", None)
    if table is not None:
        table.selectRow(candidate_index)
    sync_warning_input_selection(window)

    selected_path = str(
        getattr(window, "_large_file_refactor_planner_selected_path", "") or ""
    )
    if not selected_path:
        message = "Planner sync blocked. Candidate selection did not resolve a source path."
        _show_blocked_message(window, message)
        return PlannerAstTargetSyncResult(
            status="blocked_selection",
            requested_target=requested_target,
            selected_path="",
            candidate_index=candidate_index,
            message=message,
        )

    try:
        report = analyze_python_file(selected_path)
        settings = _settings_from_window(window)
        plan = build_split_plan(report, settings, source_path=selected_path)
        proposals = build_docstring_proposals(report, plan)
    except (OSError, SyntaxError, ValueError) as exc:
        message = f"Planner sync blocked while analyzing target: {exc}"
        _show_blocked_message(window, message)
        return PlannerAstTargetSyncResult(
            status="blocked_analysis",
            requested_target=requested_target,
            selected_path=selected_path,
            candidate_index=candidate_index,
            message=message,
        )

    window._large_file_refactor_last_analysis = report
    window._large_file_refactor_last_plan = plan
    window._large_file_refactor_docstring_proposals = proposals
    window._large_file_refactor_evidence_output.setPlainText(
        format_analysis_report(report)
    )
    window._large_file_refactor_plan_output.setPlainText(
        format_split_plan(plan)
        + "\n\n"
        + format_docstring_proposals(proposals)
    )
    window._large_file_refactor_planner_state = (
        PlannerState.BLOCKED.value
        if getattr(plan, "status", "") == "blocked"
        else PlannerState.DOCSTRING_READY.value
    )
    message = (
        "Planner populated from the current Large Module AST Split Audit target. "
        "Analysis evidence, split plan, and docstring proposals are current for this file."
    )
    _show_status_message(window, message)
    return PlannerAstTargetSyncResult(
        status="populated",
        requested_target=requested_target,
        selected_path=selected_path,
        candidate_index=candidate_index,
        message=message,
    )


def _settings_from_window(window: object) -> PlannerSettings:
    """Build Planner settings from current controls without changing user choices."""
    return PlannerSettings(
        ideal_physical_lines=int(window._large_file_refactor_ideal_spin.value()),
        maximum_physical_lines=int(window._large_file_refactor_max_spin.value()),
        minimum_helper_physical_lines=int(
            window._large_file_refactor_min_helper_spin.value()
        ),
    )


def _match_candidate_index(
    candidates: Sequence[object],
    normalized_target: str,
    requested_target: str,
) -> int:
    """Return the candidate index matching one relative or absolute target path."""
    wanted = {
        _path_key(normalized_target),
        _path_key(requested_target),
    }
    for index, candidate in enumerate(candidates):
        keys = {
            _path_key(str(getattr(candidate, "relative_path", "") or "")),
            _path_key(str(getattr(candidate, "path", "") or "")),
        }
        if wanted.intersection(keys):
            return index
    return -1


def _path_key(path_text: str) -> str:
    """Return a case-insensitive slash-normalized path key."""
    return path_text.strip().replace("\\", "/").rstrip("/").casefold()


def _clear_target_specific_planner_state(window: object) -> None:
    """Clear downstream Planner state so one target cannot contaminate another."""
    for name in (
        "_large_file_refactor_last_analysis",
        "_large_file_refactor_last_plan",
        "_large_file_refactor_llm_result",
        "_large_file_refactor_preview_bundle",
        "_large_file_refactor_preview_write_result",
        "_large_file_refactor_import_migration_preview",
        "_large_file_refactor_preview_validation",
        "_large_file_refactor_patch_gate_result",
        "_large_file_refactor_project_patch_payload_result",
        "_large_file_refactor_payload_apply_gate_result",
    ):
        setattr(window, name, None)
    window._large_file_refactor_docstring_proposals = []


def _clear_planner_selection(window: object, requested_target: str) -> None:
    """Clear accepted Planner selection while showing the requested AST target."""
    window._large_file_refactor_planner_selected_path = ""
    window._large_file_refactor_planner_state = PlannerState.BLOCKED.value
    target_edit = getattr(window, "_large_file_refactor_target_edit", None)
    if target_edit is not None:
        target_edit.setText(requested_target)
    analyze_button = getattr(window, "_large_file_refactor_analyze_button", None)
    if analyze_button is not None:
        analyze_button.setEnabled(False)


def _show_blocked_message(window: object, message: str) -> None:
    """Show one fail-closed synchronization result in Planner panels."""
    window._large_file_refactor_planner_state = PlannerState.BLOCKED.value
    evidence = getattr(window, "_large_file_refactor_evidence_output", None)
    plan_output = getattr(window, "_large_file_refactor_plan_output", None)
    if evidence is not None:
        evidence.setPlainText(message)
    if plan_output is not None:
        plan_output.setPlainText(
            message
            + "\n\nNo split plan was generated and no preview/source write was performed."
        )
    _show_status_message(window, message)


def _show_status_message(window: object, message: str) -> None:
    """Show a short synchronization message when a status bar is available."""
    status_bar_method = getattr(window, "statusBar", None)
    if callable(status_bar_method):
        status_bar = status_bar_method()
        if status_bar is not None:
            status_bar.showMessage(message)


def _ast_target_text(window: object) -> str:
    """Return current AST Split Audit Target .py text."""
    edit = getattr(window, "_large_module_target_edit", None)
    return edit.text().strip() if edit is not None else ""


def _root_text(window: object) -> str:
    """Return the active project root text."""
    edit = getattr(window, "_root_path_edit", None)
    if edit is None:
        return str(Path.cwd())
    return edit.text().strip() or str(Path.cwd())
