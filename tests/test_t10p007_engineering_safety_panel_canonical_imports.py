"""Tests for canonical package use in Engineering Safety panel public helpers."""

from __future__ import annotations

from pathlib import Path
import unittest

from reasoner_tools_gui_engineering_safety_panel import (
    build_engineering_safety_panel_command,
    build_engineering_safety_panel_cli_args,
)


class EngineeringSafetyPanelCanonicalImportTests(unittest.TestCase):
    """Verify root Engineering Safety panel helpers use canonical package paths."""

    def test_display_command_uses_canonical_module_path(self) -> None:
        command = build_engineering_safety_panel_command("list-tools")
        self.assertEqual(
            command.display_args,
            ["python", "-m", "kanda_reasoner_app.safety_suite_cli.commands", "list-tools"],
        )
        self.assertNotIn('ask_' 'ai_project_reasoner', " ".join(command.display_args))

    def test_raw_cli_args_are_unchanged_for_list_tools(self) -> None:
        self.assertEqual(build_engineering_safety_panel_cli_args("list-tools"), ["list-tools"])

    def test_dynamic_root_args_still_include_explicit_root(self) -> None:
        demo_root = str(Path("E:/demo_root"))
        args = build_engineering_safety_panel_cli_args("evidence-freshness", demo_root)
        self.assertEqual(args, ["evidence-freshness", "--root", demo_root])


if __name__ == "__main__":
    unittest.main()
