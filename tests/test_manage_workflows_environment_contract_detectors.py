"""Focused tests for remaining Tab 2 workflow environment contract detectors."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    run_workflow_detectors,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors import (  # noqa: E501
    detect_workflow_environment_contract_issues,
)


def _context(command: object) -> WorkflowDetectorContext:
    return WorkflowDetectorContext(
        project_root=Path(".").resolve(),
        workflow_manifest={
            "workflows": {
                "business_checks": {
                    "enabled": True,
                    "commands": [command],
                }
            }
        },
        workflows_doc="",
    )


class WorkflowEnvironmentContractDetectorTests(unittest.TestCase):
    """Protect remaining Tab 2 help-file workflow error contracts."""

    def test_project_relative_utf8_command_is_allowed(self) -> None:
        context = _context(
            {
                "name": "safe_command",
                "args": ["{python}", "tool.py", "--validate"],
                "cwd": "{root}",
                "line_endings": "preserve",
                "dependencies": ["pytest>=8"],
            }
        )

        issues = detect_workflow_environment_contract_issues(context)

        self.assertEqual(issues, [])

    def test_bad_encoding_marker_is_error(self) -> None:
        context = _context(
            {
                "name": "bad_encoding",
                "command": "Set-Content -Path out.txt -Encoding Unicode",
            }
        )

        issues = detect_workflow_environment_contract_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_ENCODING_OR_LINE_ENDING_MISMATCH",
        )

    def test_bad_line_ending_value_is_error(self) -> None:
        context = _context(
            {
                "name": "bad_line_endings",
                "args": ["{python}", "tool.py"],
                "line_endings": "random",
            }
        )

        issues = detect_workflow_environment_contract_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_ENCODING_OR_LINE_ENDING_MISMATCH",
        )

    def test_explicit_empty_output_success_is_error(self) -> None:
        context = _context(
            {
                "name": "empty_success",
                "args": ["{python}", "tool.py"],
                "expected_outputs": ["report.txt"],
                "allow_empty_output": True,
            }
        )

        issues = detect_workflow_environment_contract_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_SILENT_EMPTY_OUTPUT_SUCCESS",
        )

    def test_non_empty_output_guard_false_is_error(self) -> None:
        context = _context(
            {
                "name": "empty_success",
                "args": ["{python}", "tool.py"],
                "expected_outputs": ["report.txt"],
                "require_non_empty_output": False,
            }
        )

        issues = detect_workflow_environment_contract_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_SILENT_EMPTY_OUTPUT_SUCCESS",
        )

    def test_unpinned_dependency_is_error(self) -> None:
        context = _context(
            {
                "name": "dependency_skew",
                "args": ["{python}", "tool.py"],
                "dependencies": ["pytest", "ruff>=0.1"],
            }
        )

        issues = detect_workflow_environment_contract_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_DEPENDENCY_VERSION_SKEW",
        )
        self.assertIn("pytest", issues[0].evidence)

    def test_path_root_drift_is_error(self) -> None:
        context = _context(
            {
                "name": "root_drift",
                "args": ["{python}", "tool.py"],
                "cwd": "E:\\developer_tools",
            }
        )

        issues = detect_workflow_environment_contract_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_PATH_ROOT_DRIFT")

    def test_default_registry_runs_detector(self) -> None:
        context = _context(
            {
                "name": "dependency_skew",
                "args": ["{python}", "tool.py"],
                "dependencies": ["pytest"],
            }
        )

        issues = run_workflow_detectors(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_DEPENDENCY_VERSION_SKEW", issue_ids)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
