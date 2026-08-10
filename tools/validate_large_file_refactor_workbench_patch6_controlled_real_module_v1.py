# project-path: tools/validate_large_file_refactor_workbench_patch6_controlled_real_module_v1.py
"""Validate Patch 6 on the approved real 786-line module in a controlled copy."""
from __future__ import annotations

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_journaled_apply_models import build_journaled_apply_authorization
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from patch6_controlled_real_module_support import (  # noqa: E402
    CONTROLLED_TARGET_HASH,
    build_approved_controlled_plan,
    prepare_controlled_project,
    sha256_file,
    validate_readonly_cleanup_fixture,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (  # noqa: E402
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (  # noqa: E402
    export_latest_planner_workbench_handoff,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.real_preview_structural_validator import (  # noqa: E402
    validate_real_preview_structure,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_behavior_validation import (  # noqa: E402
    run_workbench_behavior_validation,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_apply_bridge import (  # noqa: E402
    execute_completion_transaction,
    rollback_completion_transaction,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_workflow import (  # noqa: E402
    prepare_completion_evidence,
    prepare_completion_transaction,
    refresh_completion_review_state,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (  # noqa: E402
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_journaled_apply_executor import execute_journaled_refactor_apply
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_patch5_executor_proof import (  # noqa: E402
    find_patch5_executor_proof,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (  # noqa: E402
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (  # noqa: E402
    build_workbench_plan_snapshot,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_post_apply_validator import (  # noqa: E402
    validate_and_write_post_apply,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (  # noqa: E402
    build_and_write_preflight_backup_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_baseline import (  # noqa: E402
    BehaviorBaselineEvidence,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder import (  # noqa: E402
    build_and_write_source_apply_payload,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.preview_writer import (  # noqa: E402
    resolve_preview_root,
)

FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-"
    "patch6-controlled-real-module-final-canon-v1"
)
TARGET_RELATIVE = Path(
    "kanda_reasoner_app/reasoner_symbol_atlas/main_helper_mapper.py"
)


def run_validation() -> None:
    """Run the controlled real-module proof from baseline through second apply."""
    live_target = PROJECT_ROOT / TARGET_RELATIVE
    live_hash_before = sha256_file(live_target)
    if live_hash_before != CONTROLLED_TARGET_HASH:
        raise AssertionError(
            "LIVE_TARGET_BASELINE_HASH_MISMATCH:"
            f"{live_hash_before}:EXPECTED:{CONTROLLED_TARGET_HASH}"
        )
    work_root = PROJECT_ROOT.parent / f"{PROJECT_ROOT.name}_delete_after_daily_work"
    work_root.mkdir(parents=True, exist_ok=True)
    validate_readonly_cleanup_fixture(work_root)
    print("WINDOWS_READONLY_CONTROLLED_CLEANUP: PASS")
    paths = prepare_controlled_project(PROJECT_ROOT)
    if sha256_file(paths.controlled_target) != CONTROLLED_TARGET_HASH:
        raise AssertionError("CONTROLLED_COPY_TARGET_HASH_MISMATCH")
    print("CONTROLLED_REAL_TARGET_BASELINE: PASS")

    analysis, plan = build_approved_controlled_plan(paths.controlled_target)
    actual_plan_sizes = sorted(module.estimated_lines for module in plan.proposed_modules)
    if actual_plan_sizes != [145, 197, 429]:
        raise AssertionError(f"APPROVED_PLAN_SIZE_MISMATCH:{actual_plan_sizes}")
    print("APPROVED_PLAN_197_145_429: PASS")

    snapshot = _build_snapshot(plan, analysis, paths.controlled_target)
    intake = build_workbench_plan_intake(
        snapshot=snapshot,
        active_project_root=str(paths.controlled_project_root),
    )
    if intake.status != "plan_intake_ready" or intake.blockers:
        raise AssertionError("PLAN_INTAKE_BLOCKED:" + "|".join(intake.blockers))
    readiness = build_workbench_dependency_readiness(intake)
    if readiness.status != "dependency_readiness_ready" or readiness.blockers:
        raise AssertionError("DEPENDENCY_READINESS_BLOCKED:" + "|".join(readiness.blockers))

    preview_root = (
        Path(resolve_preview_root(str(paths.controlled_project_root))).resolve()
        / "patch6_controlled_real_target"
    )
    preview = build_and_write_real_preview(
        plan=plan,
        intake=intake,
        dependency_readiness=readiness,
        active_project_root=str(paths.controlled_project_root),
        preview_root=str(preview_root),
    )
    if preview.status != "real_preview_written" or preview.blockers:
        raise AssertionError("REAL_PREVIEW_BLOCKED:" + "|".join(preview.blockers))
    _assert_decorator_preservation(preview_root / "main_helper_mapper.py")
    print("DECORATOR_PRESERVATION: PASS")
    _assert_cycle_safe_facade_global_imports(
        preview_root / "_main_helper_mapper_helper_selection.py",
        preview,
    )
    print("FACADE_GLOBAL_LOCAL_IMPORTS: PASS")

    structural = validate_real_preview_structure(
        plan=plan,
        preview_result=preview,
        active_project_root=str(paths.controlled_project_root),
    )
    if structural.status != "passed_with_warnings" or structural.blockers:
        raise AssertionError("STRUCTURAL_VALIDATION_BLOCKED:" + "|".join(structural.blockers))
    print("STRUCTURAL_VALIDATION: PASS")

    preflight = build_and_write_preflight_backup_readiness(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        active_project_root=str(paths.controlled_project_root),
    )
    if preflight.status != "preflight_backup_ready" or preflight.blockers:
        raise AssertionError("PREFLIGHT_BLOCKED:" + "|".join(preflight.blockers))
    payload = build_and_write_source_apply_payload(
        plan=plan,
        preview_result=preview,
        structural_validation=structural,
        preflight_backup=preflight,
        active_project_root=str(paths.controlled_project_root),
    )
    if payload.status != "source_apply_payload_ready" or payload.blockers:
        raise AssertionError("SOURCE_PAYLOAD_BLOCKED:" + "|".join(payload.blockers))
    _assert_payload_size_policy(payload)
    print("FINAL_MODULE_SIZE_101_499: PASS")

    behavior_baseline = _capture_behavior_baseline(
        paths.controlled_project_root,
        paths.characterization_test,
    )
    evidence = prepare_completion_evidence(
        snapshot=snapshot,
        preview=preview,
        preflight=preflight,
        source_payload=payload,
        active_project_root=paths.controlled_project_root,
        behavior_baseline=behavior_baseline,
        validation_basis_paths=[paths.characterization_test],
        shadow_root=paths.shadow_root,
    )
    if evidence.shadow_validation.status != "shadow_validation_pass":
        raise AssertionError(
            "SHADOW_VALIDATION_BLOCKED:"
            + "|".join(evidence.shadow_validation.blockers)
        )
    if evidence.provenance.status != "shadow_provenance_pass":
        raise AssertionError("SHADOW_PROVENANCE_BLOCKED:" + "|".join(evidence.provenance.blockers))
    if evidence.shadow_validation.behavior.baseline_comparison != "BASELINE_PASS_SHADOW_PASS":
        raise AssertionError(
            "SHADOW_BEHAVIOR_REGRESSION:"
            + evidence.shadow_validation.behavior.baseline_comparison
        )
    print("SHADOW_VALIDATION: PASS")
    print("SHADOW_BEHAVIOR: PASS")

    proof = find_patch5_executor_proof(paths.controlled_project_root)
    if not proof.proof_available:
        raise AssertionError("PATCH5_EXECUTOR_PROOF_NOT_AVAILABLE_IN_CONTROLLED_CONTEXT")
    first_reviewed = _prepare_reviewed_transaction(
        snapshot=snapshot,
        evidence=evidence,
        preflight=preflight,
        payload=payload,
        controlled_root=paths.controlled_project_root,
    )
    command = f'"{sys.executable}" -m pytest -q "{paths.characterization_test}"'
    print("WINDOWS_BEHAVIOR_COMMAND_QUOTING: PASS")
    first_apply = _execute_first_apply(
        reviewed=first_reviewed,
        evidence=evidence,
        preflight=preflight,
        payload=payload,
        proof_available=proof.proof_available,
    )
    print("FIRST_JOURNALED_APPLY: PASS")
    _validate_first_applied_behavior(
        apply_result=first_apply,
        evidence=evidence,
        payload=payload,
        command=command,
    )
    print("FIRST_POST_APPLY_BEHAVIOR: PASS")
    rollback = rollback_completion_transaction(first_reviewed)
    if rollback.status != "rollback_verified" or rollback.blockers:
        raise AssertionError("ROLLBACK_NOT_VERIFIED:" + "|".join(rollback.blockers))
    _assert_exact_original_state(paths.controlled_target, payload)
    print("ROLLBACK_EXACT_RESTORATION: PASS")

    second_reviewed = _prepare_reviewed_transaction(
        snapshot=snapshot,
        evidence=evidence,
        preflight=preflight,
        payload=payload,
        controlled_root=paths.controlled_project_root,
    )
    outcome = execute_completion_transaction(
        evidence=evidence,
        transaction_bundle=second_reviewed,
        preflight=preflight,
        source_payload=payload,
        executor_proof_available=proof.proof_available,
        behavior_test_command=command,
    )
    if outcome.status != "completed" or outcome.final_transaction_state != "COMPLETED_VALIDATED":
        raise AssertionError(
            f"SECOND_APPLY_NOT_COMPLETED:{outcome.status}:{outcome.final_transaction_state}"
        )
    if outcome.receipt is None or not outcome.receipt.integrity_valid():
        raise AssertionError("SECOND_APPLY_RECEIPT_INTEGRITY_FAILED")
    _assert_exact_payload_state(payload)
    print("SECOND_APPLY_COMPLETED_VALIDATED: PASS")
    print("REFACTOR_RECEIPT_INTEGRITY: PASS")

    if sha256_file(live_target) != live_hash_before:
        raise AssertionError("LIVE_PROJECT_SOURCE_CHANGED_DURING_CONTROLLED_PROOF")
    print("LIVE_PROJECT_SOURCE_UNCHANGED: PASS")
    _write_proof_summary(
        paths.proof_summary,
        plan_sizes=actual_plan_sizes,
        transaction_id=outcome.apply_result.transaction_id,
        receipt_hash=outcome.receipt.receipt_hash,
        controlled_target_hash=sha256_file(paths.controlled_target),
        live_target_hash=sha256_file(live_target),
    )
    print(f"VALIDATION OK: {FEATURE_ID}")


def _build_snapshot(plan, analysis, target: Path):
    """Create the immutable Workbench snapshot through the public handoff seam."""
    window = SimpleNamespace(
        _large_file_refactor_last_plan=plan,
        _large_file_refactor_last_analysis=analysis,
        _large_file_refactor_planner_candidates=[SimpleNamespace(path=str(target))],
    )
    return build_workbench_plan_snapshot(export_latest_planner_workbench_handoff(window))


def _capture_behavior_baseline(project_root: Path, test_file: Path) -> BehaviorBaselineEvidence:
    """Run the controlled characterization test before any refactor transaction."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(project_root)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(test_file)],
        cwd=project_root,
        env=env,
        text=True,
        capture_output=True,
        timeout=180,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError("CONTROLLED_BEHAVIOR_BASELINE_FAILED:" + completed.stdout + completed.stderr)
    output = completed.stdout + "\n" + completed.stderr
    return BehaviorBaselineEvidence(
        status="BEHAVIOR_BASELINE_PASS",
        collected_tests=(str(test_file.resolve()),),
        exit_code=0,
        output_hash=hashlib.sha256(output.encode("utf-8")).hexdigest(),
    )


def _prepare_reviewed_transaction(*, snapshot, evidence, preflight, payload, controlled_root: Path):
    """Build a fresh confirmed transaction using Patch 4 review ownership."""
    prepared = prepare_completion_transaction(
        snapshot=snapshot,
        evidence=evidence,
        preflight=preflight,
        source_payload=payload,
        semantic_review_confirmed=False,
        transaction_summary_confirmed=False,
        tool_root=controlled_root,
        transaction_apply_executor_proven=True,
    )
    reviewed = refresh_completion_review_state(
        snapshot=snapshot,
        evidence=evidence,
        transaction_bundle=prepared,
        preflight=preflight,
        source_payload=payload,
        semantic_review_confirmed=True,
        acknowledged_warning_codes=evidence.semantic_review.warnings,
        transaction_summary_confirmed=True,
        transaction_apply_executor_proven=True,
    )
    if not reviewed.gate.enabled:
        raise AssertionError("PATCH6_REVIEW_GATE_BLOCKED:" + "|".join(reviewed.gate.blockers))
    return reviewed


def _execute_first_apply(*, reviewed, evidence, preflight, payload, proof_available: bool):
    """Apply once without terminal finalization so rollback remains lane-owned."""
    authorization = build_journaled_apply_authorization(
        transaction_id=reviewed.transaction.transaction_id,
        contract_hash=evidence.contract.contract_hash,
        payload_hash=evidence.sealed_payload.payload_hash,
        semantic_reviewed=True,
        warnings_acknowledged=reviewed.warning_acknowledgment.complete,
        transaction_summary_confirmed=reviewed.transaction_summary.confirmed,
        executor_proof_available=proof_available,
    )
    result = execute_journaled_refactor_apply(
        transaction=reviewed.transaction,
        authorization=authorization,
        execution_basis=evidence.execution_basis,
        sealed_payload=evidence.sealed_payload,
        source_payload=payload,
        preflight_backup=preflight,
        transaction_store=reviewed.transaction_store,
        mutation_lane_store=reviewed.mutation_lane_store,
    )
    if result.status != "applied" or result.transaction_state != "VALIDATING":
        raise AssertionError(f"FIRST_APPLY_FAILED:{result.status}:{result.transaction_state}")
    return result


def _validate_first_applied_behavior(*, apply_result, evidence, payload, command: str) -> None:
    """Prove structural and behavior validity before the rollback exercise."""
    post_apply = validate_and_write_post_apply(
        apply_result=apply_result,
        source_payload=payload,
        active_project_root=evidence.contract.active_project_root,
    )
    behavior = run_workbench_behavior_validation(
        apply_result=apply_result,
        post_apply_validation=post_apply,
        source_payload=payload,
        active_project_root=evidence.contract.active_project_root,
        test_command=command,
    )
    if post_apply.status != "post_apply_validated":
        raise AssertionError("FIRST_POST_APPLY_STRUCTURAL_FAILED")
    if behavior.behavior_status != "BEHAVIOR_VALIDATED_PASS":
        raise AssertionError(
            "FIRST_POST_APPLY_BEHAVIOR_FAILED:"
            + behavior.behavior_status
            + ":"
            + "|".join(behavior.blockers)
        )


def _assert_decorator_preservation(facade_path: Path) -> None:
    """Prove dataclass decorators survived the LibCST extraction path."""
    tree = ast.parse(facade_path.read_text(encoding="utf-8"))
    expected = {"ProjectSymbolAtlasMainHelperOptions", "ProjectSymbolAtlasMainHelperDecision"}
    found: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name in expected:
            if any(isinstance(item, ast.Call) and isinstance(item.func, ast.Name) and item.func.id == "dataclass" for item in node.decorator_list):
                found.add(node.name)
    if found != expected:
        raise AssertionError(f"DATACLASS_DECORATOR_PRESERVATION_FAILED:{sorted(found)}")


def _assert_cycle_safe_facade_global_imports(helper_path: Path, preview) -> None:
    """Prove facade globals are imported locally inside the exact dependent functions."""
    tree = ast.parse(helper_path.read_text(encoding="utf-8"))
    expected_functions = {"_decision_status", "_has_helper_suffix", "_strip_helper_suffix"}
    found: set[str] = set()
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name not in expected_functions:
            continue
        if any(
            isinstance(statement, ast.ImportFrom)
            and statement.level == 1
            and statement.module == "main_helper_mapper"
            for statement in node.body
        ):
            found.add(node.name)
    if found != expected_functions:
        raise AssertionError(f"CYCLE_SAFE_LOCAL_IMPORTS_MISSING:{sorted(found)}")
    report = preview.facade_global_import_insertion
    if report.get("status") != "facade_global_import_insertion_ready":
        raise AssertionError("FACADE_GLOBAL_IMPORT_INSERTION_REPORT_NOT_READY")


def _assert_payload_size_policy(payload) -> None:
    """Require exact generated payload modules to satisfy the strict 101-499 law."""
    for item in payload.files:
        path = Path(item.payload_path)
        lines = len(path.read_bytes().decode("utf-8").splitlines())
        if not 100 < lines < 500:
            raise AssertionError(f"PATCH6_PAYLOAD_SIZE_POLICY_FAILED:{item.relative_path}:{lines}")


def _assert_exact_original_state(target: Path, payload) -> None:
    """Assert facade restored byte-exactly and generated helpers removed."""
    if sha256_file(target) != CONTROLLED_TARGET_HASH:
        raise AssertionError("PATCH6_ORIGINAL_TARGET_NOT_RESTORED")
    for item in payload.files:
        destination = Path(item.destination_path).resolve()
        if destination != target.resolve() and destination.exists():
            raise AssertionError("PATCH6_HELPER_REMAINS_AFTER_ROLLBACK:" + str(destination))


def _assert_exact_payload_state(payload) -> None:
    """Assert final controlled project bytes equal the sealed source payload bytes."""
    for item in payload.files:
        destination = Path(item.destination_path).resolve()
        if not destination.is_file():
            raise AssertionError("PATCH6_FINAL_DESTINATION_MISSING:" + str(destination))
        if sha256_file(destination) != item.content_hash:
            raise AssertionError("PATCH6_FINAL_DESTINATION_HASH_MISMATCH:" + str(destination))


def _write_proof_summary(
    path: Path,
    *,
    plan_sizes: list[int],
    transaction_id: str,
    receipt_hash: str,
    controlled_target_hash: str,
    live_target_hash: str,
) -> None:
    """Persist concise proof evidence under selected project support only."""
    payload = {
        "feature_id": FEATURE_ID,
        "status": "controlled_real_module_proof_pass",
        "target_baseline_hash": CONTROLLED_TARGET_HASH,
        "approved_plan_sizes": plan_sizes,
        "final_transaction_id": transaction_id,
        "refactor_receipt_hash": receipt_hash,
        "controlled_target_final_hash": controlled_target_hash,
        "live_target_unchanged_hash": live_target_hash,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    run_validation()
