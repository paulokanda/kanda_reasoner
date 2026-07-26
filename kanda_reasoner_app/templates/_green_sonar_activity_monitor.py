# project-path: kanda_reasoner_app/templates/_green_sonar_activity_monitor.py
"""Activity monitor controller for the green sonar floating panel."""

from __future__ import annotations

from typing import Any

from ._green_sonar_panel import _SonarPanel
from ._green_sonar_runtime import (
    QObject,
    QEvent,
    QSize,
    QTimer,
    _HIDE_AFTER_FINISH_MS,
    _PANEL_HEIGHT,
    _PANEL_MARGIN,
    _PANEL_WIDTH,
)

class _GreenSonarActivityMonitor(QObject):
    """Reusable lower-right floating green sonar process monitor."""

    def __init__(self, window: Any, *, title: str, host: Any | None = None) -> None:
        """Create a monitor attached to ``window`` or ``host``."""

        super().__init__(window)
        self._window = window
        self._title = title
        self._host = host or self._resolve_host_widget(window)
        self._panel = _SonarPanel(self._host)
        self._timer = QTimer(self._panel)
        self._timer.setInterval(25)
        self._timer.timeout.connect(self._tick)
        self._hide_timer = QTimer(self._panel)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.set_idle)
        self._install_event_filters()
        self.set_idle()

    def widget(self) -> Any:
        """Return the floating panel widget."""

        return self._panel

    def start(self, status: str, details: tuple[str, str, str]) -> None:
        """Show the monitor in running state."""

        if self._hide_timer.isActive():
            self._hide_timer.stop()
        self._panel.set_content(self._title, status, details, "running")
        self._reposition()
        self._panel.show()
        self._panel.raise_()
        if not self._timer.isActive():
            self._timer.start()

    def finish_success(self, status: str, details: tuple[str, str, str]) -> None:
        """Show the monitor briefly in success state."""

        self._finish(status, details, "success")

    def finish_error(self, status: str, details: tuple[str, str, str]) -> None:
        """Show the monitor briefly in error state."""

        self._finish(status, details, "error")

    def set_idle(self) -> None:
        """Hide the monitor and stop timers."""

        if self._timer.isActive():
            self._timer.stop()
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        self._panel.hide()

    def eventFilter(self, _watched: Any, event: Any) -> bool:
        """Reposition the panel when the host is resized or shown."""

        event_type = event.type() if event is not None else None
        if event_type in (QEvent.Resize, QEvent.Show):
            self._reposition()
        return False

    def _resolve_host_widget(self, window: Any) -> Any:
        """Return a central widget when the window exposes one."""

        central_widget = getattr(window, "centralWidget", None)
        if callable(central_widget):
            host = central_widget()
            if host is not None:
                return host
        return window

    def _install_event_filters(self) -> None:
        """Install resize/show event filters on host and window."""

        for widget in (self._host, self._window):
            install = getattr(widget, "installEventFilter", None)
            if callable(install):
                install(self)

    def _finish(self, status: str, details: tuple[str, str, str], state: str) -> None:
        """Show the monitor in a terminal state and schedule hiding."""

        if self._timer.isActive():
            self._timer.stop()
        self._panel.set_content(self._title, status, details, state)
        self._reposition()
        self._panel.show()
        self._panel.raise_()
        self._hide_timer.start(_HIDE_AFTER_FINISH_MS)

    def _tick(self) -> None:
        """Advance the panel scope animation."""

        self._panel.scope.tick(0.025)

    def _reposition(self) -> None:
        """Move the panel to the lower-right corner of the host."""

        host = self._host
        width_getter = getattr(host, "width", None)
        height_getter = getattr(host, "height", None)
        if not callable(width_getter) or not callable(height_getter):
            return
        width = int(width_getter())
        height = int(height_getter())
        if width <= 0 or height <= 0:
            return
        size = QSize(_PANEL_WIDTH, _PANEL_HEIGHT)
        x = max(_PANEL_MARGIN, width - size.width() - _PANEL_MARGIN)
        y = max(_PANEL_MARGIN, height - size.height() - _PANEL_MARGIN)
        self._panel.move(x, y)
