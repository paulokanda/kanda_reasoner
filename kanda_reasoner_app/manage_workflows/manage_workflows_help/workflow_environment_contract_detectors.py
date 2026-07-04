# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_environment_contract_detectors.py
"""Detect remaining Tab 2 environment and root contract workflow errors."""

from __future__ import annotations

import re
from typing import Any

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = ["detect_workflow_environment_contract_issues"]

_BAD_ENCODING_MARKERS = (
    "-encoding unicode",
    "-encoding default",
    "-encoding oem",
    "-encoding ascii",
    "encoding='ascii'",
    'encoding="ascii"',
    "encoding='cp1252'",
    'encoding="cp1252"',
    "encoding='mbcs'",
    'encoding="mbcs"',
)

_LINE_ENDING_MARKERS = (
    "line_endings",
    "newline",
    "lineEnding",
    "line_ending",
)

_ALLOWED_LINE_ENDINGS = {
    "lf",
    "crlf",
    "native",
    "preserve",
}

_OUTPUT_KEYS = (
    "expected_outputs",
    "expected_output_files",
    "expected_json_files",
    "outputs",
)

_NON_EMPTY_GUARD_KEYS = (
    "require_non_empty_output",
    "require_non_empty_outputs",
    "non_empty_outputs",
    "expected_stdout_markers",
    "expected_stderr_markers",
    "expected_content_markers",
    "content_markers",
)

_DEPENDENCY_KEYS = (
    "dependencies",
    "required_dependencies",
    "python_dependencies",
    "requires",
)

_PINNED_DEPENDENCY_RE = re.compile(
    r"^[A-Za-z0-9_.-]+\s*(==|>=|<=|~=|>|<)\s*[A-Za-z0-9_.!*+-]+$"
)

_WINDOWS_ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_{}])[A-Za-z]:[\\/][^\s\"'`<>|]+"
)

_ROOT_PLACEHOLDERS = (
    "{root}",
    "{project_root}",
    "{workspace_root}",
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
        category="workflow_environment_contract",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
    )

def _iter_workflow_commands(manifest: dict[str, Any]) -> list[tuple[str, int, Any]]:
    """Support iter workflow commands behavior.
    
    Parameters
    ----------
    manifest : dict[str, Any]
        The manifest value.
    
    Returns
    -------
    list[tuple[str, int, Any]]
        The list of values.
    """
    
    workflows = manifest.get("workflows", {})
    if not isinstance(workflows, dict):
        return []

    items: list[tuple[str, int, Any]] = []
    for workflow_name, workflow_cfg in sorted(workflows.items()):
        if not isinstance(workflow_cfg, dict):
            continue
        if workflow_cfg.get("enabled") is False:
            continue
        commands = workflow_cfg.get("commands") or []
        if not isinstance(commands, list):
            continue
        for index, spec in enumerate(commands, start=1):
            items.append((str(workflow_name), index, spec))
    return items

def _command_name(spec: Any, index: int) -> str:
    """Support command name behavior.
    
    Parameters
    ----------
    spec : Any
        The spec value.
    index : int
        The index value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(spec, dict) and spec.get("name"):
        return str(spec.get("name"))
    return "command_" + str(index)

def _command_text(spec: Any) -> str:
    """Support command text behavior.
    
    Parameters
    ----------
    spec : Any
        The spec value.
    
    Returns
    -------
    str
        The string result.
    """
    
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

    cwd = spec.get("cwd")
    if cwd is not None:
        parts.append(str(cwd))

    return " ".join(parts)

def _dict_text(spec: Any) -> str:
    """Support dict text behavior.
    
    Parameters
    ----------
    spec : Any
        The spec value.
    
    Returns
    -------
    str
        The string result.
    """
    
    try:
        return json_dumps_safe(spec)
    except Exception:
        return str(spec)

def json_dumps_safe(value: Any) -> str:
    """Support json dumps safe behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    import json

    return json.dumps(value, sort_keys=True, ensure_ascii=True)

def _has_bad_encoding_marker(text: str) -> str | None:
    """Support has bad encoding marker behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str | None
        The string result.
    """
    
    lowered = text.lower()
    for marker in _BAD_ENCODING_MARKERS:
        if marker in lowered:
            return marker
    return None

def _bad_line_ending_value(spec: dict[str, Any]) -> tuple[str, str] | None:
    """Support bad line ending value behavior.
    
    Parameters
    ----------
    spec : dict[str, Any]
        The spec value.
    
    Returns
    -------
    tuple[str, str] | None
        The tuple of values.
    """
    
    for key in _LINE_ENDING_MARKERS:
        if key not in spec:
            continue
        value = str(spec.get(key)).strip().lower()
        if value and value not in _ALLOWED_LINE_ENDINGS:
            return key, value
    return None

def _has_expected_output_contract(spec: dict[str, Any]) -> bool:
    """Support has expected output contract behavior.
    
    Parameters
    ----------
    spec : dict[str, Any]
        The spec value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return any(key in spec for key in _OUTPUT_KEYS)

def _has_non_empty_guard(spec: dict[str, Any]) -> bool:
    """Support has non empty guard behavior.
    
    Parameters
    ----------
    spec : dict[str, Any]
        The spec value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for key in _NON_EMPTY_GUARD_KEYS:
        value = spec.get(key)
        if value:
            return True
    return False

def _allows_empty_output(spec: dict[str, Any]) -> bool:
    """Support allows empty output behavior.
    
    Parameters
    ----------
    spec : dict[str, Any]
        The spec value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for key in ("allow_empty_output", "allow_empty_outputs", "success_on_empty_output"):
        if spec.get(key) is True:
            return True
    return False

def _dependency_items(value: Any) -> list[str]:
    """Support dependency items behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if isinstance(item, str)]
    if isinstance(value, dict):
        return [str(key) + str(val) for key, val in value.items()]
    return []

def _find_unpinned_dependencies(spec: dict[str, Any]) -> list[str]:
    """Support find unpinned dependencies behavior.
    
    Parameters
    ----------
    spec : dict[str, Any]
        The spec value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    unpinned: list[str] = []
    for key in _DEPENDENCY_KEYS:
        if key not in spec:
            continue
        for item in _dependency_items(spec.get(key)):
            text = item.strip()
            if text and not _PINNED_DEPENDENCY_RE.match(text):
                unpinned.append(text)
    return sorted(set(unpinned))

def _path_root_drift_hits(spec: dict[str, Any]) -> list[str]:
    """Support path root drift hits behavior.
    
    Parameters
    ----------
    spec : dict[str, Any]
        The spec value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    hits: list[str] = []
    for key in ("cwd", "root", "project_root", "output_root", "cache_root", "workspace_root"):
        if key not in spec:
            continue
        value = str(spec.get(key))
        if any(marker in value for marker in _ROOT_PLACEHOLDERS):
            continue
        for match in _WINDOWS_ABSOLUTE_PATH_RE.finditer(value):
            hits.append(key + "=" + match.group(0))
    return sorted(set(hits))

def detect_workflow_environment_contract_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect remaining Tab 2 help-list workflow environment contract errors."""
    manifest = context.workflow_manifest
    if not isinstance(manifest, dict):
        return []

    issues: list[WorkflowIssue] = []

    for workflow_name, index, spec in _iter_workflow_commands(manifest):
        command_name = _command_name(spec, index)
        workflow_step = workflow_name + "::" + command_name
        text = _command_text(spec)

        bad_encoding = _has_bad_encoding_marker(text)
        if bad_encoding is not None:
            issues.append(
                _issue(
                    issue_id="WORKFLOW_ENCODING_OR_LINE_ENDING_MISMATCH",
                    workflow_step=workflow_step,
                    evidence=bad_encoding,
                    expected="Workflow commands that write or read text should use utf-8 or preserve/native line ending contracts.",
                    actual=text,
                )
            )

        if isinstance(spec, dict):
            bad_line_ending = _bad_line_ending_value(spec)
            if bad_line_ending is not None:
                key, value = bad_line_ending
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_ENCODING_OR_LINE_ENDING_MISMATCH",
                        workflow_step=workflow_step,
                        evidence=key + "=" + value,
                        expected="Allowed line ending contracts are lf, crlf, native, or preserve.",
                        actual=_dict_text(spec),
                    )
                )

            if _allows_empty_output(spec):
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_SILENT_EMPTY_OUTPUT_SUCCESS",
                        workflow_step=workflow_step,
                        evidence="allow_empty_output=true",
                        expected="Workflow success should not explicitly allow empty required outputs.",
                        actual=_dict_text(spec),
                    )
                )
            elif _has_expected_output_contract(spec) and spec.get("require_non_empty_output") is False:
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_SILENT_EMPTY_OUTPUT_SUCCESS",
                        workflow_step=workflow_step,
                        evidence="require_non_empty_output=false",
                        expected="Expected output contracts should require non-empty output or explicit content markers.",
                        actual=_dict_text(spec),
                    )
                )

            unpinned = _find_unpinned_dependencies(spec)
            if unpinned:
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_DEPENDENCY_VERSION_SKEW",
                        workflow_step=workflow_step,
                        evidence=", ".join(unpinned),
                        expected="Declared workflow dependencies should include version constraints such as ==, >=, <=, ~=, >, or <.",
                        actual=_dict_text(spec),
                    )
                )

            root_hits = _path_root_drift_hits(spec)
            if root_hits:
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_PATH_ROOT_DRIFT",
                        workflow_step=workflow_step,
                        evidence=", ".join(root_hits),
                        expected="Workflow root, cwd, output_root, cache_root, and workspace_root should use {root} or project-relative paths.",
                        actual=_dict_text(spec),
                    )
                )

    return issues
