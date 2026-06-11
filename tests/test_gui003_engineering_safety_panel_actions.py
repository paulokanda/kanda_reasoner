"""Focused tests for GUI003 Engineering Safety panel button actions."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel  # noqa: E402


def test_gui003_known_commands_have_runnable_default_args() -> None:
    catalog = panel.get_engineering_safety_panel_catalog()
    for tool in catalog:
        argv = panel.build_engineering_safety_panel_cli_args(tool.command_name, project_root=ROOT)
        assert argv
        assert argv[0] == tool.command_name


def test_gui003_list_tools_button_action_runs_cli() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status_code == 0
    assert "risk-radar" in result.stdout
    assert "property-test" in result.stdout
    assert result.stderr == ""


def test_gui003_risk_radar_button_action_runs_with_defaults() -> None:
    result = panel.run_engineering_safety_panel_command("risk-radar", project_root=ROOT)
    assert result.status_code == 0
    assert "Risk Change Radar" in result.stdout or "risk_change_radar" in result.stdout
    assert "reasoner_tools_gui_engineering_safety_panel.py" in result.stdout


def test_gui003_existing_display_command_contract_is_preserved() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]


def main() -> None:
    test_gui003_known_commands_have_runnable_default_args()
    test_gui003_list_tools_button_action_runs_cli()
    test_gui003_risk_radar_button_action_runs_with_defaults()
    test_gui003_existing_display_command_contract_is_preserved()
    print("GUI003 Engineering Safety panel action tests passed.")


if __name__ == "__main__":
    main()
