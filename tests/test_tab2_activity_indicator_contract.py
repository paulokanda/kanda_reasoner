"""Direct public import tests for the Tab 2 activity indicator."""

from __future__ import annotations

import sys
import types


class FakeSignal:
    """Small fake Qt signal."""

    def __init__(self) -> None:
        self.callbacks: list[object] = []

    def connect(self, callback: object) -> None:
        """Record one callback."""
        self.callbacks.append(callback)


class FakeWidget:
    """Small fake QWidget-like object."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.visible = True
        self.text = ""

    def setObjectName(self, name: str) -> None:
        """Accept object names."""
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
        """Record style text."""
        self.style = text

    def setText(self, text: str) -> None:
        """Record label text."""
        self.text = text


class FakeProgressBar(FakeWidget):
    """Small fake progress bar."""

    def setTextVisible(self, visible: bool) -> None:
        """Record text visibility."""
        self.text_visible = visible

    def setRange(self, minimum: int, maximum: int) -> None:
        """Record progress range."""
        self.range = (minimum, maximum)

    def setValue(self, value: int) -> None:
        """Record progress value."""
        self.value = value


class FakeLayout:
    """Small fake layout."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        self.widgets: list[object] = []

    def setContentsMargins(self, *args: object) -> None:
        """Accept margins."""
        return None

    def setSpacing(self, value: int) -> None:
        """Accept spacing."""
        self.spacing = value

    def addWidget(self, widget: object, *args: object, **kwargs: object) -> None:
        """Record one widget."""
        self.widgets.append(widget)


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


class FakeQt:
    """Small fake Qt namespace."""

    AlignRight = 1


def install_pyside6_stubs() -> None:
    """Install fake PySide6 modules for public import tests."""
    pyside6 = types.ModuleType("PySide6")
    qtcore = types.ModuleType("PySide6.QtCore")
    qtwidgets = types.ModuleType("PySide6.QtWidgets")
    qtcore.QTimer = FakeTimer
    qtcore.Qt = FakeQt
    qtwidgets.QFrame = FakeWidget
    qtwidgets.QHBoxLayout = FakeLayout
    qtwidgets.QLabel = FakeWidget
    qtwidgets.QProgressBar = FakeProgressBar
    sys.modules["PySide6"] = pyside6
    sys.modules["PySide6.QtCore"] = qtcore
    sys.modules["PySide6.QtWidgets"] = qtwidgets


install_pyside6_stubs()

from kanda_reasoner_app.manage_workflows.ai_review.running_indicator import (  # noqa: E402
    Tab2ActivityIndicator,
    install_tab2_activity_indicator,
)


class FakeWindow:
    """Small fake window."""


class FakeButtonLayout(FakeLayout):
    """Small fake button layout."""


def test_indicator_is_hidden_when_idle_and_visible_when_running() -> None:
    """The indicator is hidden until Tab 2 work is running."""
    indicator = Tab2ActivityIndicator()

    assert indicator.widget().visible is False

    indicator.start_deterministic("Check")
    assert indicator.widget().visible is True

    indicator.finish_success("Check finished")
    assert indicator.widget().visible is False


def test_public_install_contract_sets_window_attribute() -> None:
    """The public install helper returns and stores the indicator."""
    window = FakeWindow()
    layout = FakeButtonLayout()

    indicator = install_tab2_activity_indicator(window, layout)

    assert indicator is getattr(window, "_tab2_activity_indicator")
    assert len(layout.widgets) == 1
    assert indicator.widget().visible is False


if __name__ == "__main__":
    test_indicator_is_hidden_when_idle_and_visible_when_running()
    test_public_install_contract_sets_window_attribute()
    print("Tab 2 activity indicator contract tests passed.")
