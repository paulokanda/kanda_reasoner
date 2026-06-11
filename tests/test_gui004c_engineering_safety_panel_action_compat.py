"""Focused tests for GUI004C Engineering Safety panel action compatibility."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import reasoner_tools_gui_engineering_safety_panel as panel


def test_gui004c_restores_public_runner() -> None:
    """The legacy GUI003 action API should be present and runnable."""
    runner = getattr(panel, "run_engineering_safety_panel_command")
    result = runner("list-tools", project_root=ROOT)
    assert result.status == 0
    assert result.command == "list-tools"
    assert "api-contract" in result.stdout
    assert "list-tools" in result.stdout


def test_gui004c_runner_is_exported_when_all_exists() -> None:
    """Public compatibility function should remain in __all__."""
    exported = tuple(getattr(panel, "__all__", ()))
    assert "run_engineering_safety_panel_command" in exported


def main() -> None:
    """Run focused tests without pytest."""
    test_gui004c_restores_public_runner()
    test_gui004c_runner_is_exported_when_all_exists()
    print("GUI004C Engineering Safety panel action compatibility tests passed.")


if __name__ == "__main__":
    main()
