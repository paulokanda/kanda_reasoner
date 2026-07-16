"""Orchestrate additive AI context bundle generation for one project."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .active_snapshot_builder import write_active_snapshot_json
from .bundle_checker import check_ai_context_bundle
from .bundle_manifest_builder import write_bundle_manifest_json
from .exclusion_rules_exporter import write_exclusion_rules_json
from .file_manifest_builder import write_file_manifest_json
from .reconstruction_payload_builder import write_reconstruction_payload_json
from .hashing import sha256_file
from .output_paths import bundle_artifact_paths
from .path_normalization import relative_posix_path
from .project_context import resolve_project_context
from .schema_models import ProjectContext
from .validation_state_builder import write_validation_state_json

__all__ = [
    "generate_ai_context_bundle",
]


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _hash_if_file(path: Path) -> str:
    if path.exists() and path.is_file():
        return sha256_file(path)
    return ""


def _artifact_record(path: Path, context: ProjectContext) -> dict[str, Any]:
    exists = path.exists() and path.is_file()
    return {
        "path": relative_posix_path(path, context.root),
        "exists": exists,
        "sha256": sha256_file(path) if exists else "",
        "size_bytes": path.stat().st_size if exists else 0,
    }


def _generated_records(paths_by_name: Mapping[str, Path], context: ProjectContext) -> dict[str, Any]:
    return {
        name: _artifact_record(path, context)
        for name, path in paths_by_name.items()
    }


def _paths_by_generated_name(project: str | Path | ProjectContext) -> dict[str, Path]:
    paths = bundle_artifact_paths(project)
    return {
        "exclusion_rules_json": paths.exclusion_rules_json,
        "file_manifest_json": paths.file_manifest_json,
        "active_snapshot_json": paths.active_snapshot_json,
        "validation_state_json": paths.validation_state_json,
        "reconstruction_payload_json": paths.reconstruction_payload_json,
        "bundle_manifest_json": paths.bundle_manifest_json,
    }


def generate_ai_context_bundle(
    project: str | Path | ProjectContext,
    command_results: Mapping[str, Mapping[str, object]] | None = None,
    *,
    check_bundle: bool = True,
    commands_run_by_bundle: bool = False,
) -> dict[str, Any]:
    """Generate all additive companion JSON artifacts for one project.

    This orchestrator is intentionally closed-box and additive. It does not
    generate or modify the existing complete JSON contract. The current Tab 4
    collector remains responsible for creating ``<project_slug>__complete.json``.
    This function writes only companion files and then optionally checks the
    bundle.
    """
    context = _context(project)
    paths = bundle_artifact_paths(context)
    complete_hash_before = _hash_if_file(paths.complete_json)

    written_paths: list[Path] = []
    written_paths.append(write_exclusion_rules_json(context))
    written_paths.append(write_file_manifest_json(context))
    written_paths.append(write_active_snapshot_json(context))
    written_paths.append(
        write_validation_state_json(
            context,
            command_results=command_results,
            commands_run_by_bundle=commands_run_by_bundle,
        )
    )
    written_paths.append(write_reconstruction_payload_json(context))
    written_paths.append(write_bundle_manifest_json(context))

    complete_hash_after = _hash_if_file(paths.complete_json)
    complete_json_preserved = complete_hash_before == complete_hash_after

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
    if not complete_json_preserved:
        failures.append("complete_json hash changed during companion generation")
    if not bool(check_result.get("ok", False)):
        failures.extend(str(item) for item in check_result.get("failures", []))

    return {
        "ok": not failures,
        "project_slug": context.project_slug,
        "project_root_marker": "<PROJECT_ROOT>",
        "evidence_root_relative": "project_analysis_evidence",
        "json_complete_relative": "project_analysis_evidence/json_complete",
        "complete_json_contract": {
            "status": "protected_existing_consumer",
            "mode": "read_hash_reference_only",
            "schema_changed_by_this_bundle": False,
            "hash_before": complete_hash_before,
            "hash_after": complete_hash_after,
            "preserved": complete_json_preserved,
        },
        "written_artifacts": [relative_posix_path(path, context.root) for path in written_paths],
        "generated_artifacts": _generated_records(generated_paths, context),
        "check_result": check_result,
        "failures": failures,
    }
