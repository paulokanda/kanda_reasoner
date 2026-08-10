# project-path: tools/validate_error_memory_local_ai_corrector_retry_v6.py
"""Validate Error Memory local AI corrector retry v6 behavior."""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOUCHED = [
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "tools/validate_error_memory_local_ai_corrector_retry_v6.py",
]


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def _compile_touched() -> None:
    for relative_path in TOUCHED:
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def _assert_line_counts() -> None:
    for relative_path in TOUCHED:
        line_count = len(_read(relative_path).splitlines())
        if line_count > 500:
            raise AssertionError(relative_path + " exceeds 500 physical lines")


def _load_validator_module() -> Any:
    path = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py"
    spec = importlib.util.spec_from_file_location("em_ai_response_validator_v6", path)
    if spec is None or spec.loader is None:
        raise AssertionError("Could not load _ai_response_validator.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _lesson_with_blank_exception() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": "lesson-pending-delete-after-daily-work-bridge-enforcement-v1",
        "status": "draft",
        "superseded_by": "",
        "operation_phase": "pending_edit",
        "created_at_utc": "2026-07-02T00:20:34Z",
        "updated_at_utc": "2026-07-02T00:20:34Z",
        "source_patch_zip": "",
        "raw_error_text": "The AI risked forgetting root-cleanliness rules for install, temp, correction, and patch files.",
        "raw_error_snapshot_scrubbed": "USER-REPORTED ISSUE\nSandbox validation passed with VALIDATION OK: delete-after-daily-work-bridge-enforcement-v1.",
        "symptom": "The AI risked forgetting root-cleanliness rules for patch deliveries.",
        "root_cause": "Lack of consistent enforcement of root-cleanliness rules.",
        "wrong_assumption": "Assuming existing canon would enforce the rule without explicit checks.",
        "correct_fix": "Enforce root-cleanliness rules in the patch delivery contract and response validator.",
        "do_not_repeat_rule": "Review all patch delivery processes for root-cleanliness containment.",
        "long_term_prevention": "Add validation coverage for root-cleanliness rules.",
        "redaction": {"applied": True, "export_safe": True, "rules": ["No secrets included."]},
        "exception": {
            "type": "",
            "phase": "",
            "relative_file_path": "",
            "function_or_test_name": "",
            "message_normalized": "",
            "stacktrace_scrubbed": "",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["patch_delivery_rules", "root_cleanliness"],
            "fingerprint_hash": "delete-after-daily-work-bridge-enforcement-v1",
        },
        "prevention_triggers": ["root cleanliness"],
        "regression_check": {"type": "not_available"},
        "validation_command_summary": "",
        "validation_evidence": ["No successful validation evidence was provided in the input; keep status draft."],
        "install_command_summary": "",
        "notes": "",
    }


def _validate_blank_exception_repair() -> None:
    module = _load_validator_module()
    block_text = module.format_lesson_block(_lesson_with_blank_exception())
    result = module.parse_one_lesson_block(block_text)
    exception = result.lesson.get("exception")
    if not isinstance(exception, dict):
        raise AssertionError("exception was not repaired as an object")
    required = [
        "type",
        "phase",
        "relative_file_path",
        "function_or_test_name",
        "message_normalized",
        "stacktrace_scrubbed",
    ]
    missing = [key for key in required if not str(exception.get(key) or "").strip()]
    if missing:
        raise AssertionError("exception blank fields were not repaired: " + ", ".join(missing))
    if result.lesson.get("status") != "draft":
        raise AssertionError("blank exception repair must keep status draft")


def _validate_memorize_saves_draft_path() -> None:
    text = _read("kanda_reasoner_app/error_memory_gui/_memorize_flow.py")
    marker = "def memorize_error_from_text_window"
    body = text[text.index(marker):]
    if "_show_active_ready_failure_copy_window" in body:
        raise AssertionError("Memorize Error still routes incomplete lessons to the correction popup")
    if "_save_draft_lesson_from_partial" not in body:
        raise AssertionError("Memorize Error does not save incomplete lessons as draft")
    if "Memorized Error lesson as draft" not in body:
        raise AssertionError("Memorize Error draft save message is missing")


def _validate_copy_close_scope() -> None:
    text = _read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    if "_show_copyable_error(" not in text:
        raise AssertionError("copyable error helper is missing")
    if "_show_success(tab, \"Error Memory AI correction\", result.message)" not in text:
        raise AssertionError("AI correction success path should use normal success notification")
    success_tail = text.rsplit("apply_corrected_lesson_to_work_windows", 1)[-1]
    if "_show_copyable_error" in success_tail:
        raise AssertionError("AI correction success path still uses the error copy-close window")


def main() -> int:
    _compile_touched()
    _assert_line_counts()
    _validate_blank_exception_repair()
    _validate_memorize_saves_draft_path()
    _validate_copy_close_scope()
    print("VALIDATION OK: error-memory-local-ai-corrector-retry-v6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
