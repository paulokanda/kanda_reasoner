# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/launch.py
"""Launch entry point for the Reasoner tools GUI shell."""

from __future__ import annotations

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from kanda_reasoner_app.templates.press_depth_button_theme import (
    apply_color_preserving_press_depth_theme,
)

from .app_constants import APP_DISPLAY_NAME, APP_ICON_PATH
from .main_window import ReasonerToolsWindow

__all__: list[str] = []

_WINDOWS_APP_USER_MODEL_ID = "KANDA.Reasoner.Desktop"


def _set_windows_app_user_model_id() -> None:
    """Set the Windows taskbar identity before Qt creates application windows."""
    if sys.platform != "win32":
        return

    try:
        from ctypes import windll

        windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            _WINDOWS_APP_USER_MODEL_ID
        )
    except (AttributeError, OSError):
        # Qt still receives the shared application and window icon below.
        return


def _configure_application_identity(app: QApplication) -> None:
    """Apply the shared name and colorful brain icon to the Qt application."""
    app.setApplicationName(APP_DISPLAY_NAME)
    app.setApplicationDisplayName(APP_DISPLAY_NAME)
    if APP_ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(APP_ICON_PATH)))


def main() -> int:
    """Launch the KANDA Reasoner desktop application.

    Returns
    -------
    int
        The integer status code returned by the Qt event loop.
    """
    _set_windows_app_user_model_id()
    app = QApplication.instance() or QApplication(sys.argv)
    _configure_application_identity(app)
    apply_color_preserving_press_depth_theme(app)
    window = ReasonerToolsWindow()
    window.show()
    return app.exec()
