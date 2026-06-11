"""Focused import protection for the private Engineering Safety panel command helper."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_private_engineering_safety_panel_commands_imports() -> None:
    """The private helper must stay import-safe and available through panel tests."""
    helper = importlib.import_module("_reasoner_tools_gui_engineering_safety_panel_commands")
    assert hasattr(helper, "_build_cli_args")
    assert hasattr(helper, "_run_command")


def test_private_engineering_safety_panel_commands_are_private() -> None:
    """Helper implementation names should remain private to avoid public ownership collisions."""
    helper = importlib.import_module("_reasoner_tools_gui_engineering_safety_panel_commands")
    public_names = [
        name
        for name in dir(helper)
        if not name.startswith("_") and name not in {"annotations"}
    ]
    assert public_names == []


def main() -> None:
    """Run tests without pytest."""
    test_private_engineering_safety_panel_commands_imports()
    test_private_engineering_safety_panel_commands_are_private()
    print("Private Engineering Safety panel command helper tests passed.")


if __name__ == "__main__":
    main()
