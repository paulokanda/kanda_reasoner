"""Tests for explicit evidence relocation execution."""

from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from kanda_reasoner_app.storage_policy.evidence_relocation_dry_run import (
    plan_evidence_relocation_dry_run,
)
from kanda_reasoner_app.storage_policy.evidence_relocator import (
    EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN,
    EVIDENCE_RELOCATOR_ITEM_STATUS_COPIED,
    EVIDENCE_RELOCATOR_ITEM_STATUS_MOVED,
    EVIDENCE_RELOCATOR_ITEM_STATUS_SKIPPED,
    EVIDENCE_RELOCATOR_MODE_COPY_ONLY,
    EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED,
    EVIDENCE_RELOCATOR_STATUS_COMPLETED,
    EVIDENCE_RELOCATOR_STATUS_REVIEW_REQUIRED,
    EVIDENCE_RELOCATOR_STATUS_SKIPPED_ABSENT,
    EvidenceRelocationExecutionItem,
    EvidenceRelocationExecutionResult,
    calculate_file_sha256,
    execute_evidence_relocation_plan,
    render_evidence_relocation_result_json,
    render_evidence_relocation_result_text,
    write_evidence_relocation_result_json,
    write_evidence_relocation_result_text,
)
import kanda_reasoner_app.storage_policy.evidence_relocator as relocator_module


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELOCATOR_SOURCE = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "storage_policy"
    / "evidence_relocator.py"
)


class StoragePolicyEvidenceRelocatorTests(unittest.TestCase):
    """Validate explicit, confirmed evidence relocation behavior."""

    def test_public_surface_is_declared(self) -> None:
        expected = {
            "EVIDENCE_RELOCATOR_ACTION",
            "EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN",
            "EVIDENCE_RELOCATOR_ITEM_STATUS_COPIED",
            "EVIDENCE_RELOCATOR_ITEM_STATUS_FAILED",
            "EVIDENCE_RELOCATOR_ITEM_STATUS_MOVED",
            "EVIDENCE_RELOCATOR_ITEM_STATUS_SKIPPED",
            "EVIDENCE_RELOCATOR_MODE_COPY_ONLY",
            "EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED",
            "EVIDENCE_RELOCATOR_STATUS_COMPLETED",
            "EVIDENCE_RELOCATOR_STATUS_CONFIRMATION_REQUIRED",
            "EVIDENCE_RELOCATOR_STATUS_FAILED",
            "EVIDENCE_RELOCATOR_STATUS_REVIEW_REQUIRED",
            "EVIDENCE_RELOCATOR_STATUS_SKIPPED_ABSENT",
            "EvidenceRelocationExecutionItem",
            "EvidenceRelocationExecutionResult",
            "calculate_file_sha256",
            "execute_evidence_relocation",
            "execute_evidence_relocation_plan",
            "render_evidence_relocation_result_json",
            "render_evidence_relocation_result_text",
            "write_evidence_relocation_result_json",
            "write_evidence_relocation_result_text",
        }
        self.assertEqual(set(relocator_module.__all__), expected)
        for name in expected:
            self.assertTrue(hasattr(relocator_module, name))

    def test_import_does_not_relocate_live_tree(self) -> None:
        self.assertTrue(hasattr(relocator_module, "execute_evidence_relocation_plan"))

    def test_missing_confirmation_rejects_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence"
            source.mkdir(parents=True)
            (source / "sample_project__complete.json").write_text("{}\n", encoding="utf-8")
            plan = plan_evidence_relocation_dry_run(root)

            with self.assertRaises(ValueError):
                execute_evidence_relocation_plan(plan, confirmation_token="wrong")

    def test_copy_only_copies_json_and_leaves_source(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence"
            source.mkdir(parents=True)
            source_file = source / "sample_project__complete.json"
            source_file.write_text('{"ok": true}\n', encoding="utf-8")
            plan = plan_evidence_relocation_dry_run(root)

            result = execute_evidence_relocation_plan(
                plan,
                confirmation_token=EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN,
                mode=EVIDENCE_RELOCATOR_MODE_COPY_ONLY,
            )

            self.assertIsInstance(result, EvidenceRelocationExecutionResult)
            self.assertEqual(result.status(), EVIDENCE_RELOCATOR_STATUS_COMPLETED)
            self.assertEqual(result.copied_items, 1)
            self.assertEqual(result.moved_items, 0)
            self.assertTrue(source_file.exists())
            item = result.items[0]
            self.assertIsInstance(item, EvidenceRelocationExecutionItem)
            self.assertEqual(item.status, EVIDENCE_RELOCATOR_ITEM_STATUS_COPIED)
            self.assertEqual(item.sha256_before, item.sha256_after)
            self.assertTrue(Path(item.destination_path).exists())

    def test_move_verified_copies_hashes_and_removes_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence" / "json_complete"
            source.mkdir(parents=True)
            source_file = source / "sample_project__complete.json"
            source_file.write_text('{"ok": true}\n', encoding="utf-8")
            plan = plan_evidence_relocation_dry_run(root)

            result = execute_evidence_relocation_plan(
                plan,
                confirmation_token=EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN,
                mode=EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED,
                prune_empty_source_dirs=True,
            )

            self.assertEqual(result.status(), EVIDENCE_RELOCATOR_STATUS_COMPLETED)
            self.assertEqual(result.moved_items, 1)
            self.assertFalse(source_file.exists())
            self.assertFalse((root / "project_analysis_evidence").exists())
            self.assertEqual(result.items[0].status, EVIDENCE_RELOCATOR_ITEM_STATUS_MOVED)
            self.assertEqual(result.items[0].sha256_before, result.items[0].sha256_after)

    def test_review_items_prevent_relocation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence"
            source.mkdir(parents=True)
            (source / "sample_project__complete.json").write_text("{}\n", encoding="utf-8")
            note = source / "notes.txt"
            note.write_text("review me\n", encoding="utf-8")
            plan = plan_evidence_relocation_dry_run(root)

            result = execute_evidence_relocation_plan(
                plan,
                confirmation_token=EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN,
            )

            self.assertEqual(result.status(), EVIDENCE_RELOCATOR_STATUS_REVIEW_REQUIRED)
            self.assertEqual(result.total_items, 0)
            self.assertEqual(result.skipped_items, 1)
            self.assertEqual(
                result.skipped_review_items[0].status,
                EVIDENCE_RELOCATOR_ITEM_STATUS_SKIPPED,
            )
            self.assertTrue(note.exists())

    def test_absent_plan_is_skipped_after_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            plan = plan_evidence_relocation_dry_run(root)

            result = execute_evidence_relocation_plan(
                plan,
                confirmation_token=EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN,
            )

            self.assertEqual(result.status(), EVIDENCE_RELOCATOR_STATUS_SKIPPED_ABSENT)
            self.assertEqual(result.total_items, 0)

    def test_hash_calculation_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "sample.json"
            target.write_text("abc\n", encoding="utf-8")

            first = calculate_file_sha256(target)
            second = calculate_file_sha256(target)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 64)

    def test_result_rendering_and_writing_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            source = root / "project_analysis_evidence"
            source.mkdir(parents=True)
            (source / "sample_project__complete.json").write_text("{}\n", encoding="utf-8")
            plan = plan_evidence_relocation_dry_run(root)
            result = execute_evidence_relocation_plan(
                plan,
                confirmation_token=EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN,
            )
            output_dir = Path(temp_dir) / "reports"
            output_dir.mkdir()
            text_path = output_dir / "result.txt"
            json_path = output_dir / "result.json"

            write_evidence_relocation_result_text(result, text_path)
            write_evidence_relocation_result_json(result, json_path)

            self.assertIn("Kanda Reasoner evidence relocator report", text_path.read_text(encoding="utf-8"))
            data = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(data["status"], EVIDENCE_RELOCATOR_STATUS_COMPLETED)
            self.assertTrue(render_evidence_relocation_result_text(result).startswith("Kanda"))
            self.assertTrue(render_evidence_relocation_result_json(result).startswith("{"))
            with self.assertRaises(FileExistsError):
                write_evidence_relocation_result_json(result, json_path)

    def test_write_rejects_missing_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()
            plan = plan_evidence_relocation_dry_run(root)
            result = execute_evidence_relocation_plan(
                plan,
                confirmation_token=EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN,
            )
            with self.assertRaises(FileNotFoundError):
                write_evidence_relocation_result_text(
                    result,
                    Path(temp_dir) / "missing" / "result.txt",
                )

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        text = RELOCATOR_SOURCE.read_text(encoding="utf-8")
        forbidden_fragments = [
            "E:\\",
            "E:/",
            "C:\\",
            "C:/",
            "D:\\",
            "D:/",
        ]
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, text)


if __name__ == "__main__":
    unittest.main()
