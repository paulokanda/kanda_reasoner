"""Focused tests for GUI004Q Engineering Safety panel owner repair."""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_HELPER = ROOT / "reasoner_tools_gui_engineering_safety_panel_commands.py"
PRIVATE_HELPER = ROOT / "_reasoner_tools_gui_engineering_safety_panel_commands.py"


def _public_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    names.append(target.id)
    return names


def test_gui004q_retired_public_helper_has_no_public_symbols() -> None:
    assert OLD_HELPER.exists()
    assert _public_names(OLD_HELPER) == []


def test_gui004q_private_helper_uses_private_symbols() -> None:
    assert PRIVATE_HELPER.exists()
    public = [name for name in _public_names(PRIVATE_HELPER) if name != "__all__"]
    assert public == []


def test_gui004q_panel_remains_public_owner() -> None:
    panel = importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
    assert hasattr(panel, "build_engineering_safety_panel_command")
    assert hasattr(panel, "build_engineering_safety_panel_cli_args")
    assert hasattr(panel, "run_engineering_safety_panel_command")
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]
    assert panel.build_engineering_safety_panel_cli_args("risk-radar")[0] == "risk-radar"


def test_gui004q_list_tools_result_contract() -> None:
    panel = importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
    result = panel.run_engineering_safety_panel_command("list-tools")
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def main() -> None:
    test_gui004q_retired_public_helper_has_no_public_symbols()
    test_gui004q_private_helper_uses_private_symbols()
    test_gui004q_panel_remains_public_owner()
    test_gui004q_list_tools_result_contract()
    print("GUI004Q Engineering Safety panel owner repair tests passed.")


if __name__ == "__main__":
    main()
