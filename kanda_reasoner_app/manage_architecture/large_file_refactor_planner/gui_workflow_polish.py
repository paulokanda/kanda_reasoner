# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/gui_workflow_polish.py
"""End-to-end GUI workflow polish for the large-file refactor planner."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .models import FEATURE_ID, PlannerState

__all__ = [
    "GUI_COMPLETION_REVIEW_TOKEN",
    "EndToEndWorkflowSnapshot",
    "attach_large_file_refactor_workflow_polish",
    "build_end_to_end_workflow_snapshot",
    "copy_end_to_end_workflow_report",
    "format_end_to_end_workflow_report",
    "show_end_to_end_workflow_report",
]

GUI_COMPLETION_REVIEW_TOKEN = "CONFIRM_REVIEW_LARGE_FILE_REFACTOR_E2E_WORKFLOW"


@dataclass(frozen=True)
class EndToEndWorkflowSnapshot:
    """Review-only status snapshot for the complete guarded refactor workflow."""

    feature_id: str
    active_project_root: str
    selected_target: str
    planner_state: str
    analysis_status: str
    split_plan_status: str
    docstring_status: str
    llm_status: str
    preview_status: str
    preview_validation_status: str
    project_payload_status: str
    payload_apply_gate_status: str
    guarded_apply_status: str
    post_apply_validation_status: str
    rollback_recovery_status: str
    multifile_recovery_status: str
    exact_review_token: str
    writes_enabled_by_this_gui_polish: bool = False
    loose_preview_artifacts_used_as_source_of_truth: bool = False
    project_reference_excluded: bool = True
    import_rewrite_application_enabled: bool = False
    non_target_removal_enabled: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blocked_until_review_steps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready workflow snapshot."""
        return asdict(self)


def attach_large_file_refactor_workflow_polish(window: object, layout: object) -> None:
    """Attach final review-only workflow buttons to the existing GUI layout."""
    from PySide6.QtWidgets import QHBoxLayout, QPushButton

    row = QHBoxLayout()
    show_btn = QPushButton("Show E2E Workflow")
    show_btn.setToolTip("Review-only workflow summary. Does not apply, rollback, or remove files.")
    show_btn.clicked.connect(lambda: show_end_to_end_workflow_report(window))
    row.addWidget(show_btn)
    copy_btn = QPushButton("Copy E2E Gate Summary")
    copy_btn.setToolTip("Copy the complete guarded workflow summary and safety gates.")
    copy_btn.clicked.connect(lambda: copy_end_to_end_workflow_report(window))
    row.addWidget(copy_btn)
    row.addStretch(1)
    layout.addLayout(row)
    window._large_file_refactor_e2e_workflow_button = show_btn
    window._large_file_refactor_copy_e2e_gate_summary_button = copy_btn


def show_end_to_end_workflow_report(window: object) -> None:
    """Render the end-to-end review report into the planner output panel."""
    output = getattr(window, "_large_file_refactor_plan_output", None)
    report = format_end_to_end_workflow_report(build_end_to_end_workflow_snapshot(window))
    if output is not None:
        output.setPlainText(report)


def copy_end_to_end_workflow_report(window: object) -> str:
    """Copy the end-to-end review report and return it for tests."""
    from PySide6.QtWidgets import QApplication

    report = format_end_to_end_workflow_report(build_end_to_end_workflow_snapshot(window))
    QApplication.clipboard().setText(report)
    return report


def build_end_to_end_workflow_snapshot(window: object) -> EndToEndWorkflowSnapshot:
    """Build a read-only snapshot of all known large-file workflow gates."""
    state = getattr(window, "_large_file_refactor_planner_state", PlannerState.IDLE.value)
    selected = getattr(window, "_large_file_refactor_planner_selected_path", "")
    root = _root_text(window)
    return EndToEndWorkflowSnapshot(
        feature_id=FEATURE_ID,
        active_project_root=root,
        selected_target=selected or "<none>",
        planner_state=str(state),
        analysis_status=_status_from_attr(window, "_large_file_refactor_last_analysis", ready="ready"),
        split_plan_status=_status_from_attr(window, "_large_file_refactor_last_plan", ready="ready"),
        docstring_status=_list_status(window, "_large_file_refactor_docstring_proposals"),
        llm_status=_object_status(window, "_large_file_refactor_llm_result"),
        preview_status=_object_status(window, "_large_file_refactor_preview_bundle"),
        preview_validation_status=_object_status(window, "_large_file_refactor_preview_validation"),
        project_payload_status=_object_status(window, "_large_file_refactor_project_patch_payload_result"),
        payload_apply_gate_status=_object_status(window, "_large_file_refactor_payload_apply_gate_result"),
        guarded_apply_status=_object_status(window, "_large_file_refactor_guarded_source_apply_execution_result"),
        post_apply_validation_status=_object_status(window, "_large_file_refactor_post_apply_validation_result"),
        rollback_recovery_status=_object_status(window, "_large_file_refactor_rollback_recovery_result"),
        multifile_recovery_status=_object_status(window, "_large_file_refactor_multifile_recovery_evidence_result"),
        exact_review_token=GUI_COMPLETION_REVIEW_TOKEN,
        writes_enabled_by_this_gui_polish=False,
        loose_preview_artifacts_used_as_source_of_truth=False,
        project_reference_excluded=True,
        import_rewrite_application_enabled=False,
        non_target_removal_enabled=False,
        checked_rules=_checked_rules(),
        blocked_until_review_steps=_blocked_steps(window),
    )


def format_end_to_end_workflow_report(snapshot: EndToEndWorkflowSnapshot) -> str:
    """Return a stable, review-only end-to-end workflow report."""
    lines = [
        "LARGE FILE REFACTOR PLANNER - END-TO-END WORKFLOW",
        "Feature: " + snapshot.feature_id,
        "Active project root: " + snapshot.active_project_root,
        "Selected target: " + snapshot.selected_target,
        "Planner state: " + snapshot.planner_state,
        "",
        "Workflow status:",
        "- Analysis: " + snapshot.analysis_status,
        "- Split plan: " + snapshot.split_plan_status,
        "- Docstrings: " + snapshot.docstring_status,
        "- Local LLM arbitration: " + snapshot.llm_status,
        "- Governed preview: " + snapshot.preview_status,
        "- Preview validation: " + snapshot.preview_validation_status,
        "- Project patch payload: " + snapshot.project_payload_status,
        "- Payload apply gate: " + snapshot.payload_apply_gate_status,
        "- Guarded source apply: " + snapshot.guarded_apply_status,
        "- Post-apply validation: " + snapshot.post_apply_validation_status,
        "- Rollback/recovery: " + snapshot.rollback_recovery_status,
        "- Multi-file recovery evidence: " + snapshot.multifile_recovery_status,
        "",
        "Safety gates:",
        "- GUI polish writes source: " + str(snapshot.writes_enabled_by_this_gui_polish),
        "- Loose preview artifacts as source of truth: " + str(snapshot.loose_preview_artifacts_used_as_source_of_truth),
        "- .project_reference excluded: " + str(snapshot.project_reference_excluded),
        "- Import rewrite application enabled: " + str(snapshot.import_rewrite_application_enabled),
        "- Non-target removal enabled: " + str(snapshot.non_target_removal_enabled),
        "- Review token: " + snapshot.exact_review_token,
    ]
    if snapshot.blocked_until_review_steps:
        lines.extend(["", "Blocked until review:"])
        lines.extend("- " + item for item in snapshot.blocked_until_review_steps)
    lines.extend(["", "Checked rules:"])
    lines.extend("- " + item for item in snapshot.checked_rules)
    return "\n".join(lines)


def _blocked_steps(window: object) -> list[str]:
    """Return missing steps needed before the full guarded workflow is complete."""
    steps: list[str] = []
    missing = {
        "_large_file_refactor_last_analysis": "Run Analyze File.",
        "_large_file_refactor_last_plan": "Generate Split Plan.",
        "_large_file_refactor_preview_bundle": "Generate governed preview.",
        "_large_file_refactor_preview_validation": "Validate governed preview artifacts.",
        "_large_file_refactor_project_patch_payload_result": "Create governed project patch payload ZIP.",
        "_large_file_refactor_payload_apply_gate_result": "Prepare payload apply gate evidence.",
    }
    for attr_name, message in missing.items():
        if getattr(window, attr_name, None) is None:
            steps.append(message)
    return steps


def _checked_rules() -> list[str]:
    """Return stable final-GUI safety rules."""
    return [
        "box_logic_active",
        "kanda_reasoner_tool_logic_separate_from_project_payload_ownership",
        "no_leak_logic_v1_active",
        "project_reference_roots_excluded",
        "daily_work_preview_root_required_for_artifacts",
        "loose_preview_artifacts_not_source_of_truth",
        "guarded_executor_owns_source_mutation_decision",
        "post_apply_validation_required_after_apply",
        "rollback_uses_verified_source_derived_backup_snapshot",
        "multi_file_recovery_does_not_remove_non_target_files",
        "module_size_gate_500_physical_lines",
    ]


def _root_text(window: object) -> str:
    """Return active project root text without importing GUI shell internals."""
    edit = getattr(window, "_root_path_edit", None)
    if edit is None:
        return "."
    text = edit.text().strip()
    return text or "."


def _object_status(window: object, attr_name: str) -> str:
    """Return status attribute text for a stored result object."""
    value = getattr(window, attr_name, None)
    if value is None:
        return "not run"
    return str(getattr(value, "status", "ready"))


def _status_from_attr(window: object, attr_name: str, *, ready: str) -> str:
    """Return ready/not-run for an arbitrary stored object."""
    return ready if getattr(window, attr_name, None) is not None else "not run"


def _list_status(window: object, attr_name: str) -> str:
    """Return a count-based status for a stored list."""
    value = getattr(window, attr_name, None)
    if not value:
        return "not generated"
    return str(len(value)) + " proposal(s)"
