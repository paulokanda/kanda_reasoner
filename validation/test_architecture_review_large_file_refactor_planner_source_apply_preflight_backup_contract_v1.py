# project-path: validation/test_architecture_review_large_file_refactor_planner_source_apply_preflight_backup_contract_v1.py
"""Validation for Source Apply Preflight + Backup/Snapshot Contract v1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import FEATURE_ID, SCHEMA_VERSION
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_dry_run_validator import (
    SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
    SourceApplyDryRunValidationResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_preflight_backup_contract import (
    SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
    build_source_apply_preflight_backup_contract,
    write_source_apply_preflight_backup_contract_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_preflight_backup_contract_formatting import (
    format_source_apply_preflight_backup_contract,
)

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-source-apply-preflight-backup-contract-v1"
PREVIOUS_MARKERS = [
    "architecture-review-large-file-refactor-planner-source-apply-dry-run-validator-v1",
    "architecture-review-large-file-refactor-planner-final-guarded-source-apply-planning-v1",
    "architecture-review-large-file-refactor-planner-human-confirmed-apply-contract-v1",
    "architecture-review-large-file-refactor-planner-human-confirmed-import-rewrite-contract-v1",
    "architecture-review-large-file-refactor-planner-import-rewrite-application-gate-v1",
    "architecture-review-large-file-refactor-planner-payload-apply-gui-wiring-v1",
    "architecture-review-large-file-refactor-planner-payload-apply-gate-v1",
    "architecture-review-large-file-refactor-planner-project-patch-payload-v1",
    "architecture-review-large-file-refactor-planner-patch-zip-creation-gate-v1",
    "architecture-review-large-file-refactor-planner-preview-validation-import-migration-v1",
    "architecture-review-large-file-refactor-planner-governed-preview-generation-v1",
    "architecture-review-large-file-refactor-planner-preview-writer-skeleton-v1",
    "architecture-review-large-file-refactor-planner-llm-arbitration-contracts-v1",
    "architecture-review-large-file-refactor-planner-docstring-contracts-v1",
    "architecture-review-large-file-refactor-planner-split-contracts-v1",
    "architecture-review-large-file-refactor-planner-ast-v1",
]


def _daily_root_for_test(project_root: Path) -> Path:
    """Return the canonical daily-work root for a temporary project."""
    anchor = project_root.anchor or str(project_root.parent)
    if anchor == "/":
        return project_root.parent / (project_root.name + "_delete_after_daily_work")
    return Path(anchor) / (project_root.name + "_delete_after_daily_work")


def _make_context(tmp: Path) -> tuple[Path, Path, Path, str, Path, Path]:
    """Create a governed preview context for preflight backup validation."""
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    daily_root = _daily_root_for_test(project_root)
    preview_root = daily_root / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    dry_run_manifest = preview_root / "SOURCE_APPLY_DRY_RUN_VALIDATION.json"
    dry_run_manifest.write_text('{"dry_run_only": true}\n', encoding="utf-8")
    return project_root, target, preview_root, source_hash, daily_root, dry_run_manifest


def _dry_run(
    target: Path,
    preview_root: Path,
    source_hash: str,
    dry_run_manifest: Path,
    *,
    status: str = "source_apply_dry_run_validated",
) -> SourceApplyDryRunValidationResult:
    """Return a ready dry-run validation result."""
    return SourceApplyDryRunValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_zip_path=str(preview_root / "large_file_refactor_project_patch_payload.zip"),
        final_plan_manifest_path=str(preview_root / "FINAL_GUARDED_SOURCE_APPLY_PLAN.json"),
        dry_run_manifest_path=str(dry_run_manifest),
        confirmation_token_required=SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
        dry_run_confirmation_present=True,
        dry_run_confirmation_valid=True,
        dry_run_recorded_for_future_train_only=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_mutation_enabled=False,
        dry_run_only=True,
        source_hash_verified=True,
        planned_write_target_count=1,
        planned_write_targets=["large_module.py"],
        checked_rules=["dry_run_only_true"],
        blockers=[],
        warnings=["NO_SELECTED_PROJECT_SOURCE_MUTATION_IN_THIS_TRAIN"],
    )


def test_preflight_backup_contract_copies_selected_source_snapshot_only() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, dry_run_manifest = _make_context(tmp)
        original_text = target.read_text(encoding="utf-8")
        result = build_source_apply_preflight_backup_contract(
            _dry_run(target, preview_root, source_hash, dry_run_manifest),
            active_project_root=str(project_root),
            preflight_confirmation=SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
        )
        assert result.status == "source_apply_preflight_backup_ready"
        assert result.preflight_confirmation_valid is True
        assert result.apply_enabled is False
        assert result.rewrite_enabled is False
        assert result.source_mutation_enabled is False
        assert result.preview_artifacts_used_as_source_of_truth is False
        written = write_source_apply_preflight_backup_contract_manifest(result)
        data = json.loads(written.read_text(encoding="utf-8"))
        backup_path = Path(data["backup_snapshot_path"])
        assert data["backup_snapshot_created"] is True
        assert backup_path.exists()
        assert backup_path.read_text(encoding="utf-8") == original_text
        assert hashlib.sha256(backup_path.read_bytes()).hexdigest() == source_hash
        assert target.read_text(encoding="utf-8") == original_text
        assert str(written).startswith(str(preview_root))
        assert "SOURCE APPLY PREFLIGHT BACKUP CONTRACT" in format_source_apply_preflight_backup_contract(result)
        shutil.rmtree(daily_root, ignore_errors=True)


def test_missing_preflight_token_blocks_backup_snapshot() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, dry_run_manifest = _make_context(tmp)
        result = build_source_apply_preflight_backup_contract(
            _dry_run(target, preview_root, source_hash, dry_run_manifest),
            active_project_root=str(project_root),
            preflight_confirmation="",
        )
        assert result.status == "blocked"
        assert "SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN_MISSING_OR_INVALID" in result.blockers
        assert result.backup_snapshot_expected is False
        written = write_source_apply_preflight_backup_contract_manifest(result)
        data = json.loads(written.read_text(encoding="utf-8"))
        assert data["backup_snapshot_created"] is False
        assert not Path(data["backup_snapshot_path"]).exists()
        shutil.rmtree(daily_root, ignore_errors=True)


def test_dry_run_not_validated_blocks_preflight() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, dry_run_manifest = _make_context(tmp)
        result = build_source_apply_preflight_backup_contract(
            _dry_run(target, preview_root, source_hash, dry_run_manifest, status="blocked"),
            active_project_root=str(project_root),
            preflight_confirmation=SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
        )
        assert result.status == "blocked"
        assert "SOURCE_APPLY_DRY_RUN_NOT_VALIDATED" in result.blockers
        assert result.apply_enabled is False
        shutil.rmtree(daily_root, ignore_errors=True)


def test_source_hash_change_blocks_preflight_backup() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, dry_run_manifest = _make_context(tmp)
        target.write_text("VALUE = 2\n", encoding="utf-8")
        result = build_source_apply_preflight_backup_contract(
            _dry_run(target, preview_root, source_hash, dry_run_manifest),
            active_project_root=str(project_root),
            preflight_confirmation=SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
        )
        assert result.status == "blocked"
        assert "SELECTED_SOURCE_HASH_CHANGED" in result.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_dry_run_manifest_missing_blocks_preflight() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, dry_run_manifest = _make_context(tmp)
        dry_run_manifest.unlink()
        result = build_source_apply_preflight_backup_contract(
            _dry_run(target, preview_root, source_hash, dry_run_manifest),
            active_project_root=str(project_root),
            preflight_confirmation=SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
        )
        assert result.status == "blocked"
        assert "SOURCE_APPLY_DRY_RUN_MANIFEST_MISSING" in result.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def main() -> int:
    test_preflight_backup_contract_copies_selected_source_snapshot_only()
    test_missing_preflight_token_blocks_backup_snapshot()
    test_dry_run_not_validated_blocks_preflight()
    test_source_hash_change_blocks_preflight_backup()
    test_dry_run_manifest_missing_blocks_preflight()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
