"""Freeze tests for the reasoner_runtime_collector folder rename."""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OLD_RUNTIME_COLLECTOR = (
    PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10_runtime_collector"
)
NEW_RUNTIME_COLLECTOR = (
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_runtime_collector"
)
SHELL_RUNNER = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner.py"


class ReasonerRuntimeCollectorFolderRenameTests(unittest.TestCase):
    """Verify the runtime collector has the canonical name."""

    def test_new_runtime_collector_folder_exists(self) -> None:
        self.assertTrue(NEW_RUNTIME_COLLECTOR.is_dir())

    def test_old_runtime_collector_folder_is_absent(self) -> None:
        self.assertFalse(OLD_RUNTIME_COLLECTOR.exists())

    def test_canonical_runtime_collector_runner_imports(self) -> None:
        module = importlib.import_module(
            "kanda_reasoner_app.reasoner_runtime_collector.runner"
        )
        self.assertTrue(hasattr(module, "Runner"))

    def test_old_runtime_collector_import_is_absent_in_fresh_interpreter(self) -> None:
        code = (
            "import importlib.util; "
            "spec = importlib.util.find_spec("
            "'kanda_reasoner_app.project_reasoner_v10_runtime_collector'"
            "); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_shell_runner_imports_with_deleted_runtime_collector_alias(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import kanda_reasoner_app.reasoner_tools_shell.runner; "
                    "import kanda_reasoner_app.reasoner_runtime_collector.runner; "
                    "print('runtime collector alias ok')"
                ),
            ],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)

    def test_shell_runner_source_has_runtime_collector_alias(self) -> None:
        text = SHELL_RUNNER.read_text(encoding="utf-8", errors="replace")
        self.assertIn("_install_deleted_legacy_runtime_collector_aliases", text)
        self.assertIn("project_reasoner_v10_runtime_collector", text)
        self.assertIn("reasoner_runtime_collector", text)


if __name__ == "__main__":
    unittest.main()
