"""Focused tests for a single dynamic GUI tab registry."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN_WINDOW_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "main_window.py"
)
WINDOW_TOOL_PATCHES_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "main_window_help"
    / "window_tool_patches.py"
)

EXPECTED_ALL_TAB_LABELS = [
    "Brain Navigator",
    "Architecture Review",
    "Workflow Review",
    "Engineering Safety",
    "Docstring Assistant",
    "Project Structure Map",
    "AI Import Builder",
    "Refactor Report",
    "Project Q&A",
    "Exclusion Rules",
    "Prompt Library",
]

EXPECTED_LAZY_TAB_LABELS = EXPECTED_ALL_TAB_LABELS[1:9]
EXPECTED_BUILTIN_TAB_LABELS = [EXPECTED_ALL_TAB_LABELS[0], *EXPECTED_ALL_TAB_LABELS[9:]]

OLD_STEP_TOKENS = (
    "First step",
    "Second step",
    "Third step",
    "Fourth step",
    "Fifth step",
    "Sixth step",
    "Seventh step",
)


class GuiTabRegistryAllTabsDynamicTests(unittest.TestCase):
    def test_all_visible_tabs_are_in_single_registry(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        labels = [spec.step_title for spec in TOOLS]
        self.assertEqual(EXPECTED_ALL_TAB_LABELS, labels)

    def test_registry_has_unique_stable_ids_and_labels(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        labels = [spec.step_title for spec in TOOLS]
        tab_ids = [spec.tab_id for spec in TOOLS]

        self.assertEqual(len(labels), len(set(labels)))
        self.assertEqual(len(tab_ids), len(set(tab_ids)))
        self.assertNotIn(None, tab_ids)

        for label in labels:
            self.assertFalse(re.match(r"^\d+\.", label), label)
            self.assertNotIn("step", label.lower(), label)

    def test_registry_marks_lazy_and_builtin_tabs(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        lazy_labels = [
            spec.step_title for spec in TOOLS
            if spec.tab_kind == "lazy_tool"
        ]
        builtin_labels = [
            spec.step_title for spec in TOOLS
            if spec.tab_kind != "lazy_tool"
        ]

        self.assertEqual(EXPECTED_LAZY_TAB_LABELS, lazy_labels)
        self.assertEqual(EXPECTED_BUILTIN_TAB_LABELS, builtin_labels)

    def test_engineering_safety_is_after_workflow_review(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        labels = [spec.step_title for spec in TOOLS]
        self.assertEqual(
            labels.index("Workflow Review") + 1,
            labels.index("Engineering Safety"),
        )

    def test_main_window_adds_every_tab_from_registry(self) -> None:
        text = MAIN_WINDOW_PATH.read_text(encoding="utf-8")

        self.assertIn("for spec in TOOLS:", text)
        self.assertIn("self._add_registered_tab(spec)", text)
        self.assertIn("def _add_registered_tab", text)
        self.assertIn("builtin_ignore_rules", text)
        self.assertIn("builtin_prompt_library", text)
        self.assertNotIn('self.tabs.addTab(self.ignore_rules_tab, "Exclusion Rules")', text)
        self.assertNotIn('self.tabs.addTab(self.prompt_library_tab, "Prompt Library")', text)

    def test_lazy_tab_loading_uses_tab_index_map(self) -> None:
        text = WINDOW_TOOL_PATCHES_PATH.read_text(encoding="utf-8")

        self.assertIn("_lazy_pages_by_tab_index", text)
        self.assertNotIn("index < len(self._pages)", text)
        self.assertNotIn("self._pages[index].ensure_loaded()", text)

    def test_old_step_labels_are_not_in_active_tab_specs(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        combined = "\n".join(spec.step_title for spec in TOOLS)
        for token in OLD_STEP_TOKENS:
            self.assertNotIn(token, combined)


if __name__ == "__main__":
    unittest.main()
