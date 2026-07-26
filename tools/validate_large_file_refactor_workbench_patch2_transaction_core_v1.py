# project-path: tools/validate_large_file_refactor_workbench_patch2_transaction_core_v1.py
"""Focused validator for Workbench Patch 2 durable transaction and serial lane core."""
from __future__ import annotations

import gc
import hashlib
import json
import warnings
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from kanda_reasoner_app.engineering_safety.project_mutation_lane import (
    ProjectMutationLaneStore,
    default_project_mutation_lane_database,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
    SCHEMA_VERSION,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (
    export_latest_planner_workbench_handoff,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_basis import (
    build_workbench_execution_basis_set,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_contract import (
    build_workbench_execution_contract,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_feasibility import (
    evaluate_workbench_execution_feasibility,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (
    build_workbench_plan_snapshot,
    load_workbench_plan_snapshot,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_baseline import (
    BehaviorBaselineEvidence,
    build_refactor_baseline,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_transaction import (
    detect_self_hosted_refactor,
    discover_workbench_recovery_pending,
    mark_workbench_transaction_recovery_pending,
    prepare_workbench_refactor_transaction,
    reserve_workbench_project_lane,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_store import (
    WorkbenchTransactionStore,
    default_workbench_transaction_root,
)

FEATURE_MARKER = (
    "architecture-review-large-file-refactor-workbench-patch2-"
    "durable-transaction-serial-lane-v1"
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_text(lines: int) -> str:
    body = ['"""Fixture module for durable transaction validation."""']
    for index in range(1, lines):
        body.append(f"fixture_value_{index:04d} = {index}")
    return "\n".join(body) + "\n"


def _build_snapshot(project_root: Path, target: Path):
    source_hash = _sha(target)
    symbols = [
        RefactorSymbol(
            schema_version=SCHEMA_VERSION,
            name="public_alpha",
            kind="function",
            visibility="public",
            start_line=2,
            end_line=20,
            physical_lines=19,
            assigned_module="_large_module_alpha.py",
            content_hash="alpha-hash",
        ),
        RefactorSymbol(
            schema_version=SCHEMA_VERSION,
            name="public_beta",
            kind="class",
            visibility="public",
            start_line=21,
            end_line=80,
            physical_lines=60,
            assigned_module="_large_module_beta.py",
            content_hash="beta-hash",
        ),
    ]
    modules = [
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="large_module.py",
            role="public_facade_and_coordination",
            symbols=[],
            estimated_lines=150,
            exports=["public_alpha", "public_beta"],
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_large_module_alpha.py",
            role="alpha_responsibility",
            symbols=["public_alpha"],
            estimated_lines=180,
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_large_module_beta.py",
            role="beta_responsibility",
            symbols=["public_beta"],
            estimated_lines=170,
        ),
    ]
    plan = RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        settings={},
        public_api_before=["public_alpha", "public_beta"],
        public_api_after_expected=["public_alpha", "public_beta"],
        symbols=symbols,
        atomic_clusters=["cluster-alpha", "cluster-beta"],
        proposed_modules=modules,
        import_migration={"enabled": False, "consumers": []},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )
    analysis = ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        line_count_physical=320,
        module_docstring_present=True,
        module_docstring_preview="Fixture module for durable transaction validation.",
        all_names=["public_alpha", "public_beta"],
        public_api_symbols=["public_alpha", "public_beta"],
        imports=[],
        symbols=symbols,
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
        risk_flags=[],
        analysis_errors=[],
    )
    window = SimpleNamespace(
        _large_file_refactor_last_plan=plan,
        _large_file_refactor_last_analysis=analysis,
        _large_file_refactor_planner_candidates=[SimpleNamespace(path=str(target))],
    )
    handoff = export_latest_planner_workbench_handoff(window)
    return build_workbench_plan_snapshot(handoff)


def _build_contract(project_root: Path, target: Path, test_file: Path):
    snapshot = _build_snapshot(project_root, target)
    plan = snapshot.materialize_plan()
    basis = build_workbench_execution_basis_set(
        plan=plan,
        active_project_root=str(project_root),
        api_basis_paths=[target],
        dependency_basis_paths=[target],
        validation_basis_paths=[test_file],
    )
    assert basis.status == "execution_basis_ready", basis.blockers
    feasibility = evaluate_workbench_execution_feasibility(
        plan=plan,
        execution_basis=basis,
    )
    assert feasibility.verdict == "EXECUTABLE", feasibility.blockers
    behavior = BehaviorBaselineEvidence(
        status="BEHAVIOR_BASELINE_PASS",
        collected_tests=(str(test_file),),
        exit_code=0,
        output_hash="fixture-behavior-hash",
    )
    baseline = build_refactor_baseline(
        snapshot=snapshot,
        execution_basis=basis,
        behavior_baseline=behavior,
    )
    assert baseline.integrity_valid()
    contract = build_workbench_execution_contract(
        snapshot=snapshot,
        baseline=baseline,
        execution_basis=basis,
        feasibility=feasibility,
    )
    assert contract.integrity_valid()
    assert contract.feasibility_verdict == "EXECUTABLE", contract.blocking_reasons
    return snapshot, basis, baseline, contract


def run_validation() -> None:
    with TemporaryDirectory(prefix="kanda_patch2_tx_core_") as raw:
        sandbox = Path(raw).resolve()
        project_root = sandbox / "fixture_project"
        package = project_root / "fixture_pkg"
        tests = project_root / "tests"
        package.mkdir(parents=True)
        tests.mkdir(parents=True)
        target = package / "large_module.py"
        test_file = tests / "test_large_module.py"
        target.write_text(_source_text(320), encoding="utf-8", newline="\n")
        test_file.write_text("def test_fixture():\n    assert True\n", encoding="utf-8")
        source_hash_before = _sha(target)

        snapshot, basis, baseline, contract = _build_contract(project_root, target, test_file)
        assert set(contract.final_size_map.values()) == {150, 170, 180}
        assert contract.symbol_movement_map == {
            "public_alpha": "_large_module_alpha.py",
            "public_beta": "_large_module_beta.py",
        }
        assert detect_self_hosted_refactor(project_root, project_root)
        assert not detect_self_hosted_refactor(project_root, sandbox / "other_tool")

        tx_root = default_workbench_transaction_root(project_root)
        lane_db = default_project_mutation_lane_database(project_root)
        assert not str(tx_root).startswith(str(project_root) + str(Path('/')))
        transaction_store = WorkbenchTransactionStore(tx_root)
        lane_store = ProjectMutationLaneStore(lane_db)

        tx1 = prepare_workbench_refactor_transaction(
            snapshot=snapshot,
            baseline=baseline,
            execution_basis=basis,
            contract=contract,
            transaction_store=transaction_store,
            mutation_lane_store=lane_store,
            tool_root=project_root,
        )
        tx2 = prepare_workbench_refactor_transaction(
            snapshot=snapshot,
            baseline=baseline,
            execution_basis=basis,
            contract=contract,
            transaction_store=transaction_store,
            mutation_lane_store=lane_store,
            tool_root=sandbox / "other_tool",
        )
        assert tx1.transaction_state == "PREPARED"
        assert tx1.self_hosted_refactor is True
        assert tx2.self_hosted_refactor is False
        assert tx1.source_mutation_enabled is False
        assert tx1.apply_authorized is False

        persisted_snapshot = Path(tx1.durable_transaction_root) / "planner_snapshot.json"
        reloaded = load_workbench_plan_snapshot(persisted_snapshot)
        assert reloaded.snapshot_hash == snapshot.snapshot_hash
        stored_contract = transaction_store.load_artifact(tx1.transaction_id, "EXECUTION_CONTRACT")
        assert stored_contract and stored_contract["contract_hash"] == contract.contract_hash

        tx1 = reserve_workbench_project_lane(
            transaction=tx1,
            transaction_store=transaction_store,
            mutation_lane_store=lane_store,
        )
        assert tx1.lane_state == "RESERVED"
        try:
            reserve_workbench_project_lane(
                transaction=tx2,
                transaction_store=transaction_store,
                mutation_lane_store=lane_store,
            )
        except RuntimeError as exc:
            assert str(exc) == "PROJECT_MUTATION_LANE_NOT_AVAILABLE"
        else:
            raise AssertionError("Second transaction reserved an already active project lane")

        tx1 = mark_workbench_transaction_recovery_pending(
            transaction=tx1,
            reason="forced-validator-interruption",
            transaction_store=transaction_store,
            mutation_lane_store=lane_store,
        )
        assert tx1.transaction_state == "RECOVERY_PENDING"
        restarted_tx_store = WorkbenchTransactionStore(tx_root)
        restarted_lane_store = ProjectMutationLaneStore(lane_db)
        recovery = discover_workbench_recovery_pending(
            project_root=project_root,
            transaction_store=restarted_tx_store,
            mutation_lane_store=restarted_lane_store,
        )
        assert any(item["transaction_id"] == tx1.transaction_id for item in recovery["transactions"])
        assert recovery["active_lane"]["lane_state"] == "RECOVERY_PENDING"
        assert restarted_lane_store.reserve_next(tx1.physical_project_id) is None

        restarted_lane_store.transition(tx1.mutation_request_id, "ROLLED_BACK")
        restarted_tx_store.transition_transaction(
            tx1.transaction_id,
            "ROLLBACK_VERIFIED",
            recovery_state="RESOLVED",
            rollback_state="ROLLBACK_VERIFIED",
        )
        tx2 = reserve_workbench_project_lane(
            transaction=tx2,
            transaction_store=restarted_tx_store,
            mutation_lane_store=restarted_lane_store,
        )
        assert tx2.lane_state == "RESERVED"

        operation_id = restarted_tx_store.register_operation(
            transaction_id=tx2.transaction_id,
            sequence_no=1,
            operation_type="REPLACE_FILE",
            target_path=str(target),
            precondition_hash=source_hash_before,
            payload_hash="future-payload-hash",
            backup_path=str(Path(tx2.durable_transaction_root) / "backup" / "large_module.py"),
        )
        restarted_tx_store.record_operation_intent(operation_id)
        restarted_tx_store.record_operation_applied(operation_id)
        restarted_tx_store.record_operation_verified(operation_id)
        operations = restarted_tx_store.list_operations(tx2.transaction_id)
        assert operations[0]["state"] == "VERIFIED"

        request_record = restarted_lane_store.get_request(tx2.mutation_request_id)
        assert request_record is not None
        mutation_paths = json.loads(request_record["mutation_paths_json"])
        assert all(isinstance(item, str) for item in mutation_paths)
        assert _sha(target) == source_hash_before, "Patch 2 validator detected unexpected source mutation"

        restarted_lane_store.transition(tx2.mutation_request_id, "CANCELLED")
        restarted_tx_store.transition_transaction(tx2.transaction_id, "ABANDONED")
        assert restarted_lane_store.active_owner(tx2.physical_project_id) is None

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always", ResourceWarning)
            gc.collect()
        leaked_connections = [
            str(item.message)
            for item in caught
            if isinstance(item.message, ResourceWarning)
            and "unclosed database" in str(item.message).casefold()
        ]
        assert not leaked_connections, (
            "SQLITE_CONNECTION_RESOURCE_LEAK:" + " | ".join(leaked_connections)
        )

        print("SQLITE_CONNECTION_CLOSURE: PASS")
        print("STATUS: IN_SYNC")
        print("SERIAL_LANE: PASS")
        print("RESTART_RECOVERY: PASS")
        print("SQLITE_TRANSACTION_METADATA: PASS")
        print("SNAPSHOT_PERSISTENCE: PASS")
        print("NO_SOURCE_MUTATION: PASS")
        print(f"VALIDATION OK: {FEATURE_MARKER}")


if __name__ == "__main__":
    run_validation()
