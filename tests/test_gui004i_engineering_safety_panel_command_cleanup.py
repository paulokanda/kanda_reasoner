"""Final compact command compatibility tests for the Engineering Safety panel."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004i_raw_and_legacy_command_contracts() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]


def test_gui004i_run_result_status_alias() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def test_gui004i_panel_stays_under_split_threshold() -> None:
    target = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
    line_count = len(target.read_text(encoding="utf-8").splitlines())
    assert line_count <= 500, line_count


def main() -> None:
    test_gui004i_raw_and_legacy_command_contracts()
    test_gui004i_run_result_status_alias()
    test_gui004i_panel_stays_under_split_threshold()
    print("GUI004I Engineering Safety panel command cleanup tests passed.")


if __name__ == "__main__":
    main()
