"""Focused tests for validation-reference workflow detectors."""

from __future__ import annotations

import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors import (  # noqa: E501
    detect_validation_reference_misroutes,
)


def make_context(command: object) -> WorkflowDetectorContext:
    manifest = {
        "workflows": {
            "business_checks": {
                "enabled": True,
                "commands": [command],
            }
        }
    }
    return WorkflowDetectorContext(
        project_root=Path(".").resolve(),
        workflow_manifest=manifest,
        workflows_doc="",
    )


class ValidationReferenceDetectorTests(unittest.TestCase):
    """Protect detection of outdated validation references in Tab 2 workflows."""

    def test_current_architecture_command_is_allowed(self) -> None:
        context = make_context(
            {
                "name": "architecture_validation_smoke",
                "args": [
                    "{python}",
                    "kanda_reasoner_app/manage_architecture/manage_architecture.py",
                    "--root",
                    "{root}",
                    "--validate",
                ],
            }
        )

        issues = detect_validation_reference_misroutes(context)

        self.assertEqual(issues, [])

    def test_current_bundle_temp_manifest_path_is_allowed(self) -> None:
        context = make_context(
            {
                "name": "bundle_manifest_check",
                "command": (
                    "python check.py "
                    "workbench/_bundle_temp/BUNDLE_MANIFEST_w017_validation_reference.txt"
                ),
            }
        )

        issues = detect_validation_reference_misroutes(context)

        self.assertEqual(issues, [])

    def test_canonical_active_governance_path_is_allowed(self) -> None:
        context = make_context(
            {
                "name": "canon_check",
                "command": (
                    "python check.py "
                    "_project_reference/ACTIVE_PROJECT_ GOVERNANCE/REASONER_PROJECT_CANON.md"
                ),
            }
        )

        issues = detect_validation_reference_misroutes(context)

        self.assertEqual(issues, [])

    def test_tools_architecture_reference_is_error(self) -> None:
        context = make_context(
            {
                "name": "outdated_architecture",
                "command": "python tools/architecture/manage_architecture.py --validate",
            }
        )

        issues = detect_validation_reference_misroutes(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC",
        )
        self.assertEqual(issues[0].severity, "error")
        self.assertIn("tools/architecture", issues[0].evidence)

    def test_old_bundle_manifest_reference_is_error(self) -> None:
        context = make_context(
            {
                "name": "outdated_bundle_manifest",
                "command": (
                    "python check.py "
                    "_project_reference/BUNDLE_MANIFEST/BUNDLE_MANIFEST_old.txt"
                ),
            }
        )

        issues = detect_validation_reference_misroutes(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC",
        )
        self.assertIn("_project_reference/bundle_manifest", issues[0].evidence)

    def test_old_active_governance_spelling_is_error(self) -> None:
        context = make_context(
            {
                "name": "outdated_governance",
                "args": [
                    "{python}",
                    "check.py",
                    "_project_reference/ACTIVE_PROJECT_GOVERNANCE/REASONER_PROJECT_CANON.md",
                ],
            }
        )

        issues = detect_validation_reference_misroutes(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC",
        )
        self.assertIn("active_project_governance", issues[0].evidence)

    def test_deprecated_project_copy_reference_is_error(self) -> None:
        context = make_context(
            {
                "name": "deprecated_copy",
                "command": "python developer_tools_older/manage_workflows.py --validate",
            }
        )

        issues = detect_validation_reference_misroutes(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC",
        )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
