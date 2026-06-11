"""Output path helpers for the additive AI context bundle."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import primary_evidence_json_path

from .project_context import resolve_project_context
from .schema_models import BundleArtifactPaths, ProjectContext

__all__ = [
    "ACTIVE_SNAPSHOT_SUFFIX",
    "BUNDLE_MANIFEST_SUFFIX",
    "EXCLUSION_RULES_SUFFIX",
    "FILE_MANIFEST_SUFFIX",
    "VALIDATION_STATE_SUFFIX",
    "RECONSTRUCTION_PAYLOAD_SUFFIX",
    "bundle_artifact_paths",
]

ACTIVE_SNAPSHOT_SUFFIX = "__active_snapshot.json"
FILE_MANIFEST_SUFFIX = "__file_manifest.json"
EXCLUSION_RULES_SUFFIX = "__exclusion_rules.json"
VALIDATION_STATE_SUFFIX = "__validation_state.json"
BUNDLE_MANIFEST_SUFFIX = "__bundle_manifest.json"
RECONSTRUCTION_PAYLOAD_SUFFIX = "__reconstruction_payload.json"


def _context(value: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(value, ProjectContext):
        return value
    return resolve_project_context(value)


def bundle_artifact_paths(project: str | Path | ProjectContext) -> BundleArtifactPaths:
    """Return all AI context bundle artifact paths for one project."""
    context = _context(project)
    slug = context.project_slug
    output_dir = context.json_complete_dir
    return BundleArtifactPaths(
        complete_json=primary_evidence_json_path(context.root),
        active_snapshot_json=output_dir / f"{slug}{ACTIVE_SNAPSHOT_SUFFIX}",
        file_manifest_json=output_dir / f"{slug}{FILE_MANIFEST_SUFFIX}",
        exclusion_rules_json=output_dir / f"{slug}{EXCLUSION_RULES_SUFFIX}",
        validation_state_json=output_dir / f"{slug}{VALIDATION_STATE_SUFFIX}",
        reconstruction_payload_json=output_dir / f"{slug}{RECONSTRUCTION_PAYLOAD_SUFFIX}",
        bundle_manifest_json=output_dir / f"{slug}{BUNDLE_MANIFEST_SUFFIX}",
    )
