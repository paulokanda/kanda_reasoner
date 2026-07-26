# project-path: tools/validate_large_file_refactor_workbench_patch5_journaled_apply_v1.py
"""Adversarial validator for Patch 5 journaled apply, recovery, and rollback proof."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from kanda_reasoner_app.engineering_safety.project_mutation_lane import (
    ProjectMutationLaneStore,
    build_mutation_request,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_apply_bridge import (
    execute_completion_transaction,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_journaled_apply_executor import (
    build_journaled_apply_authorization,
    execute_journaled_refactor_apply,
    finalize_journaled_refactor_transaction,
    resume_journaled_refactor_apply,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_patch5_executor_proof import (
    PATCH5_EXECUTOR_PROOF_FEATURE_ID,
    PATCH5_FREEZE_FEATURE_TITLE,
    find_patch5_executor_proof,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_receipt import (
    build_and_write_refactor_receipt,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_rollback import (
    rollback_journaled_refactor_transaction,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_store import (
    WorkbenchTransactionStore,
)
from patch5_transaction_fixture_support import (
    assert_original_state,
    assert_payload_exact_on_disk,
    build_patch5_direct_context,
    build_patch5_fixture_context,
    cleanup_fixture_siblings,
    mutation_lane_database,
    payload_hashes_by_destination,
    sha256_file,
    transaction_store_root,
)

FEATURE_ID = PATCH5_EXECUTOR_PROOF_FEATURE_ID


def _direct_authorization(context):
    return build_journaled_apply_authorization(
        transaction_id=context.transaction.transaction_id,
        contract_hash=context.contract.contract_hash,
        payload_hash=context.sealed_payload.payload_hash,
        semantic_reviewed=True,
        warnings_acknowledged=True,
        transaction_summary_confirmed=True,
        executor_proof_available=True,
    )


def _direct_apply(context, failure_injection: str = ""):
    return execute_journaled_refactor_apply(
        transaction=context.transaction,
        authorization=_direct_authorization(context),
        execution_basis=context.execution_basis,
        sealed_payload=context.sealed_payload,
        source_payload=context.payload,
        preflight_backup=context.preflight,
        transaction_store=context.transaction_store,
        mutation_lane_store=context.mutation_lane_store,
        failure_injection=failure_injection,
    )


def _scenario_success(root: Path) -> None:
    context = build_patch5_fixture_context(root, shadow_suffix="patch5_success_shadow")
    outcome = execute_completion_transaction(
        evidence=context.evidence,
        transaction_bundle=context.transaction_bundle,
        preflight=context.preflight,
        source_payload=context.payload,
        executor_proof_available=True,
        behavior_test_command="",
    )
    assert outcome.status == "completed", outcome.to_dict()
    assert outcome.final_transaction_state == "COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED"
    assert outcome.post_apply and outcome.post_apply.status == "post_apply_validated"
    assert outcome.receipt and outcome.receipt.integrity_valid()
    assert_payload_exact_on_disk(context)
    operations = context.transaction_bundle.transaction_store.list_operations(context.transaction_bundle.transaction.transaction_id)
    assert operations and {item["state"] for item in operations} == {"VERIFIED"}
    assert context.transaction_bundle.mutation_lane_store.active_owner(
        context.transaction_bundle.transaction.physical_project_id
    ) is None


def _scenario_basis_drift(root: Path) -> None:
    context = build_patch5_direct_context(root)
    original_hash = sha256_file(context.target)
    context.test_file.write_text(
        context.test_file.read_text(encoding="utf-8") + "\n# external drift\n",
        encoding="utf-8",
    )
    result = _direct_apply(context)
    assert result.status == "blocked", result.to_dict()
    assert any("BASIS_HASH_CHANGED" in item for item in result.blockers), result.blockers
    assert sha256_file(context.target) == original_hash
    for item in context.payload.files:
        destination = Path(item.destination_path)
        if destination != context.target:
            assert not destination.exists()


def _scenario_failure_rollback_and_serial_lane(root: Path) -> None:
    context = build_patch5_direct_context(root)
    result = _direct_apply(context, "after_write:2")
    assert result.status == "recovery_pending", result.to_dict()
    active = context.mutation_lane_store.active_owner(context.transaction.physical_project_id)
    assert active and active["lane_state"] == "RECOVERY_PENDING"
    second = build_mutation_request(
        request_id=context.transaction.transaction_id + "-second-request",
        project_root=context.project_root,
        owner_box="patch5_adversarial_second_box",
        operation_family="TEST_SERIAL_BLOCK",
        transaction_id=context.transaction.transaction_id + "-second",
        mutation_paths=[context.target],
        basis_paths=[context.target],
    )
    context.mutation_lane_store.port("patch5_adversarial_second_box").submit(second)
    assert context.mutation_lane_store.reserve_next(context.transaction.physical_project_id) is None
    rollback = rollback_journaled_refactor_transaction(
        transaction_id=context.transaction.transaction_id,
        transaction_store=context.transaction_store,
        mutation_lane_store=context.mutation_lane_store,
    )
    assert rollback.status == "rollback_verified", rollback.to_dict()
    assert_original_state(context)
    receipt = build_and_write_refactor_receipt(
        transaction_id=context.transaction.transaction_id,
        transaction_store=context.transaction_store,
    )
    assert receipt.integrity_valid()


def _scenario_rollback_conflict(root: Path) -> None:
    context = build_patch5_direct_context(root)
    result = _direct_apply(context, "after_write:2")
    assert result.status == "recovery_pending"
    operations = context.transaction_store.list_operations(context.transaction.transaction_id)
    drift_target = Path(operations[0]["target_path"])
    drift_target.write_bytes(b"# external edit after interrupted transaction\n")
    rollback = rollback_journaled_refactor_transaction(
        transaction_id=context.transaction.transaction_id,
        transaction_store=context.transaction_store,
        mutation_lane_store=context.mutation_lane_store,
    )
    assert rollback.status == "rollback_conflict", rollback.to_dict()
    assert any("ROLLBACK_CONFLICT_EXTERNAL_DRIFT" in item for item in rollback.blockers)
    active = context.mutation_lane_store.active_owner(context.transaction.physical_project_id)
    assert active and active["lane_state"] == "RECOVERY_PENDING"


def _scenario_freeze_proof(root: Path) -> None:
    before = find_patch5_executor_proof(root)
    assert not before.proof_available
    entries = (
        root.parent
        / f"{root.name}_show_project_to_AI"
        / "project_freeze_after_update"
        / "frozen_features_memory"
        / "entries"
    )
    entries.mkdir(parents=True)
    entry = entries / "freeze-20260705-large-file-refactor-workbench-patch-5-journaled-apply-and-adversarial-transaction-proof.md"
    entry.write_text(
        f'''---\nstatus: "frozen"\n---\n# {PATCH5_FREEZE_FEATURE_TITLE}\n\nfeature_id: {FEATURE_ID}\n\nJournaled sealed payload apply with rollback and recovery proof.\n''',
        encoding="utf-8",
    )
    after = find_patch5_executor_proof(root)
    assert after.proof_available, after.blockers


def _hard_crash_child(project_root: Path, marker: Path) -> None:
    project_root.mkdir(parents=True, exist_ok=True)
    context = build_patch5_direct_context(project_root)
    marker.write_text(
        json.dumps(
            {
                "transaction_id": context.transaction.transaction_id,
                "transaction_root": str(transaction_store_root(context)),
                "lane_database": str(mutation_lane_database(context)),
                "target_file": str(context.target),
                "expected": payload_hashes_by_destination(context.payload),
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _direct_apply(context, "hard_exit_after_write:1")
    raise AssertionError("HARD_EXIT_INJECTION_DID_NOT_EXIT")


def _scenario_hard_crash_restart(root: Path) -> None:
    marker = root / "_hard_crash_marker.json"
    completed = subprocess.run(
        [sys.executable, str(Path(__file__).resolve()), "--hard-crash-child", str(root), str(marker)],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    assert completed.returncode == 97, completed.stdout + completed.stderr
    data = json.loads(marker.read_text(encoding="utf-8"))
    store = WorkbenchTransactionStore(data["transaction_root"])
    lane = ProjectMutationLaneStore(data["lane_database"])
    tx_id = data["transaction_id"]
    tx = store.get_transaction(tx_id)
    assert tx and tx["state"] == "EXECUTING"
    operations = store.list_operations(tx_id)
    assert operations[0]["state"] == "INTENT_RECORDED"
    resumed = resume_journaled_refactor_apply(
        transaction_id=tx_id,
        transaction_store=store,
        mutation_lane_store=lane,
    )
    assert resumed.status == "applied", resumed.to_dict()
    assert {item["state"] for item in store.list_operations(tx_id)} == {"VERIFIED"}
    for raw_path, digest in data["expected"].items():
        assert sha256_file(Path(raw_path)) == digest
    terminal = finalize_journaled_refactor_transaction(
        result=resumed,
        structural_pass=True,
        behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
        behavior_risk_accepted=True,
        transaction_store=store,
        mutation_lane_store=lane,
    )
    assert terminal == "COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED"
    assert lane.active_owner(tx["physical_project_id"]) is None


def _validate_changed_file_sizes() -> None:
    relative = [
        "kanda_reasoner_app/engineering_safety/project_mutation_lane.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_source_mutation_primitives.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_models.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_support.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_executor.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_transaction_rollback.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_patch5_executor_proof.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_apply_bridge.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_refactor_receipt.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_review.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_gui.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_guarded_source_apply.py",
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_post_apply_validator.py",
        "tools/patch5_transaction_fixture_support.py",
        "tools/validate_large_file_refactor_workbench_patch5_journaled_apply_v1.py",
    ]
    for item in relative:
        path = PROJECT_ROOT / item
        lines = len(path.read_bytes().splitlines())
        assert 100 < lines < 500, f"SIZE_POLICY:{item}:{lines}"


def run_validation() -> None:
    created_roots: list[Path] = []
    with TemporaryDirectory(prefix="kanda_patch5_adversarial_") as raw:
        sandbox = Path(raw).resolve()
        prefix = f"kanda_patch5_{sandbox.name}"
        roots = {
            name: Path(sandbox.anchor) / f"{prefix}_{name}"
            for name in ("success", "drift", "rollback", "conflict", "proof", "crash")
        }
        created_roots.extend(roots.values())
        try:
            _scenario_success(roots["success"])
            _scenario_basis_drift(roots["drift"])
            _scenario_failure_rollback_and_serial_lane(roots["rollback"])
            _scenario_rollback_conflict(roots["conflict"])
            _scenario_freeze_proof(roots["proof"])
            _scenario_hard_crash_restart(roots["crash"])
        finally:
            for root in created_roots:
                shutil.rmtree(root, ignore_errors=True)
                shutil.rmtree(root.parent / f"{root.name}_delete_after_daily_work", ignore_errors=True)
                shutil.rmtree(root.parent / f"{root.name}_workbench_transactions", ignore_errors=True)
                shutil.rmtree(root.parent / f"{root.name}_show_project_to_AI", ignore_errors=True)
                marker = root / "_hard_crash_marker.json"
                if marker.exists():
                    marker.unlink()
                for shadow in root.parent.glob(f"patch5_*_shadow"):
                    shutil.rmtree(shadow, ignore_errors=True)
    _validate_changed_file_sizes()
    print("FINAL_BASIS_RECHECK: PASS")
    print("EXACT_SEALED_PAYLOAD_REAL_APPLY: PASS")
    print("OPERATION_INTENT_APPLIED_VERIFIED_JOURNAL: PASS")
    print("SERIAL_LANE_RECOVERY_CLOSURE: PASS")
    print("SOFT_FAILURE_ROLLBACK_EXACT_RESTORATION: PASS")
    print("ROLLBACK_EXTERNAL_DRIFT_CONFLICT: PASS")
    print("HARD_CRASH_RESTART_RECOVERY: PASS")
    print("REFACTOR_RECEIPT: PASS")
    print("PATCH5_CANONICAL_FREEZE_PROOF_GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--hard-crash-child":
        _hard_crash_child(Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
    else:
        run_validation()
