# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/error_memory_header_ai.py
"""Header AI action helper for the Error Memory lazy tab."""

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget

from kanda_reasoner_app.error_memory_gui._ai_correction_action import (
    run_error_memory_ai_correction_from_header,
)

__all__ = [
    "run_error_memory_ai_review_first_check",
]


def run_error_memory_ai_review_first_check(lazy_tab: QWidget) -> None:
    """Run local AI correction from the Error Memory header action."""
    try:
        run_error_memory_ai_correction_from_header(lazy_tab)
    except Exception as exc:
        QMessageBox.warning(
            lazy_tab,
            "Error Memory AI correction",
            "Could not run Error Memory local AI correction:\n" + str(exc),
        )
