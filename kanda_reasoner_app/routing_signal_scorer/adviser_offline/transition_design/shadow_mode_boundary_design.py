# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_boundary_design.py
"""Design-only M18 shadow-mode boundary.

M18 is the post-Adviser bridge safety wall. It does not implement shadow mode,
Auxiliar/Assistant behavior, observation execution, input/output schemas,
runtime routing, prompt loading, persistence, or candidate promotion.

The only public entry point returns a deterministic immutable boundary record.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_shadow_mode_boundary_design_v1"
SCHEMA_VERSION: Final[str] = "3.59-shadow-mode-boundary-design"
DESIGN_KIND: Final[str] = "post_adviser_shadow_mode_boundary_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M19 - Routing Signal Scorer v3 Shadow Mode Input Output Contract Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Shadow boundary observes design limits only. The real router and human "
    "governance keep decision authority. This output has no routing effect, "
    "no prompt-loading effect, no candidate-promotion effect, and no "
    "Auxiliar/Assistant behavior."
)


@dataclass(frozen=True)
class PhaseAssertions:
    """Fixed phase state for the Adviser-to-Auxiliar/Assistant bridge."""

    adviser_phase: str
    post_adviser_transition_design_phase: str
    shadow_mode_status: str
    assistant_status: str
    pilot_copilot_status: str
    candidate_promotion_status: str
    runtime_authority_status: str
    implementation_status: str


@dataclass(frozen=True)
class ShadowModeBoundaryDesign:
    """Immutable design-only M18 boundary record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    boundary_role: str
    authority_disclaimer: str
    phase_assertions: PhaseAssertions
    allowed_capability_principles: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    import_boundary_rules: tuple[str, ...]
    side_effect_boundary_rules: tuple[str, ...]
    naming_boundary_rules: tuple[str, ...]
    next_allowed_milestone: str
    implementation_gate: str


_PHASE_ASSERTIONS: Final[PhaseAssertions] = PhaseAssertions(
    adviser_phase="closed",
    post_adviser_transition_design_phase="started",
    shadow_mode_status="design_only",
    assistant_status="not_started",
    pilot_copilot_status="not_started",
    candidate_promotion_status="blocked",
    runtime_authority_status="not_granted",
    implementation_status="blocked_by_default",
)

_ALLOWED_CAPABILITY_PRINCIPLES: Final[tuple[str, ...]] = (
    "define_shadow_boundary_principles_only",
    "record_post_adviser_phase_state_only",
    "document_future_contract_milestone_only",
    "preserve_router_and_human_decision_authority",
    "preserve_candidate_promotion_block",
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "shadow_mode_activation",
    "auxiliar_assistant_behavior",
    "pilot_copilot_behavior",
    "runtime_router_integration",
    "route_decision_or_override",
    "prompt_loading_or_prompt_selection",
    "candidate_execution_or_candidate_promotion",
    "input_output_contract_execution",
    "observation_execution",
    "report_generation",
    "review_queue_creation",
    "registry_or_gold_mutation",
    "freeze_memory_write",
    "startup_behavior_change",
    "file_read_or_file_write",
    "directory_creation",
    "logging_or_printing",
    "environment_access",
    "source_scanning",
    "network_access",
    "subprocess_or_shell_execution",
    "thread_or_process_creation",
    "dynamic_import_or_code_evaluation",
    "provider_model_call",
    "embedding_or_vector_index_use",
    "dependency_installation",
)

_IMPORT_BOUNDARY_RULES: Final[tuple[str, ...]] = (
    "transition_design_must_not_import_runtime_router_modules",
    "runtime_router_modules_must_not_import_transition_design_modules",
    "transition_design_must_not_import_prompt_loader_modules",
    "transition_design_must_not_import_freeze_writer_modules",
    "transition_design_must_not_import_gold_or_registry_writer_modules",
    "transition_design_must_not_import_provider_embedding_or_vector_modules",
)

_SIDE_EFFECT_BOUNDARY_RULES: Final[tuple[str, ...]] = (
    "m18_boundary_builder_accepts_no_runtime_case_input",
    "m18_boundary_builder_returns_static_immutable_design_record",
    "m18_boundary_builder_must_not_read_or_write_files",
    "m18_boundary_builder_must_not_create_directories",
    "m18_boundary_builder_must_not_print_or_log",
    "m18_boundary_builder_must_not_read_environment_variables",
)

_NAMING_BOUNDARY_RULES: Final[tuple[str, ...]] = (
    "use_blocked_by_default_language",
    "use_not_started_for_auxiliar_assistant_phase",
    "use_not_granted_for_runtime_authority",
    "avoid_forward_motion_readiness_language",
    "avoid_numeric_certainty_language",
)

_BOUNDARY_DESIGN: Final[ShadowModeBoundaryDesign] = ShadowModeBoundaryDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M18",
    boundary_role="immutable_design_only_safety_wall_between_adviser_and_future_shadow_work",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    phase_assertions=_PHASE_ASSERTIONS,
    allowed_capability_principles=_ALLOWED_CAPABILITY_PRINCIPLES,
    forbidden_operations=_FORBIDDEN_OPERATIONS,
    import_boundary_rules=_IMPORT_BOUNDARY_RULES,
    side_effect_boundary_rules=_SIDE_EFFECT_BOUNDARY_RULES,
    naming_boundary_rules=_NAMING_BOUNDARY_RULES,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m18_validation_freeze_and_separate_human_review",
)


__all__ = ["build_shadow_mode_boundary_design"]


def build_shadow_mode_boundary_design() -> ShadowModeBoundaryDesign:
    """Return the immutable design-only M18 boundary record.

    The function accepts no routing input and performs no observation logic.
    """

    return _BOUNDARY_DESIGN
