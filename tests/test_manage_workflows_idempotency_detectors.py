"""Focused tests for workflow idempotency detectors."""

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
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors import (  # noqa: E501
    detect_workflow_idempotency_issues,
)


def _context_for_commands(*commands: object) -> WorkflowDetectorContext:
    manifest = {
        "workflows": {
            "runtime_smoke": {
                "enabled": True,
                "commands": list(commands),
            }
        }
    }
    return WorkflowDetectorContext(
        project_root=Path(".").resolve(),
        workflow_manifest=manifest,
        workflows_doc="",
    )


class WorkflowIdempotencyDetectorTests(unittest.TestCase):
    """Protect rerun-safety detection for Tab 2 workflow validation."""

    def test_append_redirection_is_error(self) -> None:
        context = _context_for_commands(
            {"name": "append log", "command": "python tool.py >> result.txt"}
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_NOT_IDEMPOTENT_APPEND_OUTPUT")
        self.assertEqual(issues[0].severity, "error")

    def test_powershell_append_is_error(self) -> None:
        context = _context_for_commands(
            {"name": "append content", "command": "Add-Content -Path out.txt -Value ok"}
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_NOT_IDEMPOTENT_APPEND_OUTPUT")

    def test_new_item_directory_without_force_is_error(self) -> None:
        context = _context_for_commands(
            {
                "name": "make dir",
                "command": "New-Item -ItemType Directory -Path workbench\\out",
            }
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_NOT_IDEMPOTENT_NEW_DIRECTORY")

    def test_new_item_directory_with_force_is_allowed(self) -> None:
        context = _context_for_commands(
            {
                "name": "make dir",
                "command": "New-Item -ItemType Directory -Force -Path workbench\\out",
            }
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(issues, [])

    def test_compress_archive_without_force_is_error(self) -> None:
        context = _context_for_commands(
            {
                "name": "zip",
                "command": "Compress-Archive -Path src -DestinationPath out.zip",
            }
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_NOT_IDEMPOTENT_COMPRESS_ARCHIVE")

    def test_compress_archive_with_force_is_allowed(self) -> None:
        context = _context_for_commands(
            {
                "name": "zip",
                "command": "Compress-Archive -Path src -DestinationPath out.zip -Force",
            }
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(issues, [])

    def test_remove_item_without_guard_is_error(self) -> None:
        context = _context_for_commands(
            {"name": "remove", "command": "Remove-Item out.txt"}
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_NOT_IDEMPOTENT_REMOVE_ITEM")

    def test_remove_item_with_error_action_is_allowed(self) -> None:
        context = _context_for_commands(
            {"name": "remove", "command": "Remove-Item out.txt -ErrorAction SilentlyContinue"}
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(issues, [])

    def test_explicit_allow_non_idempotent_suppresses_issue(self) -> None:
        context = _context_for_commands(
            {
                "name": "append intentional",
                "command": "python tool.py >> result.txt",
                "allow_non_idempotent": True,
            }
        )

        issues = detect_workflow_idempotency_issues(context)

        self.assertEqual(issues, [])

    def test_registry_can_run_idempotency_detector(self) -> None:
        context = _context_for_commands(
            {"name": "append log", "command": "python tool.py >> result.txt"}
        )
        registry = WorkflowDetectorRegistry()
        registry.register("idempotency", detect_workflow_idempotency_issues)

        issues = run_workflow_detectors(context, registry=registry)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_id, "WORKFLOW_STEP_NOT_IDEMPOTENT_APPEND_OUTPUT")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
