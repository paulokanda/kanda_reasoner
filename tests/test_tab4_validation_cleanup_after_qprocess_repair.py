"""Focused validation cleanup after Tab 4 QProcess runtime runner repair."""

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
BAD_COMPLETE_JSON = (
    PROJECT_ROOT
    / "project_analysis_evidence"
    / "json_complete"
    / "kanda_reasoner__complete.json"
)


class Tab4ValidationCleanupAfterQProcessRepairTests(unittest.TestCase):
    """Protect post-repair validation cleanup."""

    def test_window_process_module_stays_under_warning_threshold(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")
        line_count = len(source.splitlines())

        self.assertLessEqual(line_count, 500)

    def test_runtime_runner_launch_does_not_use_stale_global(self) -> None:
        source = TARGET.read_text(encoding="utf-8", errors="ignore")

        self.assertNotIn("_RUNTIME_RUNNER_SCRIPT.resolve()", source)
        self.assertIn("reasoner_runtime_collector", source)
        self.assertIn("runtime_runner.py", source)

    def test_failed_empty_complete_json_is_removed_or_validated_later(self) -> None:
        if not BAD_COMPLETE_JSON.exists():
            return

        text = BAD_COMPLETE_JSON.read_text(encoding="utf-8", errors="ignore")
        self.assertNotEqual("{}", text.strip())


if __name__ == "__main__":
    unittest.main()
