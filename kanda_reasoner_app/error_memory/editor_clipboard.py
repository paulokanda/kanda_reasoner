# project-path: kanda_reasoner_app/error_memory/editor_clipboard.py
"""Clipboard payload helpers for Error Memory editor actions.

These helpers are deliberately GUI-free so the clipboard contract can be
validated without importing PySide6. The Copy error/draft button must copy the
latest meaningful Error Editor payload, not the old AI formulary prompt or the
sample receive-ready block inside that prompt.
"""

from __future__ import annotations

from .intake_normalization import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
)

import json
from typing import Any

ERROR_DRAFT_MARKER = "Current error/draft JSON for completion or correction:"


def _first_json_object_text(text: str) -> str:
    """Return the first balanced JSON object text in *text*, or an empty string."""
    source = str(text or "")
    start = source.find("{")
    if start == -1:
        return ""

    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(source)):
        char = source[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    return ""




def _raw_error_text_from_json_text(text: str) -> str:
    """Return raw_error_text from the first JSON object in *text*, when present."""
    json_text = _first_json_object_text(text)
    if not json_text:
        return ""
    try:
        payload: Any = json.loads(json_text)
    except json.JSONDecodeError:
        return ""
    if not isinstance(payload, dict):
        return ""
    raw_error_text = payload.get("raw_error_text")
    if isinstance(raw_error_text, str) and raw_error_text.strip():
        return raw_error_text.strip()
    return ""

def _last_receive_ready_block(text: str) -> str:
    """Return the last KANDA_ERROR_LESSON_JSON block in *text*, if present."""
    source = str(text or "")
    begin = source.rfind(ERROR_LESSON_JSON_BEGIN)
    if begin == -1:
        return ""
    end = source.find(ERROR_LESSON_JSON_END, begin)
    if end == -1:
        return ""
    return source[begin : end + len(ERROR_LESSON_JSON_END)].strip()


def _payload_from_last_error_draft_marker(text: str) -> str:
    """Extract the payload after the last Current error/draft marker.

    Old AI prompt wrappers include a sample KANDA_ERROR_LESSON_JSON_BEGIN/END
    answer shape before the real Current error/draft JSON section. Therefore the
    marker section must win over any earlier receive-ready sample block.
    """
    source = str(text or "")
    marker_index = source.rfind(ERROR_DRAFT_MARKER)
    if marker_index == -1:
        return ""

    tail = source[marker_index + len(ERROR_DRAFT_MARKER) :].strip()
    json_text = _first_json_object_text(tail)
    if not json_text:
        return ""

    try:
        payload: Any = json.loads(json_text)
    except json.JSONDecodeError:
        return ""

    if not isinstance(payload, dict):
        return ""

    raw_error_text = payload.get("raw_error_text")
    if isinstance(raw_error_text, str) and raw_error_text.strip():
        return raw_error_text.strip()

    meaningful_payload = {key: value for key, value in payload.items() if value not in ("", [], {}, None)}
    if meaningful_payload:
        return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False)
    return ""


def extract_error_editor_text_for_ai(text: str) -> str:
    """Return only the latest error/draft payload from Error Editor text.

    Priority order:
    1. The payload after the last Current error/draft marker, when present.
       This beats sample KANDA blocks inside old AI prompt wrappers.
    2. Last receive-ready KANDA_ERROR_LESSON_JSON block, when no marker payload
       is present.
    3. The raw editor text, stripped.
    """
    source = str(text or "").strip()
    if not source:
        return ""

    marker_payload = _payload_from_last_error_draft_marker(source)
    if marker_payload:
        return marker_payload

    receive_ready = _last_receive_ready_block(source)
    if receive_ready:
        raw_error_text = _raw_error_text_from_json_text(receive_ready)
        return raw_error_text or receive_ready

    raw_error_text = _raw_error_text_from_json_text(source)
    return raw_error_text or source
