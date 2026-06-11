"""Tests for canonical kanda_reasoner_app CLI entrypoints."""

from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


class KandaReasonerAppCanonicalCliEntrypointTests(unittest.TestCase):
    """Verify canonical CLI wrappers work before legacy package removal."""

    def setUp(self) -> None:
        self.project_root = Path(__file__).resolve().parents[1]
        self.env = os.environ.copy()
        self.env["PYTHONPATH"] = str(self.project_root)
        self.env["kanda_reasoner_project_root"] = str(self.project_root)

    def _run_help(self, relative_path: str) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, relative_path, "--help"]
        return subprocess.run(
            command,
            cwd=str(self.project_root),
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def _skip_if_reconstruction_dependency_is_missing(
        self,
        result: subprocess.CompletedProcess[str],
    ) -> None:
        text = result.stdout + result.stderr
        if "workflow_placeholder_contract" in text:
            self.skipTest(
                "Reconstructed sandbox is missing workflow_placeholder_contract."
            )

    def test_architecture_cli_wrapper_help_runs(self) -> None:
        result = self._run_help(
            "kanda_reasoner_app/manage_architecture/manage_architecture.py"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Manage architecture manifest", result.stdout)
        self.assertIn(str(self.project_root), result.stdout)

    def test_workflow_cli_wrapper_help_runs(self) -> None:
        result = self._run_help(
            "kanda_reasoner_app/manage_workflows/manage_workflows.py"
        )
        self._skip_if_reconstruction_dependency_is_missing(result)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Manage runtime/business/gui", result.stdout)
        self.assertIn(str(self.project_root), result.stdout)

    def test_canonical_cli_modules_import_without_heavy_legacy_imports(self) -> None:
        import kanda_reasoner_app.manage_architecture.manage_architecture as arch_cli
        import kanda_reasoner_app.manage_workflows.manage_workflows as workflow_cli

        self.assertTrue(callable(arch_cli.main))
        self.assertTrue(callable(workflow_cli.main))
        self.assertTrue(callable(workflow_cli.validate_project))


if __name__ == "__main__":
    unittest.main()
