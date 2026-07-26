"""Validate Workbench external source stale invalidation lifecycle logic."""

from __future__ import annotations

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
    detect_external_source_stale_state,
    sync_external_source_stale_state_from_window,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_transaction import (
    WorkbenchRefactorTransaction,
    _preparation_blockers,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_store import (
    WorkbenchTransactionStore,
)

FEATURE_ID = "workbench-external-source-stale-invalidation-logic-v1"
PLANNER_RELATIVE = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
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


class _Button:
    """Minimal enablement fixture for stale GUI static behavior checks."""

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def setEnabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)


class _Output:
    """Minimal text output fixture."""

    def __init__(self) -> None:
        self.text = ""

    def setPlainText(self, text: str) -> None:
        self.text = str(text)


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


def _sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def _window(bundle: object, basis: WorkbenchExecutionBasisSet) -> SimpleNamespace:
    return SimpleNamespace(
        _large_file_refactor_workbench_completion_evidence=SimpleNamespace(
            execution_basis=basis
        ),
        _large_file_refactor_workbench_completion_transaction=bundle,
    )


def _validate_fresh_prepared_state() -> None:
    root = Path(tempfile.mkdtemp(prefix="kanda_stale_fresh_"))
    try:
        project = root / "project"
        project.mkdir()
        target = project / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")
        bundle, basis, tx_store, lane_store = _transaction_fixture(
            root, project, target
        )
        result = sync_external_source_stale_state_from_window(
            _window(bundle, basis)
        )
        assert result.status == "EXECUTION_BASIS_FRESH"
        assert result.stale is False
        assert tx_store.get_transaction("tx-stale-fixture")["state"] == "PREPARED"
        assert lane_store.get_request("request-stale-fixture")["state"] == "QUEUED"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _validate_prepared_stale_invalidation() -> None:
    root = Path(tempfile.mkdtemp(prefix="kanda_stale_prepared_"))
    try:
        project = root / "project"
        project.mkdir()
        target = project / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")
        bundle, basis, tx_store, lane_store = _transaction_fixture(
            root, project, target
        )
        window = _window(bundle, basis)
        target.write_text("value = 2\n", encoding="utf-8")

        result = sync_external_source_stale_state_from_window(window)
        assert result.status == STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        assert result.stale is True
        assert result.invalidated is True
        assert result.message == EXTERNAL_SOURCE_STALE_MESSAGE
        assert any(item.startswith("BASIS_HASH_CHANGED:") for item in result.blockers)
        assert tx_store.get_transaction("tx-stale-fixture")["state"] == (
            STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        )
        assert lane_store.get_request("request-stale-fixture")["state"] == "CANCELLED"
        artifact = tx_store.load_artifact(
            "tx-stale-fixture",
            "EXTERNAL_SOURCE_STALE_INVALIDATION",
        )
        assert artifact is not None
        assert artifact["status"] == STALE_AFTER_EXTERNAL_SOURCE_MUTATION

        repeated = sync_external_source_stale_state_from_window(window)
        assert repeated.invalidated is True
        assert repeated.transaction_state == STALE_AFTER_EXTERNAL_SOURCE_MUTATION
        assert repeated.lane_state == "CANCELLED"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _validate_workbench_owned_completed_state_not_stale() -> None:
    root = Path(tempfile.mkdtemp(prefix="kanda_stale_completed_"))
    try:
        project = root / "project"
        project.mkdir()
        target = project / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")
        bundle, basis, tx_store, lane_store = _transaction_fixture(
            root, project, target
        )
        request_id = "request-stale-fixture"
        lane_store.transition(request_id, "RESERVED")
        lane_store.transition(request_id, "EXECUTING")
        lane_store.transition(request_id, "VALIDATING")
        lane_store.transition(request_id, "COMPLETED")
        tx_store.transition_transaction(
            "tx-stale-fixture",
            "COMPLETED_VALIDATED",
            rollback_state="ROLLBACK_AVAILABLE",
        )
        target.write_text("value = 2\n", encoding="utf-8")

        result = sync_external_source_stale_state_from_window(
            _window(bundle, basis)
        )
        assert result.stale is False
        assert result.status == (
            "WORKBENCH_TRANSACTION_OWNS_OR_RETIRES_SOURCE_CHANGE"
        )
        assert result.transaction_state == "COMPLETED_VALIDATED"
        assert result.lane_state == "COMPLETED"
        assert tx_store.get_transaction("tx-stale-fixture")["state"] == (
            "COMPLETED_VALIDATED"
        )
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _validate_recovery_pending_state_not_stale() -> None:
    root = Path(tempfile.mkdtemp(prefix="kanda_stale_recovery_"))
    try:
        project = root / "project"
        project.mkdir()
        target = project / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")
        bundle, basis, tx_store, lane_store = _transaction_fixture(
            root, project, target
        )
        request_id = "request-stale-fixture"
        lane_store.transition(request_id, "RESERVED")
        lane_store.transition(request_id, "EXECUTING")
        lane_store.transition(request_id, "RECOVERY_PENDING")
        tx_store.transition_transaction(
            "tx-stale-fixture",
            "RECOVERY_PENDING",
            rollback_state="ROLLBACK_AVAILABLE",
        )
        target.write_text("value = 2\n", encoding="utf-8")

        result = sync_external_source_stale_state_from_window(
            _window(bundle, basis)
        )
        assert result.stale is False
        assert result.transaction_state == "RECOVERY_PENDING"
        assert result.lane_state == "RECOVERY_PENDING"
        assert tx_store.get_transaction("tx-stale-fixture")["rollback_state"] == (
            "ROLLBACK_AVAILABLE"
        )
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _validate_unowned_stale_basis_classification() -> None:
    root = Path(tempfile.mkdtemp(prefix="kanda_stale_unowned_"))
    try:
        target = root / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")
        basis = _basis(root, target)
        target.write_text("value = 2\n", encoding="utf-8")
        result = detect_external_source_stale_state(
            execution_basis=basis,
            transaction_bundle=None,
        )
        assert result.stale is True
        assert result.invalidated is False
        assert result.status == STALE_AFTER_EXTERNAL_SOURCE_MUTATION
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _validate_preparation_guard() -> None:
    root = Path(tempfile.mkdtemp(prefix="kanda_stale_prepare_"))
    try:
        target = root / "target.py"
        target.write_text("value = 1\n", encoding="utf-8")
        basis = _basis(root, target)
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
        blockers = _preparation_blockers(snapshot, baseline, basis, contract)
        assert STALE_AFTER_EXTERNAL_SOURCE_MUTATION in blockers
        assert any(item.startswith("BASIS_HASH_CHANGED:") for item in blockers)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _validate_gui_contract(project_root: Path) -> None:
    planner = project_root / PLANNER_RELATIVE
    completion_text = (planner / "workbench_completion_gui.py").read_text(
        encoding="utf-8"
    )
    exchange_text = (
        planner / "external_ai_candidate_exchange_gui.py"
    ).read_text(encoding="utf-8")
    workbench_text = (planner / "workbench_gui.py").read_text(encoding="utf-8")
    stale_gui_text = (
        planner / "workbench_external_source_stale_gui.py"
    ).read_text(encoding="utf-8")
    stale_state_text = (
        planner / "workbench_external_source_stale_state.py"
    ).read_text(encoding="utf-8")

    assert "sync_completion_external_source_stale_state(window)" in completion_text
    assert "sync_external_source_stale_state_from_window(window)" in exchange_text
    assert "and not stale_state.stale" in exchange_text
    assert "sync_completion_external_source_stale_state(window)" in workbench_text
    assert "EXTERNAL_SOURCE_STALE_MESSAGE" in stale_gui_text
    assert "Reload the card and create a fresh pipeline." in stale_state_text
    assert "_WORKBENCH_OWNED_OR_RETIRED_STATES" in stale_state_text
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
    """Run focused stale-lifecycle validation."""
    project_root = Path(__file__).resolve().parents[1]

    _validate_fresh_prepared_state()
    print("FRESH_PREPARED_TRANSACTION_REMAINS_ACTIVE: PASS")

    _validate_prepared_stale_invalidation()
    print("STALE_AFTER_EXTERNAL_SOURCE_MUTATION_CLASSIFIED: PASS")
    print("PREPARED_TRANSACTION_INVALIDATED_DURABLY: PASS")
    print("QUEUED_MUTATION_REQUEST_CANCELLED: PASS")
    print("STALE_INVALIDATION_ARTIFACT_RECORDED: PASS")
    print("STALE_INVALIDATION_IDEMPOTENT: PASS")

    _validate_workbench_owned_completed_state_not_stale()
    print("WORKBENCH_OWNED_COMPLETED_STATE_NOT_MISCLASSIFIED: PASS")

    _validate_recovery_pending_state_not_stale()
    print("RECOVERY_PENDING_ROLLBACK_OWNERSHIP_PRESERVED: PASS")

    _validate_unowned_stale_basis_classification()
    print("UNOWNED_STALE_BASIS_CLASSIFIED_READ_ONLY: PASS")

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
