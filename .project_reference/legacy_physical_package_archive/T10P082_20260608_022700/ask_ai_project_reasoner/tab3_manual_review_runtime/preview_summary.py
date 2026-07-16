# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Build approved-only manual docstring review previews.
# EXPORTS       : _build_approved_review_preview
# DEPENDS ON    : none
# REFACTOR DATE : 2026-06-01
# ------------------------------------------------------
"""Build approved-only manual docstring review previews."""

from __future__ import annotations



def _build_approved_review_preview(locations: list[dict]) -> str:
    """Return a read-only preview of approved manual review locations."""
    approved = [
        location
        for location in locations or []
        if str(location.get("approval_state", "")).strip().lower() == "approved"
    ]
    if not approved:
        return "Approved-only preview: no approved locations."
    lines = ["Approved-only preview: " + str(len(approved)) + " location(s)."]
    for index, location in enumerate(approved, 1):
        lines.extend(_location_preview_lines(index, location))
    return "\n".join(lines)


def _location_preview_lines(index: int, location: dict) -> list[str]:
    """Return preview lines for one approved location."""
    draft = str(location.get("draft_docstring", "") or "").strip()
    if not draft:
        draft = "<empty draft>"
    return [
        "",
        "[" + str(index) + "] " + str(location.get("file", "")) + ":" + str(location.get("line", "")),
        "target: " + str(location.get("target_kind", "")) + " " + str(location.get("target_name", "")),
        "classification: " + str(location.get("classification", "")),
        "approval_state: " + str(location.get("approval_state", "")),
        "draft_docstring:",
        draft,
    ]
