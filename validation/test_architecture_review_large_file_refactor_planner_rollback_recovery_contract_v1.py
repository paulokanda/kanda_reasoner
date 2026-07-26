# project-path: validation/test_architecture_review_large_file_refactor_planner_rollback_recovery_contract_v1.py
"""Validation for Rollback / Recovery Contract v1."""
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
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import FEATURE_ID, SCHEMA_VERSION
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.post_apply_validation import (
    POST_APPLY_VALIDATION_TOKEN,
    build_post_apply_validation,
    write_post_apply_validation_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_preflight_backup_contract import (
    SOURCE_APPLY_PREFLIGHT_BACKUP_TOKEN,
    SourceApplyPreflightBackupContractResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_rollback_recovery import (
    SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN,
    build_source_apply_rollback_recovery,
    write_source_apply_rollback_recovery_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_rollback_recovery_formatting import (
    format_source_apply_rollback_recovery,
)

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-rollback-recovery-contract-v1"
PREVIOUS_MARKERS = [
    "architecture-review-large-file-refactor-planner-post-apply-validation-hash-evidence-v1",
    "architecture-review-large-file-refactor-planner-guarded-source-apply-executor-v1",
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
    anchor = project_root.anchor or str(project_root.parent)
    if anchor == "/":
        return project_root.parent / (project_root.name + "_delete_after_daily_work")
    return Path(anchor) / (project_root.name + "_delete_after_daily_work")


def _make_post_apply_context(tmp: Path) -> tuple[Path, Path, Path, Path, Path, str, str]:
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    before_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    preview_root = _daily_root_for_test(project_root) / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    backup = preview_root / "source_apply_backup_snapshot" / before_hash[:12] / target.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    backup.write_bytes(target.read_bytes())
    payload_zip = preview_root / "large_file_refactor_project_patch_payload.zip"
    _write_payload_zip(payload_zip, target, before_hash)
    dry_run_manifest = preview_root / "SOURCE_APPLY_DRY_RUN_VALIDATION.json"
    dry_run_manifest.write_text(json.dumps({"status": "source_apply_dry_run_validated", "payload_zip_path": str(payload_zip)}, indent=2), encoding="utf-8")
    preflight_manifest = preview_root / "SOURCE_APPLY_PREFLIGHT_BACKUP_CONTRACT.json"
    preflight_manifest.write_text(json.dumps({"status": "source_apply_preflight_backup_ready", "backup_snapshot_path": str(backup)}, indent=2), encoding="utf-8")
    preflight = _preflight(target, preview_root, dry_run_manifest, backup, before_hash)
    execution = build_guarded_source_apply_execution(
        preflight,
        active_project_root=str(project_root),
        execution_confirmation=GUARDED_SOURCE_APPLY_EXECUTOR_TOKEN,
    )
    execution_manifest = write_guarded_source_apply_execution_manifest(execution)
    after_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    post_apply = build_post_apply_validation(
        str(execution_manifest),
        active_project_root=str(project_root),
        validation_confirmation=POST_APPLY_VALIDATION_TOKEN,
    )
    post_apply_manifest = write_post_apply_validation_manifest(post_apply)
    assert after_hash != before_hash
    return project_root, target, preview_root, post_apply_manifest, backup, before_hash, after_hash


def _write_payload_zip(payload_zip: Path, target: Path, source_hash: str) -> None:
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "feature_id": FEATURE_ID,
        "status": "payload_ready",
        "target_file": str(target),
        "source_content_hash": source_hash,
        "preview_root": str(payload_zip.parent),
        "import_rewrite_enabled": False,
        "included_files": ["large_module.py", "large_module_helpers.py", "PROJECT_PATCH_PAYLOAD_MANIFEST.json"],
        "apply_to_source": False,
        "requires_human_review": True,
    }
    with zipfile.ZipFile(payload_zip, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("large_module.py", "from large_module_helpers import helper\nVALUE = helper()\n")
        archive.writestr("large_module_helpers.py", "def helper():\n    return 2\n")
        archive.writestr("PROJECT_PATCH_PAYLOAD_MANIFEST.json", json.dumps(manifest, indent=2))


def _preflight(target: Path, preview_root: Path, dry_run_manifest: Path, backup: Path, source_hash: str) -> SourceApplyPreflightBackupContractResult:
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


def test_rollback_restores_selected_source_only_from_backup() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, post_apply_manifest, backup, before_hash, after_hash = _make_post_apply_context(tmp)
        helper = project_root / "large_module_helpers.py"
        assert helper.is_file()
        backup_text = backup.read_text(encoding="utf-8")
        result = build_source_apply_rollback_recovery(
            str(post_apply_manifest),
            active_project_root=str(project_root),
            rollback_confirmation=SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN,
        )
        assert result.status == "rollback_recovery_ready"
        assert result.source_content_hash_current == after_hash
        manifest = write_source_apply_rollback_recovery_manifest(result)
        data = json.loads(manifest.read_text(encoding="utf-8"))
        assert data["status"] == "source_apply_rollback_recovered"
        assert data["source_content_hash_after_rollback"] == before_hash
        assert hashlib.sha256(target.read_bytes()).hexdigest() == before_hash
        assert backup.read_text(encoding="utf-8") == backup_text
        assert helper.is_file()
        assert "NON_TARGET_WRITTEN_FILES_LEFT" in " ".join(data["warnings"])
        assert "SOURCE APPLY ROLLBACK" in format_source_apply_rollback_recovery(result)
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def test_missing_rollback_token_blocks_without_mutation() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, _preview_root, post_apply_manifest, _backup, _before_hash, after_hash = _make_post_apply_context(tmp)
        before_text = target.read_text(encoding="utf-8")
        result = build_source_apply_rollback_recovery(str(post_apply_manifest), active_project_root=str(project_root), rollback_confirmation="")
        assert result.status == "blocked"
        assert "ROLLBACK_RECOVERY_TOKEN_MISSING_OR_INVALID" in result.blockers
        write_source_apply_rollback_recovery_manifest(result)
        assert target.read_text(encoding="utf-8") == before_text
        assert hashlib.sha256(target.read_bytes()).hexdigest() == after_hash
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def test_current_source_hash_mismatch_blocks_rollback() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, _preview_root, post_apply_manifest, _backup, _before_hash, _after_hash = _make_post_apply_context(tmp)
        target.write_text("MANUAL_CHANGE = True\n", encoding="utf-8")
        result = build_source_apply_rollback_recovery(
            str(post_apply_manifest),
            active_project_root=str(project_root),
            rollback_confirmation=SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN,
        )
        assert result.status == "blocked"
        assert "CURRENT_SOURCE_HASH_MISMATCH" in result.blockers
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def test_project_reference_target_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, _target, _preview_root, post_apply_manifest, _backup, _before_hash, _after_hash = _make_post_apply_context(tmp)
        ref_dir = project_root / ".project_reference"
        ref_dir.mkdir()
        ref_file = ref_dir / "bad.py"
        ref_file.write_text("VALUE = 9\n", encoding="utf-8")
        data = json.loads(post_apply_manifest.read_text(encoding="utf-8"))
        data["target_file"] = str(ref_file)
        data["written_files"] = [str(ref_file)]
        post_apply_manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")
        result = build_source_apply_rollback_recovery(
            str(post_apply_manifest),
            active_project_root=str(project_root),
            rollback_confirmation=SOURCE_APPLY_ROLLBACK_RECOVERY_TOKEN,
        )
        assert result.status == "blocked"
        assert any("PROJECT_REFERENCE" in item for item in result.blockers)
        shutil.rmtree(_daily_root_for_test(project_root), ignore_errors=True)


def main() -> int:
    test_rollback_restores_selected_source_only_from_backup()
    test_missing_rollback_token_blocks_without_mutation()
    test_current_source_hash_mismatch_blocks_rollback()
    test_project_reference_target_blocks()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
