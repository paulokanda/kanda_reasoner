# project-path: validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_repair_v2.py
"""Regression checks for import rewrite rollback visibility repair v2."""
from __future__ import annotations

import importlib
import py_compile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ImportRewriteRollbackVisibilityRepairV2Tests(unittest.TestCase):
    """Validate rollback visibility modules and script-path repair assumptions."""

    def test_required_modules_import(self) -> None:
        modules = [
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_rollback_executor",
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_rollback_formatting",
        ]
        for module_name in modules:
            with self.subTest(module_name=module_name):
                importlib.import_module(module_name)

    def test_required_exports_exist(self) -> None:
        executor = importlib.import_module(
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_rollback_executor"
        )
        self.assertTrue(hasattr(executor, "execute_import_rewrite_rollback"))
        self.assertTrue(hasattr(executor, "expected_import_rewrite_rollback_token"))
        formatter = importlib.import_module(
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_rollback_formatting"
        )
        self.assertTrue(hasattr(formatter, "format_import_rewrite_rollback_result"))

    def test_v1_and_v2_validators_exist_and_compile(self) -> None:
        paths = [
            ROOT / "tools/validate_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py",
            ROOT / "tools/validate_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_repair_v2.py",
            ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py",
            ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_repair_v2.py",
        ]
        for path in paths:
            with self.subTest(path=str(path)):
                self.assertTrue(path.exists(), str(path))
                py_compile.compile(str(path), doraise=True)


if __name__ == "__main__":
    unittest.main()
