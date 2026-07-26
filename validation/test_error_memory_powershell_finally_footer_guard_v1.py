"""Validate Error Memory intake for PowerShell finally footer guard."""

from __future__ import annotations

import json
from pathlib import Path

FEATURE_ID = "error-memory-powershell-finally-footer-guard-v1"
LESSON_SLUG = "powershell_finally_footer_paste_split_guard_v1"
LESSON_ID = "lesson-powershell-finally-footer-paste-split-guard-v1"
BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
END = "KANDA_ERROR_LESSON_JSON_END"

REQUIRED_FIELDS = (
    "schema_version",
    "lesson_id",
    "status",
    "project_slug",
    "operation_phase",
    "symptom",
    "root_cause",
    "correct_fix",
    "long_term_prevention",
    "do_not_repeat_rule",
    "exception",
    "fingerprint",
    "prevention_triggers",
    "regression_check",
    "validation_evidence",
    "redaction",
    "raw_error_snapshot_scrubbed",
    "install_command_summary",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _pending_dir(project_root: Path) -> Path:
    drive_root = Path(project_root.anchor)
    show_project_root = drive_root / f"{project_root.name}_show_project_to_AI"
    return show_project_root / "project_error_memory" / "pending_ai_assisted_error_lesson_intake"


def _extract_json(text: str) -> dict:
    if BEGIN not in text or END not in text:
        raise AssertionError("KANDA_ERROR_LESSON_JSON markers are missing.")
    start = text.index(BEGIN) + len(BEGIN)
    stop = text.index(END, start)
    raw_json = text[start:stop].strip()
    data = json.loads(raw_json)
    if not isinstance(data, dict):
        raise AssertionError("Lesson payload must be a JSON object.")
    return data


def _validate_lesson(data: dict) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise AssertionError("Lesson missing fields: " + ", ".join(missing))
    if data["lesson_id"] != LESSON_ID:
        raise AssertionError("Unexpected lesson_id.")
    if data["status"] != "active":
        raise AssertionError("Lesson must be active-ready.")
    if data["operation_phase"] != "validation":
        raise AssertionError("operation_phase must be validation.")
    triggers = data.get("prevention_triggers")
    if not isinstance(triggers, list) or not triggers:
        raise AssertionError("prevention_triggers must be a non-empty list.")
    trigger_text = "\n".join(str(item).lower() for item in triggers)
    if "finally" not in trigger_text or "powershell" not in trigger_text:
        raise AssertionError("prevention_triggers must mention PowerShell finally.")
    evidence = data.get("validation_evidence")
    if not isinstance(evidence, list) or not evidence:
        raise AssertionError("validation_evidence must be a non-empty list.")
    redaction = data.get("redaction")
    if not isinstance(redaction, dict):
        raise AssertionError("redaction must be an object.")
    if redaction.get("applied") is not True or redaction.get("export_safe") is not True:
        raise AssertionError("redaction.applied and redaction.export_safe must be true.")
    exception = data.get("exception")
    if not isinstance(exception, dict):
        raise AssertionError("exception must be an object.")
    if "finally is not recognized" not in exception.get("message_normalized", ""):
        raise AssertionError("exception message must capture the finally footer failure.")
    regression = data.get("regression_check")
    if not isinstance(regression, dict):
        raise AssertionError("regression_check must be an object.")
    if regression.get("expected_marker") != f"VALIDATION OK: {FEATURE_ID}":
        raise AssertionError("regression_check expected marker is wrong.")


def main() -> int:
    project_root = _project_root()
    packaged_lesson = (
        project_root
        / "error_memory_receive_blocks"
        / f"KANDA_ERROR_LESSON_JSON_{LESSON_SLUG}.txt"
    )
    installed_lesson = _pending_dir(project_root) / f"KANDA_ERROR_LESSON_JSON_{LESSON_SLUG}.txt"

    if packaged_lesson.exists():
        data = _extract_json(packaged_lesson.read_text(encoding="utf-8", errors="replace"))
        _validate_lesson(data)

    if not installed_lesson.is_file():
        raise AssertionError("Installed pending intake lesson was not found: " + str(installed_lesson))
    installed_data = _extract_json(installed_lesson.read_text(encoding="utf-8", errors="replace"))
    _validate_lesson(installed_data)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("ERROR_MEMORY_PENDING_INTAKE: staged")
    print("POWERSHELL_FINALLY_FOOTER_GUARD: active-ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
