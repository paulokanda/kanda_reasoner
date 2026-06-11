"""Tests for the project_reasoner_v10 deletion dry-run helper."""

from __future__ import annotations

import unittest
from pathlib import Path

import tools.project_reasoner_v10_deletion_dry_run as deletion_dry_run


class ProjectReasonerV10DeletionDryRunTests(unittest.TestCase):
    def test_dry_run_script_exists(self):
        path = Path("tools/project_reasoner_v10_deletion_dry_run.py")
        self.assertTrue(path.exists(), str(path))

    def test_delete_target_constant_points_to_project_reasoner_v10(self):
        self.assertEqual(
            deletion_dry_run.DELETE_TARGET_RELATIVE_PATH,
            "kanda_reasoner_app/project_reasoner_v10",
        )

    def test_public_contract_is_collision_safe(self):
        self.assertIn("run_dry_run", deletion_dry_run.__all__)
        self.assertIn("run_command", deletion_dry_run.__all__)
        self.assertIn("main", deletion_dry_run.__all__)
        self.assertNotIn("build_parser", deletion_dry_run.__all__)

    def test_dry_run_public_functions_are_callable(self):
        self.assertTrue(callable(deletion_dry_run.run_dry_run))
        self.assertTrue(callable(deletion_dry_run.run_command))
        self.assertTrue(callable(deletion_dry_run.main))


if __name__ == "__main__":
    unittest.main()
