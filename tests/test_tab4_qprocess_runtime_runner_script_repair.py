"""Focused regression tests for Tab 4 QProcess runtime runner path.

The Tab 4 runtime trace process must launch the canonical runtime runner from:
kanda_reasoner_app/reasoner_runtime_collector/runtime_runner.py

It must not use the stale global _RUNTIME_RUNNER_SCRIPT value, because that
value can still point to the deleted ask_ai_project_reasoner package.
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


class Tab4QProcessRuntimeRunnerScriptRepairTests(unittest.TestCase):
    """Protect Tab 4 runtime runner QProcess path."""

    def test_window_process_source_exists(self) -> None:
        self.assertTrue(TARGET.exists(), str(TARGET))

    def test_runtime_runner_qprocess_uses_canonical_runtime_runner_path(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertIn(
            "reasoner_runtime_collector",
            source,
        )
        self.assertIn(
            "runtime_runner.py",
            source,
        )
        self.assertIn(
            "runtime_runner_script",
            source,
        )
        self.assertIn(
            "CANONICAL_PACKAGE_NAME",
            source,
        )

    def test_runtime_runner_qprocess_does_not_use_stale_global_script(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertNotIn(
            "process_args = [str(_RUNTIME_RUNNER_SCRIPT.resolve())]",
            source,
        )

    def test_deleted_legacy_runtime_collector_physical_path_is_not_required(self) -> None:
        old_path = (
            PROJECT_ROOT
            / "ask_ai_project_reasoner"
            / "project_reasoner_v10_runtime_collector"
            / "runtime_runner.py"
        )

        self.assertFalse(old_path.exists(), str(old_path))

    def test_canonical_runtime_runner_physical_path_exists(self) -> None:
        canonical = (
            PROJECT_ROOT
            / "kanda_reasoner_app"
            / "reasoner_runtime_collector"
            / "runtime_runner.py"
        )

        self.assertTrue(canonical.exists(), str(canonical))


if __name__ == "__main__":
    unittest.main()
