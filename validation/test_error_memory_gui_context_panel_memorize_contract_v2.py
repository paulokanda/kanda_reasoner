"""Validation for Error Memory GUI context-panel placement and memorize contract v2."""

from __future__ import annotations

import json
from pathlib import Path

from kanda_reasoner_app.error_memory.intake import (
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    build_lesson_from_ai_form,
    parse_error_lesson_ai_response,
)
from kanda_reasoner_app.error_memory.models import active_ready


FEATURE_ID = "error-memory-gui-context-panel-memorize-contract-v2"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _source() -> str:
    return Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py").read_text(encoding="utf-8-sig")


def _receive_block(status: str = "active") -> str:
    payload = {
        "status": status,
        "raw_error_text": "validation_evidence =\nSyntaxError: invalid syntax\nFREEZE INTAKE PREP OK",
        "operation_phase": "install",
        "symptom": "Generated freeze-intake helper failed with SyntaxError while wrapper printed success.",
        "root_cause": "The helper was generated with incomplete validation evidence assignment and the wrapper did not stop on helper failure.",
        "wrong_assumption": "The wrapper assumed the helper succeeded without checking compile and process exit status.",
        "correct_fix": "Write multiline evidence through a JSON payload file and check helper compile and exit code before printing success.",
        "long_term_prevention": "Generated helper workflows must verify compile, exit code, and expected artifact before success footers.",
        "do_not_repeat_rule": "Do not print success for generated helper workflows unless the helper compiled, exited with code 0, and verified the expected artifact.",
        "prevention_triggers": ["validation_evidence =", "SyntaxError: invalid syntax", "missing LASTEXITCODE check"],
        "validation_evidence": [
            "VALIDATION OK: error-memory-receive-formulary-freeze-intake-syntaxerror-guard-v2",
            "STATUS: RECEIVE_BLOCK_READY_FOR_CURRENT_TAB",
        ],
        "regression_check": {
            "type": "validation_command",
            "command": "python validation\\test_error_memory_gui_context_panel_memorize_contract_v2.py",
            "expected_marker": "VALIDATION OK: error-memory-gui-context-panel-memorize-contract-v2",
            "required_before_freeze": False,
        },
        "source_patch_zip": "kanda_error_memory_gui_context_panel_memo_contract_v2_patch.zip",
        "install_command_summary": "Installer stages ZIP from project drive root and extracts only from the staged ZIP.",
        "validation_command_summary": "Validation checks GUI source order and formatted-only memorize contract.",
        "notes": "Formatted active-ready lesson used to validate Memorize Error contract.",
    }
    return ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps(payload, indent=2) + "\n" + ERROR_LESSON_JSON_END + "\n"


def test_project_root_panel_is_above_intake() -> None:
    source = _source()
    context_index = source.index('self.loaded_project_context_label = QLabel("Loaded project context")')
    intake_index = source.index('QGroupBox("AI-assisted error lesson intake")')
    right_index = source.index("# RIGHT COLUMN")
    _assert(context_index < intake_index < right_index, "Project Root panel must be above AI-assisted intake in the left column")
    _assert('QGroupBox("Project context")' not in source, "Project context group must remain dismantled")
    _assert('QGroupBox("Project Root")' not in source, "Project Root must not be wrapped in a group box")
    _assert('context_title = QLabel("Project Root:")' in source, "Project Root label missing")
    _assert('self.project_root_value_label = QLabel(str(self._project_root))' in source, "Project root path field missing")
    _assert('self.search_project_button = QPushButton("Search")' in source, "Search button missing")
    _assert('self.open_memory_button = QPushButton("Open EM Folder")' in source, "Open EM Folder button missing")
    _assert('self.open_second_prompt_button = QPushButton("Open Second Prompt Files")' in source, "Open Second Prompt Files button missing")
    _assert('self.copy_memory_path_button = QPushButton("Get path to EM Folder")' in source, "Get path to EM Folder button missing")
    _assert('self.copy_second_prompt_path_button = QPushButton("Get path to Second Prompt Files")' in source, "Get path to Second Prompt Files button missing")
    _assert('left_layout.addWidget(context_panel, 0)' in source, "Project Root panel should use compact top placement")
    _assert('left_layout.addWidget(intake_box, 2)' in source, "Intake group should remain below project root panel")


def test_manual_operation_phase_and_raw_draft_remain_removed() -> None:
    source = _source()
    _assert("QComboBox" not in source, "manual operation phase combo returned")
    _assert("phase_combo" not in source, "phase combo references returned")
    _assert("Save Draft from Raw Error" not in source, "Save Draft from Raw Error returned")
    _assert("_save_raw_draft" not in source, "raw draft method returned")
    _assert("fallback_operation_phase=\"unknown\"" in source, "Operation phase should be metadata from AI JSON or inference, not manual chooser")


def test_memorize_error_is_formatted_only_by_source_contract() -> None:
    source = _source()
    _assert('self.memorize_error_button = QPushButton("Memorize Error")' in source, "Memorize Error button missing")
    _assert("_memorize_error_from_text_window" in source, "Memorize Error handler missing")
    _assert("_text_has_formatted_lesson_payload" in source, "formatted lesson gate missing")
    _assert("Memorize Error accepts only a KANDA_ERROR_LESSON_JSON block or one valid lesson JSON object" in source, "formatted-only warning missing")
    _assert('lesson.get("status") != "active" or not active_ready(lesson)' in source, "Memorize Error must reject non-active-ready lessons")
    _assert("The formatted lesson was parsed, but it is not active-ready. It was not memorized." in source, "not-active-ready rejection message missing")


def test_current_intake_builds_active_ready_formatted_lesson() -> None:
    form = parse_error_lesson_ai_response(_receive_block())
    lesson = build_lesson_from_ai_form(
        selected_project_root=Path("E:/kanda_reasoner"),
        form_inputs=form,
        fallback_raw_error_text="",
        fallback_operation_phase="unknown",
    )
    _assert(lesson.get("status") == "active", "formatted lesson should remain active")
    _assert(lesson.get("operation_phase") == "install", "operation phase should come from JSON metadata")
    _assert(active_ready(lesson), "formatted lesson should be active-ready")


def test_current_intake_downgrades_incomplete_json_to_draft() -> None:
    incomplete = ERROR_LESSON_JSON_BEGIN + "\n" + json.dumps({"status": "active", "symptom": "Only symptom"}) + "\n" + ERROR_LESSON_JSON_END
    form = parse_error_lesson_ai_response(incomplete)
    lesson = build_lesson_from_ai_form(
        selected_project_root=Path("E:/kanda_reasoner"),
        form_inputs=form,
        fallback_raw_error_text="",
        fallback_operation_phase="unknown",
    )
    _assert(lesson.get("status") == "draft", "incomplete formatted JSON must not become active")
    _assert(not active_ready(lesson), "incomplete formatted JSON must not be active-ready")


def main() -> None:
    test_project_root_panel_is_above_intake()
    test_manual_operation_phase_and_raw_draft_remain_removed()
    test_memorize_error_is_formatted_only_by_source_contract()
    test_current_intake_builds_active_ready_formatted_lesson()
    test_current_intake_downgrades_incomplete_json_to_draft()
    print("VALIDATION OK: error-memory-gui-context-panel-memorize-contract-v2")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
