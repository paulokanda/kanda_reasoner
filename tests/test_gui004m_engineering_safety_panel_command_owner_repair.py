"""Focused tests for GUI004M command owner repair."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel
import reasoner_tools_gui_engineering_safety_panel_commands as helper


def test_gui004m_command_contracts_are_preserved() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]

    args = panel.build_engineering_safety_panel_cli_args("shadow-audit", project_root=ROOT)
    assert args[0] == "shadow-audit"
    assert "--root" in args


def test_gui004m_runner_result_contract_is_preserved() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def test_gui004m_helper_has_no_public_owner_collisions() -> None:
    public_helper_names = [
        name for name in dir(helper)
        if not name.startswith("_") and name not in {"annotations"}
    ]
    assert public_helper_names == []


def test_gui004m_panel_file_stays_below_split_threshold() -> None:
    line_count = len((ROOT / "reasoner_tools_gui_engineering_safety_panel.py").read_text(encoding="utf-8").splitlines())
    assert line_count <= 500, line_count


def main() -> None:
    test_gui004m_command_contracts_are_preserved()
    test_gui004m_runner_result_contract_is_preserved()
    test_gui004m_helper_has_no_public_owner_collisions()
    test_gui004m_panel_file_stays_below_split_threshold()
    print("GUI004M Engineering Safety panel command owner repair tests passed.")


if __name__ == "__main__":
    main()
