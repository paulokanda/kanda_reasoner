"""Validate complete Error Memory clipboard export includes all saved statuses."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import types

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
    write_complete_error_memory_ai_clipboard_export,
    write_error_memory_ai_send_files,
)
from kanda_reasoner_app.error_memory.models import build_lesson  # noqa: E402
from kanda_reasoner_app.error_memory.paths import resolve_error_memory_lessons_dir  # noqa: E402
from kanda_reasoner_app.error_memory.store import save_lesson  # noqa: E402


def _make_lesson(project_root: Path, idx: int, status: str) -> dict:
    return build_lesson(
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
            "command": "python validation\\test_error_memory_export_complete_json_all_statuses_v4.py",
            "expected_marker": "VALIDATION OK: error-memory-export-complete-json-all-statuses-v4",
            "required_before_freeze": True,
        },
        status=status,
    )


def _method_block(source: str, name: str) -> str:
    marker = "def " + name + "("
    start = source.index(marker)
    next_start = source.find("\ndef ", start + 1)
    if next_start == -1:
        return source[start:]
    return source[start:next_start]


def _assert_complete_builder_reads_saved_json_directly() -> None:
    exporter_path = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory" / "exporter.py"
    source = exporter_path.read_text(encoding="utf-8")
    build_block = _method_block(source, "build_complete_error_memory_ai_clipboard_json")
    helper_block = _method_block(source, "_all_saved_lesson_json_objects")
    if "list_lessons(" in build_block:
        raise AssertionError("Complete clipboard export must not depend on list_lessons filtering behavior.")
    if "resolve_error_memory_lessons_dir" not in helper_block:
        raise AssertionError("Complete clipboard export must read the canonical lessons folder directly.")
    if ".glob(\"lesson-*.json\")" not in helper_block:
        raise AssertionError("Complete clipboard export must enumerate every saved lesson JSON file.")
    if "status" in helper_block and "include_inactive" not in build_block:
        raise AssertionError("Saved-JSON helper must not filter lessons by status.")


def main() -> None:
    tmp_dir = Path(tempfile.mkdtemp(prefix="kanda_em_export_v4_"))
    try:
        project_root = tmp_dir / "demo_project"
        project_root.mkdir(parents=True)
        second_prompt_destination = tmp_dir / "demo_project_show_project_to_AI" / "second_prompt_files"

        statuses = ["active"] * 12 + ["draft", "deprecated", "superseded"]
        for idx, status in enumerate(statuses):
            save_lesson(project_root, _make_lesson(project_root, idx, status))

        saved_files = list(resolve_error_memory_lessons_dir(project_root).glob("lesson-*.json"))
        if len(saved_files) != 15:
            raise AssertionError("Test setup failed to save 15 lesson JSON files.")

        complete_result = write_complete_error_memory_ai_clipboard_export(project_root, include_inactive=True)
        clipboard_text = str(complete_result.get("complete_clipboard_json") or "")
        payload = json.loads(clipboard_text)

        if not clipboard_text.strip().startswith("{"):
            raise AssertionError("Clipboard payload is not JSON text.")
        if clipboard_text.strip() == str(second_prompt_destination):
            raise AssertionError("Clipboard payload is still the destination folder path.")
        if payload.get("artifact_type") != "error_memory_ai_clipboard_export":
            raise AssertionError("Unexpected complete export artifact type.")
        if payload.get("lesson_count_exported") != 15:
            raise AssertionError("Complete clipboard export must include every saved lesson JSON file.")
        exported_statuses = sorted(str(lesson.get("status", "")) for lesson in payload.get("lessons", []))
        for required_status in ("active", "draft", "deprecated", "superseded"):
            if required_status not in exported_statuses:
                raise AssertionError("Complete clipboard export is missing status: " + required_status)
        if complete_result.get("complete_json_lesson_count") != 15:
            raise AssertionError("Complete export result count must include all saved statuses.")

        active_only_payload = json.loads(build_complete_error_memory_ai_clipboard_json(project_root, include_inactive=False))
        if active_only_payload.get("lesson_count_exported") != 12:
            raise AssertionError("include_inactive=False should still support active-only export.")

        complete_path = Path(str(complete_result.get("complete_json", "")))
        if not complete_path.exists():
            raise AssertionError("Backup complete JSON export file was not written.")
        if json.loads(complete_path.read_text(encoding="utf-8")) != payload:
            raise AssertionError("Backup complete JSON export does not match clipboard payload.")

        compact_result = write_error_memory_ai_send_files(project_root, second_prompt_destination)
        compact_payload = json.loads(Path(str(compact_result["compact_json"])).read_text(encoding="utf-8"))
        if len(compact_payload.get("lessons", [])) != 10:
            raise AssertionError("Compact second-prompt export should remain capped at 10 active lessons.")

        _assert_complete_builder_reads_saved_json_directly()

        print("VALIDATION OK: error-memory-export-complete-json-all-statuses-v4")
        print("ERROR_MEMORY_EXPORT_CLIPBOARD: complete JSON copied")
        print("ERROR_MEMORY_EXPORT_ALL_STATUSES: active draft deprecated superseded included")
        print("ERROR_MEMORY_EXPORT_NO_SECOND_PROMPT_PATH: enforced")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
