# project-path: kanda_reasoner_app/freeze_after_update_gui/_local_freeze_preview_presentation.py
"""Truthful rendering for writable and blocked local Freeze previews."""

from __future__ import annotations

from typing import Any, Mapping

from kanda_reasoner_app.freeze_after_update_gui.local_freeze_confirmation_binding import (
    render_freeze_findings,
)

__all__ = ["render_local_freeze_preview"]


def _not_ready_text(*results: Mapping[str, Any]) -> str:
    findings = "".join(render_freeze_findings(result) for result in results if result)
    guidance = (
        "FREEZE PREVIEW NOT READY\n\n"
        "This draft is not writable and is intentionally not rendered as a frozen "
        "entry. Correct the form, then run Preview Freeze Entry again.\n\n"
        "Validation evidence must contain the literal current-feature markers:\n"
        "VALIDATION OK: <feature_id>\n"
        "STATUS: IN_SYNC\n"
    )
    return findings + guidance


def render_local_freeze_preview(
    preview: Mapping[str, Any],
    validation: Mapping[str, Any] | None = None,
) -> str:
    """Render frozen-style Markdown only for a writable validated Preview."""
    preview_data = dict(preview or {})
    validation_data = dict(validation or {})
    preview_ready = bool(preview_data.get("ok") and preview_data.get("is_writable"))
    validation_ready = not validation_data or bool(validation_data.get("ok"))
    if preview_ready and validation_ready:
        return render_freeze_findings(preview_data) + str(
            preview_data.get("markdown") or ""
        )
    return _not_ready_text(preview_data, validation_data)
