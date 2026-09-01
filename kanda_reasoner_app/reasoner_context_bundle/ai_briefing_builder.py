# project-path: kanda_reasoner_app/reasoner_context_bundle/ai_briefing_builder.py
"""Build the AI-first briefing artifact for a dynamic project scan."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_artifact_staging import (
    build_project_artifact_staging_contract,
)

from .handoff_boundary_contract import build_handoff_trust_envelope
from .hashing import sha256_file
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .path_normalization import artifact_logical_posix_path
from .project_context import resolve_project_context
from .schema_models import ProjectContext
from .source_state_identity import load_source_state_identity

__all__ = [
    "build_ai_briefing_payload",
    "write_ai_briefing_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "ai_briefing"
GENERATOR_NAME = "reasoner_context_bundle.ai_briefing_builder"
GENERATOR_VERSION = "1.6.0"


def _utc_now() -> str:
    """Support utc now behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


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


def _path_record(
    path: Path,
    context: ProjectContext,
    *,
    mutual_reference: bool = False,
    self_reference: bool = False,
) -> dict[str, Any]:
    """Support path record behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    context : ProjectContext
        The context value.
    mutual_reference : bool, optional
        The optional mutual reference value.
    self_reference : bool, optional
        The optional self reference value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    exists = path.exists() and path.is_file()
    record = {
        "path": artifact_logical_posix_path(path, context),
        "exists": exists,
        "sha256": "",
        "size_bytes": path.stat().st_size if exists else 0,
    }
    if self_reference:
        record["sha256"] = ""
        record["size_bytes"] = 0
        record["hash_status"] = "self_hash_not_embedded"
        record["size_status"] = "self_size_not_embedded"
        record["self_reference"] = True
        record["reason"] = (
            "The AI briefing cannot embed its own final sha256 or final size "
            "without changing that artifact. The bundle manifest is the hash "
            "authority for generated artifacts."
        )
        return record
    if mutual_reference:
        record["hash_status"] = "not_embedded_mutual_reference"
        record["reason"] = (
            "The first-read briefing and bundle manifest can reference each "
            "other. The bundle manifest is the hash authority for generated "
            "artifacts; this briefing records existence and path only for the "
            "manifest to avoid stale mutual hashes."
        )
        return record
    if exists:
        record["sha256"] = sha256_file(path)
        record["hash_status"] = "sha256"
    else:
        record["hash_status"] = "missing"
    return record


def build_ai_briefing_payload(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Build a compact first-read briefing for AI project handoff."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    source_state = load_source_state_identity(paths.file_manifest_json)
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": _utc_now(),
        "handoff_trust": build_handoff_trust_envelope(context),
        "artifact_staging": build_project_artifact_staging_contract(context.root),
        "project": {
            "project_slug": context.project_slug,
            "active_project_id": context.active_project_id,
            "active_project_root_fingerprint": context.active_project_root_fingerprint,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
            "dynamic_path_policy": (
                "Evidence is generated for the selected project root. The real "
                "output folder is <project_drive>:\\<project_slug>_show_project_to_AI\\second_prompt_files."
            ),
        },
        "purpose": {
            "summary": (
                "First-read AI briefing for the selected project. Use this file "
                "to orient the AI before loading larger evidence artifacts."
            ),
            "deliver_project_to_ai_use": True,
        },
        "source_truth_policy": {
            "source_files_are_truth": True,
            "json_is_evidence_not_truth": True,
            "inspect_exact_source_before_editing": True,
            "do_not_patch_from_summaries_alone": True,
        },
        "first_read_order": [
            "ai_briefing_json",
            "routing_manifest_json",
            "bundle_manifest_json",
            "patch_safety_routes_json",
            "source_archive_manifest_json for exact reconstruction map",
        ],
        "default_loading_policy": {
            "always_read": ["ai_briefing_json", "routing_manifest_json"],
            "read_for_routing": ["bundle_manifest_json", "file_manifest_json"],
            "read_for_subsystem_edit": ["patch_safety_routes_json", "file_manifest_json"],
            "read_only_on_request": ["runtime raw traces", "full large indexes"],
        },
        "generated_files_policy": {
            "generated_files_are_not_source_truth": True,
            "do_not_edit_generated_evidence_as_source": True,
            "evidence_folder_logical_prefix": "show_project_to_AI",
        },
        "source_state": source_state,
        "source_state_policy": {
            "canonical_owner": "file_manifest_json",
            "source_archive_is_verified_subset_projection": True,
            "source_archive_has_distinct_projection_identity": True,
            "handoff_is_a_verified_source_snapshot": True,
            "handoff_is_not_live_source_authority_after_export": True,
            "post_export_source_changes_require_new_handoff_or_local_baseline_check": True,
        },
        "evidence_files": {
            "ai_briefing_json": _path_record(
                paths.ai_briefing_json,
                context,
                self_reference=True,
            ),
            "routing_manifest_json": _path_record(paths.routing_manifest_json, context),
            "bundle_manifest_json": _path_record(paths.bundle_manifest_json, context, mutual_reference=True),
            "file_manifest_json": _path_record(paths.file_manifest_json, context),
            "validation_state_json": _path_record(paths.validation_state_json, context),
            "patch_safety_routes_json": _path_record(paths.patch_safety_routes_json, context),
        },
        "freshness_policy": {
            "if_evidence_is_stale": (
                "Use generated JSON for orientation only, then inspect exact source files."
            ),
            "after_meaningful_source_change": "Run Project Structure Map again.",
            "source_state_sha256_is_snapshot_identity_not_live_memory": True,
        },
        "fallback_policy": {
            "if_route_is_missing": (
                "Use file_manifest and source_archive_manifest to find the exact source files, "
                "then inspect source before editing."
            )
        },
    }


def write_ai_briefing_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__ai_briefing.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_ai_briefing_payload(context)
    return write_json_atomic(paths.ai_briefing_json, payload)
