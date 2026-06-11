"""Focused tests for ask_ai_project_reasoner deletion dry-run."""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path

import tools.ask_ai_project_reasoner_deletion_dry_run as dry_run


class AskAiProjectReasonerDeletionDryRunTests(unittest.TestCase):
    def test_dry_run_script_exists(self):
        self.assertTrue(Path("tools/ask_ai_project_reasoner_deletion_dry_run.py").exists())

    def test_delete_target_constant_points_to_ask_ai_root(self):
        self.assertEqual("ask_ai_project_reasoner", dry_run.DELETE_TARGET_RELATIVE)

    def test_deleted_engine_package_remains_absent(self):
        self.assertFalse(Path("kanda_reasoner_app/project_reasoner_v10").exists())

    def test_dry_run_public_functions_are_callable(self):
        self.assertTrue(callable(dry_run.run_ask_ai_deletion_dry_run))
        self.assertTrue(callable(dry_run.main))

    def test_public_contract_is_collision_safe(self):
        self.assertIn("run_ask_ai_deletion_dry_run", dry_run.PUBLIC_API)
        self.assertNotIn("build_parser", dry_run.PUBLIC_API)

    def test_canonical_runtime_imports_now(self):
        module = importlib.import_module("kanda_reasoner_app.reasoner_engine")
        self.assertIsNotNone(module)

    def test_fresh_interpreter_ask_ai_currently_importable_before_dry_run(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import importlib.util; "
                    "spec = importlib.util.find_spec('ask_ai_project_reasoner'); "
                    "raise SystemExit(0 if spec is not None else 1)"
                ),
            ],
            text=True,
        )
        self.assertEqual(0, completed.returncode)


if __name__ == "__main__":
    unittest.main()
