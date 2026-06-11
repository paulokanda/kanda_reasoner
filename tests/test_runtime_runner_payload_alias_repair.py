"""Focused regression tests for runtime_runner payload legacy alias repair."""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class RuntimeRunnerPayloadAliasRepairTests(unittest.TestCase):
    """Protect canonical runtime_runner import after legacy package deletion."""

    def test_runtime_runner_imports_in_current_interpreter(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner"
        )

        self.assertIsNotNone(module)

    def test_runtime_runner_imports_in_fresh_interpreter(self) -> None:
        command = (
            "import kanda_reasoner_app.reasoner_runtime_collector.runtime_runner; "
            "print('runtime_runner fresh import ok')"
        )

        result = subprocess.run(
            [sys.executable, "-c", command],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_deleted_legacy_runtime_collector_folder_stays_absent(self) -> None:
        old_folder = (
            PROJECT_ROOT
            / "kanda_reasoner_app"
            / "project_reasoner_v10_runtime_collector"
        )

        self.assertFalse(old_folder.exists(), str(old_folder))

    def test_deleted_legacy_root_folder_stays_absent(self) -> None:
        old_root = PROJECT_ROOT / "ask_ai_project_reasoner"

        self.assertFalse(old_root.exists(), str(old_root))


if __name__ == "__main__":
    unittest.main()
