# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_readiness.py
"""Exact-token readiness evidence for future import rewrite application."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .workbench_project_support_paths import daily_work_root, preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import ImportMigrationPreview, ImportMigrationRecord, SCHEMA_VERSION

__all__ = [
    "IMPORT_REWRITE_APPLY_READINESS_FEATURE_ID",
    "ImportRewriteApplyReadinessResult",
    "build_and_write_import_rewrite_apply_readiness",
    "daily_work_root_for_import_rewrite",
    "expected_import_rewrite_apply_token",
    "import_rewrite_preview_root_blockers",
]

IMPORT_REWRITE_APPLY_READINESS_FEATURE_ID = (
    "architecture-review-large-file-refactor-import-rewrite-apply-gating-v1"
)
_READINESS_MANIFEST = "IMPORT_REWRITE_APPLY_READINESS.json"
_DIFF_PREVIEW = "IMPORT_REWRITE_APPLY_DIFF_PREVIEW.txt"
_TOKEN_PREFIX = "KANDA-IMPORT-REWRITE"
_BLOCKING_RECORD_FLAGS = {
    "STAR_IMPORT_RISK",
    "RELATIVE_IMPORT_RISK",
    "DYNAMIC_IMPORT_RISK",
    "STRING_REFERENCE_RISK",
    "PATCH_TARGET_RISK",
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
class ImportRewriteApplyReadinessResult:
    """Readiness result for a future governed import rewrite apply train."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    readiness_manifest_path: str
    diff_preview_path: str
    exact_token_required: str
    exact_token_present: bool
    exact_token_valid: bool
    rewrite_enabled: bool = False
    apply_enabled: bool = False
    importer_count: int = 0
    no_op_importer_count: int = 0
    manual_review_count: int = 0
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    rewrite_plan: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready readiness evidence."""
        return asdict(self)


def daily_work_root_for_import_rewrite(project_root: str | Path) -> Path:
    """Return the disposable daily-work root used by import-rewrite tooling."""
    return daily_work_root(project_root)


def expected_import_rewrite_apply_token(import_preview: ImportMigrationPreview) -> str:
    """Return the deterministic exact token for the current import preview."""
    basis = {
        "target_file": import_preview.target_file,
        "source_hash": import_preview.source_content_hash,
        "records": [
            [record.importer_file, record.original_import, record.suggested_import]
            for record in import_preview.records
        ],
    }
    digest = hashlib.sha256(json.dumps(basis, sort_keys=True).encode("utf-8")).hexdigest()[:8].upper()
    return f"{_TOKEN_PREFIX}-{digest}"


def build_and_write_import_rewrite_apply_readiness(
    import_preview: ImportMigrationPreview,
    *,
    active_project_root: str,
    preview_root: str,
    exact_token: str = "",
) -> ImportRewriteApplyReadinessResult:
    """Build and write read-only import rewrite apply readiness evidence."""
    project_root = Path(active_project_root).resolve()
    preview_path = Path(preview_root).resolve()
    manifest_path = preview_path / _READINESS_MANIFEST
    diff_path = preview_path / _DIFF_PREVIEW
    token_required = expected_import_rewrite_apply_token(import_preview)
    token_present = bool(exact_token.strip())
    token_valid = exact_token.strip() == token_required
    rewrite_plan = [_rewrite_plan_record(record, project_root) for record in import_preview.records]
    blockers = _readiness_blockers(import_preview, project_root, preview_path, manifest_path, diff_path)
    manual_review_count = sum(1 for item in rewrite_plan if item["status"] == "manual_review_required")
    no_op_count = sum(1 for item in rewrite_plan if item["status"] == "no_rewrite_needed_facade_owned")
    warnings = _readiness_warnings(import_preview, rewrite_plan, token_present, token_valid)
    status = "import_rewrite_apply_ready_for_future_train" if not blockers else "blocked"
    result = ImportRewriteApplyReadinessResult(
        schema_version=SCHEMA_VERSION,
        feature_id=IMPORT_REWRITE_APPLY_READINESS_FEATURE_ID,
        status=status,
        target_file=import_preview.target_file,
        source_content_hash=import_preview.source_content_hash,
        preview_root=str(preview_path),
        readiness_manifest_path=str(manifest_path),
        diff_preview_path=str(diff_path),
        exact_token_required=token_required,
        exact_token_present=token_present,
        exact_token_valid=token_valid,
        rewrite_enabled=False,
        apply_enabled=False,
        importer_count=len(import_preview.records),
        no_op_importer_count=no_op_count,
        manual_review_count=manual_review_count,
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
        rewrite_plan=rewrite_plan,
    )
    _write_readiness_files(result)
    return result


def _rewrite_plan_record(record: ImportMigrationRecord, project_root: Path) -> dict[str, Any]:
    """Return one read-only rewrite-plan record."""
    flags = sorted(set(record.risk_flags))
    importer = Path(record.importer_file).resolve()
    status = "manual_review_required" if _record_needs_manual_review(record) else "no_rewrite_needed_facade_owned"
    action = "do_not_rewrite" if status == "no_rewrite_needed_facade_owned" else "manual_review_before_any_rewrite"
    return {
        "importer_file": str(importer),
        "importer_relative": _safe_relative(importer, project_root),
        "original_import": record.original_import,
        "suggested_import": record.suggested_import,
        "action": action,
        "status": status,
        "risk_flags": flags,
        "reason": _record_reason(record, status),
    }


def _record_needs_manual_review(record: ImportMigrationRecord) -> bool:
    """Return whether a record blocks automatic/no-op import rewrite classification."""
    if record.blockers:
        return True
    if record.status != "preview_only" or record.action != "review_only_no_rewrite":
        return True
    return bool(set(record.risk_flags) & _BLOCKING_RECORD_FLAGS)


def _record_reason(record: ImportMigrationRecord, status: str) -> str:
    """Return a concise human reason for a rewrite-plan record."""
    if status == "manual_review_required":
        return (
            "Import record has star, relative, dynamic, string, patch-target, blocker, "
            "or non-preview-only risk. It must not be rewritten automatically."
        )
    return (
        "Original module remains the public facade owner after source apply, so this "
        "record is captured as a no-op import rewrite candidate."
    )


def _readiness_blockers(
    import_preview: ImportMigrationPreview,
    project_root: Path,
    preview_root: Path,
    manifest_path: Path,
    diff_path: Path,
) -> list[str]:
    """Return blockers for unsafe readiness evidence."""
    blockers = list(import_preview.blockers)
    if import_preview.rewrite_enabled is not False:
        blockers.append("IMPORT_PREVIEW_REWRITE_ENABLED_UNEXPECTEDLY")
    if import_preview.status not in {"preview_only", "ready"}:
        blockers.append("IMPORT_PREVIEW_NOT_READY")
    blockers.extend(
        import_rewrite_preview_root_blockers(
            project_root, preview_root, manifest_path, diff_path
        )
    )
    target = Path(import_preview.target_file)
    if target.exists():
        current_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if current_hash != import_preview.source_content_hash:
            blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    for record in import_preview.records:
        if record.action != "review_only_no_rewrite":
            blockers.append("IMPORT_RECORD_ACTION_NOT_REVIEW_ONLY")
        if record.status != "preview_only":
            blockers.append("IMPORT_RECORD_NOT_PREVIEW_ONLY")
    return blockers


def import_rewrite_preview_root_blockers(
    project_root: Path,
    preview_root: Path,
    manifest_path: Path,
    diff_path: Path,
) -> list[str]:
    """Return root/shielding blockers for generated readiness files."""
    blockers: list[str] = []
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    for path, label in ((manifest_path, "MANIFEST"), (diff_path, "DIFF_PREVIEW")):
        if not _is_relative_to(path, preview_root):
            blockers.append(f"{label}_OUTSIDE_PREVIEW_ROOT")
        if _is_relative_to(path, project_root):
            blockers.append(f"{label}_INSIDE_PROJECT_SOURCE")
        lowered = {part.lower() for part in path.parts}
        for forbidden in _PROTECTED_PARTS:
            if forbidden.lower() in lowered:
                blockers.append(f"{label}_INSIDE_PROTECTED_{forbidden.upper()}")
    return blockers


# Backward-compatible private alias for existing internal consumers.
_preview_root_blockers = import_rewrite_preview_root_blockers


def _readiness_warnings(
    import_preview: ImportMigrationPreview,
    rewrite_plan: list[dict[str, Any]],
    token_present: bool,
    token_valid: bool,
) -> list[str]:
    """Return review warnings for readiness evidence."""
    warnings = [
        "IMPORT_REWRITE_APPLY_GATING_ONLY",
        "IMPORT_REWRITE_NOT_APPLIED_IN_THIS_TRAIN",
        "IMPORT_REWRITE_ROLLBACK_NOT_IMPLEMENTED",
        "FACADE_OWNERSHIP_PRESERVED_NO_REWRITE_DEFAULT",
    ]
    warnings.extend(import_preview.warnings)
    if token_present and token_valid:
        warnings.append("EXACT_IMPORT_REWRITE_TOKEN_VALID_FOR_FUTURE_TRAIN_ONLY")
    elif token_present:
        warnings.append("EXACT_IMPORT_REWRITE_TOKEN_INVALID")
    for item in rewrite_plan:
        if item["status"] == "manual_review_required":
            warnings.append("IMPORT_REWRITE_MANUAL_REVIEW_RECORD_PRESENT")
    return warnings


def _write_readiness_files(result: ImportRewriteApplyReadinessResult) -> None:
    """Write manifest and human-readable diff preview under selected project support only."""
    manifest = Path(result.readiness_manifest_path).resolve()
    diff = Path(result.diff_preview_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root) or not _is_relative_to(diff, preview_root):
        raise RuntimeError("Import rewrite readiness files must stay inside preview root.")
    preview_root.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    diff.write_text(_diff_preview_text(result), encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("rewrite_enabled") is not False or saved.get("apply_enabled") is not False:
        raise RuntimeError("Import rewrite readiness must keep rewrite/apply disabled.")


def _diff_preview_text(result: ImportRewriteApplyReadinessResult) -> str:
    """Return readable no-write diff preview text."""
    lines = [
        "IMPORT REWRITE APPLY READINESS - NO WRITE",
        f"Status: {result.status}",
        f"Rewrite enabled: {result.rewrite_enabled}",
        f"Apply enabled: {result.apply_enabled}",
        f"Exact token required: {result.exact_token_required}",
        "",
    ]
    for item in result.rewrite_plan:
        lines.append(f"File: {item['importer_relative']}")
        lines.append(f"Status: {item['status']}")
        lines.append(f"Action: {item['action']}")
        lines.append(f"Original: {item['original_import']}")
        lines.append(f"Reason: {item['reason']}")
        lines.append("")
    return "\n".join(lines)


def _checked_rules() -> list[str]:
    """Return stable checked-rule labels."""
    return [
        "import_preview_rewrite_enabled_false",
        "import_records_review_only",
        "facade_ownership_preserved_no_rewrite_default",
        "manual_review_required_for_star_relative_dynamic_string_patch_targets",
        "readiness_manifest_project_support_only",
        "diff_preview_project_support_only",
        "project_source_not_modified",
        "apply_enabled_false",
        "rewrite_enabled_false",
    ]


def _allowed_preview_roots_for(project_root: Path) -> list[Path]:
    """Return the selected project's persistent Workbench Preview support root."""
    return [preview_runs_root(project_root)]


def _safe_relative(path: Path, root: Path) -> str:
    """Return a display relative path without raising."""
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
