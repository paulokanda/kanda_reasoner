# project-path: kanda_reasoner_app/manage_architecture/ai_review/running_indicator.py
"""Green sonar floating activity monitor for Architecture Review work."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QEvent, QObject, QSize

from ._running_indicator_sonar_panel import _SonarFloatingPanel

__all__ = ["Tab1ActivityIndicator", "install_tab1_activity_indicator"]

_HIDE_AFTER_FINISH_MS = 2200
_ANIMATION_INTERVAL_MS = 25
_PANEL_WIDTH = 390
_PANEL_HEIGHT = 184
_PANEL_MARGIN = 22

_MODE_CONTEXT = {
    "validate": (
        "Checking architecture manifests",
        "Verifying import surfaces and module maps",
        "Results stream into Project Audit Results",
    ),
    "diff": (
        "Comparing generated architecture reports",
        "Finding drift before any write action",
        "Diff evidence stays in the audit panel",
    ),
    "scan": (
        "Mapping source ownership seams",
        "Collecting module and package structure",
        "No files are written during scan mode",
    ),
    "write": (
        "Preparing governed architecture writes",
        "Strict confirmation stays active before changes",
        "Write output will be recorded in the audit panel",
    ),
}


class Tab1ActivityIndicator(QObject):
    """Floating green sonar monitor shown while Tab 1 work runs."""

    def __init__(self, window: Any) -> None:
        """Create the controller, panel, and event-filter lifecycle."""
        super().__init__(window)
        self._window = window
        self._host = self._resolve_host_widget(window)
        self._panel = _SonarFloatingPanel(self._host)
        self._animation_timer_id: int | None = None
        self._hide_timer_id: int | None = None
        self._last_state = "idle"
        self._install_event_filters()
        self.set_idle()

    def widget(self) -> Any:
        """Return the floating panel for compatibility with older callers."""
        return self._panel

    def start_heuristic(self, mode: str) -> None:
        """Show deterministic Architecture Review work context."""
        normalized_mode = str(mode or "validate").strip().lower()
        details = _MODE_CONTEXT.get(normalized_mode, _MODE_CONTEXT["validate"])
        self._start(
            title="Architecture Review",
            status="Running " + normalized_mode + " mode",
            details=details,
        )

    def start_ai_review(self, model_name: str = "") -> None:
        """Show advisory AI review context."""
        model = str(model_name or "auto model").strip()
        self._start(
            title="Architecture Review",
            status="Advisory AI review running",
            details=(
                "Reading the latest deterministic audit output",
                "Model: " + model,
                "Deterministic checks remain authoritative",
            ),
        )

    def finish_success(self, message: str) -> None:
        """Show a brief success state, then hide."""
        self._stop(
            status="Complete: " + str(message or "work finished"),
            details=(
                "Architecture review process finished",
                "Review the Project Audit Results panel",
                "Ready for the next governed action",
            ),
            state="success",
        )

    def finish_error(self, message: str) -> None:
        """Show a brief attention state, then hide."""
        self._stop(
            status="Needs review: " + str(message or "work finished"),
            details=(
                "Architecture review process finished with issues",
                "Check the audit panel before continuing",
                "No automatic write is performed by this monitor",
            ),
            state="error",
        )

    def set_idle(self) -> None:
        """Hide the floating panel and stop both timer lifecycles."""
        self._last_state = "idle"
        self._stop_animation_timer()
        self._cancel_hide_timer()
        self._panel.hide()

    def eventFilter(self, watched: Any, event: Any) -> bool:
        """Reposition when the host or window is resized or shown."""
        del watched
        event_type = event.type() if event is not None else None
        if event_type in (QEvent.Resize, QEvent.Show):
            self._reposition()
        return False

    def timerEvent(self, event: Any) -> None:
        """Advance animation or complete the delayed-hide timer event."""
        timer_id = event.timerId()
        if self._animation_timer_id == timer_id:
            self._tick()
            return
        if self._hide_timer_id == timer_id:
            self._cancel_hide_timer()
            self.set_idle()
            return
        super().timerEvent(event)

    def _resolve_host_widget(self, window: Any) -> Any:
        """Return the central widget when the window exposes one."""
        try:
            central_widget = window.centralWidget
        except AttributeError:
            return window
        if callable(central_widget):
            host = central_widget()
            if host is not None:
                return host
        return window

    def _install_event_filters(self) -> None:
        """Install this QObject as a filter on the host and window."""
        for widget in (self._host, self._window):
            try:
                install = widget.installEventFilter
            except AttributeError:
                continue
            if callable(install):
                install(self)

    def _start(
        self,
        title: str,
        status: str,
        details: tuple[str, str, str],
    ) -> None:
        """Enter running state and ensure animation timer ownership."""
        self._last_state = "running"
        self._cancel_hide_timer()
        self._panel.set_content(title, status, details, "running")
        self._reposition()
        self._panel.show()
        self._panel.raise_()
        self._start_animation_timer()

    def _stop(
        self,
        status: str,
        details: tuple[str, str, str],
        state: str,
    ) -> None:
        """Show one terminal state and schedule delayed hiding."""
        self._last_state = state
        self._stop_animation_timer()
        self._panel.set_content("Architecture Review", status, details, state)
        self._reposition()
        self._panel.show()
        self._panel.raise_()
        self._cancel_hide_timer()
        self._hide_timer_id = self.startTimer(_HIDE_AFTER_FINISH_MS)

    def _start_animation_timer(self) -> None:
        """Start the repeating animation timer when not already active."""
        if self._animation_timer_id is None:
            self._animation_timer_id = self.startTimer(_ANIMATION_INTERVAL_MS)

    def _stop_animation_timer(self) -> None:
        """Stop the repeating animation timer when active."""
        if self._animation_timer_id is None:
            return
        timer_id = self._animation_timer_id
        self._animation_timer_id = None
        self.killTimer(timer_id)

    def _cancel_hide_timer(self) -> None:
        """Stop the delayed-hide timer when active."""
        if self._hide_timer_id is None:
            return
        timer_id = self._hide_timer_id
        self._hide_timer_id = None
        self.killTimer(timer_id)

    def _tick(self) -> None:
        """Advance the sonar scope by one 25 ms animation step."""
        self._panel.scope.tick(0.025)

    def _reposition(self) -> None:
        """Move the panel to the lower-right corner of its host."""
        host = self._host
        if host is None:
            return
        try:
            width_getter = host.width
            height_getter = host.height
        except AttributeError:
            return
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


def install_tab1_activity_indicator(
    window: Any,
    buttons_layout: Any,
) -> Tab1ActivityIndicator:
    """Install and return the Tab 1 floating green sonar activity monitor."""
    del buttons_layout
    indicator = Tab1ActivityIndicator(window)
    window._tab1_activity_indicator = indicator
    return indicator
