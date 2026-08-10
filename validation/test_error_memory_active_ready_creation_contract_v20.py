"""Regression tests for active-ready Error Memory lesson creation contract v20."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# The portable validation sandbox may not contain the full storage-policy tree.
# Mock only the project-analysis helpers used by Error Memory path/model modules;
# the real installed app provides these helpers normally.
import types  # noqa: E402

project_paths = types.ModuleType("kanda_reasoner_app.project_analysis_evidence_paths")
project_paths.SECOND_PROMPT_FILES_DIR = "second_prompt_files"
project_paths.project_name_from_root = lambda value: Path(value).name or "kanda_reasoner"
project_paths.show_project_to_ai_root_from_hint = lambda value: Path(value).resolve(strict=False).parent / (Path(value).resolve(strict=False).name + "_show_project_to_AI")
sys.modules.setdefault("kanda_reasoner_app.project_analysis_evidence_paths", project_paths)

from kanda_reasoner_app.error_memory.intake import (  # noqa: E402
    ALLOWED_ERROR_LESSON_FORM_KEYS,
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    build_error_lesson_ai_form_prompt,
    build_lesson_from_ai_form,
)
from kanda_reasoner_app.error_memory.models import active_ready, active_ready_missing_reasons  # noqa: E402
from kanda_reasoner_app.patch_governance.validator import (  # noqa: E402
    _validate_error_memory_lesson_payload,
)

PROMPT_PATH = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "error_memory_ai_formulary_startup_canon.md"


def _bad_user_example() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "lesson_id": "lesson-freeze-hint-no-stale-local-validation-pending-v1",
        "status": "active",
        "project_slug": "kanda_reasoner",
        "operation_phase": "freeze-intake",
        "created_at_utc": "2026-06-26T02:55:00Z",
        "updated_at_utc": "2026-06-26T02:55:00Z",
        "source_patch_zip": "kanda_error_memory_memorize_clears_intake_only_v2_patch.zip",
        "symptom": "Freeze Feature After Update blocked Confirm and Write because KANDA_FREEZE_HINT.json still said local validation was pending.",
        "root_cause": "The patch ZIP included stale pending wording.",
        "wrong_assumption": "Assumed stale local-validation-pending wording was acceptable.",
        "correct_fix": "Remove stale local-validation-pending wording from KANDA_FREEZE_HINT.json.",
        "do_not_repeat_rule": "Do not ship KANDA_FREEZE_HINT.json with stale local-validation-pending wording.",
        "long_term_prevention": "Inspect KANDA_FREEZE_HINT.json before patch delivery.",
        "exception": {
            "type": "FreezeHintMetadataError",
            "phase": "freeze-intake",
            "relative_file_path": "KANDA_FREEZE_HINT.json",
            "function_or_test_name": "Freeze Feature After Update intake",
            "message_normalized": "FREEZE BLOCKED - local validation is still pending",
            "stacktrace_scrubbed": "",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["FreezeHintMetadataError", "KANDA_FREEZE_HINT.json", "freeze-intake"],
            "fingerprint_hash": "bec13c7dc00d34fd04e7c7666198db8d48e65e2d4c83fbc6a50d5b6b805b48a8",
        },
        "prevention_triggers": ["FREEZE BLOCKED - local validation is still pending"],
        "regression_check": {
            "type": "validation_command",
            "command": "python validation\\test_error_memory_memorize_clears_intake_only_v2.py",
            "expected_marker": "VALIDATION OK: error-memory-memorize-clears-intake-only-v2",
            "required_before_freeze": True,
        },
        "validation_command_summary": "Validation must include py_compile and successful execution.",
        "validation_evidence": ["User reported Freeze tab error."],
        "install_command_summary": "Installer stages this lesson into pending intake.",
        "notes": "Missing active-ready metadata should be rejected.",
    }


def _active_ready_lesson() -> dict[str, object]:
    lesson = _bad_user_example()
    lesson["raw_error_text"] = "FREEZE BLOCKED - local validation is still pending; run local validation and remove stale pending sidecar wording before Confirm and Write."
    lesson["raw_error_snapshot_scrubbed"] = "Freeze Feature After Update blocked Confirm and Write because KANDA_FREEZE_HINT.json contained stale local-validation-pending wording in validation_evidence_summary."
    lesson["redaction"] = {
        "applied": True,
        "export_safe": True,
        "rules": [
            "No secrets or credentials present.",
            "No patient data present.",
            "Project identifiers are intentional technical context.",
        ],
    }
    lesson["exception"] = dict(lesson["exception"])
    lesson["exception"]["stacktrace_scrubbed"] = "No traceback was provided; Freeze tab reported the normalized blocker message."
    return lesson


def main() -> int:
    required_keys = {
        "schema_version",
        "lesson_id",
        "project_slug",
        "created_at_utc",
        "updated_at_utc",
        "raw_error_text",
        "raw_error_snapshot_scrubbed",
        "exception",
        "fingerprint",
        "redaction",
    }
    missing_allowed = sorted(required_keys - set(ALLOWED_ERROR_LESSON_FORM_KEYS))
    assert not missing_allowed, "required active-ready keys missing from AI allowed form keys: " + ", ".join(missing_allowed)

    prompt = build_error_lesson_ai_form_prompt(
        selected_project_root=PROJECT_ROOT,
        raw_error_text="FREEZE BLOCKED - local validation is still pending",
        operation_phase="freeze-intake",
    )
    assert "The first visible characters must be KANDA_ERROR_LESSON_JSON_BEGIN" in prompt, "AI prompt must instruct marker-first output"
    assert ERROR_LESSON_JSON_BEGIN in prompt and ERROR_LESSON_JSON_END in prompt, "AI prompt must include receive markers"
    assert "raw_error_snapshot_scrubbed" in prompt, "prompt must request raw_error_snapshot_scrubbed"
    assert "redaction.applied=true" in prompt, "prompt must request redaction metadata"
    assert "Allowed keys only" not in prompt, "prompt must not use the obsolete limited allowed-keys instruction"

    prompt_file_text = PROMPT_PATH.read_text(encoding="utf-8")
    assert "Version: 1.3" in prompt_file_text, "startup canon must be v1.3"
    assert "Error Memory active-ready creation contract - v2" in prompt_file_text, "startup canon must include v2 creation contract"
    assert "raw_error_snapshot_scrubbed" in prompt_file_text, "startup canon must include raw_error_snapshot_scrubbed"
    assert "redaction" in prompt_file_text, "startup canon must include redaction metadata"

    bad = _bad_user_example()
    reasons = active_ready_missing_reasons(dict(bad))
    assert not active_ready(dict(bad)), "bad user example must not be active-ready"
    assert any("raw_error_text" in reason for reason in reasons), "missing raw_error_text must be detected"
    assert any("raw_error_snapshot_scrubbed" in reason for reason in reasons), "missing raw_error_snapshot_scrubbed must be detected"
    assert any("redaction" in reason for reason in reasons), "missing redaction must be detected"

    good = _active_ready_lesson()
    assert active_ready(dict(good)), "complete active lesson should be active-ready"
    _validate_error_memory_lesson_payload(good, "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_good.txt")
    try:
        _validate_error_memory_lesson_payload(bad, "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_bad.txt")
    except Exception as exc:
        assert "raw_error_text" in str(exc) or "redaction" in str(exc)
    else:
        raise AssertionError("package validator must block missing active-ready metadata")

    rebuilt = build_lesson_from_ai_form(
        selected_project_root=PROJECT_ROOT,
        form_inputs=good,
        fallback_operation_phase="freeze-intake",
    )
    assert rebuilt.get("raw_error_text"), "builder must preserve/create raw_error_text"
    assert rebuilt.get("raw_error_snapshot_scrubbed"), "builder must preserve/create raw_error_snapshot_scrubbed"
    assert isinstance(rebuilt.get("redaction"), dict), "builder must preserve/create redaction object"

    print("VALIDATION OK: error-memory-active-ready-creation-contract-v20")
    print("ERROR_MEMORY_ACTIVE_READY_CREATION: obsolete minimal AI prompt removed")
    print("ERROR_MEMORY_ACTIVE_READY_CREATION: active-ready keys required in AI creation prompt")
    print("ERROR_MEMORY_ACTIVE_READY_CREATION: raw_error_text and raw_error_snapshot_scrubbed enforced")
    print("ERROR_MEMORY_ACTIVE_READY_CREATION: redaction, exception, fingerprint enforced")
    print("ERROR_MEMORY_ACTIVE_READY_CREATION: package validator blocks non-memorizable active lessons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
