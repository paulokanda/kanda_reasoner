from __future__ import annotations

import importlib
import sys
import types
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class _Signal:
    def __init__(self) -> None:
        self._callbacks = []

    def connect(self, callback) -> None:
        self._callbacks.append(callback)

    def emit(self) -> None:
        for callback in list(self._callbacks):
            callback()


class _Widget:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.object_name = ""

    def setObjectName(self, value: str) -> None:
        self.object_name = value


class _PushButton(_Widget):
    def __init__(self, text="", parent=None) -> None:
        super().__init__(parent)
        self._text = text
        self.enabled = True
        self.clicked = _Signal()

    def setText(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def setToolTip(self, _text: str) -> None:
        return None

    def setStyleSheet(self, _text: str) -> None:
        return None

    def setEnabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)


class _Action:
    def __init__(self, text: str) -> None:
        self.text = text
        self.triggered = _Signal()


class _Menu:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.actions = []

    def addAction(self, text: str):
        action = _Action(text)
        self.actions.append(action)
        return action


class _ToolButton(_PushButton):
    InstantPopup = 1

    def setFixedWidth(self, _width: int) -> None:
        return None

    def setPopupMode(self, _mode: int) -> None:
        return None

    def setMenu(self, menu) -> None:
        self.menu = menu


class _Layout:
    def __init__(self, parent=None) -> None:
        self.parent = parent
        self.widgets = []
        if parent is not None:
            parent.layout = self

    def setContentsMargins(self, *args) -> None:
        return None

    def setSpacing(self, _value: int) -> None:
        return None

    def addWidget(self, widget) -> None:
        self.widgets.append(widget)


def _install_fake_qt() -> None:
    pyside = types.ModuleType("PySide6")
    widgets = types.ModuleType("PySide6.QtWidgets")
    widgets.QHBoxLayout = _Layout
    widgets.QMenu = _Menu
    widgets.QPushButton = _PushButton
    widgets.QToolButton = _ToolButton
    widgets.QWidget = _Widget
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtWidgets"] = widgets


def test_split_control_has_only_two_routes_and_main_repeats_selection() -> None:
    _install_fake_qt()
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.warning_resolver_split_control"
    )
    calls: list[str] = []
    control = module.build_warning_resolver_split_control(
        _Widget(),
        heuristic_callback=lambda: calls.append("heuristic"),
        model_callback=lambda: calls.append("model"),
        cancel_callback=lambda: calls.append("cancel"),
    )
    assert control.main_button.text() == "Warning Heuristic Resolver"
    assert [action.text for action in control.dropdown_button.menu.actions] == [
        "Warning Heuristic Resolver",
        "Warning Local AI Resolver",
    ]
    control.main_button.clicked.emit()
    assert calls == ["heuristic"]
    control.dropdown_button.menu.actions[1].triggered.emit()
    assert calls == ["heuristic", "model"]
    assert control.main_button.text() == "Warning Local AI Resolver"
    control.main_button.clicked.emit()
    assert calls == ["heuristic", "model", "model"]
    control.dropdown_button.menu.actions[0].triggered.emit()
    assert calls[-1] == "heuristic"
    assert control.main_button.text() == "Warning Heuristic Resolver"
    assert control.container.layout.widgets == [
        control.main_button,
        control.dropdown_button,
        control.cancel_button,
    ]
    assert control.cancel_button.enabled is False
    control.cancel_button.clicked.emit()
    assert calls[-1] == "cancel"


def main() -> int:
    test_split_control_has_only_two_routes_and_main_repeats_selection()
    print("WARNING_RESOLVER_SPLIT_CONTROL_TWO_ROUTES: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
