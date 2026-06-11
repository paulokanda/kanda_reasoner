"""Detect workflow steps that run in a dangerous order."""

from __future__ import annotations

import re
import shlex
from typing import Any, Iterable

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_step_order_issues",
]

_STAGE_ORDER = {
    "collect_evidence": 10,
    "complete_json": 20,
    "local_ai_refresh": 30,
    "split_chunks": 40,
    "route_manifest": 50,
    "upload_web_ai": 60,
    "ask_ai": 70,
}

_STAGE_LABELS = {
    "collect_evidence": "evidence collection",
    "complete_json": "complete JSON generation",
    "local_ai_refresh": "local-AI JSON refresh",
    "split_chunks": "split chunk generation",
    "route_manifest": "route manifest generation",
    "upload_web_ai": "web-AI upload",
    "ask_ai": "AI ask/retrieval",
}

_STAGE_MARKERS = {
    "collect_evidence": (
        "data_collector",
        "runtime_collector",
        "collector_main",
        "collect_static",
        "collect_runtime",
        "evidence collection",
    ),
    "complete_json": (
        "json_complete",
        "complete_json",
        "complete json",
        "developer_tools__complete.json",
        "canonical complete",
    ),
    "local_ai_refresh": (
        "complete_local_ai",
        "complete local ai",
        "complete_local_ai_json",
        "developer_tools__complete_local_ai.json",
        "developer_tools__complete_local_AI.json",
        "local-ai refresh",
        "local_ai refresh",
    ),
    "split_chunks": (
        "json_splitter",
        "json_splitted",
        "split_manifest",
        "split_index",
        "split chunks",
        "chunk generation",
        "split/reassemble",
        "reassemble validation",
    ),
    "route_manifest": (
        "route_manifest",
        "route manifest",
        "web_ai_route_manifest",
        "question_route",
        "question routes",
        "deterministic route",
    ),
    "upload_web_ai": (
        "upload workflow",
        "upload_web_ai",
        "web_ai upload",
        "web ai upload",
        "web-ai upload",
        "notebooklm upload",
    ),
    "ask_ai": (
        "ask_ai",
        "ask ai",
        "ai question",
        "question type",
        "promptbuilder responsibility",
        "retriever prioritizing",
    ),
}

_REQUIRED_PREDECESSORS = {
    "complete_json": ("collect_evidence",),
    "local_ai_refresh": ("complete_json",),
    "split_chunks": ("complete_json",),
    "route_manifest": ("split_chunks",),
    "upload_web_ai": ("route_manifest",),
    "ask_ai": ("route_manifest",),
}

_TOKEN_CLEAN_RE = re.compile(r"^[\"'`([{<]+|[\"'`.,;:)>}\]]+$")


def _workflow_command_specs(
    manifest: dict[str, Any],
) -> Iterable[tuple[str, int, dict[str, Any]]]:
    """Yield workflow command specs from a workflow manifest."""
    workflows = manifest.get("workflows")
    if not isinstance(workflows, dict):
        return
    for workflow_name, workflow_payload in workflows.items():
        if not isinstance(workflow_payload, dict):
            continue
        commands = workflow_payload.get("commands") or []
        if not isinstance(commands, list):
            continue
        for index, spec in enumerate(commands, start=1):
            if isinstance(spec, dict):
                yield str(workflow_name), index, spec
            elif isinstance(spec, str):
                yield str(workflow_name), index, {"command": spec}


def _step_name(workflow_name: str, index: int, spec: dict[str, Any]) -> str:
    """Return a stable workflow step display name."""
    name = spec.get("name")
    if isinstance(name, str) and name.strip():
        return workflow_name + ":" + name.strip()
    return workflow_name + ":command_" + str(index)


def _string_values(value: Any) -> Iterable[str]:
    """Yield nested string values from command specs."""
    if isinstance(value, str):
        yield value
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _string_values(item)
        return
    if isinstance(value, dict):
        for item in value.values():
            yield from _string_values(item)


def _clean_token(token: str) -> str:
    """Normalize one command token for marker matching."""
    cleaned = _TOKEN_CLEAN_RE.sub("", token.strip())
    cleaned = cleaned.replace("\\", "/")
    while "//" in cleaned:
        cleaned = cleaned.replace("//", "/")
    return cleaned.strip()


def _split_text(value: str) -> list[str]:
    """Split command text into stable, marker-friendly pieces."""
    try:
        parts = shlex.split(value, posix=False)
    except ValueError:
        parts = value.split()
    cleaned = [_clean_token(part) for part in parts]
    return [part for part in cleaned if part]


def _spec_text_fragments(spec: dict[str, Any]) -> list[str]:
    """Return command text fragments with the step name first."""
    fragments: list[str] = []
    name = spec.get("name")
    if isinstance(name, str) and name.strip():
        fragments.append(name)

    for key in (
        "command",
        "args",
        "cwd",
        "expected_files",
        "expected_outputs",
        "expected_json_files",
        "expected_output_folders",
        "outputs",
        "output_files",
        "required_files",
    ):
        if key not in spec:
            continue
        for value in _string_values(spec.get(key)):
            fragments.append(value)
            fragments.extend(_split_text(value))
    return fragments


def _normalize_marker_text(text: str) -> str:
    """Return normalized text for stage marker matching."""
    lowered = text.lower().replace("\\", "/").replace("-", "_")
    lowered = lowered.replace("__complete_local_ai", "__complete_local_ai")
    return " ".join(lowered.split())


def _marker_matches(text: str, marker: str) -> bool:
    """Return True when text contains a stage marker."""
    normalized_text = _normalize_marker_text(text)
    normalized_marker = _normalize_marker_text(marker)
    return normalized_marker in normalized_text


def _stage_ids_for_spec(spec: dict[str, Any]) -> set[str]:
    """Infer canonical pipeline stage identifiers for a workflow step."""
    fragments = _spec_text_fragments(spec)
    if not fragments:
        return set()

    name = spec.get("name")
    if isinstance(name, str) and name.strip():
        name_matches = {
            stage_id
            for stage_id, markers in _STAGE_MARKERS.items()
            if any(_marker_matches(name, marker) for marker in markers)
        }
        if name_matches:
            return name_matches

    matches: set[str] = set()
    for fragment in fragments:
        for stage_id, markers in _STAGE_MARKERS.items():
            if any(_marker_matches(fragment, marker) for marker in markers):
                matches.add(stage_id)
    return matches


def _lowest_stage_rank(stage_ids: set[str]) -> int:
    """Return the earliest canonical rank represented by stage identifiers."""
    return min(_STAGE_ORDER[stage_id] for stage_id in stage_ids)


def _highest_stage_rank(stage_ids: set[str]) -> int:
    """Return the latest canonical rank represented by stage identifiers."""
    return max(_STAGE_ORDER[stage_id] for stage_id in stage_ids)


def _stage_label(stage_id: str) -> str:
    """Return a readable stage label."""
    return _STAGE_LABELS.get(stage_id, stage_id)


def _issue(
    *,
    issue_id: str,
    workflow_step: str,
    evidence: str,
    expected: str,
    actual: str,
    details: dict[str, Any],
) -> WorkflowIssue:
    """Build a workflow detector error issue."""
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_detectors",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
        details=details,
    )


def detect_workflow_step_order_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect canonical workflow pipeline steps that run out of order."""
    steps: list[tuple[int, str, set[str]]] = []

    for position, (workflow_name, index, spec) in enumerate(
        _workflow_command_specs(context.workflow_manifest),
        start=1,
    ):
        stage_ids = _stage_ids_for_spec(spec)
        if not stage_ids:
            continue
        steps.append((_lowest_stage_rank(stage_ids), _step_name(workflow_name, index, spec), stage_ids))

    if len(steps) < 2:
        return []

    issues: list[WorkflowIssue] = []
    seen: set[tuple[str, str, str]] = set()

    first_stage_positions: dict[str, tuple[int, str]] = {}
    for position, (_rank, step, stage_ids) in enumerate(steps, start=1):
        for stage_id in stage_ids:
            first_stage_positions.setdefault(stage_id, (position, step))

    for position, (_rank, step, stage_ids) in enumerate(steps, start=1):
        for stage_id in sorted(stage_ids, key=lambda item: _STAGE_ORDER[item]):
            for predecessor in _REQUIRED_PREDECESSORS.get(stage_id, ()):
                predecessor_position = first_stage_positions.get(predecessor)
                if predecessor_position is None:
                    continue
                required_position, required_step = predecessor_position
                if required_position <= position:
                    continue
                key = ("WORKFLOW_STEP_ORDER_MISMATCH", step, predecessor)
                if key in seen:
                    continue
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_STEP_ORDER_MISMATCH",
                        workflow_step=step,
                        evidence=(
                            "Workflow step runs before its required predecessor. "
                            + "Step "
                            + step
                            + " represents "
                            + _stage_label(stage_id)
                            + ", but "
                            + _stage_label(predecessor)
                            + " appears later at "
                            + required_step
                            + "."
                        ),
                        expected=(
                            _stage_label(predecessor)
                            + " should run before "
                            + _stage_label(stage_id)
                            + "."
                        ),
                        actual=(
                            _stage_label(stage_id)
                            + " appears before "
                            + _stage_label(predecessor)
                            + "."
                        ),
                        details={
                            "stage": stage_id,
                            "required_predecessor": predecessor,
                            "step_position": position,
                            "required_position": required_position,
                            "required_step": required_step,
                        },
                    )
                )
                seen.add(key)

    return issues
