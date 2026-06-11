"""Focused tests for GUI004D Engineering Safety panel status compatibility."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004d_status_code_alias_is_available() -> None:
    """The older GUI003 public result contract exposes status_code."""
    result = panel.run_engineering_safety_panel_command("list-tools", project_root=ROOT)
    assert result.status_code == 0
    assert "list-tools" in result.stdout


def test_gui004d_panel_module_stays_under_split_threshold() -> None:
    """The panel module remains below the architecture split threshold."""
    panel_path = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"
    line_count = len(panel_path.read_text(encoding="utf-8").splitlines())
    assert line_count <= 500, line_count


def main() -> None:
    test_gui004d_status_code_alias_is_available()
    test_gui004d_panel_module_stays_under_split_threshold()
    print("GUI004D Engineering Safety panel status compatibility tests passed.")


if __name__ == "__main__":
    main()
