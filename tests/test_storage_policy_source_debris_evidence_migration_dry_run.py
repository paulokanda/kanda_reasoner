"""Tests for source debris evidence migration dry-run planning."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.source_debris_evidence_migration_dry_run import (
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_EMPTY,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_PLANNED,
    SourceDebrisEvidenceMigrationDryRunItem,
    SourceDebrisEvidenceMigrationDryRunPlan,
    build_source_debris_evidence_migration_dry_run,
    render_source_debris_evidence_migration_dry_run_json,
    render_source_debris_evidence_migration_dry_run_text,
    write_source_debris_evidence_migration_dry_run_json,
    write_source_debris_evidence_migration_dry_run_text,
)
import kanda_reasoner_app.storage_policy.source_debris_evidence_migration_dry_run as dry_run_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "source_debris_evidence_migration_dry_run.py"
)


class StoragePolicySourceDebrisEvidenceMigrationDryRunTests(unittest.TestCase):
    """Validate source debris evidence migration dry-run behavior."""

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.source_debris_evidence_migration_dry_run"
        )
        expected = {
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_SCHEMA_VERSION",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_EMPTY",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_PLANNED",
            "SourceDebrisEvidenceMigrationDryRunItem",
            "SourceDebrisEvidenceMigrationDryRunPlan",
            "build_source_debris_evidence_migration_dry_run",
            "build_source_debris_evidence_migration_dry_run_from_quarantine_plan",
            "render_source_debris_evidence_migration_dry_run_json",
            "render_source_debris_evidence_migration_dry_run_text",
            "write_source_debris_evidence_migration_dry_run_json",
            "write_source_debris_evidence_migration_dry_run_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_import_does_not_scan_or_create_live_tree(self) -> None:
        self.assertEqual(
            dry_run_module.SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION,
            "dry_run_only",
        )

    def test_clean_tree_is_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py").write_text("print('ok')\n", encoding="utf-8")

            plan = build_source_debris_evidence_migration_dry_run(root)

        self.assertIsInstance(plan, SourceDebrisEvidenceMigrationDryRunPlan)
        self.assertEqual(plan.action, SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION)
        self.assertEqual(plan.status(), SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_EMPTY)
        self.assertEqual(plan.total_items, 0)

    def test_evidence_items_get_exact_json_complete_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            source_file = evidence / "sample_project__complete.json"
            source_file.write_text("{}\n", encoding="utf-8")
            expected_byte_count = source_file.stat().st_size
            audit_current = Path(temp_dir) / "sample_project_architecture_audit" / "current"

            plan = build_source_debris_evidence_migration_dry_run(
                root,
                audit_root=audit_current,
            )

        self.assertEqual(plan.status(), SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_PLANNED)
        self.assertEqual(plan.total_items, 1)
        self.assertEqual(plan.existing_source_items, 1)
        item = plan.items[0]
        self.assertIsInstance(item, SourceDebrisEvidenceMigrationDryRunItem)
        self.assertTrue(item.source_exists)
        self.assertEqual(item.byte_count, expected_byte_count)
        self.assertTrue(
            item.destination_path.endswith(
                "current/json_complete/sample_project__complete.json"
            )
            or item.destination_path.endswith(
                "current\\json_complete\\sample_project__complete.json"
            )
        )

    def test_nested_legacy_evidence_is_planned_but_not_moved(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = (
                root
                / ".project_reference"
                / "legacy"
                / "project_analysis_evidence"
                / "json_complete"
            )
            evidence.mkdir(parents=True)
            source_file = evidence / "legacy_project__validation_state.json"
            source_file.write_text("{}\n", encoding="utf-8")
            audit_current = Path(temp_dir) / "sample_project_architecture_audit" / "current"

            plan = build_source_debris_evidence_migration_dry_run(
                root,
                audit_root=audit_current,
            )

            self.assertEqual(plan.total_items, 1)
            self.assertTrue(source_file.exists())
            self.assertTrue(plan.items[0].source_exists)
            self.assertIn("json_complete", plan.items[0].destination_path)

    def test_packaging_and_quarantine_items_are_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            (root / "module.py.bak").write_text("old\n", encoding="utf-8")
            workbench = root / "workbench"
            workbench.mkdir()
            (workbench / "note.txt").write_text("dev\n", encoding="utf-8")

            plan = build_source_debris_evidence_migration_dry_run(root)

        self.assertEqual(plan.total_items, 0)

    def test_destination_exists_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            source_file = evidence / "sample_project__complete.json"
            source_file.write_text("{}\n", encoding="utf-8")
            audit_current = Path(temp_dir) / "sample_project_architecture_audit" / "current"
            destination = audit_current / "json_complete" / source_file.name
            destination.parent.mkdir(parents=True)
            destination.write_text("{}\n", encoding="utf-8")

            plan = build_source_debris_evidence_migration_dry_run(
                root,
                audit_root=audit_current,
            )

        self.assertEqual(plan.existing_destination_items, 1)
        self.assertTrue(plan.items[0].destination_exists)
        self.assertIn("destination already exists", plan.items[0].message)

    def test_json_render_is_stable_and_serializable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            (evidence / "sample_project__complete.json").write_text(
                "{}\n",
                encoding="utf-8",
            )
            plan = build_source_debris_evidence_migration_dry_run(root)
            payload = json.loads(render_source_debris_evidence_migration_dry_run_json(plan))

        self.assertEqual(payload["action"], SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION)
        self.assertEqual(payload["status"], SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_PLANNED)
        self.assertEqual(payload["total_items"], 1)
        self.assertEqual(len(payload["items"]), 1)

    def test_text_summary_contains_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            (evidence / "sample_project__complete.json").write_text(
                "{}\n",
                encoding="utf-8",
            )
            plan = build_source_debris_evidence_migration_dry_run(root)
            text = render_source_debris_evidence_migration_dry_run_text(plan)

        self.assertIn("Kanda Reasoner source debris evidence migration", text)
        self.assertIn("Action: dry_run_only", text)
        self.assertIn("Items: 1", text)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            plan = build_source_debris_evidence_migration_dry_run(root)
            output_dir = Path(temp_dir) / "reports"
            output_dir.mkdir()
            text_path = output_dir / "plan.txt"
            json_path = output_dir / "plan.json"

            write_source_debris_evidence_migration_dry_run_text(plan, text_path)
            write_source_debris_evidence_migration_dry_run_json(plan, json_path)

            with self.assertRaises(FileExistsError):
                write_source_debris_evidence_migration_dry_run_text(plan, text_path)

            write_source_debris_evidence_migration_dry_run_text(
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
            plan = build_source_debris_evidence_migration_dry_run(root)

            with self.assertRaises(ValueError):
                write_source_debris_evidence_migration_dry_run_json(
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
