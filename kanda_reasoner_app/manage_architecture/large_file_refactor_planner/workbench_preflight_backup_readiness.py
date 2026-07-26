# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_preflight_backup_readiness.py
"""Preflight source-hash, preview-integrity, collision, and backup readiness."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

from .cst_real_preview_writer import RealPreviewWriteResult
from .models import RefactorPlan, SCHEMA_VERSION
from .preview_writer import resolve_preview_root
from .real_preview_structural_validator import RealPreviewStructuralValidationResult

__all__ = [
    "WORKBENCH_PREFLIGHT_FEATURE_ID",
    "WorkbenchPreflightBackupReadinessResult",
    "build_and_write_preflight_backup_readiness",
]

WORKBENCH_PREFLIGHT_FEATURE_ID = (
    "architecture-review-large-file-refactor-preflight-backup-readiness-v1"
)
_PREFLIGHT_MANIFEST = "WORKBENCH_PREFLIGHT_BACKUP_READINESS.json"
_ROLLBACK_MANIFEST = "WORKBENCH_PREFLIGHT_ROLLBACK_MANIFEST.json"
_BACKUP_DIR = "workbench_preflight_backup"
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_ai",
    "_show_project_to_ai",
}


@dataclass(frozen=True)
class WorkbenchPreflightBackupReadinessResult:
    """Deterministic readiness evidence before source-payload construction."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    preflight_manifest_path: str
    backup_root: str
    backup_snapshot_path: str
    backup_snapshot_hash: str
    rollback_manifest_path: str
    source_hash_verified: bool
    preview_hashes_verified: bool
    destination_collision_free: bool
    backup_destination_writable: bool
    backup_snapshot_verified: bool
    rollback_manifest_prepared: bool
    source_mutation_enabled: bool = False
    apply_enabled: bool = False
    import_rewrite_enabled: bool = False
    checked_preview_files: list[str] = field(default_factory=list)
    checked_destination_paths: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preflight readiness dictionary."""
        return asdict(self)


def build_and_write_preflight_backup_readiness(
    *,
    plan: RefactorPlan | None,
    preview_result: RealPreviewWriteResult | None,
    structural_validation: RealPreviewStructuralValidationResult | None,
    active_project_root: str,
) -> WorkbenchPreflightBackupReadinessResult:
    """Validate the exact preview basis and create verified recovery evidence."""
    project_root = Path(active_project_root).resolve()
    preview_root = _preview_root(project_root, preview_result)
    blockers = _entry_blockers(plan, preview_result, structural_validation)
    target = Path(plan.target_file).resolve() if plan else Path("").resolve()
    source_hash = plan.source_content_hash if plan else ""
    backup_root = preview_root / _BACKUP_DIR
    backup_snapshot = backup_root / "source_snapshot" / target.name
    preflight_manifest = preview_root / _PREFLIGHT_MANIFEST
    rollback_manifest = backup_root / _ROLLBACK_MANIFEST

    blockers.extend(_root_blockers(project_root, preview_root, backup_root))
    source_hash_verified = bool(source_hash and _sha256_file(target) == source_hash)
    if target and plan and not source_hash_verified:
        blockers.append("SOURCE_DRIFT_DETECTED")

    preview_ok, checked_preview, preview_blockers = _verify_preview_hashes(
        preview_root,
        preview_result,
    )
    blockers.extend(preview_blockers)

    collision_free, destinations, collision_blockers = _destination_collision_check(
        project_root,
        target,
        preview_result,
    )
    blockers.extend(collision_blockers)

    writable = _prepare_backup_destination(backup_root, blockers)
    backup_hash = ""
    backup_verified = False
    rollback_prepared = False
    if not blockers and writable and plan is not None:
        backup_hash, backup_verified = _create_verified_snapshot(
            target,
            backup_snapshot,
            source_hash,
            blockers,
        )
        if backup_verified:
            rollback_prepared = _write_rollback_manifest(
                rollback_manifest,
                target,
                backup_snapshot,
                source_hash,
                destinations,
                preview_result,
                blockers,
            )

    status = "preflight_backup_ready" if not blockers and rollback_prepared else "blocked"
    result = WorkbenchPreflightBackupReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_PREFLIGHT_FEATURE_ID,
        status=status,
        target_file=str(target) if plan else "",
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        preflight_manifest_path=str(preflight_manifest),
        backup_root=str(backup_root),
        backup_snapshot_path=str(backup_snapshot),
        backup_snapshot_hash=backup_hash,
        rollback_manifest_path=str(rollback_manifest),
        source_hash_verified=source_hash_verified,
        preview_hashes_verified=preview_ok,
        destination_collision_free=collision_free,
        backup_destination_writable=writable,
        backup_snapshot_verified=backup_verified,
        rollback_manifest_prepared=rollback_prepared,
        source_mutation_enabled=False,
        apply_enabled=False,
        import_rewrite_enabled=False,
        checked_preview_files=checked_preview,
        checked_destination_paths=destinations,
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
    )
    _write_preflight_manifest(result)
    return result


def _entry_blockers(
    plan: RefactorPlan | None,
    preview_result: RealPreviewWriteResult | None,
    structural_validation: RealPreviewStructuralValidationResult | None,
) -> list[str]:
    """Return prerequisite blockers before filesystem readiness checks."""
    blockers: list[str] = []
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
    if preview_result is None or preview_result.status != "real_preview_written":
        blockers.append("REAL_PREVIEW_NOT_READY")
    if structural_validation is None:
        blockers.append("STRUCTURAL_PREVIEW_VALIDATION_MISSING")
    elif not structural_validation.status.startswith("passed"):
        blockers.append("REAL_PREVIEW_STRUCTURAL_VALIDATION_NOT_ACCEPTED")
    if preview_result is not None and preview_result.source_mutation_enabled:
        blockers.append("PREVIEW_RESULT_ENABLED_SOURCE_MUTATION")
    if structural_validation is not None and structural_validation.source_mutation_enabled:
        blockers.append("STRUCTURAL_VALIDATION_ENABLED_SOURCE_MUTATION")
    return blockers


def _verify_preview_hashes(
    preview_root: Path,
    preview_result: RealPreviewWriteResult | None,
) -> tuple[bool, list[str], list[str]]:
    """Verify that every generated preview file still matches recorded content."""
    if preview_result is None:
        return False, [], ["REAL_PREVIEW_RESULT_MISSING"]
    blockers: list[str] = []
    checked: list[str] = []
    for item in preview_result.files:
        path = (preview_root / item.relative_path).resolve()
        checked.append(str(path))
        if not _is_relative_to(path, preview_root):
            blockers.append("PREVIEW_FILE_OUTSIDE_PREVIEW_ROOT:" + item.relative_path)
            continue
        if not path.is_file():
            blockers.append("PREVIEW_FILE_MISSING:" + item.relative_path)
            continue
        actual_hash = _sha256_file(path)
        if actual_hash != item.content_hash:
            blockers.append("PREVIEW_HASH_CHANGED:" + item.relative_path)
    return not blockers, checked, blockers


def _destination_collision_check(
    project_root: Path,
    target: Path,
    preview_result: RealPreviewWriteResult | None,
) -> tuple[bool, list[str], list[str]]:
    """Reject helper destinations that already exist outside the original target."""
    if preview_result is None:
        return False, [], ["REAL_PREVIEW_RESULT_MISSING"]
    blockers: list[str] = []
    destinations: list[str] = []
    target_dir = target.parent.resolve()
    for item in preview_result.files:
        relative = Path(item.relative_path)
        destination = (target_dir / relative).resolve()
        destinations.append(str(destination))
        if relative.is_absolute() or ".." in relative.parts:
            blockers.append("UNSAFE_DESTINATION_RELATIVE_PATH:" + item.relative_path)
            continue
        if destination.parent != target_dir:
            blockers.append("DESTINATION_OUTSIDE_TARGET_DIRECTORY:" + item.relative_path)
        if not _is_relative_to(destination, project_root):
            blockers.append("DESTINATION_OUTSIDE_PROJECT_ROOT:" + item.relative_path)
        if _protected_parts(destination):
            blockers.append("DESTINATION_INSIDE_PROTECTED_ROOT:" + item.relative_path)
        if destination.exists() and destination != target:
            blockers.append("DESTINATION_HELPER_COLLISION:" + item.relative_path)
    return not blockers, destinations, blockers


def _prepare_backup_destination(backup_root: Path, blockers: list[str]) -> bool:
    """Create the backup root and prove it is writable without touching source."""
    try:
        backup_root.mkdir(parents=True, exist_ok=True)
        probe = backup_root / ".kanda_write_probe"
        probe.write_text("preflight-write-probe\n", encoding="utf-8")
        probe.unlink()
        return True
    except OSError:
        blockers.append("BACKUP_DESTINATION_NOT_WRITABLE")
        return False


def _create_verified_snapshot(
    target: Path,
    backup_snapshot: Path,
    source_hash: str,
    blockers: list[str],
) -> tuple[str, bool]:
    """Copy the original target and verify exact content identity."""
    try:
        backup_snapshot.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, backup_snapshot)
    except OSError:
        blockers.append("BACKUP_SNAPSHOT_CREATE_FAILED")
        return "", False
    backup_hash = _sha256_file(backup_snapshot)
    if backup_hash != source_hash:
        blockers.append("BACKUP_SNAPSHOT_HASH_MISMATCH")
        return backup_hash, False
    return backup_hash, True


def _write_rollback_manifest(
    rollback_manifest: Path,
    target: Path,
    backup_snapshot: Path,
    source_hash: str,
    destinations: list[str],
    preview_result: RealPreviewWriteResult | None,
    blockers: list[str],
) -> bool:
    """Prepare explicit recovery intent before future payload application."""
    created = []
    if preview_result is not None:
        created = [
            destination
            for destination in destinations
            if Path(destination).resolve() != target.resolve()
        ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "target_file": str(target),
        "source_content_hash": source_hash,
        "backup_snapshot_path": str(backup_snapshot),
        "restore_modified": [str(target)],
        "delete_if_created": created,
        "source_mutation_enabled": False,
    }
    try:
        rollback_manifest.parent.mkdir(parents=True, exist_ok=True)
        rollback_manifest.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        saved = json.loads(rollback_manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        blockers.append("ROLLBACK_MANIFEST_PREPARE_FAILED")
        return False
    if saved.get("source_content_hash") != source_hash:
        blockers.append("ROLLBACK_MANIFEST_SOURCE_HASH_MISMATCH")
        return False
    return True


def _root_blockers(
    project_root: Path,
    preview_root: Path,
    backup_root: Path,
) -> list[str]:
    """Return No-Leak blockers for all preflight artifact roots."""
    from .workbench_project_support_paths import preview_root_blockers

    blockers: list[str] = list(preview_root_blockers(project_root, preview_root))
    if not _is_relative_to(backup_root, preview_root):
        blockers.append("BACKUP_ROOT_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(backup_root, project_root):
        blockers.append("BACKUP_ROOT_INSIDE_PROJECT_SOURCE")
    if _protected_parts(preview_root) or _protected_parts(backup_root):
        blockers.append("PREFLIGHT_ARTIFACT_ROOT_INSIDE_PROTECTED_ROOT")
    return blockers


def _write_preflight_manifest(result: WorkbenchPreflightBackupReadinessResult) -> None:
    """Write deterministic readiness evidence under preview root only."""
    path = Path(result.preflight_manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    if not _is_relative_to(path, preview_root):
        raise RuntimeError("Preflight readiness manifest path is outside preview root.")
    if _protected_parts(path):
        raise RuntimeError("Preflight readiness manifest path is protected.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    saved = json.loads(path.read_text(encoding="utf-8"))
    for field_name in ("source_mutation_enabled", "apply_enabled", "import_rewrite_enabled"):
        if saved.get(field_name) is not False:
            raise RuntimeError("Preflight readiness must keep mutation gates disabled: " + field_name)


def _checked_rules() -> list[str]:
    """Return stable rule labels for the readiness evidence."""
    return [
        "planner_plan_required",
        "real_preview_required",
        "structural_preview_validation_must_be_accepted",
        "selected_source_hash_must_match_plan_basis",
        "preview_file_hashes_must_match_generation_evidence",
        "destination_helper_collisions_must_be_absent",
        "preview_and_backup_roots_must_stay_outside_project_source",
        "backup_destination_must_be_writable",
        "backup_snapshot_hash_must_match_source_basis",
        "rollback_manifest_must_be_prepared",
        "preflight_never_enables_source_mutation",
    ]


def _warnings() -> list[str]:
    """Return stable operator warnings."""
    return [
        "PREFLIGHT_BACKUP_IS_RECOVERY_EVIDENCE_NOT_SOURCE_TRUTH",
        "PREFLIGHT_DOES_NOT_AUTHORIZE_APPLY",
        "PREVIEW_DRIFT_OR_SOURCE_DRIFT_INVALIDATES_READINESS",
    ]


def _preview_root(
    project_root: Path,
    preview_result: RealPreviewWriteResult | None,
) -> Path:
    """Return the current preview root or the governed default root."""
    if preview_result is not None and preview_result.preview_root:
        return Path(preview_result.preview_root).resolve()
    return Path(resolve_preview_root(str(project_root))).resolve()


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for one file or empty text when unavailable."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _protected_parts(path: Path) -> list[str]:
    """Return protected path components present after path resolution."""
    return [part for part in (item.lower() for item in path.resolve().parts) if part in _PROTECTED_PARTS]


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return whether a resolved path is contained by a resolved root."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
