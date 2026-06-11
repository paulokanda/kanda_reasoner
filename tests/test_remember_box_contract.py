"""Focused tests for the Remember Box scaffold."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "remember_box"
)
CONTRACT_PATH = BOX_ROOT / "contract.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"

FORBIDDEN_IMPORT_ROOTS = (
    "PySide6",
    "main_window",
    "brain_navigator",
    "tab_navigation_controller",
    "tool_specs",
    "engineering_safety",
    "prompt_library",
)


class RememberBoxContractTests(unittest.TestCase):
    """Verify the Remember Box scaffold is display-state only and safe."""

    def test_public_contract_imports_contract_module_directly(self) -> None:
        """The focused test should import the public contract module directly."""

        import kanda_reasoner_app.reasoner_tools_gui_shell.remember_box.contract as contract_module

        self.assertEqual("remember_box", contract_module.REMEMBER_BOX_ID)
        self.assertEqual("0.1", contract_module.REMEMBER_BOX_CONTRACT_VERSION)
        self.assertIn("build_remember_box_state", contract_module.__all__)

    def test_public_package_imports_without_gui_side_effects(self) -> None:
        """The package facade should import without Qt, WebEngine, or registry."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box import (
            REMEMBER_BOX_CONTRACT_VERSION,
            REMEMBER_BOX_ID,
        )

        self.assertEqual("remember_box", REMEMBER_BOX_ID)
        self.assertEqual("0.1", REMEMBER_BOX_CONTRACT_VERSION)

    def test_summary_declares_display_state_boundary(self) -> None:
        """The summary should describe a display-state-only scaffold."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box import (
            get_remember_box_summary,
        )

        summary = get_remember_box_summary()

        self.assertEqual("remember_box", summary.box_id)
        self.assertEqual("0.1", summary.contract_version)
        self.assertEqual("scaffold_only_display_state", summary.implementation_state)
        self.assertIn("build_remember_box_state", summary.public_functions)
        self.assertIn(
            "kanda_reasoner_app/reasoner_tools_gui_shell/remember_box/",
            summary.owner_paths,
        )
        self.assertIn("tab switching", summary.responsibility)
        self.assertIn("PySide6", summary.forbidden_dependencies)

    def test_empty_state_is_safe_placeholder(self) -> None:
        """The empty state should be safe before any brain region is selected."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box import (
            create_empty_remember_box_state,
        )

        state = create_empty_remember_box_state()

        self.assertTrue(state.is_placeholder)
        self.assertFalse(state.can_open_target)
        self.assertEqual("placeholder", state.status)
        self.assertEqual("", state.target_tab_id)
        self.assertIn("Hover or click", state.analogy_text)

    def test_clear_state_returns_placeholder(self) -> None:
        """Clearing should not preserve stale navigation data."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box import (
            clear_remember_box_state,
        )

        state = clear_remember_box_state()

        self.assertTrue(state.is_placeholder)
        self.assertFalse(state.can_open_target)
        self.assertEqual("Select a brain region", state.action_label)

    def test_known_target_builds_openable_display_state(self) -> None:
        """A known target should become an openable display card state."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box import (
            build_remember_box_state,
        )

        target = SimpleNamespace(
            region_id="frontal_lobe",
            region_name="Frontal lobe",
            target_tab_id="architecture_review",
            target_tab_label="Architecture Review",
            analogy_title="Executive planning",
            analogy_text="Planning and organizing the whole app.",
            is_known=True,
        )

        state = build_remember_box_state(target)

        self.assertFalse(state.is_placeholder)
        self.assertTrue(state.can_open_target)
        self.assertEqual("mapped", state.status)
        self.assertEqual("frontal_lobe", state.region_id)
        self.assertEqual("architecture_review", state.target_tab_id)
        self.assertEqual("Open tool", state.action_label)

    def test_unknown_target_builds_unmapped_display_state(self) -> None:
        """Unknown targets should not ask the future navigator to open a tab."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box import (
            build_remember_box_state,
        )

        target = SimpleNamespace(
            region_id="not_real",
            region_name="Unknown brain region",
            target_tab_id="",
            target_tab_label="No target tab",
            analogy_title="No mapping available",
            analogy_text="Safe fallback text.",
            is_known=False,
        )

        state = build_remember_box_state(target)

        self.assertFalse(state.is_placeholder)
        self.assertFalse(state.can_open_target)
        self.assertEqual("unmapped", state.status)
        self.assertEqual("No action available", state.action_label)
        self.assertEqual("", state.target_tab_id)

    def test_none_target_returns_placeholder(self) -> None:
        """A missing target should use the same safe placeholder state."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box import (
            build_remember_box_state,
        )

        state = build_remember_box_state(None)

        self.assertTrue(state.is_placeholder)
        self.assertFalse(state.can_open_target)

    def test_manifest_declares_box_architecture_metadata(self) -> None:
        """The manifest should describe ownership, contract, and restrictions."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("remember_box", manifest["box_id"])
        self.assertEqual("gui_view", manifest["box_type"])
        self.assertEqual("module", manifest["box_size"])
        self.assertEqual("draft", manifest["health_state"])
        self.assertEqual("0.1", manifest["contract_version"])
        self.assertTrue(manifest["disable_safe"])
        self.assertEqual("optional", manifest["removal_policy"])
        self.assertIn("PySide6", manifest["forbidden_dependencies"])
        self.assertIn(
            "build_remember_box_state",
            manifest["public_contract"]["provides_functions"],
        )

    def test_contract_has_no_forbidden_imports_or_tab_switch_calls(self) -> None:
        """The scaffold contract should not import GUI or navigation boxes."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

        for token in FORBIDDEN_IMPORT_ROOTS:
            self.assertNotIn(token, imported_roots)
        self.assertNotIn("setCurrentIndex", text)
        self.assertNotIn("open_tab_by_id", text)

    def test_readme_declares_no_gui_or_navigation_ownership(self) -> None:
        """The README should make the display-state boundary explicit."""

        readme_text = README_PATH.read_text(encoding="utf-8")

        self.assertIn("scaffold only", readme_text)
        self.assertIn("display-state contract only", readme_text)
        self.assertIn("does not render the brain", readme_text)
        self.assertIn("does not open tabs", readme_text)
        self.assertIn("does not import PySide6", readme_text)


if __name__ == "__main__":
    unittest.main()
