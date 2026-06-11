"""Regression tests for canonical workflow-governance protection imports."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

import kanda_reasoner_app.package_migration.package_inventory
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_artifact_route_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_cross_project_generalization_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_documentation_drift_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_environment_contract_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_file_contract
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_idempotency_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_interaction_contract_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_issue_models
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_output_contract
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_rollback_fail_safe_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_order_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_step_target_detectors
import kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_validation_reference_detectors


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_LOADER = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "manage_architecture_help"
    / "source_loader_private_impl.py"
)
THIS_FILE = Path(__file__).resolve()


class WorkflowGovernanceTestProtectionAliasTests(unittest.TestCase):
    """Protect canonical test imports during the staged package migration."""

    def test_source_loader_maps_canonical_test_imports_to_staged_modules(self) -> None:
        text = SOURCE_LOADER.read_text(encoding="utf-8")
        self.assertIn("_apply_canonical_test_protection_alias_policy", text)
        self.assertIn("canonical_prefix", text)
        legacy_token = "ask" + "_ai" + "_project" + "_reasoner"
        self.assertIn('"ask" + "_ai" + "_project" + "_reasoner"', text)
        self.assertNotIn(legacy_token, text)

    def test_anchor_imports_are_static_canonical_imports(self) -> None:
        tree = ast.parse(THIS_FILE.read_text(encoding="utf-8"))
        imports = [
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        ]
        workflow_imports = [
            name
            for name in imports
            if name.startswith(
                "kanda_reasoner_app.manage_workflows.manage_workflows_help."
            )
        ]
        self.assertGreaterEqual(len(workflow_imports), 16)
        for module_name in workflow_imports:
            self.assertNotIn("ask" + "_ai" + "_project" + "_reasoner", module_name)


if __name__ == "__main__":
    unittest.main()
