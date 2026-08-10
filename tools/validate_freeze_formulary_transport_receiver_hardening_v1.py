# project-path: tools/validate_freeze_formulary_transport_receiver_hardening_v1.py
"""Validate transport-safe manual Freeze formulary exchange and parsing."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "freeze-formulary-transport-receiver-hardening-v1"
PARSER_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "freeze_after_update_gui"
    / "_ai_formulary_response_parser.py"
)
REPAIR_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "freeze_after_update_gui"
    / "_ai_formulary_transport_repair.py"
)
RUNTIME_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "freeze_after_update_gui"
    / "_local_freeze_dialog_runtime.py"
)
EXPORTS_PATH = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "freeze_after_update_gui"
    / "_freeze_memory_exports.py"
)
VALIDATOR_PATH = Path(__file__).resolve()
FORM_FIELDS = (
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
)


def _baseline() -> dict[str, str]:
    return {field: "" for field in FORM_FIELDS}


def _parser():
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import (
        parse_ai_formulary_response,
    )

    return parse_ai_formulary_response


def _marker_block(payload_text: str, *, fenced: bool = False) -> str:
    if fenced:
        payload_text = "```json\n" + payload_text + "\n```"
    return (
        "KANDA_FREEZE_FORM_JSON_BEGIN\n"
        + payload_text
        + "\nKANDA_FREEZE_FORM_JSON_END"
    )


def _assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def _assert_contains(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        raise AssertionError(f"Missing {label}: {fragment}")


def _validate_fenced_arrays() -> None:
    parse = _parser()
    payload = {
        "feature_title": "Transport safe",
        "validated_files": ["a.py", "b.py"],
        "protected_paths": ["project_error_memory/", "project_freeze_after_update/"],
        "validation_evidence_summary": [
            "ZIP CONTRACT: PASS",
            "VALIDATION EVIDENCE: E:\\kanda_reasoner_show_project_to_AI\\project_validation_evidence\\feature.txt",
            "STATUS: IN_SYNC",
        ],
    }
    response = _marker_block(json.dumps(payload, ensure_ascii=False, indent=2), fenced=True)
    parsed = parse(response, _baseline())
    _assert_equal(parsed.inputs["validated_files"], "a.py\nb.py", "array normalization")
    _assert_equal(
        parsed.inputs["validation_evidence_summary"].splitlines(),
        payload["validation_evidence_summary"],
        "fenced validation lines",
    )
    print("FREEZE_FORMULARY_MARKER_FENCED_JSON: PASS")
    print("FREEZE_FORMULARY_MULTILINE_ARRAYS: PASS")


def _validate_markdown_collapsed_paths() -> None:
    parse = _parser()
    invalid_escape_payload = (
        '{"feature_title":"Transport repair",'
        '"validation_evidence_summary":"VALIDATION EVIDENCE: '
        r'E:\kanda_reasoner_show_project_to_AI\project_validation_evidence\feature.txt"}'
    )
    parsed = parse(_marker_block(invalid_escape_payload), _baseline())
    expected = (
        "VALIDATION EVIDENCE: "
        r"E:\kanda_reasoner_show_project_to_AI\project_validation_evidence\feature.txt"
    )
    _assert_equal(
        parsed.inputs["validation_evidence_summary"],
        expected,
        "invalid Windows escape repair",
    )
    print("WINDOWS_INVALID_ESCAPE_REPAIRED: PASS")

    valid_escape_damage_payload = (
        '{"feature_title":"Control repair",'
        '"validation_evidence_summary":"VALIDATION EVIDENCE: '
        r'E:\new\test\feature.txt"}'
    )
    parsed = parse(_marker_block(valid_escape_damage_payload), _baseline())
    expected = "VALIDATION EVIDENCE: " + r"E:\new\test\feature.txt"
    _assert_equal(
        parsed.inputs["validation_evidence_summary"],
        expected,
        "valid-escape path corruption repair",
    )
    if any(char in parsed.inputs["validation_evidence_summary"] for char in "\n\t\r\b\f"):
        raise AssertionError("Windows path retained decoded control characters")
    print("WINDOWS_VALID_ESCAPE_CORRUPTION_BLOCKED: PASS")


def _validate_legacy_repairs_and_failure_message() -> None:
    parse = _parser()
    raw_controls = (
        '{"feature_title":"Raw controls","notes":"first line\nsecond line\tvalue"}'
    )
    parsed = parse(raw_controls, _baseline())
    _assert_equal(parsed.inputs["notes"], "first line\nsecond line\tvalue", "control repair")
    print("RAW_CONTROL_CHARACTER_REPAIR: PASS")

    try:
        parse("This answer has no JSON form.", _baseline())
    except ValueError as exc:
        if "\\u005C" not in str(exc):
            raise AssertionError("transport-safe Windows guidance missing from parse error")
    else:
        raise AssertionError("non-JSON response did not fail closed")
    print("FREEZE_FORMULARY_PARSE_FAILURE_GUIDANCE: PASS")


def _validate_prompt_contracts() -> None:
    runtime_source = RUNTIME_PATH.read_text(encoding="utf-8")
    exports_source = EXPORTS_PATH.read_text(encoding="utf-8")
    parser_source = PARSER_PATH.read_text(encoding="utf-8")
    ast.parse(runtime_source, filename=str(RUNTIME_PATH))
    ast.parse(exports_source, filename=str(EXPORTS_PATH))
    ast.parse(parser_source, filename=str(PARSER_PATH))

    for fragment in (
        "_manual_ai_transport_payload",
        '"```json\\n"',
        "as JSON arrays",
        "inside the fenced code block",
        "doubled backslashes or \\\\u005C",
    ):
        _assert_contains(runtime_source, fragment, "manual Copy Formulary transport contract")
    print("FREEZE_FORMULARY_COPY_PROMPT_TRANSPORT_SAFE: PASS")

    for fragment in (
        "one fenced json code block",
        "Use JSON arrays for validated_files",
        "KANDA_FREEZE_FORM_JSON_BEGIN\n```json",
        "doubled backslashes or \\\\u005C",
        "KANDA_FREEZE_FORM_JSON_END",
    ):
        _assert_contains(exports_source, fragment, "Freeze blueprint transport contract")
    print("FREEZE_FORM_BLUEPRINT_TRANSPORT_SAFE: PASS")

    for fragment in (
        "Preview is read-only",
        "Confirm and Write ",
        "remains human",
        "write_confirmed_freeze_entry(",
        "confirmation=True",
    ):
        _assert_contains(runtime_source, fragment, "human Freeze boundary")
    print("PREVIEW_CONFIRM_HUMAN_BOUNDARY_PRESERVED: PASS")


def _validate_module_sizes() -> None:
    for path in (PARSER_PATH, REPAIR_PATH, RUNTIME_PATH, EXPORTS_PATH, VALIDATOR_PATH):
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if not 101 <= line_count <= 499:
            raise AssertionError(
                f"TOUCHED_SOURCE_MODULE_SIZE_OUT_OF_RANGE: {path.relative_to(PROJECT_ROOT)}={line_count}"
            )
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")


def main() -> int:
    _validate_fenced_arrays()
    _validate_markdown_collapsed_paths()
    _validate_legacy_repairs_and_failure_message()
    _validate_prompt_contracts()
    _validate_module_sizes()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
