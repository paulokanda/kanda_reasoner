# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_review_stage_contract.py
"""Canonical stage-order contract for refactor review and external AI exchange."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "WORKBENCH_REVIEW_STAGE_FOUNDATION_FEATURE_ID",
    "CANONICAL_REFACTOR_STAGE_ORDER",
    "OPTIONAL_EXTERNAL_AI_STAGE",
    "WorkbenchReviewStageContract",
    "build_workbench_review_stage_contract",
    "validate_workbench_review_stage_contract",
]

WORKBENCH_REVIEW_STAGE_FOUNDATION_FEATURE_ID = (
    "workbench-review-stage-foundation-v1"
)

OPTIONAL_EXTERNAL_AI_STAGE = "EXTERNAL_AI_CANDIDATE_REVIEW"

CANONICAL_REFACTOR_STAGE_ORDER = (
    "PLAN_INTAKE",
    "DEPENDENCY_READINESS",
    "REAL_PREVIEW",
    "INTERNAL_PREVIEW_QUALITY_GATE",
    "STRUCTURAL_VALIDATION",
    "ADVANCED_QUALITY_REVIEW",
    "PREFLIGHT_BACKUP",
    "SOURCE_PAYLOAD",
    "COMPLETION_EVIDENCE",
    "SHADOW_RUNTIME_BEHAVIOR_VALIDATION",
    "ASSISTED_REVIEW",
    OPTIONAL_EXTERNAL_AI_STAGE,
    "FINAL_DIFF_TRANSACTION_SUMMARY",
    "HUMAN_AUTHORIZATION",
    "GOVERNED_APPLY",
)


@dataclass(frozen=True)
class WorkbenchReviewStageContract:
    """Describe canonical stage placement without inventing implementation PASS."""

    schema_version: str
    feature_id: str
    ordered_stages: tuple[str, ...]
    advanced_quality_review_after: str
    advanced_quality_review_before: str
    external_ai_stage_optional: bool
    external_ai_stage_after: str
    external_ai_stage_before: str
    analyzer_source_mutation_allowed: bool
    external_ai_direct_apply_allowed: bool
    human_authorization_required: bool


def build_workbench_review_stage_contract() -> WorkbenchReviewStageContract:
    """Return the canonical placement contract for future GUI and service wiring."""
    return WorkbenchReviewStageContract(
        schema_version="1.0",
        feature_id=WORKBENCH_REVIEW_STAGE_FOUNDATION_FEATURE_ID,
        ordered_stages=CANONICAL_REFACTOR_STAGE_ORDER,
        advanced_quality_review_after="STRUCTURAL_VALIDATION",
        advanced_quality_review_before="PREFLIGHT_BACKUP",
        external_ai_stage_optional=True,
        external_ai_stage_after="ASSISTED_REVIEW",
        external_ai_stage_before="FINAL_DIFF_TRANSACTION_SUMMARY",
        analyzer_source_mutation_allowed=False,
        external_ai_direct_apply_allowed=False,
        human_authorization_required=True,
    )


def validate_workbench_review_stage_contract(
    contract: WorkbenchReviewStageContract,
) -> tuple[str, ...]:
    """Return blockers for stage drift or authorization bypass."""
    blockers: list[str] = []
    stages = tuple(contract.ordered_stages)
    if len(stages) != len(set(stages)):
        blockers.append("WORKBENCH_REVIEW_STAGE_DUPLICATE")
    required = set(CANONICAL_REFACTOR_STAGE_ORDER)
    missing = sorted(required.difference(stages))
    blockers.extend("WORKBENCH_REVIEW_STAGE_MISSING:" + item for item in missing)
    blockers.extend(
        _relative_order_blockers(
            stages,
            left=contract.advanced_quality_review_after,
            middle="ADVANCED_QUALITY_REVIEW",
            right=contract.advanced_quality_review_before,
            marker="ADVANCED_QUALITY_REVIEW_ORDER_INVALID",
        )
    )
    blockers.extend(
        _relative_order_blockers(
            stages,
            left=contract.external_ai_stage_after,
            middle=OPTIONAL_EXTERNAL_AI_STAGE,
            right=contract.external_ai_stage_before,
            marker="EXTERNAL_AI_STAGE_ORDER_INVALID",
        )
    )
    if not contract.external_ai_stage_optional:
        blockers.append("EXTERNAL_AI_STAGE_MUST_REMAIN_OPTIONAL")
    if contract.analyzer_source_mutation_allowed:
        blockers.append("ANALYZER_SOURCE_MUTATION_MUST_BE_FALSE")
    if contract.external_ai_direct_apply_allowed:
        blockers.append("EXTERNAL_AI_DIRECT_APPLY_MUST_BE_FALSE")
    if not contract.human_authorization_required:
        blockers.append("HUMAN_AUTHORIZATION_MUST_REMAIN_REQUIRED")
    return tuple(sorted(set(blockers)))


def _relative_order_blockers(
    stages: tuple[str, ...],
    *,
    left: str,
    middle: str,
    right: str,
    marker: str,
) -> tuple[str, ...]:
    """Return one blocker when a three-stage ordering contract is not preserved."""
    try:
        left_index = stages.index(left)
        middle_index = stages.index(middle)
        right_index = stages.index(right)
    except ValueError:
        return (marker,)
    if not left_index < middle_index < right_index:
        return (marker,)
    return ()
