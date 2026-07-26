#!/usr/bin/env python3
"""Validate the compact Docstring Assistant column and action layout."""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import types
from pathlib import Path
from types import SimpleNamespace


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    layout = read(root, "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py")
    state = read(
        root,
        "kanda_reasoner_app/insert_missing_docstrings_gui/"
        "insert_missing_docstrings_gui_help/window_state.py",
    )

    require("column_splitter.setStretchFactor(0, 42)" in layout, "left splitter ratio missing")
    require("column_splitter.setStretchFactor(1, 58)" in layout, "right splitter ratio missing")
    require("column_splitter.setSizes([42, 58])" in layout, "splitter initial sizes missing")
    require("_compact_fixed_button(window._open_web_ai_config_button" in layout,
            "Open Config AI is not content-sized")
    require("_compact_fixed_button(window._browse_target_button" in layout,
            "Browse target button is not compact")
    require("_compact_fixed_button(window._clear_target_button" in layout,
            "Clear target button is not compact")
    require("include_row.addStretch(1)\n    include_row.addWidget(window._confirm_write_checkbox)" in layout,
            "write confirmation is not aligned to the right edge")
    require("action_row.addStretch(1)\n    _compact_fixed_button(window._copy_report_button" in layout,
            "Copy report is not aligned to the right edge")
    require("_build_compact_action_rows(" in layout, "compact After Correction rows missing")
    require("smaller_font=True" in layout, "After Correction smaller-font contract missing")
    require("size_policy_cls.Fixed, size_policy_cls.Fixed" in layout,
            "After Correction buttons are not content-sized")
    require("font.setPointSize(max(8, point_size - 1))" in layout,
            "After Correction font reduction missing")
    require("button.adjustSize()" in layout, "label-driven button sizing missing")
    require("self.resize(1360, 860)" in state, "main Docstring GUI size changed")

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
        require(marker in layout, f"After Correction action missing: {marker}")

    line_count = len(layout.splitlines())
    require(line_count <= 500, f"layout_runtime.py exceeds 500 lines: {line_count}")

    print("DOCSTRING_LEFT_COLUMN_42_58_SPLIT: PASS")
    print("DOCSTRING_LEFT_ACTION_EDGE_ALIGNMENT: PASS")
    print("DOCSTRING_RUN_OPTIONS_COMPACT_REFLOW: PASS")
    print("DOCSTRING_REPORT_COMPACT_REFLOW: PASS")
    print("DOCSTRING_AFTER_CORRECTION_CONTENT_WIDTH_BUTTONS: PASS")
    print("DOCSTRING_AFTER_CORRECTION_SMALLER_FONT: PASS")
    print("DOCSTRING_AFTER_CORRECTION_MINIMUM_ROW_PACKING: PASS")
    print("DOCSTRING_MAIN_GUI_SIZE_UNCHANGED: PASS")
    print("DOCSTRING_LAYOUT_MODULE_SIZE_GATE: PASS")


class FakeSizePolicy:
    Ignored = "ignored"
    Expanding = "expanding"
    Fixed = "fixed"


class FakeFont:
    def __init__(self, point_size: int = 10) -> None:
        self._point_size = point_size

    def pointSize(self) -> int:
        return self._point_size

    def setPointSize(self, value: int) -> None:
        self._point_size = value


class FakeSignal:
    def connect(self, _slot: object) -> None:
        return None


class FakeWidget:
    def __init__(self, *args: object) -> None:
        self.args = args
        self.layout = None
        self.minimum_width = None
        self.size_policy = None
        self.enabled = True
        self.hidden = False
        self._font = FakeFont()
        self.adjusted = False
        self.clicked = FakeSignal()

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

    def font(self) -> FakeFont:
        copied = FakeFont(self._font.pointSize())
        return copied

    def setFont(self, font: FakeFont) -> None:
        self._font = font

    def adjustSize(self) -> None:
        self.adjusted = True


class FakePlainTextEdit(FakeWidget):
    WidgetWidth = "widget-width"


class FakeLayout:
    def __init__(self, parent: object | None = None) -> None:
        self.items: list[tuple[str, object, tuple[object, ...]]] = []
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

    def setSpacing(self, value: int) -> None:
        self.spacing = value


class FakeSplitter(FakeWidget):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.children: list[object] = []
        self.stretch: dict[int, int] = {}
        self.sizes: list[int] = []

    def addWidget(self, widget: object) -> None:
        self.children.append(widget)

    def setStretchFactor(self, index: int, value: int) -> None:
        self.stretch[index] = value

    def setSizes(self, values: list[int]) -> None:
        self.sizes = list(values)

    def setChildrenCollapsible(self, _value: bool) -> None:
        return None


class FakeTabs(FakeWidget):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.tabs: list[tuple[object, str]] = []

    def addTab(self, widget: object, title: str) -> None:
        self.tabs.append((widget, title))


class FakeGroupBox(FakeWidget):
    def __init__(self, title: str = "") -> None:
        super().__init__(title)
        self.title = title


class FakeWindow:
    def __init__(self) -> None:
        self.central = None

    def setCentralWidget(self, widget: object) -> None:
        self.central = widget


class FakeScanRuntime:
    def configure_scan_diff_write_controls(self, _window: object) -> None:
        return None

    def refresh_selected_mode_controls(self, _window: object, _mode: object = None) -> None:
        return None


class FakeAIRuntime:
    def build_ai_group(self, owner: object) -> object:
        group = FakeGroupBox("AI Assistant")
        layout = FakeLayout(group)
        row = FakeLayout()
        row.addStretch(1)
        row.addWidget(owner._open_web_ai_config_button)
        layout.addLayout(row)
        return group


def fake_qt_module() -> types.ModuleType:
    module = types.ModuleType("PySide6.QtWidgets")
    module.QGroupBox = FakeGroupBox
    module.QHBoxLayout = FakeLayout
    module.QLabel = FakeWidget
    module.QPlainTextEdit = FakePlainTextEdit
    module.QPushButton = FakeWidget
    module.QSizePolicy = FakeSizePolicy
    module.QSplitter = FakeSplitter
    module.QTabWidget = FakeTabs
    module.QVBoxLayout = FakeLayout
    module.QWidget = FakeWidget
    return module


def load_layout_module(root: Path) -> object:
    pyside = types.ModuleType("PySide6")
    qt_widgets = fake_qt_module()
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtWidgets"] = qt_widgets
    path = root / "kanda_reasoner_app/tab3_manual_review_runtime/layout_runtime.py"
    spec = importlib.util.spec_from_file_location("layout_runtime_under_test", path)
    require(spec is not None and spec.loader is not None, "layout module spec failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module._scan_only_runtime = lambda: FakeScanRuntime()
    module._ai_controls_runtime = lambda: FakeAIRuntime()
    return module


def widget() -> FakeWidget:
    return FakeWidget()


def validate_runtime(root: Path) -> None:
    module = load_layout_module(root)

    review_window = SimpleNamespace(
        _review_summary=widget(),
        _review_filter_combo=widget(),
        _review_list=widget(),
    )
    tabs = module._build_review_panel(review_window)
    review_tab, title = tabs.tabs[0]
    require(title == "Review and Correct Missing Docstrings", "review tab title changed")
    splitter = next(
        item[1]
        for item in review_tab.layout.items
        if item[0] == "widget" and isinstance(item[1], FakeSplitter)
    )
    after_group = splitter.children[1]
    action_columns = [item[1] for item in after_group.layout.items if item[0] == "layout"]
    require(len(action_columns) == 2, "expected draft and decision action columns")
    draft_column, decision_column = action_columns
    require(len([item for item in draft_column.items if item[0] == "layout"]) == 3,
            "draft actions are not packed into three rows")
    require(len([item for item in decision_column.items if item[0] == "layout"]) == 2,
            "decision actions are not packed into two rows")

    buttons = (
        review_window._review_generate_draft_button,
        review_window._review_generate_visible_drafts_button,
        review_window._review_generate_all_drafts_button,
        review_window._review_stop_ai_drafts_button,
        review_window._review_undo_bulk_drafts_button,
        review_window._review_save_change_button,
        review_window._review_approve_row_button,
        review_window._review_reject_row_button,
        review_window._review_undo_button,
        review_window._review_save_all_button,
    )
    for button in buttons:
        require(button.size_policy == (FakeSizePolicy.Fixed, FakeSizePolicy.Fixed),
                "After Correction button is not fixed to content width")
        require(button._font.pointSize() == 9, "After Correction font was not reduced once")
        require(button.adjusted, "After Correction button did not adjust to its label")

    options_window = SimpleNamespace(
        _mode_combo=widget(),
        _tab1_audit_docstring_radio=widget(),
        _scope_combo=widget(),
        _target_path_edit=widget(),
        _browse_target_button=widget(),
        _clear_target_button=widget(),
        _module_checkbox=widget(),
        _class_checkbox=widget(),
        _function_checkbox=widget(),
        _file_address_checkbox=widget(),
        _confirm_write_checkbox=widget(),
        _workers_spin=widget(),
    )
    options_group = module._build_options_group(options_window)
    option_rows = [item[1] for item in options_group.layout.items if item[0] == "layout"]
    require(len(option_rows) == 4, "Run Options was not reflowed into four compact rows")
    include_row = option_rows[2]
    require(include_row.items[-2][0] == "stretch", "confirm checkbox lacks right-side spacer")
    require(include_row.items[-1][1] is options_window._confirm_write_checkbox,
            "confirm checkbox is not the right-edge widget")
    for button in (options_window._browse_target_button, options_window._clear_target_button):
        require(button.size_policy == (FakeSizePolicy.Fixed, FakeSizePolicy.Fixed),
                "Browse/Clear button is not compact")

    report_window = SimpleNamespace(
        _report_path_edit=widget(),
        _browse_report_button=widget(),
    )
    report_group = module._build_report_group(report_window)
    report_rows = [item[1] for item in report_group.layout.items if item[0] == "layout"]
    require(len(report_rows) == 2, "Report group was not reflowed into two rows")
    require(report_rows[1].items[-2][0] == "stretch", "Copy report lacks right-side spacer")
    require(report_rows[1].items[-1][1] is report_window._copy_report_button,
            "Copy report is not the right-edge action")

    ai_window = SimpleNamespace(_open_web_ai_config_button=widget())
    module._build_ai_group(ai_window)
    require(ai_window._open_web_ai_config_button.size_policy ==
            (FakeSizePolicy.Fixed, FakeSizePolicy.Fixed),
            "Open Config AI is not content-sized")

    print("DOCSTRING_COMPACT_LAYOUT_RUNTIME_ROWS: PASS")
    print("DOCSTRING_COMPACT_LAYOUT_RUNTIME_FIXED_BUTTONS: PASS")
    print("DOCSTRING_COMPACT_LAYOUT_RUNTIME_RIGHT_EDGE_ACTIONS: PASS")


def validate_real_qt(root: Path) -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtWidgets import QApplication, QGroupBox, QPushButton, QSplitter
    except ImportError:
        print("REAL_QT_DOCSTRING_COMPACT_COLUMNS: SKIPPED_NO_PYSIDE6")
        return

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui import (
        MissingDocstringsWindow,
    )

    app = QApplication.instance() or QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = MissingDocstringsWindow()
    try:
        window.show()
        app.processEvents()
        require(window.size().width() == 1360, "Docstring main-window width changed")
        require(window.size().height() == 860, "Docstring main-window height changed")

        central = window.centralWidget()
        splitters = central.findChildren(QSplitter)
        require(splitters, "main column splitter missing")
        splitter = max(splitters, key=lambda item: item.width())
        sizes = splitter.sizes()
        require(len(sizes) >= 2 and sizes[0] < sizes[1], "right column did not gain lateral space")

        after_groups = [
            group for group in window.findChildren(QGroupBox)
            if str(group.title()).strip() == "After Correction"
        ]
        require(len(after_groups) == 1, "After Correction group missing")
        after_group = after_groups[0]
        after_buttons = [
            button for button in after_group.findChildren(QPushButton)
            if button.text() in {
                "Generate Draft", "Generate Visible Drafts", "Generate All Drafts",
                "Stop AI Drafts", "Undo Last Bulk Drafts", "Save Review Decision",
                "Approve Row", "Reject Row", "Undo Row Change", "Approve Visible Rows",
            }
        ]
        require(len(after_buttons) == 10, "After Correction buttons missing")
        default_points = window.font().pointSize()
        for button in after_buttons:
            require(button.width() >= button.sizeHint().width(),
                    f"button label clipped: {button.text()}")
            require(button.font().pointSize() <= max(8, default_points - 1),
                    f"button font was not reduced: {button.text()}")

        right_edges = []
        for control in (
            window._open_web_ai_config_button,
            window._clear_target_button,
            window._progress,
            window._confirm_write_checkbox,
            window._copy_report_button,
        ):
            point = control.mapTo(window, control.rect().topRight())
            right_edges.append(point.x())
        require(max(right_edges) - min(right_edges) <= 32,
                f"left action edges are not aligned: {right_edges}")

        print("REAL_QT_DOCSTRING_LEFT_COLUMN_NARROWER: PASS")
        print("REAL_QT_DOCSTRING_LEFT_ACTION_EDGE_ALIGNMENT: PASS")
        print("REAL_QT_DOCSTRING_AFTER_CORRECTION_LABEL_WIDTHS: PASS")
        print("REAL_QT_DOCSTRING_AFTER_CORRECTION_SMALLER_FONT: PASS")
        print("REAL_QT_DOCSTRING_MAIN_GUI_SIZE_UNCHANGED: PASS")
    finally:
        window.close()
        window.deleteLater()
        app.processEvents()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    validate_static(root)
    validate_runtime(root)
    if not args.static_only:
        validate_real_qt(root)
    print("VALIDATION OK: docstring-assistant-compact-columns-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
