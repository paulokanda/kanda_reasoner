"""Focused tests for workflow detector registry public contract."""

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
)


class WorkflowDetectorRegistryContractTests(unittest.TestCase):
    """Protect the registry contract used by Tab 2 detector tests and GUI flow."""

    def _context(self) -> WorkflowDetectorContext:
        return WorkflowDetectorContext(
            project_root=Path(".").resolve(),
            workflow_manifest={"workflows": {}},
            workflows_doc="",
        )

    def test_registry_exposes_run_method(self) -> None:
        registry = WorkflowDetectorRegistry()

        def detector(context: WorkflowDetectorContext) -> list[WorkflowIssue]:
            return []

        registry.register("clean", detector)

        self.assertEqual(registry.run(self._context()), [])

    def test_registry_run_returns_detector_issues(self) -> None:
        registry = WorkflowDetectorRegistry()

        def detector(context: WorkflowDetectorContext) -> list[WorkflowIssue]:
            return [
                WorkflowIssue(
                    issue_id="WORKFLOW_REGISTRY_SAMPLE",
                    category="workflow_detectors",
                    severity="error",
                    workflow_step="sample",
                    evidence="sample evidence",
                    expected="expected",
                    actual="actual",
                )
            ]

        registry.register("sample", detector)
        issues = registry.run(self._context())

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_REGISTRY_SAMPLE")

    def test_detector_value_error_becomes_typed_issue(self) -> None:
        registry = WorkflowDetectorRegistry()

        def detector(context: WorkflowDetectorContext) -> list[WorkflowIssue]:
            raise ValueError("broken detector")

        registry.register("broken", detector)
        issues = run_workflow_detectors(self._context(), registry=registry)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_DETECTOR_EXECUTION_ERROR")
        self.assertEqual(issues[0].severity, "error")
        self.assertIn("ValueError", issues[0].evidence)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
