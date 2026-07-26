# project-path: tools/patch5_transaction_fixture_support.py
"""Reusable disposable-fixture builder for Patch 5 adversarial transaction validation."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_workflow import (
    CompletionEvidenceBundle,
    CompletionTransactionBundle,
    prepare_completion_evidence,
    prepare_completion_transaction,
    refresh_completion_review_state,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_preflight_backup_readiness import (
    WorkbenchPreflightBackupReadinessResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder import (
    SourceApplyPayloadReadinessResult,
)

__all__ = [
    "Patch5FixtureContext",
    "build_patch5_fixture_context",
    "payload_hashes_by_destination",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Patch5FixtureContext:
    """All disposable fixture objects needed for one independent transaction scenario."""

    project_root: Path
    target: Path
    test_file: Path
    source_hash_before: str
    snapshot: Any
    preview: Any
    preflight: WorkbenchPreflightBackupReadinessResult
    payload: SourceApplyPayloadReadinessResult
    evidence: CompletionEvidenceBundle
    transaction_bundle: CompletionTransactionBundle


def build_patch5_fixture_context(
    project_root: Path,
    *,
    shadow_suffix: str,
) -> Patch5FixtureContext:
    """Build a fully reviewed and executor-proof-enabled transaction fixture."""
    patch3 = _load_tool_module(
        "patch3_fixture_helpers_patch5",
        PROJECT_ROOT / "tools" / "validate_large_file_refactor_workbench_patch3_transformation_shadow_v1.py",
    )
    patch4 = _load_tool_module(
        "patch4_fixture_helpers_patch5",
        PROJECT_ROOT / "tools" / "validate_large_file_refactor_workbench_patch4_completion_gui_gate_v1.py",
    )
    snapshot, preview, preflight, payload, test_file, target, source_hash_before = (
        patch4._build_ready_artifacts(project_root, patch3)
    )
    behavior = patch3._baseline_behavior(project_root, test_file)
    evidence = prepare_completion_evidence(
        snapshot=snapshot,
        preview=preview,
        preflight=preflight,
        source_payload=payload,
        active_project_root=project_root,
        behavior_baseline=behavior,
        validation_basis_paths=[test_file],
        shadow_root=project_root.parent / shadow_suffix,
    )
    prepared = prepare_completion_transaction(
        snapshot=snapshot,
        evidence=evidence,
        preflight=preflight,
        source_payload=payload,
        acknowledged_warning_codes=(),
        semantic_review_confirmed=False,
        transaction_summary_confirmed=False,
        tool_root=PROJECT_ROOT,
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
        raise AssertionError("PATCH5_FIXTURE_GATE_BLOCKED:" + "|".join(reviewed.gate.blockers))
    return Patch5FixtureContext(
        project_root=project_root,
        target=target,
        test_file=test_file,
        source_hash_before=source_hash_before,
        snapshot=snapshot,
        preview=preview,
        preflight=preflight,
        payload=payload,
        evidence=evidence,
        transaction_bundle=reviewed,
    )


def sha256_file(path: Path) -> str:
    """Return exact byte SHA-256 for a fixture file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_hashes_by_destination(
    payload: SourceApplyPayloadReadinessResult,
) -> dict[str, str]:
    """Return exact destination-to-payload hash mapping for applied-state assertions."""
    return {
        str(Path(item.destination_path).resolve()): item.content_hash
        for item in payload.files
    }


def assert_payload_exact_on_disk(context: Patch5FixtureContext) -> None:
    """Assert every applied destination contains the exact source-payload bytes."""
    expected = payload_hashes_by_destination(context.payload)
    for raw_path, digest in expected.items():
        path = Path(raw_path)
        if not path.is_file():
            raise AssertionError("EXPECTED_APPLIED_FILE_MISSING:" + raw_path)
        if sha256_file(path) != digest:
            raise AssertionError("EXPECTED_APPLIED_FILE_HASH_MISMATCH:" + raw_path)


def assert_original_state(context: Patch5FixtureContext) -> None:
    """Assert original facade hash restored and generated helpers absent."""
    if sha256_file(context.target) != context.source_hash_before:
        raise AssertionError("ORIGINAL_TARGET_HASH_NOT_RESTORED")
    for item in context.payload.files:
        path = Path(item.destination_path).resolve()
        if path != context.target.resolve() and path.exists():
            raise AssertionError("GENERATED_HELPER_REMAINS_AFTER_ROLLBACK:" + str(path))


def transaction_store_root(context: Any) -> Path:
    """Return durable transaction-store root from prepared or direct fixture context."""
    if hasattr(context, "transaction_store"):
        return context.transaction_store.transaction_root
    return context.transaction_bundle.transaction_store.transaction_root


def mutation_lane_database(context: Any) -> Path:
    """Return durable project mutation lane database path."""
    if hasattr(context, "mutation_lane_store"):
        return context.mutation_lane_store.database_path
    return context.transaction_bundle.mutation_lane_store.database_path


def _load_tool_module(name: str, path: Path):
    """Load one validator as a fixture helper without requiring tools package import."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError("PATCH5_FIXTURE_HELPER_IMPORT_SPEC_FAILED:" + str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cleanup_fixture_siblings(context: Patch5FixtureContext) -> tuple[Path, ...]:
    """Return known disposable sibling roots that callers may remove after assertions."""
    root = context.project_root
    return (
        root.parent / f"{root.name}_delete_after_daily_work",
        root.parent / f"{root.name}_workbench_transactions",
    )


@dataclass(frozen=True)
class Patch5DirectContext:
    """Faster executor fixture that reuses frozen contract/seal builders without Shadow rerun."""

    project_root: Path
    target: Path
    test_file: Path
    source_hash_before: str
    snapshot: Any
    baseline: Any
    execution_basis: Any
    contract: Any
    preflight: WorkbenchPreflightBackupReadinessResult
    payload: SourceApplyPayloadReadinessResult
    sealed_payload: Any
    transaction: Any
    transaction_store: Any
    mutation_lane_store: Any


def build_patch5_direct_context(project_root: Path) -> Patch5DirectContext:
    """Build exact contract, sealed payload, and durable transaction without Shadow repetition."""
    from kanda_reasoner_app.engineering_safety.project_mutation_lane import ProjectMutationLaneStore
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_execution_basis import (
        build_workbench_execution_basis_set,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_transaction import (
        prepare_workbench_refactor_transaction,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_store import (
        WorkbenchTransactionStore,
        default_workbench_transaction_root,
    )

    patch3 = _load_tool_module(
        "patch3_direct_helpers_patch5_" + project_root.name,
        PROJECT_ROOT / "tools" / "validate_large_file_refactor_workbench_patch3_transformation_shadow_v1.py",
    )
    package = project_root / "fixture_pkg"
    tests = project_root / "tests"
    package.mkdir(parents=True)
    tests.mkdir(parents=True)
    (package / "__init__.py").write_bytes(b"\n")
    target = package / "large_module.py"
    test_file = tests / "test_large_module.py"
    target.write_bytes(patch3._source_text().encode("utf-8"))
    test_file.write_bytes(patch3._test_text().encode("utf-8"))
    source_hash_before = sha256_file(target)
    snapshot, baseline, contract = patch3._build_contract(project_root, target, test_file)
    plan = snapshot.materialize_plan()
    basis = build_workbench_execution_basis_set(
        plan=plan,
        active_project_root=str(project_root),
        api_basis_paths=[target],
        dependency_basis_paths=[target],
        validation_basis_paths=[test_file],
    )
    _risks, _recipe, sealed = patch3._build_payload_chain(project_root, snapshot, contract)
    preview_root = Path(sealed.payload_root).resolve().parent
    preflight_manifest = preview_root / "WORKBENCH_PREFLIGHT_BACKUP_READINESS.json"
    preflight_data = json.loads(preflight_manifest.read_text(encoding="utf-8"))
    preflight = WorkbenchPreflightBackupReadinessResult(**preflight_data)
    payload_manifest = Path(sealed.payload_root).parent / "SOURCE_APPLY_PAYLOAD_MANIFEST.json"
    payload_data = json.loads(payload_manifest.read_text(encoding="utf-8"))
    payload_data["files"] = [
        __import__(
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_payload_builder",
            fromlist=["SourceApplyPayloadFile"],
        ).SourceApplyPayloadFile(**item)
        for item in payload_data["files"]
    ]
    payload = SourceApplyPayloadReadinessResult(**payload_data)
    tx_root = default_workbench_transaction_root(project_root)
    store = WorkbenchTransactionStore(tx_root)
    lane = ProjectMutationLaneStore(tx_root.parent / "project_mutation_lane.sqlite3")
    transaction = prepare_workbench_refactor_transaction(
        snapshot=snapshot,
        baseline=baseline,
        execution_basis=basis,
        contract=contract,
        transaction_store=store,
        mutation_lane_store=lane,
        tool_root=PROJECT_ROOT,
    )
    return Patch5DirectContext(
        project_root=project_root,
        target=target,
        test_file=test_file,
        source_hash_before=source_hash_before,
        snapshot=snapshot,
        baseline=baseline,
        execution_basis=basis,
        contract=contract,
        preflight=preflight,
        payload=payload,
        sealed_payload=sealed,
        transaction=transaction,
        transaction_store=store,
        mutation_lane_store=lane,
    )
