"""Validation for Error Memory ZIP Import Dependency Repair v1.

This repair is intentionally small: the previous ZIP-import patch imported
kanda_reasoner_app.error_memory.intake, but a local install may not have had
that module if the AI-formulary-intake patch was not installed first.  This
validation proves the dependency is now bundled and the GUI source exposes the
Import Error Lesson ZIP button.
"""

from __future__ import annotations

import json
import sys
import tempfile
import uuid
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.error_memory.importer import import_error_memory_zip  # noqa: E402
from kanda_reasoner_app.error_memory.intake import (  # noqa: E402
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    parse_error_lesson_ai_response,
)
from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root  # noqa: E402
from kanda_reasoner_app.error_memory.store import list_lessons  # noqa: E402


def _make_project_root() -> Path:
    base = Path(tempfile.mkdtemp(prefix="kanda_error_memory_dependency_repair_"))
    root = base / ("Project " + uuid.uuid4().hex[:8])
    root.mkdir(parents=True)
    return root


def test_intake_module_is_available_and_parses_receive_block() -> None:
    payload = f"""{ERROR_LESSON_JSON_BEGIN}
{{
  "status": "active",
  "raw_error_text": "VALIDATION FAILED\\nKeyError: sample_state",
  "operation_phase": "validation",
  "symptom": "Validation failed with a missing sample state key.",
  "root_cause": "The state producer did not return the key expected by validation.",
  "wrong_assumption": "The validation contract was updated without updating the producer.",
  "correct_fix": "Update the producer and add a regression validation.",
  "long_term_prevention": "Update producer, consumer, and validation together.",
  "do_not_repeat_rule": "Do not update only the validation expectation for a GUI state key.",
  "prevention_triggers": ["KeyError in GUI state", "missing producer key"],
  "validation_evidence": ["VALIDATION OK: sample"]
}}
{ERROR_LESSON_JSON_END}
"""
    form = parse_error_lesson_ai_response(payload)
    assert form["status"] == "active"
    assert "missing sample state" in form["symptom"]


def test_zip_import_uses_intake_and_populates_project_store() -> None:
    root = _make_project_root()
    zip_path = root.parent / "sample_error_memory_formulary.zip"
    text = f"""{ERROR_LESSON_JSON_BEGIN}
{{
  "status": "active",
  "raw_error_text": "VALIDATION FAILED\\nKeyError: sample_state",
  "operation_phase": "validation",
  "symptom": "Validation failed with a missing sample state key.",
  "root_cause": "The state producer did not return the key expected by validation.",
  "wrong_assumption": "The validation contract was updated without updating the producer.",
  "correct_fix": "Update the producer and add a regression validation.",
  "long_term_prevention": "Update producer, consumer, and validation together.",
  "do_not_repeat_rule": "Do not update only the validation expectation for a GUI state key.",
  "prevention_triggers": ["KeyError in GUI state", "missing producer key"],
  "validation_evidence": ["VALIDATION OK: sample"]
}}
{ERROR_LESSON_JSON_END}
"""
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("sample_error_memory/KANDA_ERROR_LESSON_JSON_SAMPLE.txt", text)

    result = import_error_memory_zip(root, zip_path)
    assert result["ok"] is True
    assert result["imported_count"] == 1
    lessons = list_lessons(root, include_inactive=False)
    assert len(lessons) == 1
    assert lessons[0]["status"] == "active"
    index_path = resolve_project_error_memory_root(root) / "lessons_index.json"
    assert index_path.exists()
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["lessons"][0]["lesson_id"] == lessons[0]["lesson_id"]


def test_gui_source_exposes_import_button_without_importing_pyside() -> None:
    gui_source = (PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py").read_text(
        encoding="utf-8"
    )
    assert "Import Error Lesson ZIP" in gui_source
    assert "_import_error_lesson_zip" in gui_source
    assert "import_error_memory_file" in gui_source


def main() -> int:
    test_intake_module_is_available_and_parses_receive_block()
    test_zip_import_uses_intake_and_populates_project_store()
    test_gui_source_exposes_import_button_without_importing_pyside()
    print("VALIDATION OK: error-memory-zip-import-dependency-repair-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
