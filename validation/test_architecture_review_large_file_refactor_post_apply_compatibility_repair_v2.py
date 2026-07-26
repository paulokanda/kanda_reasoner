# project-path: validation/test_architecture_review_large_file_refactor_post_apply_compatibility_repair_v2.py
"""Focused validation for Workbench post-apply compatibility repair v2."""
from __future__ import annotations

import dataclasses
import importlib
import py_compile
from pathlib import Path
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator import (
    POST_APPLY_VALIDATION_FEATURE_ID,
    PostApplyValidationResult,
    WorkbenchPostApplyValidationResult,
    validate_and_write_post_apply,
)


class PostApplyCompatibilityRepairV2Tests(unittest.TestCase):
    """Validate both compatibility symbols required by Workbench import chains."""

    def test_both_result_export_names_are_available(self) -> None:
        """Both old and new result names must point to the same dataclass."""
        self.assertIs(WorkbenchPostApplyValidationResult, PostApplyValidationResult)
        self.assertTrue(dataclasses.is_dataclass(PostApplyValidationResult))
        fields = {field.name for field in dataclasses.fields(PostApplyValidationResult)}
        self.assertIn("structural_status", fields)
        self.assertIn("behavior_status", fields)
        self.assertIn("checked_files", fields)
        self.assertTrue(callable(validate_and_write_post_apply))
        self.assertEqual(
            POST_APPLY_VALIDATION_FEATURE_ID,
            "architecture-review-large-file-refactor-post-apply-validation-v1",
        )

    def test_dependent_workbench_import_chains_load(self) -> None:
        """Dependent modules must import after both result aliases are restored."""
        module_names = [
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_guarded_apply_formatting",
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_behavior_validation",
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator",
        ]
        for module_name in module_names:
            module = importlib.import_module(module_name)
            self.assertIsNotNone(module)

    def test_changed_modules_compile_and_stay_under_size_cap(self) -> None:
        """The repaired module and focused validators must compile under 500 lines."""
        project_root = Path(__file__).resolve().parents[1]
        files = [
            project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_validator.py",
            project_root / "validation/test_architecture_review_large_file_refactor_post_apply_compatibility_repair_v2.py",
            project_root / "tools/validate_architecture_review_large_file_refactor_post_apply_compatibility_repair_v2.py",
        ]
        for path in files:
            self.assertTrue(path.is_file(), str(path))
            py_compile.compile(str(path), doraise=True)
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(line_count, 500, str(path))


if __name__ == "__main__":
    unittest.main()
