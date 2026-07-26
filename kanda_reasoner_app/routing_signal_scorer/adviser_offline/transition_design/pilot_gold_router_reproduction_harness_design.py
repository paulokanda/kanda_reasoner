# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_gold_router_reproduction_harness_design.py
"""P4 Pilot gold/frozen-router reproduction harness design.

P4 defines a design-only contract for a future reproduction harness that may later
prove a candidate can reproduce frozen router/canon outcomes before any
Pilot disagreement evidence is trusted. This module does not implement a live
harness, load gold data, read freeze memory, compare routes, execute cases,
score candidates, persist records, or grant Pilot/Copilot authority.
"""

from __future__ import annotations


__all__ = [
    'get_pilot_gold_router_reproduction_harness_design',
    'PilotGoldRouterReproductionHarnessDesign',
    'PilotReproductionHarnessPhaseDesign',
    'PilotReproductionMetricDesign',
    'PilotReproductionReferenceDesign',
]
from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_gold_frozen_router_reproduction_harness_design_v1"
SCHEMA_VERSION: Final[str] = "3.81-pilot-gold-frozen-router-reproduction-harness-design"
DESIGN_KIND: Final[str] = "pilot_gold_frozen_router_reproduction_harness_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P5 - Routing Signal Scorer v3 Pilot Simulation Skeleton Design v1, only "
    "after P4 validation, freeze, startup freeze context refresh, and "
    "FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot Gold/Frozen Router Reproduction Harness Design v1 defines only the "
    "future harness boundaries needed to prove frozen router/canon reproduction "
    "before any disagreement taxonomy evidence can be trusted. It does not run a "
    "harness, load gold data, read freeze memory, compare routes, score candidates, "
    "generate reports, persist records, train models, run batch mode, activate "
    "Limited Shadow Runtime, load prompts, or grant Pilot/Copilot authority."
)
MATCH_BEFORE_DISAGREE_RULE: Final[str] = (
    "Future Pilot disagreement evidence remains untrusted until a separately "
    "governed reproduction harness first proves exact frozen router/canon match "
    "on governed reference cases."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True
CRITICAL_BOUNDARY_ERROR_BUDGET: Final[int] = 0


@dataclass(frozen=True)
class PilotReproductionReferenceDesign:
    """Immutable design record for one future reference source category."""

    reference_id: str
    display_name: str
    allowed_future_source: str
    required_provenance: str
    forbidden_access: str
    fail_closed_condition: str


@dataclass(frozen=True)
class PilotReproductionHarnessPhaseDesign:
    """Immutable design record for one future harness phase."""

    phase_id: str
    display_name: str
    design_purpose: str
    required_gate_before_phase: str
    forbidden_operation: str
    human_review_requirement: str


@dataclass(frozen=True)
class PilotReproductionMetricDesign:
    """Immutable design record for one future reproduction metric."""

    metric_id: str
    required_result: str
    rationale: str
    failure_effect: str


@dataclass(frozen=True)
class PilotGoldRouterReproductionHarnessDesign:
    """Immutable design-only P4 reproduction harness boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    match_before_disagree_rule: str
    design_status: str
    harness_status: str
    gold_loading_status: str
    frozen_router_access_status: str
    route_comparison_status: str
    metric_calculation_status: str
    report_generation_status: str
    pilot_status: str
    copilot_status: str
    projection_status: str
    runtime_authority_status: str
    prompt_loading_authority_status: str
    persistence_authority_status: str
    training_data_use_status: str
    batch_mode_status: str
    limited_shadow_runtime_status: str
    critical_boundary_error_budget: int
    required_preconditions: tuple[str, ...]
    reference_designs: tuple[PilotReproductionReferenceDesign, ...]
    harness_phase_designs: tuple[PilotReproductionHarnessPhaseDesign, ...]
    metric_designs: tuple[PilotReproductionMetricDesign, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
    "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
    "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
    "p1_pilot_boundary_design_frozen",
    "p2_pilot_input_output_contract_validator_design_frozen",
    "p3_pilot_disagreement_taxonomy_design_frozen",
    "kanda_patch_delivery_root_drive_staging_canon_frozen",
    "startup_freeze_context_refreshed_after_p3_and_installer_canon",
    "freeze_memory_status_ok_after_p3_and_installer_canon",
    "human_request_explicitly_targets_p4_design_only_reproduction_harness",
)

_REFERENCE_DESIGNS: Final[tuple[PilotReproductionReferenceDesign, ...]] = (
    PilotReproductionReferenceDesign(
        reference_id="frozen_router_canon_reference",
        display_name="Frozen router/canon reference",
        allowed_future_source="A separately supplied immutable reference summary from frozen router/canon evidence.",
        required_provenance="Provenance must include freeze ID, feature ID, validation marker, and human-reviewed source summary.",
        forbidden_access="No direct freeze-memory read, prompt-library read, file scan, registry lookup, or runtime router import.",
        fail_closed_condition="Missing provenance blocks reproduction evidence and any later disagreement trust.",
    ),
    PilotReproductionReferenceDesign(
        reference_id="governed_case_reference",
        display_name="Governed case reference",
        allowed_future_source="A caller-supplied JSON-safe case summary approved under a later governed harness scope.",
        required_provenance="Provenance must include case identifier, source hash or human-supplied case label, expected frozen outcome, and review status.",
        forbidden_access="No case discovery, dataset crawling, hidden file IO, provider calls, or external retrieval.",
        fail_closed_condition="Unknown case provenance blocks use of the case in reproduction scoring.",
    ),
    PilotReproductionReferenceDesign(
        reference_id="expected_output_reference",
        display_name="Expected output reference",
        allowed_future_source="A human-reviewed expected frozen output summary supplied to the future harness.",
        required_provenance="Provenance must include expected task classification, boundary flags, supporting-material hints, and freeze traceability.",
        forbidden_access="No automatic route selection, prompt selection, or prompt loading from expected output fields.",
        fail_closed_condition="Any missing expected output field blocks match certification.",
    ),
)

_HARNESS_PHASE_DESIGNS: Final[tuple[PilotReproductionHarnessPhaseDesign, ...]] = (
    PilotReproductionHarnessPhaseDesign(
        phase_id="preflight_provenance_check_design",
        display_name="Preflight provenance check design",
        design_purpose="Require complete caller-supplied provenance before any future reproduction attempt.",
        required_gate_before_phase="P5+ implementation gate must explicitly permit a non-runtime preflight helper.",
        forbidden_operation="No file IO, freeze-memory read, prompt-library read, runtime import, or case discovery.",
        human_review_requirement="Human reviewer confirms provenance adequacy before any result can be trusted.",
    ),
    PilotReproductionHarnessPhaseDesign(
        phase_id="frozen_outcome_alignment_design",
        display_name="Frozen outcome alignment design",
        design_purpose="Describe how future evidence would compare supplied candidate summaries against supplied frozen summaries.",
        required_gate_before_phase="A later frozen implementation gate must authorize exact comparison semantics.",
        forbidden_operation="No live comparison execution, no score calculation, no candidate ranking, and no route recommendation in P4.",
        human_review_requirement="Human reviewer inspects mismatches before any later taxonomy label is considered.",
    ),
    PilotReproductionHarnessPhaseDesign(
        phase_id="critical_failure_blocker_design",
        display_name="Critical failure blocker design",
        design_purpose="Preserve zero tolerance for authority drift, prompt loading, runtime authority, or frozen-boundary conflicts.",
        required_gate_before_phase="Critical blocker handling must be separately governed before implementation.",
        forbidden_operation="No automated repair, no automatic supersession, and no continuation after a critical boundary conflict.",
        human_review_requirement="Human reviewer stops progression and resolves under governed freeze workflow.",
    ),
)

_METRIC_DESIGNS: Final[tuple[PilotReproductionMetricDesign, ...]] = (
    PilotReproductionMetricDesign(
        metric_id="exact_frozen_outcome_match_required",
        required_result="required_for_trust",
        rationale="Pilot disagreement evidence cannot be trusted until frozen router/canon outcomes are reproduced first.",
        failure_effect="Block all disagreement trust and block any candidate promotion discussion.",
    ),
    PilotReproductionMetricDesign(
        metric_id="critical_boundary_error_count_zero",
        required_result="0",
        rationale="Authority, prompt-loading, persistence, runtime, and freeze-boundary errors have zero error budget.",
        failure_effect="Fail closed and require human-governed remediation before any next milestone.",
    ),
    PilotReproductionMetricDesign(
        metric_id="human_review_mandatory_true",
        required_result="True",
        rationale="Future harness evidence is review support only and never approval authority.",
        failure_effect="Block use of the evidence record and treat it as invalid.",
    ),
    PilotReproductionMetricDesign(
        metric_id="effect_fields_none",
        required_result="routing_effect=none; prompt_loading_effect=none; runtime_effect=none; activation_effect=none",
        rationale="The future harness must not alter routing, prompts, runtime, or activation state.",
        failure_effect="Treat any non-none effect as a critical boundary error.",
    ),
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "run_reproduction_harness",
    "execute_harness_case",
    "load_gold_set",
    "read_gold_manifest",
    "read_freeze_memory",
    "read_prompt_library",
    "inspect_runtime_router",
    "import_runtime_router",
    "compare_routes",
    "calculate_reproduction_score",
    "rank_candidate",
    "certify_candidate",
    "trust_disagreement_label",
    "detect_disagreement",
    "score_disagreement",
    "project_route",
    "recommend_route",
    "select_route",
    "select_prompt",
    "load_prompt",
    "write_report",
    "write_review_queue",
    "persist_harness_record",
    "record_human_decision",
    "mutate_gold_registry",
    "mutate_freeze_memory",
    "train_from_harness_result",
    "run_batch_mode",
    "activate_limited_shadow_runtime",
    "promote_candidate",
    "call_provider",
    "use_embeddings",
)


def get_pilot_gold_router_reproduction_harness_design() -> PilotGoldRouterReproductionHarnessDesign:
    """Return the immutable P4 reproduction harness design record."""

    return PilotGoldRouterReproductionHarnessDesign(
        feature_id=FEATURE_ID,
        schema_version=SCHEMA_VERSION,
        design_kind=DESIGN_KIND,
        milestone="P4",
        title="Pilot Gold/Frozen Router Reproduction Harness Design v1",
        authority_statement=AUTHORITY_STATEMENT,
        match_before_disagree_rule=MATCH_BEFORE_DISAGREE_RULE,
        design_status="design_only",
        harness_status="not_implemented_design_only",
        gold_loading_status="not_implemented",
        frozen_router_access_status="not_implemented",
        route_comparison_status="not_implemented",
        metric_calculation_status="not_implemented",
        report_generation_status="not_implemented",
        pilot_status="not_implemented",
        copilot_status="not_implemented",
        projection_status="not_implemented",
        runtime_authority_status="not_granted",
        prompt_loading_authority_status="not_granted",
        persistence_authority_status="not_granted",
        training_data_use_status="forbidden",
        batch_mode_status="forbidden",
        limited_shadow_runtime_status="forbidden",
        critical_boundary_error_budget=CRITICAL_BOUNDARY_ERROR_BUDGET,
        required_preconditions=_REQUIRED_PRECONDITIONS,
        reference_designs=_REFERENCE_DESIGNS,
        harness_phase_designs=_HARNESS_PHASE_DESIGNS,
        metric_designs=_METRIC_DESIGNS,
        forbidden_operations=_FORBIDDEN_OPERATIONS,
        next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    )
