"""Focused tests for GUI004L Engineering Safety panel command cleanup."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004l_raw_and_legacy_command_contracts() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]


def test_gui004l_result_contract_and_list_tools() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def test_gui004l_panel_module_stays_under_split_threshold() -> None:
    path = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
    assert len(path.read_text(encoding="utf-8").splitlines()) <= 500


def main() -> None:
    test_gui004l_raw_and_legacy_command_contracts()
    test_gui004l_result_contract_and_list_tools()
    test_gui004l_panel_module_stays_under_split_threshold()
    print("GUI004L Engineering Safety panel command cleanup tests passed.")


if __name__ == "__main__":
    main()
