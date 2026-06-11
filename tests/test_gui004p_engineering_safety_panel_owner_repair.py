"""Focused checks for GUI004P owner repair."""

from __future__ import annotations

import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _public_helper_names() -> list[str]:
    helper = importlib.import_module("reasoner_tools_gui_engineering_safety_panel_commands")
    names = []
    for name in dir(helper):
        if name.startswith("_"):
            continue
        value = getattr(helper, name)
        module_name = getattr(value, "__module__", "")
        if module_name == helper.__name__:
            names.append(name)
    return sorted(names)


def test_gui004p_helper_has_no_public_owned_symbols() -> None:
    assert _public_helper_names() == []


def test_gui004p_panel_owns_public_command_contracts() -> None:
    panel = importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]
    args = panel.build_engineering_safety_panel_cli_args("risk-radar", project_root=ROOT)
    assert args[0] == "risk-radar"
    assert "--root" in args
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status_code == 0
    assert result.status == 0
    assert "risk-radar" in result.stdout


def main() -> None:
    test_gui004p_helper_has_no_public_owned_symbols()
    test_gui004p_panel_owns_public_command_contracts()
    print("GUI004P Engineering Safety panel owner repair tests passed.")


if __name__ == "__main__":
    main()
