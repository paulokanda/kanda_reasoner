"""Detect Tab 2 generated-artifact route and dual JSON workflow mistakes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_name_from_root,
    relative_parts_manifest_file_path,
    relative_primary_evidence_json_path,
    relative_route_manifest_file_path,
    relative_working_copy_json_path,
)

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_artifact_route_issues",
]

_EVIDENCE_ROOT = "project_analysis_evidence"
_SPLIT_DIR = _EVIDENCE_ROOT + "/json_splitted"
_CHUNK_SUFFIX = ".chunk.json"

_REQUIRED_ROUTE_KEYS = (
    "web_" + "ai_readme",
    "symbol_lookup",
    "file_or_box_responsibility",
    "test_protection",
    "local_" + "ai_answer_flow",
    "u" + "i_flow",
)

_LEGACY_OUTPUT_ROOT = "dev_" + "tools_docs"
_REFERENCE_EVIDENCE_ROOT = "_project_reference/project_analysis_evidence"
_WRONG_OUTPUT_FOLDER_SEGMENTS = {
    _LEGACY_OUTPUT_ROOT + "/json_complete/": _EVIDENCE_ROOT + "/json_complete/",
    _LEGACY_OUTPUT_ROOT + "/json_splitted/": _EVIDENCE_ROOT + "/json_splitted/",
    _LEGACY_OUTPUT_ROOT + "/json_split/": _EVIDENCE_ROOT + "/json_splitted/",
    _LEGACY_OUTPUT_ROOT + "/json_splits/": _EVIDENCE_ROOT + "/json_splitted/",
    _LEGACY_OUTPUT_ROOT + "/json_completed/": _EVIDENCE_ROOT + "/json_complete/",
    _LEGACY_OUTPUT_ROOT + "/json_complete_local_" + "ai/": _EVIDENCE_ROOT + "/json_complete/",
    _REFERENCE_EVIDENCE_ROOT + "/json_complete/": _EVIDENCE_ROOT + "/json_complete/",
    _REFERENCE_EVIDENCE_ROOT + "/json_splitted/": _EVIDENCE_ROOT + "/json_splitted/",
    _REFERENCE_EVIDENCE_ROOT + "/json_split/": _EVIDENCE_ROOT + "/json_splitted/",
    _REFERENCE_EVIDENCE_ROOT + "/json_splits/": _EVIDENCE_ROOT + "/json_splitted/",
    _EVIDENCE_ROOT + "/json_split/": _EVIDENCE_ROOT + "/json_splitted/",
    _EVIDENCE_ROOT + "/json_splits/": _EVIDENCE_ROOT + "/json_splitted/",
    _EVIDENCE_ROOT + "/json_completed/": _EVIDENCE_ROOT + "/json_complete/",
    _EVIDENCE_ROOT + "/json_complete_local_" + "ai/": _EVIDENCE_ROOT + "/json_complete/",
}




def _project_artifact_name(context: WorkflowDetectorContext) -> str:
    """Return the artifact name stem for the selected project root."""
    return project_name_from_root(context.resolved_root())


def _canonical_complete_json(context: WorkflowDetectorContext) -> str:
    """Return the canonical complete JSON relative path for this project."""
    return relative_primary_evidence_json_path(_project_artifact_name(context))


def _local_ai_complete_json(context: WorkflowDetectorContext) -> str:
    """Return the local-AI complete JSON relative path for this project."""
    return relative_working_copy_json_path(_project_artifact_name(context))


def _split_manifest_name(context: WorkflowDetectorContext) -> str:
    """Return the split manifest filename for this project."""
    return Path(relative_parts_manifest_file_path(_project_artifact_name(context))).name


def _route_manifest_name(context: WorkflowDetectorContext) -> str:
    """Return the route manifest filename for this project."""
    return Path(relative_route_manifest_file_path(_project_artifact_name(context))).name

_PATHLIKE_KEYS = {
    "args",
    "command",
    "cwd",
    "expected_file",
    "expected_files",
    "expected_json_file",
    "expected_json_files",
    "expected_output_file",
    "expected_output_files",
    "generated_output",
    "generated_outputs",
    "input",
    "inputs",
    "output",
    "outputs",
    "path",
    "paths",
}


def _workflow_issue(
    *,
    issue_id: str,
    workflow_step: str,
    evidence: str,
    expected: str,
    actual: str,
    details: dict[str, Any] | None = None,
) -> WorkflowIssue:
    """Return a generated-artifact workflow issue."""
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_artifacts",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
        owning_box="workflow_governance",
        suggested_action=(
            "Update the workflow command, generated-artifact contract, or upload "
            "route so Tab 2 exposes the mistake before AI evidence is consumed."
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


def _collect_strings(value: Any, *, parent_key: str = "") -> list[str]:
    """Return string leaves from a command spec that can contain paths."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(_collect_strings(item, parent_key=parent_key))
        return strings
    if isinstance(value, dict):
        strings = []
        for key, item in value.items():
            key_text = str(key)
            if key_text in _PATHLIKE_KEYS or parent_key in _PATHLIKE_KEYS:
                strings.extend(_collect_strings(item, parent_key=key_text))
            elif isinstance(item, (dict, list)):
                strings.extend(_collect_strings(item, parent_key=key_text))
        return strings
    return []


def _command_text(spec: Any) -> str:
    """Return a conservative command text representation."""
    return " ".join(_collect_strings(spec))


def _normalize_path_text(text: str) -> str:
    """Normalize a path-like string for detector matching."""
    return text.replace("\\", "/").lower()


def _load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Load a JSON object from path."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, type(exc).__name__ + ": " + str(exc)
    if not isinstance(payload, dict):
        return None, "top level is " + type(payload).__name__
    return payload, None


def _detect_output_folder_naming(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect command specs that point to known wrong output folders."""
    issues: list[WorkflowIssue] = []
    for category, index, spec in _iter_enabled_commands(context.workflow_manifest):
        if isinstance(spec, dict) and spec.get("allow_deprecated_output_folder_name"):
            continue
        step = _command_name(category, index, spec)
        for raw_text in _collect_strings(spec):
            normalized = _normalize_path_text(raw_text)
            for wrong, replacement in _WRONG_OUTPUT_FOLDER_SEGMENTS.items():
                if wrong.lower() not in normalized:
                    continue
                issues.append(
                    _workflow_issue(
                        issue_id="WORKFLOW_OUTPUT_FOLDER_NAMING_MISMATCH",
                        workflow_step=step,
                        evidence=(
                            "Workflow command references deprecated or wrong "
                            "output folder segment: " + wrong
                        ),
                        expected="Use " + replacement + " for this generated artifact.",
                        actual=raw_text,
                        details={
                            "category": category,
                            "command_index": index,
                            "wrong_segment": wrong,
                            "replacement": replacement,
                        },
                    )
                )
    return issues


def _detect_dual_json_command_misuse(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect commands that mix canonical and local-AI JSON tracks."""
    issues: list[WorkflowIssue] = []
    canonical = _normalize_path_text(_canonical_complete_json(context))
    local_track = _normalize_path_text(_local_ai_complete_json(context))
    for category, index, spec in _iter_enabled_commands(context.workflow_manifest):
        if isinstance(spec, dict) and spec.get("allow_dual_json_track"):
            continue
        text = _normalize_path_text(_command_text(spec))
        if canonical in text and local_track in text:
            issues.append(
                _workflow_issue(
                    issue_id="WORKFLOW_DUAL_JSON_TRACK_MISMATCH",
                    workflow_step=_command_name(category, index, spec),
                    evidence=(
                        "One workflow command references both canonical complete "
                        "JSON and local-AI complete JSON."
                    ),
                    expected=(
                        "Use exactly one JSON track per command, or set an explicit "
                        "allow_dual_json_track flag with a documented handoff."
                    ),
                    actual=_command_text(spec),
                    details={
                        "category": category,
                        "command_index": index,
                    },
                )
            )
    return issues


def _looks_like_upload_command(category: str, spec: Any) -> bool:
    """Return True when a command appears to upload split web-AI artifacts."""
    text = _normalize_path_text(category + " " + _command_name(category, 0, spec) + " " + _command_text(spec))
    has_upload_signal = "upload" in text or "web_" + "ai" in text or "web-ai" in text
    has_split_signal = (
        _SPLIT_DIR.lower() in text
        or _CHUNK_SUFFIX in text
        or "chunk" in text
        or "json_splitted" in text
    )
    return bool(has_upload_signal and has_split_signal)


def _detect_upload_route_and_readme_contract(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect upload commands that ignore route/readme artifacts."""
    issues: list[WorkflowIssue] = []
    route_name = _route_manifest_name(context).lower()
    for category, index, spec in _iter_enabled_commands(context.workflow_manifest):
        if not _looks_like_upload_command(category, spec):
            continue
        text = _normalize_path_text(_command_text(spec))
        step = _command_name(category, index, spec)
        if route_name not in text:
            issues.append(
                _workflow_issue(
                    issue_id="WORKFLOW_ROUTE_MANIFEST_IGNORED_BY_UPLOAD",
                    workflow_step=step,
                    evidence=(
                        "Upload-like workflow command consumes split artifacts "
                        "without naming the web-AI route manifest."
                    ),
                    expected="Upload workflow includes " + _route_manifest_name(context) + ".",
                    actual=_command_text(spec),
                    details={"category": category, "command_index": index},
                )
            )
        if "web_" + "ai_readme" not in text:
            issues.append(
                _workflow_issue(
                    issue_id="WORKFLOW_WEB_AI_README_IGNORED",
                    workflow_step=step,
                    evidence=(
                        "Upload-like workflow command does not expose web AI readme "
                        "as an upload or validation input."
                    ),
                    expected="Upload workflow explicitly includes web AI readme evidence.",
                    actual=_command_text(spec),
                    details={"category": category, "command_index": index},
                )
            )
    return issues


def _chunk_files(split_dir: Path) -> list[Path]:
    """Return split chunk files."""
    if not split_dir.exists():
        return []
    return sorted(path for path in split_dir.glob("*.json") if path.name.endswith(_CHUNK_SUFFIX))


def _route_collection(route_data: dict[str, Any]) -> dict[str, Any]:
    """Return the route collection from a route manifest."""
    routes = route_data.get("question_routes")
    if isinstance(routes, dict):
        return routes
    routes = route_data.get("routes")
    if isinstance(routes, dict):
        return routes
    return {}


def _detect_route_manifest_contract(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect stale or incomplete deterministic route manifests."""
    root = context.resolved_root()
    split_dir = root / _SPLIT_DIR
    route_name = _route_manifest_name(context)
    split_manifest_name = _split_manifest_name(context)
    route_path = split_dir / route_name
    split_manifest_path = split_dir / split_manifest_name
    chunks = _chunk_files(split_dir)

    if not split_dir.exists():
        return []
    if not route_path.exists():
        if split_manifest_path.exists() or chunks:
            return [
                _workflow_issue(
                    issue_id="WORKFLOW_ROUTE_MANIFEST_MISSING",
                    workflow_step="generated_artifacts",
                    evidence=(
                        "Split artifacts exist but the deterministic web-AI route "
                        "manifest is missing."
                    ),
                    expected=route_name + " exists in " + _SPLIT_DIR + ".",
                    actual="missing route manifest",
                )
            ]
        return []

    route_data, route_error = _load_json(route_path)
    if route_error is not None or route_data is None:
        return [
            _workflow_issue(
                issue_id="WORKFLOW_ROUTE_MANIFEST_INVALID",
                workflow_step="generated_artifacts",
                evidence="Route manifest cannot be parsed as a JSON object.",
                expected="Route manifest is valid JSON with deterministic question routes.",
                actual=route_error or "invalid route manifest",
            )
        ]

    issues: list[WorkflowIssue] = []
    routes = _route_collection(route_data)
    if not routes:
        issues.append(
            _workflow_issue(
                issue_id="WORKFLOW_DETERMINISTIC_ROUTE_MISSING",
                workflow_step="generated_artifacts",
                evidence="Route manifest does not expose question_routes or routes.",
                expected="Route manifest contains deterministic AI question routes.",
                actual="route collection missing or empty",
            )
        )
    else:
        missing_routes = [key for key in _REQUIRED_ROUTE_KEYS if key not in routes]
        if missing_routes:
            issues.append(
                _workflow_issue(
                    issue_id="WORKFLOW_DETERMINISTIC_ROUTE_MISSING",
                    workflow_step="generated_artifacts",
                    evidence=(
                        "Route manifest is missing deterministic route keys: "
                        + ", ".join(missing_routes)
                    ),
                    expected="Route manifest includes all required route keys.",
                    actual="missing: " + ", ".join(missing_routes),
                    details={"missing_routes": missing_routes},
                )
            )

    split_data, split_error = _load_json(split_manifest_path)
    if split_manifest_path.exists() and split_error is None and split_data is not None:
        split_hash = split_data.get("source_sha256")
        route_hash = route_data.get("source_sha256")
        if isinstance(split_hash, str) and isinstance(route_hash, str):
            if split_hash != route_hash:
                issues.append(
                    _workflow_issue(
                        issue_id="WORKFLOW_ROUTE_MANIFEST_STALE",
                        workflow_step="generated_artifacts",
                        evidence=(
                            "Route manifest source_sha256 does not match split "
                            "manifest source_sha256."
                        ),
                        expected="Route manifest and split manifest share source_sha256.",
                        actual=(
                            "route source_sha256=" + route_hash
                            + "; split source_sha256=" + split_hash
                        ),
                    )
                )

    return issues


def detect_workflow_artifact_route_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect generated-artifact route and dual JSON workflow mistakes."""
    issues: list[WorkflowIssue] = []
    issues.extend(_detect_output_folder_naming(context))
    issues.extend(_detect_dual_json_command_misuse(context))
    issues.extend(_detect_upload_route_and_readme_contract(context))
    issues.extend(_detect_route_manifest_contract(context))
    return issues
