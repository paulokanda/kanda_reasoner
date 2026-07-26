"""Focused validation for Workbench GUI height restore v2."""
from __future__ import annotations

import py_compile
from pathlib import Path
import unittest

FEATURE_ID = "architecture-review-large-file-refactor-workbench-gui-height-restore-v2"


class WorkbenchGuiHeightRestoreV2Tests(unittest.TestCase):
    """Validate safe scroll ownership for compact Workbench GUI layout."""

    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.workbench_gui = self.project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui.py"
        self.layout_helper = self.project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui_layout.py"

    def test_workbench_adds_scroll_area_not_internal_parent_widget(self) -> None:
        """Workbench must add the explicit QScrollArea, never content.parentWidget()."""
        text = self.workbench_gui.read_text(encoding="utf-8")
        self.assertIn("scroll_area, content, content_layout = build_scrollable_workbench_content()", text)
        self.assertIn("layout.addWidget(scroll_area, 1)", text)
        self.assertIn("_large_file_refactor_workbench_scroll_area", text)
        self.assertIn("_large_file_refactor_workbench_content_widget", text)
        self.assertNotIn("content.parentWidget()", text)

    def test_layout_helper_returns_scroll_area_content_and_layout(self) -> None:
        """Helper must keep scroll ownership explicit to prevent deleted C++ layouts."""
        text = self.layout_helper.read_text(encoding="utf-8")
        self.assertIn("QScrollArea", text)
        self.assertIn("tuple[QScrollArea, QWidget, QVBoxLayout]", text)
        self.assertIn("content = QWidget(scroll)", text)
        self.assertIn("scroll.setWidget(content)", text)
        self.assertIn("return scroll, content, content_layout", text)
        self.assertNotIn("return content, layout", text)

    def test_output_height_caps_remain_compact(self) -> None:
        """Output panels must remain compact after the ownership repair."""
        text = self.layout_helper.read_text(encoding="utf-8")
        self.assertIn("_OUTPUT_MAX_HEIGHT = 96", text)
        self.assertIn("_OUTPUT_MIN_HEIGHT = 54", text)
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
        """Changed Python files must compile and stay under the 500-line cap."""
        for path in [self.workbench_gui, self.layout_helper, Path(__file__)]:
            self.assertTrue(path.is_file(), str(path))
            py_compile.compile(str(path), doraise=True)
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 500, str(path))


if __name__ == "__main__":
    unittest.main()
