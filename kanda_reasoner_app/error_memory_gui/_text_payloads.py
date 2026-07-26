# project-path: kanda_reasoner_app/error_memory_gui/_text_payloads.py
"""Pure text and archive payload helpers for the Error Memory GUI tab."""
from __future__ import annotations

import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory.intake import ERROR_LESSON_JSON_BEGIN, ERROR_LESSON_JSON_END

__all__ = [
    "archive_entry_text",
    "json_payload_from_text",
    "lesson_id_from_text_lenient",
    "operation_phase_from_editor_texts",
    "pending_file_updated_text",
    "summary_from_pending_raw_text",
    "text_has_formatted_lesson_payload",
    "validation_evidence_is_passing",
]


def text_has_formatted_lesson_payload(text: str) -> bool:
    """Return whether text looks like wrapped or raw lesson JSON."""
    stripped = str(text or "").strip()
    if not stripped:
        return False
    if ERROR_LESSON_JSON_BEGIN in stripped and ERROR_LESSON_JSON_END in stripped:
        return True
    return stripped.startswith("{") and stripped.endswith("}")


def json_payload_from_text(text: str) -> dict[str, Any] | None:
    """Return one JSON object from wrapped or raw text when possible."""
    stripped = str(text or "").strip()
    if not stripped:
        return None
    if ERROR_LESSON_JSON_BEGIN in stripped and ERROR_LESSON_JSON_END in stripped:
        stripped = stripped.split(ERROR_LESSON_JSON_BEGIN, 1)[1].split(ERROR_LESSON_JSON_END, 1)[0].strip()
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def lesson_id_from_text_lenient(text: str) -> str:
    """Return lesson_id from wrapped or raw JSON without active-ready checks."""
    payload = json_payload_from_text(text)
    if isinstance(payload, dict):
        return str(payload.get("lesson_id", "")).strip()
    return ""


def operation_phase_from_editor_texts(editor_text: str, intake_text: str) -> str:
    """Return operation_phase from editor text, then intake text, else unknown."""
    for text in (editor_text, intake_text):
        payload = json_payload_from_text(text)
        if isinstance(payload, dict) and str(payload.get("operation_phase", "")).strip():
            return str(payload.get("operation_phase", "")).strip()
    return "unknown"


def pending_file_updated_text(pending_file: Path) -> str:
    """Return a stable UTC mtime string for a pending file."""
    try:
        return (
            datetime.fromtimestamp(Path(pending_file).stat().st_mtime, timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
    except Exception:
        return ""


def summary_from_pending_raw_text(text: str, pending_file: Path) -> str:
    """Return a short row summary for raw pending evidence."""
    for line in str(text or "").splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned[:140]
    return "Pending raw evidence: " + Path(pending_file).name


def archive_entry_text(archive: zipfile.ZipFile, member_name: str) -> str:
    """Return safe UTF-8 text for one archive member or an empty string."""
    normalized_name = str(member_name or "").replace("\\", "/").strip()
    if not normalized_name or normalized_name.startswith("/") or "../" in normalized_name:
        return ""
    info = archive.getinfo(normalized_name)
    if info.is_dir() or info.file_size > 2_000_000:
        return ""
    return archive.read(info).decode("utf-8-sig", errors="replace").strip()


def validation_evidence_is_passing(lesson: dict[str, Any]) -> bool:
    """Return whether lesson evidence is strong enough for active status."""
    evidence_text = "\n".join(str(item) for item in lesson.get("validation_evidence", []) or [])
    command_text = str(lesson.get("validation_command_summary", "") or "")
    combined = (evidence_text + "\n" + command_text).upper()
    return "VALIDATION OK" in combined and "STATUS: IN_SYNC" in combined
