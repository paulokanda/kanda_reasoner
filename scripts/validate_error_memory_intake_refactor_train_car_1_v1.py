"""Validate Error Memory intake refactor train car 1."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-intake-refactor-train-car-1-v1"
ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

INTAKE_DIR = ROOT / "kanda_reasoner_app" / "error_memory"

FILES = [
    INTAKE_DIR / "intake.py",
    INTAKE_DIR / "intake_ai_form_prompt.py",
    INTAKE_DIR / "intake_form_builder.py",
    INTAKE_DIR / "intake_json_parser.py",
    INTAKE_DIR / "intake_normalization.py",
    INTAKE_DIR / "intake_plain_text.py",
]

EXPECTED_HELPERS = {
    "intake_ai_form_prompt.py",
    "intake_form_builder.py",
    "intake_json_parser.py",
    "intake_normalization.py",
    "intake_plain_text.py",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read(path).splitlines())


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sample_active_form() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "project_slug": "sample_project",
        "lesson_id": "lesson-sample-validation-v1",
        "status": "active",
        "operation_phase": "validation",
        "created_at_utc": "2026-06-30T00:00:00Z",
        "updated_at_utc": "2026-06-30T00:00:00Z",
        "source_patch_zip": "sample_patch.zip",
        "raw_error_text": "Validation failed before the fix; after correction VALIDATION OK: sample-feature and ZIP CONTRACT: PASS.",
        "raw_error_snapshot_scrubbed": "Scrubbed validation output with no secrets.",
        "symptom": "Validation failed before the patch was corrected.",
        "root_cause": "The validator expectation was incomplete.",
        "wrong_assumption": "Assumed validation evidence could be omitted.",
        "correct_fix": "Require validation evidence before active lesson status.",
        "long_term_prevention": "Keep active lessons gated by validation markers.",
        "do_not_repeat_rule": "Do not save active lessons without successful validation evidence.",
        "exception": {
            "type": "ValidationError",
            "phase": "validation",
            "relative_file_path": "scripts/validate_sample.py",
            "function_or_test_name": "validate_sample",
            "message_normalized": "validation failed before correction",
            "stacktrace_scrubbed": "No traceback provided.",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["ValidationError", "scripts/validate_sample.py", "validation", "missing evidence"],
            "fingerprint_hash": "abcdef1234567890",
        },
        "prevention_triggers": ["validation evidence", "active-ready"],
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets present.", "No patient data present."],
        },
        "regression_check": {
            "type": "validation_command",
            "command": "python scripts/validate_sample.py",
            "expected_marker": "VALIDATION OK: sample-feature",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run validation and confirm VALIDATION OK plus ZIP CONTRACT: PASS.",
        "validation_evidence": ["VALIDATION OK: sample-feature", "ZIP CONTRACT: PASS"],
        "install_command_summary": "Installer copies only payload files.",
        "notes": "STATUS: IN_SYNC confirmed.",
    }


def main() -> int:
    _ensure_project_root_on_path()
    for path in FILES:
        _assert(path.exists(), f"missing expected file: {path}")
        _assert(_line_count(path) <= 500, f"module exceeds v7.2 line cap: {path} ({_line_count(path)})")
    _assert(_line_count(INTAKE_DIR / "intake.py") <= 120, "intake.py facade is too large")
    helper_names = {path.name for path in INTAKE_DIR.glob("intake_*.py")}
    unexpected = helper_names - EXPECTED_HELPERS
    _assert(not unexpected, f"unexpected intake helper sprawl: {sorted(unexpected)}")

    facade = _read(INTAKE_DIR / "intake.py")
    for public_name in (
        "build_error_lesson_ai_form_prompt",
        "build_lesson_from_ai_form",
        "parse_error_lesson_ai_response",
        "save_ai_form_as_lesson",
    ):
        _assert(public_name in facade, f"facade missing public API: {public_name}")
    _assert("from .intake_json_parser import" in facade, "facade must re-export parser helpers")
    _assert("from .intake_normalization import" in facade, "facade must re-export normalization helpers")
    _assert("from .intake_plain_text import" in facade, "facade must re-export plain-text helpers")

    normalization = _read(INTAKE_DIR / "intake_normalization.py")
    _assert("_VALIDATION_SUCCESS_MARKERS" in normalization, "validation success markers moved out of normalization")
    _assert("_should_force_draft_status" in normalization, "draft forcing helper missing")
    _assert("active_ready_missing_reasons" in normalization, "active-ready downgrade reasons must be preserved")

    parser = _read(INTAKE_DIR / "intake_json_parser.py")
    for marker in (
        "_strip_markdown_fences",
        "_remove_trailing_commas",
        "_escape_raw_control_chars_inside_strings",
        "_extract_balanced_json_objects",
        "_json_load_attempts",
        "_plain_text_to_form",
    ):
        _assert(marker in parser, f"JSON parser missing recovery behavior: {marker}")

    prompt = _read(INTAKE_DIR / "intake_ai_form_prompt.py")
    _assert("KANDA_ERROR_LESSON_JSON_BEGIN" in prompt, "AI prompt must require begin marker")
    _assert("Do not use Windows backslashes" in prompt, "AI prompt must keep command/path backslash warning")
    _assert("Required active-ready keys" in prompt, "AI prompt must preserve active-ready key instruction")

    form_builder = _read(INTAKE_DIR / "intake_form_builder.py")
    _assert("save_lesson" in form_builder, "save boundary must remain explicit in form builder")
    _assert("_downgrade_non_active_ready_lesson" in form_builder, "active-ready downgrade must be applied before save")

    from kanda_reasoner_app.error_memory import intake

    for public_name in intake.__all__:
        _assert(hasattr(intake, public_name), f"public API missing at runtime: {public_name}")
    for private_name in (
        "_json_load_attempts",
        "_should_force_draft_status",
        "_plain_text_to_form",
        "_normalize_regression_check_for_error_memory_json",
    ):
        _assert(hasattr(intake, private_name), f"private compatibility helper missing: {private_name}")

    wrapped_json = "KANDA_ERROR_LESSON_JSON_BEGIN\n" + json.dumps(_sample_active_form(), ensure_ascii=False, indent=2) + "\nKANDA_ERROR_LESSON_JSON_END"
    parsed = intake.parse_error_lesson_ai_response(wrapped_json)
    _assert(parsed.get("status") == "active", f"valid evidence-backed active form should parse as active: {parsed.get('status')}")
    _assert(parsed.get("prevention_triggers") == ["validation evidence", "active-ready"], "prevention triggers list changed")
    _assert(isinstance(parsed.get("regression_check"), dict), "regression_check dict must be preserved")

    pending = _sample_active_form()
    pending["validation_evidence"] = ["validation failed before correction"]
    pending["validation_command_summary"] = "Validation failed before correction."
    pending["notes"] = "Needs investigation."
    parsed_pending = intake.parse_error_lesson_ai_response(json.dumps(pending, ensure_ascii=False))
    _assert(parsed_pending.get("status") == "draft", "failed/unvalidated active form must be forced to draft")

    corrupted = '{"status": "draft", "symptom": "line one\nline two",}'
    loaded = intake._json_load_attempts(corrupted)
    _assert(isinstance(loaded, dict), "JSON recovery must handle raw newline and trailing comma")
    _assert("line one" in loaded.get("symptom", ""), "recovered JSON string content changed")

    fallback = intake.parse_error_lesson_ai_response("Symptom: zip contract failed\nDo not repeat: validate the staged zip before freeze")
    _assert(fallback.get("status") == "draft", "plain-text fallback must default to draft")
    _assert(fallback.get("operation_phase") == "patch_contract", "plain-text phase inference changed")

    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "sample_project"
        project_root.mkdir()
        lesson = intake.build_lesson_from_ai_form(selected_project_root=project_root, form_inputs=parsed)
        _assert(lesson.get("status") == "active", "build_lesson_from_ai_form should keep active only for active-ready evidence-backed lessons")
        saved_path, saved_lesson = intake.save_ai_form_as_lesson(selected_project_root=project_root, form_inputs=parsed)
        _assert(saved_path.exists(), "save_ai_form_as_lesson did not write lesson")
        _assert(saved_lesson.get("lesson_id"), "saved lesson missing id")
        _assert("project_freeze" not in saved_path.as_posix(), "Error Memory intake must not write freeze memory")

    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
