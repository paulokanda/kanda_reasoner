"""Focused test for GUI004B Engineering Safety panel action compatibility."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004b_restores_run_engineering_safety_panel_command() -> None:
    """The GUI003 public action helper remains available after GUI004."""
    runner = getattr(panel, "run_engineering_safety_panel_command")
    result = runner("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.status_code == 0
    assert "list-tools" in result.arguments
    assert "api-contract" in result.stdout


def main() -> None:
    """Run focused tests without requiring pytest."""
    test_gui004b_restores_run_engineering_safety_panel_command()
    print("GUI004B Engineering Safety panel action compatibility tests passed.")


if __name__ == "__main__":
    main()
