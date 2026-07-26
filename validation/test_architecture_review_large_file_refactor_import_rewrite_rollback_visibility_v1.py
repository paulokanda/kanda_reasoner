# project-path: validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py
"""Focused tests for import rewrite rollback visibility."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_rollback_executor import (
    execute_import_rewrite_rollback,
    expected_import_rewrite_rollback_token,
)


class ImportRewriteRollbackVisibilityTests(unittest.TestCase):
    """Validate exact-token import rewrite rollback behavior."""

    def _project(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path]:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name) / "sample_project"
        source = root / "pkg" / "consumer.py"
        preview = root.parent / "sample_project_delete_after_daily_work" / "large_file_refactor_preview"
        backup_dir = preview / "import_rewrite_backups"
        source.parent.mkdir(parents=True)
        backup_dir.mkdir(parents=True)
        source.write_text("from pkg.new_home import alpha\n\nprint(alpha)\n", encoding="utf-8")
        backup = backup_dir / "consumer.bak"
        backup.write_text("from pkg.old_home import alpha\n\nprint(alpha)\n", encoding="utf-8")
        manifest = {
            "schema_version": "1.0",
            "feature_id": "architecture-review-large-file-refactor-import-rewrite-guarded-apply-v1",
            "status": "rollback_ready",
            "entries": [{
                "file": str(source.resolve()),
                "backup_file": str(backup.resolve()),
                "before_hash": self._sha(backup.read_text(encoding="utf-8")),
                "after_hash": self._sha(source.read_text(encoding="utf-8")),
            }],
        }
        (preview / "IMPORT_REWRITE_ROLLBACK_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return tmp, root, preview, source

    def test_token_required_blocks_rollback(self) -> None:
        """Rollback must not run without the exact rollback token."""
        tmp, root, preview, source = self._project()
        self.addCleanup(tmp.cleanup)
        result = execute_import_rewrite_rollback(
            active_project_root=str(root),
            preview_root=str(preview),
            exact_token="",
        )
        self.assertEqual(result.status, "import_rewrite_rollback_blocked")
        self.assertIn("EXACT_IMPORT_REWRITE_ROLLBACK_TOKEN_REQUIRED", result.blockers)
        self.assertIn("new_home", source.read_text(encoding="utf-8"))

    def test_successful_rollback_restores_importer(self) -> None:
        """Exact rollback token restores the importer from backup."""
        tmp, root, preview, source = self._project()
        self.addCleanup(tmp.cleanup)
        token = expected_import_rewrite_rollback_token(preview_root=str(preview))
        result = execute_import_rewrite_rollback(
            active_project_root=str(root),
            preview_root=str(preview),
            exact_token=token,
        )
        self.assertEqual(result.status, "import_rewrite_rollback_completed")
        self.assertEqual(result.validation_status, "IMPORT_REWRITE_ROLLBACK_STRUCTURAL_PASS")
        self.assertIn("old_home", source.read_text(encoding="utf-8"))
        self.assertTrue((preview / "IMPORT_REWRITE_ROLLBACK_EXECUTION.json").exists())

    def test_changed_importer_is_retained_for_manual_review(self) -> None:
        """Changed importers are not overwritten during rollback."""
        tmp, root, preview, source = self._project()
        self.addCleanup(tmp.cleanup)
        source.write_text("from pkg.new_home import beta\n", encoding="utf-8")
        token = expected_import_rewrite_rollback_token(preview_root=str(preview))
        result = execute_import_rewrite_rollback(
            active_project_root=str(root),
            preview_root=str(preview),
            exact_token=token,
        )
        self.assertEqual(result.status, "import_rewrite_rollback_blocked")
        self.assertIn("IMPORT_REWRITE_ROLLBACK_RETAINED_CHANGED_FILES_FOR_MANUAL_REVIEW", result.warnings)
        self.assertIn("beta", source.read_text(encoding="utf-8"))

    @staticmethod
    def _sha(text: str) -> str:
        """Return SHA-256 for text."""
        import hashlib

        return hashlib.sha256(text.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    unittest.main()
