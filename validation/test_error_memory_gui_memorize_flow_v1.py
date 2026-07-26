"""Validation for Error Memory GUI memorize/import flow v1."""

from __future__ import annotations

import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from kanda_reasoner_app.error_memory.importer import import_error_memory_file
from kanda_reasoner_app.error_memory.intake import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    build_error_lesson_ai_form_prompt,
    parse_error_lesson_ai_response,
)
from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root
from kanda_reasoner_app.error_memory.store import list_lessons


FEATURE_ID = "error-memory-gui-memorize-formatted-import-flow-v1"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _receive_block() -> str:
    payload = {
        "status": "active",
        "raw_error_text": "validation_evidence =\nSyntaxError: invalid syntax\nFREEZE INTAKE PREP OK",
        "operation_phase": "install",
        "symptom": "Freeze-intake helper failed with SyntaxError but wrapper printed a success message.",
        "root_cause": "The generated helper left validation_evidence empty and the wrapper did not stop on the helper failure.",
        "wrong_assumption": "The wrapper assumed writing and running the helper meant the freeze intake was prepared.",
        "correct_fix": "Write multiline evidence through a JSON payload file and check the helper exit code before printing success.",
        "long_term_prevention": "Generated helper scripts must be compiled and their exit code checked before any OK footer is printed.",
        "do_not_repeat_rule": "Do not print success for generated helper workflows unless the helper compiled, exited with code 0, and verified the expected artifact.",
        "prevention_triggers": ["validation_evidence =", "SyntaxError: invalid syntax", "missing LASTEXITCODE check"],
        "validation_evidence": [
            "VALIDATION OK: error-memory-receive-formulary-freeze-intake-syntaxerror-guard-v2",
            "STATUS: RECEIVE_BLOCK_READY_FOR_CURRENT_TAB",
        ],
        "regression_check": {
            "type": "validation_command",
            "command": "python validation\\test_error_memory_gui_memorize_flow_v1.py",
            "expected_marker": "VALIDATION OK: error-memory-gui-memorize-formatted-import-flow-v1",
            "required_before_freeze": False,
        },
        "source_patch_zip": "kanda_error_memory_gui_memorize_formatted_import_flow_v1_patch.zip",
        "install_command_summary": "Installer stages ZIP from project drive root into delete_after_daily_work and extracts only the staged ZIP.",
        "validation_command_summary": "Validation confirms parser, import, source fragments, and active lesson behavior.",
        "notes": "Receive block intended for current Error Memory tab formatted import/memorize flow.",
    }
    return ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps(payload, indent=2) + "\n" + ERROR_LESSON_JSON_END + "\n"


def test_gui_source_contract() -> None:
    source = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py").read_text(encoding="utf-8-sig")
    _assert("AI-assisted error lesson intake" in source, "missing intake group")
    _assert("Last received lesson Preview" in source, "missing preview group")
    _assert("QComboBox" not in source, "manual operation phase combo still present")
    _assert("phase_combo" not in source, "phase_combo references still present")
    _assert("Save Draft from Raw Error" not in source, "old Save Draft button still present")
    _assert("_save_raw_draft" not in source, "old raw draft method still present")
    _assert("Memorize Error" in source, "new Memorize Error button missing")
    _assert("_memorize_error_from_text_window" in source, "memorize handler missing")
    _assert("Project context" not in source, "old Project context group still present")
    _assert("Project Root:" in source, "Project Root label missing")
    _assert("Open EM Folder" in source, "Open EM Folder button missing")
    _assert("Open Second Prompt Files" in source, "Open Second Prompt Files button missing")
    _assert("Get path to EM Folder" in source, "copy EM path button missing")
    _assert("Get path to Second Prompt Files" in source, "copy second prompt path button missing")
    _assert("_formatted_import_text_for_window" in source, "formatted import text helper missing")
    _assert("raw_error_edit.setPlainText(formatted_text" in source, "import does not populate text window with formatted lesson text")
    _assert("received_preview_edit.setPlainText(json.dumps(imported_lesson" in source, "import does not load canonical lesson into preview")
    _assert("operation_phase=\"unknown\"" in source, "copy/receive fallback should not depend on manual phase combo")


def test_receive_prompt_and_parser_contract() -> None:
    prompt = build_error_lesson_ai_form_prompt(
        selected_project_root=Path("E:/kanda_reasoner"),
        raw_error_text="SyntaxError: invalid syntax",
        operation_phase="unknown",
    )
    _assert("infer it from the evidence" in prompt, "AI prompt does not require operation phase inference")
    form = parse_error_lesson_ai_response(_receive_block())
    _assert(form.get("operation_phase") == "install", "parser did not preserve operation_phase install")
    _assert(form.get("status") == "active", "parser did not preserve active status")
    _assert("validation_evidence =" in form.get("prevention_triggers", []), "parser lost trigger")


def test_import_zip_saves_active_lesson() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "ProjectMemorizeFlowV1"
        project_root.mkdir()
        error_root = resolve_project_error_memory_root(project_root)
        if error_root.exists():
            shutil.rmtree(error_root)
        zip_path = Path(tmp) / "lesson.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("payload/KANDA_ERROR_LESSON_JSON.txt", _receive_block())
        result = import_error_memory_file(project_root, zip_path)
        _assert(result.get("imported_count") == 1, "imported_count should be 1")
        lessons = list_lessons(project_root, include_inactive=True)
        _assert(len(lessons) == 1, "expected one imported lesson")
        lesson = lessons[0]
        _assert(lesson.get("status") == "active", "imported lesson should be active")
        _assert(lesson.get("operation_phase") == "install", "imported lesson operation_phase should be install")
        _assert("validation_evidence =" in lesson.get("prevention_triggers", []), "imported lesson lost prevention trigger")


def main() -> None:
    test_gui_source_contract()
    test_receive_prompt_and_parser_contract()
    test_import_zip_saves_active_lesson()
    print("VALIDATION OK: error-memory-gui-memorize-formatted-import-flow-v1")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
