"""Validate source recovery and Workbench external-mutation stale invalidation."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import shutil
from types import SimpleNamespace
import tempfile

from kanda_reasoner_app.engineering_safety.project_mutation_lane import (
    ProjectMutationLaneStore,
    build_mutation_request,
    physical_project_id,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_basis import (
    ExecutionBasisFile,
    WorkbenchExecutionBasisSet,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_external_source_stale_state import (
    EXTERNAL_SOURCE_STALE_MESSAGE,
    STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
    sync_external_source_stale_state_from_window,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_transaction import (
    WorkbenchRefactorTransaction,
    _preparation_blockers,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_store import (
    WorkbenchTransactionStore,
)

__all__ = [
    "main",
]


FEATURE_ID = (
    "workbench-external-source-stale-invalidation-recovery-v1"
)
ORIGINAL_TARGET_HASH = (
    "1aa8b65f8138d95efd5ce55c8ca7027b0604164727246df04e5499dcc9fd2406"
)
TARGET_RELATIVE = Path(
    "kanda_reasoner_app/routing_signal_scorer/similarity_runtime.py"
)
HELPERS = (
    "_similarity_runtime_serialization.py",
    "_similarity_runtime_decision_reporting.py",
    "_similarity_runtime_cohesive_operations_2.py",
)
PLANNER_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/"
    "large_file_refactor_planner"
)
TOUCHED_ENGINE_FILES = (
    "workbench_transaction_store.py",
    "workbench_refactor_transaction.py",
    "workbench_completion_gui.py",
    "external_ai_candidate_exchange_gui.py",
    "workbench_gui.py",
    "workbench_external_source_stale_state.py",
    "workbench_external_source_stale_gui.py",
)


class _IntegrityObject:
    """Tiny deterministic contract fixture."""

    def __init__(self, **values: object) -> None:
        self.__dict__.update(values)

    def integrity_valid(self) -> bool:
        """Return fixture integrity success."""
        return True


def _sha256(path: Path) -> str:
    """Return one file SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _basis(project_root: Path, target: Path) -> WorkbenchExecutionBasisSet:
    digest = _sha256(target)
    item = ExecutionBasisFile(
        path=str(target),
        role="mutation",
        exists=True,
        content_hash=digest,
        project_relative_path="target.py",
    )
    return WorkbenchExecutionBasisSet(
        schema_version="1.0",
        feature_id="fixture",
        status="execution_basis_ready",
        active_project_root=str(project_root),
        target_file=str(target),
        mutation_basis=[item],
        api_basis=[],
        dependency_basis=[],
        validation_basis=[],
        all_basis=[item],
        blockers=[],
        warnings=[],
    )


def _transaction_fixture(
    root: Path,
    project_root: Path,
    target: Path,
) -> tuple[object, WorkbenchExecutionBasisSet, WorkbenchTransactionStore, ProjectMutationLaneStore]:
    basis = _basis(project_root, target)
    transaction_store = WorkbenchTransactionStore(root / "transactions")
    lane_store = ProjectMutationLaneStore(root / "project_mutation_lane.sqlite3")
    project_id = physical_project_id(project_root)
    transaction_id = "tx-stale-fixture"
    request_id = "request-stale-fixture"

    transaction_store.create_transaction(
        transaction_id=transaction_id,
        contract_hash="contract",
        snapshot_hash="snapshot",
        baseline_hash="baseline",
        physical_project_id=project_id,
        project_root=str(project_root),
        owner_box="large_file_refactor_workbench",
        mutation_request_id=request_id,
    )
    request = build_mutation_request(
        request_id=request_id,
        project_root=project_root,
        owner_box="large_file_refactor_workbench",
        operation_family="LARGE_MODULE_REFACTOR",
        transaction_id=transaction_id,
        mutation_paths=[target],
        basis_paths=[target],
    )
    lane_store.port("large_file_refactor_workbench").submit(request)

    transaction = WorkbenchRefactorTransaction(
        schema_version="1.0",
        feature_id="fixture",
        transaction_id=transaction_id,
        contract_hash="contract",
        snapshot_hash="snapshot",
        baseline_hash="baseline",
        execution_basis_hash="basis",
        project_root=str(project_root),
        physical_project_id=project_id,
        durable_transaction_root=str(root / "transactions"),
        mutation_request_id=request_id,
        lane_state="QUEUED",
        transaction_state="PREPARED",
    )
    bundle = SimpleNamespace(
        transaction=transaction,
        transaction_store=transaction_store,
        mutation_lane_store=lane_store,
    )
    return bundle, basis, transaction_store, lane_store


def _validate_recovery_state(project_root: Path) -> None:
    target = project_root / TARGET_RELATIVE
    assert target.is_file(), "RECOVERY_TARGET_MISSING"
    assert _sha256(target) == ORIGINAL_TARGET_HASH, "RECOVERY_TARGET_HASH_MISMATCH"

    package_root = target.parent
    for helper in HELPERS:
        assert not (package_root / helper).exists(), (
            "RECOVERY_HELPER_STILL_EXISTS:" + helper
        )


def _validate_stale_invalidation() -> None:
    fixture_root = Path(tempfile.mkdtemp(prefix="kanda_stale_validation_"))
    try:
        project_root = fixture_root / "project"
        project_root.mkdir(parents=True)
        target = project_root / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")

        bundle, basis, transaction_store, lane_store = _transaction_fixture(
            fixture_root,
            project_root,
            target,
        )
        evidence = SimpleNamespace(execution_basis=basis)
        window = SimpleNamespace(
            _large_file_refactor_workbench_completion_evidence=evidence,
            _large_file_refactor_workbench_completion_transaction=bundle,
        )

        target.write_text("value = 2\n", encoding="utf-8")
        result = sync_external_source_stale_state_from_window(window)

        assert result.status == STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        assert result.stale is True
        assert result.invalidated is True
        assert result.message == EXTERNAL_SOURCE_STALE_MESSAGE
        assert any(
            item.startswith("BASIS_HASH_CHANGED:")
            for item in result.blockers
        )
        assert (
            transaction_store.get_transaction("tx-stale-fixture")["state"]
            == STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        )
        assert (
            lane_store.get_request("request-stale-fixture")["state"]
            == "CANCELLED"
        )
        assert (
            window._large_file_refactor_workbench_state
            == STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        )

        repeated = sync_external_source_stale_state_from_window(window)
        assert repeated.invalidated is True
        assert repeated.transaction_state == STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        assert repeated.lane_state == "CANCELLED"
    finally:
        shutil.rmtree(fixture_root, ignore_errors=True)


def _validate_preparation_guard() -> None:
    fixture_root = Path(tempfile.mkdtemp(prefix="kanda_stale_prepare_"))
    try:
        target = fixture_root / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")
        basis = _basis(fixture_root, target)
        target.write_text("value = 2\n", encoding="utf-8")

        snapshot = _IntegrityObject(snapshot_hash="snapshot")
        baseline = _IntegrityObject(
            snapshot_hash="snapshot",
            baseline_hash="baseline",
        )
        contract = _IntegrityObject(
            snapshot_hash="snapshot",
            baseline_hash="baseline",
            feasibility_verdict="EXECUTABLE",
            blocking_reasons=(),
        )
        blockers = _preparation_blockers(
            snapshot,
            baseline,
            basis,
            contract,
        )
        assert STALE_AFTER_EXTERNAL_SOURCE_MUTATION in blockers
        assert any(
            item.startswith("BASIS_HASH_CHANGED:")
            for item in blockers
        )
    finally:
        shutil.rmtree(fixture_root, ignore_errors=True)


def _validate_gui_contract(project_root: Path) -> None:
    planner = project_root / PLANNER_RELATIVE
    completion_text = (planner / "workbench_completion_gui.py").read_text(
        encoding="utf-8"
    )
    exchange_text = (
        planner / "external_ai_candidate_exchange_gui.py"
    ).read_text(encoding="utf-8")
    workbench_text = (planner / "workbench_gui.py").read_text(
        encoding="utf-8"
    )
    stale_gui_text = (
        planner / "workbench_external_source_stale_gui.py"
    ).read_text(encoding="utf-8")

    assert "sync_completion_external_source_stale_state(window)" in completion_text
    assert "sync_external_source_stale_state_from_window(window)" in exchange_text
    assert "and not stale_state.stale" in exchange_text
    assert "sync_completion_external_source_stale_state(window)" in workbench_text
    assert "EXTERNAL_SOURCE_STALE_MESSAGE" in stale_gui_text
    assert "Reload the card and create a fresh pipeline." in (
        planner / "workbench_external_source_stale_state.py"
    ).read_text(encoding="utf-8")
    assert "Rollback is unavailable because this Workbench transaction did " in stale_gui_text


def _validate_line_law_and_compile(project_root: Path) -> None:
    planner = project_root / PLANNER_RELATIVE
    for filename in TOUCHED_ENGINE_FILES:
        path = planner / filename
        source = path.read_text(encoding="utf-8")
        count = len(source.splitlines())
        assert 101 <= count <= 500, (
            "TOUCHED_ENGINE_LINE_LAW:" + filename + ":" + str(count)
        )
        compile(source, str(path), "exec")


def _validate_optional_real_gui_import() -> None:
    """Import touched GUI modules when PySide6 is available on the host."""
    if importlib.util.find_spec("PySide6") is None:
        print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: SKIP_UNAVAILABLE")
        return
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
        external_ai_candidate_exchange_gui,
        workbench_completion_gui,
        workbench_gui,
    )

    assert external_ai_candidate_exchange_gui is not None
    assert workbench_completion_gui is not None
    assert workbench_gui is not None
    print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: PASS")


def main() -> None:
    """Run focused recovery and stale-state validation."""
    project_root = Path(__file__).resolve().parents[1]

    _validate_recovery_state(project_root)
    print("EXACT_OLD_PROJECT_RECOVERY_BASELINE: PASS")
    print("THREE_EXTERNAL_REFACTOR_HELPERS_REMOVED: PASS")

    _validate_stale_invalidation()
    print("STALE_AFTER_EXTERNAL_SOURCE_MUTATION_CLASSIFIED: PASS")
    print("PREPARED_TRANSACTION_INVALIDATED_DURABLY: PASS")
    print("QUEUED_MUTATION_REQUEST_CANCELLED: PASS")
    print("STALE_INVALIDATION_IDEMPOTENT: PASS")

    _validate_preparation_guard()
    print("STALE_BASIS_BLOCKS_NEW_TRANSACTION_PREPARATION: PASS")

    _validate_gui_contract(project_root)
    print("COMPLETION_WORKFLOW_STALE_PROJECTION: PASS")
    print("EXTERNAL_AI_EXCHANGE_STALE_LINEAGE_BLOCKED: PASS")
    print("EXACT_RECOVERY_MESSAGE_PRESENT: PASS")

    _validate_line_law_and_compile(project_root)
    print("TOUCHED_ENGINE_LINE_LAW_101_500: PASS")
    print("TOUCHED_ENGINE_PYTHON_COMPILE: PASS")

    _validate_optional_real_gui_import()

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
