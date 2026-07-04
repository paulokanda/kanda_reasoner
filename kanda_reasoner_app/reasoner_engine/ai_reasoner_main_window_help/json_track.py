# project-path: kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/json_track.py
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

CANONICAL_COMPLETE_JSON_NAME = "<project_slug>__complete.json"
LOCAL_AI_COMPLETE_JSON_NAME = "<project_slug>__complete_local_AI.json"
KNOWN_COMPLETE_JSON_PARENTS = {"json_complete", "second_prompt_files"}


def _is_canonical_complete_name(name: str) -> bool:
    """Return True for a generated canonical complete JSON filename."""
    return name.endswith("__complete.json")


def _is_local_ai_complete_name(name: str) -> bool:
    """Return True for a generated local-AI working JSON filename."""
    return name.endswith("__complete_local_ai.json")


def classify_loaded_json_track(file_path: str) -> str:
    """Return a short user-facing label for the loaded JSON path."""
    path_text = str(file_path or "").strip()
    if not path_text:
        return "Not loaded"

    normalized = path_text.replace("\\", "/")
    parts = [part for part in normalized.split("/") if part]
    name = parts[-1].lower() if parts else ""
    parent = parts[-2].lower() if len(parts) >= 2 else ""

    if _is_canonical_complete_name(name) and parent in KNOWN_COMPLETE_JSON_PARENTS:
        return "Canonical web-AI JSON"

    if _is_local_ai_complete_name(name) and parent in KNOWN_COMPLETE_JSON_PARENTS:
        return "Local-AI working JSON"

    if _is_canonical_complete_name(name):
        return "Canonical web-AI JSON candidate"

    if _is_local_ai_complete_name(name):
        return "Local-AI working JSON candidate"

    return "Other JSON"
