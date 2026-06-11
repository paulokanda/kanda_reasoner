"""Focused regression tests for Tab 4 selected-root runtime runner path."""

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


class Tab4ProjectRootRuntimeRunnerPathRepairTests(unittest.TestCase):
    """Protect Tab 4 runtime runner physical path after folder deletion."""

    def test_window_process_source_exists(self) -> None:
        self.assertTrue(TARGET.exists(), str(TARGET))

    def test_runtime_runner_launch_uses_selected_project_root_candidate(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertIn(
            "project_root / CANONICAL_PACKAGE_NAME",
            source,
        )
        self.assertIn(
            "reasoner_runtime_collector",
            source,
        )
        self.assertIn(
            "runtime_runner.py",
            source,
        )

    def test_runtime_runner_launch_does_not_use_stale_global_or_drive_root_path(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertNotIn("_RUNTIME_RUNNER_SCRIPT.resolve()", source)
        self.assertNotIn("E:\\\\ask_ai_project_reasoner", source)
        self.assertNotIn("E:\\\\kanda_reasoner_app", source)

    def test_selected_project_root_canonical_runner_exists_for_current_project(self) -> None:
        canonical = (
            PROJECT_ROOT
            / "kanda_reasoner_app"
            / "reasoner_runtime_collector"
            / "runtime_runner.py"
        )

        self.assertTrue(canonical.exists(), str(canonical))


if __name__ == "__main__":
    unittest.main()
