# project-path: kanda_reasoner_app/error_memory_gui/_pending_rows.py
"""Pending Lessons-table row helpers for Error Memory GUI.

This module is intentionally non-GUI.  It assembles draft pending lessons and
virtual pending table rows without importing GUI frameworks or the Error Memory tab facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

from kanda_reasoner_app.error_memory_gui._lesson_payloads import (
    canonical_draft_lesson_from_partial,
)
from kanda_reasoner_app.error_memory_gui._pending_sources import (
    safe_pending_lesson_id_from_file,
)
from kanda_reasoner_app.error_memory_gui._text_payloads import (
    pending_file_updated_text,
    summary_from_pending_raw_text,
)

__all__ = [
    "draft_lesson_from_pending_raw_text",
    "pending_lesson_rows_for_table",
]


def draft_lesson_from_pending_raw_text(
    pending_file: Path,
    raw_text: str,
    *,
    project_slug: str,
) -> dict[str, Any]:
    """Build an editable draft lesson from a raw pending evidence file.

    This does not save anything.  It only creates the structured draft used by
    the Error Editor so the user can edit raw evidence, ask AI to correct it,
    or later promote an active-ready lesson.
    """
    summary = summary_from_pending_raw_text(raw_text, pending_file)
    stripped_text = str(raw_text or "").strip()
    partial: dict[str, Any] = {
        "lesson_id": safe_pending_lesson_id_from_file(pending_file),
        "status": "draft",
        "operation_phase": "pending_edit",
        "raw_error_text": stripped_text,
        "raw_error_snapshot_scrubbed": stripped_text,
        "symptom": summary,
        "root_cause": "",
        "wrong_assumption": "",
        "correct_fix": "",
        "long_term_prevention": "",
        "do_not_repeat_rule": "",
        "prevention_triggers": [],
        "validation_evidence": [],
        "exception": {},
        "fingerprint": {},
        "regression_check": {
            "type": "not_available",
            "command": "",
            "expected_marker": "",
            "required_before_freeze": False,
        },
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": [
                "Pending raw evidence loaded from AI-assisted intake; review before active promotion.",
            ],
        },
    }
    return canonical_draft_lesson_from_partial(
        partial,
        project_slug=project_slug,
        source_text=raw_text,
    )


def _normalized_dismissed_markers(values: Iterable[str]) -> set[str]:
    """Return resolved dismissed pending source markers for comparison."""
    markers: set[str] = set()
    for value in values:
        marker = str(value or "").strip()
        if not marker:
            continue
        try:
            marker = str(Path(marker).expanduser().resolve(strict=False))
        except Exception:
            pass
        markers.add(marker)
    return markers


def pending_lesson_rows_for_table(
    pending_files: Iterable[Path],
    dismissed_pending_files: Iterable[str],
    existing_lesson_ids: Iterable[str],
    *,
    is_formatted_lesson_payload: Callable[[str], bool],
    lesson_from_formatted_text: Callable[[str], dict[str, Any]],
) -> list[dict[str, str]]:
    """Return virtual Lessons rows for pending intake files waiting for edition."""
    dismissed_markers = _normalized_dismissed_markers(dismissed_pending_files)
    existing_ids = {str(item or "").strip() for item in existing_lesson_ids if str(item or "").strip()}
    rows: list[dict[str, str]] = []
    for candidate in pending_files:
        candidate = Path(candidate).expanduser().resolve(strict=False)
        marker = str(candidate)
        if marker in dismissed_markers:
            continue
        try:
            text = candidate.read_text(encoding="utf-8-sig", errors="replace").strip()
        except Exception:
            continue
        if not text:
            continue
        row = {
            "kind": "pending_edit",
            "status": "pending_edit",
            "symptom": "Pending raw evidence: " + candidate.name,
            "do_not_repeat_rule": "Raw pending evidence waiting for edition. Select this row to load it into AI-assisted intake and Error Editor.",
            "updated_at_utc": pending_file_updated_text(candidate),
            "lesson_id": safe_pending_lesson_id_from_file(candidate),
            "pending_path": marker,
        }
        if is_formatted_lesson_payload(text):
            try:
                lesson = lesson_from_formatted_text(text)
                lesson_id = str(lesson.get("lesson_id", "")).strip()
                duplicate = bool(lesson_id and lesson_id in existing_ids)
                row["kind"] = "pending_duplicate" if duplicate else "pending_review"
                row["status"] = row["kind"]
                row["symptom"] = str(lesson.get("symptom") or candidate.name).strip()[:180]
                row["do_not_repeat_rule"] = str(
                    lesson.get("do_not_repeat_rule")
                    or "Formatted pending lesson waiting for user review."
                ).strip()[:220]
                row["lesson_id"] = lesson_id or safe_pending_lesson_id_from_file(candidate)
            except Exception:
                row["kind"] = "pending_edit"
                row["status"] = "pending_edit"
                row["symptom"] = "Pending malformed formatted lesson: " + candidate.name
                row["do_not_repeat_rule"] = "Formatted pending file could not be parsed. Select this row to inspect/edit raw text."
        else:
            row["symptom"] = summary_from_pending_raw_text(text, candidate)
        rows.append(row)
    rows.sort(
        key=lambda item: (
            item.get("status", ""),
            item.get("updated_at_utc", ""),
            item.get("pending_path", ""),
        ),
        reverse=True,
    )
    return rows
