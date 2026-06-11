"""Focused tests for GUI004R Engineering Safety panel import repair."""

from __future__ import annotations

import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gui004r_private_helper_has_direct_test_import() -> None:
    """Directly import the private helper so architecture protection is visible."""
    helper = importlib.import_module("_reasoner_tools_gui_engineering_safety_panel_commands")
    assert hasattr(helper, "_build_cli_args")
    assert hasattr(helper, "_build_display_command")
    assert hasattr(helper, "_run_command")


def test_gui004r_panel_imports_cleanly_after_import_repair() -> None:
    """The public panel module must import after moving the helper import."""
    panel = importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
    assert hasattr(panel, "build_engineering_safety_panel_command")
    assert hasattr(panel, "build_engineering_safety_panel_cli_args")
    assert hasattr(panel, "run_engineering_safety_panel_command")


def test_gui004r_command_contracts_survive_import_repair() -> None:
    """Both legacy display equality and raw CLI indexing remain available."""
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


def test_gui004r_public_helper_is_retired_stub() -> None:
    """The old public helper should not expose ownership symbols."""
    helper = importlib.import_module("reasoner_tools_gui_engineering_safety_panel_commands")
    forbidden = {
        "DEFAULT_PROJECT_ROOT",
        "build_engineering_safety_panel_command",
        "build_engineering_safety_panel_cli_args",
    }
    visible = set(dir(helper))
    assert not (forbidden & visible)


def main() -> None:
    """Run focused tests without pytest."""
    test_gui004r_private_helper_has_direct_test_import()
    test_gui004r_panel_imports_cleanly_after_import_repair()
    test_gui004r_command_contracts_survive_import_repair()
    test_gui004r_public_helper_is_retired_stub()
    print("GUI004R Engineering Safety panel import repair tests passed.")


if __name__ == "__main__":
    main()
