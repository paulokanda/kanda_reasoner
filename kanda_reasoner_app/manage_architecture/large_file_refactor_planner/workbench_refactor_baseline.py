# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_refactor_baseline.py
"""Durable BEFORE-state evidence for one Workbench-owned Planner snapshot."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION
from .workbench_execution_basis import WorkbenchExecutionBasisSet
from .workbench_plan_snapshot import WorkbenchPlanSnapshot

__all__ = [
    "WORKBENCH_REFACTOR_BASELINE_FEATURE_ID",
    "BehaviorBaselineEvidence",
    "RefactorBaseline",
    "build_refactor_baseline",
]

WORKBENCH_REFACTOR_BASELINE_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-refactor-baseline-v1"
)


@dataclass(frozen=True)
class BehaviorBaselineEvidence:
    """Explicit behavior evidence captured before transformation."""

    status: str
    collected_tests: tuple[str, ...] = ()
    exit_code: int | None = None
    output_hash: str = ""
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["collected_tests"] = list(self.collected_tests)
        data["warnings"] = list(self.warnings)
        return data


@dataclass(frozen=True)
class RefactorBaseline:
    """Immutable baseline compared with shadow and post-apply evidence."""

    schema_version: str
    feature_id: str
    baseline_id: str
    snapshot_hash: str
    execution_basis_hash: str
    target_file: str
    source_hash_map: dict[str, str]
    physical_size_map: dict[str, int]
    public_api_manifest: dict[str, Any]
    topology_evidence: dict[str, Any]
    dynamic_risk_inventory: tuple[str, ...]
    related_tests: tuple[str, ...]
    behavior_baseline: BehaviorBaselineEvidence
    baseline_hash: str
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["dynamic_risk_inventory"] = list(self.dynamic_risk_inventory)
        data["related_tests"] = list(self.related_tests)
        data["behavior_baseline"] = self.behavior_baseline.to_dict()
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data

    def integrity_valid(self) -> bool:
        return self.baseline_hash == _baseline_hash(self)


def build_refactor_baseline(
    *,
    snapshot: WorkbenchPlanSnapshot,
    execution_basis: WorkbenchExecutionBasisSet,
    behavior_baseline: BehaviorBaselineEvidence | None = None,
) -> RefactorBaseline:
    """Build the authoritative BEFORE state without reading mutable Planner GUI state."""
    blockers: list[str] = []
    if not snapshot.integrity_valid():
        blockers.append("WORKBENCH_SNAPSHOT_HASH_MISMATCH")
    if execution_basis.status != "execution_basis_ready":
        blockers.append("EXECUTION_BASIS_NOT_READY")
    plan = snapshot.materialize_plan()
    analysis = snapshot.materialize_analysis()
    source_hash_map = {
        item.path: item.content_hash
        for item in execution_basis.all_basis
        if item.exists
    }
    physical_size_map = {
        item.path: _physical_lines(Path(item.path))
        for item in execution_basis.all_basis
        if item.exists and Path(item.path).suffix == ".py"
    }
    public_api_manifest = {
        "module_path": plan.target_file,
        "explicit_all": list(analysis.all_names),
        "public_symbols": list(analysis.public_api_symbols),
        "expected_after": list(plan.public_api_after_expected),
        "known_external_importers": _external_importers(analysis.symbols),
    }
    topology_evidence = {
        "atomic_clusters": list(plan.atomic_clusters),
        "planned_modules": [
            {
                "filename": module.filename,
                "role": module.role,
                "symbols": list(module.symbols),
                "imports": list(module.imports),
            }
            for module in plan.proposed_modules
        ],
        "import_migration": dict(plan.import_migration),
    }
    dynamic_risks = sorted(
        set(
            analysis.risk_flags
            + plan.risks
            + _dynamic_analysis_flags(analysis)
        )
    )
    related_tests = tuple(
        sorted(
            item.path
            for item in execution_basis.validation_basis
            if item.exists
        )
    )
    behavior = behavior_baseline or BehaviorBaselineEvidence(
        status="BEHAVIOR_BASELINE_NOT_RUN",
        warnings=("BEHAVIOR_BASELINE_REQUIRED_BEFORE_FINAL_AUTHORIZATION",),
    )
    basis_hash = _execution_basis_hash(execution_basis)
    baseline_id = "baseline-" + hashlib.sha256(
        f"{snapshot.snapshot_hash}|{basis_hash}".encode("utf-8")
    ).hexdigest()[:20]
    provisional = RefactorBaseline(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_REFACTOR_BASELINE_FEATURE_ID,
        baseline_id=baseline_id,
        snapshot_hash=snapshot.snapshot_hash,
        execution_basis_hash=basis_hash,
        target_file=plan.target_file,
        source_hash_map=source_hash_map,
        physical_size_map=physical_size_map,
        public_api_manifest=public_api_manifest,
        topology_evidence=topology_evidence,
        dynamic_risk_inventory=tuple(dynamic_risks),
        related_tests=related_tests,
        behavior_baseline=behavior,
        baseline_hash="",
        blockers=tuple(sorted(set(blockers))),
        warnings=(
            "BASELINE_IS_BEFORE_STATE_EVIDENCE_NOT_SOURCE_APPLY_AUTHORIZATION",
        ),
    )
    return RefactorBaseline(
        **{
            **provisional.__dict__,
            "baseline_hash": _baseline_hash(provisional),
        }
    )


def _baseline_hash(baseline: RefactorBaseline) -> str:
    payload = {
        "schema_version": baseline.schema_version,
        "feature_id": baseline.feature_id,
        "baseline_id": baseline.baseline_id,
        "snapshot_hash": baseline.snapshot_hash,
        "execution_basis_hash": baseline.execution_basis_hash,
        "target_file": baseline.target_file,
        "source_hash_map": baseline.source_hash_map,
        "physical_size_map": baseline.physical_size_map,
        "public_api_manifest": baseline.public_api_manifest,
        "topology_evidence": baseline.topology_evidence,
        "dynamic_risk_inventory": list(baseline.dynamic_risk_inventory),
        "related_tests": list(baseline.related_tests),
        "behavior_baseline": baseline.behavior_baseline.to_dict(),
        "blockers": list(baseline.blockers),
        "warnings": list(baseline.warnings),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _execution_basis_hash(basis: WorkbenchExecutionBasisSet) -> str:
    canonical = json.dumps(
        basis.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _physical_lines(path: Path) -> int:
    try:
        return len(path.read_bytes().splitlines())
    except OSError:
        return 0


def _external_importers(symbols: list[object]) -> list[str]:
    values: set[str] = set()
    for symbol in symbols:
        values.update(str(item) for item in getattr(symbol, "external_importers", []) if str(item))
    return sorted(values)


def _dynamic_analysis_flags(analysis: object) -> list[str]:
    flags: list[str] = []
    all_names = list(getattr(analysis, "all_names", []))
    assignments = set(getattr(analysis, "assignments", []))
    calls = [str(item) for item in getattr(analysis, "module_level_calls", [])]
    if "__all__" in assignments and not all_names:
        flags.append("DYNAMIC_ALL_REQUIRES_REVIEW")
    if "__getattr__" in {getattr(item, "name", "") for item in getattr(analysis, "symbols", [])}:
        flags.append("MODULE_GETATTR_DYNAMIC_API")
    if "__dir__" in {getattr(item, "name", "") for item in getattr(analysis, "symbols", [])}:
        flags.append("MODULE_DIR_DYNAMIC_API")
    if getattr(analysis, "global_statements", []):
        flags.append("MODULE_GLOBAL_STATE_USAGE")
    if calls:
        flags.append("MODULE_LEVEL_CALL_SIDE_EFFECT_REVIEW")
    return flags
