"""Validate complete Error Memory JSON clipboard export behavior."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import types

# Some source exports omit optional storage-policy helper modules that are not
# needed for this Error Memory export test. Stub the optional module before
# importing project path helpers so the focused validation remains deterministic.
_optional_name = "kanda_reasoner_app.storage_policy.maintenance_subfolder_policy"
if _optional_name not in sys.modules:
    _optional_module = types.ModuleType(_optional_name)
    _optional_module.MAINTENANCE_SUBFOLDER_NAMES = ()
    _optional_module.MAINTENANCE_SUBFOLDER_PARTS = {}
    _optional_module.describe_maintenance_subfolder_policy = lambda *args, **kwargs: {}
    _optional_module.ensure_maintenance_structure = lambda *args, **kwargs: {}
    _optional_module.ensure_maintenance_subfolder = lambda *args, **kwargs: Path("")
    _optional_module.get_all_maintenance_subfolders = lambda *args, **kwargs: []
    _optional_module.get_maintenance_subfolder = lambda *args, **kwargs: Path("")
    _optional_module.relative_maintenance_subfolder_parts = lambda *args, **kwargs: ()
    sys.modules[_optional_name] = _optional_module

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.error_memory.exporter import (  # noqa: E402
    build_complete_error_memory_ai_clipboard_json,
    write_error_memory_ai_send_files,
)
from kanda_reasoner_app.error_memory.models import build_lesson  # noqa: E402
from kanda_reasoner_app.error_memory.store import save_lesson  # noqa: E402


def _make_lesson(project_root: Path, idx: int, status: str) -> dict:
    lesson = build_lesson(
        selected_project_root=project_root,
        raw_error_text="Traceback example " + str(idx),
        operation_phase="validation",
        symptom="Symptom " + str(idx),
        root_cause="Root cause " + str(idx),
        wrong_assumption="Wrong assumption " + str(idx),
        correct_fix="Correct fix " + str(idx),
        long_term_prevention="Long term prevention " + str(idx),
        do_not_repeat_rule="Do not repeat rule " + str(idx),
        prevention_triggers=["trigger " + str(idx)],
        validation_evidence=["validation evidence " + str(idx)],
        regression_check={
            "type": "validation_command",
            "command": "python validation\\test_example.py",
            "expected_marker": "VALIDATION OK: example",
            "required_before_freeze": True,
        },
        status=status,
        lesson_id="lesson-export-clipboard-" + str(idx),
    )
    lesson["source_patch_zip"] = "example_patch_" + str(idx) + ".zip"
    lesson["install_command_summary"] = "Install summary " + str(idx)
    lesson["validation_command_summary"] = "Validation summary " + str(idx)
    lesson["notes"] = "Notes " + str(idx)
    return lesson


def main() -> int:
    temp_root = Path(tempfile.mkdtemp(prefix="kanda_em_export_clipboard_"))
    try:
        project_root = temp_root / "demo_project"
        project_root.mkdir(parents=True)
        destination = temp_root / "manual_export"

        for idx in range(12):
            status = "draft" if idx in {2, 7} else "active"
            save_lesson(project_root, _make_lesson(project_root, idx, status))

        clipboard_text = build_complete_error_memory_ai_clipboard_json(
            project_root,
            include_inactive=True,
        )
        payload = json.loads(clipboard_text)

        assert payload["artifact_type"] == "error_memory_ai_clipboard_export"
        assert payload["schema_version"] == "1.0"
        assert payload["project_slug"] == "demo_project"
        assert payload["include_inactive"] is True
        assert payload["lesson_count_exported"] == 12
        assert len(payload["lessons"]) == 12
        statuses = {lesson.get("status") for lesson in payload["lessons"]}
        assert "draft" in statuses
        assert "active" in statuses
        assert any(lesson.get("lesson_id") == "lesson-export-clipboard-11" for lesson in payload["lessons"])
        assert "not capped" in payload["clipboard_contract"]

        result = write_error_memory_ai_send_files(project_root, destination, max_lessons=3)
        assert Path(result["complete_json"]).is_file()
        complete_payload = json.loads(Path(result["complete_json"]).read_text(encoding="utf-8"))
        assert complete_payload["lesson_count_exported"] == 12
        assert result["complete_json_lesson_count"] == 12

        compact_payload = json.loads(Path(result["compact_json"]).read_text(encoding="utf-8"))
        assert len(compact_payload["lessons"]) == 3

        tab_source = (PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py").read_text(encoding="utf-8")
        assert "build_complete_error_memory_ai_clipboard_json" in tab_source
        assert "QApplication.clipboard().setText(clipboard_text)" in tab_source
        assert "QApplication.clipboard().setText(destination)" not in tab_source

        print("VALIDATION OK: error-memory-export-clipboard-complete-json-v1")
        print("ERROR_MEMORY_EXPORT_CLIPBOARD: complete JSON copied")
        print("ERROR_MEMORY_EXPORT_COUNT: all lessons included")
        return 0
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
