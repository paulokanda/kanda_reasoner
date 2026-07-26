"""Validate Error Memory export copies complete JSON, not a folder path."""

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
            "command": "python validation\\test_error_memory_export_clipboard_complete_json_v2.py",
            "expected_marker": "VALIDATION OK: error-memory-export-clipboard-complete-json-v2",
            "required_before_freeze": True,
        },
        status=status,
    )
    lesson["source_patch_zip"] = "patch_" + str(idx) + ".zip"
    lesson["install_command_summary"] = "Install summary " + str(idx)
    lesson["validation_command_summary"] = "Validation summary " + str(idx)
    lesson["notes"] = "Notes " + str(idx)
    return lesson


def _method_block(source: str, name: str) -> str:
    marker = "    def " + name + "("
    start = source.index(marker)
    next_start = source.find("\n    def ", start + 1)
    if next_start == -1:
        return source[start:]
    return source[start:next_start]


def _assert_gui_handler_cannot_copy_destination_path() -> None:
    tab_path = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    source = tab_path.read_text(encoding="utf-8")
    export_block = _method_block(source, "_export_for_ai")
    helper_block = _method_block(source, "_copy_complete_error_memory_json_to_clipboard")
    if "setText(destination" in export_block:
        raise AssertionError("Export handler still copies destination path to clipboard.")
    if "Destination path copied" in source:
        raise AssertionError("Old destination-path clipboard message is still present.")
    if "_copy_complete_error_memory_json_to_clipboard(clipboard_text)" not in export_block:
        raise AssertionError("Export handler does not use the dedicated JSON clipboard helper.")
    if export_block.count("_copy_complete_error_memory_json_to_clipboard(clipboard_text)") < 2:
        raise AssertionError("Export handler must copy JSON before and after the modal information dialog.")
    if "QClipboard.Mode.Clipboard" not in helper_block:
        raise AssertionError("JSON clipboard helper must write to the system clipboard mode explicitly.")
    if "second_prompt_files" not in helper_block:
        raise AssertionError("JSON clipboard helper must reject path-looking payloads.")
    if "Export Error Memory for AI - Copy Complete JSON" not in source:
        raise AssertionError("Button label must make the clipboard contract explicit.")


def main() -> None:
    tmp_dir = Path(tempfile.mkdtemp(prefix="kanda_em_export_v2_"))
    try:
        project_root = tmp_dir / "demo_project"
        project_root.mkdir(parents=True)
        destination = tmp_dir / "demo_project_show_project_to_AI" / "second_prompt_files"

        for idx in range(15):
            status = "active" if idx != 13 else "draft"
            save_lesson(project_root, _make_lesson(project_root, idx, status))

        result = write_error_memory_ai_send_files(project_root, destination)
        clipboard_text = str(result.get("complete_clipboard_json") or "")
        payload = json.loads(clipboard_text)

        if not clipboard_text.strip().startswith("{"):
            raise AssertionError("Clipboard payload is not JSON text.")
        if clipboard_text.strip() == str(destination):
            raise AssertionError("Clipboard payload is still the destination folder path.")
        if payload.get("artifact_type") != "error_memory_ai_clipboard_export":
            raise AssertionError("Unexpected complete export artifact type.")
        if payload.get("lesson_count_exported") != 15:
            raise AssertionError("Complete clipboard export must include all lessons, including inactive/draft lessons.")
        if result.get("complete_json_lesson_count") != 15:
            raise AssertionError("Result lesson count must include all complete JSON lessons.")
        complete_path = Path(str(result.get("complete_json", "")))
        if not complete_path.exists():
            raise AssertionError("Backup complete JSON export file was not written.")
        if json.loads(complete_path.read_text(encoding="utf-8")) != payload:
            raise AssertionError("Backup complete JSON export does not match clipboard payload.")

        compact_payload = json.loads(Path(str(result["compact_json"])).read_text(encoding="utf-8"))
        compact_lessons = compact_payload.get("lessons", [])
        if len(compact_lessons) != 10:
            raise AssertionError("Compact export should remain capped at 10 lessons.")

        _assert_gui_handler_cannot_copy_destination_path()

        print("VALIDATION OK: error-memory-export-clipboard-complete-json-v2")
        print("ERROR_MEMORY_EXPORT_CLIPBOARD: complete JSON copied")
        print("ERROR_MEMORY_EXPORT_NO_PATH_CLIPBOARD: enforced")
        print("ERROR_MEMORY_EXPORT_COUNT: all lessons included")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
