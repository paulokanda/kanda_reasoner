"""Public contract tests for Error Memory lesson import helpers."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

from kanda_reasoner_app.error_memory_gui._lesson_imports import (
    formatted_import_text_for_window,
    formatted_text_from_manifested_lesson_zip,
)
from kanda_reasoner_app.error_memory_gui.error_memory_tab import ErrorMemoryTab


def _is_payload(text: str) -> bool:
    return "lesson-abc" in str(text or "") and "do_not_repeat_rule" in str(text or "")


def _lesson_text() -> str:
    return json.dumps(
        {
            "lesson_id": "lesson-abc",
            "symptom": "Sample symptom",
            "do_not_repeat_rule": "Sample rule",
        },
        sort_keys=True,
    )


def test_error_memory_tab_facade_import_stays_stable() -> None:
    assert ErrorMemoryTab.__name__ == "ErrorMemoryTab"


def test_lesson_import_helper_has_no_gui_or_facade_imports() -> None:
    source = Path("kanda_reasoner_app/error_memory_gui/_lesson_imports.py").read_text(encoding="utf-8")
    assert "PySide6" not in source
    assert "QWidget" not in source
    assert "error_memory_tab" not in source
    assert "ErrorMemoryTab" not in source


def test_formatted_text_from_manifested_lesson_zip_prefers_receive_block(tmp_path: Path) -> None:
    archive_path = tmp_path / "lesson.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "bundle_manifest.json",
            json.dumps(
                {
                    "artifact_type": "formatted_error_memory_lesson_zip",
                    "receive_block": "receive/lesson.txt",
                }
            ),
        )
        archive.writestr("receive/lesson.txt", _lesson_text())
        archive.writestr("other.txt", "not a lesson")

    assert formatted_text_from_manifested_lesson_zip(
        archive_path,
        is_formatted_lesson_payload=_is_payload,
    ) == _lesson_text()


def test_formatted_import_text_for_window_scans_zip_when_manifest_absent(tmp_path: Path) -> None:
    archive_path = tmp_path / "lesson.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("notes/readme.md", "not a lesson")
        archive.writestr("lesson.json", _lesson_text())

    assert formatted_import_text_for_window(
        archive_path,
        is_formatted_lesson_payload=_is_payload,
    ) == _lesson_text()


def test_formatted_import_text_for_window_reads_text_file(tmp_path: Path) -> None:
    source = tmp_path / "lesson.md"
    source.write_text(_lesson_text(), encoding="utf-8")
    assert formatted_import_text_for_window(
        source,
        is_formatted_lesson_payload=_is_payload,
    ) == _lesson_text()
