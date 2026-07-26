"""Validate complete Error Memory JSON export with Windows-isolated test roots.

This validation intentionally avoids counting all files in a drive-root
show_project_to_AI folder without first isolating that folder. On Windows the
project path resolver maps a project root to <drive>:/<project>_show_project_to_AI,
so stale generated files from earlier runs can survive outside tempfile cleanup.
"""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
import tempfile
import types
import uuid

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
from kanda_reasoner_app.error_memory.paths import (  # noqa: E402
    resolve_error_memory_lessons_dir,
    resolve_show_project_to_ai_root,
)
from kanda_reasoner_app.error_memory.store import save_lesson  # noqa: E402


STATUSES = ["active"] * 12 + ["draft", "deprecated", "superseded"]


def _make_lesson(project_root: Path, idx: int, status: str) -> dict:
    return build_lesson(
        selected_project_root=project_root,
        lesson_id="lesson-export-v5-" + str(idx).zfill(2),
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
            "command": "python validation\\test_error_memory_export_complete_json_windows_isolated_v5.py",
            "expected_marker": "VALIDATION OK: error-memory-export-complete-json-windows-isolated-v5",
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


def _assert_exporter_contracts() -> None:
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
    if "if not include_inactive" not in build_block:
        raise AssertionError("Complete export must keep an explicit include_inactive switch.")


def _assert_gui_contracts() -> None:
    gui_path = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    source = gui_path.read_text(encoding="utf-8")
    export_block = _method_block(source, "_export_for_ai")
    if "write_error_memory_ai_send_files" in export_block:
        raise AssertionError("Error Memory export button must not call the second-prompt export writer.")
    if "resolve_second_prompt_files_root" in export_block:
        raise AssertionError("Error Memory export button must not resolve second_prompt_files.")
    if "_copy_complete_error_memory_json_to_clipboard" not in export_block:
        raise AssertionError("Error Memory export button must copy complete JSON through the JSON-only clipboard helper.")
    if "Copy Complete Error Memory JSON for AI" not in source:
        raise AssertionError("Error Memory export button label must state the complete JSON clipboard contract.")


def _assert_patch_zip_schema_gate_restored() -> None:
    validator_path = PROJECT_ROOT / "kanda_reasoner_app" / "patch_governance" / "validator.py"
    source = validator_path.read_text(encoding="utf-8")
    required_fragments = [
        "ERROR_MEMORY_BASE_REQUIRED_KEYS",
        "_validate_error_memory_lesson_blocks",
        "error_memory_lesson_blocks_checked",
        "schema_version",
        "project_slug",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in source]
    if missing:
        raise AssertionError("Patch ZIP validator is missing Error Memory schema gate fragments: " + ", ".join(missing))


def main() -> None:
    tmp_dir = Path(tempfile.mkdtemp(prefix="kanda_em_export_v5_"))
    show_root = None
    try:
        unique_project_name = "demo_project_em_export_v5_" + uuid.uuid4().hex[:12]
        project_root = tmp_dir / unique_project_name
        project_root.mkdir(parents=True)
        show_root = resolve_show_project_to_ai_root(project_root)

        # Critical Windows isolation: the resolved show_project_to_AI root may
        # live at the drive root and can survive tempfile cleanup. Remove only
        # this unique test root before saving lessons.
        if show_root.exists():
            shutil.rmtree(show_root, ignore_errors=True)

        lessons_dir = resolve_error_memory_lessons_dir(project_root)
        expected_lesson_ids = []
        for idx, status in enumerate(STATUSES):
            lesson = _make_lesson(project_root, idx, status)
            expected_lesson_ids.append(str(lesson["lesson_id"]))
            save_lesson(project_root, lesson)

        missing_paths = [
            lesson_id
            for lesson_id in expected_lesson_ids
            if not (lessons_dir / (lesson_id + ".json")).is_file()
        ]
        if missing_paths:
            raise AssertionError("Test setup failed to save expected lesson files: " + ", ".join(missing_paths))

        saved_files = list(lessons_dir.glob("lesson-*.json"))
        if len(saved_files) != len(expected_lesson_ids):
            raise AssertionError(
                "Isolated test root contains unexpected lesson count: "
                + str(len(saved_files))
                + "; expected "
                + str(len(expected_lesson_ids))
            )

        complete_result = write_complete_error_memory_ai_clipboard_export(project_root, include_inactive=True)
        clipboard_text = str(complete_result.get("complete_clipboard_json") or "")
        payload = json.loads(clipboard_text)

        if not clipboard_text.strip().startswith("{"):
            raise AssertionError("Clipboard payload is not JSON text.")
        if "second_prompt_files" in clipboard_text and clipboard_text.strip().endswith("second_prompt_files"):
            raise AssertionError("Clipboard payload is still a second_prompt_files path.")
        if payload.get("artifact_type") != "error_memory_ai_clipboard_export":
            raise AssertionError("Unexpected complete export artifact type.")
        if payload.get("lesson_count_exported") != len(expected_lesson_ids):
            raise AssertionError("Complete clipboard export must include every saved lesson JSON file.")

        exported_ids = {str(lesson.get("lesson_id", "")) for lesson in payload.get("lessons", [])}
        missing_exported = sorted(set(expected_lesson_ids) - exported_ids)
        if missing_exported:
            raise AssertionError("Complete export missed expected lesson ids: " + ", ".join(missing_exported))

        exported_statuses = sorted(str(lesson.get("status", "")) for lesson in payload.get("lessons", []))
        for required_status in ("active", "draft", "deprecated", "superseded"):
            if required_status not in exported_statuses:
                raise AssertionError("Complete clipboard export is missing status: " + required_status)
        if complete_result.get("complete_json_lesson_count") != len(expected_lesson_ids):
            raise AssertionError("Complete export result count must include all saved statuses.")

        active_only_payload = json.loads(build_complete_error_memory_ai_clipboard_json(project_root, include_inactive=False))
        if active_only_payload.get("lesson_count_exported") != 12:
            raise AssertionError("include_inactive=False should still support active-only export.")

        complete_path = Path(str(complete_result.get("complete_json", "")))
        if not complete_path.exists():
            raise AssertionError("Backup complete JSON export file was not written.")
        if json.loads(complete_path.read_text(encoding="utf-8")) != payload:
            raise AssertionError("Backup complete JSON export does not match clipboard payload.")

        second_prompt_destination = tmp_dir / "manual_second_prompt_files"
        compact_result = write_error_memory_ai_send_files(project_root, second_prompt_destination)
        compact_payload = json.loads(Path(str(compact_result["compact_json"])).read_text(encoding="utf-8"))
        if len(compact_payload.get("lessons", [])) != 10:
            raise AssertionError("Compact second-prompt export should remain capped at 10 active lessons.")

        _assert_exporter_contracts()
        _assert_gui_contracts()
        _assert_patch_zip_schema_gate_restored()

        print("VALIDATION OK: error-memory-export-complete-json-windows-isolated-v5")
        print("ERROR_MEMORY_EXPORT_CLIPBOARD: complete JSON copied")
        print("ERROR_MEMORY_EXPORT_ALL_STATUSES: active draft deprecated superseded included")
        print("ERROR_MEMORY_EXPORT_NO_SECOND_PROMPT_PATH: enforced")
        print("ERROR_MEMORY_EXPORT_WINDOWS_ISOLATION: show_project root cleaned")
        print("PATCH_ZIP_SCHEMA_GATE_RESTORED: error memory lesson blocks checked")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        if show_root is not None:
            shutil.rmtree(show_root, ignore_errors=True)


if __name__ == "__main__":
    main()
