"""Detect workflow command target integrity problems."""

from __future__ import annotations

import re
import shlex
from pathlib import Path
from typing import Any, Iterable

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_step_target_integrity",
]

_FILE_SUFFIXES = (
    ".py",
    ".pyw",
    ".json",
    ".md",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
)

_DEPRECATED_PATH_MARKERS = {
    "old",
    "older",
    "oldies",
    "deprecated",
    "backup",
    "backups",
    "archive",
    "archives",
    "legacy_cleanup",
    "legacy_project_older",
}

_OLD_VALIDATION_MARKERS = (
    "old_validation",
    "legacy_validation",
    "deprecated_validation",
    "validate_old",
    "old_validator",
    "legacy_validator",
    "deprecated_validator",
)

_CANONICAL_OUTPUT_FOLDERS = {
    "project_analysis_evidence/json_complete",
    "project_analysis_evidence/json_splitted",
    "workbench/_bundle_temp",
    "_project_reference/ACTIVE_PROJECT_ GOVERNANCE",
}

_EVIDENCE_ROOT = "project_analysis_evidence"
_REFERENCE_EVIDENCE_ROOT = "_project_reference/project_analysis_evidence"
_LEGACY_OUTPUT_ROOT = "dev_" + "tools_docs"

_NON_CANONICAL_OUTPUT_FOLDERS = {
    _LEGACY_OUTPUT_ROOT + "/json_complete": _EVIDENCE_ROOT + "/json_complete",
    _LEGACY_OUTPUT_ROOT + "/json_splitted": _EVIDENCE_ROOT + "/json_splitted",
    _LEGACY_OUTPUT_ROOT + "/json_split": _EVIDENCE_ROOT + "/json_splitted",
    _LEGACY_OUTPUT_ROOT + "/json_splitter": _EVIDENCE_ROOT + "/json_splitted",
    _LEGACY_OUTPUT_ROOT + "/json_splits": _EVIDENCE_ROOT + "/json_splitted",
    _REFERENCE_EVIDENCE_ROOT + "/json_complete": _EVIDENCE_ROOT + "/json_complete",
    _REFERENCE_EVIDENCE_ROOT + "/json_splitted": _EVIDENCE_ROOT + "/json_splitted",
    _REFERENCE_EVIDENCE_ROOT + "/json_split": _EVIDENCE_ROOT + "/json_splitted",
    _REFERENCE_EVIDENCE_ROOT + "/json_splitter": _EVIDENCE_ROOT + "/json_splitted",
    _REFERENCE_EVIDENCE_ROOT + "/json_splits": _EVIDENCE_ROOT + "/json_splitted",
    _EVIDENCE_ROOT + "/json_split": _EVIDENCE_ROOT + "/json_splitted",
    _EVIDENCE_ROOT + "/json_splitter": _EVIDENCE_ROOT + "/json_splitted",
    _EVIDENCE_ROOT + "/json_splits": _EVIDENCE_ROOT + "/json_splitted",
    "_bundle_temp": "workbench/_bundle_temp",
    "_project_reference/BUNDLE_MANIFEST": "workbench/_bundle_temp",
}

_TOKEN_CLEAN_RE = re.compile(r"^[\"'`([{<]+|[\"'`.,;:)>}\]]+$")


def _workflow_command_specs(manifest: dict[str, Any]) -> Iterable[tuple[str, int, dict[str, Any]]]:
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
    """Yield nested string values from command specs and expected-output fields."""
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


def _command_tokens(spec: dict[str, Any]) -> list[str]:
    """Return candidate path tokens from a workflow command spec."""
    raw_values: list[str] = []
    for key in (
        "command",
        "args",
        "cwd",
        "expected_files",
        "expect_files",
        "required_files",
        "output_files",
        "outputs",
        "expected_outputs",
        "expected_json_files",
        "expected_output_folders",
    ):
        if key in spec:
            raw_values.extend(_string_values(spec.get(key)))

    tokens: list[str] = []
    for value in raw_values:
        parts: list[str]
        try:
            parts = shlex.split(value, posix=False)
        except ValueError:
            parts = value.split()
        if not parts:
            parts = [value]
        for part in parts:
            cleaned = _clean_token(part)
            if cleaned:
                tokens.append(cleaned)
    return tokens


def _clean_token(token: str) -> str:
    """Normalize a command token for path inspection."""
    cleaned = _TOKEN_CLEAN_RE.sub("", token.strip())
    if not cleaned:
        return ""
    cleaned = cleaned.replace("{root}", "").replace("{python}", "")
    cleaned = cleaned.replace("\\", "/")
    while "//" in cleaned:
        cleaned = cleaned.replace("//", "/")
    cleaned = cleaned.strip("/")
    return cleaned


def _looks_like_project_path(token: str) -> bool:
    """Return True when a token is likely a project-relative file path."""
    lowered = token.lower()
    if lowered.startswith(("http://", "https://", "python", "-", "/")):
        return False
    if ":" in token[:3]:
        return False
    if any(lowered.endswith(suffix) for suffix in _FILE_SUFFIXES):
        staged_package = "_".join(("ask", "ai", "project", "reasoner"))
        return "/" in token or token.startswith((".", staged_package))
    return False


def _path_from_token(root: Path, token: str) -> Path | None:
    """Return an absolute path for a project-relative token, if applicable."""
    if not _looks_like_project_path(token):
        return None
    normalized = token.lstrip("./")
    if normalized.startswith("root/"):
        normalized = normalized[5:]
    return root / normalized


def _relative_display(root: Path, path: Path) -> str:
    """Return a project-relative display path."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _path_has_deprecated_marker(token: str) -> bool:
    """Return True when a path token points through an old/deprecated area."""
    parts = [part.lower() for part in token.replace("\\", "/").split("/") if part]
    return any(part in _DEPRECATED_PATH_MARKERS for part in parts)


def _has_old_validation_marker(token: str) -> bool:
    """Return True when a command token references old validation logic."""
    lowered = token.lower().replace("-", "_").replace("\\", "/")
    return any(marker in lowered for marker in _OLD_VALIDATION_MARKERS)


def _noncanonical_output_folder(token: str) -> tuple[str, str] | None:
    """Return noncanonical/canonical folder pair for output-folder naming drift."""
    normalized = token.replace("\\", "/").strip("/")
    normalized_lower = normalized.lower()
    for canonical in _CANONICAL_OUTPUT_FOLDERS:
        if normalized_lower.startswith(canonical.lower()):
            return None
    for bad, replacement in _NON_CANONICAL_OUTPUT_FOLDERS.items():
        if normalized_lower == bad.lower() or normalized_lower.startswith(bad.lower() + "/"):
            return bad, replacement
    return None


def _issue(
    *,
    issue_id: str,
    workflow_step: str,
    evidence: str,
    expected: str,
    actual: str,
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
    )


def detect_workflow_step_target_integrity(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect missing, deprecated, or stale targets referenced by workflow steps."""
    issues: list[WorkflowIssue] = []
    root = context.project_root.resolve()
    seen: set[tuple[str, str, str]] = set()

    for workflow_name, index, spec in _workflow_command_specs(context.workflow_manifest):
        step = _step_name(workflow_name, index, spec)
        for token in _command_tokens(spec):
            output_mismatch = _noncanonical_output_folder(token)
            if output_mismatch is not None:
                bad_folder, replacement = output_mismatch
                key = ("WORKFLOW_OUTPUT_FOLDER_NAMING_MISMATCH", step, token)
                if key not in seen:
                    issues.append(
                        _issue(
                            issue_id="WORKFLOW_OUTPUT_FOLDER_NAMING_MISMATCH",
                            workflow_step=step,
                            evidence="Workflow step references noncanonical output folder: " + token,
                            expected="Use canonical output folder: " + replacement,
                            actual="Referenced folder: " + bad_folder,
                        )
                    )
                    seen.add(key)

            if _path_has_deprecated_marker(token):
                key = ("WORKFLOW_STEP_TARGET_DEPRECATED_FILE", step, token)
                if key not in seen:
                    issues.append(
                        _issue(
                            issue_id="WORKFLOW_STEP_TARGET_DEPRECATED_FILE",
                            workflow_step=step,
                            evidence="Workflow step references an old/deprecated path: " + token,
                            expected="Workflow commands should target active project files only.",
                            actual=token,
                        )
                    )
                    seen.add(key)

            if _has_old_validation_marker(token):
                key = ("WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC", step, token)
                if key not in seen:
                    issues.append(
                        _issue(
                            issue_id="WORKFLOW_REFERENCES_OLD_VALIDATION_LOGIC",
                            workflow_step=step,
                            evidence="Workflow step appears to reference old validation logic: " + token,
                            expected="Use the current manage_architecture/manage_workflows validation gates.",
                            actual=token,
                        )
                    )
                    seen.add(key)

            path = _path_from_token(root, token)
            if path is None:
                continue
            if path.exists():
                continue
            rel = _relative_display(root, path)
            key = ("WORKFLOW_STEP_TARGET_MISSING_FILE", step, rel)
            if key in seen:
                continue
            issues.append(
                _issue(
                    issue_id="WORKFLOW_STEP_TARGET_MISSING_FILE",
                    workflow_step=step,
                    evidence="Workflow step references a file that does not exist: " + rel,
                    expected="Referenced workflow target file should exist or the command should be updated.",
                    actual=rel,
                )
            )
            seen.add(key)

    return issues
