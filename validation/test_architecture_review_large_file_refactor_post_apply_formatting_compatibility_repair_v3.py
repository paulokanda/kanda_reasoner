# project-path: validation/test_architecture_review_large_file_refactor_post_apply_formatting_compatibility_repair_v3.py
"""Focused validation for Workbench post-apply formatting compatibility repair v3."""
from __future__ import annotations

import dataclasses
import importlib
import importlib.util
import py_compile
from pathlib import Path
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_guarded_apply_formatting import (
    format_guarded_source_apply,
    format_post_apply_validation,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator import (
    POST_APPLY_VALIDATION_FEATURE_ID,
    PostApplyValidationResult,
    WorkbenchPostApplyValidationResult,
    validate_and_write_post_apply,
)


class PostApplyFormattingCompatibilityRepairV3Tests(unittest.TestCase):
    """Validate stable Workbench post-apply compatibility exports."""

    def test_post_apply_result_names_and_formatter_are_available(self) -> None:
        """Both result aliases and the GUI formatter must be importable."""
        self.assertIs(WorkbenchPostApplyValidationResult, PostApplyValidationResult)
        self.assertTrue(dataclasses.is_dataclass(PostApplyValidationResult))
        self.assertTrue(callable(validate_and_write_post_apply))
        self.assertTrue(callable(format_guarded_source_apply))
        self.assertTrue(callable(format_post_apply_validation))
        self.assertEqual(
            POST_APPLY_VALIDATION_FEATURE_ID,
            "architecture-review-large-file-refactor-post-apply-validation-v1",
        )

    def test_formatter_accepts_post_apply_result(self) -> None:
        """format_post_apply_validation must handle the exported result dataclass."""
        result = WorkbenchPostApplyValidationResult(
            schema_version="1.0",
            feature_id=POST_APPLY_VALIDATION_FEATURE_ID,
            status="post_apply_validated",
            structural_status="STRUCTURAL_PASS_WITH_WARNINGS",
            behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
            target_file="example.py",
            preview_root="daily/preview",
            report_path="daily/preview/SOURCE_APPLY_POST_APPLY_VALIDATION.json",
            rollback_manifest_path="daily/preview/SOURCE_APPLY_ROLLBACK_MANIFEST.json",
            checked_files=["example.py"],
            blockers=[],
            warnings=["STRUCTURAL_VALIDATION_ONLY"],
            checked_rules=["formatting_compatibility"],
        )
        formatted = format_post_apply_validation(result)
        self.assertIn("Post-Apply Validation", formatted)
        self.assertIn("STRUCTURAL_PASS_WITH_WARNINGS", formatted)
        self.assertIn("BEHAVIOR_VALIDATION_NOT_RUN", formatted)
        self.assertIn("example.py", formatted)

    def test_dependent_non_gui_import_chains_load(self) -> None:
        """Dependent non-GUI Workbench modules must import after repair."""
        module_names = [
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_guarded_apply_formatting",
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_behavior_validation",
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator",
        ]
        for module_name in module_names:
            module = importlib.import_module(module_name)
            self.assertIsNotNone(module)

    def test_gui_import_chain_when_pyside_is_available(self) -> None:
        """Import the full GUI chain when local GUI dependencies are installed."""
        if importlib.util.find_spec("PySide6") is None:
            self.skipTest("PySide6 not available in this validation runtime")
        module = importlib.import_module("kanda_reasoner_app.manage_architecture.manage_architecture_gui")
        self.assertIsNotNone(module)

    def test_workbench_gui_references_stable_formatter_export(self) -> None:
        """The Workbench GUI source must import the stable post-apply formatter name."""
        project_root = Path(__file__).resolve().parents[1]
        gui_path = project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui.py"
        self.assertTrue(gui_path.is_file(), str(gui_path))
        gui_text = gui_path.read_text(encoding="utf-8", errors="replace")
        self.assertIn("format_post_apply_validation", gui_text)
        self.assertIn("workbench_guarded_apply_formatting", gui_text)

    def test_changed_modules_compile_and_stay_under_size_cap(self) -> None:
        """Changed modules and validators must compile and stay below 500 lines."""
        project_root = Path(__file__).resolve().parents[1]
        files = [
            project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_validator.py",
            project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_guarded_apply_formatting.py",
            project_root / "validation/test_architecture_review_large_file_refactor_post_apply_formatting_compatibility_repair_v3.py",
            project_root / "tools/validate_architecture_review_large_file_refactor_post_apply_formatting_compatibility_repair_v3.py",
        ]
        for path in files:
            self.assertTrue(path.is_file(), str(path))
            py_compile.compile(str(path), doraise=True)
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLessEqual(line_count, 500, str(path))


if __name__ == "__main__":
    unittest.main()
