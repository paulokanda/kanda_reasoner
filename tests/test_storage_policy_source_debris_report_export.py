"""Tests for report-only source debris report/export helpers."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "source_debris_report_export.py"
)


class StoragePolicySourceDebrisReportExportTests(unittest.TestCase):
    """Validate report-only source debris report/export behavior."""

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.source_debris_report_export"
        )
        expected = {
            "SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT",
            "SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE",
            "SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION",
            "SOURCE_DEBRIS_REPORT_ACTION",
            "SOURCE_DEBRIS_REPORT_SCHEMA_VERSION",
            "SourceDebrisExportPlan",
            "SourceDebrisReportItem",
            "build_source_debris_report_export",
            "render_source_debris_report_json",
            "render_source_debris_report_text",
            "write_source_debris_report_json",
            "write_source_debris_report_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_import_does_not_scan_live_tree(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.source_debris_report_export"
        )
        self.assertEqual(module.SOURCE_DEBRIS_REPORT_ACTION, "report_only")

    def test_clean_tree_has_empty_plan(self) -> None:
        from kanda_reasoner_app.storage_policy.source_debris_report_export import (
            build_source_debris_report_export,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "app.py").write_text("print('ok')\n", encoding="utf-8")

            plan = build_source_debris_report_export(root)

        self.assertTrue(plan.is_empty())
        self.assertEqual(plan.total_items, 0)
        self.assertEqual(plan.total_failures, 0)
        self.assertEqual(plan.total_warnings, 0)

    def test_debris_items_are_classified_by_destination(self) -> None:
        from kanda_reasoner_app.storage_policy.source_debris_report_export import (
            SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT,
            SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE,
            SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION,
            build_source_debris_report_export,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "module.py.bak").write_text("old\n", encoding="utf-8")
            evidence = root / "project_analysis_evidence"
            evidence.mkdir()
            (evidence / "sample__complete.json").write_text("{}\n", encoding="utf-8")
            workbench = root / "workbench"
            workbench.mkdir()
            (workbench / "note.txt").write_text("dev\n", encoding="utf-8")

            plan = build_source_debris_report_export(root)

        destinations = {item.recommended_destination for item in plan.items}
        self.assertIn(SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE, destinations)
        self.assertIn(SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT, destinations)
        self.assertIn(SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION, destinations)
        self.assertGreaterEqual(plan.total_failures, 2)
        self.assertGreaterEqual(plan.total_warnings, 1)

    def test_json_render_is_stable_and_serializable(self) -> None:
        from kanda_reasoner_app.storage_policy.source_debris_report_export import (
            build_source_debris_report_export,
            render_source_debris_report_json,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "module.py.backup").write_text("old\n", encoding="utf-8")

            plan = build_source_debris_report_export(root)
            payload = json.loads(render_source_debris_report_json(plan))

        self.assertEqual(payload["action"], "report_only")
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["total_items"], 1)
        self.assertEqual(len(payload["items"]), 1)

    def test_text_summary_contains_counts(self) -> None:
        from kanda_reasoner_app.storage_policy.source_debris_report_export import (
            build_source_debris_report_export,
            render_source_debris_report_text,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "module_old.py").write_text("old\n", encoding="utf-8")
            plan = build_source_debris_report_export(root)
            text = render_source_debris_report_text(plan)

        self.assertIn("Kanda Reasoner source debris report/export", text)
        self.assertIn("Items: 1", text)
        self.assertIn("Maintenance quarantine items: 1", text)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        from kanda_reasoner_app.storage_policy.source_debris_report_export import (
            build_source_debris_report_export,
            write_source_debris_report_json,
            write_source_debris_report_text,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "module.py.bak").write_text("old\n", encoding="utf-8")
            plan = build_source_debris_report_export(root)

            text_path = root / "report.txt"
            json_path = root / "report.json"

            write_source_debris_report_text(plan, text_path)
            write_source_debris_report_json(plan, json_path)

            with self.assertRaises(FileExistsError):
                write_source_debris_report_text(plan, text_path)

            write_source_debris_report_text(plan, text_path, overwrite=True)

            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())

    def test_write_rejects_missing_parent(self) -> None:
        from kanda_reasoner_app.storage_policy.source_debris_report_export import (
            build_source_debris_report_export,
            write_source_debris_report_json,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plan = build_source_debris_report_export(root)
            output_path = root / "missing" / "report.json"

            with self.assertRaises(ValueError):
                write_source_debris_report_json(plan, output_path)

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = MODULE_PATH.read_text(encoding="utf-8")
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "E:\\\\",
            "kanda_reasoner_architecture_audit",
            "_kanda_reasoner_temp",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
