"""Beginner-facing labels for Architecture Review mode actions."""

from __future__ import annotations

__all__ = ["action_label_for_mode", "bind_mode_action_button"]

_MODE_ACTION_LABELS = {
    "validate": "Validate Project",
    "diff": "Preview Changes",
    "scan": "Scan Project",
    "write": "Write Architecture Files",
}


def action_label_for_mode(mode: str) -> str:
    """Return the action-button label for one technical mode name."""
    normalized_mode = mode.strip().lower()
    return _MODE_ACTION_LABELS.get(normalized_mode, "Run Selected Action")


def bind_mode_action_button(mode_combo: object, run_button: object) -> None:
    """Keep the action button aligned with the selected technical mode."""

    def update_label(mode: str) -> None:
        run_button.setText(action_label_for_mode(mode))

    mode_combo.currentTextChanged.connect(update_label)
    update_label(mode_combo.currentText())
