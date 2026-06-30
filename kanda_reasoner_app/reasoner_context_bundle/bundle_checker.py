# project-path: kanda_reasoner_app/reasoner_context_bundle/bundle_checker.py
"""Verify an additive AI context bundle for one active project."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .exclusion_engine import decide_path_exclusion
from .exclusion_provider import load_bundle_exclusion_rules
from .hashing import sha256_file
from .output_paths import bundle_artifact_paths
from .path_normalization import resolve_logical_artifact_path
from .project_context import resolve_project_context
from .schema_models import ProjectContext

__all__ = [
    "check_ai_context_bundle",
    "raise_for_ai_context_bundle_errors",
]


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    """Support context behavior.
    
    Parameters
    ----------
    project : str | Path | ProjectContext
        The project value.
    
    Returns
    -------
    ProjectContext
        The project context result.
    """
    
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _load_json(path: Path) -> dict[str, Any]:
    """Support load json behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("JSON artifact is not an object: " + str(path))
    return data


def _artifact_path(context: ProjectContext, relative_path: str) -> Path:
    """Support artifact path behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    relative_path : str
        The relative path value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    return resolve_logical_artifact_path(context, relative_path)


def _check_manifest_artifacts(
    context: ProjectContext,
    manifest: dict[str, Any],
    failures: list[str],
) -> None:
    """Support check manifest artifacts behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    manifest : dict[str, Any]
        The manifest value.
    failures : list[str]
        The failures value.
    """
    
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        failures.append("bundle_manifest.artifacts must be a list")
        return
    for item in artifacts:
        if not isinstance(item, dict):
            failures.append("bundle_manifest artifact is not an object")
            continue
        name = str(item.get("name", ""))
        rel_path = str(item.get("path", ""))
        expected_hash = str(item.get("sha256", ""))
        required = bool(item.get("required", False))
        self_reference = bool(item.get("self_reference", False))
        hash_status = str(item.get("hash_status", ""))
        if not rel_path:
            failures.append("Artifact " + name + " is missing path")
            continue
        try:
            artifact = _artifact_path(context, rel_path)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        if not artifact.exists():
            if required:
                failures.append("Required artifact is missing: " + rel_path)
            continue
        if self_reference:
            if hash_status != "self_hash_not_embedded":
                failures.append("Self manifest artifact has invalid hash_status: " + rel_path)
            continue
        if expected_hash and sha256_file(artifact) != expected_hash:
            failures.append("Artifact hash mismatch: " + rel_path)
        if required and not expected_hash:
            failures.append("Required non-self artifact has no sha256: " + rel_path)


def _check_payload_project_contract(
    payload: dict[str, Any],
    expected_kind: str,
    failures: list[str],
) -> None:
    """Support check payload project contract behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    expected_kind : str
        The expected kind value.
    failures : list[str]
        The failures value.
    """
    
    if payload.get("bundle_kind") != expected_kind:
        failures.append("Expected bundle_kind " + expected_kind)
    project = payload.get("project")
    if not isinstance(project, dict):
        failures.append(expected_kind + ".project must be an object")
        return
    if project.get("project_root_marker") != "<PROJECT_ROOT>":
        failures.append(expected_kind + " must use <PROJECT_ROOT> marker")
    if project.get("evidence_root_relative") != "show_project_to_AI":
        failures.append(expected_kind + " evidence root must be show_project_to_AI")
    if "_project" + "_reference" in json.dumps(project, sort_keys=True):
        failures.append(expected_kind + " project metadata must not use " + "_project" + "_reference")


def _check_paths_obey_exclusions(
    context: ProjectContext,
    paths: list[str],
    label: str,
    failures: list[str],
) -> None:
    """Support check paths obey exclusions behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    paths : list[str]
        The file or folder paths.
    label : str
        The label value.
    failures : list[str]
        The failures value.
    """
    
    rules = load_bundle_exclusion_rules(context)
    for rel_path in paths:
        decision = decide_path_exclusion(rel_path, context, rules)
        if decision.excluded:
            failures.append(
                label + " path is excluded by active project rules: " + rel_path
            )


def _check_manifest_paths(context: ProjectContext, failures: list[str]) -> None:
    """Support check manifest paths behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    failures : list[str]
        The failures value.
    """
    
    paths = bundle_artifact_paths(context)
    if not paths.file_manifest_json.exists():
        failures.append("file_manifest artifact is missing")
        return
    payload = _load_json(paths.file_manifest_json)
    _check_payload_project_contract(payload, "file_manifest", failures)
    files = payload.get("files", [])
    if not isinstance(files, list):
        failures.append("file_manifest.files must be a list")
        return
    rel_paths = [str(item.get("path", "")) for item in files if isinstance(item, dict)]
    _check_paths_obey_exclusions(context, rel_paths, "file_manifest", failures)


def _check_snapshot_paths(context: ProjectContext, failures: list[str]) -> None:
    """Support check snapshot paths behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    failures : list[str]
        The failures value.
    """
    
    paths = bundle_artifact_paths(context)
    if not paths.active_snapshot_json.exists():
        failures.append("active_snapshot artifact is missing")
        return
    payload = _load_json(paths.active_snapshot_json)
    _check_payload_project_contract(payload, "active_snapshot", failures)
    files = payload.get("files", [])
    if not isinstance(files, list):
        failures.append("active_snapshot.files must be a list")
        return
    rel_paths = [str(item.get("path", "")) for item in files if isinstance(item, dict)]
    _check_paths_obey_exclusions(context, rel_paths, "active_snapshot", failures)




def _check_manifest_snapshot_alignment(context: ProjectContext, failures: list[str]) -> None:
    """Support check manifest snapshot alignment behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    failures : list[str]
        The failures value.
    """
    
    paths = bundle_artifact_paths(context)
    if not paths.file_manifest_json.exists() or not paths.active_snapshot_json.exists():
        return
    manifest = _load_json(paths.file_manifest_json)
    snapshot = _load_json(paths.active_snapshot_json)
    manifest_files = manifest.get("files", [])
    snapshot_files = snapshot.get("files", [])
    if not isinstance(manifest_files, list) or not isinstance(snapshot_files, list):
        return
    manifest_included = {
        str(item.get("path", ""))
        for item in manifest_files
        if isinstance(item, dict) and item.get("included_in_active_snapshot") is True
    }
    snapshot_paths = {
        str(item.get("path", ""))
        for item in snapshot_files
        if isinstance(item, dict)
    }
    if manifest_included != snapshot_paths:
        failures.append(
            "file_manifest included_in_active_snapshot paths do not match active_snapshot.files"
        )


def _check_validation_state(context: ProjectContext, failures: list[str]) -> None:
    """Support check validation state behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    failures : list[str]
        The failures value.
    """
    
    paths = bundle_artifact_paths(context)
    if not paths.validation_state_json.exists():
        failures.append("validation_state artifact is missing")
        return
    payload = _load_json(paths.validation_state_json)
    _check_payload_project_contract(payload, "validation_state", failures)
    capture_mode = payload.get("capture_mode")
    if not isinstance(capture_mode, dict):
        failures.append("validation_state.capture_mode must be an object")
        return
    runs_commands = capture_mode.get("runs_commands")
    mode = str(capture_mode.get("mode", ""))
    if not isinstance(runs_commands, bool):
        failures.append("validation_state.capture_mode.runs_commands must be boolean")
    if runs_commands and mode != "local_commands_run":
        failures.append("validation_state may only run commands in local_commands_run mode")
    if capture_mode.get("internet_or_ai_contact") is not False:
        failures.append("validation_state must declare no internet or AI contact")


def check_ai_context_bundle(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Return a check result for the current project's AI context bundle."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    failures: list[str] = []
    if not paths.bundle_manifest_json.exists():
        failures.append("bundle_manifest artifact is missing")
        return {
            "ok": False,
            "project_slug": context.project_slug,
            "failures": failures,
        }

    manifest = _load_json(paths.bundle_manifest_json)
    _check_payload_project_contract(manifest, "bundle_manifest", failures)
    _check_manifest_artifacts(context, manifest, failures)
    _check_manifest_paths(context, failures)
    # Hybrid Source Archive mode deliberately does not require the old heavy
    # active_snapshot artifact. Exact source reconstruction is handled by the
    # source_archive_manifest and source_archive_part ZIPs written after this
    # lightweight bundle check passes.
    _check_validation_state(context, failures)

    return {
        "ok": not failures,
        "project_slug": context.project_slug,
        "failures": failures,
        "checked_artifacts": len(manifest.get("artifacts", []))
        if isinstance(manifest.get("artifacts"), list)
        else 0,
    }


def raise_for_ai_context_bundle_errors(project: str | Path | ProjectContext) -> None:
    """Raise ValueError when the AI context bundle check fails."""
    result = check_ai_context_bundle(project)
    if result.get("ok"):
        return
    failures = result.get("failures", [])
    if not isinstance(failures, list):
        failures = ["Unknown AI context bundle failure"]
    raise ValueError("AI context bundle check failed: " + "; ".join(str(item) for item in failures))
