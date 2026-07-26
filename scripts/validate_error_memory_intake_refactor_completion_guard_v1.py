"""Validate Error Memory Intake Refactor Completion Guard v1."""

from __future__ import annotations

import ast
import json
import sys
import tempfile
from pathlib import Path

__all__: list[str] = []


FEATURE_ID = "error-memory-intake-refactor-completion-guard-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

INTAKE_DIR = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory"

EXPECTED_MODULES = {
    "intake.py",
    "intake_ai_form_prompt.py",
    "intake_form_builder.py",
    "intake_json_parser.py",
    "intake_normalization.py",
    "intake_plain_text.py",
}
MAX_LINES = 500
FACADE_MAX_LINES = 80
HELPER_MIN_LINES = 80


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read(path).splitlines())


def _function_names(path: Path) -> set[str]:
    tree = ast.parse(_read(path))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _assert_completion_shape() -> None:
    actual = {path.name for path in INTAKE_DIR.glob("intake*.py")}
    missing = EXPECTED_MODULES - actual
    unexpected = actual - EXPECTED_MODULES
    _assert(not missing, f"missing Error Memory intake modules: {sorted(missing)}")
    _assert(not unexpected, f"unexpected Error Memory intake helper sprawl: {sorted(unexpected)}")

    counts = {name: _line_count(INTAKE_DIR / name) for name in sorted(EXPECTED_MODULES)}
    _assert(counts["intake.py"] < FACADE_MAX_LINES, f"intake.py facade too large: {counts}")
    for name, count in counts.items():
        _assert(count <= MAX_LINES, f"module exceeds v7.2 cap: {name} ({count})")
    for name in sorted(EXPECTED_MODULES - {"intake.py"}):
        _assert(counts[name] >= HELPER_MIN_LINES, f"unexpected tiny helper module: {name} ({counts[name]})")


def _assert_facade_contract() -> None:
    facade = _read(INTAKE_DIR / "intake.py")
    for public_name in (
        "build_error_lesson_ai_form_prompt",
        "build_lesson_from_ai_form",
        "parse_error_lesson_ai_response",
        "save_ai_form_as_lesson",
    ):
        _assert(public_name in facade, f"facade missing public API re-export: {public_name}")
    for import_marker in (
        "from .intake_ai_form_prompt import",
        "from .intake_form_builder import",
        "from .intake_json_parser import",
        "from .intake_normalization import",
        "from .intake_plain_text import",
    ):
        _assert(import_marker in facade, f"facade missing import marker: {import_marker}")
    _assert("def build_error_lesson_ai_form_prompt" not in facade, "facade must not reimplement AI prompt builder")
    _assert("def parse_error_lesson_ai_response" not in facade, "facade must not reimplement parser")
    _assert("def save_ai_form_as_lesson" not in facade, "facade must not reimplement save boundary")
    _assert("__all__" in facade, "facade must define public API __all__")


def _assert_ownership() -> None:
    ownership = {
        "intake_ai_form_prompt.py": {"build_error_lesson_ai_form_prompt"},
        "intake_form_builder.py": {"build_lesson_from_ai_form", "save_ai_form_as_lesson"},
        "intake_json_parser.py": {
            "_normalize_ai_text",
            "_strip_markdown_fences",
            "_remove_trailing_commas",
            "_escape_raw_control_chars_inside_strings",
            "_extract_balanced_json_objects",
            "_candidate_blocks",
            "_json_load_attempts",
            "_payload_score",
            "parse_error_lesson_ai_response",
        },
        "intake_normalization.py": {
            "_contains_any_marker",
            "_has_successful_validation_evidence",
            "_should_force_draft_status",
            "_coerce_status_for_ai_form",
            "_as_text",
            "_as_list",
            "_normalize_regression_check_for_error_memory_json",
            "_normalize_redaction_for_error_memory_json",
            "_downgrade_non_active_ready_lesson",
        },
        "intake_plain_text.py": {
            "_strip_list_marker",
            "_label_key",
            "_infer_phase_from_plain_text",
            "_plain_text_triggers",
            "_plain_text_to_form",
        },
    }
    for filename, expected in ownership.items():
        names = _function_names(INTAKE_DIR / filename)
        missing = expected - names
        _assert(not missing, f"ownership functions missing from {filename}: {sorted(missing)}")


def _sample_active_form() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "project_slug": "sample_project",
        "lesson_id": "lesson-sample-active-ready-v1",
        "status": "active",
        "operation_phase": "validation",
        "created_at_utc": "2026-06-30T00:00:00Z",
        "updated_at_utc": "2026-06-30T00:00:00Z",
        "source_patch_zip": "sample_patch.zip",
        "raw_error_text": "Validation failed before correction; after repair VALIDATION OK: sample and ZIP CONTRACT: PASS.",
        "raw_error_snapshot_scrubbed": "Scrubbed validation output with no secrets.",
        "symptom": "Validation failed before the patch was corrected.",
        "root_cause": "The validator expectation was incomplete.",
        "wrong_assumption": "Assumed active Error Memory lessons did not need validation evidence.",
        "correct_fix": "Require successful validation evidence before preserving active status.",
        "long_term_prevention": "Keep active-ready gates before saving AI-generated lessons.",
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
            "command": "python scripts\\validate_sample.py",
            "expected_marker": "VALIDATION OK: sample",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Run validation and confirm VALIDATION OK plus ZIP CONTRACT: PASS.",
        "validation_evidence": ["VALIDATION OK: sample", "STATUS: IN_SYNC", "ZIP CONTRACT: PASS"],
        "install_command_summary": "Installer copies payload files only.",
        "notes": "STATUS: IN_SYNC confirmed.",
    }


def _assert_runtime_contract() -> None:
    from kanda_reasoner_app.error_memory import intake

    expected_public = {
        "build_error_lesson_ai_form_prompt",
        "build_lesson_from_ai_form",
        "parse_error_lesson_ai_response",
        "save_ai_form_as_lesson",
    }
    _assert(set(intake.__all__) == expected_public, f"unexpected public API: {intake.__all__}")
    for name in expected_public:
        _assert(hasattr(intake, name), f"runtime public API missing: {name}")
    for private_name in (
        "_json_load_attempts",
        "_should_force_draft_status",
        "_plain_text_to_form",
        "_normalize_regression_check_for_error_memory_json",
        "_downgrade_non_active_ready_lesson",
    ):
        _assert(hasattr(intake, private_name), f"private compatibility helper missing: {private_name}")

    prompt = intake.build_error_lesson_ai_form_prompt(selected_project_root=Path("sample_project"), raw_error_text="raw", operation_phase="validation")
    _assert("KANDA_ERROR_LESSON_JSON_BEGIN" in prompt, "AI prompt missing begin marker")
    _assert("KANDA_ERROR_LESSON_JSON_END" in prompt, "AI prompt missing end marker")
    _assert("Required active-ready keys" in prompt, "AI prompt missing active-ready contract")
    _assert("Do not use Windows backslashes" in prompt, "AI prompt missing backslash warning")

    active_form = _sample_active_form()
    wrapped = "KANDA_ERROR_LESSON_JSON_BEGIN\n" + json.dumps(active_form, ensure_ascii=False, indent=2) + "\nKANDA_ERROR_LESSON_JSON_END"
    parsed = intake.parse_error_lesson_ai_response(wrapped)
    _assert(parsed.get("status") == "active", f"evidence-backed active form should remain active: {parsed.get('status')}")
    _assert(parsed.get("regression_check", {}).get("command") == "python scripts\\validate_sample.py", "parser should preserve raw AI command before builder normalization")

    no_evidence = dict(active_form)
    no_evidence["validation_evidence"] = ["validation failed before correction"]
    no_evidence["validation_command_summary"] = "Validation failed before correction."
    no_evidence["notes"] = "Needs investigation; not corrected yet."
    parsed_draft = intake.parse_error_lesson_ai_response(json.dumps(no_evidence, ensure_ascii=False))
    _assert(parsed_draft.get("status") == "draft", "unvalidated active AI form must be forced to draft")

    fenced = "```json\n{" + '"status":"draft", "symptom":"one",}' + "\n```"
    recovered_fenced = intake.parse_error_lesson_ai_response(fenced)
    _assert(recovered_fenced.get("status") == "draft", "markdown fenced trailing-comma JSON must parse")

    corrupted = '{"status": "draft", "symptom": "line one\nline two",}'
    loaded = intake._json_load_attempts(corrupted)
    _assert(isinstance(loaded, dict), "JSON recovery must handle raw newline and trailing comma")
    _assert("line one" in loaded.get("symptom", ""), "recovered JSON content changed")

    fallback = intake.parse_error_lesson_ai_response(
        "Symptom: patch ZIP contract failed\nDo not repeat: validate the staged zip before freeze"
    )
    _assert(fallback.get("status") == "draft", "plain-text fallback must stay draft-first")
    _assert(fallback.get("operation_phase") == "patch_contract", "plain-text phase inference changed")

    normalized = intake._normalize_regression_check_for_error_memory_json(
        {"type": "validation_command", "command": "python scripts\\validate_sample.py"}
    )
    _assert(normalized and normalized.get("command") == "python scripts/validate_sample.py", "safe backslashes should normalize to forward slashes")
    corrupted_command = intake._normalize_regression_check_for_error_memory_json(
        {"type": "validation_command", "command": "python scripts\tvalidate_sample.py"}
    )
    _assert(corrupted_command and "\t" in corrupted_command.get("command", ""), "corrupted control characters must be preserved")

    with tempfile.TemporaryDirectory(prefix="kanda_error_memory_intake_completion_guard_") as tmp_text:
        project_root = Path(tmp_text) / "sample_project"
        project_root.mkdir()
        lesson = intake.build_lesson_from_ai_form(selected_project_root=project_root, form_inputs=parsed)
        _assert(lesson.get("status") == "active", "builder should keep active only for active-ready evidence-backed lesson")
        _assert(lesson.get("regression_check", {}).get("command") == "python scripts/validate_sample.py", "builder should normalize safe command slashes")
        saved_path, saved_lesson = intake.save_ai_form_as_lesson(selected_project_root=project_root, form_inputs=parsed)
        _assert(saved_path.exists(), "save_ai_form_as_lesson did not write lesson")
        _assert(saved_lesson.get("lesson_id"), "saved lesson missing lesson_id")
        safe_path = saved_path.as_posix()
        _assert("project_freeze" not in safe_path, "Error Memory intake must not write freeze memory")
        _assert("frozen_features_memory" not in safe_path, "Error Memory intake must not write frozen feature memory")
        _assert("project_freeze_ledger" not in safe_path, "Error Memory intake must not write freeze ledger")


def main() -> int:
    _ensure_project_root_on_path()
    _assert_completion_shape()
    _assert_facade_contract()
    _assert_ownership()
    _assert_runtime_contract()
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
