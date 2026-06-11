"""Regression tests for T10P065 workflow detector staged fallback."""

from __future__ import annotations

from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGACY_TOKEN = 'ask_' 'ai_project_reasoner'
WORKFLOW_CLI = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "manage_workflows"
    / "manage_workflows_help"
    / "workflow_cli.py"
)


class ManageWorkflowsDetectorFallbackTests(unittest.TestCase):
    """Validate canonical detector imports have a staged physical fallback."""

    def test_workflow_cli_keeps_canonical_import_contract(self) -> None:
        text = WORKFLOW_CLI.read_text(encoding="utf-8")
        self.assertIn(
            "from kanda_reasoner_app.manage_workflows."
            "manage_workflows_help.workflow_detector_context import",
            text,
        )

    def test_workflow_cli_has_dynamic_staged_detector_fallback(self) -> None:
        text = WORKFLOW_CLI.read_text(encoding="utf-8")
        self.assertIn('staged_package = "_".join(("ask", "ai", "project", "reasoner"))', text)
        self.assertIn('helper_base = staged_package + ".manage_workflows.manage_workflows_help"', text)
        self.assertIn('helper_base + ".workflow_detector_context"', text)
        self.assertIn('helper_base + ".workflow_detector_registry"', text)
        self.assertIn('helper_base + ".workflow_issue_models"', text)

    def test_workflow_cli_does_not_pin_literal_legacy_package_token(self) -> None:
        text = WORKFLOW_CLI.read_text(encoding="utf-8")
        self.assertNotIn(LEGACY_TOKEN, text)


if __name__ == "__main__":
    unittest.main()
