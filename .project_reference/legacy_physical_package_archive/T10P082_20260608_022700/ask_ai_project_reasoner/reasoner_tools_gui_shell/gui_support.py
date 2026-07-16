"""Internal support functions for embedded GUI tabs and help catalogs."""

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

from kanda_reasoner_app import LEGACY_PACKAGE_NAME

from .app_constants import _PROJECT_ROOT

__all__: list[str] = []

def _first_existing_attr(module: object, names: Iterable[str]):
    for name in names:
        if hasattr(module, name):
            return getattr(module, name)
    raise AttributeError(f"None of the expected classes were found: {', '.join(names)}")


def _first_imported_module(module_names: Iterable[str]):
    errors: list[str] = []
    for module_name in module_names:
        try:
            return importlib.import_module(module_name)
        except Exception as exc:
            errors.append(f"{module_name}: {exc}")
    raise ImportError("Could not import any module candidate.\n" + "\n".join(errors))


def _prepare_embedded_widget(widget: QWidget) -> QWidget:
    widget.setParent(None)
    widget.setWindowFlags(Qt.Widget)
    widget.setAttribute(Qt.WA_DeleteOnClose, False)
    widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return widget


def _safe_disconnect(signal) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        with contextlib.suppress(Exception):
            signal.disconnect()


def _replace_exact_label_text(root: QWidget, old_text: str, new_text: str) -> None:
    for label in root.findChildren(QLabel):
        if label.text().strip() == old_text:
            label.setText(new_text)


def _find_button_by_text(root: QWidget, text: str) -> QPushButton | None:
    for button in root.findChildren(QPushButton):
        if button.text().strip() == text:
            return button
    return None


def _normalized_tab_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _prune_named_subtabs(root: QWidget, names_to_remove: set[str]) -> None:
    for tabs in root.findChildren(QTabWidget):
        remove_indexes: list[int] = []
        for index in range(tabs.count()):
            tab_text = _normalized_tab_text(tabs.tabText(index))
            if tab_text in names_to_remove:
                remove_indexes.append(index)

        for index in reversed(remove_indexes):
            page = tabs.widget(index)
            tabs.removeTab(index)
            if page is not None:
                page.setParent(None)
                page.deleteLater()


def _architecture_worker_script_path() -> Path:
    return (
        _PROJECT_ROOT
        / LEGACY_PACKAGE_NAME
        / "manage_architecture"
        / "manage_architecture.py"
    )


def _docstring_worker_script_path() -> Path:
    return (
        _PROJECT_ROOT
        / LEGACY_PACKAGE_NAME
        / "insert_missing_docstrings_gui"
        / "insert_missing_docstrings.py"
    )


def _help_catalog_path(filename: str) -> Path:
    return (
        _PROJECT_ROOT
        / LEGACY_PACKAGE_NAME
        / "reasoner_tools_gui_help"
        / filename
    )


def _format_help_catalog_text(path: Path) -> str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"Failed to read help catalog:\n{path}\n\nDetails: {exc}"

    lines: list[str] = []
    tab = payload.get("tab")
    purpose = payload.get("purpose")
    if tab:
        lines.append(str(tab))
        lines.append("=" * len(str(tab)))
        lines.append("")
    if purpose:
        lines.append(str(purpose))
        lines.append("")

    errors = payload.get("errors", [])
    if isinstance(errors, list):
        for item in errors:
            if not isinstance(item, dict):
                continue
            number = item.get("number", "")
            name = item.get("error", "Unnamed error")
            lines.append(f"{number}. {name}")
            explanation = item.get("plain_explanation")
            if explanation:
                lines.append(f"What it is: {explanation}")
            consequence = item.get("if_not_corrected")
            if consequence:
                lines.append(f"If not corrected: {consequence}")
            example = item.get("easy_example")
            if example:
                lines.append(f"Easy example: {example}")
            status = item.get("code_status")
            if status:
                lines.append(f"Code status: {status}")
            gate = item.get("planned_detector_gate")
            if gate:
                lines.append(f"Planned detector: {gate}")
            lines.append("")

    if not lines:
        return json.dumps(payload, indent=2, ensure_ascii=True)
    return "\n".join(lines)
