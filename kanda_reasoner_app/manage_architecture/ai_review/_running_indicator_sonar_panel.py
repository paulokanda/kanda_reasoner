# project-path: kanda_reasoner_app/manage_architecture/ai_review/_running_indicator_sonar_panel.py
"""Private visual owner for the Architecture Review sonar activity panel."""

from __future__ import annotations

import math
from typing import Any

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

__all__: list[str] = []

_PANEL_WIDTH = 390
_PANEL_HEIGHT = 184

# Green sonar palette. The historical _BLUE_* names remain private compatibility
# labels for existing validation vocabulary; the values are the active green set.
_BLUE_BG = "#040A06"
_BLUE_BG_2 = "#07120A"
_BLUE_BORDER = "#00CC66"
_BLUE_MID = "#00CC66"
_BLUE_BRIGHT = "#AAFFCC"
_BLUE_TEXT = "#D9FFE8"
_BLUE_MUTED = "#6FE6A5"
_GRID_LINE = "#003318"
_SUCCESS = "#00FF88"
_WARNING = "#FFCC44"
_ERROR = "#FF4444"


class _BlueSonarScope(QWidget):
    """Compact green sonar sweep with blip-hit ripple waves."""

    def __init__(self, parent: Any = None) -> None:
        """Initialize the visual state and fixed widget sizing."""
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
        """Set the current visual state and request repaint."""
        self._state = str(state or "running")
        self.update()

    def tick(self, dt: float) -> None:
        """Advance sweep, blip brightness, and ripple animation."""
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
        """Paint the complete sonar scope."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._draw_scope(painter)
        painter.end()

    def _sweep_crossed(self, target_angle: float) -> bool:
        """Return whether the sweep crossed one target angle this tick."""
        previous = self._last_angle
        current = self._angle
        if current >= previous:
            return previous <= target_angle < current
        return target_angle >= previous or target_angle < current

    def _energize_crossed_blips(self) -> None:
        """Light crossed blips and append their new ripple waves."""
        for blip in self._blips:
            if self._sweep_crossed(float(blip["angle"])):
                blip["brightness"] = 1.0
                self._waves.append(
                    {
                        "angle": float(blip["angle"]),
                        "distance": float(blip["distance"]),
                        "radius": 0.02,
                        "alpha": 1.0,
                    }
                )

    def _point(
        self,
        centre: Any,
        radius: float,
        angle_degrees: float,
        distance: float,
    ) -> Any:
        """Return a point at a polar offset inside the sonar circle."""
        angle = math.radians(angle_degrees - 90)
        return QPointF(
            centre.x() + radius * distance * math.cos(angle),
            centre.y() + radius * distance * math.sin(angle),
        )

    def _draw_scope(self, painter: Any) -> None:
        """Draw background, grid, sweep, ripples, blips, and bezel."""
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
        """Draw the translucent sweep trail and bright current sweep line."""
        trail_degrees = 115.0
        steps = 34
        for index in range(steps):
            fraction = index / float(steps)
            angle_degrees = (
                self._angle - (1.0 - fraction) * trail_degrees
            ) % 360.0
            color = QColor(_BLUE_MID)
            color.setAlphaF(0.04 + fraction * 0.22)
            path = QPainterPath()
            path.moveTo(centre)
            path.arcTo(
                QRectF(
                    centre.x() - radius,
                    centre.y() - radius,
                    radius * 2,
                    radius * 2,
                ),
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
        """Draw the expanding hit ripples."""
        painter.setBrush(Qt.NoBrush)
        for wave in self._waves:
            point = self._point(
                centre,
                radius,
                wave["angle"],
                wave["distance"],
            )
            color = QColor(_BLUE_BRIGHT)
            color.setAlphaF(max(0.0, min(0.75, wave["alpha"] * 0.70)))
            painter.setPen(QPen(color, 1.25))
            wave_radius = radius * wave["radius"]
            painter.drawEllipse(point, wave_radius, wave_radius)

    def _draw_blips(self, painter: Any, centre: Any, radius: float) -> None:
        """Draw sonar blips and glow halos."""
        if self._state == "error":
            state_color = _ERROR
        elif self._state == "success":
            state_color = _SUCCESS
        else:
            state_color = _BLUE_BRIGHT
        for blip in self._blips:
            point = self._point(
                centre,
                radius,
                blip["angle"],
                blip["distance"],
            )
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
            painter.drawEllipse(
                point,
                3.4 + brightness * 1.2,
                3.4 + brightness * 1.2,
            )

    def _draw_bezel(self, painter: Any, centre: Any, radius: float) -> None:
        """Draw the outer sonar bezel."""
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(_BLUE_BORDER), 1.5))
        painter.drawEllipse(centre, radius, radius)


class _SonarFloatingPanel(QFrame):
    """Floating lower-right Architecture Review monitor panel."""

    def __init__(self, parent: Any = None) -> None:
        """Build the floating panel layout and initial hidden state."""
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

    def set_content(
        self,
        title: str,
        status: str,
        details: tuple[str, str, str],
        state: str,
    ) -> None:
        """Update text, scope state, and state-dependent styling."""
        self.title_label.setText(str(title or "Architecture Review"))
        self.status_label.setText(str(status or "Running"))
        for index, label in enumerate(self.detail_labels):
            label.setText(str(details[index] if index < len(details) else ""))
        self.scope.set_state(state)
        self._apply_style(state)

    def _apply_style(self, state: str) -> None:
        """Apply the panel accent and text palette for one state."""
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
