"""Focused tests for workflow rollback and fail-safe detectors."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    run_workflow_detectors,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors import (  # noqa: E501
    detect_workflow_rollback_fail_safe_issues,
)


def _context(workflows: dict) -> WorkflowDetectorContext:
    return WorkflowDetectorContext(
        project_root=Path(".").resolve(),
        workflow_manifest={"workflows": workflows},
        workflows_doc="",
    )


class WorkflowRollbackFailSafeDetectorTests(unittest.TestCase):
    """Protect Tab 2 rollback and fail-safe workflow detection."""

    def test_read_only_command_has_no_issue(self) -> None:
        context = _context({
            "business_checks": {
                "commands": [
                    {
                        "name": "validate",
                        "args": ["python", "tool.py", "--validate"],
                    }
                ],
            }
        })

        issues = detect_workflow_rollback_fail_safe_issues(context)

        self.assertEqual(issues, [])

    def test_mutating_command_without_rollback_is_error(self) -> None:
        context = _context({
            "business_checks": {
                "commands": [
                    {
                        "name": "unsafe_write",
                        "args": ["python", "tool.py", "--write"],
                    }
                ],
            }
        })

        issues = detect_workflow_rollback_fail_safe_issues(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_MUTATION_WITHOUT_ROLLBACK_FAIL_SAFE", issue_ids)
        self.assertIn("WORKFLOW_WRITE_WITHOUT_PREFLIGHT_VALIDATION", issue_ids)
        self.assertTrue(all(issue.severity == "error" for issue in issues))

    def test_mutating_command_with_rollback_and_preflight_is_allowed(self) -> None:
        context = _context({
            "business_checks": {
                "note": "rollback checkpoint is available before write",
                "commands": [
                    {
                        "name": "validate",
                        "args": ["python", "tool.py", "--validate"],
                    },
                    {
                        "name": "safe_write",
                        "args": ["python", "tool.py", "--write"],
                        "rollback_plan": "restore from backup checkpoint",
                    },
                ],
            }
        })

        issues = detect_workflow_rollback_fail_safe_issues(context)

        self.assertEqual(issues, [])

    def test_disabled_workflow_is_ignored(self) -> None:
        context = _context({
            "dangerous": {
                "enabled": False,
                "commands": [
                    {
                        "name": "disabled_write",
                        "args": ["python", "tool.py", "--write"],
                    }
                ],
            }
        })

        issues = detect_workflow_rollback_fail_safe_issues(context)

        self.assertEqual(issues, [])

    def test_destructive_shell_command_requires_fail_safe(self) -> None:
        context = _context({
            "cleanup": {
                "commands": [
                    {
                        "name": "remove_output",
                        "command": "Remove-Item -Recurse -Force output",
                    }
                ],
            }
        })

        issues = detect_workflow_rollback_fail_safe_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_MUTATION_WITHOUT_ROLLBACK_FAIL_SAFE",
        )

    def test_default_registry_runs_detector(self) -> None:
        context = _context({
            "business_checks": {
                "commands": [
                    {
                        "name": "unsafe_write",
                        "args": ["python", "tool.py", "--write"],
                    }
                ],
            }
        })

        issues = run_workflow_detectors(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_MUTATION_WITHOUT_ROLLBACK_FAIL_SAFE", issue_ids)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
