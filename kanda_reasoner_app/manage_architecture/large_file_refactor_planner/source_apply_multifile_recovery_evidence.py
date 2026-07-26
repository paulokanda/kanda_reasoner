# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_multifile_recovery_evidence.py
"""Multi-file recovery evidence for guarded large-file source application."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import FEATURE_ID, SCHEMA_VERSION

__all__ = [
    "SOURCE_APPLY_MULTIFILE_RECOVERY_EVIDENCE_TOKEN",
    "SourceApplyMultiFileRecoveryEvidenceResult",
    "build_source_apply_multifile_recovery_evidence",
    "write_source_apply_multifile_recovery_evidence_manifest",
]

SOURCE_APPLY_MULTIFILE_RECOVERY_EVIDENCE_TOKEN = "CONFIRM_REVIEW_MULTIFILE_RECOVERY_EVIDENCE"
_MULTI_FILE_EVIDENCE_NAME = "SOURCE_APPLY_MULTIFILE_RECOVERY_EVIDENCE.json"


@dataclass(frozen=True)
class SourceApplyMultiFileRecoveryEvidenceResult:
    """Evidence describing whether multi-file rollback can be safely automated."""

    schema_version: str
    feature_id: str
    status: str
    preview_root: str
    rollback_manifest_path: str
    multifile_recovery_manifest_path: str
    target_file: str
    backup_snapshot_path: str
    confirmation_token_required: str
    recovery_evidence_confirmation_present: bool
    recovery_evidence_confirmation_valid: bool
    selected_source_recovered: bool = False
    backup_snapshot_verified: bool = False
    loose_preview_artifacts_used_as_source_of_truth: bool = False
    import_rewrite_rollback_enabled: bool = False
    non_target_removal_enabled: bool = False
    automated_multifile_recovery_enabled: bool = False
    per_file_backup_evidence_required: bool = True
    per_file_backup_evidence_present: bool = False
    non_target_written_files: list[str] = field(default_factory=list)
    files_requiring_manual_review: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready multi-file recovery evidence dictionary."""
        return asdict(self)


def build_source_apply_multifile_recovery_evidence(
    rollback_manifest_path: str,
    *,
    active_project_root: str,
    evidence_confirmation: str = "",
) -> SourceApplyMultiFileRecoveryEvidenceResult:
    """Build non-mutating multi-file recovery evidence from rollback output."""
    project_root = Path(active_project_root).resolve()
    rollback_manifest = Path(rollback_manifest_path).resolve()
    rollback = _read_json_file(rollback_manifest)
    preview_root = Path(str(rollback.get("preview_root", rollback_manifest.parent))).resolve()
    target = Path(str(rollback.get("target_file", ""))).resolve()
    backup = Path(str(rollback.get("backup_snapshot_path", ""))).resolve()
    non_target = [str(item) for item in rollback.get("non_target_written_files", []) if str(item)]
    token_valid = evidence_confirmation.strip() == SOURCE_APPLY_MULTIFILE_RECOVERY_EVIDENCE_TOKEN
    blockers = _build_blockers(project_root, preview_root, rollback_manifest, rollback, target, backup, non_target, token_valid)
    per_file_present = _per_file_backup_evidence_present(rollback, non_target)
    if non_target and not per_file_present:
        blockers.append("PER_FILE_BACKUP_EVIDENCE_MISSING_FOR_NON_TARGET_FILES")
    status = "multifile_recovery_evidence_ready" if not blockers else "blocked"
    return SourceApplyMultiFileRecoveryEvidenceResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        preview_root=str(preview_root),
        rollback_manifest_path=str(rollback_manifest),
        multifile_recovery_manifest_path=str(preview_root / _MULTI_FILE_EVIDENCE_NAME),
        target_file=str(target),
        backup_snapshot_path=str(backup),
        confirmation_token_required=SOURCE_APPLY_MULTIFILE_RECOVERY_EVIDENCE_TOKEN,
        recovery_evidence_confirmation_present=bool(evidence_confirmation.strip()),
        recovery_evidence_confirmation_valid=token_valid,
        selected_source_recovered=rollback.get("status") == "source_apply_rollback_recovered",
        backup_snapshot_verified=bool(rollback.get("backup_snapshot_unchanged_after_restore")),
        loose_preview_artifacts_used_as_source_of_truth=False,
        import_rewrite_rollback_enabled=False,
        non_target_removal_enabled=False,
        automated_multifile_recovery_enabled=False,
        per_file_backup_evidence_required=True,
        per_file_backup_evidence_present=per_file_present,
        non_target_written_files=sorted(non_target),
        files_requiring_manual_review=sorted(non_target if not per_file_present else []),
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=_warnings(non_target, per_file_present),
    )


def write_source_apply_multifile_recovery_evidence_manifest(result: SourceApplyMultiFileRecoveryEvidenceResult) -> Path:
    """Write multi-file recovery evidence under the governed preview root only."""
    preview_root = Path(result.preview_root).resolve()
    manifest = Path(result.multifile_recovery_manifest_path).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Multi-file recovery evidence manifest is outside preview root.")
    _raise_if_protected(manifest, "multi-file recovery evidence manifest")
    payload = result.to_dict()
    payload["non_target_removal_enabled"] = False
    payload["automated_multifile_recovery_enabled"] = False
    payload["import_rewrite_rollback_enabled"] = False
    payload["loose_preview_artifacts_used_as_source_of_truth"] = False
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("non_target_removal_enabled") is not False:
        raise RuntimeError("This train must not enable non-target file removal.")
    if saved.get("automated_multifile_recovery_enabled") is not False:
        raise RuntimeError("This train must not enable automated multi-file recovery.")
    if saved.get("loose_preview_artifacts_used_as_source_of_truth") is not False:
        raise RuntimeError("Loose preview artifacts must not be used as source of truth.")
    return manifest


def _build_blockers(
    project_root: Path,
    preview_root: Path,
    rollback_manifest: Path,
    rollback: dict[str, object],
    target: Path,
    backup: Path,
    non_target: list[str],
    token_valid: bool,
) -> list[str]:
    """Return blockers that prevent multi-file recovery evidence readiness."""
    blockers: list[str] = []
    if not token_valid:
        blockers.append("MULTIFILE_RECOVERY_EVIDENCE_TOKEN_MISSING_OR_INVALID")
    if not rollback_manifest.is_file():
        blockers.append("ROLLBACK_MANIFEST_MISSING")
    if rollback.get("status") != "source_apply_rollback_recovered":
        blockers.append("ROLLBACK_NOT_RECORDED_AS_RECOVERED")
    if bool(rollback.get("import_rewrite_rollback_enabled")):
        blockers.append("IMPORT_REWRITE_ROLLBACK_ENABLED_UNSUPPORTED")
    if bool(rollback.get("loose_preview_artifacts_used_as_source_of_truth")):
        blockers.append("LOOSE_PREVIEW_ARTIFACTS_USED_AS_SOURCE_OF_TRUTH")
    if not bool(rollback.get("backup_snapshot_unchanged_after_restore")):
        blockers.append("BACKUP_SNAPSHOT_NOT_VERIFIED_UNCHANGED")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, rollback_manifest, "ROLLBACK_MANIFEST"))
    blockers.extend(_artifact_path_blockers(project_root, preview_root, backup, "BACKUP_SNAPSHOT"))
    blockers.extend(_target_path_blockers(project_root, target, "TARGET"))
    for item in non_target:
        blockers.extend(_target_path_blockers(project_root, Path(item).resolve(), "NON_TARGET_WRITTEN_FILE"))
    return blockers


def _artifact_path_blockers(project_root: Path, preview_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for support artifacts."""
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
    """Return blockers for protected support/reference roots."""
    lowered = {part.lower() for part in path.parts}
    blockers: list[str] = []
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append(label + "_INSIDE_PROTECTED_" + forbidden.upper())
    if ".project_reference" in lowered or "_project_reference" in lowered:
        blockers.append(label + "_INSIDE_PROJECT_REFERENCE")
    return blockers


def _per_file_backup_evidence_present(rollback: dict[str, object], non_target: list[str]) -> bool:
    """Return whether all non-target written files have governed per-file backup evidence."""
    evidence = rollback.get("per_file_backup_evidence", {})
    if not non_target:
        return True
    if not isinstance(evidence, dict):
        return False
    for item in non_target:
        value = evidence.get(item)
        if not isinstance(value, dict) or not value.get("backup_snapshot_path"):
            return False
    return True


def _checked_rules() -> list[str]:
    """Return stable checked rules for evidence formatting and freeze intake."""
    return [
        "rollback_manifest_under_daily_work_preview_root",
        "selected_source_rollback_evidence_required",
        "source_derived_backup_snapshot_required",
        "loose_preview_artifacts_not_source_of_truth",
        "project_reference_roots_blocked",
        "protected_support_roots_blocked",
        "non_target_removal_requires_per_file_backup_evidence",
        "no_source_mutation_in_multifile_evidence_train",
        "import_rewrite_rollback_disabled",
    ]


def _warnings(non_target: list[str], per_file_present: bool) -> list[str]:
    """Return human-readable recovery warnings."""
    warnings: list[str] = []
    if non_target and not per_file_present:
        warnings.append("NON_TARGET_WRITTEN_FILES_REQUIRE_MANUAL_REVIEW")
        warnings.append("PER_FILE_BACKUP_EVIDENCE_REQUIRED_BEFORE_AUTOMATED_REMOVAL")
    return warnings


def _read_json_file(path: Path) -> dict[str, object]:
    """Read a JSON object from path, returning an empty dict on invalid input."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return True when path is within root."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _raise_if_protected(path: Path, label: str) -> None:
    """Raise when path is inside protected support/reference roots."""
    blockers = _protected_root_blockers(path, label.upper().replace(" ", "_"))
    if blockers:
        raise RuntimeError("Protected path blocked: " + ", ".join(blockers))
