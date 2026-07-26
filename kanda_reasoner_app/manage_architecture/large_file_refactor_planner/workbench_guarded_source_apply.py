# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_guarded_source_apply.py
"""Exact-token guarded source apply for Workbench source payloads."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import SCHEMA_VERSION
from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult
from .workbench_source_mutation_primitives import (
    apply_source_mutation_operation,
    build_source_mutation_operations,
)

__all__ = [
    "GUARDED_SOURCE_APPLY_FEATURE_ID",
    "GuardedSourceApplyResult",
    "expected_guarded_apply_token",
    "execute_guarded_source_apply",
]

GUARDED_SOURCE_APPLY_FEATURE_ID = "architecture-review-large-file-refactor-guarded-source-apply-v1"
_APPLY_MANIFEST = "SOURCE_APPLY_EXECUTION_MANIFEST.json"
_ROLLBACK_MANIFEST = "SOURCE_APPLY_ROLLBACK_MANIFEST.json"
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
class GuardedSourceApplyResult:
    """Result for exact-token governed source writes."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash_before: str
    source_content_hash_after: str
    preview_root: str
    payload_manifest_path: str
    rollback_manifest_path: str
    execution_manifest_path: str
    expected_confirmation_token: str
    confirmation_token_present: bool
    confirmation_token_valid: bool
    source_mutation_enabled: bool
    import_rewrite_enabled: bool
    written_files: list[str] = field(default_factory=list)
    generated_files: list[str] = field(default_factory=list)
    restored_after_failure: bool = False
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready result dictionary."""
        return asdict(self)


def expected_guarded_apply_token(payload: SourceApplyPayloadReadinessResult | None) -> str:
    """Return the exact token required for the current source payload."""
    if payload is None:
        return "KANDA-REFACTOR-NO-PAYLOAD"
    seed = "|".join(
        [payload.target_file, payload.source_content_hash, payload.payload_manifest_path]
    )
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12].upper()
    return "KANDA-REFACTOR-" + digest


def execute_guarded_source_apply(
    *,
    source_payload: SourceApplyPayloadReadinessResult | None,
    preflight_backup: WorkbenchPreflightBackupReadinessResult | None,
    active_project_root: str,
    confirmation_token: str,
) -> GuardedSourceApplyResult:
    """Apply source-ready payload files only after all exact-token gates pass."""
    project_root = Path(active_project_root).resolve()
    expected = expected_guarded_apply_token(source_payload)
    blockers = _entry_blockers(source_payload, preflight_backup)
    if source_payload is None:
        return _blocked(project_root, "", "", expected, confirmation_token, blockers)
    preview_root = Path(source_payload.preview_root).resolve()
    target = Path(source_payload.target_file).resolve()
    blockers.extend(_root_blockers(project_root, preview_root, target))
    token_valid = confirmation_token.strip() == expected
    if not token_valid:
        blockers.append("EXACT_CONFIRMATION_TOKEN_MISSING_OR_INVALID")
    current_hash = _sha256_file(target)
    if current_hash != source_payload.source_content_hash:
        blockers.append("STALE_SOURCE_BEFORE_APPLY")
    if preflight_backup is None or not Path(preflight_backup.backup_snapshot_path).is_file():
        blockers.append("BACKUP_SNAPSHOT_MISSING")
    elif _sha256_file(Path(preflight_backup.backup_snapshot_path)) != source_payload.source_content_hash:
        blockers.append("BACKUP_SNAPSHOT_HASH_MISMATCH")
    operations, operation_blockers = build_source_mutation_operations(
        source_payload=source_payload,
        active_project_root=project_root,
    )
    blockers.extend(operation_blockers)
    rollback_manifest = preview_root / _ROLLBACK_MANIFEST
    execution_manifest = preview_root / _APPLY_MANIFEST
    if blockers:
        result = _result(source_payload, expected, confirmation_token, "blocked", blockers, [], [])
        _write_json(execution_manifest, result.to_dict(), preview_root)
        return result
    records = [
        {"destination": Path(operation.destination_path), "hash": operation.payload_hash}
        for operation in operations
    ]
    _write_rollback_manifest(source_payload, preflight_backup, records, rollback_manifest, preview_root)
    written: list[Path] = []
    restored = False
    try:
        for operation in operations:
            apply_source_mutation_operation(
                operation,
                operation_id=f"legacy-{operation.sequence_no:04d}",
            )
            written.append(Path(operation.destination_path))
    except Exception:
        restored = _restore_after_failed_apply(target, preflight_backup, written, records)
        raise
    after_hash = _sha256_file(target)
    result = GuardedSourceApplyResult(
        schema_version=SCHEMA_VERSION,
        feature_id=GUARDED_SOURCE_APPLY_FEATURE_ID,
        status="applied",
        target_file=str(target),
        source_content_hash_before=source_payload.source_content_hash,
        source_content_hash_after=after_hash,
        preview_root=str(preview_root),
        payload_manifest_path=source_payload.payload_manifest_path,
        rollback_manifest_path=str(rollback_manifest),
        execution_manifest_path=str(execution_manifest),
        expected_confirmation_token=expected,
        confirmation_token_present=bool(confirmation_token.strip()),
        confirmation_token_valid=True,
        source_mutation_enabled=True,
        import_rewrite_enabled=False,
        written_files=[str(path) for path in written],
        generated_files=[str(Path(item.destination_path)) for item in operations if Path(item.destination_path) != target],
        restored_after_failure=restored,
        blockers=[],
        warnings=_warnings(),
        checked_rules=_checked_rules(),
    )
    _write_json(execution_manifest, result.to_dict(), preview_root)
    return result


def _entry_blockers(
    source_payload: SourceApplyPayloadReadinessResult | None,
    preflight_backup: WorkbenchPreflightBackupReadinessResult | None,
) -> list[str]:
    """Return blockers for missing prerequisite stages."""
    blockers: list[str] = []
    if source_payload is None or source_payload.status != "source_apply_payload_ready":
        blockers.append("SOURCE_APPLY_PAYLOAD_NOT_READY")
    if preflight_backup is None or preflight_backup.status != "preflight_backup_ready":
        blockers.append("PREFLIGHT_BACKUP_NOT_READY")
    if source_payload is not None and source_payload.import_rewrite_enabled:
        blockers.append("IMPORT_REWRITE_MUST_REMAIN_DISABLED")
    return blockers


def _load_payload_files(
    payload: SourceApplyPayloadReadinessResult,
    target_dir: Path,
    project_root: Path,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Load and validate source payload files before writing."""
    blockers: list[str] = []
    records: list[dict[str, Any]] = []
    target = Path(payload.target_file).resolve()
    seen: set[Path] = set()
    for file_record in payload.files:
        source = Path(file_record.payload_path).resolve()
        destination = Path(file_record.destination_path).resolve()
        if destination in seen:
            blockers.append("DUPLICATE_DESTINATION:" + str(destination))
        seen.add(destination)
        blockers.extend(_destination_blockers(destination, target, target_dir, project_root))
        if destination != target and destination.exists():
            blockers.append("DESTINATION_ALREADY_EXISTS_NOT_TARGET:" + str(destination))
        if not source.is_file():
            blockers.append("SOURCE_PAYLOAD_FILE_MISSING:" + str(source))
            continue
        text = source.read_text(encoding="utf-8", errors="replace")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if digest != file_record.content_hash:
            blockers.append("SOURCE_PAYLOAD_HASH_MISMATCH:" + str(source))
        if "KANDA PREVIEW ARTIFACT" in text:
            blockers.append("PREVIEW_WATERMARK_IN_SOURCE_PAYLOAD:" + str(source))
        try:
            compile(text, str(destination), "exec")
            ast.parse(text)
        except SyntaxError:
            blockers.append("SOURCE_PAYLOAD_SYNTAX_INVALID:" + str(source))
        records.append({"source": source, "destination": destination, "text": text, "hash": digest})
    if not records:
        blockers.append("NO_SOURCE_PAYLOAD_FILES")
    return blockers, records


def _destination_blockers(destination: Path, target: Path, target_dir: Path, project_root: Path) -> list[str]:
    """Return blockers for one source destination path."""
    blockers: list[str] = []
    if not _is_relative_to(destination, project_root):
        blockers.append("DESTINATION_OUTSIDE_PROJECT_ROOT:" + str(destination))
    if destination.parent != target_dir:
        blockers.append("DESTINATION_NOT_IN_TARGET_DIRECTORY:" + str(destination))
    if destination.suffix != ".py":
        blockers.append("DESTINATION_NOT_PYTHON:" + str(destination))
    if _protected_parts(destination):
        blockers.append("DESTINATION_IN_PROTECTED_ROOT:" + str(destination))
    return blockers


def _root_blockers(project_root: Path, preview_root: Path, target: Path) -> list[str]:
    """Return project, preview, and target containment blockers."""
    blockers: list[str] = []
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    if not _is_relative_to(target, project_root):
        blockers.append("TARGET_OUTSIDE_PROJECT_ROOT")
    if _protected_parts(target):
        blockers.append("TARGET_IN_PROTECTED_ROOT")
    return blockers


def _write_rollback_manifest(
    payload: SourceApplyPayloadReadinessResult,
    preflight: WorkbenchPreflightBackupReadinessResult | None,
    records: list[dict[str, Any]],
    manifest: Path,
    preview_root: Path,
) -> None:
    """Write rollback metadata before mutating source."""
    data = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": GUARDED_SOURCE_APPLY_FEATURE_ID,
        "target_file": payload.target_file,
        "source_content_hash_before": payload.source_content_hash,
        "backup_snapshot_path": preflight.backup_snapshot_path if preflight else "",
        "generated_files": [str(item["destination"]) for item in records if str(item["destination"]) != payload.target_file],
        "written_files": [str(item["destination"]) for item in records],
        "import_rewrite_enabled": False,
    }
    _write_json(manifest, data, preview_root)


def _restore_after_failed_apply(
    target: Path,
    preflight: WorkbenchPreflightBackupReadinessResult | None,
    written: list[Path],
    records: list[dict[str, Any]],
) -> bool:
    """Best-effort recovery if a guarded apply raises mid-write."""
    try:
        if preflight and Path(preflight.backup_snapshot_path).is_file():
            target.write_bytes(Path(preflight.backup_snapshot_path).read_bytes())
        generated = {item["destination"] for item in records if item["destination"] != target}
        for path in generated:
            if path in written and path.exists():
                path.unlink()
        return True
    except OSError:
        return False


def _result(
    payload: SourceApplyPayloadReadinessResult,
    expected: str,
    confirmation: str,
    status: str,
    blockers: list[str],
    written: list[str],
    generated: list[str],
) -> GuardedSourceApplyResult:
    """Build a blocked or non-mutating result."""
    return GuardedSourceApplyResult(
        schema_version=SCHEMA_VERSION,
        feature_id=GUARDED_SOURCE_APPLY_FEATURE_ID,
        status=status,
        target_file=payload.target_file,
        source_content_hash_before=payload.source_content_hash,
        source_content_hash_after="",
        preview_root=payload.preview_root,
        payload_manifest_path=payload.payload_manifest_path,
        rollback_manifest_path=str(Path(payload.preview_root) / _ROLLBACK_MANIFEST),
        execution_manifest_path=str(Path(payload.preview_root) / _APPLY_MANIFEST),
        expected_confirmation_token=expected,
        confirmation_token_present=bool(confirmation.strip()),
        confirmation_token_valid=confirmation.strip() == expected,
        source_mutation_enabled=False,
        import_rewrite_enabled=False,
        written_files=written,
        generated_files=generated,
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
        checked_rules=_checked_rules(),
    )


def _blocked(
    project_root: Path,
    target: str,
    preview_root: str,
    expected: str,
    confirmation: str,
    blockers: list[str],
) -> GuardedSourceApplyResult:
    """Return a result when payload context is unavailable."""
    root = preview_runs_root(project_root)
    preview = str(preview_root or root)
    return GuardedSourceApplyResult(
        schema_version=SCHEMA_VERSION,
        feature_id=GUARDED_SOURCE_APPLY_FEATURE_ID,
        status="blocked",
        target_file=target,
        source_content_hash_before="",
        source_content_hash_after="",
        preview_root=preview,
        payload_manifest_path="",
        rollback_manifest_path=str(Path(preview) / _ROLLBACK_MANIFEST),
        execution_manifest_path=str(Path(preview) / _APPLY_MANIFEST),
        expected_confirmation_token=expected,
        confirmation_token_present=bool(confirmation.strip()),
        confirmation_token_valid=False,
        source_mutation_enabled=False,
        import_rewrite_enabled=False,
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
        checked_rules=_checked_rules(),
    )


def _write_json(path: Path, payload: dict[str, Any], allowed_root: Path) -> None:
    """Write JSON evidence only inside the allowed preview root."""
    if not _is_relative_to(path, allowed_root):
        raise RuntimeError("Evidence path outside preview root: " + str(path))
    if _protected_parts(path):
        raise RuntimeError("Evidence path inside protected root: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _checked_rules() -> list[str]:
    """Return stable checked-rule labels."""
    return [
        "source_payload_ready_required",
        "preflight_backup_ready_required",
        "source_hash_rechecked_before_apply",
        "exact_confirmation_token_required",
        "backup_snapshot_verified_before_write",
        "payload_hashes_verified_before_write",
        "helper_destination_collision_blocks_apply",
        "writes_limited_to_target_directory",
        "import_rewrite_disabled",
        "rollback_manifest_written_before_mutation",
    ]


def _warnings() -> list[str]:
    """Return stable warning labels."""
    return [
        "SOURCE_APPLY_MUTATES_SELECTED_PROJECT_SOURCE_AFTER_EXACT_TOKEN",
        "IMPORT_REWRITE_REMAINS_DISABLED",
        "BEHAVIOR_EQUIVALENCE_NOT_CLAIMED_UNLESS_POST_APPLY_TESTS_PASS",
    ]


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for a file, or empty string if unavailable."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _protected_parts(path: Path) -> list[str]:
    """Return protected path parts found in a resolved path."""
    return [part for part in path.resolve().parts if part in _PROTECTED_PARTS]


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return True if path is inside root after resolution."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
