"""Regression checks for migrated workflow and architecture tests."""

from __future__ import annotations

import importlib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGACY_TOKEN = "ask" + "_ai" + "_project" + "_reasoner"
CANONICAL_TOKEN = "kanda_reasoner_app"

MIGRATED_TEST_FILES = [
    "tests/test_manage_workflows_artifact_route_detectors.py",
    "tests/test_manage_workflows_cross_project_generalization_detectors.py",
    "tests/test_manage_workflows_detector_registry.py",
    "tests/test_manage_workflows_detector_registry_contract.py",
    "tests/test_manage_workflows_detector_report_integration.py",
    "tests/test_manage_workflows_documentation_drift_detectors.py",
    "tests/test_manage_workflows_environment_contract_detectors.py",
    "tests/test_manage_workflows_expected_files_contract.py",
    "tests/test_manage_workflows_expected_json_contract.py",
    "tests/test_manage_workflows_helper_facade_exports.py",
    "tests/test_manage_workflows_idempotency_detectors.py",
    "tests/test_manage_workflows_interaction_contract_detectors.py",
    "tests/test_manage_workflows_output_content_contract.py",
    "tests/test_manage_workflows_placeholder_contract.py",
    "tests/test_manage_workflows_reader_ai_contract_detectors.py",
    "tests/test_manage_workflows_rollback_fail_safe_detectors.py",
    "tests/test_manage_workflows_silent_success_gate.py",
    "tests/test_manage_workflows_step_order_detectors.py",
    "tests/test_manage_workflows_step_target_detectors.py",
    "tests/test_manage_workflows_structure_detectors.py",
    "tests/test_manage_workflows_validation_reference_detectors.py",
    "tests/test_architecture_cli_dynamic_root_help.py",
]


class WorkflowArchitectureTestsCanonicalRefsTests(unittest.TestCase):
    """Verify the migrated workflow and architecture test batch."""

    def test_migrated_tests_do_not_pin_legacy_package_token(self) -> None:
        for relative_path in MIGRATED_TEST_FILES:
            with self.subTest(relative_path=relative_path):
                text = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
                self.assertNotIn(LEGACY_TOKEN, text)
                self.assertIn(CANONICAL_TOKEN, text)

    def test_canonical_workflow_helper_subpackage_is_importable(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cli"
        )
        self.assertTrue(hasattr(module, "validate_project"))

    def test_canonical_project_analysis_evidence_paths_is_importable(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.project_analysis_evidence_paths"
        )
        self.assertTrue(hasattr(module, "project_analysis_evidence_root"))


if __name__ == "__main__":
    unittest.main()
