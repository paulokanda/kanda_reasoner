"""Focused tests for GUI004S Engineering Safety panel owner/import repair."""

from __future__ import annotations

import importlib
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _public_names(module):
    names = []
    for name, value in vars(module).items():
        if name.startswith("_"):
            continue
        if name == "__all__":
            continue
        if getattr(value, "__module__", None) == module.__name__:
            names.append(name)
    return sorted(names)


def test_gui004s_private_helper_imports_directly():
    helper = importlib.import_module("_reasoner_tools_gui_engineering_safety_panel_commands")
    assert helper.__all__ == []
    assert helper._build_cli_args("risk-radar")[0] == "risk-radar"


def test_gui004s_public_helper_is_retired():
    helper = importlib.import_module("reasoner_tools_gui_engineering_safety_panel_commands")
    assert helper.__all__ == []
    assert _public_names(helper) == []


def test_gui004s_panel_owns_public_wrappers():
    panel = importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
    assert panel.build_engineering_safety_panel_command("risk-radar")[0] == "risk-radar"
    assert panel.build_engineering_safety_panel_command("risk-radar") == [
        "python",
        "-m",
        "kanda_reasoner_app.safety_suite_cli.commands",
        "risk-radar",
    ]
    assert panel.build_engineering_safety_panel_cli_args("risk-radar")[0] == "risk-radar"
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status_code == 0
    assert "risk-radar" in result.stdout


def main() -> None:
    test_gui004s_private_helper_imports_directly()
    test_gui004s_public_helper_is_retired()
    test_gui004s_panel_owns_public_wrappers()
    print("GUI004S Engineering Safety panel owner/import repair tests passed.")


if __name__ == "__main__":
    main()
