"""Public contract tests for Error Memory lesson payload helpers."""
from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.error_memory_gui._lesson_payloads import (
    canonical_draft_lesson_from_partial,
    lesson_from_formatted_text,
    text_is_formatted_error_lesson_payload,
)
from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab


def test_error_memory_tab_facade_import_stays_stable() -> None:
    assert ErrorMemoryTab.__name__ == "ErrorMemoryTab"


def test_lesson_payload_helper_has_no_gui_imports() -> None:
    source = Path("kanda_reasoner_app/error_memory_gui/_lesson_payloads.py").read_text(encoding="utf-8")
    assert "PySide6" not in source
    assert "error_memory_tab" not in source
    assert "ErrorMemoryTab" not in source


def test_canonical_draft_lesson_from_partial_preserves_draft_status() -> None:
    draft = canonical_draft_lesson_from_partial(
        {
            "lesson_id": "lesson-sample",
            "symptom": "Sample symptom",
            "prevention_triggers": "alpha; beta",
            "validation_evidence": "VALIDATION OK: sample",
            "redaction": {"rules": "safe; export"},
        },
        project_slug="sample_project",
        source_text="raw fallback",
    )
    assert draft["status"] == "draft"
    assert draft["project_slug"] == "sample_project"
    assert draft["raw_error_text"] == "raw fallback"
    assert draft["prevention_triggers"] == ["alpha", "beta"]
    assert draft["redaction"]["rules"] == ["safe", "export"]


def test_lesson_from_formatted_text_accepts_raw_canonical_json() -> None:
    text = '{"lesson_id":"lesson-abc","symptom":"s","do_not_repeat_rule":"r"}'
    lesson = lesson_from_formatted_text(text, selected_project_root=Path.cwd())
    assert lesson["lesson_id"] == "lesson-abc"


def test_text_is_formatted_error_lesson_payload_requires_lesson_fields() -> None:
    assert text_is_formatted_error_lesson_payload(
        '{"lesson_id":"lesson-abc","symptom":"s","do_not_repeat_rule":"r"}',
        selected_project_root=Path.cwd(),
    )
    assert not text_is_formatted_error_lesson_payload(
        '{"lesson_id":"lesson-abc"}',
        selected_project_root=Path.cwd(),
    )
