# project-path: kanda_reasoner_app/reasoner_context_bundle/bundle_orchestrator.py
"""Orchestrate additive AI context bundle generation for one project."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .ai_briefing_builder import write_ai_briefing_json
from .bundle_checker import check_ai_context_bundle
from .bundle_manifest_builder import write_bundle_manifest_json
from .exclusion_rules_exporter import write_exclusion_rules_json
from .file_manifest_builder import write_file_manifest_json
from .patch_safety_routes_builder import write_patch_safety_routes_json
from .routing_manifest_builder import write_routing_manifest_json
from .hashing import sha256_file
from .output_paths import bundle_artifact_paths
from .path_normalization import artifact_logical_posix_path
from .project_context import resolve_project_context
from .schema_models import ProjectContext
from .validation_state_builder import write_validation_state_json

__all__ = [
    "generate_ai_context_bundle",
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


def _hash_if_file(path: Path) -> str:
    """Support hash if file behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    if path.exists() and path.is_file():
        return sha256_file(path)
    return ""


def _artifact_record(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Support artifact record behavior.
    
    Parameters
    ----------
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
    return {
        "path": artifact_logical_posix_path(path, context),
        "exists": exists,
        "sha256": sha256_file(path) if exists else "",
        "size_bytes": path.stat().st_size if exists else 0,
    }


def _generated_records(paths_by_name: Mapping[str, Path], context: ProjectContext) -> dict[str, Any]:
    """Support generated records behavior.
    
    Parameters
    ----------
    paths_by_name : Mapping[str, Path]
        The paths by name value.
    context : ProjectContext
        The context value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        name: _artifact_record(path, context)
        for name, path in paths_by_name.items()
    }


def _paths_by_generated_name(project: str | Path | ProjectContext) -> dict[str, Path]:
    """Support paths by generated name behavior.
    
    Parameters
    ----------
    project : str | Path | ProjectContext
        The project value.
    
    Returns
    -------
    dict[str, Path]
        The mapped values.
    """
    
    paths = bundle_artifact_paths(project)
    return {
        "ai_briefing_json": paths.ai_briefing_json,
        "routing_manifest_json": paths.routing_manifest_json,
        "patch_safety_routes_json": paths.patch_safety_routes_json,
        "exclusion_rules_json": paths.exclusion_rules_json,
        "file_manifest_json": paths.file_manifest_json,
        "validation_state_json": paths.validation_state_json,
        "bundle_manifest_json": paths.bundle_manifest_json,
    }


def generate_ai_context_bundle(
    project: str | Path | ProjectContext,
    command_results: Mapping[str, Mapping[str, object]] | None = None,
    *,
    check_bundle: bool = True,
    commands_run_by_bundle: bool = False,
) -> dict[str, Any]:
    """Generate lightweight AI handoff map artifacts for one project.

    Hybrid Source Archive export makes ZIP source archive parts the exact
    reconstruction authority. Second Prompt Files intentionally skips the
    separately owned canonical complete JSON artifact. This function writes
    the lightweight companion map, routing, manifest, validation, and exclusion
    artifacts used by the prompt-file delivery.
    """
    context = _context(project)
    paths = bundle_artifact_paths(context)
    written_paths: list[Path] = []
    written_paths.append(write_exclusion_rules_json(context))
    written_paths.append(write_file_manifest_json(context))
    written_paths.append(write_routing_manifest_json(context))
    written_paths.append(write_patch_safety_routes_json(context))
    written_paths.append(
        write_validation_state_json(
            context,
            command_results=command_results,
            commands_run_by_bundle=commands_run_by_bundle,
        )
    )
    # Two-pass first-read artifact generation:
    # 1. Write briefing after peer artifacts exist so it never reports false
    #    missing artifacts.
    # 2. Write bundle manifest after briefing so it can hash the final briefing.
    # 3. Rewrite the briefing once more so it can report the manifest as present
    #    without embedding a stale mutual hash.
    # 4. Rewrite the bundle manifest once more so its briefing hash is current.
    briefing_path = write_ai_briefing_json(context)
    manifest_path = write_bundle_manifest_json(context)
    briefing_path = write_ai_briefing_json(context)
    manifest_path = write_bundle_manifest_json(context)
    written_paths.append(briefing_path)
    written_paths.append(manifest_path)

    check_result: dict[str, Any] = {
        "ok": True,
        "project_slug": context.project_slug,
        "failures": [],
        "checked_artifacts": 0,
        "skipped": True,
    }
    if check_bundle:
        check_result = check_ai_context_bundle(context)

    generated_paths = _paths_by_generated_name(context)
    failures = []
    if not bool(check_result.get("ok", False)):
        failures.extend(str(item) for item in check_result.get("failures", []))

    return {
        "ok": not failures,
        "project_slug": context.project_slug,
        "project_root_marker": "<PROJECT_ROOT>",
        "evidence_root_relative": "show_project_to_AI",
        "json_complete_relative": "show_project_to_AI/second_prompt_files",
        "dynamic_output_contract": "<project_drive>:\\<project_slug>_show_project_to_AI\\second_prompt_files",
        "source_context_contract": {
            "status": "hybrid_manifest_source_archive",
            "mode": "lightweight_map_json_plus_source_archive_manifest",
            "complete_json_generated_by_second_prompt_files": False,
            "active_snapshot_generated_by_second_prompt_files": False,
            "source_archive_is_exact_reconstruction_authority": True,
        },
        "written_artifacts": [artifact_logical_posix_path(path, context) for path in written_paths],
        "generated_artifacts": _generated_records(generated_paths, context),
        "check_result": check_result,
        "failures": failures,
    }
