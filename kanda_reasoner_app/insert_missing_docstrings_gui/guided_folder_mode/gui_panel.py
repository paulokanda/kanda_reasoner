
"""Visual Safe Mode panel helpers.

The module is safe to import without PySide installed. PySide is imported only
inside create_safe_mode_panel_widget, so tests and non-GUI workflows can use
the panel model without opening a GUI window.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from .gui_bridge import (
    SAFE_MODE_ACTION_ACCEPT,
    SAFE_MODE_ACTION_CLEAR,
    SAFE_MODE_ACTION_EDIT,
    SAFE_MODE_ACTION_FALLBACK,
    SAFE_MODE_ACTION_REGENERATE,
    SAFE_MODE_ACTION_REJECT,
    SAFE_MODE_ACTION_SKIP,
    SafeModeButtonState,
    SafeModeGuiSnapshot,
)


SAFE_MODE_PANEL_ACTIONS = (
    SAFE_MODE_ACTION_ACCEPT,
    SAFE_MODE_ACTION_EDIT,
    SAFE_MODE_ACTION_REGENERATE,
    SAFE_MODE_ACTION_FALLBACK,
    SAFE_MODE_ACTION_SKIP,
    SAFE_MODE_ACTION_REJECT,
    SAFE_MODE_ACTION_CLEAR,
    "apply_folder",
    "next_folder",
)


@dataclass(frozen=True)
class SafeModePanelModel:
    """Represent GUI text and button state for the Safe Mode visual panel."""

    title: str
    folder_label: str
    progress_label: str
    pending_label: str
    review_label: str
    status_message: str
    button_enabled: dict[str, bool]
    button_text: dict[str, str]


@dataclass(frozen=True)
class SafeModePanelCallbacks:
    """Store optional callbacks for visual Safe Mode panel buttons."""

    on_accept: Callable[[], None] | None = None
    on_edit: Callable[[], None] | None = None
    on_regenerate: Callable[[], None] | None = None
    on_fallback: Callable[[], None] | None = None
    on_skip: Callable[[], None] | None = None
    on_reject: Callable[[], None] | None = None
    on_clear: Callable[[], None] | None = None
    on_apply_folder: Callable[[], None] | None = None
    on_next_folder: Callable[[], None] | None = None


def build_safe_mode_panel_model(
    snapshot: SafeModeGuiSnapshot,
    buttons: SafeModeButtonState,
) -> SafeModePanelModel:
    """Build a widget-ready Safe Mode panel model."""
    total = snapshot.total_folders
    current_display = snapshot.current_index + 1 if total else 0

    folder_label = snapshot.folder_relative_path or "No active folder"
    progress_label = f"Folder {current_display} of {total}"
    pending_label = f"Pending rows: {snapshot.pending_count}"
    review_label = (
        f"Accepted: {snapshot.accepted_count} | "
        f"Skipped: {snapshot.skipped_count} | "
        f"Rejected: {snapshot.rejected_count}"
    )

    button_enabled = {
        SAFE_MODE_ACTION_ACCEPT: buttons.can_edit,
        SAFE_MODE_ACTION_EDIT: buttons.can_edit,
        SAFE_MODE_ACTION_REGENERATE: buttons.can_regenerate,
        SAFE_MODE_ACTION_FALLBACK: buttons.can_fallback,
        SAFE_MODE_ACTION_SKIP: buttons.can_edit,
        SAFE_MODE_ACTION_REJECT: buttons.can_edit,
        SAFE_MODE_ACTION_CLEAR: buttons.can_edit,
        "apply_folder": buttons.can_apply_folder,
        "next_folder": buttons.can_continue_to_next_folder,
    }

    button_text = {
        SAFE_MODE_ACTION_ACCEPT: "Accept",
        SAFE_MODE_ACTION_EDIT: "Edit",
        SAFE_MODE_ACTION_REGENERATE: "Regenerate",
        SAFE_MODE_ACTION_FALLBACK: "Fallback",
        SAFE_MODE_ACTION_SKIP: "Skip",
        SAFE_MODE_ACTION_REJECT: "Reject",
        SAFE_MODE_ACTION_CLEAR: "Clear",
        "apply_folder": "Apply folder",
        "next_folder": "Next folder",
    }

    return SafeModePanelModel(
        title="Safe Mode",
        folder_label=folder_label,
        progress_label=progress_label,
        pending_label=pending_label,
        review_label=review_label,
        status_message=snapshot.status_message or buttons.message,
        button_enabled=button_enabled,
        button_text=button_text,
    )


def create_safe_mode_panel_widget(
    parent: object | None = None,
    callbacks: SafeModePanelCallbacks | None = None,
) -> object:
    """Create a PySide Safe Mode panel widget.

    PySide is imported inside this function to avoid import-time GUI coupling.
    The returned widget stores child references in a private Python attribute
    named _safe_mode_panel_parts for later updates.
    """
    try:
        from PySide6.QtWidgets import (  # type: ignore
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QVBoxLayout,
            QWidget,
        )
    except Exception as exc:
        raise RuntimeError(
            "PySide6 is required to create the Safe Mode panel widget."
        ) from exc

    container = QGroupBox("Safe Mode", parent)
    outer_layout = QVBoxLayout(container)

    folder_label = QLabel("No active folder")
    progress_label = QLabel("Folder 0 of 0")
    pending_label = QLabel("Pending rows: 0")
    review_label = QLabel("Accepted: 0 | Skipped: 0 | Rejected: 0")
    status_label = QLabel("Safe Mode has no active folder.")

    outer_layout.addWidget(folder_label)
    outer_layout.addWidget(progress_label)
    outer_layout.addWidget(pending_label)
    outer_layout.addWidget(review_label)
    outer_layout.addWidget(status_label)

    button_row = QWidget(container)
    button_layout = QHBoxLayout(button_row)
    buttons: dict[str, object] = {}

    for action in SAFE_MODE_PANEL_ACTIONS:
        button = QPushButton(_default_button_text(action), button_row)
        button.setEnabled(False)
        button_layout.addWidget(button)
        buttons[action] = button

    outer_layout.addWidget(button_row)

    panel_parts = {
        "folder_label": folder_label,
        "progress_label": progress_label,
        "pending_label": pending_label,
        "review_label": review_label,
        "status_label": status_label,
        "buttons": buttons,
    }
    setattr(container, "_safe_mode_panel_parts", panel_parts)

    if callbacks is not None:
        connect_safe_mode_panel_callbacks(container, callbacks)

    return container


def apply_safe_mode_panel_model(panel: object, model: SafeModePanelModel) -> None:
    """Apply a Safe Mode panel model to a PySide panel created by this module."""
    parts = _panel_parts(panel)

    parts["folder_label"].setText(model.folder_label)
    parts["progress_label"].setText(model.progress_label)
    parts["pending_label"].setText(model.pending_label)
    parts["review_label"].setText(model.review_label)
    parts["status_label"].setText(model.status_message)

    buttons: Mapping[str, object] = parts["buttons"]
    for action, button in buttons.items():
        button.setText(model.button_text.get(action, _default_button_text(action)))
        button.setEnabled(bool(model.button_enabled.get(action, False)))


def connect_safe_mode_panel_callbacks(
    panel: object,
    callbacks: SafeModePanelCallbacks,
) -> None:
    """Connect Safe Mode panel buttons to optional callbacks."""
    parts = _panel_parts(panel)
    buttons: Mapping[str, object] = parts["buttons"]

    callback_map = {
        SAFE_MODE_ACTION_ACCEPT: callbacks.on_accept,
        SAFE_MODE_ACTION_EDIT: callbacks.on_edit,
        SAFE_MODE_ACTION_REGENERATE: callbacks.on_regenerate,
        SAFE_MODE_ACTION_FALLBACK: callbacks.on_fallback,
        SAFE_MODE_ACTION_SKIP: callbacks.on_skip,
        SAFE_MODE_ACTION_REJECT: callbacks.on_reject,
        SAFE_MODE_ACTION_CLEAR: callbacks.on_clear,
        "apply_folder": callbacks.on_apply_folder,
        "next_folder": callbacks.on_next_folder,
    }

    for action, callback in callback_map.items():
        if callback is None:
            continue
        button = buttons.get(action)
        if button is None:
            continue
        button.clicked.connect(callback)


def _panel_parts(panel: object) -> dict[str, object]:
    parts = getattr(panel, "_safe_mode_panel_parts", None)
    if not isinstance(parts, dict):
        raise ValueError("Panel was not created by create_safe_mode_panel_widget.")
    return parts


def _default_button_text(action: str) -> str:
    return {
        SAFE_MODE_ACTION_ACCEPT: "Accept",
        SAFE_MODE_ACTION_EDIT: "Edit",
        SAFE_MODE_ACTION_REGENERATE: "Regenerate",
        SAFE_MODE_ACTION_FALLBACK: "Fallback",
        SAFE_MODE_ACTION_SKIP: "Skip",
        SAFE_MODE_ACTION_REJECT: "Reject",
        SAFE_MODE_ACTION_CLEAR: "Clear",
        "apply_folder": "Apply folder",
        "next_folder": "Next folder",
    }.get(action, action.replace("_", " ").title())
