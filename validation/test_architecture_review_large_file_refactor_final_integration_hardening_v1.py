"""Validation tests for Large File Refactor final integration hardening."""
from __future__ import annotations

import os
from pathlib import Path
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_final_integration_hardening import (
    build_final_integration_hardening_report,
)


class FinalIntegrationHardeningTests(unittest.TestCase):
    """Read-only integration checks for the Workbench package."""

    def test_final_integration_report_passes_for_current_project(self) -> None:
        """The current installed project should pass final integration hardening."""
        project_root = Path(os.environ.get("KANDA_PROJECT_ROOT", Path(__file__).resolve().parents[1])).resolve()
        patch_root = os.environ.get("KANDA_PATCH_EXTRACT_ROOT")
        report = build_final_integration_hardening_report(
            project_root=project_root,
            patch_extract_root=patch_root,
        )
        self.assertEqual(report.status, "integration_hardening_pass", report.to_dict())
        self.assertFalse(report.blockers, report.to_dict())
        self.assertLessEqual(report.line_counts.get("workbench_gui.py", 9999), 500)
        self.assertIn("workbench_import_rewrite_apply_executor.py", report.line_counts)
        self.assertIn("workbench_import_rewrite_rollback_executor.py", report.line_counts)

    def test_required_exports_are_available(self) -> None:
        """Compatibility names must remain available for lazy GUI import chains."""
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (  # noqa: PLC0415
            build_final_integration_hardening_report,
            execute_guarded_import_rewrite_apply,
            execute_import_rewrite_rollback,
        )
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator import (  # noqa: PLC0415
            PostApplyValidationResult,
            WorkbenchPostApplyValidationResult,
        )
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_guarded_apply_formatting import (  # noqa: PLC0415
            format_post_apply_validation,
        )
        self.assertTrue(callable(build_final_integration_hardening_report))
        self.assertTrue(callable(execute_guarded_import_rewrite_apply))
        self.assertTrue(callable(execute_import_rewrite_rollback))
        self.assertIs(PostApplyValidationResult, WorkbenchPostApplyValidationResult)
        self.assertTrue(callable(format_post_apply_validation))


if __name__ == "__main__":
    unittest.main(verbosity=2)
