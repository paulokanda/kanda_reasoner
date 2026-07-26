"""Qt presentation for the Workbench Page Code snapshot."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QPlainTextEdit, QPushButton, QVBoxLayout

from .workbench_page_code_snapshot import build_workbench_page_code_text


__all__ = [
    "build_workbench_page_code_button",
    "open_workbench_page_code_dialog",
]


def build_workbench_page_code_button(window: object) -> QPushButton:
    """Create the top-level button that opens the current Page Code snapshot."""
    button = QPushButton("Get Page Code")
    button.setToolTip(
        "Open a read-only snapshot of every Workbench text window, grouped by stage with data-origin explanations."
    )
    button.clicked.connect(lambda: open_workbench_page_code_dialog(window))
    window._large_file_refactor_workbench_page_code_button = button
    return button


def open_workbench_page_code_dialog(window: object) -> None:
    """Open a modal read-only text window for the current Workbench Page Code."""
    dialog = QDialog(window)
    dialog.setWindowTitle("Large File Refactor Workbench - Page Code")
    dialog.resize(1100, 760)

    layout = QVBoxLayout(dialog)
    output = QPlainTextEdit()
    output.setReadOnly(True)
    output.setPlainText(build_workbench_page_code_text(window))
    layout.addWidget(output, 1)

    close_button = QPushButton("Close")
    close_button.clicked.connect(dialog.accept)
    layout.addWidget(close_button)

    window._large_file_refactor_workbench_page_code_dialog = dialog
    window._large_file_refactor_workbench_page_code_output = output
    dialog.exec()
