"""Public-contract test for Tab 3 layout builder facade."""

from __future__ import annotations

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder import (
    build_ui,
    set_ai_controls_enabled,
    wire_events,
)


def test_layout_builder_public_contract_imports() -> None:
    """Verify Tab 3 layout facade public symbols remain importable."""
    assert callable(build_ui)
    assert callable(wire_events)
    assert callable(set_ai_controls_enabled)


def main() -> int:
    """Run Tab 3 layout builder public-contract test without pytest."""
    test_layout_builder_public_contract_imports()
    print("Tab 3 layout builder public contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
