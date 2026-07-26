"""Validate Error Memory lesson block schema gate in patch ZIP validation."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.patch_governance.validator import (  # noqa: E402
    PatchZipContractError,
    validate_patch_zip,
)

FEATURE_ID = "error-memory-lesson-block-schema-gate-v1"


def _freeze_hint() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "kind": "kanda_freeze_hint",
        "patch_name": "unit_test_patch",
        "feature_id": FEATURE_ID,
        "feature_title": "Error Memory Lesson Block Schema Gate",
        "primary_box": "kanda_reasoner_app/patch_governance",
        "box_type": "patch ZIP contract validator",
        "validated_files": ["kanda_reasoner_app/patch_governance/validator.py"],
        "generated_files": ["payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_test.txt"],
        "protected_paths": ["<drive>:/<project>_show_project_to_AI/project_error_memory"],
        "do_not_regress_rules": ["Packaged Error Memory lessons must include schema_version and project_slug."],
        "validation_evidence_summary": "VALIDATION OK: " + FEATURE_ID,
        "known_warnings": "Unit test sidecar.",
        "planned_next_step": "Run validation.",
        "notes": "Unit test sidecar.",
    }


def _active_lesson() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "lesson_id": "lesson-error-memory-schema-gate-test-v1",
        "status": "active",
        "superseded_by": "",
        "project_slug": "kanda_reasoner",
        "operation_phase": "validation",
        "created_at_utc": "2026-06-26T13:20:00Z",
        "updated_at_utc": "2026-06-26T13:20:00Z",
        "source_patch_zip": "unit_test_patch.zip",
        "raw_error_text": "scrubbed test evidence",
        "symptom": "A packaged Error Memory lesson missed required schema fields.",
        "root_cause": "The ZIP validator did not inspect KANDA_ERROR_LESSON_JSON blocks.",
        "wrong_assumption": "Prompt-only guidance was enough to prevent invalid lesson blocks.",
        "correct_fix": "Validate packaged Error Memory lesson blocks inside patch ZIP contract validation.",
        "long_term_prevention": "Block invalid Error Memory lesson blocks before release.",
        "do_not_repeat_rule": "Do not release a ZIP containing KANDA_ERROR_LESSON_JSON without schema_version and project_slug.",
        "exception": {
            "type": "ErrorMemoryLessonSchemaError",
            "phase": "validation",
            "relative_file_path": "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_test.txt",
            "function_or_test_name": "validate_patch_zip",
            "message_normalized": "missing key: schema_version; missing key: project_slug",
            "stacktrace_scrubbed": "",
        },
        "fingerprint": {
            "strategy": "v1_structural_conservative",
            "components": ["ErrorMemoryLessonSchemaError", "KANDA_ERROR_LESSON_JSON", "missing schema_version", "missing project_slug"],
            "fingerprint_hash": "unit-test-error-memory-schema-gate-v1",
        },
        "prevention_triggers": ["missing key: schema_version", "missing key: project_slug"],
        "regression_check": {
            "type": "validation_command",
            "command": "python validation\\test_error_memory_lesson_block_schema_gate_v1.py",
            "expected_marker": "VALIDATION OK: " + FEATURE_ID,
            "required_before_freeze": True,
        },
        "validation_command_summary": "The test proves patch ZIP validation blocks invalid Error Memory lesson blocks.",
        "validation_evidence": ["ZIP CONTRACT: PASS", "VALIDATION OK: " + FEATURE_ID],
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": ["No secrets or credentials present."],
        },
        "raw_error_snapshot_scrubbed": "missing key: schema_version; missing key: project_slug",
        "install_command_summary": "Installer updates the patch ZIP validator and prompt guardrails.",
        "notes": "Unit test lesson.",
    }


def _write_zip(path: Path, lesson: dict[str, object]) -> None:
    block = "KANDA_ERROR_LESSON_JSON_BEGIN\n" + json.dumps(lesson, indent=2, sort_keys=True) + "\nKANDA_ERROR_LESSON_JSON_END\n"
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(_freeze_hint(), indent=2, sort_keys=True))
        archive.writestr("payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_test.txt", block)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        bad_lesson = _active_lesson()
        bad_lesson.pop("schema_version")
        bad_lesson.pop("project_slug")
        bad_zip = tmp_path / "bad.zip"
        _write_zip(bad_zip, bad_lesson)
        try:
            validate_patch_zip(bad_zip)
        except PatchZipContractError as exc:
            message = str(exc)
            if "schema_version" not in message or "project_slug" not in message:
                raise AssertionError("Expected missing schema_version/project_slug error, got: " + message) from exc
        else:
            raise AssertionError("Invalid Error Memory lesson block was not rejected.")

        good_zip = tmp_path / "good.zip"
        _write_zip(good_zip, _active_lesson())
        report = validate_patch_zip(good_zip)
        if int(report.get("error_memory_lesson_blocks_checked", 0)) != 1:
            raise AssertionError("Expected one Error Memory lesson block to be checked.")

    print("VALIDATION OK: " + FEATURE_ID)
    print("ERROR_MEMORY_LESSON_BLOCK_SCHEMA_GATE: active")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
