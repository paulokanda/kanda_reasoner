"""Regression test for Tab 3 lazy-load import repair."""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path


class _FakeSignal:
    """Small signal object that accepts Qt-style connect calls."""

    def connect(self, callback):
        self.callback = callback


class _FakeWidget:
    """Small stand-in for PySide6 widgets used during import tests."""

    Save = 1
    Cancel = 2
    Apply = 4
    Warning = 8
    Yes = 16
    No = 32
    UserRole = 256
    NoWrap = 1
    Expanding = 1

    def __init__(self, *args, **kwargs):
        self.clicked = _FakeSignal()
        self.toggled = _FakeSignal()
        self.currentTextChanged = _FakeSignal()
        self.currentItemChanged = _FakeSignal()
        self.itemDoubleClicked = _FakeSignal()
        self.accepted = _FakeSignal()
        self.rejected = _FakeSignal()
        self._items = []
        self._text = ""
        self._data = {}

    def __or__(self, other):
        return int(self) | int(other)

    def __int__(self):
        return 1

    def addWidget(self, *args, **kwargs):
        return None

    def insertWidget(self, *args, **kwargs):
        return None

    def addLayout(self, *args, **kwargs):
        return None

    def addRow(self, *args, **kwargs):
        return None

    def addStretch(self, *args, **kwargs):
        return None

    def addTab(self, *args, **kwargs):
        return None

    def addItems(self, items):
        self._items.extend(list(items))

    def addItem(self, item):
        self._items.append(item)

    def clear(self):
        self._items.clear()
        self._text = ""

    def setText(self, text):
        self._text = str(text)

    def text(self):
        return self._text

    def setPlainText(self, text):
        self._text = str(text)

    def toPlainText(self):
        return self._text

    def appendPlainText(self, text):
        self._text += str(text)

    def insertPlainText(self, text):
        self._text += str(text)

    def currentText(self):
        return self._text or (str(self._items[0]) if self._items else "")

    def setCurrentText(self, text):
        self._text = str(text)

    def setChecked(self, value):
        self._checked = bool(value)

    def isChecked(self):
        return bool(getattr(self, "_checked", False))

    def setEnabled(self, value):
        self._enabled = bool(value)

    def setData(self, role, value):
        self._data[role] = value

    def data(self, role):
        return self._data.get(role)

    def button(self, which):
        del which
        return self

    def exec(self):
        return 0

    def accept(self):
        return None

    def reject(self):
        return None

    def statusBar(self):
        return self

    def showMessage(self, message):
        self._text = str(message)

    def moveCursor(self, *args, **kwargs):
        return None

    def font(self):
        return self

    def setBold(self, value):
        self._bold = bool(value)

    def __getattr__(self, name):
        if name == "MoveOperation":
            return types.SimpleNamespace(End=1)
        def _method(*args, **kwargs):
            return None
        return _method


class _FakeModule(types.ModuleType):
    """Module that supplies fake PySide6 attributes on demand."""

    def __getattr__(self, name):
        if name == "Qt":
            return types.SimpleNamespace(UserRole=256)
        if name == "Signal":
            return lambda *args, **kwargs: _FakeSignal()
        return _FakeWidget


def _install_fake_pyside6() -> None:
    pyside6 = types.ModuleType("PySide6")
    qtcore = _FakeModule("PySide6.QtCore")
    qtwidgets = _FakeModule("PySide6.QtWidgets")
    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets


def test_tab3_imports_do_not_use_stale_reasoner_tools_gui_package() -> None:
    _install_fake_pyside6()
    stale_module = types.ModuleType("reasoner_tools_gui")
    sys.modules["reasoner_tools_gui"] = stale_module

    module_names = [
        "kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.layout_builder",
        "kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.report_review_panel",
        "kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.manual_docstring_review_editor",
        "kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode.actual_tab3_wiring",
        "kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui",
    ]
    imported = {}
    for module_name in module_names:
        module = importlib.import_module(module_name)
        assert module is not None
        imported[module_name] = module

    main_module = imported[
        "kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui"
    ]
    window = main_module.MissingDocstringsWindow()
    assert hasattr(window, "_run_button")
    assert window._safe_mode_actual_tab3_wiring_result["installed"] is True


def test_tab3_repaired_files_do_not_contain_stale_import_string() -> None:
    root = Path(__file__).resolve().parents[1]
    files = [
        root / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help" / "layout_builder.py",
        root / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help" / "report_review_panel.py",
        root / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help" / "manual_docstring_review_editor.py",
    ]
    stale = "reasoner_tools_gui.tab3_manual_review_runtime"
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert stale not in text


def main() -> int:
    """Run focused Tab 3 import repair tests without pytest."""
    test_tab3_imports_do_not_use_stale_reasoner_tools_gui_package()
    test_tab3_repaired_files_do_not_contain_stale_import_string()
    print("Tab 3 failed-load import repair tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
