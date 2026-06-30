# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_documentation_drift_detectors.py
"""Detect explicit workflow documentation drift against the active manifest."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_documentation_drift_issues",
]

_MANIFEST_HASH_PATTERNS = (
    re.compile(r"workflow_manifest_sha256\s*[:=]\s*([a-fA-F0-9]{64})"),
    re.compile(r"manifest_sha256\s*[:=]\s*([a-fA-F0-9]{64})"),
)

_DOCUMENTED_WORKFLOW_PATTERNS = (
    re.compile(r"workflow\s*[:=]\s*([A-Za-z0-9_.-]+)", re.IGNORECASE),
    re.compile(r"workflow_name\s*[:=]\s*([A-Za-z0-9_.-]+)", re.IGNORECASE),
    re.compile(r"^#{2,6}\s+workflow\s+([A-Za-z0-9_.-]+)\s*$", re.IGNORECASE | re.MULTILINE),
)

_EXPECTED_FILE_PATTERNS = (
    re.compile(r"expected_output\s*[:=]\s*([^\s`]+)", re.IGNORECASE),
    re.compile(r"expected_json\s*[:=]\s*([^\s`]+)", re.IGNORECASE),
)


def _stable_manifest_hash(manifest: dict[str, Any]) -> str:
    """Return a stable hash for the active workflow manifest payload."""
    payload = json.dumps(
        manifest,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _find_declared_manifest_hashes(text: str) -> list[str]:
    """Return explicit manifest hashes declared by WORKFLOWS.md."""
    hashes: list[str] = []
    for pattern in _MANIFEST_HASH_PATTERNS:
        hashes.extend(match.group(1).lower() for match in pattern.finditer(text))
    return sorted(set(hashes))


def _configured_workflow_names(manifest: dict[str, Any]) -> set[str]:
    """Return workflow names configured in the active manifest."""
    workflows = manifest.get("workflows", {})
    if not isinstance(workflows, dict):
        return set()
    return {str(name) for name in workflows}


def _documented_workflow_names(text: str) -> set[str]:
    """Return explicitly documented workflow names."""
    names: set[str] = set()
    for pattern in _DOCUMENTED_WORKFLOW_PATTERNS:
        for match in pattern.finditer(text):
            names.add(match.group(1).strip())
    return {name for name in names if name}


def _configured_expected_files(manifest: dict[str, Any]) -> set[str]:
    """Return expected files declared by workflow command specs."""
    workflows = manifest.get("workflows", {})
    if not isinstance(workflows, dict):
        return set()

    expected: set[str] = set()
    for workflow_cfg in workflows.values():
        if not isinstance(workflow_cfg, dict):
            continue
        commands = workflow_cfg.get("commands") or []
        if not isinstance(commands, list):
            continue
        for spec in commands:
            if not isinstance(spec, dict):
                continue
            for key in ("expected_outputs", "expected_output_files", "expected_json_files"):
                value = spec.get(key)
                if isinstance(value, str):
                    expected.add(value.replace("\\", "/").strip())
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            expected.add(item.replace("\\", "/").strip())
    return {item for item in expected if item}


def _documented_expected_files(text: str) -> set[str]:
    """Return expected files explicitly documented by WORKFLOWS.md markers."""
    files: set[str] = set()
    for pattern in _EXPECTED_FILE_PATTERNS:
        for match in pattern.finditer(text):
            files.add(match.group(1).strip().replace("\\", "/"))
    return {item for item in files if item}


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
        category="workflow_documentation_drift",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
    )


def detect_workflow_documentation_drift_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect explicit drift markers in WORKFLOWS.md."""
    text = context.workflows_doc or ""
    if not text.strip():
        return []

    manifest = context.workflow_manifest
    issues: list[WorkflowIssue] = []

    declared_hashes = _find_declared_manifest_hashes(text)
    if declared_hashes:
        current_hash = _stable_manifest_hash(manifest)
        for declared_hash in declared_hashes:
            if declared_hash != current_hash:
                issues.append(
                    _issue(
                        issue_id="WORKFLOW_DOCUMENTATION_MANIFEST_HASH_DRIFT",
                        workflow_step="WORKFLOWS.md::manifest_hash",
                        evidence=declared_hash,
                        expected="WORKFLOWS.md manifest hash must match the active workflow manifest.",
                        actual="Current manifest hash is " + current_hash + ".",
                    )
                )

    configured_names = _configured_workflow_names(manifest)
    documented_names = _documented_workflow_names(text)
    missing_names = sorted(documented_names - configured_names)
    for workflow_name in missing_names:
        issues.append(
            _issue(
                issue_id="WORKFLOW_DOCUMENTS_MISSING_WORKFLOW",
                workflow_step="WORKFLOWS.md::" + workflow_name,
                evidence=workflow_name,
                expected="Documented workflow names must exist in workflow_manifest.json.",
                actual="No matching workflow exists in the active manifest.",
            )
        )

    configured_files = _configured_expected_files(manifest)
    documented_files = _documented_expected_files(text)
    stale_files = sorted(documented_files - configured_files)
    for file_name in stale_files:
        issues.append(
            _issue(
                issue_id="WORKFLOW_DOCUMENTS_STALE_EXPECTED_FILE",
                workflow_step="WORKFLOWS.md::" + file_name,
                evidence=file_name,
                expected="Documented expected_output or expected_json markers must exist in active command contracts.",
                actual="The documented expected file is not declared by the active workflow manifest.",
            )
        )

    return issues
