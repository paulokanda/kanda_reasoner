"""Import contract tests for Tab 2 advisory AI review modules."""

from __future__ import annotations

import sys
import types


class FakeSignal:
    """Small fake signal."""

    def __init__(self) -> None:
        self.callbacks: list[object] = []

    def connect(self, callback: object) -> None:
        """Record callback."""
        self.callbacks.append(callback)


class FakeWidget:
    """Small fake widget."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def setObjectName(self, name: str) -> None:
        """Accept object name."""
        return None

    def setMinimumWidth(self, value: int) -> None:
        """Accept minimum width."""
        return None

    def setMaximumWidth(self, value: int) -> None:
        """Accept maximum width."""
        return None

    def setTextVisible(self, visible: bool) -> None:
        """Accept text visibility."""
        return None

    def setRange(self, minimum: int, maximum: int) -> None:
        """Accept range."""
        return None

    def setValue(self, value: int) -> None:
        """Accept value."""
        return None

    def setVisible(self, visible: bool) -> None:
        """Accept visibility."""
        return None

    def setStyleSheet(self, text: str) -> None:
        """Accept style."""
        return None

    def setText(self, text: str) -> None:
        """Accept text."""
        return None

    def setLayout(self, layout: object) -> None:
        """Accept layout."""
        return None

    def setToolTip(self, text: str) -> None:
        """Accept tooltip."""
        return None


class FakeLayout:
    """Small fake layout."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def setContentsMargins(self, *args: object) -> None:
        """Accept margins."""
        return None

    def setSpacing(self, value: int) -> None:
        """Accept spacing."""
        return None

    def addWidget(self, widget: object, *args: object, **kwargs: object) -> None:
        """Accept widget."""
        return None

    def addStretch(self) -> None:
        """Accept stretch."""
        return None


class FakeTimer:
    """Small fake timer."""

    def __init__(self) -> None:
        self.timeout = FakeSignal()
        self.active = False

    def setInterval(self, interval: int) -> None:
        """Accept interval."""
        return None

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
        """Accept singleshot."""
        if callable(callback):
            callback()


class FakeSettings:
    """Small fake settings."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        pass

    def value(self, key: str, default: str = "") -> str:
        """Return default."""
        return default

    def setValue(self, key: str, value: object) -> None:
        """Accept setting."""
        return None

    def sync(self) -> None:
        """Accept sync."""
        return None


class FakeQt:
    """Small fake Qt namespace."""

    AlignRight = 1


def install_pyside6_stubs() -> None:
    """Install fake PySide6 modules for import tests."""
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
    qtwidgets.QComboBox = FakeWidget
    qtwidgets.QFrame = FakeWidget
    qtwidgets.QHBoxLayout = FakeLayout
    qtwidgets.QLabel = FakeWidget
    qtwidgets.QMessageBox = FakeWidget
    qtwidgets.QProgressBar = FakeWidget
    qtwidgets.QPushButton = FakeWidget
    qtwidgets.QWidget = FakeWidget
    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets


def test_qt_facing_modules_import_with_stubs() -> None:
    """Qt-facing Tab 2 AI review modules import through their public contracts."""
    install_pyside6_stubs()

    from kanda_reasoner_app.manage_workflows.ai_review.gui_integration import (
        AUTO_MODEL_LABEL,
        create_tab2_ai_review_window_class,
        populate_tab2_ai_review_model_combo,
    )
    from kanda_reasoner_app.manage_workflows.ai_review.qt_worker import (
        Tab2AIReviewWorker,
    )
    from kanda_reasoner_app.manage_workflows.ai_review.running_indicator import (
        Tab2ActivityIndicator,
        install_tab2_activity_indicator,
    )

    assert AUTO_MODEL_LABEL.startswith("Auto")
    assert callable(create_tab2_ai_review_window_class)
    assert callable(populate_tab2_ai_review_model_combo)
    assert Tab2AIReviewWorker is not None
    assert Tab2ActivityIndicator is not None
    assert callable(install_tab2_activity_indicator)


if __name__ == "__main__":
    test_qt_facing_modules_import_with_stubs()
    print("Tab 2 AI review Qt import contract tests passed.")
