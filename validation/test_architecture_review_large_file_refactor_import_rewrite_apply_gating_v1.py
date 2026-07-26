# project-path: validation/test_architecture_review_large_file_refactor_import_rewrite_apply_gating_v1.py
"""Focused tests for import rewrite apply gating v1."""
from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ImportMigrationPreview,
    ImportMigrationRecord,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_apply_readiness import (
    build_and_write_import_rewrite_apply_readiness,
    expected_import_rewrite_apply_token,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_apply_formatting import (
    format_import_rewrite_apply_readiness,
)


class ImportRewriteApplyGatingTests(unittest.TestCase):
    """Validate no-write import rewrite apply readiness."""

    def test_noop_records_write_manifest_and_keep_apply_disabled(self) -> None:
        """Facade-owned imports are no-op readiness records, not rewrites."""
        with tempfile.TemporaryDirectory() as temp:
            root, target, preview = _project_paths(temp)
            preview_data = _preview(target, [_record(root / "consumer.py", ["FROM_IMPORT_REVIEW"])])
            token = expected_import_rewrite_apply_token(preview_data)
            result = build_and_write_import_rewrite_apply_readiness(
                preview_data,
                active_project_root=str(root),
                preview_root=str(preview),
                exact_token=token,
            )
            self.assertEqual(result.status, "import_rewrite_apply_ready_for_future_train")
            self.assertFalse(result.rewrite_enabled)
            self.assertFalse(result.apply_enabled)
            self.assertTrue(result.exact_token_valid)
            self.assertEqual(result.no_op_importer_count, 1)
            self.assertEqual(result.manual_review_count, 0)
            self.assertTrue(Path(result.readiness_manifest_path).exists())
            self.assertTrue(Path(result.diff_preview_path).exists())
            self.assertIn("NO WRITE", Path(result.diff_preview_path).read_text(encoding="utf-8"))
            self.assertIn("Apply enabled: False", format_import_rewrite_apply_readiness(result))

    def test_risky_records_remain_manual_review_and_no_apply(self) -> None:
        """Star/relative/dynamic/string risks stay manual-review records."""
        with tempfile.TemporaryDirectory() as temp:
            root, target, preview = _project_paths(temp)
            preview_data = _preview(
                target,
                [
                    _record(root / "star.py", ["STAR_IMPORT_RISK"]),
                    _record(root / "dynamic.py", ["DYNAMIC_IMPORT_RISK", "STRING_REFERENCE_RISK"]),
                ],
            )
            result = build_and_write_import_rewrite_apply_readiness(
                preview_data,
                active_project_root=str(root),
                preview_root=str(preview),
            )
            self.assertEqual(result.manual_review_count, 2)
            self.assertFalse(result.rewrite_enabled)
            self.assertFalse(result.apply_enabled)
            self.assertIn("IMPORT_REWRITE_MANUAL_REVIEW_RECORD_PRESENT", result.warnings)

    def test_project_source_preview_root_blocks(self) -> None:
        """Readiness artifacts must not be written inside project source."""
        with tempfile.TemporaryDirectory() as temp:
            root, target, _preview = _project_paths(temp)
            unsafe_preview = root / "large_file_refactor_preview"
            preview_data = _preview_for_target(target)
            result = build_and_write_import_rewrite_apply_readiness(
                preview_data,
                active_project_root=str(root),
                preview_root=str(unsafe_preview),
            )
            self.assertEqual(result.status, "blocked")
            self.assertIn("PREVIEW_ROOT_OUTSIDE_DAILY_WORK", result.blockers)
            self.assertIn("PREVIEW_ROOT_INSIDE_PROJECT_SOURCE", result.blockers)


def _project_paths(temp: str) -> tuple[Path, Path, Path]:
    """Create a tiny project and daily-work preview root."""
    root = Path(temp) / "demo_project"
    root.mkdir()
    target = root / "module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    (root / "consumer.py").write_text("from module import VALUE\n", encoding="utf-8")
    preview = root.parent / "demo_project_delete_after_daily_work" / "large_file_refactor_preview"
    return root, target, preview


def _preview_for_target(target: Path) -> ImportMigrationPreview:
    """Return a preview with one no-op record."""
    return _preview(target, [_record(target.parent / "consumer.py", ["FROM_IMPORT_REVIEW"])])


def _preview(target: Path, records: list[ImportMigrationRecord]) -> ImportMigrationPreview:
    """Build import migration preview test data."""
    return ImportMigrationPreview(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=hashlib.sha256(target.read_bytes()).hexdigest(),
        rewrite_enabled=False,
        records=records,
        blockers=[],
        warnings=["IMPORT_MIGRATION_PREVIEW_ONLY_NO_REWRITE"],
        status="preview_only",
    )


def _record(importer: Path, flags: list[str]) -> ImportMigrationRecord:
    """Build one preview-only import migration record."""
    return ImportMigrationRecord(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        importer_file=str(importer),
        original_import="from module import VALUE",
        suggested_import="keep facade from-import",
        action="review_only_no_rewrite",
        reason="preview only",
        status="preview_only",
        blockers=[],
        risk_flags=flags,
    )


if __name__ == "__main__":
    unittest.main()
