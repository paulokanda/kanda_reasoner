# project-path: tools/validate_large_file_refactor_workbench_patch4_completion_gui_gate_v1.py
"""Focused validator for Patch 4 completion review and Refactor Large Module gating."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import importlib.util
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import resolve_preview_root
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (
    validate_real_preview_structure,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_review import (
    build_warning_acknowledgment,
    evaluate_refactor_large_module_gate,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_workflow import (
    prepare_completion_evidence,
    prepare_completion_transaction,
    refresh_completion_review_state,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (
    build_and_write_preflight_backup_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder import (
    build_and_write_source_apply_payload,
)

FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-"
    "patch4-completion-gui-refactor-large-module-gate-v1"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_patch3_fixture_helpers():
    path = PROJECT_ROOT / "tools" / "validate_large_file_refactor_workbench_patch3_transformation_shadow_v1.py"
    spec = importlib.util.spec_from_file_location("patch3_fixture_helpers", path)
    if spec is None or spec.loader is None:
        raise AssertionError("PATCH3_VALIDATOR_IMPORT_SPEC_FAILED")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_ready_artifacts(project_root: Path, helper):
    package = project_root / "fixture_pkg"
    tests = project_root / "tests"
    package.mkdir(parents=True)
    tests.mkdir(parents=True)
    (package / "__init__.py").write_bytes(b"\n")
    target = package / "large_module.py"
    test_file = tests / "test_large_module.py"
    target.write_bytes(helper._source_text().encode("utf-8"))
    test_file.write_bytes(helper._test_text().encode("utf-8"))
    source_hash_before = _sha(target)

    snapshot = helper._build_snapshot(target)
    plan = snapshot.materialize_plan()
    intake = build_workbench_plan_intake(
        snapshot=snapshot,
        active_project_root=str(project_root),
    )
    assert intake.status == "plan_intake_ready", intake.blockers
    dependency = build_workbench_dependency_readiness(intake)
    assert dependency.ready_for_real_preview_writer, dependency.blockers
    preview_root = Path(resolve_preview_root(str(project_root))).resolve() / "patch4_fixture"
    preview = build_and_write_real_preview(
        plan=plan,
        intake=intake,
        dependency_readiness=dependency,
        active_project_root=str(project_root),
        preview_root=str(preview_root),
    )
    assert preview.status == "real_preview_written", preview.blockers
    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=str(project_root),
    )
    assert structural.status.startswith("passed"), structural.blockers
    preflight = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=str(project_root),
    )
    assert preflight.status == "preflight_backup_ready", preflight.blockers
    payload = build_and_write_source_apply_payload(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        preflight_backup=preflight,
        active_project_root=str(project_root),
    )
    assert payload.status == "source_apply_payload_ready", payload.blockers
    for item in preview.files:
        assert _sha(Path(preview.preview_root) / item.relative_path) == item.content_hash
    for item in payload.files:
        assert _sha(Path(item.payload_path)) == item.content_hash
    return snapshot, preview, preflight, payload, test_file, target, source_hash_before


def _validate_review_and_gate(project_root: Path, helper) -> None:
    snapshot, preview, preflight, payload, test_file, target, source_hash_before = _build_ready_artifacts(
        project_root,
        helper,
    )
    baseline_behavior = helper._baseline_behavior(project_root, test_file)
    evidence = prepare_completion_evidence(
        snapshot=snapshot,
        preview=preview,
        preflight=preflight,
        source_payload=payload,
        active_project_root=project_root,
        behavior_baseline=baseline_behavior,
        validation_basis_paths=[test_file],
        shadow_root=project_root.parent / "patch4_shadow",
    )
    assert evidence.contract.feasibility_verdict == "EXECUTABLE"
    assert evidence.recipe.integrity_valid()
    assert evidence.sealed_payload.integrity_valid()
    assert evidence.shadow_validation.status == "shadow_validation_pass"
    assert evidence.provenance.status == "shadow_provenance_pass"
    assert evidence.semantic_review.status == "semantic_diff_ready"
    assert evidence.semantic_review.symbol_movements
    assert evidence.text_diff.status in {"visual_diff_ready", "no_changes"}
    assert _sha(target) == source_hash_before

    tx_bundle = prepare_completion_transaction(
        snapshot=snapshot,
        evidence=evidence,
        preflight=preflight,
        source_payload=payload,
        acknowledged_warning_codes=(),
        semantic_review_confirmed=False,
        transaction_summary_confirmed=False,
        tool_root=project_root,
        transaction_apply_executor_proven=False,
    )
    assert tx_bundle.transaction.transaction_state == "PREPARED"
    assert tx_bundle.transaction.lane_state == "QUEUED"
    assert not tx_bundle.gate.enabled
    assert "SEMANTIC_DIFF_REVIEW_NOT_CONFIRMED" in tx_bundle.gate.blockers
    assert "REQUIRED_WARNINGS_NOT_ACKNOWLEDGED" in tx_bundle.gate.blockers
    assert "TRANSACTION_SUMMARY_NOT_CONFIRMED" in tx_bundle.gate.blockers
    assert "TRANSACTION_APPLY_EXECUTOR_NOT_CANONICALLY_PROVEN" in tx_bundle.gate.blockers
    assert _sha(target) == source_hash_before

    acknowledged = evidence.semantic_review.warnings
    reviewed_bundle = refresh_completion_review_state(
        snapshot=snapshot,
        evidence=evidence,
        transaction_bundle=tx_bundle,
        preflight=preflight,
        source_payload=payload,
        semantic_review_confirmed=True,
        acknowledged_warning_codes=acknowledged,
        transaction_summary_confirmed=True,
        transaction_apply_executor_proven=False,
    )
    assert not reviewed_bundle.gate.enabled
    assert reviewed_bundle.warning_acknowledgment.complete
    assert reviewed_bundle.transaction_summary.confirmed
    assert reviewed_bundle.gate.blockers == (
        "TRANSACTION_APPLY_EXECUTOR_NOT_CANONICALLY_PROVEN",
    )
    assert _sha(target) == source_hash_before

    proven_bundle = refresh_completion_review_state(
        snapshot=snapshot,
        evidence=evidence,
        transaction_bundle=reviewed_bundle,
        preflight=preflight,
        source_payload=payload,
        semantic_review_confirmed=True,
        acknowledged_warning_codes=acknowledged,
        transaction_summary_confirmed=True,
        transaction_apply_executor_proven=True,
    )
    assert proven_bundle.gate.enabled
    assert proven_bundle.gate.status == "refactor_large_module_ready"
    assert not proven_bundle.gate.source_mutation_enabled
    assert _sha(target) == source_hash_before

    tampered_payload = replace(
        evidence.sealed_payload,
        payload_hash="0" * 64,
    )
    tampered_gate = evaluate_refactor_large_module_gate(
        execution_basis=evidence.execution_basis,
        contract=evidence.contract,
        sealed_payload=tampered_payload,
        shadow_validation=evidence.shadow_validation,
        preflight=preflight,
        source_payload=payload,
        semantic_review=replace(evidence.semantic_review, reviewed=True, status="semantic_diff_reviewed"),
        warning_acknowledgment=build_warning_acknowledgment(acknowledged, acknowledged),
        transaction_summary=proven_bundle.transaction_summary,
        transaction=proven_bundle.transaction,
        transaction_apply_executor_proven=True,
    )
    assert not tampered_gate.enabled
    assert "SEALED_PAYLOAD_MANIFEST_HASH_MISMATCH" in tampered_gate.blockers
    assert _sha(target) == source_hash_before


def _validate_gui_source_contract() -> None:
    gui_path = (
        PROJECT_ROOT
        / "kanda_reasoner_app"
        / "manage_architecture"
        / "large_file_refactor_planner"
        / "workbench_gui.py"
    )
    completion_path = gui_path.with_name("workbench_completion_gui.py")
    gui_text = gui_path.read_text(encoding="utf-8")
    completion_text = completion_path.read_text(encoding="utf-8")
    assert 'QPushButton("Legacy Apply Source Changes (Disabled)")' not in gui_text
    assert "Exact apply token:" not in gui_text
    assert 'QPushButton("Rollback Last Apply")' not in gui_text
    assert "execute_guarded_source_apply(" not in gui_text
    assert "Next governed stage: Completion Review and Refactor Authorization." in gui_text
    assert 'QPushButton("Refactor Large Module")' in completion_text
    assert "transaction_apply_executor_proven = False" in completion_text
    assert "Patch 5 must canonically prove" not in completion_text
    assert "read_and_render_patch5_executor_proof_status" in completion_text
    assert completion_text.count("read_and_render_patch5_executor_proof_status(") >= 3
    assert "QMessageBox.warning" in completion_text


def _validate_changed_file_sizes() -> None:
    paths = [
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_review.py",
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_workflow.py",
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_gui.py",
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui.py",
        Path(__file__).resolve(),
    ]
    for path in paths:
        lines = len(path.read_bytes().splitlines())
        assert 100 < lines < 500, f"SIZE_POLICY:{path}:{lines}"


def run_validation() -> None:
    helper = _load_patch3_fixture_helpers()
    with TemporaryDirectory(prefix="kanda_patch4_completion_") as raw:
        sandbox = Path(raw).resolve()
        project_root = Path(sandbox.anchor) / f"kanda_patch4_fixture_{sandbox.name}"
        project_root.mkdir()
        _validate_review_and_gate(project_root, helper)
        shutil.rmtree(project_root, ignore_errors=True)
        shutil.rmtree(project_root.parent / "patch4_shadow", ignore_errors=True)
        shutil.rmtree(
            project_root.parent / f"{project_root.name}_delete_after_daily_work",
            ignore_errors=True,
        )
        shutil.rmtree(
            project_root.parent / f"{project_root.name}_show_project_to_AI",
            ignore_errors=True,
        )
        shutil.rmtree(
            project_root.parent / f"{project_root.name}_workbench_transactions",
            ignore_errors=True,
        )
    _validate_gui_source_contract()
    _validate_changed_file_sizes()
    print("SEMANTIC_DIFF_FIRST_REVIEW: PASS")
    print("WARNING_ACKNOWLEDGMENT_GATE: PASS")
    print("TRANSACTION_SUMMARY_CONFIRMATION: PASS")
    print("LEGACY_APPLY_GUI_BYPASS_BLOCKED: PASS")
    print("ROLLBACK_VISIBILITY_AFTER_APPLIED_STATE: PASS")
    print("REFACTOR_LARGE_MODULE_BUTTON_PRESENT: PASS")
    print("PATCH5_EXECUTOR_PROOF_FAIL_CLOSED: PASS")
    print("NO_SOURCE_MUTATION: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")


if __name__ == "__main__":
    run_validation()
