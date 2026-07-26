# project-path: kanda_reasoner_app/templates/green_sonar_monitor.py
"""Public facade for the reusable green sonar activity monitor."""

from __future__ import annotations

from ._green_sonar_activity_monitor import _GreenSonarActivityMonitor
from ._green_sonar_panel import _SonarPanel
from ._green_sonar_runtime import (
    ERROR,
    GRID_LINE,
    QColor,
    QEvent,
    QFont,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QObject,
    QPainter,
    QPainterPath,
    QPen,
    QPointF,
    QRadialGradient,
    QRectF,
    QSize,
    QSizePolicy,
    QTimer,
    QVBoxLayout,
    QWidget,
    Qt,
    SONAR_BG,
    SONAR_BG_2,
    SONAR_BORDER,
    SONAR_BRIGHT,
    SONAR_DIM,
    SONAR_MID,
    SONAR_MUTED,
    SONAR_TEXT,
    SUCCESS,
    WARNING,
    _HIDE_AFTER_FINISH_MS,
    _PANEL_HEIGHT,
    _PANEL_MARGIN,
    _PANEL_WIDTH,
    _qt_core_attr,
    _qt_gui_attr,
    _qt_widgets_attr,
)
from ._green_sonar_scope import _SonarScope

__all__ = ["GreenSonarActivityMonitor"]


class GreenSonarActivityMonitor(_GreenSonarActivityMonitor):
    """Public facade class for the reusable green sonar activity monitor."""
