# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/error_panels.py
"""Error panel widgets for failed embedded tool loads."""

from __future__ import annotations


from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

__all__ = [
    "ToolLoadErrorPanel",
]

class ToolLoadErrorPanel(QWidget):
    """Represent tool load error panel."""
    
    def __init__(self, title: str, source_hint: str, error_text: str) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        title : str
            The title value.
        source_hint : str
            The source hint value.
        error_text : str
            The error text value.
        """
        
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        title_label = QLabel(title)
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        title_label.setFont(font)
        root.addWidget(title_label)

        hint = QLabel(f"Expected source: {source_hint}")
        hint.setTextInteractionFlags(Qt.TextSelectableByMouse)
        hint.setWordWrap(True)
        root.addWidget(hint)

        info = QLabel("The tool could not be embedded. Review the traceback below.")
        info.setWordWrap(True)
        root.addWidget(info)

        details = QTextEdit()
        details.setReadOnly(True)
        details.setPlainText(error_text)
        root.addWidget(details, 1)
