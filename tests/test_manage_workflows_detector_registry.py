"""Focused tests for Tab 2 workflow detector infrastructure."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    WorkflowDetectorRegistry,
    run_workflow_detectors,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models import (  # noqa: E501
    WorkflowIssue,
    workflow_issue_to_check_result,
)


class WorkflowDetectorInfrastructureTests(unittest.TestCase):
    """Protect the public detector scaffold contract."""

    def test_issue_to_check_result_preserves_issue_payload(self) -> None:
        issue = WorkflowIssue(
            issue_id="WORKFLOW_TEST",
            category="workflow_test",
            severity="warning",
            evidence="evidence text",
        )

        result = workflow_issue_to_check_result(issue)

        self.assertEqual(result["category"], "workflow_detectors")
        self.assertEqual(result["name"], "WORKFLOW_TEST")
        self.assertEqual(result["status"], "warn")
        self.assertEqual(result["details"]["issue_id"], "WORKFLOW_TEST")

    def test_context_resolves_paths_from_project_root(self) -> None:
        context = WorkflowDetectorContext(project_root=Path("<PROJECT_ROOT>"))
        resolved = context.resolve_project_path("kanda_reasoner_app")

        self.assertTrue(str(resolved).endswith("kanda_reasoner_app"))

    def test_registry_runs_detector_and_returns_issue(self) -> None:
        registry = WorkflowDetectorRegistry()

        def detector(context: WorkflowDetectorContext) -> list[WorkflowIssue]:
            return [
                WorkflowIssue(
                    issue_id="WORKFLOW_SAMPLE",
                    category="workflow_sample",
                    severity="warn",
                    evidence=str(context.resolved_root()),
                )
            ]

        registry.register("sample", detector)
        issues = run_workflow_detectors(
            WorkflowDetectorContext(project_root=Path(".")),
            registry=registry,
        )

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_SAMPLE")

    def test_registry_returns_typed_issue_for_expected_detector_error(self) -> None:
        registry = WorkflowDetectorRegistry()

        def broken_detector(context: WorkflowDetectorContext) -> list[WorkflowIssue]:
            raise ValueError("detector failed")

        registry.register("broken", broken_detector)
        issues = registry.run(WorkflowDetectorContext(project_root=Path(".")))

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_DETECTOR_EXECUTION_ERROR")
        self.assertEqual(issues[0].severity, "error")
        self.assertIn("detector failed", issues[0].evidence)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
