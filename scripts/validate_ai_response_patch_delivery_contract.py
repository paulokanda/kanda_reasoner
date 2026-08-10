# project-path: scripts/validate_ai_response_patch_delivery_contract.py
"""Shared contract constants and primitive checks for patch delivery validation."""

from __future__ import annotations

__all__ = []  # Implementation-only module; public facade owns exported validator symbols.

import re
import zipfile
from pathlib import Path

__all__ = ['ResponseValidationError', 'validate_response_text', 'validate_zip_member_names']

REQUIRED_GATE_FIELDS = (
    "PATCH DELIVERY GATE",
    "ZIP purpose:",
    "ZIP placement path:",
    "What this ZIP is:",
    "What this ZIP is not:",
    "Install code present:",
    "Validation code present:",
    "Expected validation markers:",
    "Changed files:",
    "Allowed write paths:",
    "Forbidden write paths:",
    "Freeze/freeze-intake:",
    "Error Memory payload:",
    "Post-validation steps:",
    "What not to do:",
    "Beginner-safe:",
    "GATE STATUS: PASS",
)

ZIP_PATTERN = re.compile(
    r"(?i)(sandbox:/[^\s)\]]+\.zip|https?://[^\s)\]]+\.zip|[A-Za-z0-9_.-]+\.zip)"
)
CODE_FENCE_PATTERN = re.compile(
    r"```(?:powershell|ps1|text|bash|cmd)?\s*(.*?)```",
    re.IGNORECASE | re.DOTALL,
)

DAILY_WORK_TOKEN = "_delete_after_daily_work"
PROJECT_ROOT_TERMS = (
    "active project root",
    "project root",
    "$project_root",
)
TRANSIENT_TERMS = (
    "transient",
    "temporary",
    "temp",
    "install",
    "patch",
    "correction",
    "validation helper",
    "helper",
    "one-use",
    "staging",
)
FORBIDDEN_INSTALL_BLOCK_TERMS = ("downloads", "desktop")
FORBIDDEN_TERMINAL_CLOSING_TERMS = (
    "exit 1",
    "exit(1)",
    "stop-process",
    "restart-computer",
)
OLD_TERMINAL_FOOTER_TERMS = (
    "start-sleep -seconds 5",
    "press enter again to finish",
)
FORBIDDEN_INLINE_PYTHON_TERMS = (
    "python -c",
    "python.exe -c",
    "py -c",
)
INSTALL_SUCCESS_TERMINAL_TERMS = (
    "install ok. terminal will clear in 2 seconds",
    "start-sleep -seconds 2",
    "clear-host",
)
NON_INSTALL_TERMINAL_TERMS = (
    'read-host "press enter to clear terminal"',
    'read-host "press enter again to clear"',
    "clear-host",
)

RECEIVER_CLASSIFICATION_VALUES = (
    "SOURCE_PATCH",
    "FREEZE_HINT_INTAKE",
    "MANUAL_FREEZE_FORM_RECEIVER",
    "ERROR_MEMORY_AI_ASSISTED_INTAKE",
    "STORAGE_ONLY_MANUAL_HELPER",
)
RECEIVER_GATE_FIELDS = (
    "RECEIVER DELIVERY CHECK",
    "Receiver classification:",
    "Actual receiver path or action:",
    "Installer stages to receiver:",
    "Manual paste required:",
    "Storage-only helper:",
    "Receiver proof:",
    "RECEIVER STATUS: PASS",
)
ERROR_MEMORY_INTAKE_TOKEN = "pending_ai_assisted_error_lesson_intake"
FREEZE_HINT_INTAKE_TOKEN = "freeze_hint_intake"
FREEZE_FORM_BEGIN = "KANDA_FREEZE_FORM_JSON_BEGIN"
FREEZE_FORM_END = "KANDA_FREEZE_FORM_JSON_END"
ERROR_LESSON_BEGIN = "KANDA_ERROR_LESSON_JSON_BEGIN"
ERROR_LESSON_END = "KANDA_ERROR_LESSON_JSON_END"

ERROR_MEMORY_REQUIRED_ACTIVE_FIELDS = (
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
    "exception",
    "fingerprint",
    "prevention_triggers",
    "redaction",
    "regression_check",
    "validation_command_summary",
    "validation_evidence",
    "install_command_summary",
    "notes",
)
FREEZE_FORM_REQUIRED_FIELDS = (
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
)


class ResponseValidationError(RuntimeError):
    """Raised when the AI response violates the patch delivery contract."""


def _fail(message: str) -> None:
    """Support fail behavior.
    
    Parameters
    ----------
    message : str
        The message text.
    """
    
    raise ResponseValidationError(message)


def _has_zip_reference(text: str) -> bool:
    """Support has zip reference behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return bool(ZIP_PATTERN.search(text))


def _code_blocks(text: str) -> list[str]:
    """Support code blocks behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return [match.group(1) for match in CODE_FENCE_PATTERN.finditer(text)]


def _unsafe_zip_member_reason(name: str) -> str | None:
    """Support unsafe zip member reason behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    
    Returns
    -------
    str | None
        The string result.
    """
    
    if not name or "\x00" in name:
        return "empty or null-containing member name"
    normalized = name.replace("\\", "/")
    if normalized.startswith("/"):
        return "absolute member path"
    if re.match(r"^[A-Za-z]:", normalized):
        return "drive-prefixed member path"
    if any(part == ".." for part in normalized.split("/")):
        return "path traversal member"
    return None


def validate_zip_member_names(zip_path: str | Path) -> list[str]:
    """Return safe ZIP member names or raise ResponseValidationError."""
    path = Path(zip_path)
    if not path.is_file():
        _fail("ZIP file not found for member safety validation: " + str(path))
    safe_names: list[str] = []
    with zipfile.ZipFile(path) as archive:
        for info in archive.infolist():
            reason = _unsafe_zip_member_reason(info.filename)
            if reason:
                _fail("Unsafe ZIP member rejected: " + info.filename + " (" + reason + ")")
            safe_names.append(info.filename)
    return safe_names
