# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Export manual docstring review state summaries.
# EXPORTS       : _export_manual_review_summary
# DEPENDS ON    : manual_docstring_review_support.py
# REFACTOR DATE : 2026-06-01
# ------------------------------------------------------
"""Export manual docstring review summaries."""

from __future__ import annotations

import json
from pathlib import Path

from .review_support import _manual_review_state_summary_text



def _export_manual_review_summary(owner: object, locations: list[dict]) -> Path:
    """Write a JSON summary of current manual review locations."""
    root = _project_root_for_export(owner)
    export_dir = root / ".project_reference" / "manual_docstring_review_exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    path = export_dir / "manual_docstring_review_summary.json"
    payload = {
        "summary": _manual_review_state_summary_text(locations),
        "locations": [_export_location(location) for location in locations or []],
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
        newline="\n",
    )
    return path


def _export_location(location: dict) -> dict:
    """Return a stable serializable location summary."""
    return {
        "approval_state": str(location.get("approval_state", "")),
        "classification": str(location.get("classification", "")),
        "draft_docstring": str(location.get("draft_docstring", "")),
        "file": str(location.get("file", "")),
        "line": int(location.get("line", 0) or 0),
        "source": str(location.get("source", "")),
        "target_kind": str(location.get("target_kind", "")),
        "target_name": str(location.get("target_name", "")),
    }


def _project_root_for_export(owner: object) -> Path:
    """Return project root for export output."""
    edit = getattr(owner, "project_root_edit", None)
    text = ""
    if edit is not None:
        try:
            text = edit.text().strip()
        except Exception:
            text = ""
    return Path(text).resolve() if text else Path.cwd()
