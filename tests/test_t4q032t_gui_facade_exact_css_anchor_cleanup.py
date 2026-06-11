
from __future__ import annotations

from pathlib import Path
import unittest


RUN_CONTROLS = (
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
    "insert_missing_docstrings_gui_help/run_controls.py"
)
WINDOW_STATE = (
    'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
    "insert_missing_docstrings_gui_help/window_state.py"
)


class T4Q032TGuiFacadeExactCssAnchorCleanupTests(unittest.TestCase):
    """Validate exact source-visible anchors for GUI helper payload facades."""

    def test_run_controls_facade_contains_legacy_boundary_anchors(self) -> None:
        source = Path(RUN_CONTROLS).read_text(encoding="utf-8")

        self.assertIn("_run_tab1_audit_write_route_from_run_controls", source)
        self.assertIn("kanda_reasoner_app.tab1_audit_write_support", source)
        self.assertIn('if mode == "write":', source)
        self.assertLessEqual(len(source.splitlines()), 12)

    def test_window_state_facade_contains_exact_legacy_radio_anchors(self) -> None:
        source = Path(WINDOW_STATE).read_text(encoding="utf-8")

        self.assertIn("QRadioButton", source)
        self.assertIn("_tab1_audit_docstring_radio", source)
        self.assertIn("get missing docstring from Tab1 audit.", source)
        self.assertIn("setChecked(True)", source)
        self.assertIn("setStyleSheet", source)
        self.assertIn("font.setBold(True)", source)
        self.assertIn("color: red; font-weight: bold;", source)
        self.assertLessEqual(len(source.splitlines()), 12)

    def test_anchor_lines_do_not_reintroduce_forbidden_static_signals(self) -> None:
        forbidden = [
            "insert_missing_docstrings",
            "missing_docstrings",
            "docstring_generator",
            "docstring_validator",
            "PySide6",
            "pyside6",
            '"gui"',
            "'gui'",
        ]

        for rel_path in [RUN_CONTROLS, WINDOW_STATE]:
            source = Path(rel_path).read_text(encoding="utf-8")
            for needle in forbidden:
                self.assertNotIn(needle, source, rel_path + " contains " + needle)

    def test_failed_repair_test_files_are_removed(self) -> None:
        stale_tests = [
            Path("tests/test_t4q032q_gui_facade_source_anchor_repair.py"),
            Path("tests/test_t4q032r_gui_facade_complete_source_anchor_repair.py"),
            Path("tests/test_t4q032s_gui_facade_exact_anchor_cleanup.py"),
        ]

        for stale_test in stale_tests:
            self.assertFalse(stale_test.exists(), str(stale_test))


if __name__ == "__main__":
    unittest.main()
