"""Focused tests for Brain Navigator first-tab fallback wiring."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
MAIN_WINDOW_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "main_window.py"
)
TOOL_SPECS_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "tool_specs.py"
)
FALLBACK_WIDGET_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "brain_navigator"
    / "_fallback_index_widget.py"
)


class BrainNavigatorFirstTabFallbackTests(unittest.TestCase):
    """Validate first-tab fallback integration without importing PySide6."""

    def test_brain_navigator_is_first_registered_tab(self) -> None:
        """Brain Navigator should be the first visible tab in the registry."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        self.assertEqual("Brain Navigator", TOOLS[0].step_title)
        self.assertEqual("brain_navigator", TOOLS[0].tab_id)
        self.assertEqual("builtin_brain_navigator", TOOLS[0].tab_kind)

    def test_existing_tabs_remain_in_their_relative_order_after_brain_tab(self) -> None:
        """The old registry order should remain intact after the new first tab."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        labels = [spec.step_title for spec in TOOLS]
        self.assertEqual(
            [
                "Brain Navigator",
                "Architecture Review",
                "Workflow Review",
                "Engineering Safety",
                "Docstring Assistant",
                "Show Project to AI",
                "Error Memory",
                "Refactor Report",
                "Project Q&A",
                "Freeze Feature After Update",
                "Exclusion Rules",
                "Prompt Library",
            ],
            labels,
        )

    def test_main_window_handles_builtin_brain_navigator_kind(self) -> None:
        """MainWindow should add the first tab through the registered tab kind."""

        text = MAIN_WINDOW_PATH.read_text(encoding="utf-8")

        self.assertIn('spec.tab_kind == "builtin_brain_navigator"', text)
        self.assertIn("create_brain_navigator_tab", text)
        self.assertIn("self._register_tab_index(spec, index)", text)
        self.assertIn("self._tab_navigation_controller.refresh_tab_index_map", text)
        self.assertIn("self.tabs.setCurrentIndex(0)", text)

    def test_brain_navigator_uses_stable_tab_id_navigation_callback(self) -> None:
        """Brain Navigator should receive stable tab-id navigation, not indexes."""

        text = MAIN_WINDOW_PATH.read_text(encoding="utf-8")

        self.assertIn("open_tab_by_id=self._tab_navigation_controller.open_tab_by_id", text)
        self.assertIn("can_open_tab_id=self._tab_navigation_controller.can_open_tab", text)
        self.assertNotIn("brain_navigator_tab.setCurrentIndex", text)
        self.assertNotIn("open_tab_by_index", text)

    def test_fallback_index_uses_mapping_and_remember_contracts_only(self) -> None:
        """The fallback widget should compose boxes through public contracts."""

        text = FALLBACK_WIDGET_PATH.read_text(encoding="utf-8")

        self.assertIn("brain_region_mapping.contract", text)
        self.assertIn("remember_box.contract", text)
        self.assertIn("list_brain_region_targets", text)
        self.assertIn("build_remember_box_state", text)
        self.assertNotIn("QWebEngine", text)
        self.assertNotIn("setCurrentIndex", text)

    def test_tool_specs_declares_brain_tab_without_lazy_tool_candidates(self) -> None:
        """The Brain Navigator registry entry should be builtin and stable."""

        text = TOOL_SPECS_PATH.read_text(encoding="utf-8")

        self.assertIn('step_title="Brain Navigator"', text)
        self.assertIn('tab_id="brain_navigator"', text)
        self.assertIn('tab_kind="builtin_brain_navigator"', text)


if __name__ == "__main__":
    unittest.main()
