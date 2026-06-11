"""Focused tests for GUI004N command owner repair."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def _public_helper_names() -> list[str]:
    helper = ROOT / "reasoner_tools_gui_engineering_safety_panel_commands.py"
    tree = ast.parse(helper.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in tree.body:
        name = None
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
        if name and not name.startswith("_") and name != "__all__":
            names.append(name)
    return sorted(names)


def test_gui004n_helper_exports_no_public_owner_symbols() -> None:
    assert _public_helper_names() == []


def test_gui004n_panel_keeps_public_command_contracts() -> None:
    display = panel.build_engineering_safety_panel_command("risk-radar")
    assert display == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]
    runnable = panel.build_engineering_safety_panel_cli_args("risk-radar", project_root=str(ROOT))
    assert runnable[0] == "risk-radar"
    assert runnable == display


def test_gui004n_result_status_code_alias() -> None:
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=str(ROOT))
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def main() -> None:
    test_gui004n_helper_exports_no_public_owner_symbols()
    test_gui004n_panel_keeps_public_command_contracts()
    test_gui004n_result_status_code_alias()
    print("GUI004N Engineering Safety panel command owner repair tests passed.")


if __name__ == "__main__":
    main()
