# project-path: kanda_reasoner_app/templates/_green_sonar_scope.py
"""Animated sonar scope widget for the green activity monitor."""

from __future__ import annotations

import math
from typing import Any

from ._green_sonar_runtime import (
    ERROR,
    GRID_LINE,
    QPointF,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
    QRectF,
    QSizePolicy,
    Qt,
    QColor,
    SONAR_BORDER,
    SONAR_BRIGHT,
    SONAR_MID,
    SUCCESS,
    QWidget,
)

class _SonarScope(QWidget):
    """Compact phosphor-green sonar sweep with hit-triggered ripples."""

    def __init__(self, parent: Any = None) -> None:
        """Initialize the scope animation state."""

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
        """Set the current visual state."""

        self._state = str(state or "running")
        self.update()

    def tick(self, dt: float) -> None:
        """Advance the sweep animation by ``dt`` seconds."""

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
        """Paint the sonar scope."""

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._draw_scope(painter)
        painter.end()

    def _sweep_crossed(self, target_angle: float) -> bool:
        """Return whether the sweep crossed ``target_angle`` this tick."""

        previous = self._last_angle
        current = self._angle
        if current >= previous:
            return previous <= target_angle < current
        return target_angle >= previous or target_angle < current

    def _energize_crossed_blips(self) -> None:
        """Light blips and spawn ripple waves as the sweep crosses them."""

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
        """Return the point at a polar offset inside the sonar circle."""

        angle = math.radians(angle_degrees - 90)
        return QPointF(
            centre.x() + radius * distance * math.cos(angle),
            centre.y() + radius * distance * math.sin(angle),
        )

    def _draw_scope(self, painter: Any) -> None:
        """Draw the scope background, grid, sweep, waves, and blips."""

        centre = QPointF(self.width() / 2.0, self.height() / 2.0)
        radius = min(self.width(), self.height()) / 2.0 - 5.0
        background = QRadialGradient(centre, radius)
        background.setColorAt(0.0, QColor("#051209"))
        background.setColorAt(0.72, QColor("#030A05"))
        background.setColorAt(1.0, QColor("#020705"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(background)
        painter.drawEllipse(centre, radius, radius)
        grid_pen = QPen(QColor(GRID_LINE), 0.8)
        grid_pen.setCosmetic(True)
        painter.setPen(grid_pen)
        painter.setBrush(Qt.NoBrush)
        for fraction in (0.33, 0.66, 1.0):
            painter.drawEllipse(centre, radius * fraction, radius * fraction)
        for degrees in range(0, 360, 45):
            painter.drawLine(centre, self._point(centre, radius, float(degrees), 1.0))
        self._draw_sweep_trail(painter, centre, radius)
        self._draw_waves(painter, centre, radius)
        self._draw_blips(painter, centre, radius)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(SONAR_BORDER), 1.5))
        painter.drawEllipse(centre, radius, radius)

    def _draw_sweep_trail(self, painter: Any, centre: Any, radius: float) -> None:
        """Draw the translucent sweep wedge and bright sweep tip."""

        trail_degrees = 115.0
        steps = 34
        for index in range(steps):
            fraction = index / float(steps)
            angle_degrees = (self._angle - (1.0 - fraction) * trail_degrees) % 360.0
            color = QColor(SONAR_MID)
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
            line_color = QColor(SONAR_BRIGHT)
            line_color.setAlphaF(alpha)
            painter.setPen(QPen(line_color, width, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(centre, tip)

    def _draw_waves(self, painter: Any, centre: Any, radius: float) -> None:
        """Draw hit ripple waves."""

        painter.setBrush(Qt.NoBrush)
        for wave in self._waves:
            point = self._point(centre, radius, wave["angle"], wave["distance"])
            color = QColor(SONAR_BRIGHT)
            color.setAlphaF(max(0.0, min(0.75, wave["alpha"] * 0.70)))
            painter.setPen(QPen(color, 1.25))
            painter.drawEllipse(point, radius * wave["radius"], radius * wave["radius"])

    def _draw_blips(self, painter: Any, centre: Any, radius: float) -> None:
        """Draw the sonar blips and their glow halos."""

        state_color = ERROR if self._state == "error" else SUCCESS if self._state == "success" else SONAR_BRIGHT
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
