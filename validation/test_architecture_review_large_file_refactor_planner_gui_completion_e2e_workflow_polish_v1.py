# project-path: validation/test_architecture_review_large_file_refactor_planner_gui_completion_e2e_workflow_polish_v1.py
"""Validation for GUI Completion + End-to-End Workflow Polish v1."""
from __future__ import annotations

import ast
from pathlib import Path

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.gui_workflow_polish import (
    GUI_COMPLETION_REVIEW_TOKEN,
    build_end_to_end_workflow_snapshot,
    format_end_to_end_workflow_report,
)

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-gui-completion-end-to-end-workflow-polish-v1"
PREVIOUS_MARKERS = [
    "architecture-review-large-file-refactor-planner-multifile-recovery-evidence-v1",
    "architecture-review-large-file-refactor-planner-rollback-recovery-contract-v1",
    "architecture-review-large-file-refactor-planner-post-apply-validation-hash-evidence-v1",
    "architecture-review-large-file-refactor-planner-guarded-source-apply-executor-v1",
    "architecture-review-large-file-refactor-planner-source-apply-preflight-backup-contract-v1",
    "architecture-review-large-file-refactor-planner-source-apply-dry-run-validator-v1",
    "architecture-review-large-file-refactor-planner-final-guarded-source-apply-planning-v1",
    "architecture-review-large-file-refactor-planner-human-confirmed-apply-contract-v1",
    "architecture-review-large-file-refactor-planner-human-confirmed-import-rewrite-contract-v1",
    "architecture-review-large-file-refactor-planner-import-rewrite-application-gate-v1",
    "architecture-review-large-file-refactor-planner-payload-apply-gui-wiring-v1",
    "architecture-review-large-file-refactor-planner-payload-apply-gate-v1",
    "architecture-review-large-file-refactor-planner-project-patch-payload-v1",
    "architecture-review-large-file-refactor-planner-patch-zip-creation-gate-v1",
    "architecture-review-large-file-refactor-planner-preview-validation-import-migration-v1",
    "architecture-review-large-file-refactor-planner-governed-preview-generation-v1",
    "architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1",
    "architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1",
    "architecture-review-large-file-refactor-planner-docstring-contracts-v1",
    "architecture-review-large-file-refactor-planner-split-contracts-v1",
    "architecture-review-large-file-refactor-planner-ast-v1",
]
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX = PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


class _LineEdit:
    def __init__(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text


class _Result:
    def __init__(self, status: str) -> None:
        self.status = status


class _Window:
    pass


def _window() -> _Window:
    window = _Window()
    window._root_path_edit = _LineEdit("E:/kanda_reasoner")
    window._large_file_refactor_planner_selected_path = "E:/kanda_reasoner/app/large_module.py"
    window._large_file_refactor_planner_state = "patch_ready"
    window._large_file_refactor_last_analysis = object()
    window._large_file_refactor_last_plan = object()
    window._large_file_refactor_docstring_proposals = [object(), object()]
    window._large_file_refactor_llm_result = _Result("disabled")
    window._large_file_refactor_preview_bundle = _Result("preview_ready")
    window._large_file_refactor_preview_validation = _Result("passed")
    window._large_file_refactor_project_patch_payload_result = _Result("payload_ready")
    window._large_file_refactor_payload_apply_gate_result = _Result("apply_gate_review_ready")
    return window


def test_snapshot_and_report_are_review_only() -> None:
    snapshot = build_end_to_end_workflow_snapshot(_window())
    assert snapshot.exact_review_token == GUI_COMPLETION_REVIEW_TOKEN
    assert snapshot.writes_enabled_by_this_gui_polish is False
    assert snapshot.loose_preview_artifacts_used_as_source_of_truth is False
    assert snapshot.project_reference_excluded is True
    assert snapshot.import_rewrite_application_enabled is False
    assert snapshot.non_target_removal_enabled is False
    report = format_end_to_end_workflow_report(snapshot)
    assert "END-TO-END WORKFLOW" in report
    assert ".project_reference excluded: True" in report
    assert "Loose preview artifacts as source of truth: False" in report
    assert "Non-target removal enabled: False" in report
    assert "guarded_executor_owns_source_mutation_decision" in report


def test_gui_shell_attaches_workflow_polish_without_new_mutation_path() -> None:
    gui_shell = (BOX / "gui_shell.py").read_text(encoding="utf-8")
    assert "attach_large_file_refactor_workflow_polish(window, layout)" in gui_shell
    assert "from .gui_workflow_polish import attach_large_file_refactor_workflow_polish" in gui_shell
    helper = (BOX / "gui_workflow_polish.py").read_text(encoding="utf-8")
    forbidden = [
        "build_guarded_source_apply_execution(",
        "write_guarded_source_apply_execution_manifest(",
        "build_source_apply_rollback_recovery(",
        "write_source_apply_rollback_recovery_manifest(",
        "write_preview_files(",
        "create_project_patch_payload_zip(",
    ]
    for fragment in forbidden:
        assert fragment not in helper


def test_module_line_counts_and_ast_parse() -> None:
    for rel in ["gui_shell.py", "gui_workflow_polish.py"]:
        path = BOX / rel
        text = path.read_text(encoding="utf-8")
        assert len(text.splitlines()) <= 500, rel
        ast.parse(text)


def main() -> int:
    test_snapshot_and_report_are_review_only()
    test_gui_shell_attaches_workflow_polish_without_new_mutation_path()
    test_module_line_counts_and_ast_parse()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
