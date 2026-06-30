# project-path: kanda_reasoner_app/reasoner_context_bundle/bundle_manifest_builder.py
"""Build the additive AI context bundle manifest for one project."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .hashing import sha256_file
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .path_normalization import artifact_logical_posix_path
from .project_context import resolve_project_context
from .schema_models import BundleArtifactPaths, ProjectContext

__all__ = [
    "BUNDLE_ARTIFACT_ORDER",
    "build_bundle_manifest_payload",
    "write_bundle_manifest_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "bundle_manifest"
GENERATOR_NAME = "reasoner_context_bundle.bundle_manifest_builder"
GENERATOR_VERSION = "1.4.0"

BUNDLE_ARTIFACT_ORDER = (
    "ai_briefing_json",
    "routing_manifest_json",
    "patch_safety_routes_json",
    "exclusion_rules_json",
    "file_manifest_json",
    "validation_state_json",
    "bundle_manifest_json",
)

_ARTIFACT_KIND_BY_NAME = {
    "ai_briefing_json": "ai_briefing",
    "routing_manifest_json": "routing_manifest",
    "patch_safety_routes_json": "patch_safety_routes",
    "exclusion_rules_json": "exclusion_rules",
    "file_manifest_json": "file_manifest",
    "validation_state_json": "validation_state",
    "bundle_manifest_json": "bundle_manifest",
}

_REQUIRED_BY_NAME = {
    "ai_briefing_json": True,
    "routing_manifest_json": True,
    "patch_safety_routes_json": True,
    "exclusion_rules_json": True,
    "file_manifest_json": True,
    "validation_state_json": True,
    "bundle_manifest_json": True,
}


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


def _relative_artifact_path(path: Path, context: ProjectContext) -> str:
    """Support relative artifact path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return artifact_logical_posix_path(path, context)


def _artifact_record(
    name: str,
    path: Path,
    context: ProjectContext,
) -> dict[str, Any]:
    """Support artifact record behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    exists = path.exists() and path.is_file()
    is_self_manifest = name == "bundle_manifest_json"
    record: dict[str, Any] = {
        "name": name,
        "kind": _ARTIFACT_KIND_BY_NAME[name],
        "path": _relative_artifact_path(path, context),
        "required": _REQUIRED_BY_NAME[name],
        "exists": exists or is_self_manifest,
        "sha256": "",
        "size_bytes": path.stat().st_size if exists else 0,
        "hash_status": "pending",
    }
    if is_self_manifest:
        record["self_reference"] = True
        record["hash_status"] = "self_hash_not_embedded"
        record["size_status"] = "self_size_not_embedded"
        record["size_bytes"] = 0
        record["reason"] = (
            "The bundle manifest cannot embed its own final sha256 or final "
            "size without changing that artifact. Existence is verified by "
            "the bundle checker."
        )
        return record
    if exists:
        record["sha256"] = sha256_file(path)
        record["hash_status"] = "sha256"
    else:
        record["hash_status"] = "missing"
    return record


def _artifact_paths_by_name(paths: BundleArtifactPaths) -> dict[str, Path]:
    """Support artifact paths by name behavior.
    
    Parameters
    ----------
    paths : BundleArtifactPaths
        The file or folder paths.
    
    Returns
    -------
    dict[str, Path]
        The mapped values.
    """
    
    return {
        "ai_briefing_json": paths.ai_briefing_json,
        "routing_manifest_json": paths.routing_manifest_json,
        "patch_safety_routes_json": paths.patch_safety_routes_json,
        "exclusion_rules_json": paths.exclusion_rules_json,
        "file_manifest_json": paths.file_manifest_json,
        "validation_state_json": paths.validation_state_json,
        "bundle_manifest_json": paths.bundle_manifest_json,
    }


def _artifact_records(context: ProjectContext, paths: BundleArtifactPaths) -> list[dict[str, Any]]:
    """Support artifact records behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    paths : BundleArtifactPaths
        The file or folder paths.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    by_name = _artifact_paths_by_name(paths)
    return [
        _artifact_record(name, by_name[name], context)
        for name in BUNDLE_ARTIFACT_ORDER
    ]


def _counts(artifacts: list[dict[str, Any]]) -> dict[str, int]:
    """Support counts behavior.
    
    Parameters
    ----------
    artifacts : list[dict[str, Any]]
        The artifacts value.
    
    Returns
    -------
    dict[str, int]
        The mapped values.
    """
    
    return {
        "artifacts_total": len(artifacts),
        "artifacts_existing": sum(1 for item in artifacts if item.get("exists") is True),
        "artifacts_missing": sum(1 for item in artifacts if item.get("exists") is not True),
        "required_artifacts_missing": sum(
            1
            for item in artifacts
            if item.get("required") is True and item.get("exists") is not True
        ),
    }


def build_bundle_manifest_payload(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Build the bundle manifest payload for one active project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    artifacts = _artifact_records(context, paths)
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "project": {
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
            "dynamic_output_contract": "<project_drive>:\\<project_slug>_show_project_to_AI\\second_prompt_files",
        },
        "compatibility": {
            "additive_bundle": True,
            "complete_json_generated_by_second_prompt_files": False,
            "active_snapshot_generated_by_second_prompt_files": False,
            "project_specific_dynamic_rules": True,
            "hardcoded_project_root": False,
        },
        "source_context_contract": {
            "status": "hybrid_manifest_source_archive",
            "complete_json_removed_from_normal_output": True,
            "active_snapshot_removed_from_normal_output": True,
            "exact_reconstruction_authority": "source_archive_manifest_json plus standalone source_archive_part ZIPs",
        },
        "source_truth_policy": {
            "source_files_are_truth": True,
            "json_is_evidence_not_truth": True,
            "inspect_exact_source_before_editing": True,
        },
        "section_loading_policy": {
            "ai_briefing_json": "always_read",
            "routing_manifest_json": "always_read",
            "bundle_manifest_json": "read_for_routing",
            "file_manifest_json": "read_for_routing",
            "patch_safety_routes_json": "read_for_subsystem_edit",
            "source_archive_manifest_json": "read_for_exact_reconstruction_map",
            "runtime_trace_raw": "read_only_on_request",
        },
        "counts": _counts(artifacts),
        "artifacts": artifacts,
    }


def write_bundle_manifest_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__bundle_manifest.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_bundle_manifest_payload(context)
    return write_json_atomic(paths.bundle_manifest_json, payload)
