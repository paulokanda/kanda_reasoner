"""Tests for source debris evidence migration executor."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.source_debris_evidence_migration_dry_run import (
    build_source_debris_evidence_migration_dry_run,
)
from kanda_reasoner_app.storage_policy.source_debris_evidence_migration_executor import (
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_ACTION,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_COMPLETED,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_CONFIRMATION_REQUIRED,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_FAILED,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_SKIPPED_EMPTY,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_DESTINATION_EXISTS,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_MOVED_VERIFIED,
    SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_SKIPPED_MISSING,
    SourceDebrisEvidenceMigrationExecutionResult,
    calculate_source_debris_evidence_sha256,
    execute_source_debris_evidence_migration,
    execute_source_debris_evidence_migration_plan,
    render_source_debris_evidence_migration_execution_json,
    render_source_debris_evidence_migration_execution_text,
    write_source_debris_evidence_migration_execution_json,
    write_source_debris_evidence_migration_execution_text,
)
import kanda_reasoner_app.storage_policy.source_debris_evidence_migration_executor as executor_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "source_debris_evidence_migration_executor.py"
)


class StoragePolicySourceDebrisEvidenceMigrationExecutorTests(unittest.TestCase):
    """Validate source debris evidence migration execution behavior."""

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.source_debris_evidence_migration_executor"
        )
        expected = {
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_ACTION",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_SCHEMA_VERSION",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_COMPLETED",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_CONFIRMATION_REQUIRED",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_FAILED",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_SKIPPED_EMPTY",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_DESTINATION_EXISTS",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_SOURCE_REMOVAL",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_VERIFICATION",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_MOVED_VERIFIED",
            "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_SKIPPED_MISSING",
            "SourceDebrisEvidenceMigrationExecutionItem",
            "SourceDebrisEvidenceMigrationExecutionResult",
            "calculate_source_debris_evidence_sha256",
            "execute_source_debris_evidence_migration",
            "execute_source_debris_evidence_migration_plan",
            "render_source_debris_evidence_migration_execution_json",
            "render_source_debris_evidence_migration_execution_text",
            "write_source_debris_evidence_migration_execution_json",
            "write_source_debris_evidence_migration_execution_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_import_does_not_move_or_scan_live_tree(self) -> None:
        self.assertEqual(
            executor_module.SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_ACTION,
            "copy_verify_and_remove_source_evidence",
        )

    def test_confirmation_is_required_before_any_move(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            source_file = evidence / "sample_project__complete.json"
            source_file.write_text("{}\n", encoding="utf-8")
            audit_current = Path(temp_dir) / "sample_project_architecture_audit" / "current"

            result = execute_source_debris_evidence_migration(
                root,
                audit_root=audit_current,
            )

            self.assertEqual(
                result.status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_CONFIRMATION_REQUIRED,
            )
            self.assertEqual(result.moved_items, 0)
            self.assertEqual(result.total_items, 0)
            self.assertTrue(source_file.exists())

    def test_executor_copies_verifies_and_removes_only_evidence_items(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            source_file = evidence / "sample_project__complete.json"
            source_file.write_text('{"ok": true}\n', encoding="utf-8")
            backup_file = root / "module.py.bak"
            backup_file.write_text("old\n", encoding="utf-8")
            workbench = root / "workbench" / "bundle_manifest"
            workbench.mkdir(parents=True)
            (workbench / "manifest.txt").write_text("dev\n", encoding="utf-8")
            audit_current = Path(temp_dir) / "sample_project_architecture_audit" / "current"

            result = execute_source_debris_evidence_migration(
                root,
                audit_root=audit_current,
                confirmation_token=(
                    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
                ),
            )

            self.assertEqual(
                result.status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_COMPLETED,
            )
            self.assertEqual(result.moved_items, 1)
            self.assertEqual(result.failed_items, 0)
            self.assertFalse(source_file.exists())
            self.assertTrue(backup_file.exists())
            self.assertTrue(workbench.exists())
            item = result.items[0]
            self.assertEqual(
                item.status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_MOVED_VERIFIED,
            )
            self.assertEqual(item.sha256_before, item.sha256_after)
            self.assertTrue(Path(item.destination_path).exists())

    def test_destination_exists_fails_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            source_file = evidence / "sample_project__complete.json"
            source_file.write_text("source\n", encoding="utf-8")
            audit_current = Path(temp_dir) / "sample_project_architecture_audit" / "current"
            destination = audit_current / "json_complete" / source_file.name
            destination.parent.mkdir(parents=True)
            destination.write_text("already here\n", encoding="utf-8")

            result = execute_source_debris_evidence_migration(
                root,
                audit_root=audit_current,
                confirmation_token=(
                    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
                ),
            )

            self.assertEqual(
                result.status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_FAILED,
            )
            self.assertEqual(result.failed_items, 1)
            self.assertTrue(source_file.exists())
            self.assertEqual(destination.read_text(encoding="utf-8"), "already here\n")
            self.assertEqual(
                result.items[0].status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_DESTINATION_EXISTS,
            )

    def test_missing_source_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            evidence = root / "project_analysis_evidence" / "json_complete"
            evidence.mkdir(parents=True)
            source_file = evidence / "sample_project__complete.json"
            source_file.write_text("{}\n", encoding="utf-8")
            audit_current = Path(temp_dir) / "sample_project_architecture_audit" / "current"
            plan = build_source_debris_evidence_migration_dry_run(
                root,
                audit_root=audit_current,
            )
            source_file.unlink()

            result = execute_source_debris_evidence_migration_plan(
                plan,
                confirmation_token=(
                    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
                ),
            )

            self.assertEqual(
                result.status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_COMPLETED,
            )
            self.assertEqual(result.moved_items, 0)
            self.assertEqual(result.skipped_items, 1)
            self.assertEqual(
                result.items[0].status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_SKIPPED_MISSING,
            )

    def test_empty_plan_is_skipped_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            result = execute_source_debris_evidence_migration(
                root,
                confirmation_token=(
                    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
                ),
            )

            self.assertEqual(
                result.status,
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_SKIPPED_EMPTY,
            )
            self.assertEqual(result.total_items, 0)

    def test_hash_calculation_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "sample.json"
            target.write_text("abc\n", encoding="utf-8")

            first = calculate_source_debris_evidence_sha256(target)
            second = calculate_source_debris_evidence_sha256(target)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_renderers_are_stable_and_serializable(self) -> None:
        result = SourceDebrisEvidenceMigrationExecutionResult(
            source_root="source",
            project_slug="sample_project",
            status="completed",
            confirmation_token_required=(
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
            ),
        )

        text = render_source_debris_evidence_migration_execution_text(result)
        payload = json.loads(render_source_debris_evidence_migration_execution_json(result))

        self.assertIn("Kanda Reasoner source debris evidence migration", text)
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["moved_items"], 0)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = SourceDebrisEvidenceMigrationExecutionResult(
                source_root="source",
                project_slug="sample_project",
                status="completed",
                confirmation_token_required=(
                    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
                ),
            )
            output_dir = Path(temp_dir) / "reports"
            output_dir.mkdir()
            text_path = output_dir / "result.txt"
            json_path = output_dir / "result.json"

            write_source_debris_evidence_migration_execution_text(result, text_path)
            write_source_debris_evidence_migration_execution_json(result, json_path)

            with self.assertRaises(FileExistsError):
                write_source_debris_evidence_migration_execution_text(result, text_path)

            write_source_debris_evidence_migration_execution_text(
                result,
                text_path,
                overwrite=True,
            )

            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())

    def test_write_rejects_missing_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = SourceDebrisEvidenceMigrationExecutionResult(
                source_root="source",
                project_slug="sample_project",
                status="completed",
                confirmation_token_required=(
                    SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
                ),
            )

            with self.assertRaises(ValueError):
                write_source_debris_evidence_migration_execution_json(
                    result,
                    Path(temp_dir) / "missing" / "result.json",
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
