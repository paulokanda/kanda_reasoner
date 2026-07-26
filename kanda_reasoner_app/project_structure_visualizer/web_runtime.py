# project-path: kanda_reasoner_app/project_structure_visualizer/web_runtime.py
"""Transient local-document and WebEngine settings support."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from .web_assets import build_visualizer_html

__all__ = [
    "LocalVisualizerDocuments",
    "configure_web_settings",
]


class LocalVisualizerDocuments:
    """Own temporary embedded and browser-only HTML documents."""

    def __init__(self) -> None:
        self._embedded_dir = tempfile.TemporaryDirectory(
            prefix="kanda_project_structure_3d_embedded_"
        )
        self._browser_dir: tempfile.TemporaryDirectory[str] | None = None
        self._closed = False

    @property
    def embedded_root(self) -> Path:
        """Return the exact temporary root allowed by the embedded page."""
        return Path(self._embedded_dir.name).resolve()

    def write_embedded(
        self,
        graph_json: str,
        generation_id: str,
    ) -> Any:
        """Write and return one cache-busted local embedded-document URL."""
        self._require_open()
        path = self.embedded_root / "index.html"
        document = build_visualizer_html(
            graph_json,
            generation_id,
            embedded=True,
        )
        path.write_text(
            document,
            encoding="utf-8",
            errors="strict",
            newline="\n",
        )
        from PySide6.QtCore import QUrl

        url = QUrl.fromLocalFile(str(path))
        url.setQuery("generation=" + str(generation_id))
        return url

    def open_browser(self, graph_json: str, generation_id: str) -> Path:
        """Write and open one standalone local browser preview."""
        self._require_open()
        if self._browser_dir is None:
            self._browser_dir = tempfile.TemporaryDirectory(
                prefix="kanda_project_structure_3d_browser_"
            )
        path = Path(self._browser_dir.name).resolve() / "preview.html"
        document = build_visualizer_html(
            graph_json,
            generation_id,
            embedded=False,
        )
        path.write_text(
            document,
            encoding="utf-8",
            errors="strict",
            newline="\n",
        )
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        if not QDesktopServices.openUrl(QUrl.fromLocalFile(str(path))):
            raise RuntimeError("the operating system rejected the local URL")
        return path

    def close(self) -> None:
        """Release temporary document roots exactly once."""
        if self._closed:
            return
        self._closed = True
        if self._browser_dir is not None:
            self._browser_dir.cleanup()
            self._browser_dir = None
        self._embedded_dir.cleanup()

    def _require_open(self) -> None:
        """Reject document creation after page teardown."""
        if self._closed:
            raise RuntimeError("visualizer document store is closed")


def configure_web_settings(settings: Any, settings_type: Any) -> None:
    """Apply local-only settings required by the pinned WebGL renderer."""
    values = (
        ("JavascriptCanOpenWindows", False),
        ("LocalContentCanAccessRemoteUrls", False),
        ("WebGLEnabled", True),
        ("Accelerated2dCanvasEnabled", True),
    )
    attributes = settings_type.WebAttribute
    for name, enabled in values:
        attribute = getattr(attributes, name, None)
        if attribute is not None:
            settings.setAttribute(attribute, enabled)
