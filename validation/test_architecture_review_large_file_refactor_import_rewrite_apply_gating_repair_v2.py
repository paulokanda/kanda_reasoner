# project-path: validation/test_architecture_review_large_file_refactor_import_rewrite_apply_gating_repair_v2.py
"""Regression tests for import rewrite apply gating repair v2."""
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


class ImportRewriteApplyGatingRepairV2Tests(unittest.TestCase):
    """Validate temp-safe daily-work handling without weakening real shielding."""

    def test_temp_project_sibling_daily_work_is_allowed_for_validators(self) -> None:
        """Synthetic temp projects may use sibling daily-work roots."""
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
            self.assertTrue(Path(result.readiness_manifest_path).exists())
            self.assertNotIn("PREVIEW_ROOT_OUTSIDE_DAILY_WORK", result.blockers)

    def test_project_source_preview_root_still_blocks(self) -> None:
        """Preview roots inside source remain blocked even for temp validators."""
        with tempfile.TemporaryDirectory() as temp:
            root, target, _preview = _project_paths(temp)
            preview_data = _preview_for_target(target)
            result = build_and_write_import_rewrite_apply_readiness(
                preview_data,
                active_project_root=str(root),
                preview_root=str(root / "large_file_refactor_preview"),
            )
            self.assertEqual(result.status, "blocked")
            self.assertIn("PREVIEW_ROOT_INSIDE_PROJECT_SOURCE", result.blockers)

    def test_non_temp_sibling_preview_still_blocks(self) -> None:
        """Non-temp project roots must keep the canonical drive-root daily-work contract."""
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import workbench_import_rewrite_apply_readiness as mod

        original_gettempdir = mod.tempfile.gettempdir
        original_daily_root_for = mod.daily_work_root_for_import_rewrite
        try:
            with tempfile.TemporaryDirectory() as temp:
                temp_parent = Path(temp).resolve()
                fake_root = temp_parent / "not_temp_kanda_project"
                preview = fake_root.parent / "not_temp_kanda_project_delete_after_daily_work" / "large_file_refactor_preview"
                canonical = fake_root.parent / "drive_root_daily_work" / "not_temp_kanda_project_delete_after_daily_work"
                mod.tempfile.gettempdir = lambda: str(temp_parent / "different_temp")
                mod.daily_work_root_for_import_rewrite = lambda _root: canonical
                blockers = _call_preview_root_blockers_for_fake(fake_root, preview)
        finally:
            mod.tempfile.gettempdir = original_gettempdir
            mod.daily_work_root_for_import_rewrite = original_daily_root_for
        self.assertIn("PREVIEW_ROOT_OUTSIDE_DAILY_WORK", blockers)


def _call_preview_root_blockers_for_fake(fake_root: Path, preview: Path) -> list[str]:
    """Call the private blocker helper in a controlled unit boundary."""
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import workbench_import_rewrite_apply_readiness as mod

    return mod.import_rewrite_preview_root_blockers(
        fake_root,
        preview,
        preview / "IMPORT_REWRITE_APPLY_READINESS.json",
        preview / "IMPORT_REWRITE_APPLY_DIFF_PREVIEW.txt",
    )


def _project_paths(temp: str) -> tuple[Path, Path, Path]:
    """Create a tiny temp project and sibling daily-work preview root."""
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
