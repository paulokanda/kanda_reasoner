# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_cross_project_generalization_detectors.py
"""Detect workflow contracts that prevent cross-project reuse."""

from __future__ import annotations

import re
from typing import Any

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_cross_project_generalization_issues",
]

_WINDOWS_ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_{}])[A-Za-z]:[\\/][^\s\"'`<>|]+"
)
_UNIX_ABSOLUTE_PROJECT_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_{}])/(?:home|users|mnt|tmp|var|opt)/[^\s\"'`<>|]+",
    re.IGNORECASE,
)

_ALLOWED_PLACEHOLDERS = (
    "{root}",
    "{python}",
)


def _issue(
    *,
    issue_id: str,
    workflow_step: str,
    evidence: str,
    expected: str,
    actual: str,
) -> WorkflowIssue:
    """Support issue behavior.
    
    Parameters
    ----------
    issue_id : str
        The issue id value.
    workflow_step : str
        The workflow step value.
    evidence : str
        The evidence value.
    expected : str
        The expected value.
    actual : str
        The actual value.
    
    Returns
    -------
    WorkflowIssue
        The workflow issue result.
    """
    
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_cross_project_generalization",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
    )


def _path_to_text(path_parts: tuple[str, ...]) -> str:
    """Support path to text behavior.
    
    Parameters
    ----------
    path_parts : tuple[str, ...]
        The path parts value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return ".".join(path_parts) if path_parts else "<manifest>"


def _iter_manifest_strings(
    value: Any,
    path_parts: tuple[str, ...] = (),
) -> list[tuple[tuple[str, ...], str]]:
    """Support iter manifest strings behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    path_parts : tuple[str, ...], optional
        The optional path parts value.
    
    Returns
    -------
    list[tuple[tuple[str, ...], str]]
        The list of values.
    """
    
    strings: list[tuple[tuple[str, ...], str]] = []
    if isinstance(value, str):
        strings.append((path_parts, value))
        return strings
    if isinstance(value, dict):
        for key, child in value.items():
            strings.extend(
                _iter_manifest_strings(child, path_parts + (str(key),))
            )
        return strings
    if isinstance(value, list):
        for index, child in enumerate(value):
            strings.extend(
                _iter_manifest_strings(child, path_parts + (str(index),))
            )
        return strings
    return strings


def _is_workflow_manifest_path(path_parts: tuple[str, ...]) -> bool:
    """Support is workflow manifest path behavior.
    
    Parameters
    ----------
    path_parts : tuple[str, ...]
        The path parts value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return bool(path_parts) and path_parts[0] == "workflows"


def _contains_placeholder(value: str) -> bool:
    """Support contains placeholder behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return any(marker in value for marker in _ALLOWED_PLACEHOLDERS)


def _absolute_path_hits(value: str) -> list[str]:
    """Support absolute path hits behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    hits: list[str] = []
    for match in _WINDOWS_ABSOLUTE_PATH_RE.finditer(value):
        hits.append(match.group(0))
    for match in _UNIX_ABSOLUTE_PROJECT_PATH_RE.finditer(value):
        hits.append(match.group(0))
    return sorted(set(hits))


def _is_safe_placeholder_wrapped_path(hit: str, full_value: str) -> bool:
    """Support is safe placeholder wrapped path behavior.
    
    Parameters
    ----------
    hit : str
        The hit value.
    full_value : str
        The full value value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if _contains_placeholder(hit):
        return True
    normalized = full_value.replace("\\", "/")
    if "{root}/" in normalized or "{python}" in normalized:
        if hit not in normalized:
            return True
    return False


def _workflow_name_from_path(path_parts: tuple[str, ...]) -> str:
    """Support workflow name from path behavior.
    
    Parameters
    ----------
    path_parts : tuple[str, ...]
        The path parts value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if len(path_parts) >= 2 and path_parts[0] == "workflows":
        return path_parts[1]
    return "workflow_manifest"


def detect_workflow_cross_project_generalization_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect hardcoded local paths inside workflow command contracts."""
    manifest = context.workflow_manifest
    if not isinstance(manifest, dict):
        return []

    issues: list[WorkflowIssue] = []

    for path_parts, value in _iter_manifest_strings(manifest):
        if not _is_workflow_manifest_path(path_parts):
            continue

        hits = _absolute_path_hits(value)
        if not hits:
            continue

        unsafe_hits = [
            hit for hit in hits
            if not _is_safe_placeholder_wrapped_path(hit, value)
        ]
        if not unsafe_hits:
            continue

        workflow_name = _workflow_name_from_path(path_parts)
        issues.append(
            _issue(
                issue_id="WORKFLOW_HARDCODED_LOCAL_PATH",
                workflow_step=workflow_name + "::" + _path_to_text(path_parts),
                evidence=", ".join(unsafe_hits),
                expected=(
                    "Workflow command contracts must use {root}, {python}, "
                    "or project-relative paths so the workflow can run from "
                    "a different selected project root."
                ),
                actual="The workflow manifest contains hardcoded local path text.",
            )
        )

    return issues
