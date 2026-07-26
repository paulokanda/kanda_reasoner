# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/project_patch_payload.py
"""Governed project patch payload ZIP creation from validated previews."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ImportMigrationPreview,
    PreviewArtifactValidationResult,
    PreviewBundle,
    ProjectPatchPayloadResult,
)
from .patch_zip_gate import PatchZipCreationGateResult

__all__ = ["create_project_patch_payload_zip", "resolve_project_patch_payload_paths"]

_PAYLOAD_ZIP_NAME = "large_file_refactor_project_patch_payload.zip"
_PAYLOAD_MANIFEST_NAME = "PROJECT_PATCH_PAYLOAD_MANIFEST.json"


def create_project_patch_payload_zip(
    gate: PatchZipCreationGateResult,
    bundle: PreviewBundle,
    artifact_result: PreviewArtifactValidationResult,
    import_preview: ImportMigrationPreview | None,
    *,
    active_project_root: str,
) -> ProjectPatchPayloadResult:
    """Create a governed project-owned patch payload ZIP from preview artifacts."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(bundle.preview_root).resolve()
    payload_zip, payload_manifest = resolve_project_patch_payload_paths(
        active_project_root,
        str(preview_root),
    )
    blockers = _payload_blockers(gate, bundle, artifact_result, import_preview, project_root)
    warnings = list(gate.warnings) + ["PROJECT_PAYLOAD_CREATED_FROM_PREVIEW_ONLY"]
    files = _collect_payload_files(bundle, preview_root, project_root, payload_zip)
    if not files:
        blockers.append("NO_PREVIEW_FILES_FOR_PAYLOAD")
    if blockers:
        return ProjectPatchPayloadResult(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            status="blocked",
            payload_zip_path=str(payload_zip),
            payload_manifest_path=str(payload_manifest),
            preview_root=str(preview_root),
            included_files=[str(p.relative_to(preview_root)).replace("\\", "/") for p in files],
            source_hash_verified=False,
            patch_payload_created=False,
            blockers=sorted(set(blockers)),
            warnings=sorted(set(warnings)),
        )
    manifest_data = _build_payload_manifest(bundle, artifact_result, import_preview, files, preview_root)
    payload_manifest.write_text(json.dumps(manifest_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files.append(payload_manifest)
    with zipfile.ZipFile(payload_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(preview_root).as_posix())
    _verify_payload_zip(payload_zip, payload_manifest, preview_root)
    return ProjectPatchPayloadResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status="payload_ready",
        payload_zip_path=str(payload_zip),
        payload_manifest_path=str(payload_manifest),
        preview_root=str(preview_root),
        included_files=[str(p.relative_to(preview_root)).replace("\\", "/") for p in files],
        source_hash_verified=True,
        patch_payload_created=True,
        blockers=[],
        warnings=sorted(set(warnings)),
    )


def resolve_project_patch_payload_paths(active_project_root: str, preview_root: str) -> tuple[Path, Path]:
    """Return payload ZIP and manifest paths inside project Preview support."""
    project_root = Path(active_project_root).resolve()
    root = Path(preview_root).resolve()
    expected = preview_runs_root(project_root)
    if not _is_relative_to(root, expected):
        root = expected
    return root / _PAYLOAD_ZIP_NAME, root / _PAYLOAD_MANIFEST_NAME


def _payload_blockers(
    gate: PatchZipCreationGateResult,
    bundle: PreviewBundle,
    artifact_result: PreviewArtifactValidationResult,
    import_preview: ImportMigrationPreview | None,
    project_root: Path,
) -> list[str]:
    """Return blockers for unsafe payload creation."""
    blockers = list(gate.blockers) + list(artifact_result.blockers)
    preview_root = Path(bundle.preview_root).resolve()
    if not gate.patch_zip_creation_enabled or gate.status != "gate_open":
        blockers.append("PATCH_GATE_NOT_OPEN")
    if artifact_result.status != "passed":
        blockers.append("PREVIEW_ARTIFACT_VALIDATION_NOT_PASSED")
    if not artifact_result.source_hash_verified:
        blockers.append("SOURCE_HASH_NOT_VERIFIED")
    blockers.extend(_preview_root_blockers(project_root, preview_root))
    if import_preview is None:
        blockers.append("IMPORT_MIGRATION_PREVIEW_MISSING")
    elif import_preview.rewrite_enabled:
        blockers.append("IMPORT_MIGRATION_REWRITE_ENABLED")
    target = Path(bundle.target_file).resolve()
    if _is_relative_to(target, preview_root):
        blockers.append("TARGET_FILE_INSIDE_PREVIEW_ROOT")
    if target.exists():
        current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if current_hash != bundle.source_content_hash:
            blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    else:
        blockers.append("TARGET_FILE_MISSING")
    return blockers


def _collect_payload_files(
    bundle: PreviewBundle,
    preview_root: Path,
    project_root: Path,
    payload_zip: Path,
) -> list[Path]:
    """Collect preview files that are safe to package."""
    safe: list[Path] = []
    known = ["PREVIEW_MANIFEST.json", "NO_SOURCE_WRITE_PROOF.txt", "IMPORT_MIGRATION_PREVIEW.json", "PATCH_ZIP_CREATION_GATE.json"]
    for name in known:
        path = preview_root / name
        if _safe_payload_file(path, preview_root, project_root, payload_zip):
            safe.append(path)
    for draft in bundle.files:
        path = preview_root / draft.relative_path
        if _safe_payload_file(path, preview_root, project_root, payload_zip):
            safe.append(path)
    unique = []
    seen: set[Path] = set()
    for path in safe:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def _safe_payload_file(path: Path, preview_root: Path, project_root: Path, payload_zip: Path) -> bool:
    """Return whether a file can be included in the project patch payload."""
    resolved = path.resolve()
    if resolved == payload_zip.resolve():
        return False
    if not resolved.exists() or not resolved.is_file():
        return False
    if not _is_relative_to(resolved, preview_root):
        return False
    if _is_relative_to(resolved, project_root):
        return False
    lowered = {part.lower() for part in resolved.parts}
    return not {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"} & lowered


def _build_payload_manifest(
    bundle: PreviewBundle,
    artifact_result: PreviewArtifactValidationResult,
    import_preview: ImportMigrationPreview | None,
    files: list[Path],
    preview_root: Path,
) -> dict[str, object]:
    """Build the payload manifest without treating preview artifacts as source of truth."""
    return {
        "schema_version": SCHEMA_VERSION,
        "feature_id": FEATURE_ID,
        "payload_kind": "large_file_refactor_project_preview_payload",
        "status": "payload_ready",
        "target_file": bundle.target_file,
        "source_content_hash": bundle.source_content_hash,
        "preview_root": str(preview_root),
        "artifact_validation_status": artifact_result.status,
        "import_migration_status": getattr(import_preview, "status", "missing"),
        "import_rewrite_enabled": bool(getattr(import_preview, "rewrite_enabled", False)),
        "included_files": [path.relative_to(preview_root).as_posix() for path in files],
        "apply_to_source": False,
        "requires_human_review": True,
    }


def _verify_payload_zip(payload_zip: Path, payload_manifest: Path, preview_root: Path) -> None:
    """Verify the generated payload ZIP contains the governed manifest."""
    if not payload_zip.exists() or payload_zip.stat().st_size <= 0:
        raise RuntimeError("Project patch payload ZIP was not created.")
    with zipfile.ZipFile(payload_zip, "r") as archive:
        names = set(archive.namelist())
    manifest_name = payload_manifest.relative_to(preview_root).as_posix()
    if manifest_name not in names:
        raise RuntimeError("Project patch payload manifest missing from ZIP.")


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
