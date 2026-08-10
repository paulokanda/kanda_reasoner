# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_executor.py
"""Exact-token guarded import rewrite apply for safe records only."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from kanda_reasoner_app.project_fire_shield import (
    FireShieldPhase,
    assert_fire_shield_payload_bytes_allowed,
    assert_fire_shield_write_allowed,
    build_current_fire_shield_context,
    verify_tool_snapshot_unchanged,
)

from .models import SCHEMA_VERSION
from .workbench_import_rewrite_apply_readiness import ImportRewriteApplyReadinessResult

__all__ = [
    "IMPORT_REWRITE_GUARDED_APPLY_FEATURE_ID",
    "ImportRewriteGuardedApplyResult",
    "execute_guarded_import_rewrite_apply",
    "expected_guarded_import_rewrite_apply_token",
    "validate_import_rewrite_post_apply",
]

IMPORT_REWRITE_GUARDED_APPLY_FEATURE_ID = (
    "architecture-review-large-file-refactor-import-rewrite-guarded-apply-v1"
)
_EXECUTION_MANIFEST = "IMPORT_REWRITE_APPLY_EXECUTION_MANIFEST.json"
_ROLLBACK_MANIFEST = "IMPORT_REWRITE_ROLLBACK_MANIFEST.json"
_POST_APPLY_REPORT = "IMPORT_REWRITE_POST_APPLY_VALIDATION.json"
_BACKUP_DIR = "import_rewrite_backups"
_SAFE_STATUSES = {"safe_rewrite_ready", "rewrite_ready"}
_BLOCKED_FLAGS = {
    "STAR_IMPORT_RISK",
    "RELATIVE_IMPORT_RISK",
    "DYNAMIC_IMPORT_RISK",
    "STRING_REFERENCE_RISK",
    "PATCH_TARGET_RISK",
    "IMPORTER_SYNTAX_RISK",
}
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_error_memory",
    "project_freeze_after_update",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class ImportRewriteGuardedApplyResult:
    """Result evidence for exact-token import rewrite apply."""

    schema_version: str
    feature_id: str
    status: str
    active_project_root: str
    preview_root: str
    exact_token_required: str
    exact_token_present: bool
    exact_token_valid: bool
    execution_manifest_path: str
    rollback_manifest_path: str
    post_apply_validation_path: str
    changed_files: list[str] = field(default_factory=list)
    skipped_files: list[str] = field(default_factory=list)
    manual_review_records: list[dict[str, Any]] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validation_status: str = "not_run"

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready result evidence."""
        return asdict(self)


def expected_guarded_import_rewrite_apply_token(readiness: ImportRewriteApplyReadinessResult | dict[str, Any]) -> str:
    """Return the exact token required for import rewrite apply."""
    data = _readiness_dict(readiness)
    return str(data.get("exact_token_required", ""))


def execute_guarded_import_rewrite_apply(
    readiness: ImportRewriteApplyReadinessResult | dict[str, Any],
    *,
    active_project_root: str,
    preview_root: str,
    exact_token: str = "",
) -> ImportRewriteGuardedApplyResult:
    """Apply only safe import rewrites after exact token and backup gates pass."""
    data = _readiness_dict(readiness)
    project_root = Path(active_project_root).resolve()
    preview_path = Path(preview_root).resolve()
    token_required = expected_guarded_import_rewrite_apply_token(data)
    token_present = bool(exact_token.strip())
    token_valid = exact_token.strip() == token_required and bool(token_required)
    execution_path = preview_path / _EXECUTION_MANIFEST
    rollback_path = preview_path / _ROLLBACK_MANIFEST
    post_apply_path = preview_path / _POST_APPLY_REPORT
    blockers = _common_blockers(data, project_root, preview_path, execution_path, rollback_path, post_apply_path)
    if not token_valid:
        blockers.append("EXACT_IMPORT_REWRITE_APPLY_TOKEN_REQUIRED")
    safe_records, manual_records, record_blockers = _classify_records(data.get("rewrite_plan", []), project_root)
    blockers.extend(record_blockers)
    changed_files: list[str] = []
    skipped_files: list[str] = []
    rollback_entries: list[dict[str, str]] = []
    if not blockers:
        changed_files, skipped_files, rollback_entries, blockers = _apply_safe_records(
            safe_records,
            project_root,
            preview_path,
        )
    status = "import_rewrite_apply_blocked" if blockers else "import_rewrite_apply_applied"
    if not blockers and not changed_files:
        status = "import_rewrite_apply_no_safe_rewrites"
    validation_status = "not_run"
    if not blockers:
        validation_status = validate_import_rewrite_post_apply(
            changed_files=changed_files,
            preview_root=str(preview_path),
        )["status"]
    result = ImportRewriteGuardedApplyResult(
        schema_version=SCHEMA_VERSION,
        feature_id=IMPORT_REWRITE_GUARDED_APPLY_FEATURE_ID,
        status=status,
        active_project_root=str(project_root),
        preview_root=str(preview_path),
        exact_token_required=token_required,
        exact_token_present=token_present,
        exact_token_valid=token_valid,
        execution_manifest_path=str(execution_path),
        rollback_manifest_path=str(rollback_path),
        post_apply_validation_path=str(post_apply_path),
        changed_files=changed_files,
        skipped_files=skipped_files,
        manual_review_records=manual_records,
        blockers=sorted(set(blockers)),
        warnings=_warnings(manual_records, skipped_files),
        validation_status=validation_status,
    )
    _write_execution_evidence(result, rollback_entries)
    return result


def validate_import_rewrite_post_apply(*, changed_files: list[str], preview_root: str) -> dict[str, Any]:
    """Validate changed importer files after guarded rewrite apply."""
    blockers: list[str] = []
    checked: list[str] = []
    for filename in changed_files:
        path = Path(filename).resolve()
        try:
            text = path.read_text(encoding="utf-8")
            compile(text, str(path), "exec")
            checked.append(str(path))
        except Exception as exc:  # pragma: no cover - exact parser exception not important.
            blockers.append(f"IMPORTER_POST_APPLY_PARSE_FAILED:{path}:{exc}")
    report = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": IMPORT_REWRITE_GUARDED_APPLY_FEATURE_ID,
        "status": "IMPORT_REWRITE_STRUCTURAL_PASS" if not blockers else "IMPORT_REWRITE_STRUCTURAL_FAIL",
        "checked_files": checked,
        "behavior_equivalence_claimed": False,
        "blockers": blockers,
        "warnings": ["IMPORT_REWRITE_BEHAVIOR_NOT_CLAIMED"],
    }
    preview_path = Path(preview_root).resolve()
    preview_path.mkdir(parents=True, exist_ok=True)
    (preview_path / _POST_APPLY_REPORT).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _apply_safe_records(
    records: list[dict[str, Any]],
    project_root: Path,
    preview_root: Path,
) -> tuple[list[str], list[str], list[dict[str, str]], list[str]]:
    """Apply safe rewrite records and return changed/skipped/rollback/blockers."""
    changed: list[str] = []
    skipped: list[str] = []
    rollback_entries: list[dict[str, str]] = []
    blockers: list[str] = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in records:
        grouped.setdefault(str(Path(item["importer_file"]).resolve()), []).append(item)
    backup_root = preview_root / _BACKUP_DIR
    backup_root.mkdir(parents=True, exist_ok=True)
    fire_shield = build_current_fire_shield_context(
        phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
        operation_id="workbench-import-rewrite-apply",
    )
    for filename, items in grouped.items():
        path = Path(filename).resolve()
        text = path.read_text(encoding="utf-8")
        original_hash = _sha256_text(text)
        new_text = text
        for item in items:
            original = str(item.get("original_import", ""))
            suggested = str(item.get("suggested_import", ""))
            if not original or not suggested or original == suggested:
                skipped.append(str(path))
                continue
            count = new_text.count(original)
            if count != 1:
                blockers.append(f"IMPORT_REWRITE_NON_UNIQUE_MATCH:{path}")
                continue
            new_text = new_text.replace(original, suggested, 1)
        if blockers or new_text == text:
            continue
        assert_fire_shield_write_allowed(
            fire_shield,
            path,
            operation="REPLACE",
        )
        assert_fire_shield_payload_bytes_allowed(
            fire_shield,
            new_text.encode("utf-8"),
            path.relative_to(project_root).as_posix(),
        )
        backup_file = backup_root / (_sha256_text(str(path))[:16] + ".bak")
        backup_file.write_text(text, encoding="utf-8")
        temp_file = path.with_suffix(path.suffix + ".kanda_import_rewrite_tmp")
        temp_file.write_text(new_text, encoding="utf-8")
        shutil.move(str(temp_file), str(path))
        new_hash = _sha256_text(new_text)
        changed.append(str(path))
        rollback_entries.append({
            "file": str(path),
            "backup_file": str(backup_file.resolve()),
            "before_hash": original_hash,
            "after_hash": new_hash,
        })
        try:
            path.relative_to(project_root)
        except ValueError:
            blockers.append(f"IMPORTER_OUTSIDE_PROJECT_AFTER_WRITE:{path}")
    verify_tool_snapshot_unchanged(fire_shield)
    return changed, skipped, rollback_entries, blockers


def _classify_records(records: list[dict[str, Any]], project_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Split rewrite records into safe and manual-review groups."""
    safe: list[dict[str, Any]] = []
    manual: list[dict[str, Any]] = []
    blockers: list[str] = []
    for item in records:
        path = Path(str(item.get("importer_file", ""))).resolve()
        flags = set(item.get("risk_flags", []))
        if not _is_relative_to(path, project_root):
            blockers.append("IMPORT_REWRITE_RECORD_OUTSIDE_PROJECT")
            continue
        if item.get("status") in _SAFE_STATUSES and item.get("action") == "rewrite_import":
            if flags & _BLOCKED_FLAGS:
                manual.append(item)
            else:
                safe.append(item)
        else:
            manual.append(item)
    return safe, manual, blockers


def _common_blockers(
    data: dict[str, Any],
    project_root: Path,
    preview_root: Path,
    execution_path: Path,
    rollback_path: Path,
    post_apply_path: Path,
) -> list[str]:
    """Return common no-leak and readiness blockers."""
    blockers = list(data.get("blockers", []))
    if data.get("status") != "import_rewrite_apply_ready_for_future_train":
        blockers.append("IMPORT_REWRITE_READINESS_NOT_READY")
    if data.get("rewrite_enabled") is not False or data.get("apply_enabled") is not False:
        blockers.append("IMPORT_REWRITE_READINESS_ENABLES_WRITES")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    for path, label in ((execution_path, "EXECUTION"), (rollback_path, "ROLLBACK"), (post_apply_path, "POST_APPLY")):
        if not _is_relative_to(path, preview_root):
            blockers.append(f"{label}_EVIDENCE_OUTSIDE_PREVIEW_ROOT")
        lowered = {part.lower() for part in path.parts}
        for forbidden in _PROTECTED_PARTS:
            if forbidden.lower() in lowered:
                blockers.append(f"{label}_EVIDENCE_INSIDE_PROTECTED_{forbidden.upper()}")
    return blockers


def _write_execution_evidence(result: ImportRewriteGuardedApplyResult, rollback_entries: list[dict[str, str]]) -> None:
    """Write execution and rollback evidence under preview root."""
    preview = Path(result.preview_root).resolve()
    preview.mkdir(parents=True, exist_ok=True)
    Path(result.execution_manifest_path).write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rollback_manifest = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": IMPORT_REWRITE_GUARDED_APPLY_FEATURE_ID,
        "status": "rollback_ready" if rollback_entries else "rollback_not_needed_no_changed_files",
        "entries": rollback_entries,
    }
    Path(result.rollback_manifest_path).write_text(json.dumps(rollback_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _readiness_dict(readiness: ImportRewriteApplyReadinessResult | dict[str, Any]) -> dict[str, Any]:
    """Return readiness as a dictionary without mutating input."""
    if isinstance(readiness, dict):
        return dict(readiness)
    return readiness.to_dict()


def _warnings(manual_records: list[dict[str, Any]], skipped_files: list[str]) -> list[str]:
    """Return warnings for import rewrite apply evidence."""
    warnings = ["IMPORT_REWRITE_APPLY_EXACT_TOKEN_GATED", "IMPORT_REWRITE_BEHAVIOR_NOT_CLAIMED"]
    if manual_records:
        warnings.append("MANUAL_REVIEW_IMPORT_RECORDS_NOT_REWRITTEN")
    if skipped_files:
        warnings.append("IMPORT_REWRITE_SKIPPED_NO_CHANGE_RECORDS")
    return sorted(set(warnings))


def _allowed_preview_roots_for(project_root: Path) -> list[Path]:
    """Return the selected project's persistent Workbench Preview support root."""
    return [preview_runs_root(project_root)]


def _sha256_text(text: str) -> str:
    """Hash text using UTF-8 bytes."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
