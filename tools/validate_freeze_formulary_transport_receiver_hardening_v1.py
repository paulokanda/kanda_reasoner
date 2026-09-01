# project-path: tools/validate_freeze_formulary_transport_receiver_hardening_v1.py
"""Validate unified Freeze formulary JSON transport and receiver contracts."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "freeze-formulary-unified-json-transport-v1"
PARSER_PATH = PROJECT_ROOT / "kanda_reasoner_app/freeze_after_update_gui/_ai_formulary_response_parser.py"
EXTERNAL_PATH = PROJECT_ROOT / "kanda_reasoner_app/freeze_after_update_gui/_external_ai_formulary_handoff.py"
LOCAL_PATH = PROJECT_ROOT / "kanda_reasoner_app/freeze_after_update_gui/_local_ai_formulary.py"
WEB_PATH = PROJECT_ROOT / "kanda_reasoner_app/freeze_after_update_gui/_web_ai_formulary.py"
RUNTIME_PATH = PROJECT_ROOT / "kanda_reasoner_app/freeze_after_update_gui/_local_freeze_dialog_runtime.py"
AI_RUNTIME_PATH = PROJECT_ROOT / "kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py"
VALIDATOR_PATH = Path(__file__).resolve()
LIST_FIELDS = (
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
)


def _parser():
    project_root = str(PROJECT_ROOT)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import (
        parse_ai_formulary_response,
    )

    return parse_ai_formulary_response


def _base() -> dict[str, str]:
    return {
        "feature_title": "Unified transport contract",
        "primary_box": "kanda_reasoner_app/freeze_after_update_gui",
        "box_type": "Freeze formulary receiver adapter",
        "validated_files": "a.py\nb.py",
        "generated_files": "",
        "protected_paths": "project_freeze_after_update/frozen_features_memory/",
        "do_not_regress_rules": "Preview remains read-only.",
        "validation_evidence_summary": "VALIDATION OK: unified-v1\nSTATUS: IN_SYNC",
        "known_warnings": "n/a",
        "planned_next_step": "Verify later if this receiver changes.",
        "notes": "Release owner: KANDA_TOOL_RELEASE.",
    }


def _arrays(payload: dict[str, str]) -> dict[str, Any]:
    converted: dict[str, Any] = dict(payload)
    for field in LIST_FIELDS:
        converted[field] = [
            line for line in payload[field].splitlines() if line.strip()
        ]
    return converted


def _marker_block(payload: dict[str, Any]) -> str:
    return (
        "KANDA_FREEZE_FORM_JSON_BEGIN\n```json\n"
        + json.dumps(payload, ensure_ascii=True, indent=2)
        + "\n```\nKANDA_FREEZE_FORM_JSON_END"
    )


def _assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def _assert_contains(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        raise AssertionError(f"Missing {label}: {fragment}")


def _assert_not_contains(text: str, fragment: str, label: str) -> None:
    if fragment in text:
        raise AssertionError(f"Forbidden {label}: {fragment}")


def _validate_canonical_raw_arrays() -> None:
    parse = _parser()
    baseline = _base()
    raw = json.dumps(_arrays(baseline), ensure_ascii=True)
    parsed = parse(raw).inputs
    _assert_equal(parsed, baseline, "canonical raw array transport")
    print("FREEZE_FORMULARY_CANONICAL_RAW_JSON: PASS")
    print("FREEZE_FORMULARY_MULTILINE_ARRAYS: PASS")


def _validate_legacy_inputs() -> None:
    parse = _parser()
    baseline = _base()
    legacy_raw_strings = json.dumps(baseline, ensure_ascii=True)
    _assert_equal(parse(legacy_raw_strings).inputs, baseline, "legacy raw strings")

    legacy_markers = _marker_block(_arrays(baseline))
    _assert_equal(
        parse(legacy_markers, transport="manual_external_ai").inputs,
        baseline,
        "legacy marker input",
    )

    duplicated_marker_words = (
        "The old marker KANDA_FREEZE_FORM_JSON_BEGIN is mentioned here.\n\n"
        + legacy_markers
        + "\n\nThe old marker KANDA_FREEZE_FORM_JSON_END was historical."
    )
    _assert_equal(
        parse(duplicated_marker_words).inputs,
        baseline,
        "duplicate marker text compatibility",
    )
    _assert_equal(
        parse(legacy_markers, transport="local_web_ai").inputs,
        baseline,
        "legacy caller mode ignored",
    )
    _assert_equal(
        parse(legacy_raw_strings, transport="unknown_old_mode").inputs,
        baseline,
        "unknown legacy caller mode ignored",
    )
    print("FREEZE_FORMULARY_LEGACY_MARKER_INPUT_COMPATIBILITY: PASS")
    print("FREEZE_FORMULARY_DUPLICATE_MARKER_ERROR_REMOVED: PASS")
    print("FREEZE_FORMULARY_CALLER_TRANSPORT_MODE_NON_SEMANTIC: PASS")


def _validate_schema_fail_closed() -> None:
    parse = _parser()
    baseline = _base()

    two = json.dumps(_arrays(baseline)) + "\n" + json.dumps(_arrays(baseline))
    try:
        parse(two)
    except ValueError as exc:
        _assert_contains(str(exc), "more than one valid 11-field", "ambiguity gate")
    else:
        raise AssertionError("two valid Freeze objects did not fail closed")

    missing = _arrays(baseline)
    missing.pop("notes")
    try:
        parse(json.dumps(missing))
    except ValueError as exc:
        _assert_contains(str(exc), "missing field(s): notes", "missing-field gate")
    else:
        raise AssertionError("missing field did not fail closed")

    extra = _arrays(baseline)
    extra["unexpected"] = "no"
    try:
        parse(json.dumps(extra))
    except ValueError as exc:
        _assert_contains(str(exc), "unknown field(s): unexpected", "extra-field gate")
    else:
        raise AssertionError("extra field did not fail closed")

    raw = json.dumps(_arrays(baseline), ensure_ascii=True)
    duplicate = raw.replace(
        '"feature_title": "Unified transport contract",',
        '"feature_title": "Unified transport contract", "feature_title": "duplicate",',
        1,
    )
    try:
        parse(duplicate)
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate JSON object key did not fail closed")

    nan_payload = raw.replace('"known_warnings": "n/a"', '"known_warnings": NaN')
    try:
        parse(nan_payload)
    except ValueError:
        pass
    else:
        raise AssertionError("non-standard JSON constant did not fail closed")

    print("FREEZE_FORMULARY_AMBIGUOUS_MULTI_OBJECT_FAIL_CLOSED: PASS")
    print("FREEZE_FORMULARY_FIELD_INVENTORY_FAIL_CLOSED: PASS")
    print("FREEZE_FORMULARY_STRICT_JSON_GATES: PASS")


def _validate_source_contracts() -> None:
    sources = {
        PARSER_PATH: PARSER_PATH.read_text(encoding="utf-8"),
        EXTERNAL_PATH: EXTERNAL_PATH.read_text(encoding="utf-8"),
        LOCAL_PATH: LOCAL_PATH.read_text(encoding="utf-8"),
        WEB_PATH: WEB_PATH.read_text(encoding="utf-8"),
        RUNTIME_PATH: RUNTIME_PATH.read_text(encoding="utf-8"),
        AI_RUNTIME_PATH: AI_RUNTIME_PATH.read_text(encoding="utf-8"),
    }
    for path, source in sources.items():
        ast.parse(source, filename=str(path))

    parser_source = sources[PARSER_PATH]
    external_source = sources[EXTERNAL_PATH]
    local_source = sources[LOCAL_PATH]
    web_source = sources[WEB_PATH]
    runtime_source = sources[RUNTIME_PATH]

    _assert_contains(parser_source, "canonical_formulary_payload", "canonical payload owner")
    _assert_contains(parser_source, "canonical_formulary_json_schema", "canonical schema owner")
    _assert_contains(parser_source, "more than one valid 11-field JSON object", "ambiguity gate")
    _assert_contains(parser_source, "backward compatibility", "legacy caller compatibility")
    _assert_not_contains(parser_source, "Manual Freeze response requires exactly one marker pair", "retired marker-count failure")

    for source, label in ((external_source, "external"), (local_source, "local"), (web_source, "web")):
        _assert_contains(source, "canonical_formulary_payload", label + " canonical producer")
    _assert_contains(external_source, "Do not use marker wrappers", "external raw JSON instruction")
    _assert_not_contains(external_source, "KANDA_FREEZE_FORM_JSON_BEGIN", "external marker producer")
    _assert_contains(local_source, "as JSON arrays of strings", "local array contract")
    _assert_contains(web_source, "canonical_formulary_json_schema", "web shared schema")
    _assert_contains(runtime_source, "Raw JSON is canonical", "manual receive help")

    for fragment in (
        "read-only preview",
        "write_confirmed_freeze_entry(",
        "confirmation=True",
    ):
        _assert_contains(runtime_source, fragment, "human Freeze boundary")

    print("FREEZE_FORMULARY_ONE_CANONICAL_SCHEMA_OWNER: PASS")
    print("FREEZE_FORMULARY_EXTERNAL_LOCAL_WEB_PRODUCER_PARITY: PASS")
    print("PREVIEW_CONFIRM_HUMAN_BOUNDARY_PRESERVED: PASS")


def _validate_module_sizes() -> None:
    for path in (
        PARSER_PATH,
        EXTERNAL_PATH,
        LOCAL_PATH,
        WEB_PATH,
        RUNTIME_PATH,
        AI_RUNTIME_PATH,
        VALIDATOR_PATH,
    ):
        count = len(path.read_text(encoding="utf-8").splitlines())
        if count > 500:
            raise AssertionError(
                "TOUCHED_OR_GOVERNED_MODULE_SIZE_EXCEEDS_500: "
                + path.relative_to(PROJECT_ROOT).as_posix()
                + "="
                + str(count)
            )
    print("FREEZE_FORMULARY_GOVERNED_MODULES_MAX500: PASS")


def main() -> int:
    _validate_canonical_raw_arrays()
    _validate_legacy_inputs()
    _validate_schema_fail_closed()
    _validate_source_contracts()
    _validate_module_sizes()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
