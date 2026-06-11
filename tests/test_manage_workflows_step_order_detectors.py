"""Focused tests for workflow step order detectors."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_order_detectors import (  # noqa: E501
    detect_workflow_step_order_issues,
)


def _context(root: Path, commands: list[object]) -> WorkflowDetectorContext:
    manifest = {
        "workflows": {
            "business_checks": {
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


class WorkflowStepOrderDetectorTests(unittest.TestCase):
    """Protect canonical workflow step order detection."""

    def test_route_before_split_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_order_issues(
                _context(
                    root,
                    [
                        {"name": "generate route manifest"},
                        {"name": "split chunks"},
                    ],
                )
            )

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_ORDER_MISMATCH")
        self.assertEqual(issues[0].severity, "error")
        self.assertEqual(issues[0].details["stage"], "route_manifest")
        self.assertEqual(issues[0].details["required_predecessor"], "split_chunks")

    def test_upload_before_route_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_order_issues(
                _context(
                    root,
                    [
                        {"name": "web ai upload"},
                        {"name": "route manifest"},
                    ],
                )
            )

        ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_STEP_ORDER_MISMATCH", ids)
        self.assertTrue(any(issue.details["required_predecessor"] == "route_manifest" for issue in issues))

    def test_ordered_pipeline_is_quiet(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_order_issues(
                _context(
                    root,
                    [
                        {"name": "evidence collection"},
                        {"name": "complete json"},
                        {"name": "local ai refresh"},
                        {"name": "split chunks"},
                        {"name": "route manifest"},
                        {"name": "web ai upload"},
                        {"name": "ask ai"},
                    ],
                )
            )

        self.assertEqual(issues, [])

    def test_unrelated_steps_are_quiet(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            issues = detect_workflow_step_order_issues(
                _context(
                    root,
                    [
                        {"name": "architecture help smoke"},
                        {"name": "workflow help smoke"},
                        {"name": "gui import smoke"},
                    ],
                )
            )

        self.assertEqual(issues, [])

    def test_registry_loads_step_order_detector(self) -> None:
        from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
            DEFAULT_WORKFLOW_DETECTOR_REGISTRY,
        )

        names = {name for name, _detector in DEFAULT_WORKFLOW_DETECTOR_REGISTRY.items()}
        self.assertIn("detect_workflow_step_order_issues", names)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
