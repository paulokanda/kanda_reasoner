# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/guarded_source_apply_executor.py
"""Guarded source apply executor for reviewed large-file refactor payloads."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import zipfile

from kanda_reasoner_app.project_fire_shield import (
    FireShieldPhase,
    assert_fire_shield_payload_bytes_allowed,
    assert_fire_shield_write_allowed,
    build_current_fire_shield_context,
    verify_tool_snapshot_unchanged,
)

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import FEATURE_ID, SCHEMA_VERSION
from .source_apply_preflight_backup_contract import SourceApplyPreflightBackupContractResult

__all__ = [
    "GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN",
    "GuardedSourceApplyExecutionResult",
    "build_guarded_source_apply_execution",
    "write_guarded_source_apply_execution_manifest",
]

GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN = "CONFIRM_EXECUTE_GUARDED_SOURCE_APPLY"
_EXECUTION_MANIFEST_NAME = "GUARDED_SOURCE_APPLY_EXECUTION.json"
_PAYLOAD_MANIFEST_NAME = "PROJECT_PATCH_PAYLOAD_MANIFEST.json"
_META_FILES = {
    _PAYLOAD_MANIFEST_NAME,
    "PREVIEW_MANIFEST.json",
    "NO_SOURCE_WRITE_PROOF.txt",
    "IMPORT_MIGRATION_PREVIEW.json",
    "PATCH_ZIP_CREATION_GATE.json",
    "PAYLOAD_APPLY_GATE.json",
    "IMPORT_REWRITE_APPLICATION_GATE.json",
    "HUMAN_CONFIRMED_IMPORT_REWRITE_CONTRACT.json",
    "HUMAN_CONFIRMED_APPLY_CONTRACT.json",
    "FINAL_GUARDED_SOURCE_APPLY_PLAN.json",
    "SOURCE_APPLY_DRY_RUN_VALIDATION.json",
    "SOURCE_APPLY_PREFLIGHT_BACKUP_CONTRACT.json",
}


@dataclass(frozen=True)
class GuardedSourceApplyExecutionResult:
    """Execution contract for exact-token guarded project source mutation."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash_before: str
    source_content_hash_after: str
    preview_root: str
    payload_zip_path: str
    dry_run_manifest_path: str
    preflight_manifest_path: str
    backup_snapshot_path: str
    execution_manifest_path: str
    confirmation_token_required: str
    execution_confirmation_present: bool
    execution_confirmation_valid: bool
    apply_enabled: bool = False
    rewrite_enabled: bool = False
    source_mutation_enabled: bool = False
    backup_snapshot_verified: bool = False
    source_hash_verified_before_write: bool = False
    payload_manifest_verified: bool = False
    planned_write_targets: list[str] = field(default_factory=list)
    written_files: list[str] = field(default_factory=list)
    written_file_count: int = 0
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready guarded source apply execution dictionary."""
        return asdict(self)


def build_guarded_source_apply_execution(
    preflight: SourceApplyPreflightBackupContractResult,
    *,
    active_project_root: str,
    execution_confirmation: str = "",
) -> GuardedSourceApplyExecutionResult:
    """Build guarded source-apply readiness without writing selected source."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(preflight.preview_root).resolve()
    target = Path(preflight.target_file).resolve()
    dry_run_manifest = Path(preflight.dry_run_manifest_path).resolve()
    preflight_manifest = Path(preflight.preflight_manifest_path).resolve()
    backup_snapshot = Path(preflight.backup_snapshot_path).resolve()
    execution_manifest = preview_root / _EXECUTION_MANIFEST_NAME
    dry_run_data = _read_json_file(dry_run_manifest)
    payload_zip = Path(str(dry_run_data.get("payload_zip_path", ""))).resolve() if dry_run_data else Path("").resolve()
    payload_data = _read_payload_manifest(payload_zip)
    targets = _planned_payload_targets(payload_zip, payload_data)
    token_valid = execution_confirmation.strip() == GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN
    blockers = _execution_blockers(
        preflight,
        project_root,
        preview_root,
        target,
        dry_run_manifest,
        preflight_manifest,
        backup_snapshot,
        payload_zip,
        payload_data,
        targets,
        token_valid,
    )
    status = "guarded_source_apply_ready" if not blockers else "blocked"
    source_after = preflight.source_content_hash if status == "guarded_source_apply_ready" else ""
    warnings = [
        "GUARDED_SOURCE_APPLY_MUTATES_SELECTED_PROJECT_SOURCE_ONLY_WHEN_READY",
        "BACKUP_SNAPSHOT_MUST_BE_VERIFIED_BEFORE_WRITE",
        "LOOSE_PREVIEW_ARTIFACTS_ARE_NOT_USED_AS_SOURCE_OF_TRUTH",
        "IMPORT_REWRITE_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN",
        "PROTECTED_SUPPORT_ROOTS_BLOCKED",
    ]
    return GuardedSourceApplyExecutionResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash_before=preflight.source_content_hash,
        source_content_hash_after=source_after,
        preview_root=str(preview_root),
        payload_zip_path=str(payload_zip),
        dry_run_manifest_path=str(dry_run_manifest),
        preflight_manifest_path=str(preflight_manifest),
        backup_snapshot_path=str(backup_snapshot),
        execution_manifest_path=str(execution_manifest),
        confirmation_token_required=GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
        execution_confirmation_present=bool(execution_confirmation.strip()),
        execution_confirmation_valid=token_valid,
        apply_enabled=status == "guarded_source_apply_ready",
        rewrite_enabled=False,
        source_mutation_enabled=status == "guarded_source_apply_ready",
        backup_snapshot_verified="BACKUP_SNAPSHOT_HASH_MISMATCH" not in blockers and "BACKUP_SNAPSHOT_MISSING" not in blockers,
        source_hash_verified_before_write="SELECTED_SOURCE_HASH_CHANGED" not in blockers and "TARGET_FILE_MISSING" not in blockers,
        payload_manifest_verified="PAYLOAD_MANIFEST_UNREADABLE_OR_MISSING" not in blockers,
        planned_write_targets=targets,
        written_files=[],
        written_file_count=0,
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_guarded_source_apply_execution_manifest(result: GuardedSourceApplyExecutionResult) -> Path:
    """Execute guarded source writes if ready, then write execution evidence."""
    manifest = Path(result.execution_manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    target = Path(result.target_file).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Guarded source apply manifest path is outside preview root.")
    _raise_if_protected(manifest, "execution manifest")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    payload = result.to_dict()
    if result.status == "guarded_source_apply_ready":
        written = _apply_payload_files(result, target.parent)
        payload["written_files"] = written
        payload["written_file_count"] = len(written)
        payload["source_content_hash_after"] = hashlib.sha256(target.read_bytes()).hexdigest()
    else:
        payload["written_files"] = []
        payload["written_file_count"] = 0
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if result.status == "guarded_source_apply_ready" and saved.get("written_file_count", 0) <= 0:
        raise RuntimeError("Guarded source apply ready state did not record written files.")
    if saved.get("rewrite_enabled") is not False:
        raise RuntimeError("Guarded source apply executor must not rewrite imports in this train.")
    return manifest


def _execution_blockers(
    preflight: SourceApplyPreflightBackupContractResult,
    project_root: Path,
    preview_root: Path,
    target: Path,
    dry_run_manifest: Path,
    preflight_manifest: Path,
    backup_snapshot: Path,
    payload_zip: Path,
    payload_data: dict[str, object] | None,
    targets: list[str],
    token_valid: bool,
) -> list[str]:
    """Return blockers that prevent guarded source application."""
    blockers: list[str] = list(preflight.blockers)
    if preflight.status != "source_apply_preflight_backup_ready":
        blockers.append("SOURCE_APPLY_PREFLIGHT_BACKUP_NOT_READY")
    if token_valid is not True:
        blockers.append("GUARDED_SOURCE_APPLY_EXECUTION_TOKEN_MISSING_OR_INVALID")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    for path, label in (
        (dry_run_manifest, "DRY_RUN_MANIFEST"),
        (preflight_manifest, "PREFLIGHT_MANIFEST"),
        (backup_snapshot, "BACKUP_SNAPSHOT"),
        (payload_zip, "PAYLOAD_ZIP"),
    ):
        blockers.extend(_path_blockers(project_root, preview_root, path, label, allow_source=False))
    if not dry_run_manifest.is_file():
        blockers.append("DRY_RUN_MANIFEST_MISSING")
    if not preflight_manifest.is_file():
        blockers.append("PREFLIGHT_MANIFEST_MISSING")
    if not payload_zip.is_file():
        blockers.append("PAYLOAD_ZIP_MISSING")
    if not backup_snapshot.is_file():
        blockers.append("BACKUP_SNAPSHOT_MISSING")
    elif hashlib.sha256(backup_snapshot.read_bytes()).hexdigest() != preflight.source_content_hash:
        blockers.append("BACKUP_SNAPSHOT_HASH_MISMATCH")
    if not target.is_file():
        blockers.append("TARGET_FILE_MISSING")
    elif hashlib.sha256(target.read_bytes()).hexdigest() != preflight.source_content_hash:
        blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    blockers.extend(_payload_manifest_blockers(payload_data, preflight.source_content_hash))
    if not targets:
        blockers.append("NO_SAFE_PAYLOAD_WRITE_TARGETS")
    for relative in targets:
        destination = (target.parent / relative).resolve()
        blockers.extend(_path_blockers(project_root, preview_root, destination, "DESTINATION", allow_source=True))
        if not _is_relative_to(destination, project_root):
            blockers.append("DESTINATION_OUTSIDE_PROJECT_SOURCE")
    return blockers


def _apply_payload_files(result: GuardedSourceApplyExecutionResult, destination_root: Path) -> list[str]:
    """Copy safe payload entries from the reviewed payload ZIP into project source."""
    fire_shield = build_current_fire_shield_context(
        phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
        operation_id="guarded-source-apply-" + hashlib.sha256(
            result.payload_zip_path.encode("utf-8")
        ).hexdigest()[:24],
    )
    target = Path(result.target_file).resolve()
    if hashlib.sha256(target.read_bytes()).hexdigest() != result.source_content_hash_before:
        raise RuntimeError("Selected source hash changed immediately before guarded write.")
    written: list[str] = []
    with zipfile.ZipFile(result.payload_zip_path, "r") as archive:
        for relative in result.planned_write_targets:
            destination = (destination_root / relative).resolve()
            data = archive.read(relative)
            assert_fire_shield_write_allowed(
                fire_shield,
                destination,
                operation="REPLACE" if destination.exists() else "CREATE",
            )
            assert_fire_shield_payload_bytes_allowed(
                fire_shield,
                data,
                relative,
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            written.append(str(destination))
    verify_tool_snapshot_unchanged(fire_shield)
    return sorted(written)


def _payload_manifest_blockers(payload: dict[str, object] | None, source_hash: str) -> list[str]:
    """Return blockers from governed payload manifest safety fields."""
    if payload is None:
        return ["PAYLOAD_MANIFEST_UNREADABLE_OR_MISSING"]
    blockers: list[str] = []
    if payload.get("apply_to_source") is not False:
        blockers.append("PAYLOAD_MANIFEST_APPLY_TO_SOURCE_NOT_FALSE")
    if payload.get("requires_human_review") is not True:
        blockers.append("PAYLOAD_MANIFEST_REQUIRES_HUMAN_REVIEW_NOT_TRUE")
    if bool(payload.get("import_rewrite_enabled")):
        blockers.append("PAYLOAD_MANIFEST_IMPORT_REWRITE_ENABLED")
    if payload.get("source_content_hash") != source_hash:
        blockers.append("PAYLOAD_MANIFEST_SOURCE_HASH_MISMATCH")
    return blockers


def _planned_payload_targets(payload_zip: Path, payload: dict[str, object] | None) -> list[str]:
    """Return safe Python payload entries that may be copied into project source."""
    if payload is None or not payload_zip.is_file():
        return []
    raw = payload.get("included_files", [])
    if not isinstance(raw, list):
        return []
    try:
        with zipfile.ZipFile(payload_zip, "r") as archive:
            names = set(archive.namelist())
    except (OSError, zipfile.BadZipFile):
        return []
    targets: list[str] = []
    for item in raw:
        text = str(item).replace("\\", "/").strip("/")
        if not text or Path(text).name in _META_FILES or not text.endswith(".py"):
            continue
        if Path(text).is_absolute() or ".." in Path(text).parts:
            continue
        if text in names:
            targets.append(text)
    return sorted(set(targets))


def _read_payload_manifest(payload_zip: Path) -> dict[str, object] | None:
    """Read the project patch payload manifest from the reviewed payload ZIP."""
    try:
        with zipfile.ZipFile(payload_zip, "r") as archive:
            if _PAYLOAD_MANIFEST_NAME not in archive.namelist():
                return None
            raw = archive.read(_PAYLOAD_MANIFEST_NAME).decode("utf-8")
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def _read_json_file(path: Path) -> dict[str, object]:
    """Return a JSON object from path, or an empty mapping when invalid."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _path_blockers(project_root: Path, preview_root: Path, path: Path, label: str, *, allow_source: bool) -> list[str]:
    """Return blockers for artifact and destination paths."""
    blockers: list[str] = []
    if allow_source:
        if _is_relative_to(path, preview_root):
            blockers.append(label + "_INSIDE_PREVIEW_ROOT")
    elif not _is_relative_to(path, preview_root):
        blockers.append(label + "_OUTSIDE_PREVIEW_ROOT")
    if not allow_source and _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    lowered = {part.lower() for part in path.parts}
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append(label + "_INSIDE_PROTECTED_" + forbidden.upper())
    return blockers


def _raise_if_protected(path: Path, label: str) -> None:
    """Raise if a support artifact path reaches protected support roots."""
    lowered = {part.lower() for part in path.parts}
    if {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"} & lowered:
        raise RuntimeError(label + " is inside a protected support root.")


def _checked_rules() -> list[str]:
    """Return stable rule labels checked by this executor."""
    return [
        "preflight_backup_contract_ready",
        "guarded_source_apply_execution_token_exact_match",
        "backup_snapshot_exists_and_hash_matches",
        "selected_source_hash_unchanged_before_write",
        "payload_manifest_requires_human_review_true",
        "payload_manifest_apply_to_source_false",
        "payload_manifest_import_rewrite_enabled_false",
        "payload_entries_are_safe_relative_python_paths",
        "destination_paths_inside_project_source_only",
        "preview_root_inside_project_support_only",
        "support_artifacts_outside_project_source",
        "protected_support_roots_blocked",
    ]


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
