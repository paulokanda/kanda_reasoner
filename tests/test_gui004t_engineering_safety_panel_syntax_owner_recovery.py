"""Focused tests for GUI004T Engineering Safety panel syntax/owner recovery."""

from __future__ import annotations

import importlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _public_names(module_name: str) -> list[str]:
    module = importlib.import_module(module_name)
    ignored = {"annotations"}
    return sorted(
        name for name in vars(module)
        if not name.startswith("_") and name not in ignored
    )


def test_gui004t_panel_imports_and_public_contracts_work() -> None:
    panel = importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
    command = panel.build_engineering_safety_panel_command("risk-radar")
    assert command[0] == "risk-radar"
    assert command == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=str(ROOT))
    assert result.status == 0
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def test_gui004t_public_helper_is_retired() -> None:
    assert _public_names("reasoner_tools_gui_engineering_safety_panel_commands") == []


def test_gui004t_private_helper_has_only_private_symbols() -> None:
    assert _public_names("_reasoner_tools_gui_engineering_safety_panel_commands") == []


def test_gui004t_panel_stays_under_architecture_split_threshold() -> None:
    panel_path = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
    assert len(panel_path.read_text(encoding="utf-8").splitlines()) <= 500


def main() -> None:
    test_gui004t_panel_imports_and_public_contracts_work()
    test_gui004t_public_helper_is_retired()
    test_gui004t_private_helper_has_only_private_symbols()
    test_gui004t_panel_stays_under_architecture_split_threshold()
    print("GUI004T Engineering Safety panel syntax/owner recovery tests passed.")


if __name__ == "__main__":
    main()
