# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/patch_zip_gate.py
"""Governed patch ZIP creation gate for validated preview artifacts."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ImportMigrationPreview,
    PreviewArtifactValidationResult,
)

__all__ = [
    "PatchZipCreationGateResult",
    "build_patch_zip_creation_gate",
    "resolve_patch_gate_manifest_path",
    "write_patch_gate_manifest",
]

_CHECKED_RULES = [
    "preview_artifact_validation_passed",
    "selected_project_source_not_modified",
    "preview_root_project_support_only",
    "preview_root_outside_project_source",
    "import_migration_preview_only_no_rewrite",
    "patch_payload_creation_deferred",
    "no_freeze_or_error_memory_write",
]


@dataclass(frozen=True)
class PatchZipCreationGateResult:
    """Reviewable gate result before project patch ZIP creation is allowed."""

    schema_version: str
    feature_id: str
    status: str
    patch_zip_creation_enabled: bool
    preview_root: str
    gate_manifest_path: str
    checked_rules: list[str]
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready gate result dictionary."""
        return asdict(self)


def build_patch_zip_creation_gate(
    artifact_result: PreviewArtifactValidationResult,
    import_preview: ImportMigrationPreview | None,
    *,
    active_project_root: str,
) -> PatchZipCreationGateResult:
    """Build a no-payload gate result for future patch ZIP creation."""
    blockers = list(artifact_result.blockers)
    warnings = list(artifact_result.warnings)
    project_root = Path(active_project_root).resolve()
    preview_root = Path(artifact_result.preview_root).resolve()
    if artifact_result.status != "passed":
        blockers.append("PREVIEW_ARTIFACT_VALIDATION_NOT_PASSED")
    if not artifact_result.source_hash_verified:
        blockers.append("SOURCE_HASH_NOT_VERIFIED")
    if not artifact_result.manifest_present:
        blockers.append("PREVIEW_MANIFEST_MISSING")
    if not artifact_result.proof_present:
        blockers.append("NO_SOURCE_WRITE_PROOF_MISSING")
    blockers.extend(_preview_root_blockers(project_root, preview_root))
    if import_preview is None:
        warnings.append("IMPORT_MIGRATION_PREVIEW_NOT_ATTACHED")
    else:
        if import_preview.rewrite_enabled:
            blockers.append("IMPORT_MIGRATION_REWRITE_ENABLED")
        blockers.extend(import_preview.blockers)
        warnings.extend(import_preview.warnings)
    warnings.append("PATCH_PAYLOAD_NOT_CREATED_BY_GATE_TRAIN")
    unique_blockers = sorted(set(blockers))
    status = "gate_open" if not unique_blockers else "blocked"
    manifest_path = resolve_patch_gate_manifest_path(str(project_root), str(preview_root))
    return PatchZipCreationGateResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        patch_zip_creation_enabled=status == "gate_open",
        preview_root=str(preview_root),
        gate_manifest_path=manifest_path,
        checked_rules=list(_CHECKED_RULES),
        blockers=unique_blockers,
        warnings=sorted(set(warnings)),
    )


def resolve_patch_gate_manifest_path(active_project_root: str, preview_root: str) -> str:
    """Return the governed project-support gate manifest path."""
    project_root = Path(active_project_root).resolve()
    root = Path(preview_root).resolve()
    expected = preview_runs_root(project_root)
    if not _is_relative_to(root, expected):
        root = expected
    return str(root / "PATCH_ZIP_CREATION_GATE.json")


def write_patch_gate_manifest(result: PatchZipCreationGateResult) -> str:
    """Write gate evidence only when the manifest path is already governed."""
    path = Path(result.gate_manifest_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    saved = json.loads(path.read_text(encoding="utf-8"))
    if saved.get("feature_id") != FEATURE_ID:
        raise RuntimeError("Patch gate manifest verification failed.")
    return str(path)


def _preview_root_blockers(project_root: Path, preview_root: Path) -> list[str]:
    """Return blockers for Preview roots outside selected project support."""
    return project_preview_root_blockers(project_root, preview_root)


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
