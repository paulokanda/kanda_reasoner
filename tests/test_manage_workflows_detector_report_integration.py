"""Focused tests for workflow detector report integration."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli import (  # noqa: E501
    run_workflow_detector_results,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_generation import (  # noqa: E501
    generate_manifest,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_models import (  # noqa: E501
    CheckResult,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_project_scan import (  # noqa: E501
    scan_project,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    WorkflowDetectorRegistry,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models import (  # noqa: E501
    WorkflowIssue,
)


class WorkflowDetectorReportIntegrationTests(unittest.TestCase):
    """Protect integration between Tab 2 validation and detector reports."""

    def test_empty_registry_adds_no_results(self) -> None:
        root = Path(".").resolve()
        manifest = generate_manifest(root, scan_project(root))
        registry = WorkflowDetectorRegistry()

        results = run_workflow_detector_results(root, manifest, registry=registry)

        self.assertEqual(results, [])

    def test_detector_issue_becomes_check_result(self) -> None:
        root = Path(".").resolve()
        manifest = generate_manifest(root, scan_project(root))
        registry = WorkflowDetectorRegistry()

        def detector(context: WorkflowDetectorContext) -> list[WorkflowIssue]:
            return [
                WorkflowIssue(
                    issue_id="WORKFLOW_SAMPLE_WARNING",
                    category="sample_detector",
                    severity="warning",
                    workflow_step="sample_step",
                    evidence="sample evidence",
                    expected="expected value",
                    actual="actual value",
                )
            ]

        registry.register("sample", detector)
        results = run_workflow_detector_results(root, manifest, registry=registry)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], CheckResult)
        self.assertEqual(results[0].category, "workflow_detectors")
        self.assertEqual(results[0].name, "WORKFLOW_SAMPLE_WARNING")
        self.assertEqual(results[0].status, "warn")
        self.assertIn("issue_id", results[0].details)

    def test_detector_execution_error_becomes_failure_result(self) -> None:
        root = Path(".").resolve()
        manifest = generate_manifest(root, scan_project(root))
        registry = WorkflowDetectorRegistry()

        def detector(context: WorkflowDetectorContext) -> list[WorkflowIssue]:
            raise ValueError("detector failed")

        registry.register("broken", detector)
        results = run_workflow_detector_results(root, manifest, registry=registry)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, "fail")
        self.assertEqual(results[0].name, "WORKFLOW_DETECTOR_EXECUTION_ERROR")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
