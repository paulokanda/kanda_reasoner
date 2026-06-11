"""Focused tests for dynamic root display in the architecture CLI."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ArchitectureCliDynamicRootHelpTests(unittest.TestCase):
    """Verify architecture help prefers dynamic roots over stale history."""

    def test_help_prefers_environment_root_over_stale_history(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temp_home, tempfile.TemporaryDirectory() as temp_project:
            history_path = Path(temp_home) / ".manage_architecture_history.json"
            history_path.write_text(
                json.dumps({"roots": [r"E:\developer_tools"], "excluded_files": []}),
                encoding="utf-8",
            )

            env = os.environ.copy()
            env["PYTHONPATH"] = str(project_root)
            env["HOME"] = temp_home
            env["USERPROFILE"] = temp_home
            env["kanda_reasoner_project_root"] = temp_project

            command = [
                sys.executable,
                str(
                    project_root
                    / "kanda_reasoner_app"
                    / "manage_architecture"
                    / "manage_architecture.py"
                ),
                "--help",
            ]
            completed = subprocess.run(
                command,
                cwd=str(project_root),
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

        output = completed.stdout + completed.stderr
        self.assertEqual(completed.returncode, 0, output)
        self.assertIn("Currently defaults to:", output)
        self.assertIn(temp_project, output)
        self.assertNotIn(r"Currently defaults to: E:\developer_tools", output)
        self.assertNotIn("hard-coded fallback", output)


if __name__ == "__main__":
    unittest.main()
