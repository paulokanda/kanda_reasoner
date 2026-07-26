# project-path: tools/validate_error_memory_local_ai_corrector_retry_v5.py
"""Focused validation for Error Memory local AI corrector retry v5."""

from __future__ import annotations

import ast
import importlib.util
import json
import py_compile
import sys
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]

TOUCHED_FILES = [
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_ai_corrector_service.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/templates/floating_windows/__init__.py",
    "kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py",
    "tools/validate_error_memory_local_ai_corrector_retry_v5.py",
]

BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
END = "KANDA_ERROR_LESSON_JSON_END"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(rel_path: str) -> str:
    return (PROJECT_ROOT / rel_path).read_text(encoding="utf-8")


def _line_count(rel_path: str) -> int:
    return len(_read(rel_path).splitlines())


def _load_validator_module():
    path = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py"
    spec = importlib.util.spec_from_file_location("em_ai_response_validator_v5", path)
    _assert(spec is not None and spec.loader is not None, "Could not create import spec.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def _lesson_base() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "project_slug": "kanda_reasoner",
        "lesson_id": "lesson-ai-forget-root-cleanliness-rules-v2",
        "status": "draft",
        "superseded_by": "",
        "operation_phase": "pending_validation",
        "created_at_utc": "2026-07-02T01:00:00Z",
        "updated_at_utc": "2026-07-02T01:05:00Z",
        "source_patch_zip": "router_bridge_patch_delivery_contract.md",
        "raw_error_text": "The AI risked forgetting root-cleanliness rules.",
        "raw_error_snapshot_scrubbed": "AI failed root-cleanliness checks.",
        "symptom": "Failure in enforcing root-cleanliness rules.",
        "root_cause": "Missing explicit enforcement.",
        "wrong_assumption": "Assumed rules were already enforced.",
        "correct_fix": "Add strict root-cleanliness checks.",
        "do_not_repeat_rule": "Do not bypass root-cleanliness checks.",
        "long_term_prevention": "Validate root cleanliness before patch delivery.",
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets included."],
        },
        "exception": {
            "type": "user_reported",
            "phase": "pending_validation",
            "relative_file_path": "scripts/validate_ai_response_patch_delivery.py",
            "function_or_test_name": "not specified",
            "message_normalized": "AI failed root-cleanliness checks",
            "stacktrace_scrubbed": "No traceback was provided.",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["root cleanliness"],
            "fingerprint_hash": "ai-forget-root-cleanliness-rules-v2",
        },
        "prevention_triggers": ["root cleanliness"],
        "regression_check": {
            "type": "validation_command",
            "command": "python validation/test_ai_root_cleanliness_enforcement_v1.py",
            "expected_marker": "VALIDATION OK: ai-forget-root-cleanliness-rules-v2",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run focused root-cleanliness validation.",
        "validation_evidence": [
            "No successful validation evidence was provided in the input; keep status draft."
        ],
        "install_command_summary": "Installer stages this lesson to pending intake only.",
        "notes": "Human review remains required.",
    }


def _block(payload: dict[str, object]) -> str:
    return BEGIN + "\n" + json.dumps(payload, indent=2, sort_keys=True) + "\n" + END


def validate_py_compile_and_line_counts() -> None:
    for rel_path in TOUCHED_FILES:
        path = PROJECT_ROOT / rel_path
        _assert(path.exists(), "Missing touched file: " + rel_path)
        _assert(_line_count(rel_path) <= 500, "Module exceeds 500 lines: " + rel_path)
        py_compile.compile(str(path), doraise=True)


def validate_exception_recovered_from_source() -> None:
    module = _load_validator_module()
    source_lesson = _lesson_base()
    ai_lesson = dict(source_lesson)
    ai_lesson.pop("exception")
    ai_text = _block(ai_lesson)
    source_text = _block(source_lesson)
    defaults = module.build_source_lesson_defaults(source_text)
    result = module.parse_one_lesson_block(ai_text, source_defaults=defaults)
    lesson = result.lesson
    _assert(isinstance(lesson.get("exception"), dict), "exception was not recovered.")
    _assert(
        lesson["exception"]["message_normalized"] == "AI failed root-cleanliness checks",
        "Recovered exception did not preserve source message.",
    )


def validate_exception_derived_when_absent() -> None:
    module = _load_validator_module()
    ai_lesson = _lesson_base()
    ai_lesson.pop("exception")
    result = module.parse_one_lesson_block(_block(ai_lesson))
    exception = result.lesson.get("exception")
    _assert(isinstance(exception, dict), "exception was not derived.")
    _assert(
        exception.get("message_normalized") == ai_lesson["raw_error_text"],
        "Derived exception did not use raw_error_text.",
    )
    _assert(result.lesson.get("status") == "draft", "Derived exception must keep draft status.")


def validate_prompt_contract_mentions_exception() -> None:
    text = _read("kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py")
    _assert("Do not omit superseded_by or exception" in text, "Retry prompt misses exception rule.")
    _assert("Include exception every time" in text, "Base prompt misses exception rule.")


def validate_copy_close_action_contract() -> None:
    text = _read("kanda_reasoner_app/error_memory_gui/_ai_correction_action.py")
    tree = ast.parse(text)
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    _assert("QMessageBox" not in names, "AI correction action still uses QMessageBox.")
    _assert("Copy and Close" in text, "Copy and Close button text is missing.")
    _assert("show_error_copy_close_window" in text, "Copy-close floating window is not used.")
    init_text = _read("kanda_reasoner_app/templates/floating_windows/__init__.py")
    _assert("show_error_copy_close_window" in init_text, "Floating window export is missing.")


def main() -> int:
    validate_py_compile_and_line_counts()
    validate_exception_recovered_from_source()
    validate_exception_derived_when_absent()
    validate_prompt_contract_mentions_exception()
    validate_copy_close_action_contract()
    print("VALIDATION OK: error-memory-local-ai-corrector-retry-v5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
