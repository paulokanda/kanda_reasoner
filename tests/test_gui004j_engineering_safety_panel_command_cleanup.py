"""GUI004J focused tests for Engineering Safety panel command cleanup."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel
import reasoner_tools_gui_engineering_safety_panel_commands as commands


def test_gui004j_raw_and_legacy_command_contracts() -> None:
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]


def test_gui004j_release_notes_has_title_argument() -> None:
    args = panel.build_engineering_safety_panel_cli_args("release-notes", ROOT)
    assert args[0] == "release-notes"
    assert "--title" in args


def test_gui004j_result_status_code_alias() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def test_gui004j_panel_module_stays_under_split_threshold() -> None:
    target = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
    assert len(target.read_text(encoding="utf-8").splitlines()) <= 500


def test_gui004j_helper_public_contract() -> None:
    assert commands.build_engineering_safety_panel_cli_args("shadow-audit", ROOT)[0] == "shadow-audit"


def main() -> None:
    test_gui004j_raw_and_legacy_command_contracts()
    test_gui004j_release_notes_has_title_argument()
    test_gui004j_result_status_code_alias()
    test_gui004j_panel_module_stays_under_split_threshold()
    test_gui004j_helper_public_contract()
    print("GUI004J Engineering Safety panel command cleanup tests passed.")


if __name__ == "__main__":
    main()
