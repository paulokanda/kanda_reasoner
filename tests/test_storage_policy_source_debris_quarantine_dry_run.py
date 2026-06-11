"""Tests for source debris quarantine dry-run planning."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run import (
    SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW,
    SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW,
    SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW,
    SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION,
    SOURCE_DEBRIS_QUARANTINE_STATUS_EMPTY,
    SOURCE_DEBRIS_QUARANTINE_STATUS_PLANNED,
    SourceDebrisQuarantineDryRunItem,
    SourceDebrisQuarantineDryRunPlan,
    build_source_debris_quarantine_dry_run,
    render_source_debris_quarantine_dry_run_json,
    render_source_debris_quarantine_dry_run_text,
    write_source_debris_quarantine_dry_run_json,
    write_source_debris_quarantine_dry_run_text,
)
import kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run as dry_run_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "source_debris_quarantine_dry_run.py"
)


class StoragePolicySourceDebrisQuarantineDryRunTests(unittest.TestCase):
    """Validate source debris quarantine dry-run behavior."""

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run"
        )
        expected = {
            "SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW",
            "SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW",
            "SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW",
            "SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION",
            "SOURCE_DEBRIS_QUARANTINE_DRY_RUN_SCHEMA_VERSION",
            "SOURCE_DEBRIS_QUARANTINE_STATUS_EMPTY",
            "SOURCE_DEBRIS_QUARANTINE_STATUS_PLANNED",
            "SourceDebrisQuarantineDryRunItem",
            "SourceDebrisQuarantineDryRunPlan",
            "build_source_debris_quarantine_dry_run",
            "build_source_debris_quarantine_dry_run_from_report",
            "render_source_debris_quarantine_dry_run_json",
            "render_source_debris_quarantine_dry_run_text",
            "write_source_debris_quarantine_dry_run_json",
            "write_source_debris_quarantine_dry_run_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_import_does_not_scan_or_create_live_tree(self) -> None:
        self.assertEqual(
            dry_run_module.SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION,
            "dry_run_only",
        )

    def test_clean_tree_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py").write_text("print('ok')\n", encoding="utf-8")

            plan = build_source_debris_quarantine_dry_run(root)

        self.assertIsInstance(plan, SourceDebrisQuarantineDryRunPlan)
        self.assertEqual(plan.action, SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION)
        self.assertEqual(plan.status(), SOURCE_DEBRIS_QUARANTINE_STATUS_EMPTY)
        self.assertEqual(plan.total_items, 0)

    def test_quarantine_items_get_planned_destination_under_maintenance_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py.bak").write_text("old\n", encoding="utf-8")
            maintenance_root = Path(temp_dir) / "maintenance"

            plan = build_source_debris_quarantine_dry_run(
                root,
                maintenance_root=maintenance_root,
            )

        self.assertEqual(plan.status(), SOURCE_DEBRIS_QUARANTINE_STATUS_PLANNED)
        self.assertEqual(plan.quarantine_review_items, 1)
        item = plan.items[0]
        self.assertIsInstance(item, SourceDebrisQuarantineDryRunItem)
        self.assertEqual(item.planned_operation, SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW)
        self.assertIn("quarantine", item.planned_destination_path)
        self.assertIn("sample_project", item.planned_destination_path)
        self.assertTrue(item.planned_destination_path.endswith("module.py.bak"))
        self.assertTrue(item.requires_human_review)

    def test_evidence_and_packaging_items_are_review_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            (evidence / "sample_project__complete.json").write_text(
                "{}\n",
                encoding="utf-8",
            )
            workbench = root / "workbench"
            workbench.mkdir()
            (workbench / "note.txt").write_text("dev\n", encoding="utf-8")
            audit_root = Path(temp_dir) / "sample_project_architecture_audit" / "current"

            plan = build_source_debris_quarantine_dry_run(root, audit_root=audit_root)

        operations = {item.planned_operation for item in plan.items}
        self.assertIn(SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW, operations)
        self.assertIn(SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW, operations)
        self.assertGreaterEqual(plan.evidence_migration_review_items, 1)
        self.assertGreaterEqual(plan.packaging_exclusion_review_items, 1)

    def test_json_render_is_stable_and_serializable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py.backup").write_text("old\n", encoding="utf-8")
            plan = build_source_debris_quarantine_dry_run(root)
            payload = json.loads(render_source_debris_quarantine_dry_run_json(plan))

        self.assertEqual(payload["action"], SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION)
        self.assertEqual(payload["status"], SOURCE_DEBRIS_QUARANTINE_STATUS_PLANNED)
        self.assertEqual(payload["total_items"], 1)
        self.assertEqual(len(payload["items"]), 1)

    def test_text_summary_contains_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module_old.py").write_text("old\n", encoding="utf-8")
            plan = build_source_debris_quarantine_dry_run(root)
            text = render_source_debris_quarantine_dry_run_text(plan)

        self.assertIn("Kanda Reasoner source debris quarantine dry-run report", text)
        self.assertIn("Action: dry_run_only", text)
        self.assertIn("Items: 1", text)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py.bak").write_text("old\n", encoding="utf-8")
            plan = build_source_debris_quarantine_dry_run(root)
            output_dir = Path(temp_dir) / "reports"
            output_dir.mkdir()
            text_path = output_dir / "plan.txt"
            json_path = output_dir / "plan.json"

            write_source_debris_quarantine_dry_run_text(plan, text_path)
            write_source_debris_quarantine_dry_run_json(plan, json_path)

            with self.assertRaises(FileExistsError):
                write_source_debris_quarantine_dry_run_text(plan, text_path)

            write_source_debris_quarantine_dry_run_text(
                plan,
                text_path,
                overwrite=True,
            )

            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())

    def test_write_rejects_missing_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            plan = build_source_debris_quarantine_dry_run(root)

            with self.assertRaises(ValueError):
                write_source_debris_quarantine_dry_run_json(
                    plan,
                    Path(temp_dir) / "missing" / "plan.json",
                )

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
