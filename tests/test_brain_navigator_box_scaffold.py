"""Focused tests for the Brain Navigator Box contract and fallback boundary."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "brain_navigator"
)
CONTRACT_PATH = BOX_ROOT / "contract.py"
FALLBACK_WIDGET_PATH = BOX_ROOT / "_fallback_index_widget.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"

FORBIDDEN_PUBLIC_CONTRACT_IMPORTS = (
    "PySide6",
    "main_window",
    "tool_specs",
)

FORBIDDEN_PUBLIC_CONTRACT_CALLS = (
    "setCurrentIndex",
)


class BrainNavigatorBoxScaffoldTests(unittest.TestCase):
    """Verify the Brain Navigator contract remains isolated."""

    def test_public_contract_imports_without_gui_side_effects(self) -> None:
        """The public contract should import without Qt or WebEngine."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract

        self.assertEqual("brain_navigator", contract.BRAIN_NAVIGATOR_BOX_ID)
        self.assertEqual("brain_navigator", contract.BRAIN_NAVIGATOR_TAB_ID)
        self.assertEqual("Brain Navigator", contract.BRAIN_NAVIGATOR_TAB_LABEL)

    def test_contract_summary_declares_single_box_boundary(self) -> None:
        """The summary should describe the Brain Navigator fallback boundary."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            get_brain_navigator_contract_summary,
        )

        summary = get_brain_navigator_contract_summary()

        self.assertEqual("brain_navigator", summary.box_id)
        self.assertEqual("Brain Navigator", summary.tab_label)
        self.assertEqual("visible_neural_architecture_brain_with_fancy_index_open_module_action", summary.implementation_state)
        self.assertIn(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/",
            summary.owner_paths,
        )
        self.assertIn("brain_region_clicked(region_id)", summary.public_outputs)
        self.assertIn("main_window", summary.forbidden_dependencies)

    def test_public_contract_lazily_loads_visible_brain_factory(self) -> None:
        """The public contract should delegate widget creation lazily."""

        contract_text = CONTRACT_PATH.read_text(encoding="utf-8")

        self.assertIn("create_visible_neural_architecture_brain_tab", contract_text)
        self.assertIn("from ._visible_neural_architecture_tab import", contract_text)
        self.assertNotIn("raise NotImplementedError", contract_text)

    def test_manifest_declares_box_architecture_metadata(self) -> None:
        """The manifest should describe ownership, contract, and restrictions."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_navigator", manifest["box_id"])
        self.assertEqual("gui_view", manifest["box_type"])
        self.assertEqual("domain", manifest["box_size"])
        self.assertEqual("active", manifest["health_state"])
        self.assertEqual("0.1", manifest["contract_version"])
        self.assertTrue(manifest["disable_safe"])
        self.assertIn("_fallback_index_widget.py", manifest["private_internals"])
        self.assertIn("_visible_neural_architecture_tab.py", manifest["private_internals"])
        self.assertIn("brain_region_mapping", manifest["allowed_dependencies"])
        self.assertIn("remember_box", manifest["allowed_dependencies"])
        self.assertIn(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/",
            manifest["owner_paths"],
        )
        self.assertIn("main_window", manifest["forbidden_dependencies"])
        self.assertIn(
            "get_brain_navigator_contract_summary",
            manifest["public_contract"]["provides_functions"],
        )

    def test_public_contract_has_no_forbidden_gui_or_tab_imports(self) -> None:
        """The public contract should not import GUI, registry, or tab internals."""

        contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(contract_text)
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

        for token in FORBIDDEN_PUBLIC_CONTRACT_IMPORTS:
            self.assertNotIn(token, imported_roots)
        for token in FORBIDDEN_PUBLIC_CONTRACT_CALLS:
            self.assertNotIn(token, contract_text)

    def test_fallback_widget_avoids_webengine_and_hardcoded_tab_indices(self) -> None:
        """Fallback internals should stay free of WebEngine and direct tab indexes."""

        fallback_text = FALLBACK_WIDGET_PATH.read_text(encoding="utf-8")

        self.assertNotIn("QWebEngine", fallback_text)
        self.assertNotIn("setCurrentIndex", fallback_text)
        self.assertNotIn("main_window", fallback_text)
        self.assertIn("open_tab_by_id", fallback_text)
        self.assertIn("build_remember_box_state", fallback_text)
        self.assertIn("list_brain_region_targets", fallback_text)

    def test_readme_declares_visible_brain_and_safe_fallback(self) -> None:
        """The README should make the visible brain boundary explicit."""

        readme_text = README_PATH.read_text(encoding="utf-8")

        self.assertIn("Visible Neural Architecture default tab", readme_text)
        self.assertIn("fallback index remains available only if WebEngine", readme_text)
        self.assertIn("does not call `setCurrentIndex`", readme_text)
        self.assertIn("does not switch tabs", readme_text)


if __name__ == "__main__":
    unittest.main()
