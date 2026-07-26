# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_apply_dry_run_validator.py
"""Dry-run validation evidence for a future guarded source-apply implementation."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
import zipfile

from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .final_guarded_source_apply_planning import FinalGuardedSourceApplyPlanResult
from .models import FEATURE_ID, SCHEMA_VERSION

__all__ = [
    "SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN",
    "SourceApplyDryRunValidationResult",
    "build_source_apply_dry_run_validation",
    "write_source_apply_dry_run_validation_manifest",
]

SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN = "CONFIRM_DRY_RUN_SOURCE_APPLY_VALIDATION"
_DRY_RUN_MANIFEST_NAME = "SOURCE_APPLY_DRY_RUN_VALIDATION.json"
_PAYLOAD_MANIFEST_NAME = "PROJECT_PATCH_PAYLOAD_MANIFEST.json"


@dataclass(frozen=True)
class SourceApplyDryRunValidationResult:
    """Review-only validation result for a future guarded source-apply train."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    payload_zip_path: str
    final_plan_manifest_path: str
    dry_run_manifest_path: str
    confirmation_token_required: str
    dry_run_confirmation_present: bool
    dry_run_confirmation_valid: bool
    dry_run_recorded_for_future_train_only: bool = True
    rewrite_enabled: bool = False
    apply_enabled: bool = False
    source_mutation_enabled: bool = False
    dry_run_only: bool = True
    source_hash_verified: bool = False
    planned_write_target_count: int = 0
    planned_write_targets: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready dry-run validation dictionary."""
        return asdict(self)


def build_source_apply_dry_run_validation(
    final_plan: FinalGuardedSourceApplyPlanResult,
    *,
    active_project_root: str,
    dry_run_confirmation: str = "",
) -> SourceApplyDryRunValidationResult:
    """Build review-only dry-run validation evidence without applying changes."""
    project_root = Path(active_project_root).resolve()
    preview_root = Path(final_plan.preview_root).resolve()
    target = Path(final_plan.target_file).resolve()
    payload_zip = Path(final_plan.payload_zip_path).resolve()
    final_plan_manifest = Path(final_plan.final_plan_manifest_path).resolve()
    dry_run_manifest = preview_root / _DRY_RUN_MANIFEST_NAME
    token_valid = dry_run_confirmation.strip() == SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN
    payload_manifest_data = _read_payload_manifest_from_zip(payload_zip)
    planned_targets = _planned_write_targets(payload_manifest_data)
    blockers = _dry_run_blockers(
        final_plan,
        project_root,
        preview_root,
        target,
        payload_zip,
        final_plan_manifest,
        payload_manifest_data,
        token_valid,
    )
    warnings = [
        "SOURCE_APPLY_DRY_RUN_RECORDED_FOR_FUTURE_TRAIN_ONLY",
        "NO_SELECTED_PROJECT_SOURCE_MUTATION_IN_THIS_TRAIN",
        "NO_IMPORT_REWRITE_APPLICATION_IN_THIS_TRAIN",
        "REWRITE_ENABLED_REMAINS_FALSE",
        "APPLY_ENABLED_REMAINS_FALSE",
        "SOURCE_MUTATION_ENABLED_REMAINS_FALSE",
    ]
    status = "source_apply_dry_run_validated" if not blockers else "blocked"
    source_hash_verified = "SELECTED_SOURCE_HASH_CHANGED" not in blockers and "TARGET_FILE_MISSING" not in blockers
    return SourceApplyDryRunValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=final_plan.source_content_hash,
        preview_root=str(preview_root),
        payload_zip_path=str(payload_zip),
        final_plan_manifest_path=str(final_plan_manifest),
        dry_run_manifest_path=str(dry_run_manifest),
        confirmation_token_required=SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
        dry_run_confirmation_present=bool(dry_run_confirmation.strip()),
        dry_run_confirmation_valid=token_valid,
        dry_run_recorded_for_future_train_only=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_mutation_enabled=False,
        dry_run_only=True,
        source_hash_verified=source_hash_verified and status.endswith("validated"),
        planned_write_target_count=len(planned_targets),
        planned_write_targets=planned_targets,
        checked_rules=_checked_rules(),
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_source_apply_dry_run_validation_manifest(result: SourceApplyDryRunValidationResult) -> Path:
    """Write dry-run validation evidence to the governed project-support Preview root."""
    manifest = Path(result.dry_run_manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Source apply dry-run manifest path is outside preview root.")
    lowered = {part.lower() for part in manifest.parts}
    forbidden = {"project_error_memory", "project_freeze_after_update", "project_freeze_ledger"}
    if lowered & forbidden:
        raise RuntimeError("Source apply dry-run manifest is inside a protected support root.")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    saved = json.loads(manifest.read_text(encoding="utf-8"))
    if saved.get("rewrite_enabled") is not False or saved.get("apply_enabled") is not False:
        raise RuntimeError("Source apply dry-run validation must keep rewrite/apply disabled.")
    if saved.get("source_mutation_enabled") is not False:
        raise RuntimeError("Source apply dry-run validation must keep source mutation disabled.")
    if saved.get("dry_run_only") is not True:
        raise RuntimeError("Source apply dry-run validation must remain dry-run only.")
    if saved.get("dry_run_recorded_for_future_train_only") is not True:
        raise RuntimeError("Source apply dry-run validation must be future-train evidence only.")
    return manifest


def _dry_run_blockers(
    final_plan: FinalGuardedSourceApplyPlanResult,
    project_root: Path,
    preview_root: Path,
    target: Path,
    payload_zip: Path,
    final_plan_manifest: Path,
    payload_manifest_data: dict[str, object] | None,
    token_valid: bool,
) -> list[str]:
    """Return blockers that prevent dry-run validation readiness."""
    blockers: list[str] = list(final_plan.blockers)
    if final_plan.status != "final_guarded_source_apply_plan_ready":
        blockers.append("FINAL_GUARDED_SOURCE_APPLY_PLAN_NOT_READY")
    if token_valid is not True:
        blockers.append("SOURCE_APPLY_DRY_RUN_TOKEN_MISSING_OR_INVALID")
    if final_plan.apply_enabled is not False:
        blockers.append("FINAL_PLAN_APPLY_ENABLED_UNEXPECTEDLY")
    if final_plan.rewrite_enabled is not False:
        blockers.append("FINAL_PLAN_REWRITE_ENABLED_UNEXPECTEDLY")
    if final_plan.source_mutation_enabled is not False:
        blockers.append("FINAL_PLAN_SOURCE_MUTATION_ENABLED_UNEXPECTEDLY")
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    blockers.extend(_path_blockers(project_root, preview_root, payload_zip, "PAYLOAD_ZIP"))
    blockers.extend(_path_blockers(project_root, preview_root, final_plan_manifest, "FINAL_PLAN_MANIFEST"))
    if not payload_zip.exists() or not payload_zip.is_file():
        blockers.append("PAYLOAD_ZIP_MISSING")
    elif payload_manifest_data is None:
        blockers.append("PAYLOAD_MANIFEST_UNREADABLE_OR_MISSING")
    if not final_plan_manifest.exists() or not final_plan_manifest.is_file():
        blockers.append("FINAL_PLAN_MANIFEST_MISSING")
    blockers.extend(_payload_manifest_blockers(payload_manifest_data))
    if not target.exists():
        blockers.append("TARGET_FILE_MISSING")
    elif hashlib.sha256(target.read_bytes()).hexdigest() != final_plan.source_content_hash:
        blockers.append("SELECTED_SOURCE_HASH_CHANGED")
    return blockers


def _payload_manifest_blockers(payload: dict[str, object] | None) -> list[str]:
    """Return blockers from payload manifest safety fields."""
    if payload is None:
        return []
    blockers: list[str] = []
    if payload.get("apply_to_source") is not False:
        blockers.append("PAYLOAD_MANIFEST_APPLY_TO_SOURCE_NOT_FALSE")
    if payload.get("requires_human_review") is not True:
        blockers.append("PAYLOAD_MANIFEST_REQUIRES_HUMAN_REVIEW_NOT_TRUE")
    if bool(payload.get("import_rewrite_enabled")):
        blockers.append("PAYLOAD_MANIFEST_IMPORT_REWRITE_ENABLED")
    if payload.get("source_content_hash") is None:
        blockers.append("PAYLOAD_MANIFEST_SOURCE_HASH_MISSING")
    return blockers


def _planned_write_targets(payload: dict[str, object] | None) -> list[str]:
    """Return normalized payload file targets that would be reviewed in a future apply train."""
    if payload is None:
        return []
    raw = payload.get("included_files", [])
    if not isinstance(raw, list):
        return []
    ignored = {
        "PROJECT_PATCH_PAYLOAD_MANIFEST.json",
        "PREVIEW_MANIFEST.json",
        "NO_SOURCE_WRITE_PROOF.txt",
        "IMPORT_MIGRATION_PREVIEW.json",
        "PATCH_ZIP_CREATION_GATE.json",
    }
    targets: list[str] = []
    for item in raw:
        text = str(item).replace("\\", "/").strip("/")
        if not text or Path(text).name in ignored:
            continue
        if ".." in Path(text).parts:
            continue
        targets.append(text)
    return sorted(set(targets))


def _read_payload_manifest_from_zip(payload_zip: Path) -> dict[str, object] | None:
    """Read the governed payload manifest from the payload ZIP."""
    try:
        with zipfile.ZipFile(payload_zip, "r") as archive:
            if _PAYLOAD_MANIFEST_NAME not in archive.namelist():
                return None
            raw = archive.read(_PAYLOAD_MANIFEST_NAME).decode("utf-8")
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except (OSError, zipfile.BadZipFile, KeyError, UnicodeDecodeError, json.JSONDecodeError):
        return None


def _path_blockers(project_root: Path, preview_root: Path, path: Path, label: str) -> list[str]:
    """Return blockers for paths that must stay in the governed preview root."""
    blockers: list[str] = []
    if not _is_relative_to(path, preview_root):
        blockers.append(label + "_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(path, project_root):
        blockers.append(label + "_INSIDE_PROJECT_SOURCE")
    lowered = {part.lower() for part in path.parts}
    for forbidden in ("project_error_memory", "project_freeze_after_update", "project_freeze_ledger"):
        if forbidden in lowered:
            blockers.append(label + "_INSIDE_PROTECTED_" + forbidden.upper())
    return blockers


def _checked_rules() -> list[str]:
    """Return stable rule labels checked by this dry-run validator."""
    return [
        "final_guarded_source_apply_plan_ready",
        "dry_run_confirmation_token_exact_match",
        "future_train_evidence_only",
        "dry_run_only_true",
        "rewrite_enabled_false_in_this_train",
        "apply_enabled_false_in_this_train",
        "source_mutation_enabled_false_in_this_train",
        "payload_manifest_apply_to_source_false",
        "payload_manifest_requires_human_review_true",
        "payload_manifest_import_rewrite_enabled_false",
        "selected_source_hash_unchanged",
        "preview_root_inside_project_support_only",
        "artifacts_outside_project_source",
        "protected_support_roots_blocked",
    ]


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is inside base."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
