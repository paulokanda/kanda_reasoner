"""Expose Main Workbench refactoring artifact paths in Plan Actions."""
from __future__ import annotations

from typing import Iterator

from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QApplication, QLayout, QPushButton, QWidget

from .main_workbench_gui import (
    build_main_workbench_controls as _build_main_workbench_controls,
)

__all__ = ["build_main_workbench_controls"]

_CANCEL_TEXT = "Cancel Main Workbench"
_FOLDER_TEXT = "Refactoring Folder"
_SEND_TEXT = "Send Complete Project to Web AI"
_COPY_BUTTON_ATTRIBUTE = (
    "_large_file_refactor_main_workbench_refactoring_folder_button"
)
_MIRROR_ATTRIBUTE = (
    "_large_file_refactor_main_workbench_refactoring_folder_enabled_mirror"
)
_PACKAGE_RESULT_ATTRIBUTE = (
    "_large_file_refactor_main_workbench_package_result"
)
_OUTPUT_ATTRIBUTE = "_large_file_refactor_main_workbench_output"
_INSTALL_ERROR_ATTRIBUTE = (
    "_large_file_refactor_main_workbench_refactoring_folder_install_error"
)


class _EnabledStateMirror(QObject):
    """Mirror the Main Workbench send-state onto the path-copy button."""

    def __init__(self, source: QPushButton, target: QPushButton) -> None:
        super().__init__(source)
        self._source = source
        self._target = target

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Update the duplicate after the source receives an enabled-state event."""
        if watched is self._source and event.type() == QEvent.EnabledChange:
            self._target.setEnabled(self._source.isEnabled())
        return False


def build_main_workbench_controls(window: object) -> QWidget:
    """Build normal controls and insert one Main Workbench path-copy button."""
    root = _build_main_workbench_controls(window)
    try:
        _install_refactoring_folder_button(window, root)
    except RuntimeError as error:
        setattr(window, _INSTALL_ERROR_ATTRIBUTE, str(error))
    return root


def _install_refactoring_folder_button(window: object, root: QWidget) -> None:
    """Insert the path-copy button before Send Complete Project to Web AI."""
    existing = getattr(window, _COPY_BUTTON_ATTRIBUTE, None)
    if isinstance(existing, QPushButton):
        return

    cancel_button = _unique_button(root, _CANCEL_TEXT)
    send_button = _unique_button(root, _SEND_TEXT)
    row, cancel_index, send_index = _shared_button_layout(
        root,
        cancel_button,
        send_button,
    )
    if cancel_index >= send_index:
        raise RuntimeError("MAIN_WORKBENCH_BUTTON_ORDER_INVALID")

    folder_button = QPushButton(_FOLDER_TEXT)
    folder_button.setObjectName(
        "large_file_refactor_main_workbench_refactoring_folder_button"
    )
    folder_button.setToolTip(
        "Copy the Main Workbench workspace folder path that contains the "
        "generated AI upload ZIP and current exchange folder."
    )
    folder_button.clicked.connect(
        lambda: _copy_main_workbench_artifact_paths(window)
    )
    folder_button.setEnabled(send_button.isEnabled())
    mirror = _EnabledStateMirror(send_button, folder_button)
    send_button.installEventFilter(mirror)
    setattr(window, _MIRROR_ATTRIBUTE, mirror)

    row.insertWidget(send_index, folder_button)
    setattr(window, _COPY_BUTTON_ATTRIBUTE, folder_button)
    setattr(window, _INSTALL_ERROR_ATTRIBUTE, "")


def _copy_main_workbench_artifact_paths(window: object) -> None:
    """Copy and display the workspace folder that contains AI upload files."""
    result = getattr(window, _PACKAGE_RESULT_ATTRIBUTE, None)
    if result is None:
        setattr(
            window,
            _INSTALL_ERROR_ATTRIBUTE,
            "MAIN_WORKBENCH_PACKAGE_RESULT_MISSING",
        )
        _set_output(
            window,
            "REFACTORING FOLDER NOT READY\n\n"
            "Click Send Complete Project to Web AI first. After the package is "
            "ready, this button copies the workspace folder path that contains "
            "the generated upload ZIP and current exchange folder.",
        )
        return

    try:
        workspace_path = _workspace_folder_path(result)
    except Exception as error:
        message = type(error).__name__ + ":" + str(error)
        setattr(window, _INSTALL_ERROR_ATTRIBUTE, message)
        _set_output(
            window,
            "REFACTORING FOLDER PATH COPY BLOCKED\n\n" + message,
        )
        return

    QApplication.clipboard().setText(workspace_path)
    _set_output(window, workspace_path)
    setattr(window, _INSTALL_ERROR_ATTRIBUTE, "")


def _workspace_folder_path(result: object) -> str:
    """Return the workspace folder that contains the generated AI upload ZIP."""
    workspace_path = str(
        getattr(result, "workspace_root", "") or ""
    ).strip()
    if not workspace_path:
        raise ValueError("MAIN_WORKBENCH_WORKSPACE_PATH_MISSING")
    return workspace_path


def _set_output(window: object, text: str) -> None:
    """Project path-copy status onto the existing Main Workbench output."""
    output = getattr(window, _OUTPUT_ATTRIBUTE, None)
    if output is not None:
        output.setPlainText(str(text))


def _unique_button(root: QWidget, text: str) -> QPushButton:
    """Return exactly one descendant button with the requested visible text."""
    matches = [
        button
        for button in root.findChildren(QPushButton)
        if button.text().strip() == text
    ]
    if len(matches) != 1:
        raise RuntimeError(
            "MAIN_WORKBENCH_BUTTON_MATCH_INVALID:"
            + text
            + ":"
            + str(len(matches))
        )
    return matches[0]


def _shared_button_layout(
    root: QWidget,
    cancel_button: QPushButton,
    send_button: QPushButton,
) -> tuple[QLayout, int, int]:
    """Find the single nested layout that directly owns both anchor buttons."""
    matches: list[tuple[QLayout, int, int]] = []
    for layout in _walk_layouts(root.layout()):
        cancel_index = layout.indexOf(cancel_button)
        send_index = layout.indexOf(send_button)
        if cancel_index >= 0 and send_index >= 0:
            matches.append((layout, cancel_index, send_index))
    if len(matches) != 1:
        raise RuntimeError(
            "MAIN_WORKBENCH_SHARED_LAYOUT_INVALID:" + str(len(matches))
        )
    layout, cancel_index, send_index = matches[0]
    if not hasattr(layout, "insertWidget"):
        raise RuntimeError("MAIN_WORKBENCH_LAYOUT_INSERT_UNSUPPORTED")
    return layout, cancel_index, send_index


def _walk_layouts(layout: QLayout | None) -> Iterator[QLayout]:
    """Yield a layout and all nested child layouts without changing ownership."""
    if layout is None:
        return
    yield layout
    for index in range(layout.count()):
        child_layout = layout.itemAt(index).layout()
        if child_layout is not None:
            yield from _walk_layouts(child_layout)
