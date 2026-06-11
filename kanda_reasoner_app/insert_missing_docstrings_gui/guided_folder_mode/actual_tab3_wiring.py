"""Compatibility hooks for Tab 3 safe-mode wiring."""

from __future__ import annotations

__all__ = [
    "install_safe_mode_actual_tab3_wiring",
    "move_safe_mode_radio_to_layout",
]


def install_safe_mode_actual_tab3_wiring(window: object) -> dict[str, object]:
    """Install optional Tab 3 wiring without failing tab load."""
    move_method = getattr(window, "move_safe_mode_radio_to_layout", None)
    return {
        "installed": True,
        "move_method_available": callable(move_method),
    }


def move_safe_mode_radio_to_layout(
    window: object,
    destination_layout: object,
    insert_index: int | None = None,
) -> None:
    """Move the existing Tab 3 source radio into a destination layout if possible."""
    radio = getattr(window, "_tab1_audit_docstring_radio", None)
    if radio is None or destination_layout is None:
        return

    insert_widget = getattr(destination_layout, "insertWidget", None)
    add_widget = getattr(destination_layout, "addWidget", None)
    if insert_index is not None and callable(insert_widget):
        insert_widget(insert_index, radio)
        return
    if callable(add_widget):
        add_widget(radio)
