# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_disagreement_taxonomy_design.py
"""P3 Pilot disagreement taxonomy design.

P3 defines immutable design-only disagreement categories and evidence-language
rules for possible later human review. It does not detect, calculate, score,
compare, validate, project, rank, recommend, promote, persist, or execute any
Pilot or Copilot behavior. It cannot produce trusted disagreements until a later
frozen-router reproduction harness has proven match-before-disagree.
"""

from __future__ import annotations


__all__ = [
    'get_pilot_disagreement_taxonomy_design',
    'PilotDisagreementCategoryDesign',
    'PilotDisagreementEvidenceRuleDesign',
    'PilotDisagreementTaxonomyDesign',
    'PilotDisagreementTaxonomyInvariantDesign',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_disagreement_taxonomy_design_v1"
SCHEMA_VERSION: Final[str] = "3.80-pilot-disagreement-taxonomy-design"
DESIGN_KIND: Final[str] = "pilot_disagreement_taxonomy_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P4 - Routing Signal Scorer v3 Pilot Gold/Frozen Router Reproduction Harness "
    "Design v1, only after P3 validation, freeze, startup freeze context refresh, "
    "and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot Disagreement Taxonomy Design v1 defines descriptive categories and "
    "evidence-language rules only. It does not detect disagreements, run a "
    "validator, compare routes, score candidates, project routes, recommend "
    "actions, load prompts, persist records, train models, run batch mode, activate "
    "limited shadow runtime, or grant Pilot/Copilot runtime authority. Human "
    "governance and the real router remain authoritative."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "No taxonomy label is trusted as a real disagreement until a later reproduction "
    "harness first proves that the Pilot candidate can reproduce frozen router/canon "
    "outcomes on governed cases."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0


@dataclass(frozen=True)
class PilotDisagreementCategoryDesign:
    """Immutable design record for one future disagreement category."""

    category_id: str
    display_name: str
    severity: str
    definition: str
    allowed_evidence_language: str
    forbidden_interpretation: str
    required_human_review_action: str


@dataclass(frozen=True)
class PilotDisagreementEvidenceRuleDesign:
    """Immutable design record for evidence wording constraints."""

    rule_id: str
    applies_to: str
    allowed_source: str
    required_wording_constraint: str
    forbidden_source_or_action: str
    fail_closed_result: str


@dataclass(frozen=True)
class PilotDisagreementTaxonomyInvariantDesign:
    """Immutable design record for one taxonomy invariant."""

    invariant_id: str
    required_value: str
    rationale: str


@dataclass(frozen=True)
class PilotDisagreementTaxonomyDesign:
    """Immutable design-only P3 taxonomy design record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    match_before_disagree_rule: str
    design_status: str
    taxonomy_status: str
    detector_status: str
    scoring_status: str
    pilot_status: str
    copilot_status: str
    projection_status: str
    route_comparison_status: str
    runtime_authority_status: str
    prompt_loading_authority_status: str
    persistence_authority_status: str
    training_data_use_status: str
    batch_mode_status: str
    limited_shadow_runtime_status: str
    critical_boundary_error_budget: int
    required_preconditions: tuple[str, ...]
    categories: tuple[PilotDisagreementCategoryDesign, ...]
    evidence_rules: tuple[PilotDisagreementEvidenceRuleDesign, ...]
    invariants: tuple[PilotDisagreementTaxonomyInvariantDesign, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
    "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
    "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
    "p1_pilot_boundary_design_frozen",
    "p2_pilot_input_output_contract_validator_design_frozen",
    "startup_freeze_context_refreshed_after_p2",
    "freeze_memory_status_ok_after_p2",
    "human_request_explicitly_targets_p3_design_only_disagreement_taxonomy",
)

_CATEGORIES: Final[tuple[PilotDisagreementCategoryDesign, ...]] = (
    PilotDisagreementCategoryDesign(
        category_id="no_observable_difference",
        display_name="No observable difference",
        severity="info",
        definition="A future review record says the candidate and frozen reference appear aligned within supplied evidence.",
        allowed_evidence_language="Descriptive language only, such as appears aligned, with supplied evidence named by the caller.",
        forbidden_interpretation="Must not be treated as approval, route authority, readiness, promotion, or ground truth.",
        required_human_review_action="Human reviewer may record that no review issue was observed; no automated action may follow.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="missing_or_insufficient_evidence",
        display_name="Missing or insufficient evidence",
        severity="review_required",
        definition="A future review record lacks enough primitive caller-supplied evidence to compare safely.",
        allowed_evidence_language="Name the missing evidence class without requesting file IO, prompt loading, or runtime access.",
        forbidden_interpretation="Must not infer a router disagreement from absence of evidence.",
        required_human_review_action="Human reviewer decides whether to gather evidence outside Pilot or stop the case.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="task_classification_difference",
        display_name="Task classification difference",
        severity="review_required",
        definition="A future candidate classification summary differs from the caller-supplied frozen reference summary.",
        allowed_evidence_language="Describe the difference between summaries without selecting routes or prompts.",
        forbidden_interpretation="Must not override current task classification or route selection.",
        required_human_review_action="Human reviewer inspects the competing classification summaries.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="boundary_condition_difference",
        display_name="Boundary condition difference",
        severity="review_required",
        definition="A future candidate flags a boundary condition differently from the frozen reference summary.",
        allowed_evidence_language="Describe the boundary flag and cited supplied text; keep language non-authoritative.",
        forbidden_interpretation="Must not open or close a boundary gate automatically.",
        required_human_review_action="Human reviewer checks the boundary rule against frozen governance.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="supporting_material_hint_difference",
        display_name="Supporting material hint difference",
        severity="review_required",
        definition="A future candidate describes different supporting material hints than the frozen reference summary.",
        allowed_evidence_language="Use supporting material hints language only, never prompt-loading field names.",
        forbidden_interpretation="Must not imply prompt selection, prompt loading, or prompt-library authority.",
        required_human_review_action="Human reviewer reconciles the hint description outside any Pilot authority.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="freeze_constraint_conflict",
        display_name="Freeze constraint conflict",
        severity="critical_review",
        definition="A future candidate statement appears to conflict with a frozen do-not-regress rule supplied for review.",
        allowed_evidence_language="Quote or summarize the supplied frozen constraint and the conflicting candidate statement.",
        forbidden_interpretation="Must not modify freeze memory, supersede an entry, or repair a freeze automatically.",
        required_human_review_action="Human reviewer stops automated progression and resolves under governed freeze workflow.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="safety_governance_boundary_conflict",
        display_name="Safety or governance boundary conflict",
        severity="critical_review",
        definition="A future candidate appears to cross a governance, safety, or authority boundary.",
        allowed_evidence_language="State the observed boundary conflict and the source summary that triggered review.",
        forbidden_interpretation="Must not continue as a normal disagreement or self-correct by executing behavior.",
        required_human_review_action="Human reviewer treats the case as blocked until governed remediation is explicit.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="maturity_path_conflict",
        display_name="Maturity path conflict",
        severity="critical_review",
        definition="A future candidate proposes work outside the current P-series milestone order.",
        allowed_evidence_language="Identify the current frozen milestone and the premature or skipped future milestone.",
        forbidden_interpretation="Must not advance to skipped milestones, runtime shadow mode, or Copilot scope.",
        required_human_review_action="Human reviewer enforces the current next safe milestone only.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="authority_drift_attempt",
        display_name="Authority drift attempt",
        severity="critical_review",
        definition="A future candidate tries to recommend, approve, route, load prompts, persist, train, or execute.",
        allowed_evidence_language="Describe the attempted authority drift and the fixed effect field that must remain none.",
        forbidden_interpretation="Must not be softened into a minor difference; critical boundary error budget is zero.",
        required_human_review_action="Human reviewer blocks candidate promotion and opens governed correction if needed.",
    ),
    PilotDisagreementCategoryDesign(
        category_id="unresolved_ambiguity",
        display_name="Unresolved ambiguity",
        severity="review_required",
        definition="A future review record cannot classify the difference into a more specific category.",
        allowed_evidence_language="State why available primitive evidence is ambiguous and avoid guessing.",
        forbidden_interpretation="Must not classify by approximation when governance confidence is insufficient.",
        required_human_review_action="Human reviewer decides whether to add a governed taxonomy category later.",
    ),
)

_EVIDENCE_RULES: Final[tuple[PilotDisagreementEvidenceRuleDesign, ...]] = (
    PilotDisagreementEvidenceRuleDesign(
        rule_id="evidence_from_caller_supplied_primitives_only",
        applies_to="all_categories",
        allowed_source="caller_supplied_primitive_summaries_and_frozen_constraint_summaries",
        required_wording_constraint="Use descriptive, non-authoritative, human-review language.",
        forbidden_source_or_action="No file IO, prompt-library reads, live router calls, provider calls, embeddings, gold mutation, or registry mutation.",
        fail_closed_result="classify_as_missing_or_insufficient_evidence_for_human_review",
    ),
    PilotDisagreementEvidenceRuleDesign(
        rule_id="taxonomy_is_not_recommendation",
        applies_to="all_categories",
        allowed_source="category_definition_only",
        required_wording_constraint="Use appears, differs, conflicts, or requires review; do not use should route, approve, select, promote, or execute.",
        forbidden_source_or_action="No automated recommendation, readiness claim, or approval language.",
        fail_closed_result="classify_as_authority_drift_attempt_for_human_review",
    ),
    PilotDisagreementEvidenceRuleDesign(
        rule_id="match_before_disagree_required",
        applies_to="all_non_info_categories",
        allowed_source="later_governed_reproduction_harness_evidence_only_after_it_exists",
        required_wording_constraint="Before P4/P8 evidence exists, say taxonomy label is design-only and not a trusted disagreement.",
        forbidden_source_or_action="No trusted disagreement claim before reproduction harness readiness.",
        fail_closed_result="classify_as_unresolved_ambiguity_for_human_review",
    ),
    PilotDisagreementEvidenceRuleDesign(
        rule_id="critical_boundary_error_budget_zero",
        applies_to="critical_review_categories",
        allowed_source="supplied_boundary_or_freeze_constraint_summary",
        required_wording_constraint="State that critical boundary conflicts block progression until human governance resolves them.",
        forbidden_source_or_action="No auto-repair, auto-ignore, retry loop, or candidate promotion.",
        fail_closed_result="classify_as_safety_governance_boundary_conflict_for_human_review",
    ),
)

_INVARIANTS: Final[tuple[PilotDisagreementTaxonomyInvariantDesign, ...]] = (
    PilotDisagreementTaxonomyInvariantDesign(
        invariant_id="human_review_mandatory",
        required_value="True",
        rationale="Every category is for human review; no Pilot label can approve or route.",
    ),
    PilotDisagreementTaxonomyInvariantDesign(
        invariant_id="routing_effect",
        required_value="none",
        rationale="Taxonomy labels cannot change routing behavior.",
    ),
    PilotDisagreementTaxonomyInvariantDesign(
        invariant_id="prompt_loading_effect",
        required_value="none",
        rationale="Taxonomy labels cannot select or load prompts.",
    ),
    PilotDisagreementTaxonomyInvariantDesign(
        invariant_id="runtime_effect",
        required_value="none",
        rationale="Taxonomy labels cannot execute runtime behavior.",
    ),
    PilotDisagreementTaxonomyInvariantDesign(
        invariant_id="activation_effect",
        required_value="none",
        rationale="Taxonomy labels cannot activate Pilot, Copilot, or shadow runtime.",
    ),
    PilotDisagreementTaxonomyInvariantDesign(
        invariant_id="storage_status",
        required_value="in_memory_only",
        rationale="P3 adds only immutable design records and no persistence behavior.",
    ),
    PilotDisagreementTaxonomyInvariantDesign(
        invariant_id="critical_boundary_error_budget",
        required_value="0",
        rationale="Critical authority drift and boundary conflicts cannot be tolerated as acceptable errors.",
    ),
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "detect_disagreement",
    "calculate_disagreement",
    "score_disagreement",
    "rank_disagreement",
    "compare_routes",
    "execute_route_comparison",
    "project_route",
    "recommend_route",
    "select_route",
    "execute_route",
    "select_prompt",
    "load_prompt",
    "read_prompt_library",
    "read_freeze_memory",
    "mutate_freeze_memory",
    "read_gold_set",
    "mutate_gold_set",
    "mutate_registry",
    "persist_disagreement_record",
    "write_review_queue",
    "record_human_decision",
    "train_from_disagreement",
    "run_batch_mode",
    "activate_limited_shadow_runtime",
    "promote_candidate",
    "call_provider",
    "use_embeddings",
)


def get_pilot_disagreement_taxonomy_design() -> PilotDisagreementTaxonomyDesign:
    """Return immutable design-only P3 taxonomy metadata."""

    return PilotDisagreementTaxonomyDesign(
        feature_id=FEATURE_ID,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        milestone="P3",
        title="Routing Signal Scorer v3 Pilot Disagreement Taxonomy Design v1",
        authority_statement=AUTHORITY_STATEMENT,
        match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
        design_status="design_only",
        taxonomy_status="descriptive_categories_only_not_a_classifier",
        detector_status="not_implemented",
        scoring_status="not_implemented",
        pilot_status="not_implemented",
        copilot_status="not_implemented",
        projection_status="not_implemented",
        route_comparison_status="not_implemented",
        runtime_authority_status="none",
        prompt_loading_authority_status="none",
        persistence_authority_status="none",
        training_data_use_status="none",
        batch_mode_status="none",
        limited_shadow_runtime_status="forbidden_in_p_series_initial_scope",
        critical_boundary_error_budget=CRITICAL_BOUNDARY_ERROR_BUDGET,
        required_preconditions=_REQUIRED_PRECONDITIONS,
        categories=_CATEGORIES,
        evidence_rules=_EVIDENCE_RULES,
        invariants=_INVARIANTS,
        forbidden_operations=_FORBIDDEN_OPERATIONS,
        next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    )
