# project-path: validation/test_architecture_review_large_file_refactor_batch_queue_v1.py
"""Regression tests for batch refactor queue evidence."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.batch_refactor_queue import (
    BATCH_REFACTOR_QUEUE_FILENAME,
    build_batch_refactor_queue,
    write_batch_refactor_queue,
)


class BatchRefactorQueueTests(unittest.TestCase):
    """Validate no-write batch queue behavior."""

    def test_writes_queue_for_multiple_unique_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "src").mkdir()
            (root / "plans").mkdir()
            (root / "src" / "alpha.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
            (root / "src" / "beta.py").write_text("def beta():\n    return 2\n", encoding="utf-8")
            (root / "plans" / "alpha.json").write_text(json.dumps({"target_relpath": "src/alpha.py"}), encoding="utf-8")
            (root / "plans" / "beta.json").write_text(json.dumps({"target_relpath": "src/beta.py"}), encoding="utf-8")
            preview = root.parent / "project_delete_after_daily_work" / "large_file_refactor_preview"

            result = write_batch_refactor_queue(
                root,
                [
                    {"plan_relpath": "plans/beta.json", "priority": 2},
                    {"plan_relpath": "plans/alpha.json", "priority": 1},
                ],
                preview_root=preview,
            )

            self.assertEqual(result.status, "batch_queue_ready")
            self.assertFalse(result.source_mutation_enabled)
            self.assertFalse(result.batch_apply_enabled)
            self.assertFalse(result.import_rewrite_apply_enabled)
            self.assertEqual([item.target_relpath for item in result.queued_items], ["src/alpha.py", "src/beta.py"])
            self.assertTrue((preview / BATCH_REFACTOR_QUEUE_FILENAME).is_file())
            saved = json.loads((preview / BATCH_REFACTOR_QUEUE_FILENAME).read_text(encoding="utf-8"))
            self.assertEqual(saved["status"], "batch_queue_ready")
            self.assertTrue(saved["queue_token"].startswith("CONFIRM_BATCH_REFACTOR_QUEUE_"))

    def test_blocks_duplicate_and_protected_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            root.mkdir()
            (root / "src").mkdir()
            (root / "plans").mkdir()
            (root / "src" / "alpha.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
            (root / "plans" / "a.json").write_text(json.dumps({"target_relpath": "src/alpha.py"}), encoding="utf-8")
            (root / "plans" / "b.json").write_text(json.dumps({"target_relpath": "src/alpha.py"}), encoding="utf-8")
            preview = root.parent / "project_delete_after_daily_work" / "large_file_refactor_preview"

            result = build_batch_refactor_queue(
                root,
                [{"plan_relpath": "plans/a.json"}, {"plan_relpath": "plans/b.json"}, {"plan_relpath": ".project_reference/x.json", "target_relpath": "src/z.py"}],
                preview_root=preview,
            )

            self.assertEqual(len(result.queued_items), 1)
            blockers = {blocker for item in result.blocked_items for blocker in item.blockers}
            self.assertIn("DUPLICATE_TARGET_IN_QUEUE", blockers)
            self.assertIn("INVALID_OR_PROTECTED_PLAN_RELPATH", blockers)

    def test_blocks_preview_root_inside_project_source(self) -> None:
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
