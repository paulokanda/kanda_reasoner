# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_io_contract_design.py
"""Design-only M27 Auxiliar/Assistant input/output contract design.

M27 defines a static input/output contract for a possible later Auxiliar/Assistant
human-review support step. It is a design record only. It does not process input,
generate output, validate live payloads, compare routes, select prompts, write
files, persist evidence, record human decisions, call providers, use embeddings,
activate shadow mode, start Assistant behavior, promote candidates, or grant any
runtime authority.

The only public entry point returns a deterministic immutable contract-design
record. Any future contract validation or Assistant-support implementation
remains separately governed and must be introduced only by later validated and
frozen milestones.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_auxiliar_assistant_io_contract_design_v1"
SCHEMA_VERSION: Final[str] = "3.68-auxiliar-assistant-io-contract-design"
DESIGN_KIND: Final[str] = "post_adviser_auxiliar_assistant_io_contract_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M28 - Routing Signal Scorer v3 Auxiliar/Assistant Contract Validator Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Auxiliar/Assistant input/output contract design describes future non-authoritative "
    "human-review support envelopes only. It is not Assistant behavior and has no routing "
    "effect, no prompt-loading effect, no persistence effect, no human-decision effect, "
    "no candidate-promotion effect, no shadow-mode activation effect, no runtime authority, "
    "and no Copilot/Pilot behavior."
)


@dataclass(frozen=True)
class AuxiliarAssistantContractFieldDesign:
    """Immutable description of one future contract field."""

    name: str
    contract_side: str
    primitive_kind: str
    required: bool
    allowed_status: str
    forbidden_use: str
    description: str


@dataclass(frozen=True)
class AuxiliarAssistantIOContractDesign:
    """Immutable design-only M27 Auxiliar/Assistant contract record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    input_contract_status: str
    output_contract_status: str
    validator_status: str
    assistant_behavior_status: str
    shadow_mode_status: str
    runtime_authority_status: str
    required_prior_milestones: tuple[str, ...]
    allowed_input_fields: tuple[AuxiliarAssistantContractFieldDesign, ...]
    allowed_output_fields: tuple[AuxiliarAssistantContractFieldDesign, ...]
    forbidden_output_fields: tuple[str, ...]
    required_future_contract_guardrails: tuple[str, ...]
    forbidden_contract_behaviors: tuple[str, ...]
    contract_invariants: tuple[str, ...]
    next_allowed_milestone: str
    implementation_gate: str


_REQUIRED_PRIOR_MILESTONES: Final[tuple[str, ...]] = (
    "m18_shadow_mode_boundary_design_frozen",
    "m19_shadow_mode_input_output_contract_design_frozen",
    "m20_shadow_mode_contract_validator_design_frozen",
    "m21_shadow_mode_observation_skeleton_design_frozen",
    "m22_shadow_mode_implementation_gate_design_frozen",
    "m23_non_runtime_shadow_observation_implementation_frozen",
    "m24_shadow_observation_review_evidence_design_frozen",
    "m25_assistant_boundary_readiness_gate_design_frozen",
    "m26_auxiliar_assistant_boundary_design_frozen",
)

_ALLOWED_INPUT_FIELDS: Final[tuple[AuxiliarAssistantContractFieldDesign, ...]] = (
    AuxiliarAssistantContractFieldDesign(
        name="assistant_case_id",
        contract_side="input",
        primitive_kind="string",
        required=True,
        allowed_status="caller_supplied_json_safe_primitive_only",
        forbidden_use="must_not_trigger_case_discovery_or_storage_lookup",
        description="Stable caller-supplied identifier for a future human-review assistance envelope.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="boundary_context_summary",
        contract_side="input",
        primitive_kind="string",
        required=True,
        allowed_status="caller_supplied_json_safe_primitive_only",
        forbidden_use="must_not_import_runtime_router_or_prompt_loader_context",
        description="Human-readable summary of the governed boundary context supplied by the caller.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="validated_shadow_observation_summary",
        contract_side="input",
        primitive_kind="string",
        required=True,
        allowed_status="caller_supplied_json_safe_primitive_only",
        forbidden_use="must_not_execute_or_transform_shadow_observation",
        description="Summary of already validated non-runtime observation evidence, supplied as text only.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="review_evidence_summary",
        contract_side="input",
        primitive_kind="string",
        required=True,
        allowed_status="caller_supplied_json_safe_primitive_only",
        forbidden_use="must_not_build_or_persist_review_evidence",
        description="Summary of review evidence prepared by prior governed milestones, supplied as text only.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="current_router_outcome_summary",
        contract_side="input",
        primitive_kind="string",
        required=True,
        allowed_status="caller_supplied_json_safe_primitive_only",
        forbidden_use="must_not_override_or_recompute_router_outcome",
        description="Descriptive summary of the current router outcome for human review context only.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="requested_support_kind",
        contract_side="input",
        primitive_kind="string",
        required=True,
        allowed_status="caller_supplied_limited_to_future_non_authoritative_human_review_support_labels",
        forbidden_use="must_not_select_route_prompt_or_patch_action",
        description="Caller-supplied label describing the kind of future non-authoritative support requested.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="known_boundary_flags_summary",
        contract_side="input",
        primitive_kind="string",
        required=False,
        allowed_status="caller_supplied_json_safe_primitive_only",
        forbidden_use="must_not_calculate_readiness_or_promotion_state",
        description="Optional summary of known safety flags for a future reviewer.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="caller_generated_timestamp_utc",
        contract_side="input",
        primitive_kind="string",
        required=True,
        allowed_status="caller_supplied_json_safe_primitive_only",
        forbidden_use="must_not_read_clock_or_filesystem_metadata",
        description="Timestamp generated by the caller, not by the contract design module.",
    ),
)

_ALLOWED_OUTPUT_FIELDS: Final[tuple[AuxiliarAssistantContractFieldDesign, ...]] = (
    AuxiliarAssistantContractFieldDesign(
        name="assistance_record_kind",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="future_in_memory_non_authoritative_envelope_only",
        forbidden_use="must_not_signal_assistant_activation_or_runtime_authority",
        description="Static record-kind marker for a future human-review assistance envelope.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="assistant_case_id",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="echo_of_caller_supplied_identifier_only",
        forbidden_use="must_not_discover_or_create_cases",
        description="Echo of the caller-supplied identifier only.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="contract_schema_version",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="static_schema_version_marker_only",
        forbidden_use="must_not_claim_runtime_compatibility_or_activation",
        description="Schema-version marker for future validation and review.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="authority_notice",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="required_non_authority_notice",
        forbidden_use="must_not_grant_router_prompt_freeze_or_promotion_authority",
        description="Required notice that the future envelope is non-authoritative.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="human_review_context_summary",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="future_human_readable_summary_only",
        forbidden_use="must_not_choose_or_override_router_outcome",
        description="Future summary for human review, not a decision or recommendation.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="boundary_questions_for_human_review",
        contract_side="output",
        primitive_kind="tuple_of_strings",
        required=False,
        allowed_status="future_question_prompts_for_human_reviewer_only",
        forbidden_use="must_not_record_or_infer_human_answer",
        description="Future review questions that require a human answer before any governed change.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="safety_flags_for_human_review",
        contract_side="output",
        primitive_kind="tuple_of_strings",
        required=False,
        allowed_status="future_explanatory_flags_only",
        forbidden_use="must_not_mark_candidate_or_assistant_as_ready",
        description="Future explanatory flags for a reviewer; they carry no authority.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="missing_information_summary",
        contract_side="output",
        primitive_kind="string",
        required=False,
        allowed_status="future_human_review_gap_summary_only",
        forbidden_use="must_not_trigger_source_scanning_or_case_discovery",
        description="Future summary of missing information that remains human-review controlled.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="requires_separate_human_review",
        contract_side="output",
        primitive_kind="boolean",
        required=True,
        allowed_status="must_remain_true_for_governed_changes",
        forbidden_use="must_not_substitute_for_human_confirmation",
        description="Future marker that separate human review remains required.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="storage_status",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="must_state_not_persisted_by_contract",
        forbidden_use="must_not_write_reports_queues_or_registry_records",
        description="Future output must remain in memory unless a later governed writer exists.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="routing_effect",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="must_state_no_routing_effect",
        forbidden_use="must_not_change_router_path_or_final_outcome",
        description="Future envelope must state that it does not affect routing.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="prompt_loading_effect",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="must_state_no_prompt_loading_effect",
        forbidden_use="must_not_load_or_select_prompts",
        description="Future envelope must state that it does not affect prompt loading.",
    ),
    AuxiliarAssistantContractFieldDesign(
        name="assistant_activation_effect",
        contract_side="output",
        primitive_kind="string",
        required=True,
        allowed_status="must_state_no_assistant_activation_effect",
        forbidden_use="must_not_start_assistant_auxiliar_pilot_or_copilot_behavior",
        description="Future envelope must state that it does not activate Assistant behavior.",
    ),
)

_FORBIDDEN_OUTPUT_FIELDS: Final[tuple[str, ...]] = (
    "final_route",
    "route_override",
    "selected_route",
    "selected_prompt",
    "prompt_to_load",
    "approved",
    "rejected",
    "overridden",
    "enabled",
    "activated",
    "promoted",
    "assistant_ready",
    "auxiliar_ready",
    "candidate_promoted",
    "promotion_ready",
    "confidence",
    "score",
    "probability",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "execute_patch",
    "write_gold",
    "write_registry",
    "write_freeze",
    "confirm_and_write",
    "router_authority_granted",
    "runtime_effect",
)

_REQUIRED_FUTURE_CONTRACT_GUARDRAILS: Final[tuple[str, ...]] = (
    "guardrail_contract_is_not_assistant_behavior",
    "guardrail_contract_is_not_shadow_activation",
    "guardrail_contract_is_not_router_authority",
    "guardrail_contract_is_not_prompt_loading",
    "guardrail_contract_is_not_persistence_or_report_writing",
    "guardrail_contract_requires_separate_human_review",
    "guardrail_contract_blocks_decision_recording_fields",
    "guardrail_contract_blocks_candidate_promotion_fields",
)

_FORBIDDEN_CONTRACT_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_input_processing",
    "live_output_generation",
    "live_contract_validation",
    "assistant_behavior",
    "auxiliar_behavior",
    "pilot_behavior",
    "copilot_behavior",
    "assistant_activation",
    "shadow_mode_activation",
    "shadow_mode_runtime_connection",
    "review_evidence_building",
    "observation_transformation_execution",
    "route_comparison_execution",
    "route_selection",
    "route_override",
    "prompt_selection",
    "prompt_loading",
    "runtime_router_import",
    "runtime_router_export",
    "runtime_state_inspection",
    "source_scanning",
    "case_discovery",
    "file_io",
    "console_io",
    "logging",
    "persistence",
    "report_writing",
    "review_queue_writing",
    "registry_writing",
    "gold_mutation",
    "freeze_writing",
    "human_decision_recording",
    "approval_recording",
    "rejection_recording",
    "override_recording",
    "patch_execution",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
)

_CONTRACT_INVARIANTS: Final[tuple[str, ...]] = (
    "m27_is_design_only",
    "m27_defines_auxiliar_assistant_io_contract_limits_only",
    "m27_does_not_process_input_or_generate_output",
    "m27_does_not_validate_live_payloads",
    "m27_does_not_start_auxiliar_assistant_or_copilot_behavior",
    "m27_does_not_activate_shadow_mode",
    "m27_does_not_compare_routes_or_select_prompts",
    "m27_does_not_grant_runtime_router_or_prompt_loader_authority",
    "m27_does_not_persist_or_write_project_state",
    "m27_does_not_record_human_decisions",
    "m27_future_outputs_must_remain_non_authoritative_human_review_support_only",
    "m28_requires_separate_governed_contract_validator_design",
)

_AUXILIAR_ASSISTANT_IO_CONTRACT_DESIGN: Final[AuxiliarAssistantIOContractDesign] = AuxiliarAssistantIOContractDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M27",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_assistant_behavior",
    input_contract_status="static_schema_design_only_no_input_processing",
    output_contract_status="static_schema_design_only_no_output_generation",
    validator_status="not_implemented_deferred_to_m28",
    assistant_behavior_status="not_started",
    shadow_mode_status="not_active",
    runtime_authority_status="not_granted",
    required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
    allowed_input_fields=_ALLOWED_INPUT_FIELDS,
    allowed_output_fields=_ALLOWED_OUTPUT_FIELDS,
    forbidden_output_fields=_FORBIDDEN_OUTPUT_FIELDS,
    required_future_contract_guardrails=_REQUIRED_FUTURE_CONTRACT_GUARDRAILS,
    forbidden_contract_behaviors=_FORBIDDEN_CONTRACT_BEHAVIORS,
    contract_invariants=_CONTRACT_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m27_validation_freeze_and_separate_m28_scope_confirmation",
)


__all__ = ["build_auxiliar_assistant_io_contract_design"]


def build_auxiliar_assistant_io_contract_design() -> AuxiliarAssistantIOContractDesign:
    """Return the immutable design-only M27 Assistant I/O contract record.

    The function accepts no observations, review evidence, prompts, candidates,
    runtime state, router objects, freeze files, or human decisions. It performs
    no input processing, no output generation, no validation, no Assistant
    behavior, no route comparison, no prompt loading, no runtime integration,
    no file IO, no persistence, no decision recording, no shadow activation,
    and no candidate promotion.
    """

    return _AUXILIAR_ASSISTANT_IO_CONTRACT_DESIGN
