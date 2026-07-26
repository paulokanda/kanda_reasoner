# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_cross_check_rules.py  # noqa: E501
"""Typed Python cross-check rules for Advanced Quality Review evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable

from .advanced_quality_evidence_models import FindingSeverity
from .advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    QualityDecision,
)
from .analyzer_adapter_contract import (
    AdapterDeltaState,
    AdapterEvidenceBundle,
    GrimpTopologyResultView,
    MypyFitnessResultView,
    VultureFitnessResultView,
)
from .analyzer_environment_contract import AnalyzerCapabilityMode
from .analyzer_specific_delta_strategies import (
    GraphTopologyDeltaState,
    MypyRelocationState,
    VultureCandidateDeltaState,
)
from .ruff_format_comparison import load_ruff_format_comparison_summary

__all__ = [
    "ADVANCED_QUALITY_CROSS_CHECK_FEATURE_ID",
    "AdvancedQualityCrossCheckInputs",
    "AdvancedQualityCrossCheckReport",
    "CrossCheckRuleDecision",
    "CrossCheckRuleResult",
    "evaluate_advanced_quality_cross_checks",
]

ADVANCED_QUALITY_CROSS_CHECK_FEATURE_ID = (
    "advanced-quality-review-cross-check-orchestration-qt-foundation-v1"
)


class CrossCheckRuleDecision(str, Enum):
    """Describe one typed rule result without scalar score compression."""

    PASS = "PASS"
    WARNING = "WARNING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True)
class CrossCheckRuleResult:
    """Record one deterministic typed rule result and its evidence references."""

    rule_id: str
    decision: CrossCheckRuleDecision
    rationale: str
    evidence_keys: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready rule evidence."""
        payload = asdict(self)
        payload["decision"] = self.decision.value
        payload["evidence_keys"] = list(self.evidence_keys)
        return payload


@dataclass(frozen=True)
class AdvancedQualityCrossCheckInputs:
    """Collect analyzer evidence required by typed cross-check rules."""

    analysis_identity_hash: str
    ruff: AdapterEvidenceBundle
    griffe: AdapterEvidenceBundle
    grimp: GrimpTopologyResultView
    mypy: MypyFitnessResultView
    vulture: VultureFitnessResultView
    expected_new_import_edges: tuple[str, ...] = ()


@dataclass(frozen=True)
class AdvancedQualityCrossCheckReport:
    """Preserve multidimensional rule evidence and one policy decision."""

    analysis_identity_hash: str
    rule_results: tuple[CrossCheckRuleResult, ...]
    quality_decision: QualityDecision

    def to_dict(self) -> dict[str, object]:
        """Return deterministic JSON-ready cross-check evidence."""
        return {
            "analysis_identity_hash": self.analysis_identity_hash,
            "quality_decision": self.quality_decision.value,
            "rule_results": [item.to_dict() for item in self.rule_results],
        }


def evaluate_advanced_quality_cross_checks(
    inputs: AdvancedQualityCrossCheckInputs,
) -> AdvancedQualityCrossCheckReport:
    """Evaluate named typed rules without YAML or external policy ownership."""
    _validate_identity_alignment(inputs)
    results = (
        _mandatory_execution_rule(inputs),
        _ruff_regression_rule(inputs.ruff),
        _griffe_contract_rule(inputs.griffe),
        _grimp_topology_rule(
            inputs.grimp,
            expected_new_import_edges=inputs.expected_new_import_edges,
        ),
        _mypy_type_contract_rule(inputs.mypy),
        _vulture_advisory_rule(inputs.vulture),
        _cross_analyzer_disagreement_rule(inputs),
    )
    return AdvancedQualityCrossCheckReport(
        analysis_identity_hash=inputs.analysis_identity_hash,
        rule_results=results,
        quality_decision=_overall_decision(results),
    )


def _validate_identity_alignment(inputs: AdvancedQualityCrossCheckInputs) -> None:
    expected = str(inputs.analysis_identity_hash or "").strip()
    if not expected:
        raise ValueError("CROSS_CHECK_ANALYSIS_IDENTITY_EMPTY")
    observed = {
        inputs.ruff.analysis_identity_hash,
        inputs.griffe.analysis_identity_hash,
        inputs.grimp.bundle.analysis_identity_hash,
        inputs.vulture.bundle.analysis_identity_hash,
    }
    if inputs.mypy.bundle is not None:
        observed.add(inputs.mypy.bundle.analysis_identity_hash)
    if observed != {expected}:
        raise ValueError("CROSS_CHECK_ANALYSIS_IDENTITY_MISMATCH")


def _mandatory_execution_rule(
    inputs: AdvancedQualityCrossCheckInputs,
) -> CrossCheckRuleResult:
    statuses = {
        "ruff": inputs.ruff.execution_status,
        "griffe": inputs.griffe.execution_status,
        "grimp": inputs.grimp.bundle.execution_status,
    }
    incomplete = tuple(
        sorted(
            engine_id + ":" + status.value
            for engine_id, status in statuses.items()
            if status is not AnalysisExecutionStatus.SUCCEEDED
        )
    )
    if incomplete:
        return _rule(
            "AQR_MANDATORY_EXECUTION_COMPLETE",
            CrossCheckRuleDecision.INDETERMINATE,
            "Mandatory analyzer execution is incomplete.",
            incomplete,
        )
    return _rule(
        "AQR_MANDATORY_EXECUTION_COMPLETE",
        CrossCheckRuleDecision.PASS,
        "All mandatory analyzers completed successfully.",
    )


def _ruff_regression_rule(bundle: AdapterEvidenceBundle) -> CrossCheckRuleResult:
    if bundle.execution_status is not AnalysisExecutionStatus.SUCCEEDED:
        return _rule(
            "AQR_RUFF_NEW_REGRESSION",
            CrossCheckRuleDecision.INDETERMINATE,
            (
                "Ruff execution did not complete successfully; "
                "regression status is unknown."
            ),
            ("execution_status:" + bundle.execution_status.value,),
        )
    new_findings = tuple(
        item.finding.semantic_key
        for item in bundle.deltas
        if item.state is AdapterDeltaState.NEW
    )
    if new_findings:
        return _rule(
            "AQR_RUFF_NEW_REGRESSION",
            CrossCheckRuleDecision.BLOCKED,
            "Preview introduces new Ruff findings.",
            new_findings,
        )
    try:
        format_summary = load_ruff_format_comparison_summary(bundle.raw_evidence_map())
    except ValueError:
        return _rule(
            "AQR_RUFF_NEW_REGRESSION",
            CrossCheckRuleDecision.INDETERMINATE,
            "Ruff formatter comparison evidence is invalid.",
            ("ruff/format_comparison.json",),
        )
    if format_summary is not None and format_summary.new_required_paths:
        return _rule(
            "AQR_RUFF_NEW_REGRESSION",
            CrossCheckRuleDecision.BLOCKED,
            "Preview introduces new Ruff formatting regressions.",
            format_summary.new_required_paths,
        )
    evidence = ()
    rationale = "Preview introduces no new Ruff findings."
    if format_summary is not None:
        evidence = format_summary.resolved_required_paths
        rationale = "Preview introduces no new Ruff lint or formatting regressions."
    return _rule(
        "AQR_RUFF_NEW_REGRESSION",
        CrossCheckRuleDecision.PASS,
        rationale,
        evidence,
    )


def _griffe_contract_rule(bundle: AdapterEvidenceBundle) -> CrossCheckRuleResult:
    if bundle.execution_status is not AnalysisExecutionStatus.SUCCEEDED:
        return _rule(
            "AQR_GRIFFE_PUBLIC_CONTRACT",
            CrossCheckRuleDecision.INDETERMINATE,
            "Griffe execution did not complete successfully; API status is unknown.",
            ("execution_status:" + bundle.execution_status.value,),
        )
    blockers = tuple(
        item.semantic_key
        for item in bundle.preview_findings
        if item.severity is FindingSeverity.BLOCKER
    )
    warnings = tuple(
        item.semantic_key
        for item in bundle.preview_findings
        if item.severity is FindingSeverity.WARNING
    )
    if blockers:
        return _rule(
            "AQR_GRIFFE_PUBLIC_CONTRACT",
            CrossCheckRuleDecision.BLOCKED,
            "Preview breaks one or more public API contracts.",
            blockers,
        )
    if warnings:
        return _rule(
            "AQR_GRIFFE_PUBLIC_CONTRACT",
            CrossCheckRuleDecision.REVIEW_REQUIRED,
            "Public API evidence changed and requires review.",
            warnings,
        )
    return _rule(
        "AQR_GRIFFE_PUBLIC_CONTRACT",
        CrossCheckRuleDecision.PASS,
        "No public API contract breakage was detected.",
    )


def _grimp_topology_rule(
    result: GrimpTopologyResultView,
    *,
    expected_new_import_edges: tuple[str, ...] = (),
) -> CrossCheckRuleResult:
    if result.bundle.execution_status is not AnalysisExecutionStatus.SUCCEEDED:
        return _rule(
            "AQR_GRIMP_TOPOLOGY_DELTA",
            CrossCheckRuleDecision.INDETERMINATE,
            (
                "Grimp execution did not complete successfully; "
                "topology status is unknown."
            ),
            ("execution_status:" + result.bundle.execution_status.value,),
        )
    new_cycles = tuple(
        item.importer + "->" + item.imported
        for item in result.topology_deltas
        if item.state is GraphTopologyDeltaState.NEW_CYCLE_BREAKER
    )
    new_edges = tuple(
        item.importer + "->" + item.imported
        for item in result.topology_deltas
        if item.state is GraphTopologyDeltaState.NEW_EDGE
    )
    if new_cycles:
        return _rule(
            "AQR_GRIMP_TOPOLOGY_DELTA",
            CrossCheckRuleDecision.BLOCKED,
            "Preview introduces new cycle-breaker topology evidence.",
            new_cycles,
        )
    expected = set(expected_new_import_edges)
    unexpected = tuple(sorted(set(new_edges) - expected))
    if unexpected:
        return _rule(
            "AQR_GRIMP_TOPOLOGY_DELTA",
            CrossCheckRuleDecision.REVIEW_REQUIRED,
            (
                "Preview introduces import edges not justified by approved "
                "Preview generation evidence."
            ),
            unexpected,
        )
    if new_edges:
        return _rule(
            "AQR_GRIMP_TOPOLOGY_DELTA",
            CrossCheckRuleDecision.PASS,
            (
                "New import edges match approved Preview generation evidence "
                "and no new cycle-breaker was found."
            ),
            tuple(sorted(new_edges)),
        )
    return _rule(
        "AQR_GRIMP_TOPOLOGY_DELTA",
        CrossCheckRuleDecision.PASS,
        "Preview introduces no new topology risk evidence.",
    )


def _mypy_type_contract_rule(
    result: MypyFitnessResultView,
) -> CrossCheckRuleResult:
    mode = result.capability_mode
    if (
        result.bundle is not None
        and result.bundle.execution_status is not AnalysisExecutionStatus.SUCCEEDED
    ):
        decision = (
            CrossCheckRuleDecision.INDETERMINATE
            if mode is AnalyzerCapabilityMode.AUTHORITATIVE
            else CrossCheckRuleDecision.WARNING
        )
        return _rule(
            "AQR_MYPY_TYPE_CONTRACT",
            decision,
            "mypy execution did not complete successfully; no type PASS is inferred.",
            ("execution_status:" + result.bundle.execution_status.value,),
        )
    if mode in {
        AnalyzerCapabilityMode.NOT_CONFIGURED,
        AnalyzerCapabilityMode.UNAVAILABLE,
    }:
        return _rule(
            "AQR_MYPY_TYPE_CONTRACT",
            CrossCheckRuleDecision.WARNING,
            "mypy evidence is explicitly unavailable for this review mode.",
            ("capability_mode:" + mode.value,),
        )
    new_findings = tuple(
        item.finding.semantic_key
        for item in result.relocation_deltas
        if item.state is MypyRelocationState.NEW_FINDING
    )
    ambiguous = tuple(
        item.finding.semantic_key
        for item in result.relocation_deltas
        if item.state is MypyRelocationState.AMBIGUOUS_MATCH
    )
    if new_findings and mode is AnalyzerCapabilityMode.AUTHORITATIVE:
        return _rule(
            "AQR_MYPY_TYPE_CONTRACT",
            CrossCheckRuleDecision.BLOCKED,
            "Authoritative mypy review found new type-contract regressions.",
            new_findings,
        )
    if new_findings or ambiguous:
        return _rule(
            "AQR_MYPY_TYPE_CONTRACT",
            CrossCheckRuleDecision.REVIEW_REQUIRED,
            "Type evidence contains new or ambiguous findings requiring review.",
            (*new_findings, *ambiguous),
        )
    return _rule(
        "AQR_MYPY_TYPE_CONTRACT",
        CrossCheckRuleDecision.PASS,
        "No new or ambiguous mypy finding remains.",
    )


def _vulture_advisory_rule(
    result: VultureFitnessResultView,
) -> CrossCheckRuleResult:
    if result.bundle.execution_status is not AnalysisExecutionStatus.SUCCEEDED:
        return _rule(
            "AQR_VULTURE_ADVISORY",
            CrossCheckRuleDecision.WARNING,
            (
                "Vulture advisory execution did not complete successfully; "
                "no PASS is inferred."
            ),
            ("execution_status:" + result.bundle.execution_status.value,),
        )
    new_candidates = tuple(
        item.finding.semantic_key
        for item in result.candidate_deltas
        if item.state is VultureCandidateDeltaState.NEW_CANDIDATE
    )
    if new_candidates:
        return _rule(
            "AQR_VULTURE_ADVISORY",
            CrossCheckRuleDecision.WARNING,
            "Vulture reports new dead-code candidates; evidence remains advisory.",
            new_candidates,
        )
    return _rule(
        "AQR_VULTURE_ADVISORY",
        CrossCheckRuleDecision.PASS,
        "No new Vulture candidate was introduced.",
    )


def _cross_analyzer_disagreement_rule(
    inputs: AdvancedQualityCrossCheckInputs,
) -> CrossCheckRuleResult:
    griffe_paths = {
        item.normalized_relative_path for item in inputs.griffe.preview_findings
    }
    vulture_new_paths = {
        item.finding.normalized_relative_path
        for item in inputs.vulture.candidate_deltas
        if item.state is VultureCandidateDeltaState.NEW_CANDIDATE
    }
    overlap = tuple(sorted(griffe_paths & vulture_new_paths))
    if overlap:
        return _rule(
            "AQR_CROSS_ANALYZER_DISAGREEMENT",
            CrossCheckRuleDecision.REVIEW_REQUIRED,
            "API-change and dead-code evidence overlap; preserve disagreement.",
            overlap,
        )
    return _rule(
        "AQR_CROSS_ANALYZER_DISAGREEMENT",
        CrossCheckRuleDecision.PASS,
        "No cross-analyzer disagreement requiring escalation was found.",
    )


def _overall_decision(
    results: Iterable[CrossCheckRuleResult],
) -> QualityDecision:
    decisions = {item.decision for item in results}
    if CrossCheckRuleDecision.BLOCKED in decisions:
        return QualityDecision.BLOCKED
    if CrossCheckRuleDecision.INDETERMINATE in decisions:
        return QualityDecision.INDETERMINATE
    if CrossCheckRuleDecision.REVIEW_REQUIRED in decisions:
        return QualityDecision.REVIEW_REQUIRED
    if CrossCheckRuleDecision.WARNING in decisions:
        return QualityDecision.PASS_WITH_WARNINGS
    return QualityDecision.PASS


def _rule(
    rule_id: str,
    decision: CrossCheckRuleDecision,
    rationale: str,
    evidence_keys: Iterable[str] = (),
) -> CrossCheckRuleResult:
    return CrossCheckRuleResult(
        rule_id=rule_id,
        decision=decision,
        rationale=rationale,
        evidence_keys=tuple(sorted(set(str(item) for item in evidence_keys))),
    )
