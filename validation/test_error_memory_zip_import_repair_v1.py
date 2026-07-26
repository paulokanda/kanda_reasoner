"""Validation for Error Memory ZIP import repair v1."""

from __future__ import annotations

import json
import sys
import tempfile
import uuid
from pathlib import Path
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.error_memory.importer import import_error_memory_file, import_error_memory_zip
from kanda_reasoner_app.error_memory.intake import ERROR_LESSON_JSON_BEGIN, ERROR_LESSON_JSON_END
from kanda_reasoner_app.error_memory.models import build_lesson
from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root
from kanda_reasoner_app.error_memory.store import list_lessons


def _make_project_root() -> Path:
    base = Path(tempfile.mkdtemp(prefix="kanda_error_memory_zip_import_test_"))
    root = base / ("Sample Project " + uuid.uuid4().hex[:8])
    root.mkdir(parents=True)
    return root


def _build_active_lesson(root: Path) -> dict:
    return build_lesson(
        selected_project_root=root,
        raw_error_text="VALIDATION FAILED\nKeyError: 'sample_state'",
        operation_phase="validation",
        symptom="Validation failed with a missing sample state key.",
        root_cause="The state producer did not return the key expected by validation.",
        wrong_assumption="The validation contract was updated without updating the producer.",
        correct_fix="Update the producer and add a regression validation.",
        long_term_prevention="Update producer, consumer, and validation together for validation-visible state.",
        do_not_repeat_rule="Do not update only the validation expectation for a GUI state key.",
        prevention_triggers=["KeyError in GUI state", "missing producer key"],
        validation_evidence=["VALIDATION OK: sample"],
        status="active",
    )


def test_import_canonical_lesson_zip_updates_store_and_index() -> None:
    root = _make_project_root()
    lesson = _build_active_lesson(root)
    zip_path = root.parent / "sample_error_memory.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("sample_error_memory/" + lesson["lesson_id"] + ".json", json.dumps(lesson))
    result = import_error_memory_zip(root, zip_path)
    assert result["ok"] is True
    assert result["imported_count"] == 1
    lessons = list_lessons(root, include_inactive=False)
    assert len(lessons) == 1
    assert lessons[0]["lesson_id"] == lesson["lesson_id"]
    index_path = resolve_project_error_memory_root(root) / "lessons_index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["lessons"][0]["lesson_id"] == lesson["lesson_id"]


def test_import_marker_wrapped_ai_form_text_file() -> None:
    root = _make_project_root()
    text_path = root.parent / "KANDA_ERROR_LESSON_JSON_SAMPLE.txt"
    text_path.write_text(
        f"""{ERROR_LESSON_JSON_BEGIN}
{{
  "status": "active",
  "raw_error_text": "VALIDATION FAILED\\nKeyError: sample_state",
  "operation_phase": "validation",
  "symptom": "Validation failed with a missing sample state key.",
  "root_cause": "The producer did not return the key expected by validation.",
  "wrong_assumption": "The validation contract was updated without updating the producer.",
  "correct_fix": "Update the producer and add a regression validation.",
  "long_term_prevention": "Update producer, consumer, and validation together.",
  "do_not_repeat_rule": "Do not update only the validation expectation for a GUI state key.",
  "prevention_triggers": ["KeyError in GUI state", "missing producer key"],
  "validation_evidence": ["VALIDATION OK: sample"]
}}
{ERROR_LESSON_JSON_END}
""",
        encoding="utf-8",
    )
    result = import_error_memory_file(root, text_path)
    assert result["ok"] is True
    assert result["imported_count"] == 1
    lessons = list_lessons(root, include_inactive=False)
    assert len(lessons) == 1
    assert lessons[0]["status"] == "active"
    assert "sample state" in lessons[0]["symptom"]


def main() -> int:
    test_import_canonical_lesson_zip_updates_store_and_index()
    test_import_marker_wrapped_ai_form_text_file()
    print("VALIDATION OK: error-memory-zip-import-repair-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
