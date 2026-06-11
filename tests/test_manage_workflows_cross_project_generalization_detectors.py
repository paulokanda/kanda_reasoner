"""Focused tests for workflow cross-project generalization detectors."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors import (  # noqa: E501
    detect_workflow_cross_project_generalization_issues,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    run_workflow_detectors,
)


def _context(manifest: dict) -> WorkflowDetectorContext:
    return WorkflowDetectorContext(
        project_root=Path(".").resolve(),
        workflow_manifest=manifest,
        workflows_doc="",
    )


class WorkflowCrossProjectGeneralizationDetectorTests(unittest.TestCase):
    """Protect Tab 2 cross-project generalization detection."""

    def test_project_relative_command_has_no_issue(self) -> None:
        manifest = {
            "workflows": {
                "runtime_smoke": {
                    "commands": [
                        {
                            "name": "help",
                            "args": [
                                "{python}",
                                "kanda_reasoner_app/manage_workflows/manage_workflows.py",
                                "--help",
                            ],
                            "cwd": "{root}",
                        }
                    ]
                }
            }
        }

        issues = detect_workflow_cross_project_generalization_issues(
            _context(manifest)
        )

        self.assertEqual(issues, [])

    def test_root_placeholder_path_has_no_issue(self) -> None:
        manifest = {
            "workflows": {
                "business_checks": {
                    "commands": [
                        {
                            "name": "validate",
                            "args": [
                                "{python}",
                                "{root}\\kanda_reasoner_app\\manage_architecture\\manage_architecture.py",
                                "--validate",
                            ],
                            "cwd": "{root}",
                        }
                    ]
                }
            }
        }

        issues = detect_workflow_cross_project_generalization_issues(
            _context(manifest)
        )

        self.assertEqual(issues, [])

    def test_hardcoded_windows_python_path_is_error(self) -> None:
        manifest = {
            "workflows": {
                "imports": {
                    "commands": [
                        {
                            "name": "probe",
                            "args": [
                                "C:\\Users\\paulo\\miniconda3\\python.exe",
                                "-m",
                                "unittest",
                            ],
                        }
                    ]
                }
            }
        }

        issues = detect_workflow_cross_project_generalization_issues(
            _context(manifest)
        )

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_HARDCODED_LOCAL_PATH")
        self.assertEqual(issues[0].severity, "error")

    def test_hardcoded_project_root_path_is_error(self) -> None:
        manifest = {
            "workflows": {
                "business_checks": {
                    "commands": [
                        {
                            "name": "validate",
                            "args": [
                                "{python}",
                                "E:\\developer_tools\\kanda_reasoner_app\\manage_architecture\\manage_architecture.py",
                            ],
                        }
                    ]
                }
            }
        }

        issues = detect_workflow_cross_project_generalization_issues(
            _context(manifest)
        )

        self.assertEqual(len(issues), 1)
        self.assertIn("E:", issues[0].evidence)

    def test_hardcoded_cwd_is_error(self) -> None:
        manifest = {
            "workflows": {
                "runtime_smoke": {
                    "commands": [
                        {
                            "name": "help",
                            "args": ["{python}", "-m", "unittest"],
                            "cwd": "E:\\developer_tools",
                        }
                    ]
                }
            }
        }

        issues = detect_workflow_cross_project_generalization_issues(
            _context(manifest)
        )

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].category, "workflow_cross_project_generalization")

    def test_hardcoded_unix_path_is_error(self) -> None:
        manifest = {
            "workflows": {
                "runtime_smoke": {
                    "commands": [
                        {
                            "name": "help",
                            "args": ["/home/user/project/run.py"],
                        }
                    ]
                }
            }
        }

        issues = detect_workflow_cross_project_generalization_issues(
            _context(manifest)
        )

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_HARDCODED_LOCAL_PATH")

    def test_non_workflow_metadata_is_ignored(self) -> None:
        manifest = {
            "generated_by": "E:\\developer_tools\\old_tool.py",
            "workflows": {
                "runtime_smoke": {
                    "commands": [
                        {
                            "name": "help",
                            "args": ["{python}", "relative.py"],
                            "cwd": "{root}",
                        }
                    ]
                }
            },
        }

        issues = detect_workflow_cross_project_generalization_issues(
            _context(manifest)
        )

        self.assertEqual(issues, [])

    def test_default_registry_runs_detector(self) -> None:
        manifest = {
            "workflows": {
                "runtime_smoke": {
                    "commands": [
                        {
                            "name": "help",
                            "args": ["E:\\developer_tools\\run.py"],
                        }
                    ]
                }
            }
        }

        issues = run_workflow_detectors(_context(manifest))

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_HARDCODED_LOCAL_PATH", issue_ids)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
