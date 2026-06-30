# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_io_contract_design.py
"""Design-only M19 shadow-mode input/output contract.

M19 defines the future non-runtime shadow observation input and output contract.
It does not validate live data, execute observation logic, compare routes,
load prompts, call candidates, write reports, persist records, or start
Auxiliar/Assistant behavior.

The only public entry point returns a deterministic immutable contract design
record. Exact validation logic belongs to a later separately governed milestone.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_shadow_mode_io_contract_design_v1"
SCHEMA_VERSION: Final[str] = "3.60-shadow-mode-io-contract-design"
DESIGN_KIND: Final[str] = "post_adviser_shadow_mode_io_contract_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M20 - Routing Signal Scorer v3 Shadow Mode Contract Validator Design v1"
)
AUTHORITY_DISCLAIMER: Final[str] = (
    "Shadow input and output contracts describe non-authoritative evidence only. "
    "The real router and human governance keep decision authority. This contract "
    "has no routing effect, no prompt-loading effect, no candidate-promotion "
    "effect, and no Auxiliar/Assistant behavior."
)


@dataclass(frozen=True)
class ContractFieldDesign:
    """Immutable field definition for a future shadow-mode contract."""

    name: str
    value_kind: str
    requirement: str
    source_rule: str
    description: str


@dataclass(frozen=True)
class ShadowModeIOContractDesign:
    """Immutable design-only M19 input/output contract record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    authority_disclaimer: str
    lifecycle_status: str
    input_contract_status: str
    output_contract_status: str
    validator_status: str
    observation_execution_status: str
    runtime_authority_status: str
    allowed_input_fields: tuple[ContractFieldDesign, ...]
    allowed_output_fields: tuple[ContractFieldDesign, ...]
    forbidden_input_kinds: tuple[str, ...]
    forbidden_output_fields: tuple[str, ...]
    contract_invariants: tuple[str, ...]
    json_safe_primitive_kinds: tuple[str, ...]
    next_allowed_milestone: str
    implementation_gate: str


_ALLOWED_INPUT_FIELDS: Final[tuple[ContractFieldDesign, ...]] = (
    ContractFieldDesign(
        name="routing_case_id",
        value_kind="string",
        requirement="required_later",
        source_rule="caller_supplied_serialized_primitive_only",
        description="Opaque case identifier supplied by a future offline harness.",
    ),
    ContractFieldDesign(
        name="user_request_summary",
        value_kind="string",
        requirement="required_later",
        source_rule="caller_supplied_sanitized_summary_only",
        description="Short sanitized summary of the user request, not raw prompt authority.",
    ),
    ContractFieldDesign(
        name="current_router_summary",
        value_kind="string",
        requirement="required_later",
        source_rule="caller_supplied_summary_only_no_router_object",
        description="Summary of the current governed router result, not a live router object.",
    ),
    ContractFieldDesign(
        name="current_router_path_summary",
        value_kind="string",
        requirement="optional_later",
        source_rule="caller_supplied_summary_only_no_runtime_reference",
        description="Summary of the existing route path chosen outside shadow mode.",
    ),
    ContractFieldDesign(
        name="current_prompt_group_summary",
        value_kind="list_of_strings",
        requirement="optional_later",
        source_rule="caller_supplied_serialized_names_only_no_prompt_loading",
        description="Names of prompt groups already selected outside shadow mode.",
    ),
    ContractFieldDesign(
        name="scorer_candidate_summary",
        value_kind="string",
        requirement="optional_later",
        source_rule="caller_supplied_summary_only_no_candidate_execution",
        description="Summary of candidate/scorer evidence supplied from outside the contract.",
    ),
    ContractFieldDesign(
        name="scorer_constraint_flags_summary",
        value_kind="list_of_strings",
        requirement="optional_later",
        source_rule="caller_supplied_serialized_flags_only",
        description="Serialized constraint flags already produced outside shadow mode.",
    ),
    ContractFieldDesign(
        name="boundary_context_summary",
        value_kind="string",
        requirement="optional_later",
        source_rule="caller_supplied_summary_only_no_file_or_registry_reference",
        description="Summary of applicable boundary context without live object references.",
    ),
    ContractFieldDesign(
        name="caller_generated_timestamp_utc",
        value_kind="string",
        requirement="optional_later",
        source_rule="caller_generated_only_shadow_module_must_not_call_time",
        description="Timestamp string supplied by the caller when needed for provenance.",
    ),
)

_ALLOWED_OUTPUT_FIELDS: Final[tuple[ContractFieldDesign, ...]] = (
    ContractFieldDesign(
        name="observation_record_kind",
        value_kind="fixed_string",
        requirement="required_later",
        source_rule="shadow_contract_defined_value_only",
        description="Marks future output as non-authoritative shadow observation evidence.",
    ),
    ContractFieldDesign(
        name="routing_case_id",
        value_kind="string",
        requirement="required_later",
        source_rule="copied_from_validated_input_only",
        description="Carries the opaque case identifier without adding authority.",
    ),
    ContractFieldDesign(
        name="contract_schema_version",
        value_kind="string",
        requirement="required_later",
        source_rule="contract_defined_value_only",
        description="Identifies the contract design version used by future observations.",
    ),
    ContractFieldDesign(
        name="authority_notice",
        value_kind="fixed_string",
        requirement="required_later",
        source_rule="contract_defined_value_only",
        description="States that the output has no routing, prompt, or promotion effect.",
    ),
    ContractFieldDesign(
        name="route_path_difference_observed",
        value_kind="boolean",
        requirement="optional_later",
        source_rule="future_non_runtime_observation_only",
        description="Records whether a difference was observed without directing action.",
    ),
    ContractFieldDesign(
        name="constraint_flags_observed",
        value_kind="list_of_strings",
        requirement="optional_later",
        source_rule="future_non_runtime_observation_only",
        description="Records observed constraint flags without declaring authority.",
    ),
    ContractFieldDesign(
        name="requires_separate_human_review",
        value_kind="boolean",
        requirement="required_later",
        source_rule="contract_defined_blocking_default",
        description="Keeps future shadow evidence under separate human review.",
    ),
    ContractFieldDesign(
        name="human_review_reason_summary",
        value_kind="string",
        requirement="optional_later",
        source_rule="future_non_runtime_observation_only",
        description="Explains why review is needed without implying workflow completion.",
    ),
    ContractFieldDesign(
        name="storage_status",
        value_kind="fixed_string",
        requirement="required_later",
        source_rule="contract_defined_value_not_persisted",
        description="Must state that future observation output is not persisted by default.",
    ),
    ContractFieldDesign(
        name="routing_effect",
        value_kind="fixed_string",
        requirement="required_later",
        source_rule="contract_defined_value_none",
        description="Must state that future observation output has no routing effect.",
    ),
    ContractFieldDesign(
        name="prompt_loading_effect",
        value_kind="fixed_string",
        requirement="required_later",
        source_rule="contract_defined_value_none",
        description="Must state that future observation output has no prompt-loading effect.",
    ),
)

_FORBIDDEN_INPUT_KINDS: Final[tuple[str, ...]] = (
    "live_router_object",
    "prompt_object",
    "file_handle",
    "path_object",
    "callable_object",
    "module_object",
    "registry_object",
    "gold_mutation_object",
    "freeze_writer_object",
    "provider_client_object",
    "embedding_index_object",
    "network_resource",
    "unknown_keys",
)

_FORBIDDEN_OUTPUT_FIELDS: Final[tuple[str, ...]] = (
    "final_route",
    "route_override",
    "selected_prompt",
    "prompt_to_load",
    "approved",
    "enabled",
    "activated",
    "promoted",
    "assistant_ready",
    "candidate_promoted",
    "confidence",
    "score",
    "probability",
    "recommendation",
    "suggested_route",
    "suggested_prompts",
    "execute_patch",
    "write_gold",
    "write_freeze",
    "confirm_and_write",
    "router_authority_granted",
    "runtime_effect",
)

_CONTRACT_INVARIANTS: Final[tuple[str, ...]] = (
    "m19_is_design_only",
    "schemas_are_static_contracts_not_validators",
    "future_inputs_must_be_caller_supplied_json_safe_primitives",
    "future_inputs_must_reject_unknown_keys",
    "future_outputs_must_remain_in_memory_non_authoritative_evidence",
    "future_outputs_must_not_direct_routes_or_prompt_loading",
    "future_outputs_must_not_persist_or_mutate_gold_registry_or_freeze_memory",
    "future_outputs_must_require_separate_human_review_by_default",
    "m20_is_required_before_contract_validation_logic",
)

_JSON_SAFE_PRIMITIVE_KINDS: Final[tuple[str, ...]] = (
    "string",
    "integer",
    "float",
    "boolean",
    "null",
    "list_of_primitives",
    "object_with_declared_keys_only",
)

_IO_CONTRACT_DESIGN: Final[ShadowModeIOContractDesign] = ShadowModeIOContractDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="M19",
    authority_disclaimer=AUTHORITY_DISCLAIMER,
    lifecycle_status="design_only_no_shadow_observation_execution",
    input_contract_status="static_schema_design_only_no_input_processing",
    output_contract_status="static_schema_design_only_no_output_generation",
    validator_status="not_implemented_deferred_to_m20",
    observation_execution_status="not_implemented",
    runtime_authority_status="not_granted",
    allowed_input_fields=_ALLOWED_INPUT_FIELDS,
    allowed_output_fields=_ALLOWED_OUTPUT_FIELDS,
    forbidden_input_kinds=_FORBIDDEN_INPUT_KINDS,
    forbidden_output_fields=_FORBIDDEN_OUTPUT_FIELDS,
    contract_invariants=_CONTRACT_INVARIANTS,
    json_safe_primitive_kinds=_JSON_SAFE_PRIMITIVE_KINDS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
    implementation_gate="blocked_until_m19_validation_freeze_and_separate_human_review",
)


__all__ = ["build_shadow_mode_io_contract_design"]


def build_shadow_mode_io_contract_design() -> ShadowModeIOContractDesign:
    """Return the immutable design-only M19 input/output contract record.

    The function accepts no input data and performs no validation or observation
    logic. M20 must be separately governed before contract validation exists.
    """

    return _IO_CONTRACT_DESIGN
