"""Validate active-ready Error Memory intake for docstring/projectqa validation scope fix."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSON_REL = Path(
    "project_error_memory"
) / "pending_ai_assisted_error_lesson_intake" / (
    "KANDA_ERROR_LESSON_JSON_docstring_projectqa_validation_scope_fix_v1.json"
)
LESSON_ID = "lesson-docstring-projectqa-validation-scope-fix-v1"
EXPECTED_MARKER = "VALIDATION OK: docstring-projectqa-normal-source-v1"


def require(condition: bool, message: str) -> None:
    """Raise an AssertionError when condition is false."""
    if not condition:
        raise AssertionError(message)


def read_lesson() -> dict:
    """Read the staged lesson from project root or external pending intake."""
    candidates = [ROOT / LESSON_REL]

    project_name = ROOT.name
    drive = ROOT.drive
    if drive:
        show_root = Path(drive + "\\") / (project_name + "_show_project_to_AI")
    else:
        show_root = ROOT.parent / (project_name + "_show_project_to_AI")
    candidates.append(show_root / LESSON_REL)

    for path in candidates:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))

    raise AssertionError("staged Error Memory lesson not found")


def assert_redaction(lesson: dict) -> None:
    """Check redaction object required by active-ready Error Memory lessons."""
    redaction = lesson.get("redaction")
    require(isinstance(redaction, dict), "redaction must be an object")
    require(redaction.get("applied") is True, "redaction.applied must be true")
    require(redaction.get("export_safe") is True, "redaction.export_safe must be true")
    rules = redaction.get("rules")
    require(isinstance(rules, list), "redaction.rules must be a list")
    require(bool(rules), "redaction.rules must be non-empty")
    require(
        all(isinstance(rule, str) and rule.strip() for rule in rules),
        "redaction.rules must contain non-empty strings",
    )


def assert_active_ready(lesson: dict) -> None:
    """Check the active-ready lesson fields needed by Error Memory."""
    required = [
        "schema_version",
        "lesson_id",
        "status",
        "superseded_by",
        "project_slug",
        "operation_phase",
        "created_at_utc",
        "updated_at_utc",
        "source_patch_zip",
        "raw_error_text",
        "raw_error_snapshot_scrubbed",
        "symptom",
        "root_cause",
        "wrong_assumption",
        "correct_fix",
        "long_term_prevention",
        "do_not_repeat_rule",
        "exception",
        "fingerprint",
        "prevention_triggers",
        "regression_check",
        "validation_command_summary",
        "validation_evidence",
        "redaction",
        "install_command_summary",
        "notes",
    ]
    for key in required:
        require(key in lesson, "missing key: " + key)

    require(lesson["lesson_id"] == LESSON_ID, "wrong lesson_id")
    require(lesson["status"] == "active", "lesson status is not active")
    require(lesson["project_slug"] == "kanda_reasoner", "wrong project_slug")
    require(lesson["operation_phase"] == "validation", "wrong operation_phase")
    require(
        lesson["source_patch_zip"]
        == "kanda_docstring_projectqa_normal_source_v1_validation_scope_fix_patch.zip",
        "wrong source_patch_zip",
    )

    regression = lesson["regression_check"]
    require(regression["type"] == "validation_command", "wrong regression type")
    require(
        regression["command"] == "python validation/test_docstring_projectqa_normal_source_v1.py",
        "wrong regression command",
    )
    require(regression["expected_marker"] == EXPECTED_MARKER, "wrong expected marker")
    require(regression["required_before_freeze"] is True, "required_before_freeze must be true")

    evidence = "\n".join(lesson["validation_evidence"])
    require(EXPECTED_MARKER in evidence, "missing validation OK evidence")
    require("STATUS: IN_SYNC" in evidence, "missing STATUS: IN_SYNC evidence")
    require("ZIP CONTRACT: PASS" in evidence, "missing ZIP CONTRACT evidence")

    assert_redaction(lesson)

    text_blob = json.dumps(lesson, ensure_ascii=True)
    require(
        "legacy placeholder" in text_blob,
        "lesson does not describe the placeholder scope problem",
    )
    require(
        "migrated visible-tab" in text_blob,
        "lesson does not describe the visible-tab scope boundary",
    )


def main() -> int:
    """Run validation."""
    lesson = read_lesson()
    assert_active_ready(lesson)
    print("VALIDATION OK: error-memory-docstring-projectqa-validation-scope-fix-v1")
    print("STATUS: IN_SYNC")
    print("ERROR MEMORY INTAKE CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
