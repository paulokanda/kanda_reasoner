# project-path: validation/test_architecture_review_large_file_refactor_batch_queue_install_repair_v2.py
"""Regression tests for batch queue install repair v2."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.batch_refactor_queue import (
    build_batch_refactor_queue,
    write_batch_refactor_queue,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class BatchQueueInstallRepairV2Tests(unittest.TestCase):
    """Validate that batch queue repair installs and preserves no-write gates."""

    def test_v1_validator_and_test_are_installed(self) -> None:
        """The original failed because this validator was absent after install."""

        required = [
            "tools/validate_architecture_review_large_file_refactor_batch_queue_v1.py",
            "validation/test_architecture_review_large_file_refactor_batch_queue_v1.py",
            "tools/validate_architecture_review_large_file_refactor_batch_queue_install_repair_v2.py",
        ]
        for rel in required:
            self.assertTrue((PROJECT_ROOT / rel).is_file(), rel)

    def test_queue_remains_no_write_after_repair(self) -> None:
        """Repair must not introduce source mutation or batch apply."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "src").mkdir()
            (root / "plans").mkdir()
            (root / "src" / "alpha.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
            (root / "plans" / "alpha.json").write_text(
                json.dumps({"target_relpath": "src/alpha.py"}), encoding="utf-8"
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

    def test_production_shielding_still_blocks_project_preview_root(self) -> None:
        """Preview roots inside project source must remain blocked."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "src").mkdir()
            (root / "src" / "alpha.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                build_batch_refactor_queue(
                    root,
                    [{"plan_relpath": "src/alpha.py", "target_relpath": "src/alpha.py"}],
                    preview_root=root / "large_file_refactor_preview",
                )


if __name__ == "__main__":
    unittest.main()
