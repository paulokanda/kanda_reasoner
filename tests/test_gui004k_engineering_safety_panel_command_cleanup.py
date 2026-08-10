"""GUI004K tests for Engineering Safety panel command cleanup."""

from __future__ import annotations

from pathlib import Path

import reasoner_tools_gui_engineering_safety_panel as panel

ROOT = Path(__file__).resolve().parents[1]


def test_gui004k_raw_and_legacy_command_contracts() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]
    assert panel.build_engineering_safety_panel_cli_args("risk-radar", project_root=ROOT)[0] == "risk-radar"


def test_gui004k_result_status_aliases() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def test_gui004k_panel_is_under_split_threshold() -> None:
    line_count = len((ROOT / "reasoner_tools_gui_engineering_safety_panel.py").read_text(encoding="utf-8").splitlines())
    assert line_count <= 500, line_count


def main() -> None:
    test_gui004k_raw_and_legacy_command_contracts()
    test_gui004k_result_status_aliases()
    test_gui004k_panel_is_under_split_threshold()
    print("GUI004K Engineering Safety panel command cleanup tests passed.")


if __name__ == "__main__":
    main()
