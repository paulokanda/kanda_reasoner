"""Focused tests for GUI004G Engineering Safety panel command contract."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004g_display_command_contract_without_project_root() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]


def test_gui004g_runnable_shadow_audit_command_uses_project_root() -> None:
    command = panel.build_engineering_safety_panel_cli_args(
        "shadow-audit",
        project_root=ROOT,
    )
    assert command[:3] == ["shadow-audit", "--root", str(ROOT)]


def test_gui004g_release_notes_includes_title() -> None:
    command = panel.build_engineering_safety_panel_cli_args(
        "release-notes",
        project_root=ROOT,
    )
    assert "--title" in command


def test_gui004g_result_has_status_code_alias() -> None:
    result = panel.run_engineering_safety_panel_command(
        "list-tools",
        project_root=ROOT,
    )
    assert result.status_code == 0
    assert result.status == 0


def main() -> None:
    test_gui004g_display_command_contract_without_project_root()
    test_gui004g_runnable_shadow_audit_command_uses_project_root()
    test_gui004g_release_notes_includes_title()
    test_gui004g_result_has_status_code_alias()
    print("GUI004G Engineering Safety panel command contract tests passed.")


if __name__ == "__main__":
    main()
