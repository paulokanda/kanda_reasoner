"""Characterization tests for Freeze tab path-control mixin."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update_gui._path_controls import FreezePathControlsMixin
from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
    FreezeAfterUpdateTab,
)


class _DummyLineEdit:
    def __init__(self) -> None:
        self.value = ""

    def text(self) -> str:
        return self.value

    def setText(self, value: str) -> None:
        self.value = value


class _DummyButton:
    def __init__(self, name: str) -> None:
        self.name = name
        self.tooltip = ""

    def setToolTip(self, value: str) -> None:
        self.tooltip = value


class _DummyLayout:
    def __init__(self) -> None:
        self.items: list[object] = []

    def addSpacing(self, value: int) -> None:
        self.items.append(("spacing", value))

    def addWidget(self, widget: object, stretch: int = 0) -> None:
        self.items.append(("widget", widget, stretch))

    def insertSpacing(self, index: int, value: int) -> None:
        self.items.insert(index, ("spacing", value))

    def insertWidget(self, index: int, widget: object, stretch: int = 0) -> None:
        self.items.insert(index, ("widget", widget, stretch))


class _DummyPathControls(FreezePathControlsMixin):
    def __init__(self) -> None:
        self.project_root_header_label = object()
        self.project_root_edit = _DummyLineEdit()
        self.search_project_button = _DummyButton("search")
        self.box_folder_button = _DummyButton("box")
        self.external_ai_review_folder_button = _DummyButton("external")
        self.help_button = _DummyButton("help")
        self._project_root_controls_moved = False
        self._last_output_folder = None
        self.logged: list[str] = []

    def _append_log(self, message: str) -> None:
        self.logged.append(message)


def test_path_controls_mixin_stays_below_facade_and_import_compatible() -> None:
    source = Path(sys.modules[FreezePathControlsMixin.__module__].__file__).read_text(encoding="utf-8")

    assert issubclass(FreezeAfterUpdateTab, FreezePathControlsMixin)
    assert hasattr(FreezeAfterUpdateTab, "set_project_root")
    assert hasattr(FreezeAfterUpdateTab, "move_project_root_controls_to_layout")
    assert "freeze_after_update_tab" not in source
    assert "__all__ = [\"FreezePathControlsMixin\"]" in source


def test_set_project_root_updates_edit_and_derived_tooltips() -> None:
    dummy = _DummyPathControls()
    project_root = PROJECT_ROOT

    dummy.set_project_root(project_root)

    assert dummy.project_root_edit.text() == str(project_root.resolve(strict=False))
    assert "project_freeze_after_update" in dummy.box_folder_button.tooltip
    assert "files_to_send_ai" in dummy.external_ai_review_folder_button.tooltip


def test_move_project_root_controls_marks_controls_as_moved_once() -> None:
    dummy = _DummyPathControls()
    layout = _DummyLayout()

    dummy.move_project_root_controls_to_layout(layout)
    dummy.move_project_root_controls_to_layout(layout)

    assert dummy._project_root_controls_moved is True
    assert len([item for item in layout.items if item[0] == "widget"]) == 6


def main() -> int:
    test_path_controls_mixin_stays_below_facade_and_import_compatible()
    test_set_project_root_updates_edit_and_derived_tooltips()
    test_move_project_root_controls_marks_controls_as_moved_once()
    print("VALIDATION OK: freeze-after-update-path-controls-refactor")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
