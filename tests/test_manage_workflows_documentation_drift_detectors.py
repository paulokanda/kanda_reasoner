"""Focused tests for workflow documentation drift detectors."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    run_workflow_detectors,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors import (  # noqa: E501
    detect_workflow_documentation_drift_issues,
)


def _context(manifest: dict, workflows_doc: str) -> WorkflowDetectorContext:
    return WorkflowDetectorContext(
        project_root=Path(".").resolve(),
        workflow_manifest=manifest,
        workflows_doc=workflows_doc,
    )


class WorkflowDocumentationDriftDetectorTests(unittest.TestCase):
    """Protect Tab 2 workflow documentation drift detection."""

    def test_empty_documentation_has_no_issue(self) -> None:
        manifest = {"workflows": {"business_checks": {"commands": []}}}
        context = _context(manifest, "")

        issues = detect_workflow_documentation_drift_issues(context)

        self.assertEqual(issues, [])

    def test_plain_documentation_has_no_issue(self) -> None:
        manifest = {"workflows": {"business_checks": {"commands": []}}}
        context = _context(
            manifest,
            "This document describes the current workflow without drift markers.",
        )

        issues = detect_workflow_documentation_drift_issues(context)

        self.assertEqual(issues, [])

    def test_manifest_hash_drift_is_error(self) -> None:
        manifest = {"workflows": {"business_checks": {"commands": []}}}
        bad_hash = "0" * 64
        context = _context(manifest, "workflow_manifest_sha256: " + bad_hash)

        issues = detect_workflow_documentation_drift_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_DOCUMENTATION_MANIFEST_HASH_DRIFT",
        )
        self.assertEqual(issues[0].severity, "error")

    def test_documented_missing_workflow_is_error(self) -> None:
        manifest = {"workflows": {"business_checks": {"commands": []}}}
        context = _context(manifest, "workflow: deprecated_validation")

        issues = detect_workflow_documentation_drift_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_DOCUMENTS_MISSING_WORKFLOW")

    def test_documented_existing_workflow_is_allowed(self) -> None:
        manifest = {"workflows": {"business_checks": {"commands": []}}}
        context = _context(manifest, "workflow: business_checks")

        issues = detect_workflow_documentation_drift_issues(context)

        self.assertEqual(issues, [])

    def test_documented_stale_expected_file_is_error(self) -> None:
        manifest = {
            "workflows": {
                "business_checks": {
                    "commands": [
                        {
                            "name": "validate",
                            "expected_outputs": ["reports/current.txt"],
                        }
                    ]
                }
            }
        }
        context = _context(manifest, "expected_output: reports/old.txt")

        issues = detect_workflow_documentation_drift_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_DOCUMENTS_STALE_EXPECTED_FILE",
        )

    def test_default_registry_runs_detector(self) -> None:
        manifest = {"workflows": {"business_checks": {"commands": []}}}
        context = _context(manifest, "workflow: deprecated_validation")

        issues = run_workflow_detectors(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_DOCUMENTS_MISSING_WORKFLOW", issue_ids)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
