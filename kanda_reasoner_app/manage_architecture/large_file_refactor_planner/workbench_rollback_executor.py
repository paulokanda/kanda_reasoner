# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_rollback_executor.py
"""Exact-token rollback executor for Large File Refactor Workbench applies."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import SCHEMA_VERSION
from .workbench_guarded_source_apply import GuardedSourceApplyResult
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult

__all__ = [
    "ROLLBACK_EXECUTOR_FEATURE_ID",
    "WorkbenchRollbackResult",
    "expected_workbench_rollback_token",
    "execute_workbench_rollback",
]

ROLLBACK_EXECUTOR_FEATURE_ID = "architecture-review-large-file-refactor-rollback-visibility-v1"
_ROLLBACK_REPORT = "SOURCE_APPLY_ROLLBACK_EXECUTION.json"
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class WorkbenchRollbackResult:
    """Result for exact-token rollback of one guarded source apply."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    preview_root: str
    rollback_manifest_path: str
    rollback_report_path: str
    expected_confirmation_token: str
    confirmation_token_present: bool
    confirmation_token_valid: bool
    source_content_hash_before_apply: str
    source_content_hash_after_apply: str
    source_content_hash_before_rollback: str
    source_content_hash_after_rollback: str
    backup_snapshot_path: str
    backup_snapshot_verified: bool
    selected_source_restored: bool
    generated_files_removed: bool
    source_mutation_enabled: bool
    import_rewrite_enabled: bool
    removed_files: list[str] = field(default_factory=list)
    retained_files: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready rollback dictionary."""
        return asdict(self)


def expected_workbench_rollback_token(apply_result: GuardedSourceApplyResult | None) -> str:
    """Return the exact token required to rollback the current apply."""
    if apply_result is None or apply_result.status != "applied":
        return "KANDA-ROLLBACK-NO-APPLY"
    seed = "|".join(
        [
            apply_result.target_file,
            apply_result.source_content_hash_before,
            apply_result.source_content_hash_after,
            apply_result.rollback_manifest_path,
        ]
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12].upper()
    return "KANDA-ROLLBACK-" + digest


def execute_workbench_rollback(
    *,
    apply_result: GuardedSourceApplyResult | None,
    source_payload: SourceApplyPayloadReadinessResult | None,
    active_project_root: str,
    confirmation_token: str,
) -> WorkbenchRollbackResult:
    """Restore the selected source from backup and remove unchanged generated helpers."""
    project_root = Path(active_project_root).resolve()
    expected = expected_workbench_rollback_token(apply_result)
    preview_root = _preview_root(project_root, apply_result)
    report_path = preview_root / _ROLLBACK_REPORT
    blockers = _entry_blockers(apply_result, source_payload)
    token_valid = confirmation_token.strip() == expected
    if not token_valid:
        blockers.append("EXACT_ROLLBACK_TOKEN_MISSING_OR_INVALID")
    target = Path(apply_result.target_file).resolve() if apply_result else Path("").resolve()
    rollback_manifest = Path(apply_result.rollback_manifest_path).resolve() if apply_result else preview_root / "SOURCE_APPLY_ROLLBACK_MANIFEST.json"
    manifest = _read_json(rollback_manifest)
    backup = Path(str(manifest.get("backup_snapshot_path", ""))).resolve()
    blockers.extend(_root_blockers(project_root, preview_root, target, rollback_manifest, backup))
    before_hash = str(manifest.get("source_content_hash_before", ""))
    after_hash = apply_result.source_content_hash_after if apply_result else ""
    current_hash = _sha256_file(target)
    if not target.is_file():
        blockers.append("TARGET_FILE_MISSING")
    elif after_hash and current_hash != after_hash:
        blockers.append("TARGET_HASH_CHANGED_AFTER_APPLY")
    backup_verified = backup.is_file() and before_hash and _sha256_file(backup) == before_hash
    if not backup_verified:
        blockers.append("BACKUP_SNAPSHOT_MISSING_OR_HASH_MISMATCH")
    generated, retained, generated_blockers = _generated_file_plan(apply_result, source_payload, project_root, target)
    blockers.extend(generated_blockers)
    if blockers:
        result = _result(
            apply_result=apply_result,
            project_root=project_root,
            preview_root=preview_root,
            rollback_manifest=rollback_manifest,
            report_path=report_path,
            expected=expected,
            confirmation=confirmation_token,
            status="blocked",
            before_hash=before_hash,
            after_hash=after_hash,
            current_hash=current_hash,
            final_hash="",
            backup=str(backup) if str(backup) != "." else "",
            backup_verified=backup_verified,
            restored=False,
            removed=[],
            retained=retained,
            blockers=blockers,
        )
        _write_report(result)
        return result
    removed: list[str] = []
    target.write_bytes(backup.read_bytes())
    for path in generated:
        if path.exists():
            path.unlink()
            removed.append(str(path))
    final_hash = _sha256_file(target)
    restored = final_hash == before_hash
    final_blockers = [] if restored else ["TARGET_HASH_NOT_RESTORED_TO_BEFORE_APPLY"]
    result = _result(
        apply_result=apply_result,
        project_root=project_root,
        preview_root=preview_root,
        rollback_manifest=rollback_manifest,
        report_path=report_path,
        expected=expected,
        confirmation=confirmation_token,
        status="rollback_completed" if not final_blockers else "blocked",
        before_hash=before_hash,
        after_hash=after_hash,
        current_hash=current_hash,
        final_hash=final_hash,
        backup=str(backup),
        backup_verified=backup_verified,
        restored=restored,
        removed=removed,
        retained=retained,
        blockers=final_blockers,
    )
    _write_report(result)
    return result


def _entry_blockers(
    apply_result: GuardedSourceApplyResult | None,
    payload: SourceApplyPayloadReadinessResult | None,
) -> list[str]:
    """Return blockers for missing rollback prerequisites."""
    blockers: list[str] = []
    if apply_result is None or apply_result.status != "applied":
        blockers.append("GUARDED_SOURCE_APPLY_NOT_SUCCESSFUL")
    if payload is None or payload.status != "source_apply_payload_ready":
        blockers.append("SOURCE_APPLY_PAYLOAD_NOT_READY")
    if apply_result is not None and apply_result.import_rewrite_enabled:
        blockers.append("IMPORT_REWRITE_ROLLBACK_NOT_SUPPORTED")
    return blockers


def _generated_file_plan(
    apply_result: GuardedSourceApplyResult | None,
    payload: SourceApplyPayloadReadinessResult | None,
    project_root: Path,
    target: Path,
) -> tuple[list[Path], list[str], list[str]]:
    """Return generated files safe to remove, retained files, and blockers."""
    blockers: list[str] = []
    retained: list[str] = []
    generated: list[Path] = []
    if apply_result is None:
        return generated, retained, blockers
    expected_hashes = _payload_hashes_by_destination(payload)
    for item in apply_result.generated_files:
        path = Path(item).resolve()
        blockers.extend(_source_path_blockers(path, project_root, "GENERATED_FILE"))
        if path == target:
            blockers.append("GENERATED_FILE_MATCHES_TARGET")
        expected_hash = expected_hashes.get(str(path))
        if path.exists():
            current = _sha256_file(path)
            if expected_hash and current != expected_hash:
                blockers.append("GENERATED_FILE_HASH_CHANGED_NOT_REMOVED:" + str(path))
                retained.append(str(path))
            else:
                generated.append(path)
        else:
            retained.append(str(path) + " (already absent)")
    return generated, retained, blockers


def _payload_hashes_by_destination(payload: SourceApplyPayloadReadinessResult | None) -> dict[str, str]:
    """Return destination-path to payload-hash mapping."""
    if payload is None:
        return {}
    return {str(Path(item.destination_path).resolve()): item.content_hash for item in payload.files}


def _root_blockers(
    project_root: Path,
    preview_root: Path,
    target: Path,
    rollback_manifest: Path,
    backup: Path,
) -> list[str]:
    """Return containment and shielding blockers."""
    blockers: list[str] = []
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    blockers.extend(_source_path_blockers(target, project_root, "TARGET"))
    blockers.extend(_artifact_blockers(rollback_manifest, preview_root, project_root, "ROLLBACK_MANIFEST"))
    blockers.extend(_artifact_blockers(backup, preview_root, project_root, "BACKUP_SNAPSHOT"))
    return blockers


def _source_path_blockers(path: Path, project_root: Path, label: str) -> list[str]:
    """Return blockers for one source path."""
    blockers: list[str] = []
    if not _is_relative_to(path, project_root):
        blockers.append(label + "_OUTSIDE_PROJECT_ROOT")
    if _protected_parts(path):
        blockers.append(label + "_IN_PROTECTED_ROOT")
    if path.suffix != ".py":
        blockers.append(label + "_NOT_PYTHON")
    return blockers


def _artifact_blockers(path: Path, preview_root: Path, project_root: Path, label: str) -> list[str]:
    """Return blockers for one daily-work rollback artifact."""
    blockers: list[str] = []
    if not _is_relative_to(path, preview_root):
        blockers.append(label + "_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    if _protected_parts(path):
        blockers.append(label + "_IN_PROTECTED_ROOT")
    return blockers


def _result(
    *,
    apply_result: GuardedSourceApplyResult | None,
    project_root: Path,
    preview_root: Path,
    rollback_manifest: Path,
    report_path: Path,
    expected: str,
    confirmation: str,
    status: str,
    before_hash: str,
    after_hash: str,
    current_hash: str,
    final_hash: str,
    backup: str,
    backup_verified: bool,
    restored: bool,
    removed: list[str],
    retained: list[str],
    blockers: list[str],
) -> WorkbenchRollbackResult:
    """Build one rollback result."""
    target = apply_result.target_file if apply_result else ""
    return WorkbenchRollbackResult(
        schema_version=SCHEMA_VERSION,
        feature_id=ROLLBACK_EXECUTOR_FEATURE_ID,
        status=status,
        target_file=target,
        preview_root=str(preview_root),
        rollback_manifest_path=str(rollback_manifest),
        rollback_report_path=str(report_path),
        expected_confirmation_token=expected,
        confirmation_token_present=bool(confirmation.strip()),
        confirmation_token_valid=confirmation.strip() == expected,
        source_content_hash_before_apply=before_hash,
        source_content_hash_after_apply=after_hash,
        source_content_hash_before_rollback=current_hash,
        source_content_hash_after_rollback=final_hash,
        backup_snapshot_path=backup,
        backup_snapshot_verified=backup_verified,
        selected_source_restored=restored,
        generated_files_removed=bool(removed) and not blockers,
        source_mutation_enabled=status == "rollback_completed",
        import_rewrite_enabled=False,
        removed_files=sorted(removed),
        retained_files=sorted(retained),
        blockers=sorted(set(blockers)),
        warnings=_warnings(retained),
        checked_rules=_checked_rules(),
    )


def _preview_root(project_root: Path, apply_result: GuardedSourceApplyResult | None) -> Path:
    """Return Preview root from apply result or selected project support."""
    if apply_result and apply_result.preview_root:
        return Path(apply_result.preview_root).resolve()
    return preview_runs_root(project_root)


def _read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object or return empty mapping."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _write_report(result: WorkbenchRollbackResult) -> None:
    """Write rollback report under preview root only."""
    path = Path(result.rollback_report_path).resolve()
    root = Path(result.preview_root).resolve()
    if not _is_relative_to(path, root):
        raise RuntimeError("Rollback report outside preview root: " + str(path))
    if _protected_parts(path):
        raise RuntimeError("Rollback report inside protected root: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checked_rules() -> list[str]:
    """Return stable rollback rule labels."""
    return [
        "exact_rollback_token_required",
        "guarded_apply_result_required",
        "source_payload_required_for_generated_file_hashes",
        "rollback_manifest_required",
        "backup_snapshot_hash_verified",
        "current_target_hash_matches_applied_hash_before_rollback",
        "selected_source_restored_to_before_apply_hash",
        "generated_helpers_removed_only_when_hash_matches_payload",
        "import_rewrite_rollback_disabled",
        "shielding_blocks_protected_roots",
    ]


def _warnings(retained: list[str]) -> list[str]:
    """Return stable rollback warnings."""
    warnings = [
        "ROLLBACK_MUTATES_SELECTED_PROJECT_SOURCE_AFTER_EXACT_TOKEN",
        "IMPORT_REWRITE_ROLLBACK_NOT_IMPLEMENTED",
        "BEHAVIOR_EQUIVALENCE_NOT_CLAIMED",
    ]
    if retained:
        warnings.append("SOME_GENERATED_FILES_RETAINED_FOR_MANUAL_REVIEW")
    return warnings


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for a file or empty string."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _protected_parts(path: Path) -> list[str]:
    """Return protected path parts in path."""
    return [part for part in path.resolve().parts if part in _PROTECTED_PARTS]


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return True when path resolves inside root."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
