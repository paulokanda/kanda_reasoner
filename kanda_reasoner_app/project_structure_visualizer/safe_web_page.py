# project-path: kanda_reasoner_app/project_structure_visualizer/safe_web_page.py
"""Fail-closed QWebEngine page for local visualizer content."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWebEngineCore import QWebEnginePage

__all__ = ["LocalVisualizerPage"]


class LocalVisualizerPage(QWebEnginePage):
    """Allow only declared local roots as main-frame targets."""

    navigation_blocked = Signal(str)
    console_message = Signal(str)

    def __init__(
        self,
        allowed_roots: Iterable[Path],
        parent: object | None = None,
    ) -> None:
        super().__init__(parent)
        roots = tuple(Path(value).resolve() for value in allowed_roots)
        if not roots:
            raise ValueError("at least one local visualizer root is required")
        self._allowed_roots = roots

    def acceptNavigationRequest(
        self,
        url: QUrl,
        navigation_type: QWebEnginePage.NavigationType,
        is_main_frame: bool,
    ) -> bool:
        """Reject external and unrelated local main-frame navigation."""
        del navigation_type
        if not is_main_frame:
            return True
        scheme = url.scheme().lower()
        if scheme in {"about", "data", "qrc"}:
            return True
        if scheme == "file":
            try:
                candidate = Path(url.toLocalFile()).resolve()
                if any(self._inside(candidate, root) for root in self._allowed_roots):
                    return True
            except (OSError, ValueError):
                pass
        self.navigation_blocked.emit(url.toString()[:1000])
        return False

    @staticmethod
    def _inside(candidate: Path, root: Path) -> bool:
        """Return whether one path belongs to an allowed local root."""
        try:
            candidate.relative_to(root)
        except ValueError:
            return False
        return True

    def createWindow(
        self,
        window_type: QWebEnginePage.WebWindowType,
    ) -> QWebEnginePage | None:
        """Reject popup windows."""
        del window_type
        return None

    def javaScriptConsoleMessage(
        self,
        level: QWebEnginePage.JavaScriptConsoleMessageLevel,
        message: str,
        line_number: int,
        source_id: str,
    ) -> None:
        """Expose bounded diagnostics without sensitive page content."""
        del level
        source_name = Path(source_id).name if source_id else "inline"
        self.console_message.emit(
            f"{source_name}:{int(line_number)}: {str(message)[:800]}"
        )
