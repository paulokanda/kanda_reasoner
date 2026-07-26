# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_rollback_recovery.py
"""Rollback and recovery contract for guarded large-file source application."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import FEATURE_ID, SCHEMA_VERSION

__all__ = [
    "SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN",
    "SourceApplyRollbackRecoveryResult",
    "build_source_apply_rollback_recovery",
    "write_source_apply_rollback_recovery_manifest",
]

SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN = "CONFIRM_EXECUTE_SOURCE_APPLY_ROLLBACK_RECOVERY"
_ROLLBACK_MANIFEST_NAME = "SOURCE_APPLY_ROLLBACK_RECOVERY.json"
_POST_APPLY_MANIFEST_NAME = "POST_APPLY_VALIDATION_HASH_EVIDENCE.json"


@dataclass(frozen=True)
class SourceApplyRollbackRecoveryResult:
    """Recovery result for restoring selected source from a verified backup snapshot."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    preview_root: str
    post_apply_manifest_path: str
    rollback_manifest_path: str
    backup_snapshot_path: str
    source_content_hash_before: str
    source_content_hash_after_apply: str
    source_content_hash_current: str
    source_content_hash_after_rollback: str
    confirmation_token_required: str
    rollback_confirmation_present: bool
    rollback_confirmation_valid: bool
    rollback_enabled: bool = False
    restore_source_from_backup_enabled: bool = False
    import_rewrite_rollback_enabled: bool = False
    backup_snapshot_verified: bool = False
    current_source_hash_verified: bool = False
    selected_source_restored: bool = False
    backup_snapshot_unchanged_after_restore: bool = False
    non_target_written_files_removed: bool = False
    written_files: list[str] = field(default_factory=list)
    non_target_written_files: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready rollback/recovery dictionary."""
        return asdict(self)


def build_source_apply_rollback_recovery(
    post_apply_manifest_path: str,
    *,
    active_project_root: str,
    rollback_confirmation: str = "",
) -> SourceApplyRollbackRecoveryResult:
    """Build rollback readiness without mutating source until the writer runs."""
    project_root = Path(active_project_root).resolve()
    post_apply_manifest = Path(post_apply_manifest_path).resolve()
    post_apply = _read_json_file(post_apply_manifest)
    preview_root = Path(str(post_apply.get("preview_root", post_apply_manifest.parent))).resolve()
    target = Path(str(post_apply.get("target_file", ""))).resolve()
    backup = Path(str(post_apply.get("backup_snapshot_path", ""))).resolve()
    before_hash = str(post_apply.get("source_content_hash_before", ""))
    after_hash = str(post_apply.get("source_content_hash_after_actual", ""))
    current_hash = _sha256_file(target) if target.is_file() else ""
    written = [str(item) for item in post_apply.get("written_files", []) if str(item)]
    token_valid = rollback_confirmation.strip() == SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN
    blockers = _rollback_blockers(
        project_root,
        preview_root,
        post_apply_manifest,
        post_apply,
        target,
        backup,
        before_hash,
        after_hash,
        current_hash,
        token_valid,
        written,
    )
    status = "rollback_recovery_ready" if not blockers else "blocked"
    non_target = _non_target_files(target, written)
    return SourceApplyRollbackRecoveryResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        preview_root=str(preview_root),
        post_apply_manifest_path=str(post_apply_manifest),
        rollback_manifest_path=str(preview_root / _ROLLBACK_MANIFEST_NAME),
        backup_snapshot_path=str(backup),
        source_content_hash_before=before_hash,
        source_content_hash_after_apply=after_hash,
        source_content_hash_current=current_hash,
        source_content_hash_after_rollback="",
        confirmation_token_required=SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN,
        rollback_confirmation_present=bool(rollback_confirmation.strip()),
        rollback_confirmation_valid=token_valid,
        rollback_enabled=status == "rollback_recovery_ready",
        restore_source_from_backup_enabled=status == "rollback_recovery_ready",
        import_rewrite_rollback_enabled=False,
        backup_snapshot_verified="BACKUP_SNAPSHOT_HASH_MISMATCH" not in blockers and "BACKUP_SNAPSHOT_MISSING" not in blockers,
        current_source_hash_verified="CURRENT_SOURCE_HASH_MISMATCH" not in blockers and "TARGET_FILE_MISSING" not in blockers,
        selected_source_restored=False,
        backup_snapshot_unchanged_after_restore=False,
        non_target_written_files_removed=False,
        written_files=sorted(written),
        non_target_written_files=sorted(non_target),
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=_warnings(non_target),
    )


def write_source_apply_rollback_recovery_manifest(result: SourceApplyRollbackRecoveryResult) -> Path:
    """Restore selected source from backup when ready and write recovery evidence."""
    manifest = Path(result.rollback_manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    target = Path(result.target_file).resolve()
    backup = Path(result.backup_snapshot_path).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Rollback recovery manifest path is outside preview root.")
    _raise_if_protected(manifest, "rollback manifest")
    payload = result.to_dict()
    if result.status == "rollback_recovery_ready":
        if _sha256_file(target) != result.source_content_hash_after_apply:
            raise RuntimeError("Current source hash changed after rollback readiness check.")
        before_backup_hash = _sha256_file(backup)
        target.write_bytes(backup.read_bytes())
        after_target_hash = _sha256_file(target)
        after_backup_hash = _sha256_file(backup)
        payload["source_content_hash_after_rollback"] = after_target_hash
        payload["selected_source_restored"] = after_target_hash == result.source_content_hash_before
        payload["backup_snapshot_unchanged_after_restore"] = before_backup_hash == after_backup_hash
        payload["status"] = "source_apply_rollback_recovered" if payload["selected_source_restored"] else "blocked"
        payload["rollback_enabled"] = True
        payload["restore_source_from_backup_enabled"] = True
    else:
        payload["rollback_enabled"] = False
        payload["restore_source_from_backup_enabled"] = False
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("import_rewrite_rollback_enabled") is not False:
        raise RuntimeError("Import rewrite rollback is not implemented in this train.")
    if saved.get("status") == "source_apply_rollback_recovered" and saved.get("source_content_hash_after_rollback") != saved.get("source_content_hash_before"):
        raise RuntimeError("Rollback manifest does not prove restoration to before hash.")
    return manifest


def _rollback_blockers(
    project_root: Path,
    preview_root: Path,
    post_apply_manifest: Path,
    post_apply: dict[str, object],
    target: Path,
    backup: Path,
    before_hash: str,
    after_hash: str,
    current_hash: str,
    token_valid: bool,
    written: list[str],
) -> list[str]:
    """Return blockers that prevent rollback recovery."""
    blockers: list[str] = []
    if not token_valid:
        blockers.append("ROLLBACK_RECOVERY_TOKEN_MISSING_OR_INVALID")
    if not post_apply_manifest.is_file():
        blockers.append("POST_APPLY_MANIFEST_MISSING")
    if post_apply.get("status") not in {"post_apply_validation_passed", "blocked"}:
        blockers.append("POST_APPLY_VALIDATION_STATUS_UNRECOGNIZED")
    if bool(post_apply.get("loose_preview_artifacts_used_as_source_of_truth")):
        blockers.append("LOOSE_PREVIEW_ARTIFACTS_USED_AS_SOURCE_OF_TRUTH")
    if bool(post_apply.get("import_rewrite_applied")):
        blockers.append("IMPORT_REWRITE_APPLIED_NOT_ROLLBACKABLE_IN_THIS_TRAIN")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, post_apply_manifest, "POST_APPLY_MANIFEST"))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, backup, "BACKUP_SNAPSHOT"))
    blockers.extend(_target_path_blockers(project_root, target, "TARGET"))
    if not backup.is_file():
        blockers.append("BACKUP_SNAPSHOT_MISSING")
    elif before_hash and _sha256_file(backup) != before_hash:
        blockers.append("BACKUP_SNAPSHOT_HASH_MISMATCH")
    if not target.is_file():
        blockers.append("TARGET_FILE_MISSING")
    if not before_hash or not after_hash or before_hash == after_hash:
        blockers.append("ROLLBACK_HASH_TRANSITION_INVALID")
    if after_hash and current_hash != after_hash:
        blockers.append("CURRENT_SOURCE_HASH_MISMATCH")
    for item in written:
        path = Path(item).resolve()
        blockers.extend(_target_path_blockers(project_root, path, "WRITTEN_FILE"))
    return blockers


def _artifact_path_blockers(project_root: Path, preview_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for recovery support artifacts."""
    blockers: list[str] = []
    if not _is_relative_to(path, preview_root):
        blockers.append(label + "_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    blockers.extend(_protected_root_blockers(path, label))
    return blockers


def _target_path_blockers(project_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for active project source paths."""
    blockers: list[str] = []
    if not _is_relative_to(path, project_root):
        blockers.append(label + "_OUTSIDE_PROJECT_SOURCE")
    blockers.extend(_protected_root_blockers(path, label))
    return blockers


def _protected_root_blockers(path: Path, label: str) -> list[str]:
    """Return blockers for protected support and reference roots."""
    lowered = {part.lower() for part in path.parts}
    blockers: list[str] = []
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append(label + "_INSIDE_PROTECTED_" + forbidden.upper())
    if ".project_reference" in lowered or "_project_reference" in lowered:
        blockers.append(label + "_INSIDE_PROJECT_REFERENCE")
    return blockers


def _non_target_files(target: Path, written: list[str]) -> list[str]:
    """Return written files that are not the selected source target."""
    target_resolved = target.resolve()
    result: list[str] = []
    for item in written:
        path = Path(item).resolve()
        if path != target_resolved:
            result.append(str(path))
    return result


def _read_json_file(path: Path) -> dict[str, object]:
    """Return a JSON object from path, or an empty mapping when invalid."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for a file, or an empty string when missing."""
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""


def _raise_if_protected(path: Path, label: str) -> None:
    """Raise if a recovery evidence path reaches a protected root."""
    if _protected_root_blockers(path, label):
        raise RuntimeError(label + " path is inside a protected or reference root.")


def _checked_rules() -> list[str]:
    """Return stable rule labels checked by rollback recovery."""
    return [
        "rollback_recovery_token_exact_match",
        "post_apply_validation_manifest_readiness_checked",
        "source_derived_backup_snapshot_verified",
        "selected_source_hash_matches_post_apply_hash_before_restore",
        "selected_source_restored_to_before_hash",
        "backup_snapshot_unchanged_after_restore",
        "support_artifacts_inside_project_support_preview_root_only",
        "project_reference_roots_excluded_from_recovery",
        "protected_support_roots_blocked",
        "import_rewrite_rollback_not_implemented_in_this_train",
        "non_target_written_files_not_removed_without_per_file_backup",
    ]


def _warnings(non_target: list[str]) -> list[str]:
    """Return stable warning labels for operator review."""
    warnings = [
        "ROLLBACK_RECOVERY_RESTORES_SELECTED_SOURCE_FROM_BACKUP_ONLY",
        "IMPORT_REWRITE_ROLLBACK_IS_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "BACKUP_SNAPSHOT_MUST_REMAIN_UNCHANGED",
    ]
    if non_target:
        warnings.append("NON_TARGET_WRITTEN_FILES_LEFT_FOR_MANUAL_OR_FUTURE_MULTI_FILE_RECOVERY")
    return warnings


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
