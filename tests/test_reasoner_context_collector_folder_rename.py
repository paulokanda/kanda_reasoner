"""Regression tests for the reasoner_context_collector folder rename."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OLD_COLLECTOR = PROJECT_ROOT / "kanda_reasoner_app" / "project_reasoner_v10_data_collector"
NEW_COLLECTOR = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_collector"
SHELL_RUNNER = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner.py"


class ReasonerContextCollectorFolderRenameTests(unittest.TestCase):
    """Protect the canonical collector folder name and runtime aliases."""

    def run_python(self, code: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(PROJECT_ROOT),
            text=True,
            capture_output=True,
            check=False,
        )

    def test_new_collector_folder_exists(self) -> None:
        self.assertTrue(NEW_COLLECTOR.exists(), str(NEW_COLLECTOR))
        self.assertTrue((NEW_COLLECTOR / "runner.py").exists())

    def test_old_collector_folder_is_absent(self) -> None:
        self.assertFalse(OLD_COLLECTOR.exists(), str(OLD_COLLECTOR))

    def test_old_collector_import_is_absent_in_fresh_interpreter(self) -> None:
        result = self.run_python(
            "import importlib.util; "
            "spec = importlib.util.find_spec('kanda_reasoner_app.project_reasoner_v10_data_collector'); "
            "raise SystemExit(0 if spec is None else 1)"
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_canonical_collector_runner_imports(self) -> None:
        result = self.run_python(
            "import kanda_reasoner_app.reasoner_context_collector.runner; "
            "print('reasoner_context_collector runner import ok')"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("reasoner_context_collector runner import ok", result.stdout)

    def test_shell_runner_imports_with_deleted_collector_alias(self) -> None:
        result = self.run_python(
            "import kanda_reasoner_app.reasoner_tools_shell.runner; "
            "print('shell runner import ok with deleted collector alias')"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("shell runner import ok with deleted collector alias", result.stdout)

    def test_shell_runner_source_has_collector_alias(self) -> None:
        text = SHELL_RUNNER.read_text(encoding="utf-8", errors="replace")
        self.assertIn("project_reasoner_v10_data_collector", text)
        self.assertIn("reasoner_context_collector", text)
        self.assertIn("_install_deleted_legacy_context_collector_aliases", text)


if __name__ == "__main__":
    unittest.main()
