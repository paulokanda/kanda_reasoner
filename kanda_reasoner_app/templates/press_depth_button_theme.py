# project-path: kanda_reasoner_app/templates/press_depth_button_theme.py
"""Application-wide press-depth styling that preserves button colors.

The shared Style 12 owner controls only border depth, corner radius, padding,
and pressed displacement. Existing button background, text color, font, and
state-specific colors remain owned by the original button or Qt palette.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any, Final

__all__ = [
    "COLOR_PRESERVING_PRESS_DEPTH_STYLE",
    "apply_color_preserving_press_depth_theme",
    "SILVER_MATTE_PRESS_DEPTH_STYLE",
    "apply_silver_matte_press_depth_theme",
    "STEEL_BLUE_PRESS_DEPTH_STYLE",
    "apply_steel_blue_press_depth_theme",
]

_THEME_MARKER: Final[str] = "KANDA_COLOR_PRESERVING_PRESS_DEPTH_V2"
_FILTER_ATTRIBUTE: Final[str] = "_kanda_press_depth_button_theme_filter"
_PREDECESSOR_MARKERS: Final[tuple[str, ...]] = (
    "KANDA_SILVER_MATTE_PRESS_DEPTH_V1",
    "KANDA_STEEL_BLUE_PRESS_DEPTH_V1",
)

COLOR_PRESERVING_PRESS_DEPTH_STYLE: Final[str] = f"""
/* {_THEME_MARKER} */
QPushButton,
QToolButton {{
    border: 1px solid rgba(92, 97, 104, 165);
    border-top: 1px solid rgba(255, 255, 255, 215);
    border-left: 1px solid rgba(245, 246, 247, 190);
    border-right: 1px solid rgba(86, 91, 97, 175);
    border-bottom: 4px solid rgba(78, 83, 89, 195);
    border-radius: 5px;
    padding: 4px 10px 3px 10px;
    min-height: 18px;
}}
QPushButton:hover,
QToolButton:hover {{
    border-top-color: rgba(255, 255, 255, 235);
    border-left-color: rgba(252, 252, 252, 215);
    border-right-color: rgba(91, 96, 102, 185);
    border-bottom-color: rgba(84, 89, 95, 205);
}}
QPushButton:pressed,
QPushButton:checked,
QToolButton:pressed,
QToolButton:checked {{
    border-top-color: rgba(76, 81, 87, 180);
    border-left-color: rgba(84, 89, 95, 185);
    border-right-color: rgba(205, 208, 212, 190);
    border-bottom: 1px solid rgba(72, 77, 83, 205);
    padding-top: 7px;
    padding-bottom: 0;
}}
QPushButton:focus,
QToolButton:focus {{
    border-top-color: rgba(255, 255, 255, 245);
    border-left-color: rgba(255, 255, 255, 225);
}}
QPushButton:default {{
    border-left-width: 2px;
    border-right-width: 2px;
}}
QPushButton:disabled,
QToolButton:disabled {{
    border: 1px solid rgba(155, 159, 164, 135);
    border-bottom: 3px solid rgba(116, 121, 127, 150);
    padding: 4px 10px 3px 10px;
}}
""".strip()

# Compatibility aliases retained for both predecessor release APIs.
SILVER_MATTE_PRESS_DEPTH_STYLE: Final[str] = COLOR_PRESERVING_PRESS_DEPTH_STYLE
STEEL_BLUE_PRESS_DEPTH_STYLE: Final[str] = COLOR_PRESERVING_PRESS_DEPTH_STYLE


def _contains_managed_marker(style_sheet: str) -> bool:
    markers = (_THEME_MARKER,) + _PREDECESSOR_MARKERS
    return any(marker in style_sheet for marker in markers)


def _merge_button_style(original_style: str) -> str:
    """Append depth geometry without replacing original visual colors."""
    clean_style = original_style.strip()
    if _THEME_MARKER in clean_style:
        return clean_style
    if any(marker in clean_style for marker in _PREDECESSOR_MARKERS):
        clean_style = ""
    if not clean_style:
        return COLOR_PRESERVING_PRESS_DEPTH_STYLE
    if "{" not in clean_style:
        clean_style = (
            "QPushButton, QToolButton {\n"
            + clean_style
            + "\n}"
        )
    return clean_style + "\n\n" + COLOR_PRESERVING_PRESS_DEPTH_STYLE


def apply_color_preserving_press_depth_theme(app: Any) -> None:
    """Install Style 12 depth while retaining original button colors."""
    qt_core = import_module("PySide6.QtCore")
    qt_widgets = import_module("PySide6.QtWidgets")
    QEvent = qt_core.QEvent
    QObject = qt_core.QObject
    QPushButton = qt_widgets.QPushButton
    QToolButton = qt_widgets.QToolButton
    button_types = (QPushButton, QToolButton)
    watched_event_types = {
        QEvent.Type.Polish,
        QEvent.Type.Show,
        QEvent.Type.StyleChange,
        QEvent.Type.EnabledChange,
    }

    theme_filter = getattr(app, _FILTER_ATTRIBUTE, None)
    if theme_filter is None:

        class PressDepthButtonThemeFilter(QObject):
            """Merge depth rules after local style changes."""

            def __init__(self, application: Any) -> None:
                super().__init__(application)
                self._active_widget_ids: set[int] = set()

            def eventFilter(self, watched: Any, event: Any) -> bool:
                if isinstance(watched, button_types):
                    if event.type() in watched_event_types:
                        self.apply_to_button(watched)
                return False

            def apply_to_button(self, button: Any) -> None:
                current_style = button.styleSheet()
                merged_style = _merge_button_style(current_style)
                if current_style.strip() == merged_style.strip():
                    return
                widget_id = id(button)
                if widget_id in self._active_widget_ids:
                    return
                self._active_widget_ids.add(widget_id)
                try:
                    button.setStyleSheet(merged_style)
                finally:
                    self._active_widget_ids.discard(widget_id)

        theme_filter = PressDepthButtonThemeFilter(app)
        app.installEventFilter(theme_filter)
        setattr(app, _FILTER_ATTRIBUTE, theme_filter)

    current_app_style = app.styleSheet().strip()
    if not _contains_managed_marker(current_app_style):
        merged_app_style = (
            current_app_style + "\n\n" + COLOR_PRESERVING_PRESS_DEPTH_STYLE
            if current_app_style
            else COLOR_PRESERVING_PRESS_DEPTH_STYLE
        )
        app.setStyleSheet(merged_app_style)

    for widget in app.allWidgets():
        if isinstance(widget, button_types):
            theme_filter.apply_to_button(widget)


def apply_silver_matte_press_depth_theme(app: Any) -> None:
    """Compatibility wrapper for the silver-matte predecessor API."""
    apply_color_preserving_press_depth_theme(app)


def apply_steel_blue_press_depth_theme(app: Any) -> None:
    """Compatibility wrapper for the steel-blue predecessor API."""
    apply_color_preserving_press_depth_theme(app)
