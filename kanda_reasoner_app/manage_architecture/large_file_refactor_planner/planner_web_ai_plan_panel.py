# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_plan_panel.py
"""Read-only Proposed Split Plan output with governed Web AI paste intake."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QApplication, QPlainTextEdit

__all__ = ["PlannerWebAIPlanOutput"]


class PlannerWebAIPlanOutput(QPlainTextEdit):
    """Display plan text while accepting explicit Web AI response paste intake."""

    def __init__(
        self,
        *,
        paste_callback: Callable[[str], None],
        load_installed_callback: Callable[[], None],
    ) -> None:
        super().__init__()
        self._paste_callback = paste_callback
        self._load_installed_callback = load_installed_callback
        self.setReadOnly(True)
        self.setAcceptDrops(True)
        self.setToolTip(
            "ZIP path: install the Web AI package, then select Imported Web AI "
            "Version or use Load Installed Web AI Version from this panel menu. "
            "Paste path: focus this panel and press Ctrl+V with the complete "
            "marker-wrapped planning response."
        )

    def keyPressEvent(self, event: object) -> None:
        """Route Ctrl+V to governed pasted-response intake without editing text."""

        if hasattr(event, "matches") and event.matches(
            QKeySequence.StandardKey.Paste
        ):
            self._paste_clipboard_response()
            if hasattr(event, "accept"):
                event.accept()
            return
        super().keyPressEvent(event)

    def contextMenuEvent(self, event: object) -> None:
        """Expose installed ZIP loading and paste intake from the panel itself."""

        menu = self.createStandardContextMenu()
        menu.addSeparator()
        load_action = menu.addAction("Load Installed Web AI Version")
        paste_action = menu.addAction("Paste Web AI Planning Response")
        load_action.triggered.connect(self._load_installed_callback)
        paste_action.triggered.connect(self._paste_clipboard_response)
        if hasattr(event, "globalPos"):
            menu.exec(event.globalPos())
        else:
            menu.exec()

    def dragEnterEvent(self, event: object) -> None:
        """Allow text drops as another direct panel intake gesture."""

        mime_data = event.mimeData() if hasattr(event, "mimeData") else None
        if mime_data is not None and mime_data.hasText():
            event.acceptProposedAction()
            return
        super().dragEnterEvent(event)

    def dropEvent(self, event: object) -> None:
        """Route dropped text to the same governed paste callback."""

        mime_data = event.mimeData() if hasattr(event, "mimeData") else None
        if mime_data is not None and mime_data.hasText():
            self._paste_callback(mime_data.text())
            event.acceptProposedAction()
            return
        super().dropEvent(event)

    def _paste_clipboard_response(self) -> None:
        """Read clipboard text and send it to the governed intake callback."""

        self._paste_callback(QApplication.clipboard().text())
