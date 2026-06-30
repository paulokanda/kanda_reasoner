# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_contract_validator_design.py
"""Design-only M20 shadow-mode contract validator design.

M20 defines how a future non-runtime validator should enforce the M19
input/output contract. It does not validate live data, process caller input,
generate observation output, compare routes, load prompts, call candidates,
write reports, persist records, or start Auxiliar/Assistant behavior.

The only public entry point returns a deterministic immutable validator design
record. Executable validation logic belongs to a later separately governed
milestone.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_shadow_mode_contract_validator_design_v1"
SCHEMA_VERSION: Final[str] = "3.61-shadow-mode-contract-validator-design"
DESIGN_KIND: Final[str] = "post_adviser_shadow_mode_contract_validator_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M21 - Routing Signal Scorer v3 Shadow Mode Observation Skeleton Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Shadow contract validator design describes future contract enforcement only. "
    "The real router and human governance keep decision authority. This design "
    "has no live validation effect, no routing effect, no prompt-loading effect, "
    "no candidate-promotion effect, and no Auxiliar/Assistant behavior."
)


@dataclass(frozen=True)
class ValidatorRuleDesign:
    """Immutable future validation rule description."""

    rule_id: str
    contract_side: str
    planned_check_kind: str
    failure_kind: str
    default_disposition: str
    description: str


@dataclass(frozen=True)
class ShadowModeContractValidatorDesign:
    """Immutable design-only M20 contract validator record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    validator_design_status: str
    live_validation_status: str
    observation_execution_status: str
    runtime_authority_status: str
    required_preconditions: tuple[str, ...]
    planned_input_validation_rules: tuple[ValidatorRuleDesign, ...]
    planned_output_validation_rules: tuple[ValidatorRuleDesign, ...]
    forbidden_validator_behaviors: tuple[str, ...]
    validator_invariants: tuple[str, ...]
    next_allowed_milestone: str
    implementation_gate: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m18_shadow_mode_boundary_design_frozen",
    "m19_shadow_mode_input_output_contract_design_frozen",
    "freezememory_status_ok_before_later_executable_validation",
    "separate_human_review_required_before_later_executable_validation",
)

_PLANNED_INPUT_VALIDATION_RULES: Final[tuple[ValidatorRuleDesign, ...]] = (
    ValidatorRuleDesign(
        rule_id="input_unknown_keys_rejected",
        contract_side="input",
        planned_check_kind="declared_key_set_exact_match",
        failure_kind="contract_shape_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future validators must reject any input key not declared by M19.",
    ),
    ValidatorRuleDesign(
        rule_id="input_json_safe_primitives_only",
        contract_side="input",
        planned_check_kind="json_safe_primitive_tree_check",
        failure_kind="non_serialized_input_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future inputs must be strings, numbers, booleans, null, or declared primitive containers.",
    ),
    ValidatorRuleDesign(
        rule_id="input_live_objects_rejected",
        contract_side="input",
        planned_check_kind="live_object_category_block",
        failure_kind="live_object_boundary_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future validators must reject router, prompt, registry, freeze, provider, embedding, module, callable, and file-handle objects.",
    ),
    ValidatorRuleDesign(
        rule_id="input_caller_supplied_only",
        contract_side="input",
        planned_check_kind="no_shadow_discovery_rule",
        failure_kind="source_discovery_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future validators may only check data supplied by the caller and must not discover files, prompts, cases, or runtime state.",
    ),
    ValidatorRuleDesign(
        rule_id="input_required_fields_checked_later",
        contract_side="input",
        planned_check_kind="required_key_presence_check",
        failure_kind="contract_shape_violation",
        default_disposition="reject_in_future_validator_design",
        description="Future validators must reject missing M19 required fields after executable validation is separately approved.",
    ),
)

_PLANNED_OUTPUT_VALIDATION_RULES: Final[tuple[ValidatorRuleDesign, ...]] = (
    ValidatorRuleDesign(
        rule_id="output_declared_keys_only",
        contract_side="output",
        planned_check_kind="declared_key_set_exact_match",
        failure_kind="contract_shape_violation",
        default_disposition="block_in_future_validator_design",
        description="Future validators must reject output keys not declared by M19.",
    ),
    ValidatorRuleDesign(
        rule_id="output_authority_notice_required",
        contract_side="output",
        planned_check_kind="fixed_non_authority_notice_check",
        failure_kind="authority_notice_missing",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must include the fixed non-authoritative notice required by the contract.",
    ),
    ValidatorRuleDesign(
        rule_id="output_no_route_or_prompt_directives",
        contract_side="output",
        planned_check_kind="authority_field_block",
        failure_kind="runtime_authority_leak",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must not contain final-route, route-override, selected-prompt, or prompt-loading directives.",
    ),
    ValidatorRuleDesign(
        rule_id="output_no_governed_write_directives",
        contract_side="output",
        planned_check_kind="governed_write_field_block",
        failure_kind="governed_write_authority_leak",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must not contain freeze, gold, registry, patch execution, or confirmation-write directives.",
    ),
    ValidatorRuleDesign(
        rule_id="output_no_readiness_metrics",
        contract_side="output",
        planned_check_kind="overtrust_field_block",
        failure_kind="automation_bias_risk",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must not contain confidence, score, probability, readiness, enabled, activated, promoted, or approval fields.",
    ),
    ValidatorRuleDesign(
        rule_id="output_in_memory_non_authoritative_only",
        contract_side="output",
        planned_check_kind="storage_and_authority_status_check",
        failure_kind="persistence_or_authority_leak",
        default_disposition="block_in_future_validator_design",
        description="Future outputs must remain in-memory non-authoritative evidence and require separate human review by default.",
    ),
)

_FORBIDDEN_VALIDATOR_BEHAVIORS: Final[tuple[str, ...]] = (
    "live_input_validation_execution",
    "callable_validator_entrypoint",
    "observation_generation",
    "route_comparison",
    "candidate_execution",
    "prompt_loading",
    "source_scanning",
    "case_discovery",
    "file_io",
    "console_io",
    "logging",
    "persistence",
    "report_writing",
    "registry_writing",
    "gold_mutation",
    "freeze_writing",
    "runtime_router_import",
    "runtime_router_export",
    "provider_or_model_call",
    "embedding_or_vector_index",
    "network_call",
    "subprocess_call",
    "dynamic_import",
    "candidate_promotion",
    "shadow_mode_activation",
    "assistant_behavior",
)

_VALIDATOR_INVARIANTS: Final[tuple[str, ...]] = (
    "m20_is_design_only",
    "m20_defines_future_validator_rules_only",
    "m20_does_not_validate_live_input",
    "m20_does_not_generate_or_validate_live_observations",
    "future_validator_must_fail_closed_on_unknown_input_keys",
    "future_validator_must_reject_non_primitive_inputs",
    "future_validator_must_block_authority_fields",
    "future_validator_must_keep_outputs_non_authoritative",
    "future_validator_must_not_persist_or_mutate_project_state",
    "m21_is_required_before_observation_skeleton_design",
)

_CONTRACT_VALIDATOR_DESIGN: Final[ShadowModeContractValidatorDesign] = ShadowModeContractValidatorDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M20",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_live_validation_execution",
    validator_design_status="static_rule_design_only_no_validator_function",
    live_validation_status="not_implemented",
    observation_execution_status="not_implemented",
    runtime_authority_status="not_granted",
    required_preconditions=_REQUIRED_PRECONDITIONS,
    planned_input_validation_rules=_PLANNED_INPUT_VALIDATION_RULES,
    planned_output_validation_rules=_PLANNED_OUTPUT_VALIDATION_RULES,
    forbidden_validator_behaviors=_FORBIDDEN_VALIDATOR_BEHAVIORS,
    validator_invariants=_VALIDATOR_INVARIANTS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m20_validation_freeze_and_separate_human_review",
)


__all__ = ["build_shadow_mode_contract_validator_design"]


def build_shadow_mode_contract_validator_design() -> ShadowModeContractValidatorDesign:
    """Return the immutable design-only M20 contract validator record.

    The function accepts no input data and performs no live validation,
    observation, route comparison, or authority logic. Executable validation must
    be separately governed later.
    """

    return _CONTRACT_VALIDATOR_DESIGN
