"""Focused tests for the workflow helper facade public surface."""

from __future__ import annotations

import unittest

import kanda_reasoner_app.manage_workflows.manage_workflows_help as helpers
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract as workflow_file_contract
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_output_contract as workflow_output_contract
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_placeholder_contract as workflow_placeholder_contract
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    WorkflowDetectorRegistry,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models import (  # noqa: E501
    WorkflowIssue,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors import (  # noqa: E501
    detect_workflow_step_target_integrity,
)


class WorkflowHelperFacadeExportTests(unittest.TestCase):
    """Protect public facade exports and private helper module imports."""

    def test_facade_exports_detector_infrastructure(self) -> None:
        self.assertIs(helpers.WorkflowDetectorContext, WorkflowDetectorContext)
        self.assertIs(helpers.WorkflowDetectorRegistry, WorkflowDetectorRegistry)
        self.assertIs(helpers.WorkflowIssue, WorkflowIssue)

    def test_facade_exports_workflow_runner_surface(self) -> None:
        for name in (
            "CheckResult",
            "command_list_results",
            "generate_manifest",
            "main",
            "run_tests",
            "run_workflow_detector_results",
            "scan_project",
            "validate_project",
        ):
            self.assertIn(name, helpers.__all__)
            self.assertTrue(hasattr(helpers, name), name)

    def test_facade_exports_step_target_detector_surface(self) -> None:
        self.assertIn("detect_workflow_step_target_integrity", helpers.__all__)
        self.assertIs(
            helpers.detect_workflow_step_target_integrity,
            detect_workflow_step_target_integrity,
        )

    def test_facade_does_not_import_obsolete_structure_detector_symbol(self) -> None:
        self.assertNotIn("detect_workflow_structure_issues", helpers.__all__)
        self.assertFalse(hasattr(helpers, "detect_workflow_structure_issues"))

    def test_contract_modules_import_directly_for_test_protection(self) -> None:
        self.assertTrue(hasattr(workflow_file_contract, "validate_file_contract"))
        self.assertTrue(hasattr(workflow_file_contract, "validate_expected_json_files"))
        self.assertTrue(hasattr(workflow_output_contract, "output_contract_failure_message"))
        self.assertTrue(hasattr(workflow_placeholder_contract, "placeholder_contract_failure_message"))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
