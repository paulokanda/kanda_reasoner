# project-path: validation/test_architecture_review_large_file_refactor_batch_queue_install_repair_v4.py
"""Regression tests for batch queue install repair v4."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.batch_refactor_queue import (
    write_batch_refactor_queue,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class BatchQueueInstallRepairV4Tests(unittest.TestCase):
    """Validate parser-safe install/validate contract and no-write gates."""

    def test_all_batch_queue_validators_are_installed_through_v4(self) -> None:
        """The repair must install all batch queue validators and tests."""

        required = [
            "tools/validate_architecture_review_large_file_refactor_batch_queue_v1.py",
            "tools/validate_architecture_review_large_file_refactor_batch_queue_install_repair_v2.py",
            "tools/validate_architecture_review_large_file_refactor_batch_queue_install_repair_v3.py",
            "tools/validate_architecture_review_large_file_refactor_batch_queue_install_repair_v4.py",
            "validation/test_architecture_review_large_file_refactor_batch_queue_v1.py",
            "validation/test_architecture_review_large_file_refactor_batch_queue_install_repair_v2.py",
            "validation/test_architecture_review_large_file_refactor_batch_queue_install_repair_v3.py",
            "validation/test_architecture_review_large_file_refactor_batch_queue_install_repair_v4.py",
        ]
        for rel in required:
            self.assertTrue((PROJECT_ROOT / rel).is_file(), rel)

    def test_batch_queue_still_has_no_apply_flags(self) -> None:
        """Repair must not introduce source mutation or batch apply behavior."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "src").mkdir()
            (root / "plans").mkdir()
            (root / "src" / "alpha.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
            (root / "plans" / "alpha.json").write_text(
                '{"target_relpath": "src/alpha.py"}', encoding="utf-8"
            )
            preview = root.parent / "project_delete_after_daily_work" / "large_file_refactor_preview"
            result = write_batch_refactor_queue(
                root,
                [{"plan_relpath": "plans/alpha.json", "priority": 1}],
                preview_root=preview,
            )
            self.assertEqual(result.status, "batch_queue_ready")
            self.assertFalse(result.source_mutation_enabled)
            self.assertFalse(result.batch_apply_enabled)
            self.assertFalse(result.import_rewrite_apply_enabled)
            self.assertTrue((preview / "BATCH_REFACTOR_QUEUE.json").is_file())


if __name__ == "__main__":
    unittest.main()
