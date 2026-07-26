# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_preflight_backup_contract.py
"""Source-derived backup readiness contract for the legacy guarded apply path."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

from .models import FEATURE_ID, SCHEMA_VERSION
from .source_apply_dry_run_validator import SourceApplyDryRunValidationResult

__all__ = [
    "SourceApplyPreflightBackupContractResult",
    "build_source_apply_preflight_backup_contract",
    "write_source_apply_preflight_backup_contract_manifest",
]

_PREFLIGHT_MANIFEST_NAME = "SOURCE_APPLY_PREFLIGHT_BACKUP_CONTRACT.json"
_BACKUP_FOLDER = "source_apply_preflight_backup"
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
class SourceApplyPreflightBackupContractResult:
    """Backup readiness evidence consumed by the legacy guarded apply owner."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    dry_run_manifest_path: str
    preflight_manifest_path: str
    backup_snapshot_path: str
    backup_snapshot_hash: str
    source_hash_verified: bool
    backup_snapshot_verified: bool
    rollback_ready: bool
    apply_enabled: bool = False
    rewrite_enabled: bool = False
    source_mutation_enabled: bool = False
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preflight contract dictionary."""
        return asdict(self)


def build_source_apply_preflight_backup_contract(
    dry_run: SourceApplyDryRunValidationResult,
    *,
    active_project_root: str,
) -> SourceApplyPreflightBackupContractResult:
    """Create and verify one source-derived backup snapshot in project support state."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(dry_run.preview_root).resolve()
    target = Path(dry_run.target_file).resolve()
    dry_run_manifest = Path(dry_run.dry_run_manifest_path).resolve()
    preflight_manifest = preview_root / _PREFLIGHT_MANIFEST_NAME
    backup_root = preview_root / _BACKUP_FOLDER
    backup_snapshot = backup_root / target.name
    blockers = _entry_blockers(
        dry_run,
        project_root,
        preview_root,
        target,
        dry_run_manifest,
        preflight_manifest,
        backup_snapshot,
    )
    backup_hash = ""
    if not blockers:
        try:
            backup_root.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_snapshot)
            backup_hash = _sha256_file(backup_snapshot)
            if backup_hash != dry_run.source_content_hash:
                blockers.append("BACKUP_SNAPSHOT_HASH_MISMATCH")
        except OSError:
            blockers.append("BACKUP_SNAPSHOT_CREATE_FAILED")
    status = "source_apply_preflight_backup_ready" if not blockers else "blocked"
    return SourceApplyPreflightBackupContractResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=dry_run.source_content_hash,
        preview_root=str(preview_root),
        dry_run_manifest_path=str(dry_run_manifest),
        preflight_manifest_path=str(preflight_manifest),
        backup_snapshot_path=str(backup_snapshot),
        backup_snapshot_hash=backup_hash,
        source_hash_verified=_sha256_file(target) == dry_run.source_content_hash,
        backup_snapshot_verified=bool(backup_hash and backup_hash == dry_run.source_content_hash),
        rollback_ready=status == "source_apply_preflight_backup_ready",
        apply_enabled=False,
        rewrite_enabled=False,
        source_mutation_enabled=False,
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
    )


def write_source_apply_preflight_backup_contract_manifest(
    result: SourceApplyPreflightBackupContractResult,
) -> Path:
    """Write the preflight contract beside other governed preview evidence."""
    manifest = Path(result.preflight_manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Preflight manifest path is outside preview root.")
    if _protected_parts(manifest):
        raise RuntimeError("Preflight manifest path is inside a protected root.")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("apply_enabled") is not False:
        raise RuntimeError("Preflight contract must not enable apply.")
    if saved.get("rewrite_enabled") is not False:
        raise RuntimeError("Preflight contract must not enable import rewrite.")
    if saved.get("source_mutation_enabled") is not False:
        raise RuntimeError("Preflight contract must not enable source mutation.")
    return manifest


def _entry_blockers(
    dry_run: SourceApplyDryRunValidationResult,
    project_root: Path,
    preview_root: Path,
    target: Path,
    dry_run_manifest: Path,
    preflight_manifest: Path,
    backup_snapshot: Path,
) -> list[str]:
    """Return deterministic blockers before backup creation."""
    blockers: list[str] = list(dry_run.blockers)
    if dry_run.status != "source_apply_dry_run_validated":
        blockers.append("SOURCE_APPLY_DRY_RUN_NOT_VALIDATED")
    if dry_run.apply_enabled is not False:
        blockers.append("DRY_RUN_APPLY_ENABLED_UNEXPECTEDLY")
    if dry_run.rewrite_enabled is not False:
        blockers.append("DRY_RUN_REWRITE_ENABLED_UNEXPECTEDLY")
    if dry_run.source_mutation_enabled is not False:
        blockers.append("DRY_RUN_SOURCE_MUTATION_ENABLED_UNEXPECTEDLY")
    from .workbench_project_support_paths import preview_root_blockers

    blockers.extend(preview_root_blockers(project_root, preview_root))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, dry_run_manifest, "DRY_RUN_MANIFEST"))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, preflight_manifest, "PREFLIGHT_MANIFEST"))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, backup_snapshot, "BACKUP_SNAPSHOT"))
    if not dry_run_manifest.is_file():
        blockers.append("DRY_RUN_MANIFEST_MISSING")
    if not target.is_file():
        blockers.append("TARGET_FILE_MISSING")
    elif not _is_relative_to(target, project_root):
        blockers.append("TARGET_OUTSIDE_PROJECT_ROOT")
    elif _protected_parts(target):
        blockers.append("TARGET_INSIDE_PROTECTED_ROOT")
    elif _sha256_file(target) != dry_run.source_content_hash:
        blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    return blockers


def _artifact_path_blockers(
    project_root: Path,
    preview_root: Path,
    path: Path,
    label: str,
) -> list[str]:
    """Return No-Leak blockers for support artifacts."""
    blockers: list[str] = []
    if not _is_relative_to(path, preview_root):
        blockers.append(label + "_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    if _protected_parts(path):
        blockers.append(label + "_INSIDE_PROTECTED_ROOT")
    return blockers


def _checked_rules() -> list[str]:
    """Return stable rule labels recorded in evidence."""
    return [
        "dry_run_validation_required",
        "selected_source_hash_must_match_plan_basis",
        "preview_root_inside_project_support_only",
        "backup_snapshot_must_remain_outside_project_source",
        "backup_snapshot_hash_must_match_source_basis",
        "protected_support_roots_must_not_be_used",
        "preflight_contract_never_enables_apply",
        "preflight_contract_never_enables_import_rewrite",
        "preflight_contract_never_enables_source_mutation",
    ]


def _warnings() -> list[str]:
    """Return stable operator warnings."""
    return [
        "BACKUP_IS_RECOVERY_EVIDENCE_NOT_CANONICAL_SOURCE",
        "PREFLIGHT_CONTRACT_DOES_NOT_AUTHORIZE_SOURCE_APPLY",
        "PROJECT_SOURCE_REMAINS_UNCHANGED_DURING_PREFLIGHT",
    ]


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for one file or an empty value on read failure."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _protected_parts(path: Path) -> list[str]:
    """Return protected root components found in a resolved path."""
    return [part for part in (item.lower() for item in path.resolve().parts) if part in _PROTECTED_PARTS]


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return whether a resolved path is inside a resolved root."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
