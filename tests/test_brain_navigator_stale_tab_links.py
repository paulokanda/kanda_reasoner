"""Brain Navigator stale tab-link protection and coverage report tests."""

from __future__ import annotations

from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
VISIBLE_TAB_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "brain_navigator"
    / "_visible_neural_architecture_tab.py"
)
FALLBACK_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "brain_navigator"
    / "_fallback_index_widget.py"
)
MAIN_WINDOW_PATH = (
    PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "main_window.py"
)


def _registry_tab_ids() -> set[str]:
    from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

    return {str(spec.tab_id) for spec in TOOLS if getattr(spec, "tab_id", None)}


def _mapped_tab_ids() -> set[str]:
    from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
        list_brain_region_targets,
    )

    return {
        target.target_tab_id
        for target in list_brain_region_targets()
        if target.target_tab_id
    }


def test_no_brain_circle_links_missing_tabs_now() -> None:
    """Current circle links should all resolve to registered tabs."""
    missing_tab_ids = sorted(_mapped_tab_ids() - _registry_tab_ids())

    assert missing_tab_ids == []


def test_registered_tabs_not_linked_to_any_brain_circle_are_explicit() -> None:
    """Report registered tabs that currently have no circle mapping."""
    unlinked_tab_ids = sorted(_registry_tab_ids() - _mapped_tab_ids())

    assert unlinked_tab_ids == ["brain_navigator"]


def test_visible_brain_refuses_stale_registered_tab_links() -> None:
    """Unavailable mapped tabs should leave the circle visible but inert."""
    from kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator._visible_neural_architecture_tab import (
        open_mapped_tab_by_region_id,
    )

    opened: list[str] = []

    def open_tab(tab_id: str) -> str:
        opened.append(tab_id)
        return tab_id

    result = open_mapped_tab_by_region_id(
        "frontal_lobe",
        open_tab,
        can_open_tab_id=lambda _tab_id: False,
    )

    assert result is None
    assert opened == []


def test_brain_navigator_receives_tab_availability_callback() -> None:
    """The main window should inject both open and can-open callbacks."""
    main_window_source = MAIN_WINDOW_PATH.read_text(encoding="utf-8")
    visible_source = VISIBLE_TAB_PATH.read_text(encoding="utf-8")
    fallback_source = FALLBACK_PATH.read_text(encoding="utf-8")

    assert "can_open_tab_id=self._tab_navigation_controller.can_open_tab" in main_window_source
    assert "can_open_tab_id: CanOpenTabId | None = None" in visible_source
    assert "not can_open_tab_id(target.target_tab_id)" in visible_source
    assert "can_open_tab_id: CanOpenTabId | None = None" in fallback_source
    assert "self._can_open_tab_id = self._config.can_open_tab_id" in fallback_source


if __name__ == "__main__":
    test_no_brain_circle_links_missing_tabs_now()
    test_registered_tabs_not_linked_to_any_brain_circle_are_explicit()
    test_visible_brain_refuses_stale_registered_tab_links()
    test_brain_navigator_receives_tab_availability_callback()
    print("Brain Navigator stale tab-link tests passed.")
