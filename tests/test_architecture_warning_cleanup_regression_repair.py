"""Regression tests for warning cleanup side effects.

The architecture warning cleanup must not break staged package rename
compatibility or direct architecture CLI execution by path.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ArchitectureWarningCleanupRegressionRepairTests(unittest.TestCase):
    def test_legacy_project_context_bundle_compatibility_package_exists(self) -> None:
        legacy_dir = PROJECT_ROOT / "kanda_reasoner_app" / "project_context_bundle"
        self.assertTrue((legacy_dir / "__init__.py").is_file())
        self.assertTrue((legacy_dir / "__main__.py").is_file())
        self.assertFalse((legacy_dir / "output_paths.py").exists())

    def test_legacy_project_context_bundle_help_still_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "kanda_reasoner_app.project_context_bundle", "--help"],
            cwd=str(PROJECT_ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Generate additive AI context bundle", result.stdout)

    def test_manage_architecture_direct_script_uses_canonical_package(self) -> None:
        path = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture.py"
        source = path.read_text(encoding="utf-8")
        self.assertIn("kanda_reasoner_app.manage_architecture", source)
        self.assertNotIn("ask_ai_project_reasoner", source)

    def test_manage_architecture_help_runs_when_called_by_path(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "kanda_reasoner_app/manage_architecture/manage_architecture.py",
                "--help",
            ],
            cwd=str(PROJECT_ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Manage architecture manifest", result.stdout)


if __name__ == "__main__":
    unittest.main()
