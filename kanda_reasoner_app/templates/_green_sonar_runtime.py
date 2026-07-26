# project-path: kanda_reasoner_app/templates/_green_sonar_runtime.py
"""Runtime constants and Qt bindings for the green sonar monitor."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "ERROR",
    "GRID_LINE",
    "QColor",
    "QEvent",
    "QFont",
    "QFrame",
    "QGraphicsDropShadowEffect",
    "QHBoxLayout",
    "QLabel",
    "QObject",
    "QPainter",
    "QPainterPath",
    "QPen",
    "QPointF",
    "QRadialGradient",
    "QRectF",
    "QSize",
    "QSizePolicy",
    "QTimer",
    "QVBoxLayout",
    "QWidget",
    "Qt",
    "SONAR_BG",
    "SONAR_BG_2",
    "SONAR_BORDER",
    "SONAR_BRIGHT",
    "SONAR_DIM",
    "SONAR_MID",
    "SONAR_MUTED",
    "SONAR_TEXT",
    "SUCCESS",
    "WARNING",
]

_HIDE_AFTER_FINISH_MS = 2200
_PANEL_WIDTH = 390
_PANEL_HEIGHT = 184
_PANEL_MARGIN = 22

SONAR_BG = "#040A06"
SONAR_BG_2 = "#07120A"
SONAR_BORDER = "#00CC66"
SONAR_DIM = "#00441E"
SONAR_MID = "#00CC66"
SONAR_BRIGHT = "#AAFFCC"
SONAR_TEXT = "#D9FFE8"
SONAR_MUTED = "#6FE6A5"
GRID_LINE = "#003318"
SUCCESS = "#00FF88"
WARNING = "#FFCC44"
ERROR = "#FF4444"


def _qt_core_attr(name: str) -> Any:
    """Return a named PySide6.QtCore attribute."""

    return getattr(import_module("PySide6.QtCore"), name)


def _qt_gui_attr(name: str) -> Any:
    """Return a named PySide6.QtGui attribute."""

    return getattr(import_module("PySide6.QtGui"), name)


def _qt_widgets_attr(name: str) -> Any:
    """Return a named PySide6.QtWidgets attribute."""

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
