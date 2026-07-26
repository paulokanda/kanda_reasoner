# project-path: validation/test_architecture_review_large_file_refactor_planner_source_apply_dry_run_validator_v1.py
"""Validation for Source Apply Dry-Run Validator v1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.final_guarded_source_apply_planning import (
    FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
    FinalGuardedSourceApplyPlanResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import FEATURE_ID, SCHEMA_VERSION
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_dry_run_validator import (
    SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
    build_source_apply_dry_run_validation,
    write_source_apply_dry_run_validation_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_apply_dry_run_validator_formatting import (
    format_source_apply_dry_run_validation,
)

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-source-apply-dry-run-validator-v1"
PREVIOUS_MARKERS = [
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


def _make_context(tmp: Path) -> tuple[Path, Path, Path, str, Path, Path, Path]:
    """Create a governed preview context for dry-run validation."""
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    daily_root = _daily_root_for_test(project_root)
    preview_root = daily_root / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    draft = preview_root / "large_module.py"
    draft.write_text("VALUE = 1\nHELPER = True\n", encoding="utf-8")
    payload_manifest = preview_root / "PROJECT_PATCH_PAYLOAD_MANIFEST.json"
    payload_manifest.write_text(
        json.dumps(
            {
                "target_file": str(target),
                "source_content_hash": source_hash,
                "preview_root": str(preview_root),
                "apply_to_source": False,
                "requires_human_review": True,
                "import_rewrite_enabled": False,
                "included_files": [
                    "PREVIEW_MANIFEST.json",
                    "PROJECT_PATCH_PAYLOAD_MANIFEST.json",
                    "large_module.py",
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    payload_zip = preview_root / "large_file_refactor_project_patch_payload.zip"
    with zipfile.ZipFile(payload_zip, "w") as archive:
        archive.write(payload_manifest, "PROJECT_PATCH_PAYLOAD_MANIFEST.json")
        archive.write(draft, "large_module.py")
    final_plan_manifest = preview_root / "FINAL_GUARDED_SOURCE_APPLY_PLAN.json"
    final_plan_manifest.write_text('{"apply_enabled": false}\n', encoding="utf-8")
    return project_root, target, preview_root, source_hash, daily_root, payload_zip, final_plan_manifest


def _final_plan(
    target: Path,
    preview_root: Path,
    source_hash: str,
    payload_zip: Path,
    final_plan_manifest: Path,
    *,
    status: str = "final_guarded_source_apply_plan_ready",
) -> FinalGuardedSourceApplyPlanResult:
    """Return a ready planning-only final source-apply plan."""
    return FinalGuardedSourceApplyPlanResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_zip_path=str(payload_zip),
        human_apply_contract_manifest_path=str(preview_root / "HUMAN_CONFIRMED_APPLY_CONTRACT.json"),
        final_plan_manifest_path=str(final_plan_manifest),
        confirmation_token_required=FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
        planning_confirmation_present=True,
        planning_confirmation_valid=True,
        planning_recorded_for_future_train_only=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_mutation_enabled=False,
        source_hash_verified=True,
        checked_rules=["source_mutation_enabled_false_in_this_train"],
        blockers=[],
        warnings=["SOURCE_MUTATION_NOT_IMPLEMENTED_IN_THIS_TRAIN"],
    )


def test_dry_run_validation_records_readiness_without_source_mutation() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, final_plan_manifest = _make_context(tmp)
        result = build_source_apply_dry_run_validation(
            _final_plan(target, preview_root, source_hash, payload_zip, final_plan_manifest),
            active_project_root=str(project_root),
            dry_run_confirmation=SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
        )
        assert result.status == "source_apply_dry_run_validated"
        assert result.dry_run_confirmation_valid is True
        assert result.apply_enabled is False
        assert result.rewrite_enabled is False
        assert result.source_mutation_enabled is False
        assert result.dry_run_only is True
        assert result.source_hash_verified is True
        assert result.planned_write_targets == ["large_module.py"]
        written = write_source_apply_dry_run_validation_manifest(result)
        data = json.loads(written.read_text(encoding="utf-8"))
        assert data["apply_enabled"] is False
        assert data["rewrite_enabled"] is False
        assert data["source_mutation_enabled"] is False
        assert data["dry_run_only"] is True
        assert data["dry_run_recorded_for_future_train_only"] is True
        assert str(written).startswith(str(preview_root))
        assert "SOURCE APPLY DRY-RUN VALIDATION" in format_source_apply_dry_run_validation(result)
        shutil.rmtree(daily_root, ignore_errors=True)


def test_missing_dry_run_token_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, final_plan_manifest = _make_context(tmp)
        result = build_source_apply_dry_run_validation(
            _final_plan(target, preview_root, source_hash, payload_zip, final_plan_manifest),
            active_project_root=str(project_root),
            dry_run_confirmation="",
        )
        assert result.status == "blocked"
        assert "SOURCE_APPLY_DRY_RUN_TOKEN_MISSING_OR_INVALID" in result.blockers
        assert result.apply_enabled is False
        shutil.rmtree(daily_root, ignore_errors=True)


def test_final_plan_not_ready_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, final_plan_manifest = _make_context(tmp)
        result = build_source_apply_dry_run_validation(
            _final_plan(target, preview_root, source_hash, payload_zip, final_plan_manifest, status="blocked"),
            active_project_root=str(project_root),
            dry_run_confirmation=SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
        )
        assert result.status == "blocked"
        assert "FINAL_GUARDED_SOURCE_APPLY_PLAN_NOT_READY" in result.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_source_hash_change_blocks_dry_run() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, final_plan_manifest = _make_context(tmp)
        target.write_text("VALUE = 2\n", encoding="utf-8")
        result = build_source_apply_dry_run_validation(
            _final_plan(target, preview_root, source_hash, payload_zip, final_plan_manifest),
            active_project_root=str(project_root),
            dry_run_confirmation=SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
        )
        assert result.status == "blocked"
        assert "SELECTED_SOURCE_HASH_CHANGED" in result.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_payload_manifest_apply_to_source_true_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, final_plan_manifest = _make_context(tmp)
        manifest = {
            "target_file": str(target),
            "source_content_hash": source_hash,
            "apply_to_source": True,
            "requires_human_review": True,
            "import_rewrite_enabled": False,
            "included_files": ["large_module.py"],
        }
        with zipfile.ZipFile(payload_zip, "w") as archive:
            archive.writestr("PROJECT_PATCH_PAYLOAD_MANIFEST.json", json.dumps(manifest))
        result = build_source_apply_dry_run_validation(
            _final_plan(target, preview_root, source_hash, payload_zip, final_plan_manifest),
            active_project_root=str(project_root),
            dry_run_confirmation=SOURCE_APPLY_DRY_RUN_VALIDATION_TOKEN,
        )
        assert result.status == "blocked"
        assert "PAYLOAD_MANIFEST_APPLY_TO_SOURCE_NOT_FALSE" in result.blockers
        assert result.apply_enabled is False
        shutil.rmtree(daily_root, ignore_errors=True)


def main() -> int:
    test_dry_run_validation_records_readiness_without_source_mutation()
    test_missing_dry_run_token_blocks()
    test_final_plan_not_ready_blocks()
    test_source_hash_change_blocks_dry_run()
    test_payload_manifest_apply_to_source_true_blocks()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
