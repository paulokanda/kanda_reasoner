"""Detect workflow commands that reference outdated validation paths."""

from __future__ import annotations

from typing import Any, Iterable

from .workflow_detector_context import (
    WorkflowDetectorContext,
)
from .workflow_issue_models import (
    WorkflowIssue,
)

__all__ = [
    "detect_validation_reference_misroutes",
]

OUTDATED_VALIDATION_REFERENCES: tuple[tuple[str, str], ...] = (
    (
        "tools/architecture",
        "Use kanda_reasoner_app/manage_architecture/manage_architecture.py.",
    ),
    (
        "_project_reference/bundle_manifest",
        "Use workbench/bundle_manifest for source/runtime bundle manifests.",
    ),
    (
        "active_project_governance",
        "Use project_freeze_ledger for reference-only governance artifacts.",
    ),
    (
        "legacy_project_older",
        "Do not route active workflow validation through older project copies.",
    ),
    (
        "oldies_deprecated",
        "Do not route active workflow validation through deprecated project copies.",
    ),
    (
        "older_deprecated",
        "Do not route active workflow validation through deprecated project copies.",
    ),
    (
        "legacy_cleanup",
        "Do not route active workflow validation through legacy cleanup folders.",
    ),
    (
        "manage_architecture_old",
        "Use the active manage_architecture.py validation entry point.",
    ),
    (
        "manage_workflows_old",
        "Use the active manage_workflows.py validation entry point.",
    ),
)


def _normalize_reference(value: str) -> str:
    """Return a normalized command fragment for validation-reference matching."""
    return value.replace("\\", "/").lower()


def _iter_command_strings(manifest: dict[str, Any]) -> Iterable[tuple[str, str]]:
    """Yield command-related strings from a workflow manifest."""
    workflows = manifest.get("workflows")
    if not isinstance(workflows, dict):
        return

    for category, cfg in workflows.items():
        if not isinstance(cfg, dict):
            continue

        commands = cfg.get("commands") or []
        if not isinstance(commands, list):
            continue

        for index, command_spec in enumerate(commands, start=1):
            base = "workflows." + str(category) + ".commands[" + str(index) + "]"

            if isinstance(command_spec, str):
                yield base + ".command", command_spec
                continue

            if not isinstance(command_spec, dict):
                continue

            for key in ("name", "command", "cwd"):
                value = command_spec.get(key)
                if isinstance(value, str):
                    yield base + "." + key, value

            args = command_spec.get("args")
            if isinstance(args, list):
                for arg_index, arg_value in enumerate(args, start=1):
                    if isinstance(arg_value, str):
                        yield base + ".args[" + str(arg_index) + "]", arg_value


def _reference_matches(value: str) -> list[tuple[str, str]]:
    """Return outdated validation references found in one command string."""
    normalized = _normalize_reference(value)
    matches: list[tuple[str, str]] = []
    for marker, expected in OUTDATED_VALIDATION_REFERENCES:
        if marker in normalized:
            matches.append((marker, expected))
    return matches


def detect_validation_reference_misroutes(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Return issues for workflow commands that reference outdated validation logic."""
    issues: list[WorkflowIssue] = []

    for location, value in _iter_command_strings(context.workflow_manifest):
        for marker, expected in _reference_matches(value):
            issues.append(
                WorkflowIssue(
                    issue_id="WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC",
                    category="workflow_validation_logic",
                    severity="error",
                    workflow_step=location,
                    evidence=(
                        "Workflow command references outdated validation marker: "
                        + marker
                    ),
                    expected=expected,
                    actual=value,
                )
            )

    return issues
