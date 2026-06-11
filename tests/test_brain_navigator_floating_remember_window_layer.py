"""Focused tests for the Neural Architecture floating Remember Box layer."""

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
ASSETS_ROOT = BOX_ROOT / "assets"
CONTRACT_PATH = BOX_ROOT / "contract.py"
FLOATING_WINDOW_PATH = ASSETS_ROOT / "brain_visual_floating_window.py"
TEMPLATE_PATH = ASSETS_ROOT / "brain_visual_template.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"


class BrainNavigatorFloatingRememberWindowLayerTests(unittest.TestCase):
    """Validate click-open floating Remember Box windows and boundaries."""

    def test_public_contract_exposes_floating_window_helpers_lazily(self) -> None:
        """The public contract should expose floating-window helpers without GUI imports."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract

        self.assertTrue(callable(contract.list_neural_architecture_floating_windows))
        self.assertTrue(callable(contract.build_neural_architecture_floating_window_data_js))
        self.assertTrue(callable(contract.get_neural_architecture_floating_window_summary))

    def test_floating_window_regions_match_mapping_contract(self) -> None:
        """Every floating window should map to a known brain-region target."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            list_neural_architecture_floating_windows,
        )
        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            list_brain_region_ids,
        )

        window_ids = tuple(window.region_id for window in list_neural_architecture_floating_windows())

        self.assertEqual(tuple(list_brain_region_ids()), window_ids)

    def test_floating_window_data_is_pure_asset_without_gui_or_navigation_reach_in(self) -> None:
        """The floating window module should not import GUI, registry, or navigation boxes."""

        text = FLOATING_WINDOW_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)

        self.assertNotIn("PySide6", imported_modules)
        self.assertNotIn("main_window", imported_modules)
        self.assertNotIn("tool_specs", imported_modules)
        self.assertNotIn("tab_navigation_controller", imported_modules)
        self.assertNotIn("brain_region_mapping", imported_modules)
        self.assertNotIn("setCurrentIndex", text)

    def test_contract_lazily_delegates_to_floating_window_asset(self) -> None:
        """The contract should import floating-window helpers only inside functions."""

        text = CONTRACT_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        top_level_imports: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top_level_imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_imports.add(node.module)

        self.assertNotIn(".assets.brain_visual_floating_window", top_level_imports)
        self.assertIn("from .assets.brain_visual_floating_window import", text)
        self.assertIn("list_neural_architecture_floating_windows", text)
        self.assertIn("build_neural_architecture_floating_window_data_js", text)

    def test_preview_html_contains_click_open_floating_window_layer(self) -> None:
        """The visible brain HTML should contain floating-window behavior."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn("const NEURAL_ARCHITECTURE_FLOATING_WINDOWS", html)
        self.assertIn("showFloatingRememberWindow(markerData", html)
        self.assertIn("hideFloatingRememberWindow", html)
        self.assertIn("findFloatingRememberWindowData", html)
        self.assertIn("positionFloatingRememberWindow", html)
        self.assertIn("floating-remember-window-title", html)
        self.assertIn("floating-remember-window-module", html)
        self.assertIn("floating-remember-window-status", html)
        self.assertIn("floating-remember-window-action", html)
        self.assertIn("event.stopPropagation()", html)
        self.assertIn("event.key === \"Escape\"", html)
        self.assertIn("!floatingWindow.contains(event.target)", html)
        self.assertIn("callBrainBridgeOpenModule(windowData.region_id)", html)
        self.assertNotIn("setCurrentIndex", html)

    def test_template_tracks_floating_window_creation(self) -> None:
        """The template should import data and render click window functions."""

        text = TEMPLATE_PATH.read_text(encoding="utf-8")

        self.assertIn("build_neural_architecture_floating_window_data_js", text)
        self.assertIn("floating_window_data_js", text)
        self.assertIn("showFloatingRememberWindow(markerData", text)
        self.assertIn("hideFloatingRememberWindow();", text)
        self.assertIn('document.addEventListener("click"', text)

    def test_manifest_tracks_floating_window_layer(self) -> None:
        """The Brain Navigator manifest should track Patch 12."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_navigator", manifest["box_id"])
        self.assertEqual("1.0.0", manifest["version"])
        self.assertIn("assets/brain_visual_floating_window.py", manifest["private_internals"])
        self.assertIn(
            "list_neural_architecture_floating_windows",
            manifest["public_contract"]["provides_functions"],
        )
        self.assertIn(
            "tests/test_brain_navigator_floating_remember_window_layer.py",
            manifest["validation"]["focused_tests"],
        )
        self.assertIn(
            "floating_fancy_index_open_module_action_via_region_mapping_and_injected_tab_callback",
            manifest["communication_route"],
        )

    def test_readme_documents_floating_window_no_navigation_state(self) -> None:
        """README should document click windows and deferred navigation."""

        readme = README_PATH.read_text(encoding="utf-8")

        self.assertIn("Patch 12 - Floating Remember Box window layer", readme)
        self.assertIn("left click on a pulse marker opens", readme)
        self.assertIn("closes when the user clicks outside it", readme)
        self.assertIn("presses Escape", readme)
        self.assertIn("does not switch tabs", readme)
        self.assertIn("Patch 16 - Floating Fancy Index open-module action", readme)
        self.assertIn("Open module action", readme)


if __name__ == "__main__":
    unittest.main()
