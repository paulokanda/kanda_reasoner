"Focused test for GUI002R Engineering Safety tab registration."

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def test_gui002r_engineering_safety_tab_is_registered_once() -> None:
    """The public GUI tool list exposes exactly one Engineering Safety tab."""
    import reasoner_tools_gui
    from kanda_reasoner_app.reasoner_tools_gui_shell import tool_specs

    public_tools = tuple(reasoner_tools_gui.TOOLS)
    owner_tools = tuple(tool_specs.TOOLS)

    public_titles = [getattr(item, "step_title", "") for item in public_tools]
    owner_titles = [getattr(item, "step_title", "") for item in owner_tools]

    assert public_titles.count("Engineering Safety") == 1, public_titles
    assert owner_titles.count("Engineering Safety") == 1, owner_titles

    matching = [
        item for item in public_tools
        if getattr(item, "step_title", "") == "Engineering Safety"
    ]
    assert len(matching) == 1

    spec = matching[0]
    assert spec.module_candidates == ("reasoner_tools_gui_engineering_safety_panel",)
    assert spec.class_candidates == ("create_engineering_safety_panel",)
    assert spec.source_hint == "reasoner_tools_gui_engineering_safety_panel.py"


def test_gui002r_panel_factory_is_importable() -> None:
    """The registered panel factory can be imported without starting the GUI."""
    import reasoner_tools_gui_engineering_safety_panel as panel

    assert hasattr(panel, "create_engineering_safety_panel")
    assert callable(panel.create_engineering_safety_panel)


def main() -> None:
    """Run focused tests without pytest."""
    test_gui002r_engineering_safety_tab_is_registered_once()
    test_gui002r_panel_factory_is_importable()
    print("GUI002R Engineering Safety tab wiring tests passed.")


if __name__ == "__main__":
    main()
