"""Validate Error Memory button uses complete JSON-only export path."""

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
    write_complete_error_memory_ai_clipboard_export,
    write_error_memory_ai_send_files,
)
from kanda_reasoner_app.error_memory.models import build_lesson  # noqa: E402
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
            "command": "python validation\test_error_memory_export_clipboard_complete_json_v3.py",
            "expected_marker": "VALIDATION OK: error-memory-export-clipboard-complete-json-v3",
            "required_before_freeze": True,
        },
        status=status,
    )


def _method_block(source: str, name: str) -> str:
    marker = "    def " + name + "("
    start = source.index(marker)
    next_start = source.find("\n    def ", start + 1)
    if next_start == -1:
        return source[start:]
    return source[start:next_start]


def _assert_gui_button_has_no_second_prompt_export_path() -> None:
    tab_path = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    source = tab_path.read_text(encoding="utf-8")
    export_block = _method_block(source, "_export_for_ai")
    helper_block = _method_block(source, "_copy_complete_error_memory_json_to_clipboard")
    if "write_error_memory_ai_send_files" in export_block:
        raise AssertionError("EM export button still calls the second-prompt export writer.")
    if "resolve_second_prompt_files_root" in export_block:
        raise AssertionError("EM export button still resolves second_prompt_files.")
    if "destination_folder" in export_block or "setText(destination" in export_block:
        raise AssertionError("EM export button still exposes a destination-folder clipboard path.")
    if "write_complete_error_memory_ai_clipboard_export" not in export_block:
        raise AssertionError("EM export button does not use the complete JSON-only writer.")
    if "received_preview_edit.setPlainText(clipboard_text)" not in export_block:
        raise AssertionError("EM export button must show JSON in Error Editor as fallback copy source.")
    if export_block.count("_copy_complete_error_memory_json_to_clipboard(clipboard_text)") < 2:
        raise AssertionError("EM export button must copy JSON before and after the information dialog.")
    if "QTimer.singleShot" not in export_block:
        raise AssertionError("EM export button must schedule a delayed recopy to beat late path overwrites.")
    if "Complete Error Memory export clipboard payload looks like a path" not in helper_block:
        raise AssertionError("JSON clipboard helper must reject path-looking payloads.")
    if "Copy Complete Error Memory JSON for AI" not in source:
        raise AssertionError("Button label must be unmistakably JSON-only.")


def main() -> None:
    tmp_dir = Path(tempfile.mkdtemp(prefix="kanda_em_export_v3_"))
    try:
        project_root = tmp_dir / "demo_project"
        project_root.mkdir(parents=True)
        second_prompt_destination = tmp_dir / "demo_project_show_project_to_AI" / "second_prompt_files"

        for idx in range(15):
            status = "active" if idx != 13 else "draft"
            save_lesson(project_root, _make_lesson(project_root, idx, status))

        complete_result = write_complete_error_memory_ai_clipboard_export(project_root, include_inactive=True)
        clipboard_text = str(complete_result.get("complete_clipboard_json") or "")
        payload = json.loads(clipboard_text)

        if not clipboard_text.strip().startswith("{"):
            raise AssertionError("Clipboard payload is not JSON text.")
        if clipboard_text.strip() == str(second_prompt_destination):
            raise AssertionError("Clipboard payload is still the destination folder path.")
        if "second_prompt_files" in clipboard_text[:200]:
            raise AssertionError("Clipboard payload begins like a path-oriented export, not complete JSON.")
        if complete_result.get("clipboard_contract") != "complete_json_only":
            raise AssertionError("Complete export writer must declare complete_json_only contract.")
        if "destination_folder" in complete_result:
            raise AssertionError("Complete export writer must not return destination_folder.")
        if payload.get("artifact_type") != "error_memory_ai_clipboard_export":
            raise AssertionError("Unexpected complete export artifact type.")
        if payload.get("lesson_count_exported") != 15:
            raise AssertionError("Complete clipboard export must include all lessons, including inactive/draft lessons.")
        complete_path = Path(str(complete_result.get("complete_json", "")))
        if not complete_path.exists():
            raise AssertionError("Backup complete JSON export file was not written.")
        if json.loads(complete_path.read_text(encoding="utf-8")) != payload:
            raise AssertionError("Backup complete JSON export does not match clipboard payload.")

        compact_result = write_error_memory_ai_send_files(project_root, second_prompt_destination)
        compact_payload = json.loads(Path(str(compact_result["compact_json"])).read_text(encoding="utf-8"))
        if len(compact_payload.get("lessons", [])) != 10:
            raise AssertionError("Compact second-prompt export should remain capped at 10 lessons.")

        _assert_gui_button_has_no_second_prompt_export_path()

        print("VALIDATION OK: error-memory-export-clipboard-complete-json-v3")
        print("ERROR_MEMORY_EXPORT_CLIPBOARD: complete JSON copied")
        print("ERROR_MEMORY_EXPORT_NO_SECOND_PROMPT_PATH: enforced")
        print("ERROR_MEMORY_EXPORT_COUNT: all lessons included")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
