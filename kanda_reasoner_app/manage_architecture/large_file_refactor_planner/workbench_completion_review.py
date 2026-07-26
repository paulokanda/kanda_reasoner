# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_review.py
"""Semantic review, warning acknowledgment, summary, and final button gating."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .models import SCHEMA_VERSION
from .workbench_completion_payload_evidence import (
    plan_size_estimate_warnings,
    sealed_payload_dependency_warnings,
    sealed_payload_import_map,
    sealed_payload_size_map,
)
from .visual_diff_ui import (
    VisualDiffReport,
    build_multi_file_visual_diff_report,
    build_visual_diff_report,
)
from .workbench_execution_basis import WorkbenchExecutionBasisSet, execution_basis_is_fresh
from .workbench_execution_contract import WorkbenchExecutionContract
from .workbench_preflight_backup_readiness import WorkbenchPreflightBackupReadinessResult
from .workbench_refactor_baseline import RefactorBaseline
from .workbench_refactor_transaction import WorkbenchRefactorTransaction
from .workbench_sealed_payload import WorkbenchSealedPayload, verify_sealed_payload
from .workbench_shadow_validation import ShadowValidationResult
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult

__all__ = [
    "WORKBENCH_COMPLETION_REVIEW_FEATURE_ID",
    "SemanticDiffReview",
    "WarningAcknowledgment",
    "TransactionSummary",
    "RefactorLargeModuleGate",
    "build_semantic_diff_review",
    "build_text_diff_review",
    "build_warning_acknowledgment",
    "build_transaction_summary",
    "evaluate_refactor_large_module_gate",
    "format_semantic_diff_review",
    "format_transaction_summary",
    "format_refactor_large_module_gate",
]

WORKBENCH_COMPLETION_REVIEW_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-completion-review-v1"
)


@dataclass(frozen=True)
class SemanticDiffReview:
    """Human-facing semantic change evidence derived from frozen execution artifacts."""

    schema_version: str
    feature_id: str
    status: str
    contract_hash: str
    payload_hash: str
    symbol_movements: tuple[tuple[str, str], ...]
    size_before: tuple[tuple[str, int], ...]
    size_after: tuple[tuple[str, int], ...]
    imports_after: tuple[tuple[str, tuple[str, ...]], ...]
    public_api_before: tuple[str, ...]
    public_api_after: tuple[str, ...]
    dependency_graph: tuple[tuple[str, tuple[str, ...]], ...]
    consumer_rewrites: tuple[tuple[str, str], ...]
    warnings: tuple[str, ...]
    blockers: tuple[str, ...]
    reviewed: bool = False
    source_mutation_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in (
            "symbol_movements",
            "size_before",
            "size_after",
            "imports_after",
            "dependency_graph",
            "consumer_rewrites",
        ):
            data[key] = [list(item) for item in getattr(self, key)]
        data["warnings"] = list(self.warnings)
        data["blockers"] = list(self.blockers)
        return data


@dataclass(frozen=True)
class WarningAcknowledgment:
    """Explicit acknowledgment evidence for all review warnings requiring judgment."""

    required_codes: tuple[str, ...]
    acknowledged_codes: tuple[str, ...]
    missing_codes: tuple[str, ...]
    complete: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "required_codes": list(self.required_codes),
            "acknowledged_codes": list(self.acknowledged_codes),
            "missing_codes": list(self.missing_codes),
            "complete": self.complete,
        }


@dataclass(frozen=True)
class TransactionSummary:
    """Stable human review summary immediately before future real mutation."""

    status: str
    transaction_id: str
    transaction_state: str
    lane_state: str
    project_root: str
    files_to_create: tuple[str, ...]
    files_to_replace: tuple[str, ...]
    files_to_delete: tuple[str, ...]
    consumer_rewrites: tuple[str, ...]
    backup_snapshot_path: str
    payload_hash: str
    shadow_status: str
    behavior_status: str
    warnings: tuple[str, ...]
    blockers: tuple[str, ...]
    confirmed: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in (
            "files_to_create",
            "files_to_replace",
            "files_to_delete",
            "consumer_rewrites",
            "warnings",
            "blockers",
        ):
            data[key] = list(getattr(self, key))
        return data


@dataclass(frozen=True)
class RefactorLargeModuleGate:
    """Fail-closed button gate computed only from immutable execution evidence."""

    status: str
    enabled: bool
    blockers: tuple[str, ...]
    checked_rules: tuple[str, ...]
    source_mutation_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["blockers"] = list(self.blockers)
        data["checked_rules"] = list(self.checked_rules)
        return data


def build_semantic_diff_review(
    *,
    baseline: RefactorBaseline,
    contract: WorkbenchExecutionContract,
    sealed_payload: WorkbenchSealedPayload,
    shadow_validation: ShadowValidationResult,
    reviewed: bool = False,
) -> SemanticDiffReview:
    """Build semantic-first review evidence without reading mutable Planner GUI state."""
    blockers: list[str] = []
    if not baseline.integrity_valid():
        blockers.append("REFACTOR_BASELINE_HASH_MISMATCH")
    if not contract.integrity_valid():
        blockers.append("EXECUTION_CONTRACT_HASH_MISMATCH")
    payload_valid, payload_blockers = verify_sealed_payload(sealed_payload)
    if not payload_valid:
        blockers.extend(payload_blockers)
    if shadow_validation.status != "shadow_validation_pass":
        blockers.append("SHADOW_VALIDATION_NOT_PASS")
        blockers.extend(shadow_validation.blockers)
    movements = tuple(sorted(contract.symbol_movement_map.items(), key=lambda item: item[0].casefold()))
    before_sizes = tuple(sorted(baseline.physical_size_map.items(), key=lambda item: item[0].casefold()))
    after_sizes = sealed_payload_size_map(sealed_payload)
    imports = sealed_payload_import_map(sealed_payload)
    graph = tuple(sorted(shadow_validation.dependency_graph.items(), key=lambda item: item[0].casefold()))
    rewrites = tuple(
        sorted(
            (str(key), str(value))
            for key, value in contract.consumer_rewrite_plan.items()
        )
    )
    warnings = tuple(
        sorted(
            set(
                (
                    *baseline.warnings,
                    *contract.warnings,
                    *sealed_payload.warnings,
                    *shadow_validation.warnings,
                    *plan_size_estimate_warnings(contract.final_size_map, sealed_payload),
                    *sealed_payload_dependency_warnings(
                        sealed_payload,
                        target_file=contract.target_file,
                    ),
                )
            )
        )
    )
    unique_blockers = tuple(sorted(set(blockers)))
    status = "semantic_diff_reviewed" if reviewed and not unique_blockers else (
        "semantic_diff_ready" if not unique_blockers else "blocked"
    )
    return SemanticDiffReview(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_COMPLETION_REVIEW_FEATURE_ID,
        status=status,
        contract_hash=contract.contract_hash,
        payload_hash=sealed_payload.payload_hash,
        symbol_movements=movements,
        size_before=before_sizes,
        size_after=after_sizes,
        imports_after=imports,
        public_api_before=tuple(shadow_validation.api_before),
        public_api_after=tuple(shadow_validation.api_after),
        dependency_graph=graph,
        consumer_rewrites=rewrites,
        warnings=warnings,
        blockers=unique_blockers,
        reviewed=bool(reviewed and not unique_blockers),
    )


def build_text_diff_review(
    *,
    contract: WorkbenchExecutionContract,
    sealed_payload: WorkbenchSealedPayload,
) -> VisualDiffReport:
    """Build secondary text diff from source bytes to sealed facade bytes."""
    comparisons: list[tuple[str, str, str, str]] = []
    for item in sorted(sealed_payload.files, key=lambda value: value.relative_path.casefold()):
        destination = Path(item.destination_path).resolve()
        source_text = (
            destination.read_bytes().decode("utf-8")
            if destination.is_file()
            else ""
        )
        target_text = Path(item.payload_path).resolve().read_bytes().decode("utf-8")
        comparisons.append(
            (
                source_text,
                target_text,
                str(destination),
                item.relative_path,
            )
        )
    if not comparisons:
        return build_visual_diff_report(
            "",
            "",
            source_label=str(Path(contract.target_file).resolve()),
            target_label="sealed-payload-empty",
            max_rows=1,
        )
    return build_multi_file_visual_diff_report(comparisons)


def build_warning_acknowledgment(
    required_codes: Iterable[str],
    acknowledged_codes: Iterable[str],
) -> WarningAcknowledgment:
    """Return normalized all-or-nothing warning acknowledgment evidence."""
    required = tuple(sorted({str(item) for item in required_codes if str(item).strip()}))
    acknowledged = tuple(sorted({str(item) for item in acknowledged_codes if str(item).strip()}))
    missing = tuple(sorted(set(required) - set(acknowledged)))
    return WarningAcknowledgment(
        required_codes=required,
        acknowledged_codes=acknowledged,
        missing_codes=missing,
        complete=not missing,
    )


def build_transaction_summary(
    *,
    transaction: WorkbenchRefactorTransaction,
    contract: WorkbenchExecutionContract,
    sealed_payload: WorkbenchSealedPayload,
    shadow_validation: ShadowValidationResult,
    preflight: WorkbenchPreflightBackupReadinessResult,
    confirmed: bool = False,
) -> TransactionSummary:
    """Build exact transaction summary from the contract and sealed payload."""
    blockers: list[str] = list(transaction.blockers)
    if transaction.contract_hash != contract.contract_hash:
        blockers.append("TRANSACTION_CONTRACT_HASH_MISMATCH")
    if shadow_validation.payload_hash != sealed_payload.payload_hash:
        blockers.append("SHADOW_PAYLOAD_HASH_MISMATCH")
    if preflight.status != "preflight_backup_ready":
        blockers.append("PREFLIGHT_BACKUP_NOT_READY")
    create: list[str] = []
    replace: list[str] = []
    for item in sealed_payload.files:
        destination = Path(item.destination_path)
        (replace if destination.exists() else create).append(str(destination.resolve()))
    deletes: list[str] = []
    consumer_rewrites = tuple(sorted(str(key) for key in contract.consumer_rewrite_plan))
    warnings = tuple(sorted(set((*transaction.warnings, *shadow_validation.warnings))))
    unique_blockers = tuple(sorted(set(blockers)))
    status = "transaction_summary_confirmed" if confirmed and not unique_blockers else (
        "transaction_summary_ready" if not unique_blockers else "blocked"
    )
    return TransactionSummary(
        status=status,
        transaction_id=transaction.transaction_id,
        transaction_state=transaction.transaction_state,
        lane_state=transaction.lane_state,
        project_root=transaction.project_root,
        files_to_create=tuple(sorted(create, key=str.casefold)),
        files_to_replace=tuple(sorted(replace, key=str.casefold)),
        files_to_delete=tuple(deletes),
        consumer_rewrites=consumer_rewrites,
        backup_snapshot_path=preflight.backup_snapshot_path,
        payload_hash=sealed_payload.payload_hash,
        shadow_status=shadow_validation.status,
        behavior_status=shadow_validation.behavior.baseline_comparison,
        warnings=warnings,
        blockers=unique_blockers,
        confirmed=bool(confirmed and not unique_blockers),
    )


def evaluate_refactor_large_module_gate(
    *,
    execution_basis: WorkbenchExecutionBasisSet,
    contract: WorkbenchExecutionContract,
    sealed_payload: WorkbenchSealedPayload,
    shadow_validation: ShadowValidationResult,
    preflight: WorkbenchPreflightBackupReadinessResult,
    source_payload: SourceApplyPayloadReadinessResult,
    semantic_review: SemanticDiffReview,
    warning_acknowledgment: WarningAcknowledgment,
    transaction_summary: TransactionSummary | None,
    transaction: WorkbenchRefactorTransaction | None,
    transaction_apply_executor_proven: bool,
) -> RefactorLargeModuleGate:
    """Evaluate the final button from evidence, never from widget state alone."""
    blockers: list[str] = []
    fresh, freshness_blockers = execution_basis_is_fresh(execution_basis)
    if not fresh:
        blockers.extend(freshness_blockers)
    if contract.feasibility_verdict != "EXECUTABLE" or not contract.integrity_valid():
        blockers.append("EXECUTION_CONTRACT_NOT_EXECUTABLE_OR_VALID")
    valid_payload, payload_blockers = verify_sealed_payload(sealed_payload)
    if not valid_payload:
        blockers.extend(payload_blockers)
    if shadow_validation.status != "shadow_validation_pass":
        blockers.append("SHADOW_VALIDATION_NOT_PASS")
    if shadow_validation.payload_hash != sealed_payload.payload_hash:
        blockers.append("SHADOW_PAYLOAD_HASH_MISMATCH")
    if preflight.status != "preflight_backup_ready":
        blockers.append("PREFLIGHT_BACKUP_NOT_READY")
    if source_payload.status != "source_apply_payload_ready":
        blockers.append("SOURCE_APPLY_PAYLOAD_NOT_READY")
    blockers.extend(_sealed_source_payload_mismatches(sealed_payload, source_payload))
    if not semantic_review.reviewed:
        blockers.append("SEMANTIC_DIFF_REVIEW_NOT_CONFIRMED")
    if not warning_acknowledgment.complete:
        blockers.append("REQUIRED_WARNINGS_NOT_ACKNOWLEDGED")
    if transaction is None or transaction.transaction_state != "PREPARED":
        blockers.append("WORKBENCH_TRANSACTION_NOT_PREPARED")
    if transaction_summary is None or not transaction_summary.confirmed:
        blockers.append("TRANSACTION_SUMMARY_NOT_CONFIRMED")
    if not transaction_apply_executor_proven:
        blockers.append("TRANSACTION_APPLY_EXECUTOR_NOT_CANONICALLY_PROVEN")
    unique = tuple(sorted(set(blockers)))
    return RefactorLargeModuleGate(
        status="refactor_large_module_ready" if not unique else "blocked",
        enabled=not unique,
        blockers=unique,
        checked_rules=(
            "execution_basis_fresh",
            "execution_contract_executable_and_hash_valid",
            "sealed_payload_exact_and_untampered",
            "shadow_validation_passes_same_payload_hash",
            "preflight_backup_ready",
            "source_payload_matches_sealed_payload",
            "semantic_diff_human_reviewed",
            "all_required_warnings_acknowledged",
            "transaction_prepared",
            "transaction_summary_human_confirmed",
            "canonical_transaction_apply_executor_proven",
        ),
    )


def _sealed_source_payload_mismatches(
    sealed_payload: WorkbenchSealedPayload,
    source_payload: SourceApplyPayloadReadinessResult,
) -> list[str]:
    sealed = {
        str(Path(item.destination_path).resolve()): item.content_hash
        for item in sealed_payload.files
    }
    source = {
        str(Path(item.destination_path).resolve()): item.content_hash
        for item in source_payload.files
    }
    blockers: list[str] = []
    if set(sealed) != set(source):
        blockers.append("SOURCE_PAYLOAD_DESTINATION_SET_DIFFERS_FROM_SEAL")
    for path in sorted(set(sealed) & set(source), key=str.casefold):
        if sealed[path] != source[path]:
            blockers.append("SOURCE_PAYLOAD_HASH_DIFFERS_FROM_SEAL:" + path)
    return blockers


def format_semantic_diff_review(review: SemanticDiffReview) -> str:
    """Return a compact semantic-first human review rendering."""
    lines = ["Semantic Diff Review", "====================", f"status: {review.status}"]
    lines.extend(["", "Symbol movements:"])
    lines.extend(f"- {symbol} -> {module}" for symbol, module in review.symbol_movements)
    lines.extend(["", "Resulting sizes (sealed payload truth):"])
    lines.extend(f"- {path}: {size}" for path, size in review.size_after)
    lines.extend(["", "Exact sealed imports:"])
    for module, imports in review.imports_after:
        lines.append(f"- {module}:")
        lines.extend(f"  - {item}" for item in imports or ("none",))
    lines.extend(["", "Exact local dependency graph:"])
    for module, dependencies in review.dependency_graph:
        lines.append(f"- {module}: {list(dependencies)}")
    lines.extend(["", "Public API:", f"- before: {list(review.public_api_before)}", f"- after: {list(review.public_api_after)}"])
    lines.extend(["", "Warnings:"])
    lines.extend(f"- {item}" for item in review.warnings or ("none",))
    lines.extend(["", "Blockers:"])
    lines.extend(f"- {item}" for item in review.blockers or ("none",))
    lines.append(f"\nhuman_reviewed: {str(review.reviewed).lower()}")
    return "\n".join(lines)


def format_transaction_summary(summary: TransactionSummary) -> str:
    """Return compact pre-authorization transaction summary text."""
    lines = ["Transaction Summary", "===================", f"status: {summary.status}"]
    lines.extend([
        f"transaction_id: {summary.transaction_id}",
        f"transaction_state: {summary.transaction_state}",
        f"lane_state: {summary.lane_state}",
        f"files_to_create: {len(summary.files_to_create)}",
        f"files_to_replace: {len(summary.files_to_replace)}",
        f"files_to_delete: {len(summary.files_to_delete)}",
        f"consumer_rewrites: {len(summary.consumer_rewrites)}",
        f"backup_snapshot: {summary.backup_snapshot_path}",
        f"shadow_status: {summary.shadow_status}",
        f"behavior_status: {summary.behavior_status}",
        f"payload_hash: {summary.payload_hash}",
        f"human_confirmed: {str(summary.confirmed).lower()}",
    ])
    lines.extend(["", "Warnings:"])
    lines.extend(f"- {item}" for item in summary.warnings or ("none",))
    lines.extend(["", "Blockers:"])
    lines.extend(f"- {item}" for item in summary.blockers or ("none",))
    return "\n".join(lines)


def format_refactor_large_module_gate(gate: RefactorLargeModuleGate) -> str:
    """Return explicit fail-closed final button state."""
    lines = [
        "Refactor Large Module Gate",
        "==========================",
        f"status: {gate.status}",
        f"enabled: {str(gate.enabled).lower()}",
        f"source_mutation_enabled: {str(gate.source_mutation_enabled).lower()}",
        "",
        "Blockers:",
    ]
    lines.extend(f"- {item}" for item in gate.blockers or ("none",))
    return "\n".join(lines)
