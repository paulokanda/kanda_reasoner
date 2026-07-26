# project-path: validation/test_architecture_review_large_file_refactor_post_apply_compatibility_repair_v1.py
"""Focused validation for Workbench post-apply compatibility repair."""
from __future__ import annotations

import dataclasses
import py_compile
from pathlib import Path
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator import (
    POST_APPLY_VALIDATION_FEATURE_ID,
    PostApplyValidationResult,
    validate_and_write_post_apply,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_guarded_apply_formatting import (
    format_post_apply_validation,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_behavior_validation import (
    run_workbench_behavior_validation,
)


class PostApplyCompatibilityRepairTests(unittest.TestCase):
    """Validate the compatibility symbol required by the GUI import chain."""

    def test_post_apply_result_export_is_available(self) -> None:
        """The result dataclass must remain importable for dependent modules."""
        self.assertTrue(dataclasses.is_dataclass(PostApplyValidationResult))
        fields = {field.name for field in dataclasses.fields(PostApplyValidationResult)}
        self.assertIn("structural_status", fields)
        self.assertIn("behavior_status", fields)
        self.assertIn("checked_files", fields)
        self.assertTrue(callable(validate_and_write_post_apply))
        self.assertTrue(callable(format_post_apply_validation))
        self.assertTrue(callable(run_workbench_behavior_validation))
        self.assertEqual(
            POST_APPLY_VALIDATION_FEATURE_ID,
            "architecture-review-large-file-refactor-post-apply-validation-v1",
        )

    def test_changed_modules_compile_and_stay_under_size_cap(self) -> None:
        """The repaired module must compile and remain under the 500-line cap."""
        project_root = Path(__file__).resolve().parents[1]
        files = [
            project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_validator.py",
            project_root / "validation/test_architecture_review_large_file_refactor_post_apply_compatibility_repair_v1.py",
            project_root / "tools/validate_architecture_review_large_file_refactor_post_apply_compatibility_repair_v1.py",
        ]
        for path in files:
            self.assertTrue(path.is_file(), str(path))
            py_compile.compile(str(path), doraise=True)
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(line_count, 500, str(path))


if __name__ == "__main__":
    unittest.main()
