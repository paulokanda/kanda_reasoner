"""Focused tests for Tab 2 workflow interface contract detectors."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    DEFAULT_WORKFLOW_DETECTOR_REGISTRY,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_interaction_contract_detectors import (  # noqa: E501
    detect_workflow_interaction_contract_issues,
)

interface_RELATIVE_PATH = "/".join(
    (
        "ask",
        "ai",
        "project",
        "reasoner",
        "manage_workflows",
        "manage_workflows_interface_help",
        "workflow_interface_window.py",
    )
)

GOOD_interface_SOURCE = """
class WorkflowManagerWindow:
    def _build_ui(self) -> None:
        run_action = QAction("> Run", self)
        run_action.triggered.connect(self.run_selected_mode)

        self._run_button = QPushButton("> Run Selected Mode")
        self._run_button.clicked.connect(self.run_selected_mode)

        for mode in ("validate", "diff", "scan", "write"):
            btn = QPushButton(mode.capitalize())
            btn.setToolTip(f"Run {mode} immediately")
            btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))

        help_btn = QPushButton("What do these modes do?")
        help_btn.clicked.connect(self.show_mode_help)

    def run_mode(self, mode: str) -> None:
        self._run_button.setEnabled(False)
        self.statusBar().showMessage(f"Running {mode}...")

    def _handle_worker_success(self, mode: str) -> None:
        self._run_button.setEnabled(True)
        self.statusBar().showMessage(f"OK Finished {mode}")
        self._output.appendPlainText(f"\n[finished] mode={mode} exit_code=0\n")
        QMessageBox.information(
            self, "Done", f"{mode.capitalize()} completed successfully."
        )

    def _handle_worker_error(self, mode: str, details: str) -> None:
        self._run_button.setEnabled(True)
        self.statusBar().showMessage(f"ERROR Finished {mode} with issues")
        self._output.appendPlainText(
            f"\n[finished] mode={mode} exit_code=1\n{details}\n"
        )
        QMessageBox.warning(
            self,
            "Finished with issues",
            f"{mode.capitalize()} finished with issues.\n"
            "Check the output panel for details.",
        )
"""


def _write_interface_source(root: Path, source: str) -> None:
    path = root / interface_RELATIVE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")


def _context(root: Path) -> WorkflowDetectorContext:
    return WorkflowDetectorContext(
        project_root=root,
        workflow_manifest={},
        workflows_doc="",
    )


class WorkflowInteractionContractDetectorTests(unittest.TestCase):
    """Protect Tab 2 interface button/action and state-label detector behavior."""

    def test_current_interface_contract_has_no_issues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_interface_source(root, GOOD_interface_SOURCE)

            issues = detect_workflow_interaction_contract_issues(_context(root))

        self.assertEqual(issues, [])

    def test_missing_interface_file_is_not_a_tab2_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            issues = detect_workflow_interaction_contract_issues(_context(Path(temp_dir)))

        self.assertEqual(issues, [])

    def test_run_selected_button_wrong_action_is_error(self) -> None:
        bad_source = GOOD_interface_SOURCE.replace(
            "self._run_button.clicked.connect(self.run_selected_mode)",
            'self._run_button.clicked.connect(lambda: self.run_mode("validate"))',
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_interface_source(root, bad_source)

            issues = detect_workflow_interaction_contract_issues(_context(root))

        self.assertIn(
            "WORKFLOW_INTERFACE_BUTTON_ACTION_MISMATCH",
            {issue.issue_id for issue in issues},
        )

    def test_mode_button_wrong_action_is_error(self) -> None:
        bad_source = GOOD_interface_SOURCE.replace(
            "btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))",
            "btn.clicked.connect(self.run_selected_mode)",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_interface_source(root, bad_source)

            issues = detect_workflow_interaction_contract_issues(_context(root))

        self.assertIn(
            "WORKFLOW_INTERFACE_BUTTON_ACTION_MISMATCH",
            {issue.issue_id for issue in issues},
        )

    def test_success_state_without_exit_code_is_error(self) -> None:
        bad_source = GOOD_interface_SOURCE.replace("exit_code=0", "status=ok")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_interface_source(root, bad_source)

            issues = detect_workflow_interaction_contract_issues(_context(root))

        self.assertIn(
            "WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
            {issue.issue_id for issue in issues},
        )

    def test_error_state_without_details_is_error(self) -> None:
        bad_source = GOOD_interface_SOURCE.replace("{details}", "details_hidden")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            _write_interface_source(root, bad_source)

            issues = detect_workflow_interaction_contract_issues(_context(root))

        self.assertIn(
            "WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
            {issue.issue_id for issue in issues},
        )

    def test_default_registry_includes_interface_contract_detector(self) -> None:
        names = [
            name
            for name, _detector in DEFAULT_WORKFLOW_DETECTOR_REGISTRY.items()
        ]

        self.assertIn("detect_workflow_interaction_contract_issues", names)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
