"""Focused tests for GUI004H Engineering Safety panel command cleanup."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004h_raw_and_legacy_display_contracts_both_hold() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]


def test_gui004h_result_status_code_alias_is_available() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "list-tools" in result.stdout


def test_gui004h_panel_module_stays_under_split_threshold() -> None:
    path = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
    line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    assert line_count <= 500, line_count


def main() -> None:
    test_gui004h_raw_and_legacy_display_contracts_both_hold()
    test_gui004h_result_status_code_alias_is_available()
    test_gui004h_panel_module_stays_under_split_threshold()
    print("GUI004H Engineering Safety panel command cleanup tests passed.")


if __name__ == "__main__":
    main()
