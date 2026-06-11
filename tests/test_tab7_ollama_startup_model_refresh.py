"""Focused tests for Tab 7 Ollama startup/dropdown model refresh."""

from __future__ import annotations

import sys
import types
from typing import Any


def _install_pyside6_stubs() -> None:
    """Install minimal PySide6 stubs needed for runtime controller import."""
    pyside6 = types.ModuleType("PySide6")
    qtcore = types.ModuleType("PySide6.QtCore")
    qtgui = types.ModuleType("PySide6.QtGui")
    qtwidgets = types.ModuleType("PySide6.QtWidgets")

    class _Qt:
        CustomContextMenu = object()
        Horizontal = object()
        UserRole = object()

    class _Dummy:
        ExtendedSelection = object()

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            del args, kwargs

        def __getattr__(self, _name: str) -> Any:
            def _method(*args: Any, **kwargs: Any) -> None:
                del args, kwargs
                return None

            return _method

    class _FileDialog:
        @staticmethod
        def getExistingDirectory(*args: Any, **kwargs: Any) -> str:
            del args, kwargs
            return ""

        @staticmethod
        def getOpenFileName(*args: Any, **kwargs: Any) -> tuple[str, str]:
            del args, kwargs
            return "", ""

    class _MessageBox:
        class StandardButton:
            Yes = 1
            No = 2

        @staticmethod
        def information(*args: Any, **kwargs: Any) -> None:
            del args, kwargs

        @staticmethod
        def critical(*args: Any, **kwargs: Any) -> None:
            del args, kwargs

        @staticmethod
        def warning(*args: Any, **kwargs: Any) -> None:
            del args, kwargs

        @staticmethod
        def question(*args: Any, **kwargs: Any) -> int:
            del args, kwargs
            return _MessageBox.StandardButton.No

    qtcore.Qt = _Qt
    qtgui.QAction = _Dummy
    qtgui.QKeySequence = _Dummy
    qtwidgets.QApplication = _Dummy
    qtwidgets.QDialog = _Dummy
    qtwidgets.QFileDialog = _FileDialog
    qtwidgets.QHBoxLayout = _Dummy
    qtwidgets.QLabel = _Dummy
    qtwidgets.QListWidget = _Dummy
    qtwidgets.QListWidgetItem = _Dummy
    qtwidgets.QMenu = _Dummy
    qtwidgets.QMessageBox = _MessageBox
    qtwidgets.QPlainTextEdit = _Dummy
    qtwidgets.QSplitter = _Dummy
    qtwidgets.QVBoxLayout = _Dummy
    qtwidgets.QWidget = _Dummy

    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtGui"] = qtgui
    sys.modules["PySide6.QtWidgets"] = qtwidgets




def _install_project_dependency_stubs() -> None:
    """Install project stubs that are outside the runtime-refresh contract."""
    local_copy = types.ModuleType("kanda_reasoner_app.local_ai_json_working_copy")

    def _not_used(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        return None

    local_copy.ensure_local_ai_copy = _not_used
    local_copy.refresh_local_ai_copy = _not_used
    sys.modules["kanda_reasoner_app.local_ai_json_working_copy"] = local_copy

class _FakeCombo:
    """Small QComboBox replacement used by the focused refresh test."""

    def __init__(self) -> None:
        self.items: list[str] = ["qwen2.5-coder:7b"]
        self.index = 0

    def currentText(self) -> str:
        if 0 <= self.index < len(self.items):
            return self.items[self.index]
        return ""

    def clear(self) -> None:
        self.items.clear()
        self.index = -1

    def addItem(self, item: str) -> None:
        self.items.append(item)
        if self.index < 0:
            self.index = 0

    def findText(self, text: str) -> int:
        try:
            return self.items.index(text)
        except ValueError:
            return -1

    def setCurrentIndex(self, index: int) -> None:
        self.index = index


class _FakeSettings:
    def value(self, key: str, default: str = "", type: Any = str) -> str:
        del key, type
        return default


class _FakeRegistry:
    def list_models(self) -> list[str]:
        return ["qwen3-coder:30b", "qwen2.5-coder:7b"]


class _FakeWindow:
    def __init__(self) -> None:
        self.model_combo = _FakeCombo()
        self.model_registry = _FakeRegistry()
        self.settings = _FakeSettings()
        self.logs: list[str] = []
        self.saved = False

    def _append_log(self, message: str) -> None:
        self.logs.append(message)

    def _save_last_config(self) -> None:
        self.saved = True


def test_refresh_models_populates_all_live_ollama_models() -> None:
    _install_pyside6_stubs()
    _install_project_dependency_stubs()

    from kanda_reasoner_app.project_reasoner_v10.main_window_help.runtime_controller import (
        RuntimeController,
    )

    window = _FakeWindow()
    RuntimeController().refresh_models(window)

    assert window.model_combo.items == ["qwen3-coder:30b", "qwen2.5-coder:7b"]
    assert window.saved is True
    assert any("Ollama model refresh found 2 model(s)" in log for log in window.logs)


if __name__ == "__main__":
    test_refresh_models_populates_all_live_ollama_models()
    print("Tab 7 Ollama startup model refresh tests passed.")
