# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/launch.py
"""Launch entry point for the Reasoner tools GUI shell."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from kanda_reasoner_app.templates.press_depth_button_theme import (
    apply_color_preserving_press_depth_theme,
)

from .main_window import ReasonerToolsWindow

__all__: list[str] = []


def main() -> int:
    """Support main behavior.

    Returns
    -------
    int
        The integer status code.
    """

    app = QApplication.instance() or QApplication(sys.argv)
    apply_color_preserving_press_depth_theme(app)
    window = ReasonerToolsWindow()
    window.show()
    return app.exec()
