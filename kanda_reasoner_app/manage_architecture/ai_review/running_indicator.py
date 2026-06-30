"""Green sonar floating activity monitor for Architecture Review work."""

from __future__ import annotations

import math
from importlib import import_module
from typing import Any

__all__ = ["Tab1ActivityIndicator", "install_tab1_activity_indicator"]


_HIDE_AFTER_FINISH_MS = 2200
_PANEL_WIDTH = 390
_PANEL_HEIGHT = 184
_PANEL_MARGIN = 22


# Green sonar palette. Variable names keep the v1 compatibility validator
# fragments, but the visual design now follows the original green sonar demo.
_BLUE_BG = "#040A06"
_BLUE_BG_2 = "#07120A"
_BLUE_BORDER = "#00CC66"
_BLUE_DIM = "#00441E"
_BLUE_MID = "#00CC66"
_BLUE_BRIGHT = "#AAFFCC"
_BLUE_TEXT = "#D9FFE8"
_BLUE_MUTED = "#6FE6A5"
_GRID_LINE = "#003318"
_SUCCESS = "#00FF88"
_WARNING = "#FFCC44"
_ERROR = "#FF4444"


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


def _qt_core_attr(name: str) -> Any:
    """Return a PySide6.QtCore attribute at GUI import time."""
    return getattr(import_module("PySide6.QtCore"), name)


def _qt_gui_attr(name: str) -> Any:
    """Return a PySide6.QtGui attribute at GUI import time."""
    return getattr(import_module("PySide6.QtGui"), name)


def _qt_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWidgets attribute at GUI import time."""
    return getattr(import_module("PySide6.QtWidgets"), name)


QColor = _qt_gui_attr("QColor")
QFont = _qt_gui_attr("QFont")
QGraphicsDropShadowEffect = _qt_widgets_attr("QGraphicsDropShadowEffect")
QHBoxLayout = _qt_widgets_attr("QHBoxLayout")
QLabel = _qt_widgets_attr("QLabel")
QPainter = _qt_gui_attr("QPainter")
QPainterPath = _qt_gui_attr("QPainterPath")
QPen = _qt_gui_attr("QPen")
QPointF = _qt_core_attr("QPointF")
QRadialGradient = _qt_gui_attr("QRadialGradient")
QRectF = _qt_core_attr("QRectF")
QFrame = _qt_widgets_attr("QFrame")
QSize = _qt_core_attr("QSize")
QSizePolicy = _qt_widgets_attr("QSizePolicy")
QObject = _qt_core_attr("QObject")
QTimer = _qt_core_attr("QTimer")
QVBoxLayout = _qt_widgets_attr("QVBoxLayout")
QWidget = _qt_widgets_attr("QWidget")
Qt = _qt_core_attr("Qt")
QEvent = _qt_core_attr("QEvent")


class _BlueSonarScope(QWidget):
    """Compact green sonar sweep with blip-hit ripple waves."""

    def __init__(self, parent: Any = None) -> None:
        super().__init__(parent)
        self._angle = 0.0
        self._last_angle = 0.0
        self._time = 0.0
        self._state = "running"
        self._waves: list[dict[str, float]] = []
        self._blips = [
            {"angle": 26.0, "distance": 0.52, "brightness": 0.0},
            {"angle": 124.0, "distance": 0.70, "brightness": 0.0},
            {"angle": 218.0, "distance": 0.46, "brightness": 0.0},
            {"angle": 304.0, "distance": 0.78, "brightness": 0.0},
        ]
        self.setMinimumSize(104, 104)
        self.setMaximumSize(118, 118)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def set_state(self, state: str) -> None:
        self._state = str(state or "running")
        self.update()

    def tick(self, dt: float) -> None:
        self._time += dt
        self._last_angle = self._angle
        self._angle = (self._angle + 78.0 * dt) % 360.0
        if self._state == "running":
            self._energize_crossed_blips()
        for blip in self._blips:
            blip["brightness"] = max(0.0, blip["brightness"] - dt * 1.35)
        for wave in self._waves:
            wave["radius"] += dt * 0.72
            wave["alpha"] -= dt * 1.05
        self._waves = [wave for wave in self._waves if wave["alpha"] > 0.0]
        self.update()

    def paintEvent(self, _event: Any) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._draw_scope(painter)
        painter.end()

    def _sweep_crossed(self, target_angle: float) -> bool:
        prev = self._last_angle
        curr = self._angle
        return prev <= target_angle < curr if curr >= prev else target_angle >= prev or target_angle < curr

    def _energize_crossed_blips(self) -> None:
        for blip in self._blips:
            if self._sweep_crossed(float(blip["angle"])):
                blip["brightness"] = 1.0
                self._waves.append({
                    "angle": float(blip["angle"]),
                    "distance": float(blip["distance"]),
                    "radius": 0.02,
                    "alpha": 1.0,
                })

    def _point(self, centre: Any, radius: float, angle_degrees: float, distance: float) -> Any:
        angle = math.radians(angle_degrees - 90)
        return QPointF(
            centre.x() + radius * distance * math.cos(angle),
            centre.y() + radius * distance * math.sin(angle),
        )

    def _draw_scope(self, painter: Any) -> None:
        width = self.width()
        height = self.height()
        centre = QPointF(width / 2.0, height / 2.0)
        radius = min(width, height) / 2.0 - 5.0

        background = QRadialGradient(centre, radius)
        background.setColorAt(0.0, QColor("#051209"))
        background.setColorAt(0.72, QColor("#030A05"))
        background.setColorAt(1.0, QColor("#020705"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(background)
        painter.drawEllipse(centre, radius, radius)

        grid_pen = QPen(QColor(_GRID_LINE), 0.8)
        grid_pen.setCosmetic(True)
        painter.setPen(grid_pen)
        painter.setBrush(Qt.NoBrush)
        for fraction in (0.33, 0.66, 1.0):
            painter.drawEllipse(centre, radius * fraction, radius * fraction)
        for degrees in range(0, 360, 45):
            edge = self._point(centre, radius, float(degrees), 1.0)
            painter.drawLine(centre, edge)

        self._draw_sweep_trail(painter, centre, radius)
        self._draw_blip_waves(painter, centre, radius)
        self._draw_blips(painter, centre, radius)
        self._draw_bezel(painter, centre, radius)

    def _draw_sweep_trail(self, painter: Any, centre: Any, radius: float) -> None:
        trail_degrees = 115.0
        steps = 34
        for index in range(steps):
            fraction = index / float(steps)
            angle_degrees = (self._angle - (1.0 - fraction) * trail_degrees) % 360.0
            color = QColor(_BLUE_MID)
            color.setAlphaF(0.04 + fraction * 0.22)
            path = QPainterPath()
            path.moveTo(centre)
            path.arcTo(
                QRectF(centre.x() - radius, centre.y() - radius, radius * 2, radius * 2),
                90 - angle_degrees,
                -(trail_degrees / float(steps)),
            )
            path.lineTo(centre)
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawPath(path)

        tip = self._point(centre, radius, self._angle, 1.0)
        for width, alpha in ((7.0, 0.10), (3.5, 0.28), (1.3, 0.96)):
            line_color = QColor(_BLUE_BRIGHT)
            line_color.setAlphaF(alpha)
            painter.setPen(QPen(line_color, width, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(centre, tip)

    def _draw_blip_waves(self, painter: Any, centre: Any, radius: float) -> None:
        painter.setBrush(Qt.NoBrush)
        for wave in self._waves:
            point = self._point(centre, radius, wave["angle"], wave["distance"])
            color = QColor(_BLUE_BRIGHT)
            color.setAlphaF(max(0.0, min(0.75, wave["alpha"] * 0.70)))
            painter.setPen(QPen(color, 1.25))
            wave_radius = radius * wave["radius"]
            painter.drawEllipse(point, wave_radius, wave_radius)

    def _draw_blips(self, painter: Any, centre: Any, radius: float) -> None:
        state_color = _ERROR if self._state == "error" else _SUCCESS if self._state == "success" else _BLUE_BRIGHT
        for blip in self._blips:
            point = self._point(centre, radius, blip["angle"], blip["distance"])
            brightness = blip["brightness"]
            halo = QRadialGradient(point, 14.0)
            halo_color = QColor(state_color)
            halo_color.setAlphaF(0.18 + brightness * 0.34)
            halo.setColorAt(0.0, halo_color)
            halo_end = QColor(state_color)
            halo_end.setAlphaF(0.0)
            halo.setColorAt(1.0, halo_end)
            painter.setPen(Qt.NoPen)
            painter.setBrush(halo)
            painter.drawEllipse(point, 14.0, 14.0)

            dot = QColor(state_color)
            dot.setAlphaF(0.55 + brightness * 0.45)
            painter.setBrush(dot)
            painter.drawEllipse(point, 3.4 + brightness * 1.2, 3.4 + brightness * 1.2)

    def _draw_bezel(self, painter: Any, centre: Any, radius: float) -> None:
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(_BLUE_BORDER), 1.5))
        painter.drawEllipse(centre, radius, radius)


class _SonarFloatingPanel(QFrame):
    """Floating lower-right Architecture Review monitor panel."""

    def __init__(self, parent: Any = None) -> None:
        super().__init__(parent)
        self.setObjectName("tab1SonarActivityPanel")
        self.setFixedSize(_PANEL_WIDTH, _PANEL_HEIGHT)
        self.setAttribute(Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

        root = QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(12)

        self.scope = _BlueSonarScope(self)
        root.addWidget(self.scope, 0, Qt.AlignVCenter)

        text_box = QWidget(self)
        text_layout = QVBoxLayout(text_box)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(3)

        self.title_label = QLabel("Architecture Review", self)
        self.title_label.setObjectName("tab1SonarTitle")
        self.status_label = QLabel("Running", self)
        self.status_label.setObjectName("tab1SonarStatus")
        self.detail_labels = [QLabel("", self) for _ in range(3)]
        for label in self.detail_labels:
            label.setObjectName("tab1SonarDetail")
            label.setWordWrap(True)

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.status_label)
        for label in self.detail_labels:
            text_layout.addWidget(label)
        text_layout.addStretch(1)
        root.addWidget(text_box, 1)

        self._apply_style("running")
        self.hide()

    def set_content(self, title: str, status: str, details: tuple[str, str, str], state: str) -> None:
        self.title_label.setText(str(title or "Architecture Review"))
        self.status_label.setText(str(status or "Running"))
        for index, label in enumerate(self.detail_labels):
            label.setText(str(details[index] if index < len(details) else ""))
        self.scope.set_state(state)
        self._apply_style(state)

    def _apply_style(self, state: str) -> None:
        accent = _BLUE_BORDER
        if state == "success":
            accent = _SUCCESS
        elif state == "error":
            accent = _ERROR
        elif state == "warning":
            accent = _WARNING
        self.setStyleSheet(
            "QFrame#tab1SonarActivityPanel {"
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, "
            "stop:0 " + _BLUE_BG_2 + ", stop:1 " + _BLUE_BG + ");"
            "border: 1px solid " + accent + ";"
            "border-radius: 16px;"
            "}"
            "QLabel#tab1SonarTitle {"
            "color: " + _BLUE_TEXT + ";"
            "font-family: Segoe UI;"
            "font-size: 11pt;"
            "font-weight: 700;"
            "}"
            "QLabel#tab1SonarStatus {"
            "color: " + accent + ";"
            "font-family: Segoe UI;"
            "font-size: 9pt;"
            "font-weight: 700;"
            "padding-bottom: 4px;"
            "}"
            "QLabel#tab1SonarDetail {"
            "color: " + _BLUE_MUTED + ";"
            "font-family: Segoe UI;"
            "font-size: 8.5pt;"
            "}"
        )


class Tab1ActivityIndicator(QObject):
    """Floating green sonar monitor shown while Tab 1 work runs."""

    def __init__(self, window: Any) -> None:
        super().__init__(window)
        self._window = window
        self._host = self._resolve_host_widget(window)
        self._panel = _SonarFloatingPanel(self._host)
        self._timer = QTimer(self._panel)
        self._timer.setInterval(25)
        self._timer.timeout.connect(self._tick)
        self._hide_timer = QTimer(self._panel)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.set_idle)
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
        """Hide the floating panel and stop animation."""
        self._last_state = "idle"
        if self._timer.isActive():
            self._timer.stop()
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        self._panel.hide()

    def eventFilter(self, watched: Any, event: Any) -> bool:
        event_type = event.type() if event is not None else None
        if event_type in (QEvent.Resize, QEvent.Show):
            self._reposition()
        return False

    def _resolve_host_widget(self, window: Any) -> Any:
        central_widget = getattr(window, "centralWidget", None)
        if callable(central_widget):
            host = central_widget()
            if host is not None:
                return host
        return window

    def _install_event_filters(self) -> None:
        for widget in (self._host, self._window):
            install = getattr(widget, "installEventFilter", None)
            if callable(install):
                install(self)

    def _start(self, title: str, status: str, details: tuple[str, str, str]) -> None:
        self._last_state = "running"
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        self._panel.set_content(title, status, details, "running")
        self._reposition()
        self._panel.show()
        self._panel.raise_()
        if not self._timer.isActive():
            self._timer.start()

    def _stop(self, status: str, details: tuple[str, str, str], state: str) -> None:
        self._last_state = state
        if self._timer.isActive():
            self._timer.stop()
        self._panel.set_content("Architecture Review", status, details, state)
        self._reposition()
        self._panel.show()
        self._panel.raise_()
        self._hide_timer.start(_HIDE_AFTER_FINISH_MS)

    def _tick(self) -> None:
        self._panel.scope.tick(0.025)

    def _reposition(self) -> None:
        host = self._host
        if host is None:
            return
        width = int(getattr(host, "width")()) if hasattr(host, "width") else 0
        height = int(getattr(host, "height")()) if hasattr(host, "height") else 0
        if width <= 0 or height <= 0:
            return
        size = QSize(_PANEL_WIDTH, _PANEL_HEIGHT)
        x = max(_PANEL_MARGIN, width - size.width() - _PANEL_MARGIN)
        y = max(_PANEL_MARGIN, height - size.height() - _PANEL_MARGIN)
        self._panel.move(x, y)


def install_tab1_activity_indicator(window: Any, buttons_layout: Any) -> Tab1ActivityIndicator:
    """Install and return the Tab 1 floating green sonar activity monitor."""
    indicator = Tab1ActivityIndicator(window)
    window._tab1_activity_indicator = indicator
    return indicator
