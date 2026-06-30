# project-path: kanda_reasoner_app/tab3_manual_review_runtime/review_engine_status_runtime.py
"""Correction-engine status helpers for Tab 3 review corrections."""

from __future__ import annotations

__all__ = [
    "local_ai_enabled_from_owner",
    "apply_correction_engine_status",
    "correction_mode_from_owner",
]


def apply_correction_engine_status(owner: object) -> None:
    """Refresh the read-only correction engine status label."""
    label = getattr(owner, "_review_engine_status_label", None)
    setter = getattr(label, "setText", None)
    if not callable(setter):
        return
    if local_ai_enabled_from_owner(owner):
        setter("CORRECTION WITH AI")
    else:
        setter("HEURISTIC CORRECTION")


def correction_mode_from_owner(owner: object) -> str:
    """Return ai or heuristics from the single Local AI checkbox source."""
    if local_ai_enabled_from_owner(owner):
        return "ai"
    return "heuristics"


def local_ai_enabled_from_owner(owner: object) -> bool:
    """Return whether the Local AI checkbox is enabled and checked."""
    checkbox = getattr(owner, "_ai_enabled_checkbox", None)
    is_enabled = getattr(checkbox, "isEnabled", None)
    is_checked = getattr(checkbox, "isChecked", None)
    if callable(is_enabled) and not is_enabled():
        return False
    if callable(is_checked):
        return bool(is_checked())
    return False
