"""Validate Error Memory ZIP import filtering.

This protects the GUI import workflow from treating README/help text inside a ZIP
as a lesson. ZIP import should save only real lesson payloads: canonical JSON,
AI form JSON, or marker-wrapped KANDA_ERROR_LESSON_JSON text.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


def _project_root_from_argv() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve(strict=False)
    return Path.cwd().resolve(strict=False)


def _selected_project_fixture(project_root: Path) -> Path:
    drive_root = Path(project_root.anchor) if project_root.anchor else project_root
    fixture = drive_root / "kanda_error_memory_zip_import_filter_fixture_project"
    if fixture.exists():
        shutil.rmtree(fixture, ignore_errors=True)
    fixture.mkdir(parents=True, exist_ok=True)
    return fixture


def _cleanup_selected_project_fixture(selected_project: Path) -> None:
    drive_root = Path(selected_project.anchor) if selected_project.anchor else selected_project.parent
    show_root = drive_root / (selected_project.name + "_show_project_to_AI")
    shutil.rmtree(selected_project, ignore_errors=True)
    shutil.rmtree(show_root, ignore_errors=True)


def _make_test_zip(zip_path: Path) -> None:
    real_lesson = """KANDA_ERROR_LESSON_JSON_BEGIN
{
  "status": "draft",
  "raw_error_text": "VALIDATION FAILED: GUI_IMPORT_FILTER_TEST_MARKER\n\nKeyError: 'gui_import_filter_key'",
  "operation_phase": "validation",
  "symptom": "Validation failed with KeyError for gui_import_filter_key.",
  "root_cause": "A validation-visible key was expected but the producer did not return it.",
  "wrong_assumption": "The validation expectation was updated without updating the producer.",
  "correct_fix": "Update the producer to return gui_import_filter_key and rerun validation.",
  "long_term_prevention": "When adding validation-visible keys, update producer and validation together.",
  "do_not_repeat_rule": "Do not add validation-visible keys only to tests; update the producer too.",
  "prevention_triggers": ["GUI_IMPORT_FILTER_TEST_MARKER", "KeyError", "producer mismatch"],
  "validation_evidence": ["Validation failed before correction with GUI_IMPORT_FILTER_TEST_MARKER."],
  "notes": "Filter test lesson. Keep draft."
}
KANDA_ERROR_LESSON_JSON_END
"""
    readme = """# README
This helper file explains the test ZIP and must not be imported as a lesson.
It does not contain KANDA_ERROR_LESSON_JSON markers.
"""
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("gui_import_filter_test/KANDA_ERROR_LESSON_JSON_FILTER_TEST.txt", real_lesson)
        archive.writestr("gui_import_filter_test/README.txt", readme)


def main() -> int:
    project_root = _project_root_from_argv()
    sys.path.insert(0, str(project_root))

    from kanda_reasoner_app.error_memory.importer import import_error_memory_zip
    from kanda_reasoner_app.error_memory.paths import resolve_error_memory_index_path, resolve_error_memory_lessons_dir

    selected_project = _selected_project_fixture(project_root)
    try:
        with tempfile.TemporaryDirectory(prefix="kanda_error_memory_zip_import_filter_") as tmp:
            zip_path = Path(tmp) / "kanda_error_memory_zip_import_filter_test.zip"
            _make_test_zip(zip_path)
            result = import_error_memory_zip(selected_project, zip_path)

        imported = result.get("imported_lessons", [])
        skipped = result.get("skipped", [])
        if result.get("imported_count") != 1:
            raise AssertionError(f"Expected exactly one imported lesson, got: {json.dumps(result, indent=2)}")
        if not skipped or not any("README.txt" in item for item in skipped):
            raise AssertionError(f"Expected README.txt to be skipped, got: {json.dumps(result, indent=2)}")
        if imported[0].get("source") != "gui_import_filter_test/KANDA_ERROR_LESSON_JSON_FILTER_TEST.txt":
            raise AssertionError(f"Unexpected imported source: {json.dumps(result, indent=2)}")

        lessons_dir = resolve_error_memory_lessons_dir(selected_project)
        lesson_files = list(lessons_dir.glob("*.json"))
        if len(lesson_files) != 1:
            raise AssertionError(f"Expected exactly one lesson JSON file, got {len(lesson_files)} at {lessons_dir}")
        lesson = json.loads(lesson_files[0].read_text(encoding="utf-8"))
        if "GUI_IMPORT_FILTER_TEST_MARKER" not in json.dumps(lesson):
            raise AssertionError("Imported lesson marker missing from canonical lesson JSON.")

        index_path = resolve_error_memory_index_path(selected_project)
        index = json.loads(index_path.read_text(encoding="utf-8"))
        if len(index.get("lessons", [])) != 1:
            raise AssertionError(f"Expected one index entry, got: {json.dumps(index, indent=2)}")

        print("VALIDATION OK: error-memory-zip-import-filter-v1")
        print("STATUS: IN_SYNC")
        return 0
    finally:
        _cleanup_selected_project_fixture(selected_project)


if __name__ == "__main__":
    raise SystemExit(main())
