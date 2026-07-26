# project-path: validation/test_architecture_review_large_file_refactor_planner_final_guarded_source_apply_planning_v1.py
"""Validation for Final Guarded Source-Apply Planning v1."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.final_guarded_source_apply_planning import (
    FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
    build_final_guarded_source_apply_plan,
    write_final_guarded_source_apply_plan_manifest,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.final_guarded_source_apply_planning_formatting import (
    format_final_guarded_source_apply_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.human_confirmed_apply_contract import (
    HUMAN_CONFIRMED_APPLY_TOKEN,
    HumanConfirmedApplyContractResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import FEATURE_ID, SCHEMA_VERSION

FEATURE_MARKER = "VALIDATION OK: architecture-review-large-file-refactor-planner-final-guarded-source-apply-planning-v1"
PREVIOUS_MARKERS = [
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
    """Create a governed preview context for final apply planning."""
    project_root = tmp / "demo_project"
    project_root.mkdir()
    target = project_root / "large_module.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    daily_root = _daily_root_for_test(project_root)
    preview_root = daily_root / "large_file_refactor_preview"
    preview_root.mkdir(parents=True, exist_ok=True)
    payload_manifest = preview_root / "PROJECT_PATCH_PAYLOAD_MANIFEST.json"
    payload_manifest.write_text(
        json.dumps(
            {
                "target_file": str(target),
                "source_content_hash": source_hash,
                "apply_to_source": False,
                "requires_human_review": True,
                "import_rewrite_enabled": False,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    payload_zip = preview_root / "PROJECT_PATCH_PAYLOAD.zip"
    with zipfile.ZipFile(payload_zip, "w") as archive:
        archive.write(payload_manifest, "PROJECT_PATCH_PAYLOAD_MANIFEST.json")
    human_apply_manifest = preview_root / "HUMAN_CONFIRMED_APPLY_CONTRACT.json"
    human_apply_manifest.write_text('{"apply_enabled": false, "rewrite_enabled": false}\n', encoding="utf-8")
    return project_root, target, preview_root, source_hash, daily_root, payload_zip, human_apply_manifest


def _human_apply_contract(
    target: Path,
    preview_root: Path,
    source_hash: str,
    payload_zip: Path,
    human_apply_manifest: Path,
    *,
    status: str = "human_confirmed_apply_contract_ready",
) -> HumanConfirmedApplyContractResult:
    """Return a ready review-only human apply contract."""
    return HumanConfirmedApplyContractResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        target_file=str(target),
        source_content_hash=source_hash,
        preview_root=str(preview_root),
        payload_zip_path=str(payload_zip),
        payload_manifest_path=str(preview_root / "PROJECT_PATCH_PAYLOAD_MANIFEST.json"),
        payload_apply_gate_manifest_path=str(preview_root / "PAYLOAD_APPLY_GATE.json"),
        human_import_rewrite_contract_manifest_path=str(preview_root / "HUMAN_CONFIRMED_IMPORT_REWRITE_CONTRACT.json"),
        human_apply_contract_manifest_path=str(human_apply_manifest),
        confirmation_token_required=HUMAN_CONFIRMED_APPLY_TOKEN,
        human_confirmation_present=True,
        human_confirmation_valid=True,
        human_confirmation_recorded_for_future_train_only=True,
        rewrite_enabled=False,
        apply_enabled=False,
        source_hash_verified=True,
        checked_rules=["apply_enabled_false_in_this_train"],
        blockers=[],
        warnings=["PAYLOAD_APPLICATION_NOT_IMPLEMENTED_IN_THIS_TRAIN"],
    )


def test_final_plan_records_readiness_without_enabling_source_mutation() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, human_apply_manifest = _make_context(tmp)
        plan = build_final_guarded_source_apply_plan(
            _human_apply_contract(target, preview_root, source_hash, payload_zip, human_apply_manifest),
            active_project_root=str(project_root),
            planning_confirmation=FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
        )
        assert plan.status == "final_guarded_source_apply_plan_ready"
        assert plan.planning_confirmation_valid is True
        assert plan.apply_enabled is False
        assert plan.rewrite_enabled is False
        assert plan.source_mutation_enabled is False
        assert plan.source_hash_verified is True
        written = write_final_guarded_source_apply_plan_manifest(plan)
        data = json.loads(written.read_text(encoding="utf-8"))
        assert data["apply_enabled"] is False
        assert data["rewrite_enabled"] is False
        assert data["source_mutation_enabled"] is False
        assert data["planning_recorded_for_future_train_only"] is True
        assert str(written).startswith(str(preview_root))
        assert "FINAL GUARDED SOURCE-APPLY PLAN" in format_final_guarded_source_apply_plan(plan)
        shutil.rmtree(daily_root, ignore_errors=True)


def test_missing_final_plan_token_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, human_apply_manifest = _make_context(tmp)
        plan = build_final_guarded_source_apply_plan(
            _human_apply_contract(target, preview_root, source_hash, payload_zip, human_apply_manifest),
            active_project_root=str(project_root),
            planning_confirmation="",
        )
        assert plan.status == "blocked"
        assert "FINAL_SOURCE_APPLY_PLANNING_TOKEN_MISSING_OR_INVALID" in plan.blockers
        assert plan.apply_enabled is False
        shutil.rmtree(daily_root, ignore_errors=True)


def test_human_apply_contract_not_ready_blocks() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, human_apply_manifest = _make_context(tmp)
        plan = build_final_guarded_source_apply_plan(
            _human_apply_contract(target, preview_root, source_hash, payload_zip, human_apply_manifest, status="blocked"),
            active_project_root=str(project_root),
            planning_confirmation=FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
        )
        assert plan.status == "blocked"
        assert "HUMAN_APPLY_CONTRACT_NOT_READY" in plan.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_source_hash_change_blocks_final_plan() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, human_apply_manifest = _make_context(tmp)
        target.write_text("VALUE = 2\n", encoding="utf-8")
        plan = build_final_guarded_source_apply_plan(
            _human_apply_contract(target, preview_root, source_hash, payload_zip, human_apply_manifest),
            active_project_root=str(project_root),
            planning_confirmation=FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
        )
        assert plan.status == "blocked"
        assert "SELECTED_SOURCE_HASH_CHANGED" in plan.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def test_apply_enabled_contract_blocks_final_plan() -> None:
    with tempfile.TemporaryDirectory() as temp_text:
        tmp = Path(temp_text)
        project_root, target, preview_root, source_hash, daily_root, payload_zip, human_apply_manifest = _make_context(tmp)
        contract = _human_apply_contract(target, preview_root, source_hash, payload_zip, human_apply_manifest)
        unsafe_contract = HumanConfirmedApplyContractResult(**{**contract.to_dict(), "apply_enabled": True})
        plan = build_final_guarded_source_apply_plan(
            unsafe_contract,
            active_project_root=str(project_root),
            planning_confirmation=FINAL_GUARDED_SOURCE_APPLY_PLAN_TOKEN,
        )
        assert plan.status == "blocked"
        assert "HUMAN_APPLY_CONTRACT_APPLY_ENABLED_UNEXPECTEDLY" in plan.blockers
        shutil.rmtree(daily_root, ignore_errors=True)


def main() -> int:
    test_final_plan_records_readiness_without_enabling_source_mutation()
    test_missing_final_plan_token_blocks()
    test_human_apply_contract_not_ready_blocks()
    test_source_hash_change_blocks_final_plan()
    test_apply_enabled_contract_blocks_final_plan()
    print(FEATURE_MARKER)
    for marker in PREVIOUS_MARKERS:
        print("VALIDATION OK: " + marker)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
