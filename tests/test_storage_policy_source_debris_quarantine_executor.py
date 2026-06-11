"""Tests for source debris quarantine executor."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.source_debris_quarantine_executor import (
    SOURCE_DEBRIS_QUARANTINE_EXECUTOR_ACTION,
    SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
    SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_COMPLETED,
    SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_CONFIRMATION_REQUIRED,
    SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_FAILED,
    SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_SKIPPED_EMPTY,
    SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED_DESTINATION_EXISTS,
    SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED,
    SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_MISSING,
    SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_NON_QUARANTINE,
    SourceDebrisQuarantineExecutionResult,
    execute_source_debris_quarantine,
    execute_source_debris_quarantine_plan,
    render_source_debris_quarantine_execution_json,
    render_source_debris_quarantine_execution_text,
    write_source_debris_quarantine_execution_json,
    write_source_debris_quarantine_execution_text,
)
from kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run import (
    build_source_debris_quarantine_dry_run,
)
import kanda_reasoner_app.storage_policy.source_debris_quarantine_executor as executor_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "source_debris_quarantine_executor.py"
)


class StoragePolicySourceDebrisQuarantineExecutorTests(unittest.TestCase):
    """Validate source debris quarantine execution behavior."""

    def test_public_surface_is_declared(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.storage_policy.source_debris_quarantine_executor"
        )
        expected = {
            "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_ACTION",
            "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN",
            "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_SCHEMA_VERSION",
            "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_COMPLETED",
            "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_CONFIRMATION_REQUIRED",
            "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_FAILED",
            "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_SKIPPED_EMPTY",
            "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED",
            "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED_DESTINATION_EXISTS",
            "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED",
            "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_MISSING",
            "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_NON_QUARANTINE",
            "SourceDebrisQuarantineExecutionItem",
            "SourceDebrisQuarantineExecutionResult",
            "execute_source_debris_quarantine",
            "execute_source_debris_quarantine_plan",
            "render_source_debris_quarantine_execution_json",
            "render_source_debris_quarantine_execution_text",
            "write_source_debris_quarantine_execution_json",
            "write_source_debris_quarantine_execution_text",
        }
        self.assertEqual(set(module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(module, name))

    def test_import_does_not_move_or_scan_live_tree(self) -> None:
        self.assertEqual(
            executor_module.SOURCE_DEBRIS_QUARANTINE_EXECUTOR_ACTION,
            "move_quarantine_review_items",
        )

    def test_confirmation_is_required_before_any_move(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            source_file = root / "module.py.bak"
            source_file.write_text("old\n", encoding="utf-8")
            maintenance_root = Path(temp_dir) / "maintenance"

            result = execute_source_debris_quarantine(
                root,
                maintenance_root=maintenance_root,
            )

            self.assertEqual(
                result.status,
                SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_CONFIRMATION_REQUIRED,
            )
            self.assertTrue(source_file.exists())
            self.assertEqual(result.moved_items, 0)
            self.assertEqual(result.total_items, 0)

    def test_executor_moves_only_quarantine_review_items(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            bak_file = root / "module.py.bak"
            bak_file.write_text("old\n", encoding="utf-8")
            cache_dir = root / "__pycache__"
            cache_dir.mkdir()
            (cache_dir / "module.pyc").write_bytes(b"cache")
            evidence_dir = root / "project_analysis_evidence"
            evidence_dir.mkdir()
            (evidence_dir / "sample_project__complete.json").write_text(
                "{}\n",
                encoding="utf-8",
            )
            workbench_dir = root / "workbench" / "bundle_manifest"
            workbench_dir.mkdir(parents=True)
            (workbench_dir / "manifest.txt").write_text("dev\n", encoding="utf-8")
            maintenance_root = Path(temp_dir) / "maintenance"

            result = execute_source_debris_quarantine(
                root,
                maintenance_root=maintenance_root,
                confirmation_token=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
            )

            self.assertEqual(result.status, SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_COMPLETED)
            self.assertEqual(result.moved_items, 2)
            self.assertEqual(result.failed_items, 0)
            self.assertFalse(bak_file.exists())
            self.assertFalse(cache_dir.exists())
            self.assertTrue(evidence_dir.exists())
            self.assertTrue(workbench_dir.exists())
            statuses = {item.relative_path: item.status for item in result.items}
            self.assertEqual(statuses["module.py.bak"], SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED)
            self.assertEqual(statuses["__pycache__/"], SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED)
            self.assertEqual(
                statuses["project_analysis_evidence/"],
                SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_NON_QUARANTINE,
            )
            self.assertEqual(
                statuses["workbench/"],
                SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_NON_QUARANTINE,
            )

    def test_missing_source_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            source_file = root / "module.py.bak"
            source_file.write_text("old\n", encoding="utf-8")
            maintenance_root = Path(temp_dir) / "maintenance"
            plan = build_source_debris_quarantine_dry_run(
                root,
                maintenance_root=maintenance_root,
            )
            source_file.unlink()

            result = execute_source_debris_quarantine_plan(
                plan,
                confirmation_token=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
            )

            self.assertEqual(result.status, SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_COMPLETED)
            self.assertEqual(result.moved_items, 0)
            self.assertEqual(result.skipped_items, 1)
            self.assertEqual(result.items[0].status, SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_MISSING)

    def test_destination_exists_fails_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            source_file = root / "module.py.backup"
            source_file.write_text("old\n", encoding="utf-8")
            maintenance_root = Path(temp_dir) / "maintenance"
            plan = build_source_debris_quarantine_dry_run(
                root,
                maintenance_root=maintenance_root,
            )
            destination = Path(plan.items[0].planned_destination_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text("already here\n", encoding="utf-8")

            result = execute_source_debris_quarantine_plan(
                plan,
                confirmation_token=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
            )

            self.assertEqual(result.status, SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_FAILED)
            self.assertEqual(result.failed_items, 1)
            self.assertTrue(source_file.exists())
            self.assertEqual(
                result.items[0].status,
                SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED_DESTINATION_EXISTS,
            )

    def test_empty_plan_is_skipped_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            result = execute_source_debris_quarantine(
                root,
                maintenance_root=Path(temp_dir) / "maintenance",
                confirmation_token=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
            )
            self.assertEqual(result.status, SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_SKIPPED_EMPTY)
            self.assertEqual(result.total_items, 0)

    def test_renderers_are_stable_and_serializable(self) -> None:
        result = SourceDebrisQuarantineExecutionResult(
            source_root="source",
            project_slug="sample_project",
            status="completed",
            confirmation_token_required=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
        )

        text = render_source_debris_quarantine_execution_text(result)
        payload = json.loads(render_source_debris_quarantine_execution_json(result))

        self.assertIn("Kanda Reasoner source debris quarantine execution result", text)
        self.assertEqual(payload["action"], SOURCE_DEBRIS_QUARANTINE_EXECUTOR_ACTION)
        self.assertEqual(payload["total_items"], 0)

    def test_write_functions_are_explicit_and_respect_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = SourceDebrisQuarantineExecutionResult(
                source_root="source",
                project_slug="sample_project",
                status="completed",
                confirmation_token_required=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
            )
            output_dir = Path(temp_dir) / "reports"
            output_dir.mkdir()
            text_path = output_dir / "result.txt"
            json_path = output_dir / "result.json"

            write_source_debris_quarantine_execution_text(result, text_path)
            write_source_debris_quarantine_execution_json(result, json_path)

            with self.assertRaises(FileExistsError):
                write_source_debris_quarantine_execution_text(result, text_path)

            write_source_debris_quarantine_execution_text(
                result,
                text_path,
                overwrite=True,
            )
            self.assertTrue(text_path.exists())
            self.assertTrue(json_path.exists())

    def test_write_rejects_missing_parent(self) -> None:
        result = SourceDebrisQuarantineExecutionResult(
            source_root="source",
            project_slug="sample_project",
            status="completed",
            confirmation_token_required=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(ValueError):
                write_source_debris_quarantine_execution_json(
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
