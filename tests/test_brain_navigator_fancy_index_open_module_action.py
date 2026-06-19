"""Focused tests for Brain Navigator floating Fancy Index open-module action."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "brain_navigator"
)
VISIBLE_TAB_PATH = BOX_ROOT / "_visible_neural_architecture_tab.py"
FLOATING_TEMPLATE_PATH = BOX_ROOT / "assets" / "brain_visual_floating_window_template.py"
FLOATING_DATA_PATH = BOX_ROOT / "assets" / "brain_visual_floating_window.py"
TEMPLATE_PATH = BOX_ROOT / "assets" / "brain_visual_template.py"


class BrainNavigatorFancyIndexOpenModuleActionTests(unittest.TestCase):
    """Protect the controlled Open module action path."""

    def test_floating_index_has_explicit_open_module_action(self) -> None:
        """The floating window should contain a controlled action button."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            build_neural_architecture_preview_html,
        )

        html = build_neural_architecture_preview_html()

        self.assertIn("floating-remember-window-action", html)
        self.assertIn("Open module", html)
        self.assertIn("Stable tab-id route", html)
        self.assertIn("callBrainBridgeOpenModule(windowData.region_id)", html)
        self.assertNotIn("callBrainBridgeClick(markerData.region_id)", html)
        self.assertNotIn("setCurrentIndex", html)

    def test_marker_click_opens_index_without_immediate_navigation(self) -> None:
        """Marker click should open the index; the button emits navigation intent."""

        text = TEMPLATE_PATH.read_text(encoding="utf-8")
        floating_text = FLOATING_TEMPLATE_PATH.read_text(encoding="utf-8")

        self.assertIn("showFloatingRememberWindow(markerData", text)
        self.assertNotIn("showFloatingRememberWindow(markerData, event.clientX, event.clientY);\n        callBrainBridgeClick(markerData.region_id);", text)
        self.assertIn("actionButton.addEventListener", floating_text)
        self.assertIn("callBrainBridgeOpenModule(windowData.region_id)", floating_text)

    def test_visible_tab_uses_mapping_and_injected_callback_only(self) -> None:
        """Navigation should use mapping and injected stable-tab callback only."""

        text = VISIBLE_TAB_PATH.read_text(encoding="utf-8")
        tree = ast.parse(text)
        top_level_imports: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.Import):
                top_level_imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level_imports.add(node.module)

        self.assertNotIn("kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping.contract", top_level_imports)
        self.assertIn("from ..brain_region_mapping.contract import resolve_brain_region", text)
        self.assertIn("open_tab_by_id(target.target_tab_id)", text)
        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator import contract
        self.assertTrue(callable(contract.open_mapped_tab_by_region_id))
        self.assertIn("on_region_clicked=lambda region_id", text)
        self.assertNotIn("setCurrentIndex", text)
        self.assertNotIn("import main_window", text)
        self.assertNotIn("import tool_specs", text)

    def test_mapping_adapter_opens_known_region_and_ignores_unknown_region(self) -> None:
        """The private adapter should open known target tabs and ignore unknowns."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            open_mapped_tab_by_region_id,
        )

        opened: list[str] = []

        def open_tab(tab_id: str) -> str:
            opened.append(tab_id)
            return tab_id

        result = open_mapped_tab_by_region_id("frontal_lobe", open_tab)
        self.assertEqual("architecture_review", result)
        self.assertEqual(["architecture_review"], opened)

        result = open_mapped_tab_by_region_id("unknown_region", open_tab)
        self.assertIsNone(result)
        self.assertEqual(["architecture_review"], opened)

    def test_floating_payloads_are_action_ready(self) -> None:
        """Every floating payload should include an action label and active action state."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.contract import (
            list_neural_architecture_floating_windows,
        )

        windows = list_neural_architecture_floating_windows()
        self.assertEqual(12, len(windows))
        self.assertTrue(any(window.region_id == "hippocampus" for window in windows))
        self.assertTrue(any(window.region_id == "broca_area" for window in windows))
        for window in windows:
            self.assertEqual("Open module", window.action_label)
            self.assertIn("injected Tab Navigation Controller", window.action_state)

    def test_floating_data_asset_remains_navigation_free(self) -> None:
        """The data asset should not import GUI or navigation internals."""

        text = FLOATING_DATA_PATH.read_text(encoding="utf-8")

        self.assertNotIn("main_window", text)
        self.assertNotIn("tool_specs", text)
        self.assertNotIn("tab_navigation_controller", text)
        self.assertNotIn("setCurrentIndex", text)


if __name__ == "__main__":
    unittest.main()
