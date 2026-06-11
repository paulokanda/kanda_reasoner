"""Focused tests for Tab 2 workflow structure detectors."""

from __future__ import annotations

import copy
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    DEFAULT_WORKFLOW_DETECTOR_REGISTRY,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_structure_detectors import (  # noqa: E501
    detect_required_validation_commands,
    detect_stale_workflow_metadata,
    detect_workflow_step_order,
)


def _base_manifest() -> dict[str, object]:
    """Return a minimal clean workflow manifest."""
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "managed_by": "manage_workflows.py",
        "version": 1,
        "workflows": {
            "runtime_smoke": {
                "enabled": True,
                "commands": [
                    {
                        "name": "architecture_help_smoke",
                        "args": [
                            "{python}",
                            "kanda_reasoner_app/manage_architecture/manage_architecture.py",
                            "--help",
                        ],
                    },
                    {
                        "name": "workflow_help_smoke",
                        "args": [
                            "{python}",
                            "kanda_reasoner_app/manage_workflows/manage_workflows.py",
                            "--help",
                        ],
                    },
                ],
            },
            "business_checks": {
                "enabled": True,
                "commands": [
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
                ],
            },
        },
    }


def _context(manifest: dict[str, object]) -> WorkflowDetectorContext:
    """Build a detector context."""
    return WorkflowDetectorContext(
        project_root=Path(".").resolve(),
        workflow_manifest=manifest,
        workflows_doc="",
    )


class WorkflowStructureDetectorTests(unittest.TestCase):
    """Protect workflow step-order, validation, and metadata detectors."""

    def test_clean_manifest_has_no_structure_issues(self) -> None:
        manifest = _base_manifest()
        context = _context(manifest)

        issues = []
        issues.extend(detect_required_validation_commands(context))
        issues.extend(detect_workflow_step_order(context))
        issues.extend(detect_stale_workflow_metadata(context))

        self.assertEqual(issues, [])

    def test_missing_architecture_validation_command_fails(self) -> None:
        manifest = _base_manifest()
        manifest["workflows"]["business_checks"]["commands"] = []

        issues = detect_required_validation_commands(_context(manifest))

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_MISSING_ARCHITECTURE_VALIDATION_STEP",
        )
        self.assertEqual(issues[0].normalized_severity(), "fail")

    def test_disabled_business_checks_fails(self) -> None:
        manifest = _base_manifest()
        manifest["workflows"]["business_checks"]["enabled"] = False

        issues = detect_required_validation_commands(_context(manifest))

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_MISSING_ARCHITECTURE_VALIDATION_STEP",
        )

    def test_runtime_smoke_wrong_order_fails(self) -> None:
        manifest = _base_manifest()
        commands = manifest["workflows"]["runtime_smoke"]["commands"]
        manifest["workflows"]["runtime_smoke"]["commands"] = list(reversed(commands))

        issues = detect_workflow_step_order(_context(manifest))

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_ORDER_MISMATCH")
        self.assertEqual(issues[0].normalized_severity(), "fail")

    def test_stale_generated_metadata_fails(self) -> None:
        manifest = _base_manifest()
        stale = datetime.now(timezone.utc) - timedelta(days=400)
        manifest["generated_at_utc"] = stale.isoformat()

        issues = detect_stale_workflow_metadata(_context(manifest))

        self.assertEqual(len(issues), 1)
        self.assertEqual(
            issues[0].issue_id,
            "WORKFLOW_METADATA_STALE_OR_INVALID",
        )

    def test_default_registry_keeps_clean_manifest_clean(self) -> None:
        context = _context(_base_manifest())

        issues = DEFAULT_WORKFLOW_DETECTOR_REGISTRY.run(context)

        self.assertEqual(issues, [])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
