"""Error panel widgets for failed embedded tool loads."""

from __future__ import annotations

import contextlib
import importlib
import json
import shutil
import sys
import traceback
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices, QFont, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QInputDialog,
    QGroupBox,
    QFileDialog,
)

__all__ = [
    "ToolLoadErrorPanel",
]

class ToolLoadErrorPanel(QWidget):
    def __init__(self, title: str, source_hint: str, error_text: str) -> None:
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
