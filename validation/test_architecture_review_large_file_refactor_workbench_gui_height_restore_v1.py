# project-path: validation/test_architecture_review_large_file_refactor_workbench_gui_height_restore_v1.py
"""Focused validation for Workbench GUI height restore v1."""
from __future__ import annotations

import py_compile
from pathlib import Path
import unittest


FEATURE_ID = "architecture-review-large-file-refactor-workbench-gui-height-restore-v1"


class WorkbenchGuiHeightRestoreTests(unittest.TestCase):
    """Validate compact Workbench GUI layout repair."""

    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.workbench_gui = self.project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui.py"
        self.layout_helper = self.project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui_layout.py"

    def test_workbench_page_uses_scrollable_compact_content(self) -> None:
        """Workbench content must be scroll-contained instead of increasing app height."""
        text = self.workbench_gui.read_text(encoding="utf-8")
        self.assertIn("build_scrollable_workbench_content", text)
        self.assertIn("compact_workbench_text_outputs", text)
        self.assertIn("layout.addWidget(content.parentWidget(), 1)", text)
        self.assertNotIn("layout.addWidget(_build_apply_section(window), 1)", text)
        self.assertNotIn("layout.addWidget(build_behavior_validation_section(window, _root_text, _sync_workbench_buttons), 1)", text)

    def test_layout_helper_limits_plain_text_output_height(self) -> None:
        """Output panels must have explicit compact height limits."""
        text = self.layout_helper.read_text(encoding="utf-8")
        self.assertIn("QScrollArea", text)
        self.assertIn("_OUTPUT_MAX_HEIGHT = 96", text)
        self.assertIn("output.setMaximumHeight(_OUTPUT_MAX_HEIGHT)", text)
        self.assertIn("QSizePolicy.Fixed", text)

    def test_workbench_logic_gates_are_preserved(self) -> None:
        """The repair must not remove guarded apply, rollback, or behavior gates."""
        text = self.workbench_gui.read_text(encoding="utf-8")
        required = [
            "expected_guarded_apply_token",
            "execute_guarded_source_apply",
            "validate_and_write_post_apply",
            "expected_workbench_rollback_token",
            "execute_workbench_rollback",
            "sync_behavior_validation_buttons",
            "format_post_apply_validation",
        ]
        for item in required:
            self.assertIn(item, text)

    def test_changed_modules_compile_and_stay_under_size_cap(self) -> None:
        """Changed Python files must compile and stay below the 500-line cap."""
        for path in [self.workbench_gui, self.layout_helper, Path(__file__)]:
            self.assertTrue(path.is_file(), str(path))
            py_compile.compile(str(path), doraise=True)
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 500, str(path))


if __name__ == "__main__":
    unittest.main()
