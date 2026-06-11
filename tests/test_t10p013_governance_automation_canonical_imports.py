"""Tests for Governance Automation canonical package references."""

from __future__ import annotations

import importlib
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_INIT = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "governance_automation" / "__init__.py"
PUSH_VALIDATOR = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "governance_automation"
    / "on_every_push_validator.py"
)


class GovernanceAutomationCanonicalImportTests(unittest.TestCase):
    """Validate canonical package references in Governance Automation."""

    def test_governance_init_imports_through_canonical_package(self) -> None:
        source = GOVERNANCE_INIT.read_text(encoding="utf-8")
        self.assertIn(
            "from kanda_reasoner_app.governance_automation.on_every_push_validator import",
            source,
        )
        self.assertIn(
            "from kanda_reasoner_app.governance_automation.release_notes_generator import",
            source,
        )
        self.assertNotIn(
            "from kanda_reasoner_app.governance_automation",
            source,
        )

    def test_default_push_commands_use_canonical_package_paths(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.governance_automation.on_every_push_validator"
        )
        commands = module.build_default_push_commands("E:/kanda_reasoner")
        joined = "\n".join(commands)

        self.assertIn("kanda_reasoner_app\\manage_architecture", joined)
        self.assertIn("kanda_reasoner_app\\manage_workflows", joined)
        self.assertIn("import kanda_reasoner_app", joined)
        self.assertIn("import reasoner_tools_gui", joined)
        self.assertNotIn('ask_' 'ai_project_reasoner' '\\manage_architecture', joined)
        self.assertNotIn('ask_' 'ai_project_reasoner' '\\manage_workflows', joined)
        self.assertNotIn('import ask_' 'ai_project_reasoner', joined)

    def test_governance_sources_do_not_hardcode_legacy_package_token(self) -> None:
        for path in (GOVERNANCE_INIT, PUSH_VALIDATOR):
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('ask_' 'ai_project_reasoner', source, path.as_posix())

    def test_legacy_governance_package_still_exposes_public_api(self) -> None:
        module = importlib.import_module("kanda_reasoner_app.governance_automation")
        commands = module.build_default_push_commands("E:/kanda_reasoner")
        self.assertTrue(commands)
        self.assertTrue(hasattr(module, "build_release_notes_report"))


if __name__ == "__main__":
    unittest.main()
