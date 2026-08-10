"""Static and behavioral contract tests for Error Memory text payload helpers."""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.error_memory.intake import ERROR_LESSON_JSON_BEGIN, ERROR_LESSON_JSON_END
from kanda_reasoner_app.error_memory_gui._text_payloads import (
    archive_entry_text,
    json_payload_from_text,
    lesson_id_from_text_lenient,
    operation_phase_from_editor_texts,
    summary_from_pending_raw_text,
    text_has_formatted_lesson_payload,
    validation_evidence_is_passing,
)

if TYPE_CHECKING:
    pass


def test_json_payload_from_wrapped_text_and_lesson_id() -> None:
    body = {"lesson_id": "lesson-demo", "operation_phase": "validation"}
    wrapped = ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps(body) + "\n" + ERROR_LESSON_JSON_END

    assert text_has_formatted_lesson_payload(wrapped) is True
    assert json_payload_from_text(wrapped) == body
    assert lesson_id_from_text_lenient(wrapped) == "lesson-demo"
    assert operation_phase_from_editor_texts(wrapped, "{}") == "validation"


def test_summary_and_validation_evidence() -> None:
    assert summary_from_pending_raw_text("\n  first real line\nsecond", Path("RAW_ERROR.txt")) == "first real line"
    assert summary_from_pending_raw_text("", Path("RAW_ERROR.txt")) == "Pending raw evidence: RAW_ERROR.txt"
    assert validation_evidence_is_passing({"validation_evidence": ["VALIDATION OK: demo", "STATUS: IN_SYNC"]}) is True
    assert validation_evidence_is_passing({"validation_evidence": ["VALIDATION OK: demo"]}) is False


def test_archive_entry_text_rejects_unsafe_member() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "lesson.zip"
        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr("safe.txt", "hello")
        with zipfile.ZipFile(archive_path) as archive:
            assert archive_entry_text(archive, "safe.txt") == "hello"
            assert archive_entry_text(archive, "../safe.txt") == ""
