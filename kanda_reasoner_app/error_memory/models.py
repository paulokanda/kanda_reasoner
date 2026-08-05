# project-path: kanda_reasoner_app/error_memory/models.py
"""Data-model builders for KANDA Error Memory lessons."""

from __future__ import annotations


__all__ = ['active_ready', 'active_ready_missing_reasons', 'build_lesson', 'compact_lesson']
from datetime import datetime, timezone
import uuid
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.project_analysis_evidence_paths import project_name_from_root

from .fingerprint import build_fingerprint, extract_exception_info
from .scrubber import scrub_text

ACTIVE_REQUIRED_PRESENT_FIELDS = (
    "schema_version",
    "lesson_id",
    "status",
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
)

ACTIVE_REQUIRED_MEANINGFUL_FIELDS = (
    "schema_version",
    "lesson_id",
    "status",
    "project_slug",
    "operation_phase",
    "raw_error_text",
    "raw_error_snapshot_scrubbed",
    "symptom",
    "root_cause",
    "wrong_assumption",
    "correct_fix",
    "long_term_prevention",
    "do_not_repeat_rule",
    "validation_command_summary",
    "validation_evidence",
    "prevention_triggers",
)

EXCEPTION_REQUIRED_FIELDS = (
    "type",
    "phase",
    "relative_file_path",
    "function_or_test_name",
    "message_normalized",
    "stacktrace_scrubbed",
)

EXCEPTION_REQUIRED_MEANINGFUL_FIELDS = (
    "type",
    "phase",
    "message_normalized",
)

FINGERPRINT_REQUIRED_FIELDS = (
    "strategy",
    "components",
    "fingerprint_hash",
)

REGRESSION_CHECK_REQUIRED_FIELDS = (
    "type",
    "command",
    "expected_marker",
    "required_before_freeze",
)


def utc_now_iso() -> str:
    """Return current UTC timestamp in stable ISO format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def new_lesson_id() -> str:
    """Return a stable lesson identifier."""
    return "lesson-" + uuid.uuid4().hex[:12]


def _as_list(value: Any) -> list[str]:
    """Support as list behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if value is None:
        return []
    if isinstance(value, str):
        candidates = value.replace(";", "\n").splitlines()
    elif isinstance(value, (list, tuple, set)):
        candidates = list(value)
    else:
        candidates = [value]
    return [str(item).strip() for item in candidates if str(item).strip()]


def _is_missing_value(value: Any) -> bool:
    """Support is missing value behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return value is None or value == "" or value == [] or value == {}


def _as_mapping(value: Any) -> Mapping[str, Any]:
    """Support as mapping behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    Mapping[str, Any]
        The mapped values.
    """
    
    return value if isinstance(value, Mapping) else {}


def active_ready_missing_reasons(payload: dict[str, Any]) -> list[str]:
    """Return reasons an active Error Memory lesson is not memorization-ready.

    This mirrors the AI-assisted intake contract: an active receive block must be
    complete enough to save directly through Memorize Error without relying on the
    user or the GUI to invent missing lesson metadata.
    """
    failures: list[str] = []

    missing = [key for key in ACTIVE_REQUIRED_PRESENT_FIELDS if key not in payload]
    failures.extend("missing key: " + key for key in missing)

    for key in ACTIVE_REQUIRED_MEANINGFUL_FIELDS:
        if key not in payload:
            continue
        if key in {"prevention_triggers", "validation_evidence"}:
            if not _as_list(payload.get(key)):
                failures.append(key + " must be a non-empty list")
        elif _is_missing_value(payload.get(key)):
            failures.append(key + " is empty")

    if str(payload.get("schema_version", "")).strip() != "1.0":
        failures.append("schema_version must be 1.0")
    if str(payload.get("status", "")).strip().lower() not in {"active", "draft", "deprecated", "superseded"}:
        failures.append("status is invalid")

    exception = payload.get("exception")
    if not isinstance(exception, Mapping):
        failures.append("exception must be an object")
    else:
        for key in EXCEPTION_REQUIRED_FIELDS:
            if key not in exception:
                failures.append("exception missing key: " + key)
        for key in EXCEPTION_REQUIRED_MEANINGFUL_FIELDS:
            if _is_missing_value(exception.get(key)):
                failures.append("exception." + key + " is empty")

    fingerprint = payload.get("fingerprint")
    if not isinstance(fingerprint, Mapping):
        failures.append("fingerprint must be an object")
    else:
        for key in FINGERPRINT_REQUIRED_FIELDS:
            if key not in fingerprint:
                failures.append("fingerprint missing key: " + key)
        if _is_missing_value(fingerprint.get("strategy")):
            failures.append("fingerprint.strategy is empty")
        if not _as_list(fingerprint.get("components")):
            failures.append("fingerprint.components must be a non-empty list")
        if _is_missing_value(fingerprint.get("fingerprint_hash")):
            failures.append("fingerprint.fingerprint_hash is empty")

    redaction = payload.get("redaction")
    if not isinstance(redaction, Mapping):
        failures.append("redaction must be an object")
    else:
        if not redaction.get("applied"):
            failures.append("redaction.applied must be true")
        if not redaction.get("export_safe"):
            failures.append("redaction.export_safe must be true")
        if not _as_list(redaction.get("rules")):
            failures.append("redaction.rules must be a non-empty list")

    for key in ("source_patch_zip", "install_command_summary", "notes"):
        if key in payload and _is_missing_value(payload.get(key)):
            failures.append(key + " is empty")

    regression_check = payload.get("regression_check")
    if not isinstance(regression_check, Mapping):
        failures.append("regression_check must be an object")
    else:
        for key in REGRESSION_CHECK_REQUIRED_FIELDS:
            if key not in regression_check:
                failures.append("regression_check missing key: " + key)
        check_type = str(regression_check.get("type", "")).strip()
        if not check_type:
            failures.append("regression_check.type is empty")
        if check_type != "validation_command":
            failures.append("regression_check.type must be validation_command for active-ready lessons")
        command = str(regression_check.get("command", "") or "")
        expected_marker = str(regression_check.get("expected_marker", "") or "")
        if not command.strip():
            failures.append("regression_check.command is empty for validation_command")
        if not expected_marker.strip():
            failures.append("regression_check.expected_marker is empty for validation_command")
        if "\\" in command:
            failures.append("regression_check.command must use forward slashes")
        if any(ord(ch) < 32 for ch in command):
            failures.append("regression_check.command contains a control character")

    return failures


def active_ready(payload: dict[str, Any]) -> bool:
    """Return whether a lesson has the fields required for active export/save."""
    return not active_ready_missing_reasons(payload)


def build_lesson(
    *,
    selected_project_root: str | Path,
    raw_error_text: str = "",
    operation_phase: str = "unknown",
    symptom: str = "",
    root_cause: str = "",
    wrong_assumption: str = "",
    correct_fix: str = "",
    long_term_prevention: str = "",
    do_not_repeat_rule: str = "",
    prevention_triggers: Any = None,
    validation_evidence: Any = None,
    regression_check: dict[str, Any] | None = None,
    status: str = "draft",
    lesson_id: str | None = None,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a canonical Lesson dict from GUI/user inputs."""
    now = utc_now_iso()
    base = dict(existing or {})
    created_at = str(base.get("created_at_utc") or now)
    raw_input = str(raw_error_text or base.get("raw_error_text") or "").strip()
    exception = extract_exception_info(raw_input, selected_project_root=selected_project_root, operation_phase=operation_phase)
    fingerprint = build_fingerprint(exception)
    redacted_raw = scrub_text(raw_input)
    scrubbed_raw_text = redacted_raw.text[:4000]
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "lesson_id": lesson_id or str(base.get("lesson_id") or new_lesson_id()),
        "status": status,
        "superseded_by": str(base.get("superseded_by") or ""),
        "project_slug": project_name_from_root(selected_project_root),
        "created_at_utc": created_at,
        "updated_at_utc": now,
        "source_patch_zip": str(base.get("source_patch_zip") or ""),
        "raw_error_text": scrubbed_raw_text,
        "symptom": symptom.strip(),
        "operation_phase": str(operation_phase or "unknown"),
        "root_cause": root_cause.strip(),
        "wrong_assumption": wrong_assumption.strip(),
        "correct_fix": correct_fix.strip(),
        "long_term_prevention": long_term_prevention.strip(),
        "do_not_repeat_rule": do_not_repeat_rule.strip(),
        "prevention_triggers": _as_list(prevention_triggers),
        "exception": exception,
        "fingerprint": fingerprint,
        "regression_check": regression_check or {
            "type": "not_available",
            "command": "",
            "expected_marker": "",
            "required_before_freeze": False,
        },
        "validation_command_summary": str(base.get("validation_command_summary") or ""),
        "validation_evidence": _as_list(validation_evidence),
        "redaction": {
            "applied": True,
            "export_safe": True,
            "rules": list(redacted_raw.rules),
        },
        "raw_error_snapshot_scrubbed": scrubbed_raw_text,
        "install_command_summary": str(base.get("install_command_summary") or ""),
        "notes": str(base.get("notes") or ""),
        "related_freeze_ids": _as_list(base.get("related_freeze_ids")),
        "promotion_status": str(base.get("promotion_status") or "not_candidate"),
    }
    if payload["status"] == "active" and not active_ready(payload):
        payload["status"] = "draft"
    return payload


def compact_lesson(lesson: dict[str, Any]) -> dict[str, Any]:
    """Return a compact AI-safe lesson projection."""
    return {
        "lesson_id": lesson.get("lesson_id", ""),
        "status": lesson.get("status", ""),
        "symptom": lesson.get("symptom", ""),
        "operation_phase": lesson.get("operation_phase", ""),
        "root_cause": lesson.get("root_cause", ""),
        "correct_fix": lesson.get("correct_fix", ""),
        "long_term_prevention": lesson.get("long_term_prevention", ""),
        "do_not_repeat_rule": lesson.get("do_not_repeat_rule", ""),
        "prevention_triggers": list(lesson.get("prevention_triggers", []) or []),
        "exception": dict(lesson.get("exception", {}) or {}),
        "fingerprint": dict(lesson.get("fingerprint", {}) or {}),
        "regression_check": dict(lesson.get("regression_check", {}) or {}),
        "validation_evidence": list(lesson.get("validation_evidence", []) or []),
        "source_patch_zip": lesson.get("source_patch_zip", ""),
        "raw_error_text": lesson.get("raw_error_text", ""),
        "raw_error_snapshot_scrubbed": lesson.get("raw_error_snapshot_scrubbed", ""),
        "install_command_summary": lesson.get("install_command_summary", ""),
        "validation_command_summary": lesson.get("validation_command_summary", ""),
        "notes": lesson.get("notes", ""),
        "superseded_by": lesson.get("superseded_by", ""),
        "owner_scope": lesson.get("owner_scope", ""),
        "owner_id": lesson.get("owner_id", ""),
        "owner_slug": lesson.get("owner_slug", ""),
        "owner_root_fingerprint": lesson.get("owner_root_fingerprint", ""),
        "affected_box": lesson.get("affected_box", ""),
    }
