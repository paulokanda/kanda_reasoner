"""Desktop renderer for local help documents."""

from __future__ import annotations

from importlib import import_module

from .path_resolver import HelpPage, find_page_by_legacy_catalog

__all__ = [
    "open_help_document_for_legacy_catalog",
]


def _qt_core_attr(name: str):
    return getattr(import_module("PySide6.QtCore"), name)


def _qt_widgets_attr(name: str):
    return getattr(import_module("PySide6.QtWidgets"), name)


def _qt_web_engine_widgets_attr(name: str):
    return getattr(import_module("PySide6.QtWebEngineWidgets"), name)


def _create_web_engine_dialog(parent, page: HelpPage, window_title: str):
    QMainWindow = _qt_widgets_attr("QMainWindow")
    QUrl = _qt_core_attr("QUrl")
    QWebEngineView = _qt_web_engine_widgets_attr("QWebEngineView")

    dialog = QMainWindow(parent)
    dialog.setWindowTitle(window_title)
    dialog.resize(1080, 800)

    view = QWebEngineView(dialog)
    view.setUrl(QUrl.fromLocalFile(str(page.rendered_path)))
    dialog.setCentralWidget(view)
    dialog.show()
    return dialog


def _create_text_browser_dialog(parent, page: HelpPage, window_title: str):
    QMainWindow = _qt_widgets_attr("QMainWindow")
    QTextBrowser = _qt_widgets_attr("QTextBrowser")
    QUrl = _qt_core_attr("QUrl")

    dialog = QMainWindow(parent)
    dialog.setWindowTitle(window_title)
    dialog.resize(1080, 800)

    browser = QTextBrowser(dialog)
    browser.setReadOnly(True)
    browser.setOpenExternalLinks(False)
    browser.setSource(QUrl.fromLocalFile(str(page.rendered_path)))
    dialog.setCentralWidget(browser)
    dialog.show()
    return dialog


def open_help_document_for_legacy_catalog(parent, legacy_help_catalog: str, *, window_title: str = ""):
    """Open a rich local help page for a legacy JSON help catalog.

    Returns ``None`` when no rich page is registered, so callers can preserve
    older plain-text help behavior.
    """

    page = find_page_by_legacy_catalog(legacy_help_catalog)
    if page is None:
        return None
    if not page.rendered_path.is_file() or not page.css_path.is_file():
        return None
    title = window_title or f"Help - {page.title}"
    try:
        return _create_web_engine_dialog(parent, page, title)
    except Exception:
        return _create_text_browser_dialog(parent, page, title)
