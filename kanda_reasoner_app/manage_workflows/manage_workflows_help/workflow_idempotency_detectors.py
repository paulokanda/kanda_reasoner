"""Detect non-idempotent Tab 2 workflow command patterns."""

from __future__ import annotations

import re
from typing import Any

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_idempotency_issues",
]

ISSUE_IDS = {'append': 'WORKFLOW_STEP_NOT_IDEMPOTENT_APPEND_OUTPUT', 'powershell_append': 'WORKFLOW_STEP_NOT_IDEMPOTENT_APPEND_OUTPUT', 'new_item_directory': 'WORKFLOW_STEP_NOT_IDEMPOTENT_NEW_DIRECTORY', 'compress_archive': 'WORKFLOW_STEP_NOT_IDEMPOTENT_COMPRESS_ARCHIVE', 'remove_without_guard': 'WORKFLOW_STEP_NOT_IDEMPOTENT_REMOVE_ITEM'}


def _iter_command_specs(manifest: dict[str, Any]) -> list[tuple[str, Any]]:
    """Return workflow command specs with stable workflow labels."""
    workflows = manifest.get("workflows")
    if not isinstance(workflows, dict):
        return []

    found: list[tuple[str, Any]] = []
    for workflow_name, workflow_cfg in workflows.items():
        if not isinstance(workflow_cfg, dict):
            continue

        commands = workflow_cfg.get("commands") or []
        if not isinstance(commands, list):
            continue

        for index, command in enumerate(commands, start=1):
            step_name = str(workflow_name) + " command " + str(index)
            found.append((step_name, command))

    return found


def _command_text(command_spec: Any) -> str:
    """Return command text from supported workflow command shapes."""
    if isinstance(command_spec, str):
        return command_spec

    if not isinstance(command_spec, dict):
        return ""

    if "command" in command_spec:
        return str(command_spec.get("command") or "")

    args = command_spec.get("args")
    if isinstance(args, list):
        return " ".join(str(item) for item in args)

    return ""


def _is_allowed_non_idempotent(command_spec: Any, command_text: str) -> bool:
    """Return True when the workflow explicitly documents non-idempotent behavior."""
    lowered = command_text.lower()
    if "allow_non_idempotent" in lowered or "allow non idempotent" in lowered:
        return True

    if not isinstance(command_spec, dict):
        return False

    explicit_keys = (
        "allow_non_idempotent",
        "allow_non_idempotent_output",
        "allow_non_idempotent_command",
        "idempotency_exception",
    )
    for key in explicit_keys:
        value = command_spec.get(key)
        if value:
            return True

    return False


def _has_flag(command_text: str, flag: str) -> bool:
    """Return True when a PowerShell-style flag is present."""
    return re.search(r"(?i)(^|\s)" + re.escape(flag) + r"(\s|$)", command_text) is not None


def _make_issue(
    *,
    issue_id: str,
    workflow_step: str,
    evidence: str,
    expected: str,
    actual: str,
) -> WorkflowIssue:
    """Build a workflow idempotency issue."""
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_idempotency",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
    )


def _uses_append_output(command_text: str) -> bool:
    """Return True when command appends to an output instead of overwriting."""
    lowered = command_text.lower()
    if re.search(r"(?<!>)>>(?!>)", command_text):
        return True
    if "add-content" in lowered:
        return True
    if "out-file" in lowered and _has_flag(command_text, "-Append"):
        return True
    if "tee-object" in lowered and _has_flag(command_text, "-Append"):
        return True
    return False


def _uses_new_item_directory_without_force(command_text: str) -> bool:
    """Return True when a directory is created without -Force."""
    lowered = command_text.lower()
    return (
        "new-item" in lowered
        and "-itemtype" in lowered
        and "directory" in lowered
        and not _has_flag(command_text, "-Force")
    )


def _uses_compress_archive_without_force(command_text: str) -> bool:
    """Return True when Compress-Archive may fail on rerun."""
    lowered = command_text.lower()
    return "compress-archive" in lowered and not _has_flag(command_text, "-Force")


def _uses_remove_item_without_guard(command_text: str) -> bool:
    """Return True when Remove-Item is used without an existence guard."""
    lowered = command_text.lower()
    if "remove-item" not in lowered:
        return False

    guard_markers = (
        "test-path",
        "-erroraction silentlycontinue",
        "-ea silentlycontinue",
        "if (",
    )
    return not any(marker in lowered for marker in guard_markers)


def _command_issues(workflow_step: str, command_text: str) -> list[WorkflowIssue]:
    """Return idempotency issues for one command string."""
    issues: list[WorkflowIssue] = []
    stripped = command_text.strip()

    if not stripped:
        return issues

    if _uses_append_output(stripped):
        issues.append(
            _make_issue(
                issue_id=ISSUE_IDS["append"],
                workflow_step=workflow_step,
                evidence=stripped,
                expected=(
                    "Workflow commands should write deterministic outputs with "
                    "overwrite-safe operations instead of append behavior."
                ),
                actual="Command appends to an output and may accumulate stale content.",
            )
        )

    if _uses_new_item_directory_without_force(stripped):
        issues.append(
            _make_issue(
                issue_id=ISSUE_IDS["new_item_directory"],
                workflow_step=workflow_step,
                evidence=stripped,
                expected=(
                    "Directory creation should be rerunnable by using "
                    "New-Item -ItemType Directory -Force."
                ),
                actual="Command creates a directory without -Force.",
            )
        )

    if _uses_compress_archive_without_force(stripped):
        issues.append(
            _make_issue(
                issue_id=ISSUE_IDS["compress_archive"],
                workflow_step=workflow_step,
                evidence=stripped,
                expected="Compress-Archive should use -Force when writing a known output path.",
                actual="Command uses Compress-Archive without -Force.",
            )
        )

    if _uses_remove_item_without_guard(stripped):
        issues.append(
            _make_issue(
                issue_id=ISSUE_IDS["remove_without_guard"],
                workflow_step=workflow_step,
                evidence=stripped,
                expected=(
                    "Remove-Item should be guarded by Test-Path, an if guard, or "
                    "explicit silent-missing-file handling."
                ),
                actual="Command uses Remove-Item without an existence guard.",
            )
        )

    return issues


def detect_workflow_idempotency_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect commands that make workflow reruns non-idempotent."""
    issues: list[WorkflowIssue] = []

    for workflow_step, command_spec in _iter_command_specs(context.workflow_manifest):
        command_text = _command_text(command_spec)
        if _is_allowed_non_idempotent(command_spec, command_text):
            continue
        issues.extend(_command_issues(workflow_step, command_text))

    return issues
