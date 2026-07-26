# project-path: validation/test_architecture_review_large_file_refactor_import_rewrite_guarded_apply_v1.py
"""Focused validation for guarded import rewrite apply v1."""
from __future__ import annotations

import json
import py_compile
import shutil
import tempfile
from pathlib import Path
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_apply_executor import (
    execute_guarded_import_rewrite_apply,
    expected_guarded_import_rewrite_apply_token,
)


class ImportRewriteGuardedApplyTests(unittest.TestCase):
    """Validate exact-token import rewrite application gates."""

    def setUp(self) -> None:
        self.temp_root = Path(tempfile.mkdtemp(prefix="kanda_import_rewrite_apply_"))
        self.project_root = self.temp_root / "proj"
        self.project_root.mkdir()
        self.preview_root = self.temp_root / "proj_delete_after_daily_work" / "large_file_refactor_preview"
        self.preview_root.mkdir(parents=True)
        self.importer = self.project_root / "consumer.py"
        self.importer.write_text("from old_module import Foo\n\nprint(Foo)\n", encoding="utf-8")
        self.readiness = {
            "schema_version": "1.0",
            "feature_id": "architecture-review-large-file-refactor-import-rewrite-apply-gating-v1",
            "status": "import_rewrite_apply_ready_for_future_train",
            "target_file": str(self.project_root / "old_module.py"),
            "source_content_hash": "hash",
            "preview_root": str(self.preview_root),
            "readiness_manifest_path": str(self.preview_root / "IMPORT_REWRITE_APPLY_READINESS.json"),
            "diff_preview_path": str(self.preview_root / "IMPORT_REWRITE_APPLY_DIFF_PREVIEW.txt"),
            "exact_token_required": "KANDA-IMPORT-REWRITE-TESTTOKEN",
            "exact_token_present": True,
            "exact_token_valid": True,
            "rewrite_enabled": False,
            "apply_enabled": False,
            "blockers": [],
            "warnings": [],
            "rewrite_plan": [
                {
                    "importer_file": str(self.importer),
                    "importer_relative": "consumer.py",
                    "original_import": "from old_module import Foo",
                    "suggested_import": "from old_module_parts import Foo",
                    "action": "rewrite_import",
                    "status": "safe_rewrite_ready",
                    "risk_flags": [],
                    "reason": "safe synthetic rewrite",
                }
            ],
        }

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_root, ignore_errors=True)

    def test_wrong_token_blocks_without_writing(self) -> None:
        """Missing/wrong exact token must block importer mutation."""
        result = execute_guarded_import_rewrite_apply(
            self.readiness,
            active_project_root=str(self.project_root),
            preview_root=str(self.preview_root),
            exact_token="wrong",
        )
        self.assertEqual(result.status, "import_rewrite_apply_blocked")
        self.assertIn("EXACT_IMPORT_REWRITE_APPLY_TOKEN_REQUIRED", result.blockers)
        self.assertIn("from old_module import Foo", self.importer.read_text(encoding="utf-8"))

    def test_safe_record_rewrites_and_writes_rollback_and_post_apply(self) -> None:
        """Safe records may rewrite after exact token and must create recovery evidence."""
        token = expected_guarded_import_rewrite_apply_token(self.readiness)
        result = execute_guarded_import_rewrite_apply(
            self.readiness,
            active_project_root=str(self.project_root),
            preview_root=str(self.preview_root),
            exact_token=token,
        )
        self.assertEqual(result.status, "import_rewrite_apply_applied")
        self.assertEqual(result.validation_status, "IMPORT_REWRITE_STRUCTURAL_PASS")
        self.assertIn("from old_module_parts import Foo", self.importer.read_text(encoding="utf-8"))
        self.assertTrue((self.preview_root / "IMPORT_REWRITE_ROLLBACK_MANIFEST.json").is_file())
        self.assertTrue((self.preview_root / "IMPORT_REWRITE_POST_APPLY_VALIDATION.json").is_file())

    def test_manual_review_records_are_not_rewritten(self) -> None:
        """Risky records remain manual-review evidence and are not rewritten."""
        self.readiness["rewrite_plan"][0]["risk_flags"] = ["STAR_IMPORT_RISK"]
        token = expected_guarded_import_rewrite_apply_token(self.readiness)
        result = execute_guarded_import_rewrite_apply(
            self.readiness,
            active_project_root=str(self.project_root),
            preview_root=str(self.preview_root),
            exact_token=token,
        )
        self.assertEqual(result.status, "import_rewrite_apply_no_safe_rewrites")
        self.assertTrue(result.manual_review_records)
        self.assertIn("from old_module import Foo", self.importer.read_text(encoding="utf-8"))

    def test_changed_modules_compile_and_stay_under_size_cap(self) -> None:
        """Changed modules and validation files must compile and remain under 500 lines."""
        project_root = Path(__file__).resolve().parents[1]
        files = [
            project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_executor.py",
            Path(__file__),
            project_root / "tools/validate_architecture_review_large_file_refactor_import_rewrite_guarded_apply_v1.py",
        ]
        for path in files:
            self.assertTrue(path.is_file(), str(path))
            py_compile.compile(str(path), doraise=True)
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 500, str(path))


if __name__ == "__main__":
    unittest.main()
