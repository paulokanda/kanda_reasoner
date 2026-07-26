"""Regression tests for complete Workbench freeze closure repair v2."""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import final_complete_workbench_freeze as closure


class CompleteWorkbenchFreezeRepairV2Tests(unittest.TestCase):
    """Verify historical validators do not block final closure evidence."""

    def test_historical_import_migration_validator_is_warning_not_blocker(self) -> None:
        """A missing old import-migration validator must not block final closure."""
        with tempfile.TemporaryDirectory() as temp_name:
            project_root = Path(temp_name) / "synthetic_project"
            planner_root = project_root / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
            tools_root = project_root / "tools"
            planner_root.mkdir(parents=True)
            tools_root.mkdir(parents=True)
            for name in closure.REQUIRED_COMPLETE_WORKBENCH_PLANNER_FILES:
                text = "# synthetic planner file\n"
                if name in {"batch_refactor_queue.py", "visual_diff_ui.py", "behavior_test_presets.py"}:
                    text += "source_mutation_enabled: bool = False\n"
                (planner_root / name).write_text(text, encoding="utf-8")
            for name in closure.REQUIRED_COMPLETE_WORKBENCH_VALIDATORS:
                (tools_root / name).write_text("# synthetic validator\n", encoding="utf-8")
            report = closure.build_complete_workbench_freeze_report(active_project_root=str(project_root))
            self.assertEqual(report.status, "complete_workbench_freeze_ready", report.blockers)
            self.assertFalse(any("MISSING_VALIDATOR:validate_architecture_review_large_file_refactor_import_migration_review_v1.py" in item for item in report.blockers))
            self.assertIn(
                "HISTORICAL_VALIDATOR_NOT_INSTALLED:validate_architecture_review_large_file_refactor_import_migration_review_v1.py",
                report.warnings,
            )

    def test_current_project_repair_still_reports_complete(self) -> None:
        """The real installed project should report completion after the repair."""
        project_root = Path(__file__).resolve().parents[1]
        report = closure.build_complete_workbench_freeze_report(active_project_root=str(project_root))
        self.assertEqual(report.status, "complete_workbench_freeze_ready", report.blockers)
        self.assertEqual(report.completed_steps, 25)
        self.assertEqual(report.target_steps, 25)
        self.assertFalse(report.source_mutation_enabled)
        self.assertFalse(report.apply_enabled)
        self.assertFalse(report.import_rewrite_apply_enabled)
        self.assertFalse(report.batch_apply_enabled)
        self.assertFalse(report.behavior_validation_claimed)
        self.assertFalse(report.writes_freeze_memory)


if __name__ == "__main__":
    unittest.main()
