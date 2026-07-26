"""Tests for final complete Workbench freeze closure evidence."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.final_complete_workbench_freeze import (
    COMPLETE_WORKBENCH_FREEZE_FEATURE_ID,
    build_complete_workbench_freeze_report,
    write_complete_workbench_freeze_report,
)


class CompleteWorkbenchFreezeTests(unittest.TestCase):
    """Verify read-only completion evidence for the 25-step roadmap."""

    def test_current_project_reports_complete_25_step_status(self) -> None:
        """The installed project should expose all final Workbench pieces."""
        project_root = Path(__file__).resolve().parents[1]
        report = build_complete_workbench_freeze_report(active_project_root=str(project_root))
        self.assertEqual(report.feature_id, COMPLETE_WORKBENCH_FREEZE_FEATURE_ID)
        self.assertEqual(report.status, "complete_workbench_freeze_ready", report.blockers)
        self.assertEqual(report.completed_steps, 25)
        self.assertEqual(report.target_steps, 25)
        self.assertFalse(report.source_mutation_enabled)
        self.assertFalse(report.apply_enabled)
        self.assertFalse(report.import_rewrite_apply_enabled)
        self.assertFalse(report.batch_apply_enabled)
        self.assertFalse(report.behavior_validation_claimed)
        self.assertFalse(report.writes_freeze_memory)
        self.assertIn("build_behavior_test_presets", report.required_exports)
        self.assertIn("validate_architecture_review_large_file_refactor_behavior_test_presets_v1.py", report.required_validators)

    def test_write_completion_report_stays_in_daily_work_preview(self) -> None:
        """Completion reports are written only under daily-work preview roots."""
        project_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp_name:
            preview_root = Path(temp_name) / "daily" / "large_file_refactor_preview"
            report = build_complete_workbench_freeze_report(
                active_project_root=str(project_root),
                preview_root=str(preview_root),
            )
            blocked = write_complete_workbench_freeze_report
            self.assertIn("PREVIEW_ROOT_OUTSIDE_DAILY_WORK", report.blockers)
            with self.assertRaises(RuntimeError):
                bad = report.__class__(**{**report.to_dict(), "report_path": str(project_root / "bad.json")})
                blocked(bad)


if __name__ == "__main__":
    unittest.main()
