"""Focused tests for intuitive, unnumbered GUI tab labels."""

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

EXPECTED_ALL_TAB_LABELS = [
    "Brain Navigator",
    "Architecture Review",
    "Workflow Review",
    "Engineering Safety",
    "Docstring Assistant",
    "Show Project to AI",
    "Refactor Report",
    "Project Q&A",
    "Freeze Feature After Update",
    "Exclusion Rules",
    "Prompt Library",
]

EXPECTED_LAZY_TAB_LABELS = EXPECTED_ALL_TAB_LABELS[1:9]

OLD_STEP_TOKENS = (
    "First step",
    "Second step",
    "Third step",
    "Fourth step",
    "Fifth step",
    "Sixth step",
    "Seventh step",
)


class GuiTabLabelsDynamicUnnumberedTests(unittest.TestCase):
    def test_lazy_tool_registry_uses_intuitive_order(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        labels = [
            spec.step_title for spec in TOOLS
            if spec.tab_kind == "lazy_tool"
        ]
        self.assertEqual(EXPECTED_LAZY_TAB_LABELS, labels)

    def test_visible_labels_are_unique_and_unnumbered(self) -> None:
        labels = list(EXPECTED_ALL_TAB_LABELS)

        self.assertEqual(len(labels), len(set(labels)))
        for label in labels:
            self.assertFalse(re.match(r"^\d+\.", label), label)
            self.assertNotIn("step", label.lower(), label)

    def test_engineering_safety_is_after_workflow_review(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        labels = [spec.step_title for spec in TOOLS]
        self.assertEqual(
            labels.index("Workflow Review") + 1,
            labels.index("Engineering Safety"),
        )

    def test_main_window_adds_tabs_without_number_prefixes(self) -> None:
        text = MAIN_WINDOW_PATH.read_text(encoding="utf-8")

        self.assertIn("self.tabs.addTab(page, spec.step_title)", text)
        self.assertIn("self._add_registered_tab(spec)", text)
        self.assertNotIn('f"{index}. {spec.step_title}"', text)
        self.assertNotIn('"8. Project Exclusion Rules"', text)
        self.assertNotIn('"9. Prompt Engineering Library"', text)
        self.assertNotIn('self.tabs.addTab(self.ignore_rules_tab, "Exclusion Rules")', text)
        self.assertNotIn('self.tabs.addTab(self.prompt_library_tab, "Prompt Library")', text)

    def test_old_step_labels_are_not_in_active_tab_specs(self) -> None:
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        combined = "\n".join(spec.step_title for spec in TOOLS)
        for token in OLD_STEP_TOKENS:
            self.assertNotIn(token, combined)


if __name__ == "__main__":
    unittest.main()
