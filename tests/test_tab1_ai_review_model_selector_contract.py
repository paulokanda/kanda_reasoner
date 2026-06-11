"""Tests for Tab 1 advisory AI model selector contract."""

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

    def setEnabled(self, enabled: bool) -> None:
        """Record enabled state."""
        self.enabled = enabled

    def setText(self, text: str) -> None:
        """Record widget text."""
        self.text = text

    def setToolTip(self, text: str) -> None:
        """Accept tooltip."""
        self.tooltip = text

    def setObjectName(self, name: str) -> None:
        """Accept object name."""
        self.object_name = name

    def setMinimumWidth(self, value: int) -> None:
        """Accept minimum width."""
        self.minimum_width = value

    def setMaximumWidth(self, value: int) -> None:
        """Accept maximum width."""
        self.maximum_width = value

    def setVisible(self, visible: bool) -> None:
        """Accept visibility."""
        self.visible = visible

    def setStyleSheet(self, text: str) -> None:
        """Accept style."""
        self.style = text


class FakeButton(FakeWidget):
    """Small fake button."""

    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.text = text
        self.clicked = FakeSignal()


class FakeCombo(FakeWidget):
    """Small fake combo box for model selector tests."""

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
        """Return the matching item index."""
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
        """Record signal blocking."""
        self.blocked = blocked


class FakeLayout:
    """Small fake layout."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.widgets: list[object] = []

    def addWidget(self, widget: object, *args: object, **kwargs: object) -> None:
        """Record one widget."""
        self.widgets.append(widget)

    def setContentsMargins(self, *args: object) -> None:
        """Accept margins."""
        return None

    def setSpacing(self, value: int) -> None:
        """Accept spacing."""
        return None


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
    """Small fake QSettings store."""

    store: dict[str, str] = {}

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def value(self, key: str, default: str = "") -> str:
        """Return one fake setting."""
        return self.store.get(key, default)

    def setValue(self, key: str, value: object) -> None:
        """Store one fake setting."""
        self.store[key] = str(value or "")

    def sync(self) -> None:
        """Match QSettings sync."""
        return None


class FakeQt:
    """Small fake Qt namespace."""

    AlignRight = 1


def install_pyside6_stubs() -> None:
    """Install fake PySide6 modules for source-level import tests."""
    pyside6 = types.ModuleType("PySide6")
    qtcore = types.ModuleType("PySide6.QtCore")
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtcore.QObject = FakeWidget
    qtcore.QSettings = FakeSettings
    qtcore.QThread = FakeWidget
    qtcore.Signal = lambda *args, **kwargs: FakeSignal()
    qtcore.QTimer = FakeTimer
    qtcore.Qt = FakeQt
    qtwidgets.QComboBox = FakeCombo
    qtwidgets.QFrame = FakeWidget
    qtwidgets.QHBoxLayout = FakeLayout
    qtwidgets.QLabel = FakeButton
    qtwidgets.QMessageBox = FakeWidget
    qtwidgets.QProgressBar = FakeProgressBar
    qtwidgets.QPushButton = FakeButton
    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets


install_pyside6_stubs()

from kanda_reasoner_app.manage_architecture.ai_review.gui_integration import (  # noqa: E402
    AUTO_MODEL_LABEL,
    SETTINGS_KEY_SELECTED_MODEL,
    install_tab1_ai_review_controls,
    populate_ai_review_model_combo,
)


class FakeStatusBar:
    """Small fake status bar."""

    def __init__(self) -> None:
        self.message = ""

    def showMessage(self, message: str) -> None:
        """Record one status message."""
        self.message = message


class FakeWindow:
    """Small fake Tab 1 window."""

    def __init__(self) -> None:
        self._ai_review_model_combo = FakeCombo()
        self._status_bar = FakeStatusBar()

    def statusBar(self) -> FakeStatusBar:
        """Return fake status bar."""
        return self._status_bar


class FakeAdapter:
    """Small fake model adapter."""

    def list_models(self) -> list[str]:
        """Return fake models."""
        return ["qwen2.5-coder:7b", "qwen3-coder:30b"]


def test_model_combo_refresh_adds_auto_and_ollama_models() -> None:
    """Refreshing fills the Tab 1 model combo with available models."""
    window = FakeWindow()

    models = populate_ai_review_model_combo(window, FakeAdapter())

    assert models == ["qwen2.5-coder:7b", "qwen3-coder:30b"]
    assert window._ai_review_model_combo.items == [
        AUTO_MODEL_LABEL,
        "qwen2.5-coder:7b",
        "qwen3-coder:30b",
    ]
    assert "2 model(s)" in window._status_bar.message


def test_saved_model_is_restored_after_refresh() -> None:
    """Refreshing restores the saved Tab 1 model when it is available."""
    FakeSettings.store = {SETTINGS_KEY_SELECTED_MODEL: "qwen3-coder:30b"}
    window = FakeWindow()

    populate_ai_review_model_combo(window, FakeAdapter())

    assert window._ai_review_model_combo.currentText() == "qwen3-coder:30b"
    assert window._ai_review_saved_model_name == "qwen3-coder:30b"


def test_user_selection_is_saved_by_installed_combo() -> None:
    """Changing the Tab 1 model combo persists the selected model."""
    FakeSettings.store = {}
    window = FakeWindow()
    layout = FakeLayout()

    install_tab1_ai_review_controls(window, layout)
    populate_ai_review_model_combo(window, FakeAdapter())
    selected_index = window._ai_review_model_combo.findText("qwen3-coder:30b")
    window._ai_review_model_combo.setCurrentIndex(selected_index)

    assert FakeSettings.store[SETTINGS_KEY_SELECTED_MODEL] == "qwen3-coder:30b"
    assert window._ai_review_saved_model_name == "qwen3-coder:30b"


if __name__ == "__main__":
    test_model_combo_refresh_adds_auto_and_ollama_models()
    test_saved_model_is_restored_after_refresh()
    test_user_selection_is_saved_by_installed_combo()
    print("Tab 1 AI review model selector tests passed.")
