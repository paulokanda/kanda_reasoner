"""Tests for workflow evidence output route guard detector."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    DEFAULT_WORKFLOW_DETECTOR_REGISTRY,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_evidence_output_route_guard_detectors import (  # noqa: E501
    detect_evidence_output_route_guard_issues,
)


class WorkflowEvidenceOutputRouteGuardDetectorTests(unittest.TestCase):
    """Protect workflow validation coverage for evidence output routing."""

    def _context(self, root: Path) -> WorkflowDetectorContext:
        return WorkflowDetectorContext(
            project_root=root,
            workflow_manifest={"workflows": {}},
            workflows_doc="",
        )

    def test_clean_external_route_returns_no_issues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()

            issues = detect_evidence_output_route_guard_issues(self._context(root))

        self.assertEqual(issues, [])

    def test_in_source_evidence_folder_returns_blocking_issue(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            (root / "project_analysis_evidence").mkdir(parents=True)

            issues = detect_evidence_output_route_guard_issues(self._context(root))

        self.assertTrue(issues)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_EVIDENCE_OUTPUT_ROUTE_GUARD_BLOCKED",
        )
        self.assertEqual(issues[0].severity, "error")
        self.assertEqual(issues[0].owning_box, "storage_policy")
        self.assertIn("project_analysis_evidence", issues[0].file_path)

    def test_detector_is_registered_for_workflow_validation(self) -> None:
        registered_names = [
            name for name, _detector in DEFAULT_WORKFLOW_DETECTOR_REGISTRY.items()
        ]

        self.assertIn(
            "detect_evidence_output_route_guard_issues",
            registered_names,
        )

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source_path = Path(
            "kanda_reasoner_app/manage_workflows/manage_workflows_help/"
            "workflow_evidence_output_route_guard_detectors.py"
        )
        source = source_path.read_text(encoding="utf-8")

        self.assertNotIn("E:\\\\", source)
        self.assertNotIn("E:/", source)
        self.assertNotIn("developer_tools", source)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
