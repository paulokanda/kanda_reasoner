# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_structure_detectors.py
"""Private workflow structure detectors for Tab 2.

These detectors are additive. They make malformed workflow manifests fail in
Tab 2 while keeping the current accepted Project Reasoner manifest clean.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue


__all__: list[str] = []


_STALE_WORKFLOW_METADATA_DAYS = 365


def _workflow_issue(
    *,
    issue_id: str,
    workflow_step: str,
    evidence: str,
    expected: str,
    actual: str,
    details: dict[str, Any] | None = None,
) -> WorkflowIssue:
    """Return a workflow-governance detector issue."""
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_structure",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
        owning_box="workflow_governance",
        suggested_action=(
            "Update workflow_manifest.json or the workflow command contract so "
            "Tab 2 exposes the failure explicitly."
        ),
        correction_allowed=False,
        details=dict(details or {}),
    )


def _workflows_from_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Return the workflows object from a manifest, or an empty mapping."""
    workflows = manifest.get("workflows")
    if isinstance(workflows, dict):
        return workflows
    return {}


def _workflow_enabled(config: Any) -> bool:
    """Return True when a workflow category is enabled."""
    if not isinstance(config, dict):
        return False
    return bool(config.get("enabled", True))


def _commands_from_config(config: Any) -> list[Any]:
    """Return the command list from a workflow category."""
    if not isinstance(config, dict):
        return []
    commands = config.get("commands") or []
    if isinstance(commands, list):
        return commands
    return []


def _iter_enabled_commands(
    manifest: dict[str, Any],
) -> Iterable[tuple[str, int, Any]]:
    """Yield command specs for enabled workflow categories."""
    for category, config in _workflows_from_manifest(manifest).items():
        if not _workflow_enabled(config):
            continue
        for index, spec in enumerate(_commands_from_config(config)):
            yield str(category), index, spec


def _command_name(category: str, index: int, spec: Any) -> str:
    """Return a stable command display name."""
    if isinstance(spec, dict) and spec.get("name"):
        return str(spec["name"])
    return category + " #" + str(index + 1)


def _command_text(spec: Any) -> str:
    """Return a conservative command text representation."""
    if isinstance(spec, str):
        return spec
    if not isinstance(spec, dict):
        return ""
    if "command" in spec:
        return str(spec.get("command") or "")
    args = spec.get("args")
    if isinstance(args, list):
        return " ".join(str(part) for part in args)
    return ""


def _is_architecture_validation_command(spec: Any) -> bool:
    """Return True when a command validates the architecture gate."""
    text = _command_text(spec).replace("\\", "/").lower()
    return (
        "manage_architecture/manage_architecture.py" in text
        and "--validate" in text
    )


def _runtime_smoke_command_index(
    manifest: dict[str, Any],
    command_name: str,
) -> int | None:
    """Return the index of a named runtime-smoke command."""
    runtime_smoke = _workflows_from_manifest(manifest).get("runtime_smoke")
    if not _workflow_enabled(runtime_smoke):
        return None
    for index, spec in enumerate(_commands_from_config(runtime_smoke)):
        if _command_name("runtime_smoke", index, spec) == command_name:
            return index
    return None


def detect_required_validation_commands(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect workflow manifests that omit the architecture validation gate."""
    manifest = context.workflow_manifest
    workflows = _workflows_from_manifest(manifest)
    if not workflows:
        return [
            _workflow_issue(
                issue_id="WORKFLOW_MISSING_WORKFLOWS_SECTION",
                workflow_step="workflow_manifest",
                evidence="workflow_manifest.json does not expose a workflows object.",
                expected="Top-level workflows object with executable gates.",
                actual=type(manifest.get("workflows")).__name__,
            )
        ]

    business_checks = workflows.get("business_checks")
    if not _workflow_enabled(business_checks):
        return [
            _workflow_issue(
                issue_id="WORKFLOW_MISSING_ARCHITECTURE_VALIDATION_STEP",
                workflow_step="business_checks",
                evidence=(
                    "The business_checks workflow is disabled, so Tab 2 cannot "
                    "prove that Tab 1 architecture validation still passes."
                ),
                expected=(
                    "Enabled business_checks workflow containing "
                    "manage_architecture.py --validate."
                ),
                actual="business_checks disabled or missing",
            )
        ]

    for _category, _index, spec in _iter_enabled_commands(manifest):
        if _is_architecture_validation_command(spec):
            return []

    return [
        _workflow_issue(
            issue_id="WORKFLOW_MISSING_ARCHITECTURE_VALIDATION_STEP",
            workflow_step="business_checks",
            evidence=(
                "No enabled workflow command runs manage_architecture.py "
                "with --validate."
            ),
            expected="One enabled command runs the architecture validation gate.",
            actual="No architecture validation command found.",
        )
    ]


def detect_workflow_step_order(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect known command ordering mistakes inside runtime smoke checks."""
    manifest = context.workflow_manifest
    architecture_index = _runtime_smoke_command_index(
        manifest,
        "architecture_help_smoke",
    )
    workflow_index = _runtime_smoke_command_index(
        manifest,
        "workflow_help_smoke",
    )

    if architecture_index is None or workflow_index is None:
        return []

    if workflow_index < architecture_index:
        return [
            _workflow_issue(
                issue_id="WORKFLOW_STEP_ORDER_MISMATCH",
                workflow_step="runtime_smoke",
                evidence=(
                    "workflow_help_smoke runs before architecture_help_smoke "
                    "inside runtime_smoke."
                ),
                expected=(
                    "architecture_help_smoke should run before "
                    "workflow_help_smoke so governance help smoke is verified first."
                ),
                actual=(
                    "workflow_help_smoke index="
                    + str(workflow_index)
                    + ", architecture_help_smoke index="
                    + str(architecture_index)
                ),
                details={
                    "workflow_help_smoke_index": workflow_index,
                    "architecture_help_smoke_index": architecture_index,
                },
            )
        ]

    return []


def _parse_generated_at(value: Any) -> datetime | None:
    """Parse a generated_at_utc value."""
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def detect_stale_workflow_metadata(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect obviously stale or malformed workflow generated metadata."""
    manifest = context.workflow_manifest
    generated_at = _parse_generated_at(manifest.get("generated_at_utc"))
    if generated_at is None:
        return [
            _workflow_issue(
                issue_id="WORKFLOW_METADATA_STALE_OR_INVALID",
                workflow_step="workflow_manifest",
                evidence=(
                    "workflow_manifest.json is missing a valid generated_at_utc "
                    "timestamp."
                ),
                expected="generated_at_utc is an ISO-8601 UTC timestamp.",
                actual=str(manifest.get("generated_at_utc")),
            )
        ]

    now = datetime.now(timezone.utc)
    if generated_at > now + timedelta(days=1):
        return [
            _workflow_issue(
                issue_id="WORKFLOW_METADATA_STALE_OR_INVALID",
                workflow_step="workflow_manifest",
                evidence=(
                    "workflow_manifest.json generated_at_utc is in the future."
                ),
                expected="generated_at_utc is not later than the current time.",
                actual=generated_at.isoformat(),
            )
        ]

    age_days = (now - generated_at).days
    if age_days > _STALE_WORKFLOW_METADATA_DAYS:
        return [
            _workflow_issue(
                issue_id="WORKFLOW_METADATA_STALE_OR_INVALID",
                workflow_step="workflow_manifest",
                evidence=(
                    "workflow_manifest.json metadata is older than "
                    + str(_STALE_WORKFLOW_METADATA_DAYS)
                    + " days."
                ),
                expected="Regenerate workflow metadata through manage_workflows.py.",
                actual="metadata age days=" + str(age_days),
                details={"metadata_age_days": age_days},
            )
        ]

    return []
