# project-path: kanda_reasoner_app/error_memory_gui/_ai_response_validator.py
"""Strict parser and safe normalizer for AI-corrected Error Memory JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from kanda_reasoner_app.error_memory.intake_normalization import (
    _normalize_regression_check_for_error_memory_json,
)
from kanda_reasoner_app.error_memory.models import active_ready_missing_reasons

__all__ = [
    "AIResponseValidationError",
    "ValidatedLessonBlock",
    "build_source_lesson_defaults",
    "format_lesson_block",
    "parse_one_lesson_block",
]

BEGIN_MARKER = "KANDA_ERROR_LESSON_JSON_BEGIN"
END_MARKER = "KANDA_ERROR_LESSON_JSON_END"
REQUIRED_FIELDS = (
    "schema_version",
    "project_slug",
    "lesson_id",
    "status",
    "superseded_by",
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
    "do_not_repeat_rule",
    "long_term_prevention",
    "redaction",
    "exception",
    "fingerprint",
    "prevention_triggers",
    "regression_check",
    "validation_command_summary",
    "validation_evidence",
    "install_command_summary",
    "notes",
)
SUPERSEDE_ALIASES = (
    "supersede",
    "superseed",
    "superseeded_by",
    "supersedes",
)
DEFAULT_MISSING_VALIDATION_EVIDENCE = (
    "No successful validation evidence was provided in the input; keep status draft."
)

class AIResponseValidationError(ValueError):
    """Raised when a local AI response is not one valid lesson block."""

@dataclass(frozen=True)
class ValidatedLessonBlock:
    """Validated lesson payload plus formatted block text."""

    lesson: dict[str, Any]
    formatted_text: str
    warning: str = ""

def _block_count(text: str) -> int:
    """Return the number of begin/end marker pairs in text."""
    return min(text.count(BEGIN_MARKER), text.count(END_MARKER))

def _extract_json_text(text: str) -> str:
    """Extract exactly one marker-wrapped JSON payload."""
    raw = str(text or "").strip()
    if _block_count(raw) != 1:
        raise AIResponseValidationError(
            "AI response must contain exactly one KANDA_ERROR_LESSON_JSON block."
        )
    begin_index = raw.find(BEGIN_MARKER)
    end_index = raw.find(END_MARKER)
    if begin_index < 0 or end_index < 0 or end_index <= begin_index:
        raise AIResponseValidationError("AI response markers are missing or out of order.")
    before = raw[:begin_index].strip()
    after = raw[end_index + len(END_MARKER):].strip()
    if before or after:
        raise AIResponseValidationError(
            "AI response must not contain prose outside the lesson markers."
        )
    return raw[begin_index + len(BEGIN_MARKER):end_index].strip()

def _find_first_json_object(text: str) -> str:
    """Return the first balanced JSON object from free text."""
    raw = str(text or "")
    start = raw.find("{")
    if start < 0:
        return ""
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(raw)):
        char = raw[index]
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return raw[start:index + 1]
    return ""

def _load_lesson_candidate(text: str) -> dict[str, Any]:
    """Load one lesson-like JSON object from marker text or raw JSON text."""
    raw = str(text or "").strip()
    if not raw:
        return {}
    if BEGIN_MARKER in raw and END_MARKER in raw and _block_count(raw) >= 1:
        begin_index = raw.find(BEGIN_MARKER)
        end_index = raw.find(END_MARKER, begin_index)
        json_text = raw[begin_index + len(BEGIN_MARKER):end_index].strip()
    else:
        json_text = _find_first_json_object(raw)
    if not json_text:
        return {}
    try:
        loaded = json.loads(json_text)
    except json.JSONDecodeError:
        return {}
    if isinstance(loaded, dict):
        return loaded
    return {}

def build_source_lesson_defaults(*texts: str) -> dict[str, Any]:
    """Build safe fallback fields from current intake/editor lesson text."""
    for text in texts:
        candidate = _load_lesson_candidate(text)
        if candidate:
            return candidate
    return {}

def _as_list(value: Any) -> list[str]:
    """Return normalized non-empty strings from a field value."""
    if value is None:
        return []
    if isinstance(value, str):
        items = value.splitlines()
    elif isinstance(value, (list, tuple, set)):
        items = list(value)
    else:
        items = [value]
    return [str(item).strip() for item in items if str(item).strip()]

def _normalize_list_field(payload: dict[str, Any], key: str, warnings: list[str]) -> None:
    """Normalize a field that must behave as a string list."""
    if key in payload and not isinstance(payload.get(key), list):
        items = _as_list(payload.get(key))
        payload[key] = items
        if items:
            warnings.append(key + " was normalized to a list.")

def _normalize_validation_evidence(payload: dict[str, Any], warnings: list[str]) -> None:
    """Normalize missing or empty validation evidence without inventing success."""
    items = _as_list(payload.get("validation_evidence"))
    if not items:
        payload["validation_evidence"] = [DEFAULT_MISSING_VALIDATION_EVIDENCE]
        payload["status"] = "draft"
        warnings.append("Missing validation_evidence was normalized to a draft-only note.")
        return
    if not isinstance(payload.get("validation_evidence"), list):
        payload["validation_evidence"] = items
        warnings.append("validation_evidence was normalized to a list.")

def _has_successful_validation_evidence(lesson: dict[str, Any]) -> bool:
    """Return whether validation_evidence contains non-placeholder evidence."""
    items = _as_list(lesson.get("validation_evidence"))
    if not items:
        return False
    joined = "\n".join(items).lower()
    blocked_fragments = (
        "no successful validation evidence",
        "expected marker",
        "expected regression target only",
        "pending intake lesson staged only",
        "human review and memorize error remain required",
    )
    return not any(fragment in joined for fragment in blocked_fragments)

def _normalize_regression_command(payload: dict[str, Any], warnings: list[str]) -> None:
    """Apply the canonical Error Memory regression-command normalizer."""
    regression = payload.get("regression_check")
    normalized = _normalize_regression_check_for_error_memory_json(regression)
    if normalized is None:
        return
    if normalized != regression:
        payload["regression_check"] = normalized
        warnings.append("regression_check.command was normalized to forward slashes.")


def _validate_regression_check_contract(payload: dict[str, Any]) -> None:
    """Reject model output that Memorize Error would reject later."""
    failures = [
        reason
        for reason in active_ready_missing_reasons(payload)
        if reason.startswith("regression_check")
    ]
    if failures:
        raise AIResponseValidationError(
            "Regression check is not active-ready: " + "; ".join(failures)
        )

def _normalize_superseded_by(payload: dict[str, Any], warnings: list[str]) -> None:
    """Add or repair the superseded_by field when the AI omitted it."""
    if "superseded_by" in payload:
        if payload["superseded_by"] is None:
            payload["superseded_by"] = ""
            warnings.append("superseded_by None was normalized to an empty string.")
        return
    for alias in SUPERSEDE_ALIASES:
        if alias in payload:
            payload["superseded_by"] = str(payload.get(alias) or "").strip()
            warnings.append("superseded_by was recovered from " + alias + ".")
            return
    payload["superseded_by"] = ""
    warnings.append("Missing superseded_by was normalized to an empty string.")

def _normalize_status(payload: dict[str, Any], warnings: list[str]) -> None:
    """Normalize known status variants returned by local models."""
    status = str(payload.get("status", "")).strip().lower()
    if status == "active_ready":
        payload["status"] = "draft"
        warnings.append("status active_ready was normalized to draft for human review.")
    elif status:
        payload["status"] = status

def _merge_missing_source_defaults(
    payload: dict[str, Any],
    source_defaults: dict[str, Any] | None,
    warnings: list[str],
) -> None:
    """Fill missing or blank top-level fields from the source lesson text."""
    defaults = source_defaults or {}
    if not isinstance(defaults, dict):
        return
    for key in REQUIRED_FIELDS:
        if key not in defaults:
            continue
        default_value = defaults.get(key)
        if _blank_like(default_value):
            continue
        if key not in payload or _blank_like(payload.get(key)):
            payload[key] = default_value
            warnings.append(key + " was recovered from the source lesson.")

def _safe_regression_command(payload: dict[str, Any]) -> str:
    """Return a regression command-like string from the payload."""
    regression = payload.get("regression_check")
    if isinstance(regression, dict):
        command = str(regression.get("command") or "").strip()
        if command:
            return command
    return "not specified"

_EXCEPTION_REQUIRED_KEYS = (
    "type",
    "phase",
    "relative_file_path",
    "function_or_test_name",
    "message_normalized",
    "stacktrace_scrubbed",
)

def _blank_like(value: Any) -> bool:
    """Return whether a local model left a required value effectively blank."""
    text = str(value or "").strip()
    lowered = text.lower()
    placeholders = {
        "n/a", "none", "null", "not_available", "not available",
        "<artifact-or-patch-name>", "<patch_zip_name_or_relevant_artifact>",
        "<wrong assumption>", "<install summary>", "<notes>",
    }
    return text == "" or lowered in placeholders or (text.startswith("<") and text.endswith(">"))

def _fallback_exception_from_payload(payload: dict[str, Any]) -> dict[str, str]:
    """Create truthful draft-safe exception fields from existing lesson fields."""
    phase = str(payload.get("operation_phase") or "unknown").strip() or "unknown"
    raw_error = str(payload.get("raw_error_text") or payload.get("symptom") or "").strip()
    if not raw_error:
        raw_error = "Error Memory lesson correction issue."
    snapshot = str(payload.get("raw_error_snapshot_scrubbed") or "").strip()
    if not snapshot:
        snapshot = "No traceback was provided; exception details were derived from lesson fields."
    relative_path = str(payload.get("source_patch_zip") or "").strip()
    if not relative_path:
        relative_path = str(payload.get("exception_surface") or "Error Memory AI correction").strip()
    return {
        "type": "ErrorMemoryLessonCorrectionIssue",
        "phase": phase,
        "relative_file_path": relative_path,
        "function_or_test_name": _safe_regression_command(payload),
        "message_normalized": raw_error,
        "stacktrace_scrubbed": snapshot,
    }

def _derive_exception_from_payload(payload: dict[str, Any], warnings: list[str]) -> None:
    """Create or complete truthful draft exception fields from existing lesson data."""
    fallback = _fallback_exception_from_payload(payload)
    current = payload.get("exception")
    if not isinstance(current, dict):
        payload["exception"] = fallback
        payload["status"] = "draft"
        warnings.append("Missing exception was reconstructed from existing lesson fields.")
        return
    repaired = dict(current)
    changed = False
    for key in _EXCEPTION_REQUIRED_KEYS:
        if _blank_like(repaired.get(key)):
            repaired[key] = fallback[key]
            changed = True
    if changed:
        payload["exception"] = repaired
        payload["status"] = "draft"
        warnings.append("Blank exception fields were reconstructed from existing lesson fields.")

def _recover_source_patch_zip(payload: dict[str, Any], warnings: list[str]) -> None:
    """Recover source_patch_zip as a non-empty relevant artifact when possible."""
    if not _blank_like(payload.get("source_patch_zip")):
        return
    regression = payload.get("regression_check")
    command = str(regression.get("command") or "").strip() if isinstance(regression, dict) else ""
    if command:
        artifact = command.replace("\\", "/").split("/")[-1].strip() or command
        payload["source_patch_zip"] = artifact
        warnings.append("source_patch_zip was recovered from regression_check.command.")
        return
    exception = payload.get("exception")
    rel_path = str(exception.get("relative_file_path") or "").strip() if isinstance(exception, dict) else ""
    if rel_path and rel_path.lower() not in {"error memory ai correction", "unknown"}:
        payload["source_patch_zip"] = rel_path.replace("\\", "/")
        warnings.append("source_patch_zip was recovered from exception.relative_file_path.")

def _normalize_lesson_payload(
    lesson: dict[str, Any],
    source_defaults: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Apply safe deterministic repairs before strict validation."""
    payload = dict(lesson)
    warnings: list[str] = []
    _merge_missing_source_defaults(payload, source_defaults, warnings)
    _normalize_superseded_by(payload, warnings)
    _normalize_status(payload, warnings)
    _derive_exception_from_payload(payload, warnings)
    _recover_source_patch_zip(payload, warnings)
    _normalize_regression_command(payload, warnings)
    _normalize_validation_evidence(payload, warnings)
    _normalize_list_field(payload, "prevention_triggers", warnings)
    fingerprint = payload.get("fingerprint")
    if isinstance(fingerprint, dict) and not isinstance(fingerprint.get("components"), list):
        components = _as_list(fingerprint.get("components"))
        payload["fingerprint"] = dict(fingerprint, components=components)
        if components:
            warnings.append("fingerprint.components was normalized to a list.")
    redaction = payload.get("redaction")
    if isinstance(redaction, dict) and not isinstance(redaction.get("rules"), list):
        rules = _as_list(redaction.get("rules"))
        payload["redaction"] = dict(redaction, rules=rules)
        if rules:
            warnings.append("redaction.rules was normalized to a list.")
    return payload, warnings

def _validate_required_fields(lesson: dict[str, Any]) -> None:
    """Validate baseline Error Memory lesson fields."""
    missing = [key for key in REQUIRED_FIELDS if key not in lesson]
    if missing:
        raise AIResponseValidationError("Lesson is missing field(s): " + ", ".join(missing))
    if str(lesson.get("schema_version", "")).strip() != "1.0":
        raise AIResponseValidationError("schema_version must be 1.0.")
    if not str(lesson.get("lesson_id", "")).strip().startswith("lesson-"):
        raise AIResponseValidationError("lesson_id must start with lesson-.")
    if str(lesson.get("status", "")).strip() not in {
        "active",
        "draft",
        "deprecated",
        "superseded",
    }:
        raise AIResponseValidationError("status must be active, draft, deprecated, or superseded.")
    if not isinstance(lesson.get("exception"), dict):
        raise AIResponseValidationError("exception must be an object.")
    if not isinstance(lesson.get("fingerprint"), dict):
        raise AIResponseValidationError("fingerprint must be an object.")
    if not isinstance(lesson.get("regression_check"), dict):
        raise AIResponseValidationError("regression_check must be an object.")
    if not _as_list(lesson.get("prevention_triggers")):
        raise AIResponseValidationError("prevention_triggers must be a non-empty list.")
    if not _as_list(lesson.get("validation_evidence")):
        raise AIResponseValidationError("validation_evidence must be a non-empty list.")

def _reject_blank_active_ready_text_fields(lesson: dict[str, Any]) -> None:
    """Reject local-AI answers that leave active-ready text fields blank."""
    blank = [
        key for key in (
            "source_patch_zip", "wrong_assumption",
            "install_command_summary", "notes",
        )
        if _blank_like(lesson.get(key))
    ]
    if blank:
        raise AIResponseValidationError(
            "Lesson has blank active-ready text field(s): " + ", ".join(blank)
        )

def _looks_active_ready(lesson: dict[str, Any]) -> bool:
    """Return whether key active-ready evidence fields are present."""
    redaction = lesson.get("redaction")
    regression = lesson.get("regression_check")
    if not isinstance(redaction, dict) or not isinstance(regression, dict):
        return False
    if not redaction.get("applied") or not redaction.get("export_safe"):
        return False
    if not _as_list(redaction.get("rules")):
        return False
    if str(regression.get("type", "")).strip() != "validation_command":
        return False
    if not str(regression.get("command", "")).strip():
        return False
    if not str(regression.get("expected_marker", "")).strip():
        return False
    if "\\" in str(regression.get("command", "")):
        return False
    return True

def _force_draft_when_not_active_ready(lesson: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Downgrade non-active-ready active lessons to draft with a warning."""
    payload = dict(lesson)
    if str(payload.get("status", "")).strip() != "active":
        return payload, ""
    if _looks_active_ready(payload):
        return payload, ""
    payload["status"] = "draft"
    return payload, "AI returned active status but active-ready checks failed; status changed to draft."

def format_lesson_block(lesson: dict[str, Any]) -> str:
    """Serialize one lesson as a marker-wrapped intake block."""
    return (
        BEGIN_MARKER
        + "\n"
        + json.dumps(dict(lesson), indent=2, sort_keys=True, ensure_ascii=True)
        + "\n"
        + END_MARKER
    )

def _source_intends_active(source_defaults: dict[str, Any] | None) -> bool:
    """Return whether the source lesson is awaiting human approval as active."""
    source = source_defaults or {}
    if not isinstance(source, dict):
        return False
    status = str(source.get("status", "") or "").strip().lower()
    intended = str(source.get("intended_status", "") or "").strip().lower()
    return status == "active" or (status == "pending" and intended == "active")


def _enforce_memorize_ready_target(
    payload: dict[str, Any],
    source_defaults: dict[str, Any] | None,
    warnings: list[str],
) -> dict[str, Any]:
    """Make Local-AI success use the same active-ready gate as Memorize Error.

    A pending transport candidate whose intended_status is active remains
    uncommitted until the human presses Memorize Error.  The AI preview may,
    however, be normalized to status active only after the canonical
    active_ready_missing_reasons() contract passes.  If it does not pass, raise
    validation feedback so the Local-AI service performs its existing retry
    instead of displaying a misleading "corrected" draft that Memorize Error
    will immediately reject.
    """
    candidate = dict(payload)
    output_status = str(candidate.get("status", "") or "").strip().lower()
    target_active = output_status == "active" or _source_intends_active(source_defaults)
    if not target_active:
        return candidate

    check = dict(candidate)
    check["status"] = "active"
    check.pop("intended_status", None)
    failures = active_ready_missing_reasons(check)
    if failures:
        raise AIResponseValidationError(
            "Correction is not Memorize-ready under canonical Error Memory "
            "active-ready validation: "
            + "; ".join(failures[:20])
        )

    if output_status != "active":
        warnings.append(
            "Source is intended for active human approval and the corrected "
            "payload passed canonical Memorize Error active-ready validation; "
            "preview status normalized to active. The pending source is still "
            "not consumed until explicit human Memorize Error."
        )
    return check


def parse_one_lesson_block(
    response_text: str,
    source_defaults: dict[str, Any] | None = None,
) -> ValidatedLessonBlock:
    """Return one validated lesson from a strict AI response.

    Local-AI correction success and human Memorize Error intentionally share
    the same canonical active-ready contract for active-intended candidates.

    Pending is a transport state, not a saved canonical status.  Therefore an
    active-intended pending correction must cross the transport-to-preview
    boundary before the saved-status validator runs.
    """
    json_text = _extract_json_text(response_text)
    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise AIResponseValidationError("Lesson JSON is invalid: " + str(exc)) from exc
    if not isinstance(payload, dict):
        raise AIResponseValidationError("Lesson payload must be one JSON object.")

    payload, warnings = _normalize_lesson_payload(payload, source_defaults)

    # Transport-aware readiness must run before _validate_required_fields().
    # That validator intentionally accepts saved lesson states only and must
    # not be broadened to make pending a canonical stored status.
    payload = _enforce_memorize_ready_target(
        payload,
        source_defaults,
        warnings,
    )

    _validate_required_fields(payload)
    _validate_regression_check_contract(payload)
    _reject_blank_active_ready_text_fields(payload)

    lesson, active_warning = _force_draft_when_not_active_ready(payload)
    if active_warning:
        warnings.append(active_warning)
    warning_text = "\n".join(warnings)
    return ValidatedLessonBlock(
        lesson=lesson,
        formatted_text=format_lesson_block(lesson),
        warning=warning_text,
    )
