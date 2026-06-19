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
GENERATOR_VERSION = "1.1.0"

BUNDLE_ARTIFACT_ORDER = (
    "complete_json",
    "exclusion_rules_json",
    "file_manifest_json",
    "active_snapshot_json",
    "validation_state_json",
    "reconstruction_payload_json",
    "bundle_manifest_json",
)

_ARTIFACT_KIND_BY_NAME = {
    "complete_json": "complete_graph",
    "exclusion_rules_json": "exclusion_rules",
    "file_manifest_json": "file_manifest",
    "active_snapshot_json": "active_snapshot",
    "validation_state_json": "validation_state",
    "reconstruction_payload_json": "reconstruction_payload",
    "bundle_manifest_json": "bundle_manifest",
}

_REQUIRED_BY_NAME = {
    "complete_json": True,
    "exclusion_rules_json": True,
    "file_manifest_json": True,
    "active_snapshot_json": True,
    "validation_state_json": True,
    "reconstruction_payload_json": True,
    "bundle_manifest_json": True,
}


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _relative_artifact_path(path: Path, context: ProjectContext) -> str:
    return artifact_logical_posix_path(path, context)


def _artifact_record(
    name: str,
    path: Path,
    context: ProjectContext,
) -> dict[str, Any]:
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
        record["reason"] = (
            "The bundle manifest cannot embed its own final sha256 without "
            "changing that sha256. Existence is verified by the bundle checker."
        )
        return record
    if exists:
        record["sha256"] = sha256_file(path)
        record["hash_status"] = "sha256"
    else:
        record["hash_status"] = "missing"
    return record


def _artifact_paths_by_name(paths: BundleArtifactPaths) -> dict[str, Path]:
    return {
        "complete_json": paths.complete_json,
        "exclusion_rules_json": paths.exclusion_rules_json,
        "file_manifest_json": paths.file_manifest_json,
        "active_snapshot_json": paths.active_snapshot_json,
        "validation_state_json": paths.validation_state_json,
        "reconstruction_payload_json": paths.reconstruction_payload_json,
        "bundle_manifest_json": paths.bundle_manifest_json,
    }


def _artifact_records(context: ProjectContext, paths: BundleArtifactPaths) -> list[dict[str, Any]]:
    by_name = _artifact_paths_by_name(paths)
    return [
        _artifact_record(name, by_name[name], context)
        for name in BUNDLE_ARTIFACT_ORDER
    ]


def _counts(artifacts: list[dict[str, Any]]) -> dict[str, int]:
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


def _complete_json_contract() -> dict[str, Any]:
    return {
        "status": "protected_existing_consumer",
        "consumer_box": "engineering_safety",
        "mode": "read_hash_reference_only",
        "schema_changed_by_this_bundle": False,
        "engineering_safety_impact": "none_in_additive_mode",
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
            "evidence_root_relative": "project_analysis_evidence",
            "json_complete_relative": "project_analysis_evidence/json_complete",
        },
        "compatibility": {
            "additive_bundle": True,
            "complete_json_unchanged_by_contract": True,
            "project_specific_dynamic_rules": True,
            "hardcoded_project_root": False,
        },
        "complete_json_contract": _complete_json_contract(),
        "counts": _counts(artifacts),
        "artifacts": artifacts,
    }


def write_bundle_manifest_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__bundle_manifest.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_bundle_manifest_payload(context)
    return write_json_atomic(paths.bundle_manifest_json, payload)
