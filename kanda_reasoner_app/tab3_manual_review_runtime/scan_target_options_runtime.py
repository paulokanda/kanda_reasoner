"""Scan target option label helpers for Tab 3."""

from __future__ import annotations

__all__ = ["configure_scan_target_checkboxes"]


def configure_scan_target_checkboxes(window: object) -> None:
    """Set user-facing labels and visibility for scan target checkboxes."""
    label_pairs = (
        ("_module_checkbox", "Module Header Docstring"),
        ("_class_checkbox", "Classes"),
        ("_function_checkbox", "Function/Method"),
        ("_file_address_checkbox", "# Path Module at top of file"),
    )
    for attribute_name, label in label_pairs:
        widget = getattr(window, attribute_name, None)
        _safe_widget_set_text(widget, label)
        _safe_widget_set_enabled(widget, True)
        _safe_widget_show(widget)


def _safe_widget_set_text(widget: object, text: str) -> None:
    """Set widget text when supported."""
    setter = getattr(widget, "setText", None)
    if callable(setter):
        setter(text)


def _safe_widget_set_enabled(widget: object, enabled: bool) -> None:
    """Set widget enabled state when supported."""
    setter = getattr(widget, "setEnabled", None)
    if callable(setter):
        setter(bool(enabled))


def _safe_widget_show(widget: object) -> None:
    """Show a widget when supported."""
    show = getattr(widget, "show", None)
    if callable(show):
        show()
