"""Import tests for Tab 1 advisory AI review Qt integration contracts."""

from __future__ import annotations

import sys
import types


class FakeSignalInstance:
    """Small fake Qt signal instance."""

    def __init__(self) -> None:
        self.callbacks: list[object] = []

    def connect(self, callback: object) -> None:
        """Record one fake callback connection."""
        self.callbacks.append(callback)

    def emit(self, *args: object) -> None:
        """Call connected callbacks."""
        for callback in list(self.callbacks):
            if callable(callback):
                callback(*args)


class FakeSignalFactory:
    """Small fake Qt Signal factory."""

    def __call__(self, *args: object, **kwargs: object) -> FakeSignalInstance:
        """Return a fake signal instance."""
        return FakeSignalInstance()


class FakeQObject:
    """Small fake Qt QObject."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def deleteLater(self) -> None:
        """Match the Qt cleanup method."""
        return None


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


class FakeQThread(FakeQObject):
    """Small fake Qt thread object."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__()
        self.started = FakeSignalInstance()
        self.finished = FakeSignalInstance()

    def start(self) -> None:
        """Emit started for fake thread tests."""
        self.started.emit()

    def quit(self) -> None:
        """Emit finished for fake thread tests."""
        self.finished.emit()


class FakeButton:
    """Small fake QPushButton."""

    def __init__(self, text: str = "") -> None:
        self.text = text
        self.tooltip = ""
        self.clicked = FakeSignalInstance()
        self.enabled = True

    def setObjectName(self, name: str) -> None:
        """Accept object names."""
        self.object_name = name

    def setMinimumWidth(self, value: int) -> None:
        """Accept minimum width calls."""
        self.minimum_width = value

    def setToolTip(self, text: str) -> None:
        """Record tooltip text."""
        self.tooltip = text

    def setEnabled(self, enabled: bool) -> None:
        """Record enabled state."""
        self.enabled = enabled

    def setText(self, text: str) -> None:
        """Record widget text."""
        self.text = text


class FakeMessageBox:
    """Small fake QMessageBox."""

    @staticmethod
    def warning(*args: object, **kwargs: object) -> None:
        """Fake warning dialog."""
        return None

    @staticmethod
    def information(*args: object, **kwargs: object) -> None:
        """Fake information dialog."""
        return None


class FakeComboBox(FakeButton):
    """Small fake QComboBox."""

    def __init__(self) -> None:
        super().__init__("")
        self.items: list[str] = []
        self.current_index = -1
        self.signals_blocked = False
        self.currentTextChanged = FakeSignalInstance()

    def setMinimumWidth(self, value: int) -> None:
        """Accept minimum width calls."""
        return None

    def addItem(self, text: str) -> None:
        """Add one fake item."""
        self.items.append(text)
        if self.current_index < 0:
            self.current_index = 0

    def clear(self) -> None:
        """Clear fake items."""
        self.items = []
        self.current_index = -1

    def currentText(self) -> str:
        """Return current fake text."""
        if 0 <= self.current_index < len(self.items):
            return self.items[self.current_index]
        return ""

    def findText(self, text: str) -> int:
        """Find one fake item."""
        try:
            return self.items.index(text)
        except ValueError:
            return -1

    def setCurrentIndex(self, index: int) -> None:
        """Set current fake index."""
        self.current_index = index

    def blockSignals(self, blocked: bool) -> None:
        """Record signal blocking."""
        self.signals_blocked = blocked


class FakeLabel(FakeButton):
    """Small fake QLabel."""


class FakeFrame(FakeButton):
    """Small fake QFrame."""

    def setObjectName(self, name: str) -> None:
        """Accept object names."""
        self.object_name = name

    def setVisible(self, visible: bool) -> None:
        """Accept visibility changes."""
        self.visible = visible

    def setStyleSheet(self, text: str) -> None:
        """Accept style changes."""
        self.style = text


class FakeProgressBar(FakeFrame):
    """Small fake QProgressBar."""

    def setMaximumWidth(self, value: int) -> None:
        """Accept maximum width calls."""
        return None

    def setTextVisible(self, visible: bool) -> None:
        """Accept text visibility changes."""
        return None

    def setRange(self, minimum: int, maximum: int) -> None:
        """Accept range changes."""
        self.range = (minimum, maximum)

    def setValue(self, value: int) -> None:
        """Accept value changes."""
        self.value = value


class FakeHBoxLayout:
    """Small fake QHBoxLayout."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.widgets: list[object] = []

    def setContentsMargins(self, *args: object) -> None:
        """Accept margins."""
        return None

    def setSpacing(self, value: int) -> None:
        """Accept spacing."""
        return None

    def addWidget(self, widget: object, *args: object, **kwargs: object) -> None:
        """Record one widget."""
        self.widgets.append(widget)


class FakeTimer:
    """Small fake QTimer."""

    def __init__(self) -> None:
        self.timeout = FakeSignalInstance()
        self.active = False

    def setInterval(self, interval: int) -> None:
        """Accept interval changes."""
        self.interval = interval

    def isActive(self) -> bool:
        """Return active state."""
        return self.active

    def start(self) -> None:
        """Start the fake timer."""
        self.active = True

    def stop(self) -> None:
        """Stop the fake timer."""
        self.active = False


class FakeQt:
    """Small fake Qt namespace."""

    AlignRight = 1


def install_pyside6_stubs() -> None:
    """Install minimal PySide6 stubs before importing Qt integration modules."""
    pyside6 = types.ModuleType("PySide6")
    qtcore = types.ModuleType("PySide6.QtCore")
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtcore.QObject = FakeQObject
    qtcore.QSettings = FakeSettings
    qtcore.QThread = FakeQThread
    qtcore.Signal = FakeSignalFactory()
    qtcore.QTimer = FakeTimer
    qtcore.Qt = FakeQt
    qtwidgets.QComboBox = FakeComboBox
    qtwidgets.QFrame = FakeFrame
    qtwidgets.QHBoxLayout = FakeHBoxLayout
    qtwidgets.QLabel = FakeLabel
    qtwidgets.QMessageBox = FakeMessageBox
    qtwidgets.QProgressBar = FakeProgressBar
    qtwidgets.QPushButton = FakeButton
    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets


install_pyside6_stubs()

from kanda_reasoner_app.manage_architecture.ai_review.gui_integration import (  # noqa: E402
    install_tab1_ai_review_controls,
)
from kanda_reasoner_app.manage_architecture.ai_review.qt_worker import (  # noqa: E402
    Tab1AIReviewWorker,
)


class FakeLayout:
    """Small fake button layout."""

    def __init__(self) -> None:
        self.widgets: list[object] = []

    def addWidget(self, widget: object, *args: object, **kwargs: object) -> None:
        """Record an added widget."""
        self.widgets.append(widget)


class FakeWindow:
    """Small fake window for installation tests."""

    pass


def test_gui_integration_imports_and_installs_button() -> None:
    """GUI integration public contract can be imported and installs a button."""
    window = FakeWindow()
    layout = FakeLayout()

    install_tab1_ai_review_controls(window, layout)

    assert len(layout.widgets) >= 5
    assert getattr(window, "_ai_review_button").text == "AI Review First Check"
    assert getattr(window, "_ai_review_model_combo").items[0].startswith("Auto")
    assert getattr(window, "_tab1_activity_indicator") is not None


def test_qt_worker_imports_with_expected_class_name() -> None:
    """Qt worker public contract can be imported with Qt stubs."""
    worker = Tab1AIReviewWorker("audit", r"<PROJECT_ROOT>", "qwen3-coder:30b")

    assert worker.__class__.__name__ == "Tab1AIReviewWorker"
    assert getattr(worker, "_model_name") == "qwen3-coder:30b"


if __name__ == "__main__":
    test_gui_integration_imports_and_installs_button()
    test_qt_worker_imports_with_expected_class_name()
    print("Tab 1 AI review Qt import contract tests passed.")
