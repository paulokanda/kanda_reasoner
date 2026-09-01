# project-path: tools/brain_navigator_lifecycle_qt_probe.py
"""Run isolated simulated and native Qt Brain Navigator lifecycle probes."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from typing import Any

__all__ = ["validate_real_qt_tab_hide", "validate_simulated_tab_hide"]

PREVIEW_MODULE_NAME = (
    "kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator."
    "_neural_architecture_preview"
)
TEMPLATE_MODULE_NAME = (
    "kanda_reasoner_app.reasoner_tools_gui_shell.brain_navigator.assets."
    "brain_visual_floating_window_template"
)


def require(condition: bool, message: str) -> None:
    """Raise one focused probe failure."""

    if not condition:
        raise AssertionError(message)


class FakePage:
    """Minimal page stand-in for JavaScript cleanup inspection."""

    def __init__(self) -> None:
        self.scripts: list[str] = []
        self.web_channel: object | None = None
        self.raise_runtime = False

    def setWebChannel(self, channel: object) -> None:
        self.web_channel = channel

    def runJavaScript(self, script: str, callback: object | None = None) -> None:
        if self.raise_runtime:
            raise RuntimeError("page already deleted")
        self.scripts.append(script)
        if callable(callback):
            callback(None)


class FakeWidget:
    """Minimal QWidget stand-in with a base hideEvent contract."""

    def __init__(self) -> None:
        self.object_name = ""
        self.window_title = ""
        self.base_hide_event_count = 0

    def setObjectName(self, value: str) -> None:
        self.object_name = value

    def setWindowTitle(self, value: str) -> None:
        self.window_title = value

    def hideEvent(self, _event: object) -> None:
        self.base_hide_event_count += 1


class FakeLayout:
    """Minimal QVBoxLayout stand-in."""

    def __init__(self, parent: object) -> None:
        self.parent = parent
        self.widgets: list[object] = []
        self.margins: tuple[int, int, int, int] | None = None

    def setContentsMargins(self, *values: int) -> None:
        self.margins = tuple(values)  # type: ignore[assignment]

    def addWidget(self, widget: object) -> None:
        self.widgets.append(widget)


class FakeSettings:
    """Minimal QWebEngineSettings stand-in."""

    def __init__(self) -> None:
        self.attributes: dict[object, bool] = {}

    def setAttribute(self, attribute: object, enabled: bool) -> None:
        self.attributes[attribute] = bool(enabled)

    def testAttribute(self, attribute: object) -> bool:
        return bool(self.attributes.get(attribute, False))


class FakeQWebEngineSettings:
    """Expose the one WebAttribute used by Brain Navigator."""

    class WebAttribute:
        LocalContentCanAccessRemoteUrls = object()


class FakeWebView:
    """Minimal QWebEngineView stand-in."""

    def __init__(self) -> None:
        self.object_name = ""
        self.html = ""
        self._page = FakePage()
        self._settings = FakeSettings()

    def setObjectName(self, value: str) -> None:
        self.object_name = value

    def page(self) -> FakePage:
        return self._page

    def settings(self) -> FakeSettings:
        return self._settings

    def setHtml(self, html: str) -> None:
        self.html = html


class FakeBridgeBundle:
    """Minimal bridge bundle stand-in."""

    def __init__(self) -> None:
        self.channel = object()

    def connect_to_page(self, page: FakePage) -> None:
        page.setWebChannel(self.channel)


def _load_preview_module(root: Path) -> Any:
    """Load a fresh preview module from the selected project root."""

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    sys.modules.pop(PREVIEW_MODULE_NAME, None)
    return importlib.import_module(PREVIEW_MODULE_NAME)


def validate_simulated_tab_hide(root: Path) -> None:
    """Exercise page cleanup and restore every injected test double."""

    module = _load_preview_module(root)
    original_widget_factory = module._qt_widgets_attr
    original_web_factory = module._qt_web_engine_widgets_attr
    original_core_factory = module._qt_web_engine_core_attr
    original_bridge_factory = module.create_brain_web_bridge
    original_html_builder = module.build_neural_architecture_preview_html
    widget_types: dict[str, Any] = {
        "QWidget": FakeWidget,
        "QVBoxLayout": FakeLayout,
    }
    try:
        module._qt_widgets_attr = lambda name: widget_types[name]
        module._qt_web_engine_widgets_attr = lambda _name: FakeWebView
        module._qt_web_engine_core_attr = lambda _name: FakeQWebEngineSettings
        module.create_brain_web_bridge = lambda _config: FakeBridgeBundle()
        module.build_neural_architecture_preview_html = lambda **_kwargs: "<html></html>"

        bundle = module.create_neural_architecture_preview()
        bundle.widget.hideEvent(object())
        require(
            bundle.widget.base_hide_event_count == 1,
            "base QWidget.hideEvent was not preserved",
        )
        require(
            bundle.web_view.page().scripts == [module._CLOSE_FLOATING_WINDOW_JS],
            "tab hide did not request page-local floating-window cleanup",
        )
        print("SIMULATED_TAB_SWITCH_CLOSES_FLOATING_WINDOW: PASS")

        bundle.web_view.page().raise_runtime = True
        bundle.widget.hideEvent(object())
        require(
            bundle.widget.base_hide_event_count == 2,
            "Qt teardown containment skipped the base hideEvent",
        )
        print("SIMULATED_DELETED_WEBENGINE_PAGE_SAFE: PASS")
    finally:
        module._qt_widgets_attr = original_widget_factory
        module._qt_web_engine_widgets_attr = original_web_factory
        module._qt_web_engine_core_attr = original_core_factory
        module.create_brain_web_bridge = original_bridge_factory
        module.build_neural_architecture_preview_html = original_html_builder
        sys.modules.pop(PREVIEW_MODULE_NAME, None)

    print("SIMULATED_QT_FACTORY_STATE_RESTORED: PASS")


def validate_real_qt_tab_hide(root: Path) -> bool:
    """Validate the real Qt wrapper lifecycle without Chromium callback coupling."""

    if os.name != "nt":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    try:
        from PySide6.QtCore import QCoreApplication, QEvent
        from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
    except Exception:
        print("REAL_QT_BRAIN_NAVIGATOR_TAB_HIDE_CLOSE: NOT_RUN", flush=True)
        print(
            "REAL_QT_BRAIN_NAVIGATOR_FLOATING_WINDOW_READABILITY: NOT_RUN",
            flush=True,
        )
        return False

    module = _load_preview_module(root)
    template_module = importlib.import_module(TEMPLATE_MODULE_NAME)
    css = template_module.build_floating_remember_window_css()
    controlled_html = """<!doctype html><html><body>
<div id=\"floatingRegionWindow\" style=\"display:block\"></div>
<script>function hideFloatingRememberWindow(){}</script>
</body></html>"""

    class NativeProbePage(FakePage):
        """Record the production cleanup request behind a real QWidget."""

    class NativeProbeWebView(QWidget):
        """Real QWidget replacement for the WebEngine surface."""

        def __init__(self) -> None:
            super().__init__()
            self._page = NativeProbePage()
            self.html = ""

        def page(self) -> NativeProbePage:
            return self._page

        def settings(self) -> FakeSettings:
            if not hasattr(self, "_settings"):
                self._settings = FakeSettings()
            return self._settings

        def setHtml(self, html: str) -> None:
            self.html = html

    class NativeBridgeBundle:
        """No-op bridge owner for the native wrapper lifecycle probe."""

        def connect_to_page(self, page: NativeProbePage) -> None:
            page.setWebChannel(self)

    original_widget_factory = module._qt_widgets_attr
    original_web_factory = module._qt_web_engine_widgets_attr
    original_core_factory = module._qt_web_engine_core_attr
    original_bridge_builder = module.create_brain_web_bridge
    original_html_builder = module.build_neural_architecture_preview_html
    module._qt_widgets_attr = lambda name: {
        "QWidget": QWidget,
        "QVBoxLayout": QVBoxLayout,
    }[name]
    module._qt_web_engine_widgets_attr = lambda _name: NativeProbeWebView
    module._qt_web_engine_core_attr = lambda _name: FakeQWebEngineSettings
    module.create_brain_web_bridge = lambda _config: NativeBridgeBundle()
    module.build_neural_architecture_preview_html = lambda **_kwargs: controlled_html

    app = QApplication.instance() or QApplication([])
    bundle = None
    try:
        bundle = module.create_neural_architecture_preview()
        widget = bundle.widget
        require(isinstance(widget, QWidget), "preview wrapper is not a real QWidget")
        require(
            isinstance(bundle.web_view, QWidget),
            "preview surface is not a real QWidget",
        )
        for method_name in ("show", "hide", "close", "deleteLater"):
            require(
                callable(getattr(widget, method_name, None)),
                "real Qt preview wrapper lacks " + method_name + "()",
            )
        print("REAL_QT_NATIVE_WIDGET_API: PASS", flush=True)
        print("REAL_QT_CHROMIUM_CALLBACK_DEPENDENCY_REMOVED: PASS", flush=True)

        require(
            bundle.web_view.html == controlled_html,
            "factory did not deliver HTML to the native probe surface",
        )
        require(
            "font-family: 'Segoe UI', Arial, sans-serif;" in css,
            "readable sans-serif CSS stack is missing",
        )
        require("font-size: 20px;" in css, "20px title CSS is missing")
        require("font-size: 14px;" in css, "14px purpose CSS is missing")
        require("Courier New" not in css, "monospace CSS remains active")
        print("REAL_QT_READABLE_CSS_CONTRACT: PASS", flush=True)
        print(
            "REAL_QT_BRAIN_NAVIGATOR_FLOATING_WINDOW_READABILITY: PASS",
            flush=True,
        )

        widget.resize(720, 480)
        widget.move(-30000, -30000)
        widget.show()
        app.processEvents()
        page = bundle.web_view.page()
        page.scripts.clear()
        widget.hide()
        app.processEvents()
        require(
            page.scripts == [module._CLOSE_FLOATING_WINDOW_JS],
            "real QWidget hideEvent did not request floating-window cleanup",
        )
        print("REAL_QT_NATIVE_HIDE_EVENT_DELIVERED: PASS", flush=True)
        print("REAL_QT_BRAIN_NAVIGATOR_TAB_HIDE_CLOSE: PASS", flush=True)
    finally:
        module._qt_widgets_attr = original_widget_factory
        module._qt_web_engine_widgets_attr = original_web_factory
        module._qt_web_engine_core_attr = original_core_factory
        module.create_brain_web_bridge = original_bridge_builder
        module.build_neural_architecture_preview_html = original_html_builder
        if bundle is not None:
            widget = getattr(bundle, "widget", None)
            for method_name in ("close", "deleteLater"):
                callback = getattr(widget, method_name, None)
                if callable(callback):
                    try:
                        callback()
                    except RuntimeError:
                        pass
        app.processEvents()
        try:
            QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
            app.processEvents()
        except (RuntimeError, TypeError):
            pass
        sys.modules.pop(PREVIEW_MODULE_NAME, None)
    return True
