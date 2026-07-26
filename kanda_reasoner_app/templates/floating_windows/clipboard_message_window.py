# project-path: kanda_reasoner_app/templates/floating_windows/clipboard_message_window.py
"""Reusable clipboard message floating window template.

Use this template when a long diagnostic message should be preserved by the
user. The only action button is Copy. Pressing Copy writes the complete message
context to the clipboard and then closes the window.

This template is intentionally not wired into any caller by itself. Import and
use it explicitly from a feature-specific patch when a real workflow should use
copy-and-close behavior.

Sound policy:
This template avoids native message-box widgets, native alert icons, application beep calls, and
OK/Close button patterns that can produce operating-system alert sounds.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any, Callable

CopyErrorHandler = Callable[[Exception], None]
CopyCallback = Callable[[str], None]

__all__ = [
    "CopyMessageFloatingWindow",
    "show_copy_message_window",
]


def _qt_core_attr(name: str) -> Any:
    """Return a PySide6.QtCore attribute."""
    return getattr(import_module("PySide6.QtCore"), name)


def _qt_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWidgets attribute."""
    return getattr(import_module("PySide6.QtWidgets"), name)


_Qt = _qt_core_attr("Qt")
_QApplication = _qt_widgets_attr("QApplication")
_QDialog = _qt_widgets_attr("QDialog")
_QHBoxLayout = _qt_widgets_attr("QHBoxLayout")
_QLabel = _qt_widgets_attr("QLabel")
_QPlainTextEdit = _qt_widgets_attr("QPlainTextEdit")
_QPushButton = _qt_widgets_attr("QPushButton")
_QSpacerItem = _qt_widgets_attr("QSpacerItem")
_QSizePolicy = _qt_widgets_attr("QSizePolicy")
_QVBoxLayout = _qt_widgets_attr("QVBoxLayout")


def _qt_enum_value(group_name: str, name: str) -> Any:
    """Return a Qt enum value across PySide6 enum variants."""
    enum_group = getattr(_Qt, group_name, None)
    if enum_group is not None:
        return getattr(enum_group, name)
    return getattr(_Qt, name)


def _compose_clipboard_text(
    *,
    title: str,
    message: str,
    detail_text: str,
    clipboard_text: str | None,
    include_title: bool,
) -> str:
    """Return the complete text copied by the Copy button."""
    if clipboard_text is not None:
        return str(clipboard_text)

    sections: list[str] = []
    if include_title and title.strip():
        sections.append(title.strip())
    if message.strip():
        sections.append(message.strip())
    if detail_text.strip():
        sections.append(detail_text.strip())
    return "\n\n".join(sections).strip()


class CopyMessageFloatingWindow(_QDialog):
    """Floating diagnostic window with one Copy button.

    The Copy button copies the complete configured message text to the clipboard
    and closes the dialog. There is intentionally no OK or Close action button.
    """

    def __init__(
        self,
        parent: Any | None = None,
        *,
        title: str,
        message: str,
        detail_text: str = "",
        clipboard_text: str | None = None,
        include_title_in_clipboard: bool = True,
        button_text: str = "Copy",
        modal: bool = True,
        on_copied: CopyCallback | None = None,
        on_copy_error: CopyErrorHandler | None = None,
    ) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        parent : Any | None, optional
            The optional parent value.
        title : str
            The title value.
        message : str
            The message text.
        detail_text : str, optional
            The optional detail text value.
        clipboard_text : str | None, optional
            The optional clipboard text value.
        include_title_in_clipboard : bool, optional
            The optional include title in clipboard value.
        button_text : str, optional
            The optional button text value.
        modal : bool, optional
            The optional modal value.
        on_copied : CopyCallback | None, optional
            The optional on copied value.
        on_copy_error : CopyErrorHandler | None, optional
            The optional on copy error value.
        """
        
        super().__init__(parent)
        self._clipboard_text = _compose_clipboard_text(
            title=title,
            message=message,
            detail_text=detail_text,
            clipboard_text=clipboard_text,
            include_title=include_title_in_clipboard,
        )
        self._on_copied = on_copied
        self._on_copy_error = on_copy_error
        self._copy_already_attempted = False
        self._closing_from_copy = False

        self.setWindowTitle(title)
        self.setWindowFlag(_qt_enum_value("WindowType", "Tool"), True)
        self.setWindowFlag(_qt_enum_value("WindowType", "WindowContextHelpButtonHint"), False)
        self.setAttribute(_qt_enum_value("WidgetAttribute", "WA_DeleteOnClose"), True)
        self.setModal(bool(modal))
        self.setMinimumWidth(560)
        self.setMinimumHeight(320)

        self._build_ui(title=title, message=message, detail_text=detail_text, button_text=button_text)

    def _build_ui(self, *, title: str, message: str, detail_text: str, button_text: str) -> None:
        """Build the copyable diagnostic body and Copy action row."""
        layout = _QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 14)
        layout.setSpacing(10)

        title_label = _QLabel(title)
        title_label.setWordWrap(True)
        title_label.setTextInteractionFlags(_qt_enum_value("TextInteractionFlag", "TextSelectableByMouse"))
        title_label.setStyleSheet("font-weight: 600;")
        layout.addWidget(title_label)

        body = message
        if detail_text:
            body = body.rstrip() + "\n\n" + detail_text.lstrip()

        message_box = _QPlainTextEdit()
        message_box.setPlainText(body)
        message_box.setReadOnly(True)
        message_box.setLineWrapMode(_QPlainTextEdit.WidgetWidth)
        message_box.setMinimumHeight(210)
        layout.addWidget(message_box)

        button_row = _QHBoxLayout()
        button_row.addItem(_QSpacerItem(10, 10, _QSizePolicy.Expanding, _QSizePolicy.Minimum))
        copy_button = _QPushButton(button_text or "Copy")
        copy_button.setAutoDefault(False)
        copy_button.setDefault(False)
        copy_button.clicked.connect(self.copy_message_and_close)
        button_row.addWidget(copy_button)
        layout.addLayout(button_row)

    def accept(self) -> None:
        """Copy and close when external code uses the accept path."""
        self.copy_message_and_close()

    def copy_message_and_close(self) -> None:
        """Copy the complete configured message to the clipboard and close."""
        if self._copy_already_attempted:
            self.close()
            return
        self._copy_already_attempted = True
        try:
            clipboard = _QApplication.clipboard()
            clipboard.setText(self._clipboard_text)
            if self._on_copied is not None:
                self._on_copied(self._clipboard_text)
        except Exception as exc:
            if self._on_copy_error is not None:
                self._on_copy_error(exc)
            else:
                print("Clipboard message floating window copy failed: " + str(exc))
        self._closing_from_copy = True
        self.close()


def show_copy_message_window(
    parent: Any | None,
    *,
    title: str,
    message: str,
    detail_text: str = "",
    clipboard_text: str | None = None,
    include_title_in_clipboard: bool = True,
    button_text: str = "Copy",
    modal: bool = True,
    on_copied: CopyCallback | None = None,
    on_copy_error: CopyErrorHandler | None = None,
) -> CopyMessageFloatingWindow:
    """Create, show, and return a copy-and-close message window.

    The returned dialog is not inserted into any workflow by this template. The
    caller owns the decision to keep a reference when parent ownership is not
    enough for its lifetime.
    """
    dialog = CopyMessageFloatingWindow(
        parent,
        title=title,
        message=message,
        detail_text=detail_text,
        clipboard_text=clipboard_text,
        include_title_in_clipboard=include_title_in_clipboard,
        button_text=button_text,
        modal=modal,
        on_copied=on_copied,
        on_copy_error=on_copy_error,
    )
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()
    return dialog
