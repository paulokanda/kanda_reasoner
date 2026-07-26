# project-path: validation/test_architecture_review_large_file_refactor_visual_diff_ui_v1.py
"""Validation tests for visual diff UI evidence."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    build_visual_diff_report,
    write_visual_diff_artifacts,
)


class VisualDiffUiTests(unittest.TestCase):
    """Visual diff artifacts remain display-only and daily-work contained."""

    def test_build_report_has_rows_and_no_write_flags(self) -> None:
        report = build_visual_diff_report("a\nb\n", "a\nc\n", source_label="old.py", target_label="new.py")
        self.assertEqual(report.status, "visual_diff_ready")
        self.assertFalse(report.source_mutation_enabled)
        self.assertFalse(report.apply_enabled)
        self.assertFalse(report.import_rewrite_apply_enabled)
        self.assertTrue(any(row.kind == "remove" and row.text == "b" for row in report.rows))
        self.assertTrue(any(row.kind == "add" and row.text == "c" for row in report.rows))
        self.assertEqual(len(report.source_sha256), 64)
        self.assertEqual(len(report.target_sha256), 64)

    def test_no_changes_status_is_visible(self) -> None:
        report = build_visual_diff_report("same\n", "same\n")
        self.assertEqual(report.status, "no_changes")
        self.assertTrue(report.visual_diff_enabled)

    def test_write_artifacts_under_temp_daily_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proj"
            root.mkdir()
            preview = root.parent / "proj_delete_after_daily_work" / "large_file_refactor_preview"
            report = write_visual_diff_artifacts(root, "x\n", "y\n", preview_root=preview)
            self.assertEqual(report.status, "visual_diff_ready")
            data = json.loads((preview / "VISUAL_DIFF_REPORT.json").read_text(encoding="utf-8"))
            self.assertFalse(data["source_mutation_enabled"])
            self.assertFalse(data["apply_enabled"])
            self.assertTrue((preview / "VISUAL_DIFF_VIEW.txt").is_file())
            self.assertTrue((preview / "VISUAL_DIFF_VIEW.html").is_file())

    def test_write_blocks_preview_inside_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proj"
            root.mkdir()
            with self.assertRaises(ValueError):
                write_visual_diff_artifacts(root, "x", "y", preview_root=root / "large_file_refactor_preview")


if __name__ == "__main__":
    unittest.main()
