"""Validation for Error Memory plain-text intake repair v1.

This repair makes the Error Memory Receive Formulary workflow tolerant when AI
returns a short lesson text instead of the strict KANDA_ERROR_LESSON_JSON block.
Plain text is saved as a draft so the GUI/table does not remain empty.
"""

from __future__ import annotations

import json
import sys
import tempfile
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.error_memory.importer import import_error_memory_file  # noqa: E402
from kanda_reasoner_app.error_memory.intake import parse_error_lesson_ai_response, save_ai_form_as_lesson  # noqa: E402
from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root  # noqa: E402
from kanda_reasoner_app.error_memory.store import list_lessons  # noqa: E402

PLAIN_TEXT_LESSON = """Validation failed with KeyError for missing ml_pilot_activation_state.
Do not add a new validation-visible GUI key only to tests or validation logic. The method that produces the GUI state must return the key consistently.
"""


def _make_project_root() -> Path:
    base = Path(tempfile.mkdtemp(prefix="kanda_error_memory_plain_text_intake_"))
    root = base / ("Project " + uuid.uuid4().hex[:8])
    root.mkdir(parents=True)
    return root


def test_plain_text_ai_answer_parses_as_draft_form() -> None:
    form = parse_error_lesson_ai_response(PLAIN_TEXT_LESSON)
    assert form["status"] == "draft"
    assert form["operation_phase"] == "validation"
    assert form["symptom"].startswith("Validation failed with KeyError")
    assert "Do not add a new validation-visible GUI key" in form["do_not_repeat_rule"]
    assert "ml_pilot_activation_state" in form["prevention_triggers"]


def test_plain_text_ai_answer_saves_and_populates_store_index() -> None:
    root = _make_project_root()
    form = parse_error_lesson_ai_response(PLAIN_TEXT_LESSON)
    path, lesson = save_ai_form_as_lesson(selected_project_root=root, form_inputs=form)
    assert path.exists()
    assert lesson["status"] == "draft"
    lessons = list_lessons(root, include_inactive=True)
    assert len(lessons) == 1
    assert lessons[0]["symptom"].startswith("Validation failed with KeyError")
    index_path = resolve_project_error_memory_root(root) / "lessons_index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["lessons"][0]["lesson_id"] == lessons[0]["lesson_id"]


def test_plain_text_file_import_uses_same_fallback() -> None:
    root = _make_project_root()
    source = root.parent / "short_ai_lesson.txt"
    source.write_text(PLAIN_TEXT_LESSON, encoding="utf-8")
    result = import_error_memory_file(root, source)
    assert result["ok"] is True
    assert result["imported_count"] == 1
    lessons = list_lessons(root, include_inactive=True)
    assert len(lessons) == 1
    assert lessons[0]["status"] == "draft"


def test_gui_receive_dialog_mentions_plain_text_fallback_without_importing_pyside() -> None:
    gui_source = (PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py").read_text(
        encoding="utf-8"
    )
    assert "Short plain-text lesson notes are also accepted as draft lessons" in gui_source
    assert "Apply and Save AI Lesson" in gui_source


def main() -> int:
    test_plain_text_ai_answer_parses_as_draft_form()
    test_plain_text_ai_answer_saves_and_populates_store_index()
    test_plain_text_file_import_uses_same_fallback()
    test_gui_receive_dialog_mentions_plain_text_fallback_without_importing_pyside()
    print("VALIDATION OK: error-memory-plain-text-intake-repair-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
