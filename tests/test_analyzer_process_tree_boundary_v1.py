"""Cross-platform behavior tests for analyzer process-tree cleanup."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_process_tree as process_tree


class AnalyzerProcessTreeBoundaryTests(unittest.TestCase):
    """Exercise both natural-exit and requested tree-termination paths."""

    def test_natural_exit_reports_no_cleanup_request(self) -> None:
        process = subprocess.Popen(
            [sys.executable, "-c", "pass"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **process_tree.process_tree_spawn_kwargs(),
        )
        process.wait(timeout=10)
        evidence = process_tree.terminate_process_tree(process, grace_seconds=0.2)
        self.assertEqual(evidence.method, "natural_exit")
        self.assertFalse(evidence.requested)
        self.assertTrue(evidence.root_process_reaped)
        self.assertTrue(evidence.cleanup_ok)

    def test_live_process_tree_is_terminated_and_reaped(self) -> None:
        process = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **process_tree.process_tree_spawn_kwargs(),
        )
        try:
            evidence = process_tree.terminate_process_tree(
                process,
                grace_seconds=1.0,
            )
            self.assertTrue(evidence.requested)
            self.assertTrue(evidence.root_process_reaped, evidence.to_dict())
            self.assertTrue(evidence.cleanup_ok, evidence.to_dict())
            self.assertIsNotNone(process.poll())
        finally:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=10)


if __name__ == "__main__":
    unittest.main()
