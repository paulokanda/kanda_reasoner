"""Launch entry point for the Reasoner tools GUI shell."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from .main_window import ReasonerToolsWindow

__all__: list[str] = []


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    window = ReasonerToolsWindow()
    window.show()
    return app.exec()
