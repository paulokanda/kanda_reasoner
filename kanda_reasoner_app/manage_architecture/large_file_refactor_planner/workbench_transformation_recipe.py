# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_transformation_recipe.py
"""Deterministic transformation recipe derived from one executable Workbench contract."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .models import SCHEMA_VERSION
from .workbench_dynamic_python_risks import DynamicPythonRiskReport
from .workbench_execution_contract import WorkbenchExecutionContract
from .workbench_plan_snapshot import WorkbenchPlanSnapshot

__all__ = [
    "TRANSFORMATION_RECIPE_FEATURE_ID",
    "TransformationStep",
    "TransformationRecipe",
    "build_transformation_recipe",
    "transformation_recipe_integrity_valid",
]

TRANSFORMATION_RECIPE_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-transformation-recipe-v1"
)


@dataclass(frozen=True)
class TransformationStep:
    """One bounded deterministic transformation mechanic."""

    sequence_no: int
    operation: str
    target_module: str
    symbols: tuple[str, ...] = ()
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["symbols"] = list(self.symbols)
        return data


@dataclass(frozen=True)
class TransformationRecipe:
    """Hash-sealed mechanics for implementing, but never redesigning, a Planner plan."""

    schema_version: str
    feature_id: str
    recipe_id: str
    snapshot_hash: str
    contract_hash: str
    source_file: str
    source_content_hash: str
    transform_backend_required: str
    steps: tuple[TransformationStep, ...]
    dynamic_risk_status: str
    dynamic_risk_codes: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    recipe_hash: str
    source_mutation_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["steps"] = [item.to_dict() for item in self.steps]
        data["dynamic_risk_codes"] = list(self.dynamic_risk_codes)
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data

    def integrity_valid(self) -> bool:
        return transformation_recipe_integrity_valid(self)


def build_transformation_recipe(
    *,
    snapshot: WorkbenchPlanSnapshot,
    contract: WorkbenchExecutionContract,
    dynamic_risks: DynamicPythonRiskReport,
) -> TransformationRecipe:
    """Build exact ordered mechanics from an immutable executable contract."""
    blockers: list[str] = []
    if not snapshot.integrity_valid():
        blockers.append("WORKBENCH_SNAPSHOT_HASH_MISMATCH")
    if not contract.integrity_valid():
        blockers.append("EXECUTION_CONTRACT_HASH_MISMATCH")
    if contract.snapshot_hash != snapshot.snapshot_hash:
        blockers.append("CONTRACT_SNAPSHOT_HASH_MISMATCH")
    if contract.feasibility_verdict != "EXECUTABLE":
        blockers.append("EXECUTION_CONTRACT_NOT_EXECUTABLE")
    blockers.extend(dynamic_risks.blockers)

    plan = snapshot.materialize_plan()
    if str(Path(plan.target_file).resolve()) != str(Path(contract.target_file).resolve()):
        blockers.append("CONTRACT_TARGET_FILE_MISMATCH")
    if plan.source_content_hash != snapshot.source_content_hash:
        blockers.append("SNAPSHOT_SOURCE_HASH_MISMATCH")

    steps: list[TransformationStep] = []
    sequence = 10
    helper_modules = [module for module in plan.proposed_modules if module.role != "public_facade"]
    facade_modules = [module for module in plan.proposed_modules if module.role == "public_facade"]

    for module in helper_modules:
        symbols = tuple(str(symbol) for symbol in module.symbols)
        steps.append(
            TransformationStep(
                sequence_no=sequence,
                operation="MOVE_APPROVED_SYMBOL_CLUSTER",
                target_module=module.filename,
                symbols=symbols,
                parameters={"role": module.role, "preserve_source_order": True},
            )
        )
        sequence += 10
        steps.append(
            TransformationStep(
                sequence_no=sequence,
                operation="SYNTHESIZE_APPROVED_IMPORTS",
                target_module=module.filename,
                symbols=symbols,
                parameters={
                    "imports": list(contract.import_synthesis_plan.get(module.filename, [])),
                    "type_checking_edges_preserved": True,
                },
            )
        )
        sequence += 10

    for facade in facade_modules:
        steps.append(
            TransformationStep(
                sequence_no=sequence,
                operation="PRESERVE_PUBLIC_FACADE",
                target_module=facade.filename,
                symbols=tuple(str(symbol) for symbol in facade.symbols),
                parameters={
                    "public_api_before": list(plan.public_api_before),
                    "public_api_expected_after": list(plan.public_api_after_expected),
                },
            )
        )
        sequence += 10

    if plan.docstring_proposals:
        steps.append(
            TransformationStep(
                sequence_no=sequence,
                operation="INSERT_APPROVED_DOCSTRINGS",
                target_module=Path(plan.target_file).name,
                parameters={"proposal_count": len(plan.docstring_proposals)},
            )
        )
        sequence += 10

    if contract.consumer_rewrite_plan:
        steps.append(
            TransformationStep(
                sequence_no=sequence,
                operation="APPLY_APPROVED_CONSUMER_REWRITES",
                target_module="<consumer-set>",
                parameters={"rewrite_plan": contract.consumer_rewrite_plan},
            )
        )
        sequence += 10

    steps.append(
        TransformationStep(
            sequence_no=sequence,
            operation="VERIFY_EXACT_ARTIFACT_SET",
            target_module="<payload>",
            parameters={
                "exact_target_files": list(contract.exact_target_files),
                "final_size_map": dict(contract.final_size_map),
            },
        )
    )

    blockers.extend(_recipe_coverage_blockers(contract, steps))
    unique_blockers = tuple(sorted(set(blockers)))
    risk_codes = tuple(sorted({item.code for item in dynamic_risks.evidence}))
    recipe_id = "recipe-" + hashlib.sha256(
        f"{snapshot.snapshot_hash}|{contract.contract_hash}".encode("utf-8")
    ).hexdigest()[:20]
    provisional = TransformationRecipe(
        schema_version=SCHEMA_VERSION,
        feature_id=TRANSFORMATION_RECIPE_FEATURE_ID,
        recipe_id=recipe_id,
        snapshot_hash=snapshot.snapshot_hash,
        contract_hash=contract.contract_hash,
        source_file=str(Path(plan.target_file).resolve()),
        source_content_hash=plan.source_content_hash,
        transform_backend_required="libcst_position_extraction_and_deterministic_render",
        steps=tuple(sorted(steps, key=lambda item: item.sequence_no)),
        dynamic_risk_status=dynamic_risks.status,
        dynamic_risk_codes=risk_codes,
        blockers=unique_blockers,
        warnings=(
            "RECIPE_MAY_IMPLEMENT_ONLY_CONTRACT_APPROVED_ARCHITECTURE",
            "SOURCE_MUTATION_DISABLED",
        ),
        recipe_hash="",
        source_mutation_enabled=False,
    )
    return TransformationRecipe(
        **{**provisional.__dict__, "recipe_hash": _recipe_hash(provisional)}
    )


def transformation_recipe_integrity_valid(recipe: TransformationRecipe) -> bool:
    return bool(recipe.recipe_hash) and recipe.recipe_hash == _recipe_hash(recipe)


def _recipe_coverage_blockers(
    contract: WorkbenchExecutionContract,
    steps: list[TransformationStep],
) -> list[str]:
    movement_seen: dict[str, str] = {}
    for step in steps:
        if step.operation not in {"MOVE_APPROVED_SYMBOL_CLUSTER", "PRESERVE_PUBLIC_FACADE"}:
            continue
        for symbol in step.symbols:
            if symbol in movement_seen and movement_seen[symbol] != step.target_module:
                return [f"RECIPE_SYMBOL_DUPLICATE_DESTINATION:{symbol}"]
            movement_seen[symbol] = step.target_module
    blockers: list[str] = []
    for symbol, module in contract.symbol_movement_map.items():
        if movement_seen.get(symbol) != module:
            blockers.append(f"RECIPE_SYMBOL_COVERAGE_MISMATCH:{symbol}")
    for symbol in movement_seen:
        if symbol not in contract.symbol_movement_map:
            blockers.append(f"RECIPE_UNAPPROVED_SYMBOL:{symbol}")
    return blockers


def _recipe_hash(recipe: TransformationRecipe) -> str:
    payload = {
        "schema_version": recipe.schema_version,
        "feature_id": recipe.feature_id,
        "recipe_id": recipe.recipe_id,
        "snapshot_hash": recipe.snapshot_hash,
        "contract_hash": recipe.contract_hash,
        "source_file": recipe.source_file,
        "source_content_hash": recipe.source_content_hash,
        "transform_backend_required": recipe.transform_backend_required,
        "steps": [item.to_dict() for item in recipe.steps],
        "dynamic_risk_status": recipe.dynamic_risk_status,
        "dynamic_risk_codes": list(recipe.dynamic_risk_codes),
        "blockers": list(recipe.blockers),
        "warnings": list(recipe.warnings),
        "source_mutation_enabled": recipe.source_mutation_enabled,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
