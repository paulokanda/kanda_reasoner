# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_artifact_validation.py
"""Validation for governed preview artifacts and import migration previews."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .workbench_project_support_paths import preview_root_blockers

from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ImportMigrationPreview,
    PreviewArtifactValidationResult,
    PreviewBundle,
    PreviewWriteResult,
)

__all__ = ["validate_preview_artifacts"]


def validate_preview_artifacts(
    bundle: PreviewBundle,
    write_result: PreviewWriteResult,
    *,
    active_project_root: str,
    import_preview: ImportMigrationPreview | None = None,
) -> PreviewArtifactValidationResult:
    """Validate governed preview files without creating patches or touching source."""
    blockers = list(write_result.blockers) + list(bundle.validation_blockers)
    warnings = list(write_result.warnings) + list(bundle.risk_flags)
    project_root = Path(active_project_root).resolve()
    preview_root = Path(write_result.preview_root or bundle.preview_root).resolve()
    checked: list[str] = []

    if write_result.status != "written":
        blockers.append("PREVIEW_ARTIFACTS_NOT_WRITTEN")
    blockers.extend(preview_root_blockers(project_root, preview_root))

    manifest = preview_root / "PREVIEW_MANIFEST.json"
    proof = preview_root / "NO_SOURCE_WRITE_PROOF.txt"
    manifest_present = manifest.exists()
    proof_present = proof.exists()
    if not manifest_present:
        blockers.append("PREVIEW_MANIFEST_MISSING")
    if not proof_present:
        blockers.append("NO_SOURCE_WRITE_PROOF_MISSING")
    if manifest_present:
        checked.append(str(manifest))
        _validate_manifest(manifest, bundle, blockers)
    if proof_present:
        checked.append(str(proof))
        proof_text = proof.read_text(encoding="utf-8", errors="replace")
        if "project_source_modified=false" not in proof_text:
            blockers.append("NO_SOURCE_WRITE_PROOF_INVALID")

    for item in write_result.written_files:
        path = Path(item).resolve()
        checked.append(str(path))
        if not _is_relative_to(path, preview_root):
            blockers.append("WRITTEN_FILE_OUTSIDE_PREVIEW_ROOT")
        if _is_relative_to(path, project_root):
            blockers.append("WRITTEN_FILE_INSIDE_PROJECT_SOURCE")

    source_hash_verified = _source_hash_matches(bundle)
    if not source_hash_verified:
        blockers.append("SOURCE_HASH_NOT_VERIFIED")
    migration_status = "not_generated"
    if import_preview is not None:
        migration_status = import_preview.status
        if import_preview.rewrite_enabled:
            blockers.append("IMPORT_MIGRATION_REWRITE_ENABLED")
        blockers.extend(import_preview.blockers)
        warnings.extend(import_preview.warnings)
    status = "passed" if not blockers else "blocked"
    return PreviewArtifactValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        preview_root=str(preview_root),
        checked_files=sorted(set(checked)),
        source_hash_verified=source_hash_verified,
        manifest_present=manifest_present,
        proof_present=proof_present,
        import_migration_preview_status=migration_status,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def _validate_manifest(manifest: Path, bundle: PreviewBundle, blockers: list[str]) -> None:
    """Validate manifest content against the in-memory preview bundle."""
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        blockers.append("PREVIEW_MANIFEST_INVALID_JSON")
        return
    if data.get("source_content_hash") != bundle.source_content_hash:
        blockers.append("PREVIEW_MANIFEST_SOURCE_HASH_MISMATCH")
    if data.get("target_file") != bundle.target_file:
        blockers.append("PREVIEW_MANIFEST_TARGET_MISMATCH")
    if data.get("write_mode") != bundle.write_mode:
        blockers.append("PREVIEW_MANIFEST_WRITE_MODE_MISMATCH")


def _source_hash_matches(bundle: PreviewBundle) -> bool:
    """Return whether the selected source still matches the carried hash."""
    target = Path(bundle.target_file)
    if not target.exists():
        return False
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return digest == bundle.source_content_hash



def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
