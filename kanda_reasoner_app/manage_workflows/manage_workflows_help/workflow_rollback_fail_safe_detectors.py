"""Detect workflow steps that mutate state without rollback or fail-safe coverage."""

from __future__ import annotations

import json
from typing import Any

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_rollback_fail_safe_issues",
]

_MUTATING_COMMAND_MARKERS = (
    "--write",
    "--apply",
    "--fix",
    "--install",
    "--clear",
    "--clear-history",
    "--delete",
    "--remove",
    "remove-item",
    "move-item",
    "set-content",
    "out-file",
    "expand-archive",
    "copy-item",
    "shutil.rmtree",
    "os.remove",
    ".unlink(",
    ".write_text(",
    ".write_bytes(",
)

_ROLLBACK_MARKERS = (
    "rollback",
    "roll back",
    "restore",
    "backup",
    "checkpoint",
    "fail-safe",
    "failsafe",
    "revert",
    "undo",
    "atomic",
    "transaction",
)

_PREFLIGHT_MARKERS = (
    "--validate",
    " validate",
    "validation",
    "preflight",
    "--diff",
    " dry-run",
    "dry run",
    "--dry-run",
    "test",
    "unittest",
    "pytest",
    "py_compile",
    "refusing to write",
)


def _stringify_command(spec: Any) -> str:
    """Return command text used to detect mutating workflow actions."""
    if isinstance(spec, str):
        return spec

    if not isinstance(spec, dict):
        return ""

    parts: list[str] = []
    command = spec.get("command")
    if command is not None:
        parts.append(str(command))

    args = spec.get("args")
    if isinstance(args, list):
        parts.extend(str(item) for item in args)

    return " ".join(parts)


def _stringify_safety_context(workflow_cfg: dict[str, Any], spec: Any) -> str:
    """Return wider workflow text used to detect rollback and fail-safe coverage."""
    payload = {
        "workflow": workflow_cfg,
        "command": spec,
    }
    try:
        return json.dumps(payload, sort_keys=True)
    except TypeError:
        return str(payload)


def _has_marker(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def _is_mutating_command(command_text: str) -> bool:
    return _has_marker(command_text, _MUTATING_COMMAND_MARKERS)


def _has_rollback_or_fail_safe(safety_text: str) -> bool:
    return _has_marker(safety_text, _ROLLBACK_MARKERS)


def _has_preflight_marker(text: str) -> bool:
    return _has_marker(text, _PREFLIGHT_MARKERS)


def _prior_commands_have_preflight(commands: list[Any], current_index: int) -> bool:
    prior_text = " ".join(_stringify_command(spec) for spec in commands[:current_index])
    return _has_preflight_marker(prior_text)


def _issue(
    *,
    issue_id: str,
    workflow_name: str,
    command_name: str,
    evidence: str,
    expected: str,
    actual: str,
) -> WorkflowIssue:
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_fail_safe",
        severity="error",
        workflow_step=workflow_name + "::" + command_name,
        evidence=evidence,
        expected=expected,
        actual=actual,
    )


def detect_workflow_rollback_fail_safe_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect mutating workflow commands without rollback/fail-safe coverage."""
    manifest = context.workflow_manifest
    workflows = manifest.get("workflows", {})
    if not isinstance(workflows, dict):
        return []

    issues: list[WorkflowIssue] = []

    for workflow_name, workflow_cfg in sorted(workflows.items()):
        if not isinstance(workflow_cfg, dict):
            continue
        if workflow_cfg.get("enabled") is False:
            continue

        commands = workflow_cfg.get("commands") or []
        if not isinstance(commands, list):
            continue

        for index, spec in enumerate(commands):
            command_text = _stringify_command(spec)
            if not _is_mutating_command(command_text):
                continue

            command_name = "command_" + str(index + 1)
            if isinstance(spec, dict) and spec.get("name"):
                command_name = str(spec.get("name"))

            safety_text = _stringify_safety_context(workflow_cfg, spec)

            if not _has_rollback_or_fail_safe(safety_text):
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_MUTATION_WITHOUT_ROLLBACK_FAIL_SAFE",
                        workflow_name=str(workflow_name),
                        command_name=command_name,
                        evidence=command_text,
                        expected=(
                            "Mutating workflow commands must document a rollback, "
                            "backup, checkpoint, restore, or fail-safe contract."
                        ),
                        actual="No rollback or fail-safe marker was found near the command.",
                    )
                )

            if "--write" in command_text.lower():
                if not (
                    _has_preflight_marker(safety_text)
                    or _prior_commands_have_preflight(commands, index)
                ):
                    issues.append(
                        _issue(
                            issue_id="WORKFLOW_WRITE_WITHOUT_PREFLIGHT_VALIDATION",
                            workflow_name=str(workflow_name),
                            command_name=command_name,
                            evidence=command_text,
                            expected=(
                                "Write-mode workflow commands must be protected by "
                                "a prior validation, diff, dry-run, test, or explicit "
                                "preflight contract."
                            ),
                            actual="No preflight validation marker was found.",
                        )
                    )

    return issues
