"""Focused regression tests for Tab 4 collector runner path.

After deleting the legacy ask_ai_project_reasoner package, Tab 4 must launch
the collector stage from the selected project root:

project_root/kanda_reasoner_app/reasoner_tools_shell/runner.py
"""

from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_shell"
    / "runner_help"
    / "window_process_private_impl.py"
)


class Tab4CollectorRunnerPathRepairTests(unittest.TestCase):
    """Protect Tab 4 collector-stage QProcess path."""

    def test_window_process_source_exists(self) -> None:
        self.assertTrue(TARGET.exists(), str(TARGET))

    def test_collector_stage_uses_selected_project_root_runner(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertIn(
            'project_root / CANONICAL_PACKAGE_NAME / "reasoner_tools_shell"',
            source,
        )
        self.assertIn(
            '"runner.py"',
            source,
        )
        self.assertNotIn(
            'str(_installed_package_dir(_tab4_tool_root()) / "reasoner_tools_shell" / "runner.py")',
            source,
        )

    def test_child_environment_prefers_selected_project_root(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertIn(
            "project_root if _has_reasoner_package(project_root) else _tab4_tool_root()",
            source,
        )

    def test_qprocess_working_directory_uses_selected_project_root(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertNotIn(
            "_tab4_apply_qprocess_env(self._process, env, _tab4_tool_root())",
            source,
        )

    def test_selected_project_root_collector_runner_exists_for_current_project(self) -> None:
        runner = (
            PROJECT_ROOT
            / "kanda_reasoner_app"
            / "reasoner_tools_shell"
            / "runner.py"
        )

        self.assertTrue(runner.exists(), str(runner))


if __name__ == "__main__":
    unittest.main()
