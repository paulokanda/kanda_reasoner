"""Design-only M28 Auxiliar/Assistant contract validator design.

M28 defines static rule descriptions for a possible later Auxiliar/Assistant
contract validator. It is a design record only. It does not validate live data,
process input, generate output, transform observations, compare routes, select
prompts, write files, persist evidence, record human decisions, call providers,
use embeddings, activate shadow mode, start Assistant behavior, promote
candidates, or grant runtime authority.

The only public entry point returns a deterministic immutable validator-design
record. Executable validation logic remains a later separately governed and
frozen milestone.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_auxiliar_assistant_contract_validator_design_v1"
SCHEMA_VERSION: Final[str] = "3.69-auxiliar-assistant-contract-validator-design"
DESIGN_KIND: Final[str] = "post_adviser_auxiliar_assistant_contract_validator_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M29 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Skeleton Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Auxiliar/Assistant contract validator design describes future fail-closed "
    "contract checks for non-authoritative human-review support envelopes only. "
    "It is not live validation, not Assistant behavior, and has no routing effect, "
    "no prompt-loading effect, no persistence effect, no human-decision effect, "
    "no candidate-promotion effect, no shadow-mode activation effect, no runtime "
    "authority, and no Copilot/Pilot behavior."
)


@dataclass(frozen=True)
class AuxiliarAssistantValidatorRuleDesign:
    """Immutable future validation rule description."""

    rule_id: str
    contract_side: str
    planned_check_kind: str
    failure_kind: str
    default_disposition: str
    description: str


@dataclass(frozen=True)
class AuxiliarAssistantContractValidatorDesign:
    """Immutable design-only M28 Auxiliar/Assistant validator record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    validator_design_status: str
    live_validation_status: str
    input_processing_status: str
    output_generation_status: str
    assistant_behavior_status: str
    shadow_mode_status: str
    runtime_authority_status: str
    required_prior_milestones: tuple[str, ...]
    planned_input_validation_rules: tuple[AuxiliarAssistantValidatorRuleDesign, ...]
    planned_output_validation_rules: tuple[AuxiliarAssistantValidatorRuleDesign, ...]
    fail_closed_boundary_rules: tuple[str, ...]
    forbidden_validator_behaviors: tuple[str, ...]
    validator_invariants: tuple[str, ...]
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
    "m27_auxiliar_assistant_input_output_contract_design_frozen",
)

_PLANNED_INPUT_VALIDATION_RULES: Final[tuple[AuxiliarAssistantValidatorRuleDesign, ...]] = (
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_input_declared_keys_only",
        contract_side="input",
        planned_check_kind="declared_key_set_exact_match",
        failure_kind="contract_shape_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future validators must reject any input key not declared by M27.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_input_required_fields_present",
        contract_side="input",
        planned_check_kind="required_key_presence_check",
        failure_kind="missing_required_human_review_context",
        default_disposition="reject_in_future_validator_design",
        description="Future validators must reject missing required M27 input fields.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_input_json_safe_primitives_only",
        contract_side="input",
        planned_check_kind="json_safe_primitive_tree_check",
        failure_kind="non_serialized_input_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future inputs must remain JSON-safe primitive values or declared primitive containers.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_input_live_objects_rejected",
        contract_side="input",
        planned_check_kind="live_object_category_block",
        failure_kind="live_object_boundary_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future validators must reject router, prompt, registry, freeze, provider, embedding, module, callable, and file-handle objects.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_input_caller_supplied_only",
        contract_side="input",
        planned_check_kind="no_discovery_rule",
        failure_kind="source_discovery_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future validators may only inspect caller-supplied payloads and must not discover files, prompts, cases, or runtime state.",
    ),
)

_PLANNED_OUTPUT_VALIDATION_RULES: Final[tuple[AuxiliarAssistantValidatorRuleDesign, ...]] = (
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_output_declared_keys_only",
        contract_side="output",
        planned_check_kind="declared_key_set_exact_match",
        failure_kind="contract_shape_violation",
        default_disposition="block_in_future_validator_design",
        description="Future validators must reject output keys not declared by M27.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_output_authority_notice_required",
        contract_side="output",
        planned_check_kind="fixed_non_authority_notice_check",
        failure_kind="authority_notice_missing",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must include the fixed non-authoritative notice required by M27.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_output_no_route_or_prompt_directives",
        contract_side="output",
        planned_check_kind="authority_field_block",
        failure_kind="runtime_authority_leak",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must not contain final-route, route-override, selected-route, selected-prompt, or prompt-loading directives.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_output_no_activation_or_readiness_claims",
        contract_side="output",
        planned_check_kind="activation_or_readiness_field_block",
        failure_kind="automation_bias_or_activation_leak",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must not contain Assistant-ready, enabled, activated, promoted, confidence, score, probability, recommendation, or readiness claims.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_output_no_governed_write_directives",
        contract_side="output",
        planned_check_kind="governed_write_field_block",
        failure_kind="governed_write_authority_leak",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must not contain freeze, gold, registry, review queue, human decision, patch execution, or confirmation-write directives.",
    ),
    AuxiliarAssistantValidatorRuleDesign(
        rule_id="assistant_output_in_memory_non_authoritative_only",
        contract_side="output",
        planned_check_kind="storage_and_authority_status_check",
        failure_kind="persistence_or_authority_leak",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must remain in-memory non-authoritative human-review support evidence requiring separate review.",
    ),
)

_FAIL_CLOSED_BOUNDARY_RULES: Final[tuple[str, ...]] = (
    "unknown_input_keys_reject",
    "unknown_output_keys_block",
    "missing_required_input_fields_reject",
    "non_primitive_inputs_reject",
    "live_object_inputs_reject",
    "authority_or_activation_fields_block",
    "governed_write_fields_block",
    "persistence_fields_block",
    "human_decision_recording_fields_block",
    "candidate_promotion_fields_block",
)

_FORBIDDEN_VALIDATOR_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_contract_validation_execution",
    "callable_validator_entrypoint",
    "live_input_processing",
    "live_output_generation",
    "assistant_behavior",
    "auxiliar_behavior",
    "copilot_behavior",
    "pilot_behavior",
    "assistant_activation",
    "shadow_mode_activation",
    "observation_transformation",
    "review_evidence_builder",
    "route_comparison_execution",
    "route_selection",
    "prompt_loading",
    "source_scanning",
    "case_discovery",
    "file_io",
    "console_io",
    "logging",
    "persistence",
    "report_writing",
    "review_queue_writing",
    "human_decision_recording",
    "registry_writing",
    "gold_mutation",
    "freeze_writing",
    "patch_execution",
    "runtime_router_import",
    "runtime_router_export",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
)

_VALIDATOR_INVARIANTS: Final[tuple[str, ...]] = (
    "m28_is_design_only",
    "m28_defines_auxiliar_assistant_contract_validator_limits_only",
    "m28_has_no_callable_validator_entrypoint",
    "m28_does_not_validate_live_payloads",
    "m28_does_not_process_input_or_generate_output",
    "m28_does_not_start_auxiliar_assistant_or_copilot_behavior",
    "m28_does_not_activate_shadow_mode",
    "m28_does_not_grant_runtime_router_or_prompt_loader_authority",
    "m28_does_not_record_human_decisions",
    "m28_does_not_persist_or_mutate_project_state",
    "future_validator_must_fail_closed_on_unknown_keys_and_authority_fields",
    "m29_requires_separate_governed_assistance_skeleton_design",
)

_CONTRACT_VALIDATOR_DESIGN: Final[AuxiliarAssistantContractValidatorDesign] = AuxiliarAssistantContractValidatorDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M28",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_live_contract_validation",
    validator_design_status="static_rule_design_only_no_validator_function",
    live_validation_status="not_implemented",
    input_processing_status="not_implemented",
    output_generation_status="not_implemented",
    assistant_behavior_status="not_started",
    shadow_mode_status="not_active",
    runtime_authority_status="not_granted",
    required_prior_milestones=_REQUIRED_PRIOR_MILESTONES,
    planned_input_validation_rules=_PLANNED_INPUT_VALIDATION_RULES,
    planned_output_validation_rules=_PLANNED_OUTPUT_VALIDATION_RULES,
    fail_closed_boundary_rules=_FAIL_CLOSED_BOUNDARY_RULES,
    forbidden_validator_behaviors=_FORBIDDEN_VALIDATOR_BEHAVIORS,
    validator_invariants=_VALIDATOR_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m28_validation_freeze_and_separate_scope_review",
)


__all__ = ["build_auxiliar_assistant_contract_validator_design"]


def build_auxiliar_assistant_contract_validator_design() -> AuxiliarAssistantContractValidatorDesign:
    """Return the immutable design-only M28 contract validator record.

    The function accepts no input and performs no validation, I/O, logging,
    persistence, route comparison, prompt loading, Assistant activation, provider
    calls, embedding work, candidate promotion, or runtime integration.
    """

    return _CONTRACT_VALIDATOR_DESIGN
