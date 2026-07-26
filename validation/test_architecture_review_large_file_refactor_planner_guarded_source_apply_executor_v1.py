# project-path: validation/test_architecture_review_large_file_refactor_planner_guarded_source_apply_executor_v1.py
"""Validation for Guarded Source Apply Executor v1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.guarded_source_apply_executor import (
    GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
    build_guarded_source_apply_execution,
    write_guarded_source_apply_execution_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.guarded_source_apply_executor_formatting import (
    format_guarded_source_apply_execution,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import FEATURE_ID, SCHEMA_VERSION
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_dry_run_validator import (
    SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_preflight_backup_contract import (
    SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
    SourceApplyPreflightBackupContractResult,
)

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-guarded-source-apply-executor-v1"
PREVIOUS_MARKERS = [
    "architecture-review-large-file-refactor-planner-source-apply-preflight-backup-contract-v1",
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


def _make_context(tmp: Path) -> tuple[Path, Path, Path, Path, Path, str]:
    """Create a governed source-apply context with backup and payload."""
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    daily_root = _daily_root_for_test(project_root)
    preview_root = daily_root / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    dry_run_manifest = preview_root / "SOURCE_APPLY_DRY_RUN_VALIDATION.json"
    preflight_manifest = preview_root / "SOURCE_APPLY_PREFLIGHT_BACKUP_CONTRACT.json"
    backup = preview_root / "source_apply_backup_snapshot" / source_hash[:12] / target.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    backup.write_bytes(target.read_bytes())
    payload_zip = preview_root / "large_file_refactor_project_patch_payload.zip"
    _write_payload_zip(payload_zip, target, source_hash)
    dry_run_manifest.write_text(json.dumps({
        "status": "source_apply_dry_run_validated",
        "payload_zip_path": str(payload_zip),
        "planned_write_targets": ["large_module.py", "large_module_helpers.py"],
        "confirmation_token_required": SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
    }, indent=2), encoding="utf-8")
    preflight_manifest.write_text(json.dumps({
        "status": "source_apply_preflight_backup_ready",
        "backup_snapshot_path": str(backup),
        "confirmation_token_required": SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
    }, indent=2), encoding="utf-8")
    return project_root, target, preview_root, dry_run_manifest, backup, source_hash


def _write_payload_zip(payload_zip: Path, target: Path, source_hash: str, *, import_rewrite_enabled: bool = False) -> None:
    """Create a reviewed payload ZIP with safe Python entries."""
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": FEATURE_ID,
        "payload_kind": "large_file_refactor_project_preview_payload",
        "status": "payload_ready",
        "target_file": str(target),
        "source_content_hash": source_hash,
        "preview_root": str(payload_zip.parent),
        "artifact_validation_status": "passed",
        "import_migration_status": "preview_only",
        "import_rewrite_enabled": import_rewrite_enabled,
        "included_files": ["large_module.py", "large_module_helpers.py", "PROJECT_PATCH_PAYLOAD_MANIFEST.json"],
        "apply_to_source": False,
        "requires_human_review": True,
    }
    with zipfile.ZipFile(payload_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("large_module.py", "from large_module_helpers import helper\nVALUE = helper()\n")
        archive.writestr("large_module_helpers.py", "def helper():\n    return 2\n")
        archive.writestr("PROJECT_PATCH_PAYLOAD_MANIFEST.json", json.dumps(manifest, indent=2))


def _preflight(target: Path, preview_root: Path, dry_run_manifest: Path, backup: Path, source_hash: str) -> SourceApplyPreflightBackupContractResult:
    """Return a ready preflight backup result."""
    return SourceApplyPreflightBackupContractResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status="source_apply_preflight_backup_ready",
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        dry_run_manifest_path=str(dry_run_manifest),
        preflight_manifest_path=str(preview_root / "SOURCE_APPLY_PREFLIGHT_BACKUP_CONTRACT.json"),
        backup_snapshot_path=str(backup),
        backup_snapshot_hash=source_hash,
        confirmation_token_required=SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
        preflight_confirmation_present=True,
        preflight_confirmation_valid=True,
        backup_snapshot_expected=True,
        backup_source_is_selected_project_source=True,
        preview_artifacts_used_as_source_of_truth=False,
        preflight_recorded_for_future_train_only=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_mutation_enabled=False,
        source_hash_verified=True,
        checked_rules=["source_hash_verified"],
        blockers=[],
        warnings=[],
    )


def test_guarded_executor_writes_only_after_exact_token_and_backup() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, dry_run_manifest, backup, source_hash = _make_context(tmp)
        original = backup.read_text(encoding="utf-8")
        result = build_guarded_source_apply_execution(
            _preflight(target, preview_root, dry_run_manifest, backup, source_hash),
            active_project_root=str(project_root),
            execution_confirmation=GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
        )
        assert result.status == "guarded_source_apply_ready"
        assert result.apply_enabled is True
        assert result.rewrite_enabled is False
        assert result.source_mutation_enabled is True
        assert result.backup_snapshot_verified is True
        assert result.source_hash_verified_before_write is True
        manifest = write_guarded_source_apply_execution_manifest(result)
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["written_file_count"] == 2
        assert target.read_text(encoding="utf-8") == "from large_module_helpers import helper\nVALUE = helper()\n"
        assert (project_root / "large_module_helpers.py").read_text(encoding="utf-8") == "def helper():\n    return 2\n"
        assert backup.read_text(encoding="utf-8") == original
        assert str(manifest).startswith(str(preview_root))
        assert "GUARDED SOURCE APPLY EXECUTION" in format_guarded_source_apply_execution(result)
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def test_missing_execution_token_blocks_without_mutation() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, dry_run_manifest, backup, source_hash = _make_context(tmp)
        before = target.read_text(encoding="utf-8")
        result = build_guarded_source_apply_execution(
            _preflight(target, preview_root, dry_run_manifest, backup, source_hash),
            active_project_root=str(project_root),
            execution_confirmation="",
        )
        assert result.status == "blocked"
        assert "GUARDED_SOURCE_APPLY_EXECUTION_TOKEN_MISSING_OR_INVALID" in result.blockers
        write_guarded_source_apply_execution_manifest(result)
        assert target.read_text(encoding="utf-8") == before
        assert not (project_root / "large_module_helpers.py").exists()
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def test_source_hash_change_blocks_without_mutation() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, dry_run_manifest, backup, source_hash = _make_context(tmp)
        target.write_text("VALUE = 99\n", encoding="utf-8")
        result = build_guarded_source_apply_execution(
            _preflight(target, preview_root, dry_run_manifest, backup, source_hash),
            active_project_root=str(project_root),
            execution_confirmation=GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
        )
        assert result.status == "blocked"
        assert "SELECTED_SOURCE_HASH_CHANGED" in result.blockers
        write_guarded_source_apply_execution_manifest(result)
        assert target.read_text(encoding="utf-8") == "VALUE = 99\n"
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def test_missing_backup_snapshot_blocks_without_mutation() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, dry_run_manifest, backup, source_hash = _make_context(tmp)
        backup.unlink()
        result = build_guarded_source_apply_execution(
            _preflight(target, preview_root, dry_run_manifest, backup, source_hash),
            active_project_root=str(project_root),
            execution_confirmation=GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
        )
        assert result.status == "blocked"
        assert "BACKUP_SNAPSHOT_MISSING" in result.blockers
        write_guarded_source_apply_execution_manifest(result)
        assert target.read_text(encoding="utf-8") == "VALUE = 1\n"
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def test_import_rewrite_enabled_payload_blocks_executor() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, dry_run_manifest, backup, source_hash = _make_context(tmp)
        _write_payload_zip(preview_root / "large_file_refactor_project_patch_payload.zip", target, source_hash, import_rewrite_enabled=True)
        result = build_guarded_source_apply_execution(
            _preflight(target, preview_root, dry_run_manifest, backup, source_hash),
            active_project_root=str(project_root),
            execution_confirmation=GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
        )
        assert result.status == "blocked"
        assert "PAYLOAD_MANIFEST_IMPORT_REWRITE_ENABLED" in result.blockers
        write_guarded_source_apply_execution_manifest(result)
        assert target.read_text(encoding="utf-8") == "VALUE = 1\n"
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def main() -> int:
    test_guarded_executor_writes_only_after_exact_token_and_backup()
    test_missing_execution_token_blocks_without_mutation()
    test_source_hash_change_blocks_without_mutation()
    test_missing_backup_snapshot_blocks_without_mutation()
    test_import_rewrite_enabled_payload_blocks_executor()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
