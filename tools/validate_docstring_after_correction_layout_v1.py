#!/usr/bin/env python3
"""Validate the Docstring Assistant After Correction multi-row layout."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import types
from pathlib import Path
from types import SimpleNamespace

FEATURE_ID = "docstring-assistant-after-correction-layout-v1"


def require(condition: bool, message: str) -> None:
    """Raise one focused validation failure."""
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    """Return one UTF-8 project source file."""
    return (root / relative).read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    """Validate source-level layout, ownership, and window-size contracts."""
    relative = "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py"
    layout = read(root, relative)
    state = read(
        root,
        "kanda_reasoner_app/insert_missing_docstrings_gui/"
        "insert_missing_docstrings_gui_help/window_state.py",
    )

    require('QGroupBox("After Correction")' in layout, "After Correction group missing")
    require("QGridLayout" in layout, "multi-row grid owner missing")
    require("_build_after_correction_grid" in layout, "grid helper missing")
    require("setColumnStretch(0, 1)" in layout, "first action column is not flexible")
    require("setColumnStretch(1, 1)" in layout, "second action column is not flexible")
    require("size_policy_cls.Expanding" in layout, "buttons are not horizontally expanding")
    require("size_policy_cls.Fixed" in layout, "button heights are not fixed")
    require("draft_action_row = QHBoxLayout()" not in layout, "legacy draft row remains")
    require("review_decision_row = QHBoxLayout()" not in layout, "legacy decision row remains")

    expected_buttons = (
        "_review_generate_draft_button",
        "_review_generate_visible_drafts_button",
        "_review_generate_all_drafts_button",
        "_review_stop_ai_drafts_button",
        "_review_undo_bulk_drafts_button",
        "_review_save_change_button",
        "_review_approve_row_button",
        "_review_reject_row_button",
        "_review_undo_button",
        "_review_save_all_button",
    )
    for marker in expected_buttons:
        require(marker in layout, "After Correction action missing: " + marker)

    require("self.resize(1360, 860)" in state, "main Docstring GUI size changed")
    line_count = len(layout.splitlines())
    require(line_count <= 500, f"layout_runtime.py exceeds 500 lines: {line_count}")

    print("DOCSTRING_AFTER_CORRECTION_MULTIROW_LAYOUT: PASS")
    print("DOCSTRING_AFTER_CORRECTION_TWO_COLUMN_REFLOW: PASS")
    print("DOCSTRING_AFTER_CORRECTION_EXPANDING_BUTTONS: PASS")
    print("DOCSTRING_AFTER_CORRECTION_ACTIONS_PRESERVED: PASS")
    print("DOCSTRING_MAIN_GUI_SIZE_UNCHANGED: PASS")
    print("DOCSTRING_LAYOUT_MODULE_SIZE_GATE: PASS")


class FakeSizePolicy:
    """Minimal QSizePolicy constants used by the layout runtime."""

    Ignored = "ignored"
    Expanding = "expanding"
    Fixed = "fixed"


class FakeWidget:
    """Minimal widget surface for deterministic layout validation."""

    def __init__(self, *args: object) -> None:
        self.args = args
        self.layout = None
        self.minimum_width = None
        self.size_policy = None
        self.enabled = True
        self.hidden = False

    def setMinimumWidth(self, value: int) -> None:
        self.minimum_width = value

    def setSizePolicy(self, horizontal: object, vertical: object) -> None:
        self.size_policy = (horizontal, vertical)

    def setReadOnly(self, _value: bool) -> None:
        return None

    def setLineWrapMode(self, _value: object) -> None:
        return None

    def setStyleSheet(self, _value: str) -> None:
        return None

    def setEnabled(self, value: bool) -> None:
        self.enabled = value

    def hide(self) -> None:
        self.hidden = True


class FakePlainTextEdit(FakeWidget):
    """Fake QPlainTextEdit with the required wrap constant."""

    WidgetWidth = "widget-width"


class FakeLayout:
    """Collect layout children and grid placements."""

    def __init__(self, parent: object | None = None) -> None:
        self.items: list[tuple[str, object, tuple[object, ...]]] = []
        self.column_stretch: dict[int, int] = {}
        self.horizontal_spacing = None
        self.vertical_spacing = None
        self.spacing = None
        if parent is not None:
            parent.layout = self

    def addWidget(self, widget: object, *args: object) -> None:
        self.items.append(("widget", widget, args))

    def addLayout(self, layout: object, *args: object) -> None:
        self.items.append(("layout", layout, args))

    def addStretch(self, *args: object) -> None:
        self.items.append(("stretch", args, ()))

    def addSpacing(self, value: int) -> None:
        self.items.append(("spacing", value, ()))

    def setColumnStretch(self, column: int, stretch: int) -> None:
        self.column_stretch[column] = stretch

    def setHorizontalSpacing(self, value: int) -> None:
        self.horizontal_spacing = value

    def setVerticalSpacing(self, value: int) -> None:
        self.vertical_spacing = value

    def setSpacing(self, value: int) -> None:
        self.spacing = value


class FakeSplitter(FakeWidget):
    """Collect splitter children."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.children: list[object] = []

    def addWidget(self, widget: object) -> None:
        self.children.append(widget)

    def setStretchFactor(self, *_args: object) -> None:
        return None

    def setSizes(self, *_args: object) -> None:
        return None


class FakeTabs(FakeWidget):
    """Collect tab pages."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.tabs: list[tuple[object, str]] = []

    def addTab(self, widget: object, title: str) -> None:
        self.tabs.append((widget, title))


class FakeGroupBox(FakeWidget):
    """Store a visible group title."""

    def __init__(self, title: str = "") -> None:
        super().__init__(title)
        self.title = title


def fake_qt_module() -> types.ModuleType:
    """Return a minimal PySide6.QtWidgets replacement."""
    module = types.ModuleType("PySide6.QtWidgets")
    module.QGridLayout = FakeLayout
    module.QGroupBox = FakeGroupBox
    module.QHBoxLayout = FakeLayout
    module.QLabel = FakeWidget
    module.QPlainTextEdit = FakePlainTextEdit
    module.QSizePolicy = FakeSizePolicy
    module.QPushButton = FakeWidget
    module.QSplitter = FakeSplitter
    module.QTabWidget = FakeTabs
    module.QVBoxLayout = FakeLayout
    module.QWidget = FakeWidget
    return module


def load_layout_module(root: Path) -> object:
    """Load the runtime against the deterministic fake Qt module."""
    pyside = types.ModuleType("PySide6")
    qt_widgets = fake_qt_module()
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtWidgets"] = qt_widgets

    path = root / "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py"
    spec = importlib.util.spec_from_file_location("layout_runtime_under_test", path)
    require(spec is not None and spec.loader is not None, "layout module spec failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_runtime(root: Path) -> None:
    """Build the panel and verify real row/column placement contracts."""
    module = load_layout_module(root)
    window = SimpleNamespace(
        _review_summary=FakeWidget(),
        _review_filter_combo=FakeWidget(),
        _review_list=FakeWidget(),
    )
    tabs = module._build_review_panel(window)
    require(len(tabs.tabs) == 1, "review tab count changed")
    review_tab, title = tabs.tabs[0]
    require(title == "Review and Correct Missing Docstrings", "review tab title changed")

    splitter = next(
        item[1]
        for item in review_tab.layout.items
        if item[0] == "widget" and isinstance(item[1], FakeSplitter)
    )
    require(len(splitter.children) == 2, "before/after splitter structure changed")
    after_group = splitter.children[1]
    require(after_group.title == "After Correction", "After Correction group moved")

    grids = [item[1] for item in after_group.layout.items if item[0] == "layout"]
    require(len(grids) == 2, "expected two action grids")
    draft_grid, decision_grid = grids

    require(len(draft_grid.items) == 5, "draft action count changed")
    require(len(decision_grid.items) == 5, "decision action count changed")
    require(draft_grid.column_stretch == {0: 1, 1: 1}, "draft columns not balanced")
    require(decision_grid.column_stretch == {0: 1, 1: 1}, "decision columns not balanced")

    draft_positions = [item[2] for item in draft_grid.items]
    decision_positions = [item[2] for item in decision_grid.items]
    require(draft_positions == [(0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 1),
                                (1, 1, 1, 1), (2, 0, 1, 2)],
            "draft action positions changed")
    require(decision_positions == [(0, 0, 1, 1), (0, 1, 1, 1), (1, 0, 1, 1),
                                   (1, 1, 1, 1), (2, 0, 1, 2)],
            "decision action positions changed")

    action_buttons = [item[1] for item in draft_grid.items + decision_grid.items]
    for button in action_buttons:
        require(button.minimum_width == 0, "button minimum width forces GUI growth")
        require(
            button.size_policy == (FakeSizePolicy.Expanding, FakeSizePolicy.Fixed),
            "button size policy does not preserve full label space",
        )

    print("DOCSTRING_AFTER_CORRECTION_RUNTIME_GRID: PASS")
    print("DOCSTRING_AFTER_CORRECTION_ALL_BUTTONS_VISIBLE: PASS")
    print("DOCSTRING_AFTER_CORRECTION_MAIN_WIDTH_PRESSURE_RELIEVED: PASS")



def validate_real_qt(root: Path) -> None:
    """Confirm complete button labels at the canonical 1360 x 860 window size."""
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication, QGroupBox
    except ImportError:
        print("REAL_QT_DOCSTRING_AFTER_CORRECTION_LAYOUT: SKIPPED_NO_PYSIDE6")
        return

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui import (
        MissingDocstringsWindow,
    )

    existing_app = QApplication.instance()
    created_app = existing_app is None
    app = existing_app or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = MissingDocstringsWindow()
    try:
        window.show()
        app.processEvents()
        require(window.size().width() == 1360, "Docstring main-window width changed")
        require(window.size().height() == 860, "Docstring main-window height changed")

        groups = [
            group
            for group in window.findChildren(QGroupBox)
            if str(group.title()).strip() == "After Correction"
        ]
        require(len(groups) == 1, "real After Correction group missing")

        buttons = (
            window._review_generate_draft_button,
            window._review_generate_visible_drafts_button,
            window._review_generate_all_drafts_button,
            window._review_stop_ai_drafts_button,
            window._review_undo_bulk_drafts_button,
            window._review_save_change_button,
            window._review_approve_row_button,
            window._review_reject_row_button,
            window._review_undo_button,
            window._review_save_all_button,
        )
        for button in buttons:
            required_width = button.fontMetrics().horizontalAdvance(button.text()) + 28
            require(
                button.width() >= required_width,
                f"button label is clipped: {button.text()} ",
            )

        print("REAL_QT_DOCSTRING_AFTER_CORRECTION_LAYOUT: PASS")
        print("REAL_QT_DOCSTRING_AFTER_CORRECTION_LABEL_WIDTHS: PASS")
        print("REAL_QT_DOCSTRING_MAIN_GUI_SIZE_UNCHANGED: PASS")
    finally:
        window.hide()
        window.close()
        window.deleteLater()
        app.processEvents()
        if created_app:
            app.quit()
            app.processEvents()

def main() -> int:
    """Run static and deterministic runtime validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    validate_static(root)
    validate_runtime(root)
    validate_real_qt(root)
    print("STATUS: IN_SYNC")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
