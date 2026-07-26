"""Static and behavioral contracts for Error Memory pending row helpers."""
from __future__ import annotations

import json
from pathlib import Path

from kanda_reasoner_app.error_memory.intake import ERROR_LESSON_JSON_BEGIN, ERROR_LESSON_JSON_END
from kanda_reasoner_app.error_memory_gui import _pending_rows


def _formatted_lesson_text(lesson_id: str = "lesson-formatted") -> str:
    payload = {
        "lesson_id": lesson_id,
        "status": "active",
        "symptom": "Formatted pending symptom",
        "do_not_repeat_rule": "Keep formatted pending behavior.",
    }
    return ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps(payload) + "\n" + ERROR_LESSON_JSON_END


def _is_formatted(text: str) -> bool:
    return ERROR_LESSON_JSON_BEGIN in text and ERROR_LESSON_JSON_END in text


def _lesson_from_formatted(text: str) -> dict[str, object]:
    inner = text.split(ERROR_LESSON_JSON_BEGIN, 1)[1].split(ERROR_LESSON_JSON_END, 1)[0]
    return json.loads(inner)


def test_pending_rows_helper_is_private_non_gui_contract() -> None:
    source = Path(_pending_rows.__file__).read_text(encoding="utf-8")

    assert "PySide" not in source
    assert "Qt" not in source
    assert "error_memory_tab" not in source
    assert "ErrorMemoryTab" not in source


def test_draft_lesson_from_pending_raw_text_uses_pending_identity(tmp_path: Path) -> None:
    pending = tmp_path / "RAW_ERROR_EVIDENCE_generated_helper_escaped.txt"
    draft = _pending_rows.draft_lesson_from_pending_raw_text(
        pending,
        "raw evidence text",
        project_slug="kanda_reasoner",
    )

    assert draft["lesson_id"] == "lesson-pending-generated-helper-escaped"
    assert draft["status"] == "draft"
    assert draft["operation_phase"] == "pending_edit"
    assert draft["raw_error_text"] == "raw evidence text"
    assert "Pending raw evidence" in draft["redaction"]["rules"][0]


def test_pending_rows_classifies_raw_formatted_and_duplicate_sources(tmp_path: Path) -> None:
    raw = tmp_path / "raw.txt"
    formatted = tmp_path / "formatted.json"
    duplicate = tmp_path / "duplicate.json"
    raw.write_text("plain raw evidence", encoding="utf-8")
    formatted.write_text(_formatted_lesson_text("lesson-new"), encoding="utf-8")
    duplicate.write_text(_formatted_lesson_text("lesson-dupe"), encoding="utf-8")

    rows = _pending_rows.pending_lesson_rows_for_table(
        [raw, formatted, duplicate],
        [],
        ["lesson-dupe"],
        is_formatted_lesson_payload=_is_formatted,
        lesson_from_formatted_text=_lesson_from_formatted,
    )
    by_id = {row["lesson_id"]: row for row in rows}

    assert by_id["lesson-new"]["kind"] == "pending_review"
    assert by_id["lesson-dupe"]["kind"] == "pending_duplicate"
    assert by_id["lesson-pending-raw"]["kind"] == "pending_edit"


def test_pending_rows_respects_dismissed_sources(tmp_path: Path) -> None:
    pending = tmp_path / "skip.txt"
    pending.write_text("skip me", encoding="utf-8")

    rows = _pending_rows.pending_lesson_rows_for_table(
        [pending],
        [str(pending.resolve(strict=False))],
        [],
        is_formatted_lesson_payload=_is_formatted,
        lesson_from_formatted_text=_lesson_from_formatted,
    )

    assert rows == []


if __name__ == "__main__":
    test_pending_rows_helper_is_private_non_gui_contract()
