# project-path: kanda_reasoner_app/tab3_manual_review_runtime/review_status_visibility.py
"""Draft-generation status helpers for Tab 3 review corrections."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime import inline_preview_runtime

__all__ = [
    "append_draft_generation_output",
    "draft_status_text_for_row",
    "apply_review_draft_status",
]


def apply_review_draft_status(owner: object, row: dict | None = None) -> None:
    """Refresh the visible draft-generation status label."""
    label = getattr(owner, "_review_draft_status_label", None)
    setter = getattr(label, "setText", None)
    if callable(setter):
        setter(draft_status_text_for_row(row))


def draft_status_text_for_row(row: dict | None) -> str:
    """Return the status shown below the selected draft controls."""
    if not row:
        return "NO REVIEW ROW SELECTED"
    if not inline_preview_runtime.is_reviewable_docstring_row(row):
        return "NOT A MISSING-DOCSTRING ROW"
    draft = str(row.get("draft_docstring") or "").strip()
    ai_draft = str(row.get("ai_draft_docstring") or "").strip()
    if not draft and not ai_draft:
        return "NO DRAFT GENERATED"
    source = str(row.get("selected_draft_source") or "").strip().lower()
    if source == "ai" and ai_draft:
        return "AI DRAFT GENERATED"
    if source == "heuristic_fallback" or bool(row.get("ai_used_fallback")):
        return "AI UNAVAILABLE - HEURISTIC FALLBACK"
    if source == "heuristic":
        return "HEURISTIC DRAFT GENERATED"
    if ai_draft:
        return "AI DRAFT GENERATED"
    return "DRAFT GENERATED"


def append_draft_generation_output(owner: object, row: dict, mode: str) -> None:
    """Append a clear generation status line to the Output panel."""
    status_text = draft_status_text_for_row(row)
    _append_output(owner, "[review] " + status_text + " for " + _row_identity(row) + "\n")
    if mode != "ai":
        return
    provider = str(row.get("ai_provider") or "").strip()
    ai_status = str(row.get("ai_status") or "").strip()
    ai_error = str(row.get("ai_error") or "").strip()
    if provider or ai_status:
        detail = "[review] AI provider"
        if provider:
            detail += ": " + provider
        if ai_status:
            detail += " | status: " + ai_status
        _append_output(owner, detail + "\n")
    if ai_error:
        _append_output(owner, "[review] AI error: " + ai_error + "\n")


def _append_output(owner: object, text: str) -> None:
    """Append text to the Tab 3 output if possible."""
    append_text = getattr(owner, "_append_text", None)
    if callable(append_text):
        append_text(text)


def _row_identity(row: dict) -> str:
    """Return a compact row identity for output messages."""
    return str(row.get("file", "")) + ":" + str(row.get("line") or row.get("insert_line") or "")
