"""Classify the currently loaded Project Reasoner JSON file.

This helper belongs to the V10 GUI / Runtime Controller box. It only labels
which JSON track is loaded. It does not create, copy, refresh, or enrich JSON
files.
"""

from __future__ import annotations


__all__ = [
    "CANONICAL_COMPLETE_JSON_NAME",
    "LOCAL_AI_COMPLETE_JSON_NAME",
    "classify_loaded_json_track",
]

CANONICAL_COMPLETE_JSON_NAME = "developer_tools__complete.json"
LOCAL_AI_COMPLETE_JSON_NAME = "developer_tools__complete_local_AI.json"


def classify_loaded_json_track(file_path: str) -> str:
    """Return a short user-facing label for the loaded JSON path."""
    path_text = str(file_path or "").strip()
    if not path_text:
        return "Not loaded"

    normalized = path_text.replace("\\", "/")
    parts = [part for part in normalized.split("/") if part]
    name = parts[-1].lower() if parts else ""
    parent = parts[-2].lower() if len(parts) >= 2 else ""

    if name == CANONICAL_COMPLETE_JSON_NAME.lower() and parent == "json_complete":
        return "Canonical web-AI JSON"

    if name == LOCAL_AI_COMPLETE_JSON_NAME.lower() and parent == "json_complete":
        return "Local-AI working JSON"

    if name == CANONICAL_COMPLETE_JSON_NAME.lower():
        return "Canonical web-AI JSON candidate"

    if name == LOCAL_AI_COMPLETE_JSON_NAME.lower():
        return "Local-AI working JSON candidate"

    return "Other JSON"
