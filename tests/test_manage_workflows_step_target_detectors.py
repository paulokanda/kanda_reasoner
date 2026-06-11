"""Focused tests for workflow step target integrity detectors."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors import (  # noqa: E501
    detect_workflow_step_target_integrity,
)


def _context(root: Path, commands: list[object]) -> WorkflowDetectorContext:
    manifest = {
        "workflows": {
            "runtime_smoke": {
                "enabled": True,
                "commands": commands,
            }
        }
    }
    return WorkflowDetectorContext(
        project_root=root,
        workflow_manifest=manifest,
        workflows_doc="",
    )


class WorkflowStepTargetDetectorTests(unittest.TestCase):
    """Protect workflow command target integrity detector behavior."""

    def test_missing_project_file_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_target_integrity(
                _context(
                    root,
                    [
                        {
                            "name": "missing_script",
                            "args": [
                                "{python}",
                                "kanda_reasoner_app/tools/missing_script.py",
                            ],
                        }
                    ],
                )
            )

        ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_STEP_TARGET_MISSING_FILE", ids)
        self.assertTrue(all(issue.severity == "error" for issue in issues))

    def test_existing_project_file_is_quiet(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "kanda_reasoner_app" / "tools" / "script.py"
            target.parent.mkdir(parents=True)
            target.write_text("print('ok')\n", encoding="utf-8")
            issues = detect_workflow_step_target_integrity(
                _context(
                    root,
                    [
                        {
                            "name": "existing_script",
                            "args": ["{python}", "kanda_reasoner_app/tools/script.py"],
                        }
                    ],
                )
            )

        self.assertEqual(issues, [])

    def test_deprecated_project_file_is_error_even_if_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "old" / "validate_workflow.py"
            target.parent.mkdir(parents=True)
            target.write_text("print('old')\n", encoding="utf-8")
            issues = detect_workflow_step_target_integrity(
                _context(
                    root,
                    [
                        {
                            "name": "old_script",
                            "args": ["{python}", "old/validate_workflow.py"],
                        }
                    ],
                )
            )

        ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_STEP_TARGET_DEPRECATED_FILE", ids)

    def test_old_validation_logic_marker_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_target_integrity(
                _context(
                    root,
                    [
                        {
                            "name": "legacy_validator",
                            "command": "python tools/legacy_validation.py",
                        }
                    ],
                )
            )

        ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC", ids)

    def test_output_folder_naming_mismatch_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_target_integrity(
                _context(
                    root,
                    [
                        {
                            "name": "bad_output_folder",
                            "expected_output_folders": [
                                "project_analysis_evidence/json_split",
                            ],
                        }
                    ],
                )
            )

        ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_OUTPUT_FOLDER_NAMING_MISMATCH", ids)

    def test_canonical_output_folders_are_quiet(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_target_integrity(
                _context(
                    root,
                    [
                        {
                            "name": "canonical_output_folders",
                            "expected_output_folders": [
                                "project_analysis_evidence/json_complete",
                                "project_analysis_evidence/json_splitted",
                                "workbench/_bundle_temp",
                            ],
                        }
                    ],
                )
            )

        self.assertEqual(issues, [])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
