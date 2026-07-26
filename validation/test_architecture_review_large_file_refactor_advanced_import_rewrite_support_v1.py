# project-path: validation/test_architecture_review_large_file_refactor_advanced_import_rewrite_support_v1.py
"""Tests for advanced import rewrite support evidence."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_import_rewrite_support import (
    build_advanced_import_rewrite_support,
    write_advanced_import_rewrite_support,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    ImportMigrationPreview,
    ImportMigrationRecord,
    SCHEMA_VERSION,
)


class AdvancedImportRewriteSupportTests(unittest.TestCase):
    """Validate no-write advanced import rewrite support."""

    def _preview(self, root: Path, records: list[ImportMigrationRecord]) -> ImportMigrationPreview:
        target = root / "pkg" / "target.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("def moved():\n    return 1\n", encoding="utf-8")
        return ImportMigrationPreview(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            target_file=str(target),
            source_content_hash="abc123",
            rewrite_enabled=False,
            records=records,
            blockers=[],
            warnings=[],
            status="preview_only",
        )

    def _record(self, root: Path, original: str, suggested: str, *, action: str, risks=None) -> ImportMigrationRecord:
        importer = root / "pkg" / "consumer.py"
        importer.parent.mkdir(parents=True, exist_ok=True)
        importer.write_text(original + "\n", encoding="utf-8")
        return ImportMigrationRecord(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            importer_file=str(importer),
            original_import=original,
            suggested_import=suggested,
            action=action,
            reason="test",
            status="preview_only" if action != "rewrite_import" else "rewrite_ready",
            blockers=[],
            risk_flags=list(risks or []),
        )

    def test_alias_and_multi_imports_are_supported_without_apply(self) -> None:
        """Alias and multi-name imports are recognized but not applied."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            preview_root = Path(tmp) / "project_delete_after_daily_work" / "large_file_refactor_preview"
            record = self._record(root, "from pkg.target import moved as alias, other", "keep facade", action="review_only_no_rewrite")
            result = build_advanced_import_rewrite_support(
                self._preview(root, [record]), active_project_root=str(root), preview_root=str(preview_root)
            )
            self.assertEqual(result.status, "advanced_import_rewrite_support_ready")
            self.assertFalse(result.apply_enabled)
            self.assertFalse(result.rewrite_enabled)
            self.assertEqual(result.alias_supported_count, 1)
            self.assertEqual(result.multi_name_supported_count, 1)
            write_advanced_import_rewrite_support(result)
            self.assertTrue(Path(result.manifest_path).exists())

    def test_future_safe_rewrite_requires_alias_preservation(self) -> None:
        """Future rewrite records must preserve aliases to be supported."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            safe = self._record(
                root,
                "from pkg.target import moved as alias",
                "from pkg.target_helpers import moved as alias",
                action="rewrite_import",
            )
            unsafe = self._record(
                root,
                "from pkg.target import moved as alias",
                "from pkg.target_helpers import moved",
                action="rewrite_import",
            )
            result = build_advanced_import_rewrite_support(
                self._preview(root, [safe, unsafe]), active_project_root=str(root)
            )
            statuses = [item["status"] for item in result.records]
            self.assertIn("future_safe_rewrite_supported", statuses)
            self.assertIn("manual_review_required", statuses)
            self.assertEqual(result.future_safe_rewrite_count, 1)

    def test_risky_records_remain_manual_review(self) -> None:
        """Star/relative/dynamic/string/patch-risk records are never auto-supported."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            record = self._record(
                root,
                "from pkg.target import *",
                "from pkg.target_helpers import *",
                action="rewrite_import",
                risks=["STAR_IMPORT_RISK"],
            )
            result = build_advanced_import_rewrite_support(self._preview(root, [record]), active_project_root=str(root))
            self.assertEqual(result.records[0]["status"], "manual_review_required")
            self.assertEqual(result.manual_review_count, 1)


if __name__ == "__main__":
    unittest.main()
