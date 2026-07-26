# project-path: kanda_reasoner_app/error_memory/intake_normalization.py
"""Normalization and safety helpers for Error Memory AI intake."""

from __future__ import annotations

import json
from typing import Any, Mapping

from .models import active_ready, active_ready_missing_reasons

ERROR_LESSON_JSON_BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
ERROR_LESSON_JSON_END = "KANDA_ERROR_LESSON_JSON_END"

ALLOWED_ERROR_LESSON_FORM_KEYS = {
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
}

_REQUIRED_ACTIVE_AI_KEYS = (
    "schema_version",
    "lesson_id",
    "status",
    "project_slug",
    "operation_phase",
    "created_at_utc",
    "updated_at_utc",
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
)

_VALIDATION_SUCCESS_MARKERS = (
    "validation ok",
    "status: in_sync",
    "zip contract: pass",
    "passed",
    "passou",
    "success",
    "install ok",
)

_VALIDATION_FAILURE_MARKERS = (
    "validation failed",
    "traceback",
    "error:",
    "failed before correction",
    "not corrected yet",
    "needs investigation",
)

_UNCERTAIN_FIX_MARKERS = (
    "should be corrected",
    "should be",
    "likely",
    "probably",
    "needs",
    "need to",
    "rerun validation",
    "after correction",
    "pending correction",
    "not corrected",
)


def _contains_any_marker(values: Any, markers: tuple[str, ...]) -> bool:
    """Return whether any normalized value contains one of the markers."""
    if isinstance(values, (list, tuple, set)):
        text = "\n".join(str(item or "") for item in values)
    else:
        text = str(values or "")
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def _has_successful_validation_evidence(form_inputs: Mapping[str, Any]) -> bool:
    """Return whether the AI form includes evidence that the repair passed."""
    values = [
        form_inputs.get("validation_evidence"),
        form_inputs.get("validation_command_summary"),
        form_inputs.get("notes"),
    ]
    return any(_contains_any_marker(value, _VALIDATION_SUCCESS_MARKERS) for value in values)


def _should_force_draft_status(form_inputs: Mapping[str, Any]) -> bool:
    """Return True when the AI form describes an unvalidated or pre-correction error."""
    if str(form_inputs.get("status") or "").strip().lower() == "draft":
        return True
    if not _has_successful_validation_evidence(form_inputs):
        failure_values = [
            form_inputs.get("raw_error_text"),
            form_inputs.get("validation_evidence"),
            form_inputs.get("validation_command_summary"),
            form_inputs.get("notes"),
        ]
        if any(_contains_any_marker(value, _VALIDATION_FAILURE_MARKERS) for value in failure_values):
            return True
        uncertain_values = [
            form_inputs.get("correct_fix"),
            form_inputs.get("long_term_prevention"),
            form_inputs.get("notes"),
        ]
        if any(_contains_any_marker(value, _UNCERTAIN_FIX_MARKERS) for value in uncertain_values):
            return True
    return False


def _coerce_status_for_ai_form(form_inputs: Mapping[str, Any], requested_status: str) -> str:
    """Return safe lesson status for AI-provided forms.

    AI can overconfidently ask for ``active`` while only describing a failed
    validation before the correction. In that case KANDA must save a draft so
    the lesson does not get exported as verified prevention guidance.
    """
    status = str(requested_status or "active").strip().lower()
    if status not in {"draft", "active", "deprecated", "superseded"}:
        status = "draft"
    if status == "active" and _should_force_draft_status(form_inputs):
        return "draft"
    return status


def _as_text(value: Any) -> str:
    """Return a stable text value for GUI/intake fields."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple, set)):
        return "\n".join(str(item).strip() for item in value if str(item).strip())
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value).strip()


def _as_list(value: Any) -> list[str]:
    """Return a clean string list from AI-provided list or multiline text."""
    if value is None:
        return []
    if isinstance(value, str):
        parts = value.replace(";", "\n").splitlines()
    elif isinstance(value, (list, tuple, set)):
        parts = list(value)
    else:
        parts = [value]
    return [str(item).strip() for item in parts if str(item).strip()]


def _normalize_regression_check_for_error_memory_json(value: Any) -> dict[str, Any] | None:
    """Normalize AI-provided regression_check while preserving corrupt escapes.

    Safe double-backslash commands are converted to forward slashes. Commands
    already corrupted into tabs/newlines are left intact so active-ready
    validation can fail closed instead of hiding the regression.
    """
    if not isinstance(value, dict):
        return None
    result = dict(value)
    command = str(result.get("command") or "").strip()
    if command:
        has_control = any(char in command for char in "\t\r\n\v\f\b")
        if not has_control:
            result["command"] = command.replace("\\", "/")
        else:
            result["command"] = command
    return result


def _normalize_redaction_for_error_memory_json(value: Any) -> dict[str, Any] | None:
    """Normalize AI-provided redaction metadata to the active-ready contract."""
    if not isinstance(value, dict):
        return None
    result = dict(value)
    rules = _as_list(result.get("rules"))
    if not rules:
        note_rules = _as_list(result.get("notes"))
        if note_rules:
            rules = note_rules
    if rules:
        result["rules"] = rules
    return result


def _downgrade_non_active_ready_lesson(lesson: dict[str, Any]) -> None:
    """Downgrade invalid active AI lessons to draft with explicit reasons."""
    if str(lesson.get("status") or "").strip().lower() != "active":
        return
    if active_ready(lesson):
        return
    failures = active_ready_missing_reasons(lesson)
    lesson["status"] = "draft"
    reason_text = "; ".join(failures[:8])
    note = str(lesson.get("notes") or "").strip()
    suffix = "Auto-downgraded from active because active-ready validation failed: " + reason_text
    lesson["notes"] = (note + "\n" + suffix).strip() if note else suffix
