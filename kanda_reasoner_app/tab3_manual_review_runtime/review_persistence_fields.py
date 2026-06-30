# project-path: kanda_reasoner_app/tab3_manual_review_runtime/review_persistence_fields.py
"""Persistence fields for Tab 3 review draft state."""

from __future__ import annotations

import json
from typing import Any

__all__ = [
    "PERSISTED_REVIEW_FIELD_NAMES",
    "apply_persisted_review_state",
    "build_persisted_review_state",
    "clear_persisted_draft_fields",
    "review_rows_jsonl",
]

PERSISTED_REVIEW_FIELD_NAMES = (
    "approval_state",
    "classification",
    "draft_docstring",
    "ai_draft_docstring",
    "ai_provider",
    "ai_status",
    "ai_error",
    "ai_used_fallback",
    "selected_draft_source",
    "ai_docstring_verbosity",
)

_TEXT_FIELDS = {
    "approval_state",
    "classification",
    "draft_docstring",
    "ai_draft_docstring",
    "ai_provider",
    "ai_status",
    "ai_error",
    "selected_draft_source",
    "ai_docstring_verbosity",
}

_DRAFT_FIELDS = (
    "draft_docstring",
    "ai_draft_docstring",
    "ai_provider",
    "ai_status",
    "ai_error",
    "ai_used_fallback",
    "selected_draft_source",
    "ai_docstring_verbosity",
)


def apply_persisted_review_state(location: dict, saved: dict) -> None:
    """Apply persisted review and AI draft fields to a report row."""
    for key in PERSISTED_REVIEW_FIELD_NAMES:
        if key not in saved:
            continue
        value = saved.get(key)
        if key in _TEXT_FIELDS:
            location[key] = str(value or "")
        elif key == "ai_used_fallback":
            location[key] = bool(value)
        else:
            location[key] = value
    location["manual_review_state"] = saved


def build_persisted_review_state(location: dict, draft_text: str) -> dict[str, Any]:
    """Build the sidecar payload for one report row."""
    payload: dict[str, Any] = {
        "approval_state": str(location.get("approval_state", "")),
        "classification": str(location.get("classification", "")),
        "draft_docstring": str(draft_text or ""),
        "file": str(location.get("file", "")),
        "line": _safe_int(location.get("line", 0)),
        "target_kind": str(location.get("target_kind", "")),
        "target_name": str(location.get("target_name", "")),
        "source": str(location.get("source", "")),
    }
    for key in (
        "ai_draft_docstring",
        "ai_provider",
        "ai_status",
        "ai_error",
        "selected_draft_source",
    "ai_docstring_verbosity",
    ):
        if key in location:
            payload[key] = str(location.get(key) or "")
    if "ai_used_fallback" in location:
        payload["ai_used_fallback"] = bool(location.get("ai_used_fallback"))
    return payload


def clear_persisted_draft_fields(location: dict) -> None:
    """Clear generated draft fields on a mutable report row."""
    for key in _DRAFT_FIELDS:
        if key in location:
            if key == "ai_used_fallback":
                location[key] = False
            else:
                location[key] = ""


def review_rows_jsonl(rows: list[dict] | tuple[dict, ...]) -> str:
    """Return report rows as UTF-8 friendly JSONL text."""
    return "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)


def _safe_int(value: object) -> int:
    """Return value as int, or zero if conversion fails."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
