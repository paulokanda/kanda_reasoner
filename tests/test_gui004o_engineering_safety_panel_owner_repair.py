"""Focused tests for GUI004O Engineering Safety panel owner repair."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "reasoner_tools_gui_engineering_safety_panel_commands.py"


def _public_helper_names() -> list[str]:
    source = HELPER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    public_names: list[str] = []
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
            public_names.append(name)
    return public_names


def test_gui004o_helper_has_no_public_owner_symbols() -> None:
    assert _public_helper_names() == []


def test_gui004o_panel_public_contracts_still_work() -> None:
    import reasoner_tools_gui_engineering_safety_panel as panel

    raw_command = panel.build_engineering_safety_panel_command("risk-radar")
    assert raw_command[0] == "risk-radar"
    assert raw_command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]

    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status_code == 0
    assert result.status == 0 or result.status == "ok"
    assert "risk-radar" in result.stdout


def main() -> None:
    test_gui004o_helper_has_no_public_owner_symbols()
    test_gui004o_panel_public_contracts_still_work()
    print("GUI004O Engineering Safety panel owner repair tests passed.")


if __name__ == "__main__":
    main()
