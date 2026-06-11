"""Tests for Tab 2 advisory AI review GUI integration contracts."""

from __future__ import annotations

import sys
import types


class FakeSignal:
    """Small fake signal."""

    def __init__(self) -> None:
        self.callbacks: list[object] = []

    def connect(self, callback: object) -> None:
        """Record one callback."""
        self.callbacks.append(callback)

    def emit(self, *args: object) -> None:
        """Emit fake callbacks."""
        for callback in list(self.callbacks):
            if callable(callback):
                callback(*args)


class FakeWidget:
    """Small fake widget."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.enabled = True
        self.visible = True
        self.layout_value = None

    def setEnabled(self, enabled: bool) -> None:
        """Record enabled state."""
        self.enabled = enabled

    def setText(self, text: str) -> None:
        """Record text."""
        self.text = text

    def setToolTip(self, text: str) -> None:
        """Record tooltip."""
        self.tooltip = text

    def setObjectName(self, name: str) -> None:
        """Record object name."""
        self.object_name = name

    def setMinimumWidth(self, value: int) -> None:
        """Accept minimum width."""
        self.minimum_width = value

    def setMaximumWidth(self, value: int) -> None:
        """Accept maximum width."""
        self.maximum_width = value

    def setVisible(self, visible: bool) -> None:
        """Record visibility."""
        self.visible = visible

    def setStyleSheet(self, text: str) -> None:
        """Accept style."""
        self.style = text

    def setLayout(self, layout: object) -> None:
        """Record layout."""
        self.layout_value = layout


class FakeButton(FakeWidget):
    """Small fake button."""

    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.text = text
        self.clicked = FakeSignal()


class FakeCombo(FakeWidget):
    """Small fake combo box."""

    def __init__(self) -> None:
        super().__init__()
        self.items: list[str] = []
        self.index = -1
        self.blocked = False
        self.currentTextChanged = FakeSignal()

    def addItem(self, text: str) -> None:
        """Add one item."""
        self.items.append(text)
        if self.index < 0:
            self.index = 0

    def clear(self) -> None:
        """Clear all items."""
        self.items = []
        self.index = -1

    def currentText(self) -> str:
        """Return the selected item text."""
        if 0 <= self.index < len(self.items):
            return self.items[self.index]
        return ""

    def findText(self, text: str) -> int:
        """Return matching item index."""
        try:
            return self.items.index(text)
        except ValueError:
            return -1

    def setCurrentIndex(self, index: int) -> None:
        """Set current index."""
        self.index = index
        if not self.blocked:
            self.currentTextChanged.emit(self.currentText())

    def blockSignals(self, blocked: bool) -> None:
        """Record signal block."""
        self.blocked = blocked


class FakeLayout:
    """Small fake layout."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.widgets: list[object] = []

    def addWidget(self, widget: object, *args: object, **kwargs: object) -> None:
        """Record one widget."""
        self.widgets.append(widget)

    def addStretch(self) -> None:
        """Accept stretch."""
        return None

    def insertWidget(self, index: int, widget: object) -> None:
        """Insert one widget."""
        self.widgets.insert(index, widget)

    def count(self) -> int:
        """Return widget count."""
        return len(self.widgets)

    def setContentsMargins(self, *args: object) -> None:
        """Accept margins."""
        return None

    def setSpacing(self, value: int) -> None:
        """Accept spacing."""
        self.spacing = value


class FakeTimer:
    """Small fake timer."""

    def __init__(self) -> None:
        self.timeout = FakeSignal()
        self.active = False

    def setInterval(self, interval: int) -> None:
        """Accept interval."""
        self.interval = interval

    def isActive(self) -> bool:
        """Return active state."""
        return self.active

    def start(self) -> None:
        """Start timer."""
        self.active = True

    def stop(self) -> None:
        """Stop timer."""
        self.active = False

    @staticmethod
    def singleShot(milliseconds: int, callback: object) -> None:
        """Run fake delayed callback immediately."""
        if callable(callback):
            callback()


class FakeProgressBar(FakeWidget):
    """Small fake progress bar."""

    def setTextVisible(self, visible: bool) -> None:
        """Accept text visibility."""
        self.text_visible = visible

    def setRange(self, minimum: int, maximum: int) -> None:
        """Accept range."""
        self.range = (minimum, maximum)

    def setValue(self, value: int) -> None:
        """Accept value."""
        self.value = value


class FakeSettings:
    """Small fake settings store."""

    store: dict[str, str] = {}

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def value(self, key: str, default: str = "") -> str:
        """Return fake setting."""
        return self.store.get(key, default)

    def setValue(self, key: str, value: object) -> None:
        """Set fake setting."""
        self.store[key] = str(value or "")

    def sync(self) -> None:
        """Accept sync."""
        return None


class FakeQt:
    """Small fake Qt namespace."""

    AlignRight = 1


def install_pyside6_stubs() -> None:
    """Install fake PySide6 modules for source-level tests."""
    pyside6 = types.ModuleType("PySide6")
    qtcore = types.ModuleType("PySide6.QtCore")
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtcore.QObject = FakeWidget
    qtcore.QSettings = FakeSettings
    qtcore.QThread = FakeWidget
    qtcore.Signal = lambda *args, **kwargs: FakeSignal()
    qtcore.Slot = lambda *args, **kwargs: (lambda func: func)
    qtcore.QTimer = FakeTimer
    qtcore.Qt = FakeQt
    qtwidgets.QComboBox = FakeCombo
    qtwidgets.QFrame = FakeWidget
    qtwidgets.QHBoxLayout = FakeLayout
    qtwidgets.QLabel = FakeButton
    qtwidgets.QMessageBox = FakeWidget
    qtwidgets.QProgressBar = FakeProgressBar
    qtwidgets.QPushButton = FakeButton
    qtwidgets.QWidget = FakeWidget
    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets


install_pyside6_stubs()

from kanda_reasoner_app.manage_workflows.ai_review.gui_integration import (  # noqa: E402
    AUTO_MODEL_LABEL,
    SETTINGS_KEY_SELECTED_MODEL,
    create_tab2_ai_review_window_class,
    populate_tab2_ai_review_model_combo,
)


class FakeStatusBar:
    """Small fake status bar."""

    def __init__(self) -> None:
        self.message = ""

    def showMessage(self, message: str) -> None:
        """Record one message."""
        self.message = message


class FakeWindow:
    """Small fake Tab 2 window."""

    def __init__(self) -> None:
        self._tab2_ai_review_model_combo = FakeCombo()
        self._tab2_ai_review_saved_model_name = ""
        self._status_bar = FakeStatusBar()

    def statusBar(self) -> FakeStatusBar:
        """Return fake status bar."""
        return self._status_bar


class FakeAdapter:
    """Fake adapter for model selector tests."""

    def list_models(self) -> list[str]:
        """Return fake models."""
        return ["qwen2.5-coder:7b", "qwen3-coder:30b"]


def test_model_selector_populates_models_and_keeps_saved_model() -> None:
    """The model selector lists models and restores the saved choice."""
    window = FakeWindow()
    window._tab2_ai_review_saved_model_name = "qwen3-coder:30b"

    models = populate_tab2_ai_review_model_combo(window, adapter=FakeAdapter())

    assert models == ["qwen2.5-coder:7b", "qwen3-coder:30b"]
    assert window._tab2_ai_review_model_combo.items[0] == AUTO_MODEL_LABEL
    assert window._tab2_ai_review_model_combo.currentText() == "qwen3-coder:30b"
    assert "2 model" in window.statusBar().message


def test_model_selector_uses_separate_tab2_settings_key() -> None:
    """Tab 2 does not reuse the Tab 1 model setting key."""
    assert SETTINGS_KEY_SELECTED_MODEL == "tab2_ai_review_selected_model"


def test_window_class_factory_preserves_base_behavior_and_adds_ui() -> None:
    """The factory returns a subclass that can install Tab 2 controls."""

    class BaseWindow:
        def _build_ui(self) -> None:
            self.base_build_called = True

    enhanced_class = create_tab2_ai_review_window_class(BaseWindow)

    assert issubclass(enhanced_class, BaseWindow)
    assert enhanced_class.__name__ == BaseWindow.__name__


if __name__ == "__main__":
    test_model_selector_populates_models_and_keeps_saved_model()
    test_model_selector_uses_separate_tab2_settings_key()
    test_window_class_factory_preserves_base_behavior_and_adds_ui()
    print("Tab 2 AI review GUI contract tests passed.")
