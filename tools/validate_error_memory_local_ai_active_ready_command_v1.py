#!/usr/bin/env python3
"""Validate Error Memory local-AI active-ready command normalization."""
from __future__ import annotations

import argparse
import importlib
import json
import py_compile
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

FEATURE_ID = "error-memory-local-ai-active-ready-command-v1"
TOUCHED = (
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_lesson_payloads.py",
    "tools/validate_error_memory_local_ai_active_ready_command_v1.py",
)


def _lesson(command: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": "lesson-local-ai-forward-slash-fixture-v1",
        "status": "draft",
        "superseded_by": "",
        "operation_phase": "validation",
        "created_at_utc": "2026-07-20T03:30:00Z",
        "updated_at_utc": "2026-07-20T03:30:00Z",
        "source_patch_zip": "fixture.zip",
        "raw_error_text": "Memorize Error rejected a local-AI corrected lesson command.",
        "raw_error_snapshot_scrubbed": "Synthetic validator fixture with no secrets.",
        "symptom": "The preview looked corrected but active-ready validation rejected its command.",
        "root_cause": "Two intake paths did not share the same regression command normalizer.",
        "wrong_assumption": "Assumed every canonical lesson JSON path used AI response normalization.",
        "correct_fix": "Use the canonical command normalizer in model response and Memorize parsing paths.",
        "do_not_repeat_rule": "Never let local-AI preview validation and Memorize parsing use different command contracts.",
        "long_term_prevention": "Run service-level retry and Memorize reparse regression tests.",
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["Synthetic paths only; no credentials or project source content."],
        },
        "exception": {
            "type": "ErrorMemoryLocalAICommandNormalizationMismatch",
            "phase": "validation",
            "relative_file_path": "kanda_reasoner_app/error_memory_gui/_lesson_payloads.py",
            "function_or_test_name": "lesson_from_formatted_text",
            "message_normalized": "regression_check.command must use forward slashes",
            "stacktrace_scrubbed": "No traceback; deterministic active-ready rejection.",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["local AI", "regression_check.command", "Memorize Error"],
            "fingerprint_hash": "error_memory_local_ai_command_normalization_mismatch_v1",
        },
        "prevention_triggers": [
            "local AI returns a Windows path",
            "Memorize Error rejects forward-slash contract",
        ],
        "regression_check": {
            "type": "validation_command",
            "command": command,
            "expected_marker": "VALIDATION OK: error-memory-local-ai-active-ready-command-v1",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run the focused local-AI command validator and require all PASS markers.",
        "validation_evidence": [
            "VALIDATION OK: error-memory-local-ai-active-ready-command-v1",
            "STATUS: IN_SYNC",
        ],
        "install_command_summary": "Install the focused Error Memory local-AI correction patch.",
        "notes": "Synthetic validation fixture; human Memorize Error remains explicit.",
    }


def _block(lesson: dict[str, Any]) -> str:
    return (
        "KANDA_ERROR_LESSON_JSON_BEGIN\n"
        + json.dumps(lesson, ensure_ascii=True, indent=2, sort_keys=True)
        + "\nKANDA_ERROR_LESSON_JSON_END"
    )


def _reload_project_modules(root: Path) -> dict[str, Any]:
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    names = (
        "kanda_reasoner_app.error_memory_gui._ai_prompt_builder",
        "kanda_reasoner_app.error_memory_gui._ai_response_validator",
        "kanda_reasoner_app.error_memory_gui._lesson_payloads",
        "kanda_reasoner_app.error_memory_gui._ai_corrector_service",
        "kanda_reasoner_app.error_memory.models",
    )
    for name in names:
        sys.modules.pop(name, None)
    return {name: importlib.import_module(name) for name in names}


def validate(root: Path) -> None:
    for rel in TOUCHED:
        path = root / rel
        if not path.is_file():
            raise RuntimeError("Touched file missing: " + rel)
        py_compile.compile(str(path), doraise=True)
    print("TOUCHED_PYTHON_COMPILE: PASS")

    prompt_source = (root / TOUCHED[0]).read_text(encoding="utf-8")
    response_source = (root / TOUCHED[1]).read_text(encoding="utf-8")
    lesson_source = (root / TOUCHED[2]).read_text(encoding="utf-8")
    if "E:/kanda_reasoner" not in prompt_source or "will trigger a retry" not in prompt_source:
        raise RuntimeError("Local-AI prompt does not state the concrete forward-slash retry contract.")
    if "_normalize_regression_check_for_error_memory_json" not in response_source:
        raise RuntimeError("AI response parser does not use the canonical command normalizer.")
    if "_validate_regression_check_contract(payload)" not in response_source:
        raise RuntimeError("AI response parser does not enforce the Memorize regression contract.")
    if "_normalize_regression_check_for_error_memory_json" not in lesson_source:
        raise RuntimeError("Memorize lesson parser does not use the canonical command normalizer.")
    print("LOCAL_AI_FORWARD_SLASH_PROMPT_CONTRACT: PASS")
    print("SHARED_REGRESSION_COMMAND_NORMALIZER: PASS")

    modules = _reload_project_modules(root)
    prompt = modules["kanda_reasoner_app.error_memory_gui._ai_prompt_builder"]
    response = modules["kanda_reasoner_app.error_memory_gui._ai_response_validator"]
    payloads = modules["kanda_reasoner_app.error_memory_gui._lesson_payloads"]
    service = modules["kanda_reasoner_app.error_memory_gui._ai_corrector_service"]
    models = modules["kanda_reasoner_app.error_memory.models"]

    messages = prompt.build_error_memory_correction_messages(
        intake_text="fixture",
        editor_text="",
        project_root=root,
    )
    combined_prompt = "\n".join(str(item.get("content", "")) for item in messages)
    if "E:/kanda_reasoner" not in combined_prompt or "trigger a retry" not in combined_prompt:
        raise RuntimeError("Built local-AI prompt lost the forward-slash retry contract.")

    safe_backslash = _lesson(r"python tools/validate_fixture.py --root E:\kanda_reasoner")
    normalized = response.parse_one_lesson_block(_block(safe_backslash))
    normalized_command = normalized.lesson["regression_check"]["command"]
    if normalized_command != "python tools/validate_fixture.py --root E:/kanda_reasoner":
        raise RuntimeError("AI response command was not normalized: " + repr(normalized_command))
    command_failures = [
        item
        for item in models.active_ready_missing_reasons(dict(normalized.lesson))
        if item.startswith("regression_check")
    ]
    if command_failures:
        raise RuntimeError("Normalized local-AI response remains invalid: " + "; ".join(command_failures))
    print("LOCAL_AI_RESPONSE_COMMAND_NORMALIZED: PASS")
    print("LOCAL_AI_ACTIVE_READY_COMMAND_CONTRACT: PASS")

    canonical_json = json.dumps(safe_backslash, ensure_ascii=False, indent=2, sort_keys=True)
    reparsed = payloads.lesson_from_formatted_text(
        canonical_json,
        selected_project_root=root,
    )
    reparsed_command = reparsed["regression_check"]["command"]
    if reparsed_command != "python tools/validate_fixture.py --root E:/kanda_reasoner":
        raise RuntimeError("Memorize parsing did not normalize canonical JSON: " + repr(reparsed_command))
    if any(
        item.startswith("regression_check")
        for item in models.active_ready_missing_reasons(dict(reparsed))
    ):
        raise RuntimeError("Memorize parser still rejects the normalized command.")
    print("LOCAL_AI_MEMORIZE_PARSE_NORMALIZED: PASS")

    control_command = "python E:\temp/validate_fixture.py"
    if "\t" not in control_command:
        raise RuntimeError("Validator fixture did not contain the intended control character.")
    bad_lesson = _lesson(control_command)
    try:
        response.parse_one_lesson_block(_block(bad_lesson))
    except response.AIResponseValidationError as exc:
        if "regression_check.command contains a control character" not in str(exc):
            raise RuntimeError("Unexpected invalid-command error: " + str(exc)) from exc
    else:
        raise RuntimeError("Control-character command was accepted instead of triggering retry.")
    print("LOCAL_AI_INVALID_COMMAND_REJECTED_FOR_RETRY: PASS")

    good_lesson = _lesson("python tools/validate_fixture.py --root E:/kanda_reasoner")
    original_candidates = service.get_local_ai_model_candidates
    original_request = service._request_model
    original_chat = service.chat_with_local_model
    original_recovery = service.recover_validation_evidence
    try:
        service.get_local_ai_model_candidates = lambda _selection="": ["fake-local-model"]
        service._request_model = lambda _messages, model_name="": (_block(bad_lesson), "fake-local-model")
        service.chat_with_local_model = lambda *_args, **_kwargs: (_block(good_lesson), "fake-local-model")
        service.recover_validation_evidence = lambda **_kwargs: list(good_lesson["validation_evidence"])
        result = service.correct_error_memory_lesson_with_local_ai(
            intake_text=_block(safe_backslash),
            editor_text=canonical_json,
            project_root=root,
            model_selection="fake-local-model",
        )
    finally:
        service.get_local_ai_model_candidates = original_candidates
        service._request_model = original_request
        service.chat_with_local_model = original_chat
        service.recover_validation_evidence = original_recovery

    if not result.ok or result.lesson_block is None:
        raise RuntimeError("Local-AI service retry did not recover: " + result.message)
    if "Retried after validation feedback" not in result.message:
        raise RuntimeError("Local-AI service did not report deterministic retry.")
    final_command = result.lesson_block.lesson["regression_check"]["command"]
    if final_command != "python tools/validate_fixture.py --root E:/kanda_reasoner":
        raise RuntimeError("Recovered local-AI result command is invalid: " + repr(final_command))
    final_reparsed = payloads.lesson_from_formatted_text(
        result.lesson_block.formatted_text,
        selected_project_root=root,
    )
    final_failures = [
        item
        for item in models.active_ready_missing_reasons(dict(final_reparsed))
        if item.startswith("regression_check")
    ]
    if final_failures:
        raise RuntimeError("End-to-end result fails Memorize contract: " + "; ".join(final_failures))
    print("LOCAL_AI_INVALID_COMMAND_RETRY: PASS")
    print("LOCAL_AI_CORRECTION_END_TO_END: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    try:
        validate(Path(args.root).expanduser().resolve())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(type(exc).__name__ + ": " + str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
