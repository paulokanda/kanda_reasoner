"""Tests for source debris quarantine report export."""

from __future__ import annotations

from datetime import datetime
import importlib
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.source_debris_quarantine_report_export import (
    SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_ACTION,
    SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_BASENAME,
    SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_FOLDER_NAME,
    SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_SCHEMA_VERSION,
    SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_TIMESTAMP_FORMAT,
    SourceDebrisQuarantineReportExportPaths,
    SourceDebrisQuarantineReportExportResult,
    build_source_debris_quarantine_report_export_paths,
    build_source_debris_quarantine_report_run_id,
    export_source_debris_quarantine_dry_run_report,
    render_source_debris_quarantine_report_export_json,
    render_source_debris_quarantine_report_export_text,
)
import kanda_reasoner_app.storage_policy.source_debris_quarantine_report_export as export_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "source_debris_quarantine_report_export.py"
)


class StoragePolicySourceDebrisQuarantineReportExportTests(unittest.TestCase):
    """Validate dry-run report export behavior."""

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.source_debris_quarantine_report_export"
        )
        expected = {
            "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_ACTION",
            "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_BASENAME",
            "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_FOLDER_NAME",
            "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_SCHEMA_VERSION",
            "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_TIMESTAMP_FORMAT",
            "SourceDebrisQuarantineReportExportPaths",
            "SourceDebrisQuarantineReportExportResult",
            "build_source_debris_quarantine_report_export_paths",
            "build_source_debris_quarantine_report_run_id",
            "export_source_debris_quarantine_dry_run_report",
            "render_source_debris_quarantine_report_export_json",
            "render_source_debris_quarantine_report_export_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_import_does_not_export_or_create_live_tree(self) -> None:
        self.assertEqual(
            export_module.SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_ACTION,
            "export_dry_run_report_only",
        )

    def test_run_id_builder_is_stable_with_injected_datetime(self) -> None:
        run_id = build_source_debris_quarantine_report_run_id(
            datetime(2026, 6, 9, 12, 34, 56),
        )
        self.assertEqual(run_id, "20260609_123456")
        self.assertEqual(
            SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_TIMESTAMP_FORMAT,
            "%Y%m%d_%H%M%S",
        )

    def test_paths_are_canonical_without_creating_folders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            maintenance_root = Path(temp_dir) / "maintenance"
            paths = build_source_debris_quarantine_report_export_paths(
                root,
                maintenance_root=maintenance_root,
                run_id="20260609_123456",
            )

            self.assertIsInstance(paths, SourceDebrisQuarantineReportExportPaths)
            self.assertEqual(paths.project_slug, "sample_project")
            self.assertIn("logs", paths.output_root)
            self.assertIn("audit", paths.output_root)
            self.assertIn(SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_FOLDER_NAME, paths.output_root)
            self.assertTrue(paths.text_path.endswith(".txt"))
            self.assertTrue(paths.json_path.endswith(".json"))
            self.assertFalse(Path(paths.output_root).exists())

    def test_export_writes_text_and_json_only_when_called(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py.bak").write_text("old\n", encoding="utf-8")
            maintenance_root = Path(temp_dir) / "maintenance"

            result = export_source_debris_quarantine_dry_run_report(
                root,
                maintenance_root=maintenance_root,
                run_id="20260609_123456",
            )

            self.assertIsInstance(result, SourceDebrisQuarantineReportExportResult)
            text_path = Path(result.text_path)
            json_path = Path(result.json_path)
            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())
            self.assertEqual(result.total_items, 1)
            self.assertEqual(result.quarantine_review_items, 1)
            self.assertEqual(result.evidence_migration_review_items, 0)
            self.assertEqual(result.packaging_exclusion_review_items, 0)
            self.assertIn(SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_BASENAME, text_path.name)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["total_items"], 1)

    def test_export_respects_overwrite_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py.backup").write_text("old\n", encoding="utf-8")
            maintenance_root = Path(temp_dir) / "maintenance"

            export_source_debris_quarantine_dry_run_report(
                root,
                maintenance_root=maintenance_root,
                run_id="fixed_run",
            )

            with self.assertRaises(FileExistsError):
                export_source_debris_quarantine_dry_run_report(
                    root,
                    maintenance_root=maintenance_root,
                    run_id="fixed_run",
                )

            result = export_source_debris_quarantine_dry_run_report(
                root,
                maintenance_root=maintenance_root,
                run_id="fixed_run",
                overwrite=True,
            )

            self.assertTrue(Path(result.text_path).exists())
            self.assertTrue(Path(result.json_path).exists())

    def test_render_export_result_is_stable_and_serializable(self) -> None:
        result = SourceDebrisQuarantineReportExportResult(
            source_root="source",
            project_slug="sample_project",
            output_root="out",
            text_path="out/report.txt",
            json_path="out/report.json",
            run_id="run",
            plan_status="planned",
            total_items=3,
            quarantine_review_items=1,
            evidence_migration_review_items=1,
            packaging_exclusion_review_items=1,
        )

        text = render_source_debris_quarantine_report_export_text(result)
        payload = json.loads(render_source_debris_quarantine_report_export_json(result))

        self.assertIn("Kanda Reasoner source debris quarantine report export", text)
        self.assertEqual(payload["action"], SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_ACTION)
        self.assertEqual(payload["schema_version"], SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_SCHEMA_VERSION)
        self.assertEqual(payload["total_items"], 3)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = MODULE_SOURCE.read_text(encoding="utf-8")
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "C:\\",
            "C:/",
            "D:\\",
            "D:/",
            "_kanda_reasoner_temp",
            "kanda_reasoner_architecture_audit",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
