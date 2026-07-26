# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/pilot_io_contract_validator_design.py
"""P2 Pilot input/output contract and validator design.

P2 defines immutable design-only field contracts and fail-closed validation-rule
plans for a possible later Pilot projection envelope. It does not implement a
live validator, process inputs, generate outputs, run Pilot, run Copilot, compare
routes, select or execute routes, select or load prompts, integrate runtime
routing, persist records, use outputs for training data, run batch mode, activate
limited shadow runtime, call providers, use embeddings, mutate gold or registry
state, record human decisions, promote candidates, or grant authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_pilot_io_contract_validator_design_v1"
SCHEMA_VERSION: Final[str] = "3.79-pilot-io-contract-validator-design"
DESIGN_KIND: Final[str] = "pilot_io_contract_validator_design_only"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "P3 - Routing Signal Scorer v3 Pilot Disagreement Taxonomy Design v1, only after "
    "P2 validation, freeze, startup freeze context refresh, and FREEZE_MEMORY_STATUS OK"
)
AUTHORITY_STATEMENT: Final[str] = (
    "Pilot Input Output Contract and Validator Design v1 defines future field and "
    "fail-closed validation-rule boundaries only. It does not implement a live validator, "
    "does not process inputs, does not generate outputs, does not start Pilot or Copilot, "
    "does not project or compare routes, does not load prompts, does not persist output, "
    "does not use output as training data, does not run batch mode, does not activate "
    "limited shadow runtime, and does not grant runtime authority. Human governance and "
    "the real router remain authoritative."
)
ROUTING_EFFECT: Final[str] = "none"
PROMPT_LOADING_EFFECT: Final[str] = "none"
RUNTIME_EFFECT: Final[str] = "none"
ACTIVATION_EFFECT: Final[str] = "none"
STORAGE_STATUS: Final[str] = "in_memory_only"
HUMAN_REVIEW_MANDATORY: Final[bool] = True


@dataclass(frozen=True)
class PilotContractFieldDesign:
    """Immutable design record for one future Pilot contract field."""

    field_name: str
    direction: str
    required_state: str
    value_shape: str
    allowed_purpose: str
    forbidden_interpretation: str
    description: str


@dataclass(frozen=True)
class PilotValidatorRuleDesign:
    """Immutable design record for one future fail-closed validator rule."""

    rule_id: str
    applies_to: str
    rejection_condition: str
    required_failure_mode: str
    rationale: str


@dataclass(frozen=True)
class PilotOutputInvariantDesign:
    """Immutable design record for one future fixed output invariant."""

    invariant_id: str
    output_field: str
    required_value: str
    value_source: str
    forbidden_alternative: str
    rationale: str


@dataclass(frozen=True)
class PilotForbiddenNameDesign:
    """Immutable design record for one banned authority-drift name."""

    name: str
    name_group: str
    forbidden_location: str
    replacement_policy: str
    rationale: str


@dataclass(frozen=True)
class PilotIOContractValidatorDesign:
    """Immutable design-only P2 contract and validator design record."""

    feature_id: str
    schema_version: str
    design_kind: str
    milestone: str
    title: str
    authority_statement: str
    design_status: str
    validator_status: str
    pilot_status: str
    copilot_status: str
    projection_status: str
    runtime_authority_status: str
    prompt_loading_authority_status: str
    persistence_authority_status: str
    training_data_use_status: str
    batch_mode_status: str
    limited_shadow_runtime_status: str
    required_preconditions: tuple[str, ...]
    allowed_input_fields: tuple[PilotContractFieldDesign, ...]
    allowed_output_fields: tuple[PilotContractFieldDesign, ...]
    input_validator_rules: tuple[PilotValidatorRuleDesign, ...]
    output_validator_rules: tuple[PilotValidatorRuleDesign, ...]
    fixed_output_invariants: tuple[PilotOutputInvariantDesign, ...]
    forbidden_field_names: tuple[PilotForbiddenNameDesign, ...]
    contract_design_invariants: tuple[str, ...]
    forbidden_operations: tuple[str, ...]
    next_allowed_milestone: str


_REQUIRED_PRECONDITIONS: Final[tuple[str, ...]] = (
    "m35_post_adviser_to_pilot_copilot_handoff_closure_design_frozen",
    "rg_pilot_000_pilot_copilot_phase0_router_canon_frozen",
    "p0_pilot_copilot_scope_charter_entry_gate_design_frozen",
    "p1_pilot_boundary_design_frozen",
    "startup_freeze_context_refreshed_after_p1",
    "freeze_memory_status_ok_after_p1",
    "human_request_explicitly_targets_p2_design_only_contract_validator",
)

_ALLOWED_INPUT_FIELDS: Final[tuple[PilotContractFieldDesign, ...]] = (
    PilotContractFieldDesign(
        field_name="case_id",
        direction="input",
        required_state="required_non_empty_string",
        value_shape="str",
        allowed_purpose="caller_supplied_case_identity_for_human_review_traceability_only",
        forbidden_interpretation="must_not_be_used_to_read_files_lookup_runtime_state_or_fetch_records",
        description="Case identity is a primitive label supplied by the caller, not a storage key.",
    ),
    PilotContractFieldDesign(
        field_name="schema_version",
        direction="input",
        required_state="required_non_empty_string",
        value_shape="str",
        allowed_purpose="caller_supplied_contract_version_label",
        forbidden_interpretation="must_not_trigger_dynamic_schema_loading_or_imports",
        description="Schema version is a passive label for future validator checks.",
    ),
    PilotContractFieldDesign(
        field_name="user_request_summary",
        direction="input",
        required_state="required_non_empty_string",
        value_shape="str",
        allowed_purpose="caller_supplied_plain_language_request_summary",
        forbidden_interpretation="must_not_be_treated_as_executable_instruction_or_prompt_content",
        description="The summary is primitive text for later non-authoritative analysis only.",
    ),
    PilotContractFieldDesign(
        field_name="routing_context_public_summary",
        direction="input",
        required_state="required_string_may_be_empty_only_when_case_has_no_public_context",
        value_shape="str",
        allowed_purpose="public_metadata_summary_only",
        forbidden_interpretation="must_not_contain_runtime_router_state_or_internal_router_decision_objects",
        description="Routing context is limited to public metadata summaries, not internal state.",
    ),
    PilotContractFieldDesign(
        field_name="task_classification_hints_summary",
        direction="input",
        required_state="required_string_may_be_empty_when_no_hints_exist",
        value_shape="str",
        allowed_purpose="caller_supplied_task_classification_hint_summary_without_prompt_group_names",
        forbidden_interpretation="must_not_imply_prompt_selection_prompt_loading_or_prompt_library_awareness",
        description="This replaces unsafe prompt-group terminology with non-authoritative hint language.",
    ),
    PilotContractFieldDesign(
        field_name="current_router_outcome_summary",
        direction="input",
        required_state="required_string_may_be_empty_until_reproduction_harness_milestone",
        value_shape="str",
        allowed_purpose="caller_supplied_summary_for_future_comparison_design_only",
        forbidden_interpretation="must_not_call_or_import_the_live_router",
        description="Future comparison can use caller-supplied summaries only, not live router calls.",
    ),
    PilotContractFieldDesign(
        field_name="frozen_canon_constraints_summary",
        direction="input",
        required_state="required_non_empty_string",
        value_shape="str",
        allowed_purpose="caller_supplied_summary_of_frozen_constraints",
        forbidden_interpretation="must_not_read_freeze_memory_gold_files_or_prompt_library_files",
        description="Frozen constraints are supplied by the caller as primitive text.",
    ),
    PilotContractFieldDesign(
        field_name="known_boundary_flags",
        direction="input",
        required_state="required_tuple_of_strings_may_be_empty",
        value_shape="tuple[str, ...]",
        allowed_purpose="caller_supplied_boundary_flag_labels_for_human_review",
        forbidden_interpretation="must_not_trigger_route_execution_prompt_loading_or_activation",
        description="Boundary flags are passive labels for future human-review support.",
    ),
    PilotContractFieldDesign(
        field_name="caller_generated_timestamp_utc",
        direction="input",
        required_state="required_non_empty_string",
        value_shape="str",
        allowed_purpose="caller_supplied_timestamp_label",
        forbidden_interpretation="must_not_call_clock_network_or_filesystem",
        description="Timestamp is supplied by the caller so the future Pilot does not read environment state.",
    ),
)

_ALLOWED_OUTPUT_FIELDS: Final[tuple[PilotContractFieldDesign, ...]] = (
    PilotContractFieldDesign("pilot_record_kind", "output", "required_constant", "str", "identify_non_authoritative_projection_note_kind", "must_not_imply_route_decision_or_approval", "Future output kind is a fixed non-authoritative label."),
    PilotContractFieldDesign("case_id", "output", "required_echo_string", "str", "echo_input_case_id_for_human_traceability", "must_not_be_used_as_storage_or_lookup_key", "Output case id mirrors caller input only."),
    PilotContractFieldDesign("schema_version", "output", "required_constant_or_echo_string", "str", "identify_contract_version", "must_not_load_dynamic_schema", "Schema version remains a primitive label."),
    PilotContractFieldDesign("authority_notice", "output", "required_exact_string", "str", "state_non_authoritative_human_review_only", "must_not_be_the_only_safety_control", "Authority notice is mandatory but structural guards remain required."),
    PilotContractFieldDesign("projection_analysis_summary", "output", "required_string", "str", "descriptive_projection_analysis_for_human_review", "must_not_be_recommendation_final_route_or_route_approval", "Projection is descriptive, not prescriptive."),
    PilotContractFieldDesign("task_classification_projection_summary", "output", "required_string", "str", "descriptive_task_classification_projection_without_prompt_group_language", "must_not_select_suggest_or_load_prompts", "Task classification projection avoids prompt-loading terms."),
    PilotContractFieldDesign("reasoning_summary_for_human_review", "output", "required_string", "str", "human_readable_reasoning_summary", "must_not_record_human_decision_or_replace_human_review", "Reasoning is support material only."),
    PilotContractFieldDesign("boundary_flags_for_human_review", "output", "required_tuple_of_strings", "tuple[str, ...]", "passive_boundary_flag_labels", "must_not_trigger_automation", "Boundary flags remain passive and in-memory."),
    PilotContractFieldDesign("divergence_summary_for_human_review", "output", "required_string", "str", "descriptive_divergence_summary_after_taxonomy_exists", "must_not_claim_pilot_is_correct_when_it_differs", "Divergence wording is deferred to P3 taxonomy."),
    PilotContractFieldDesign("divergence_type", "output", "required_string_from_future_p3_taxonomy", "str", "taxonomy_bound_divergence_label", "must_not_invent_types_before_p3", "Divergence type must later be a member of the frozen P3 taxonomy."),
    PilotContractFieldDesign("missing_information_summary", "output", "required_string", "str", "explain_missing_context_for_human_review", "must_not_auto_fetch_context", "Missing information is reported, not fetched."),
    PilotContractFieldDesign("human_review_mandatory", "output", "required_constant_true", "bool", "make_human_review_non_suppressible", "must_not_be_false_optional_or_completed", "Human review remains mandatory and non-approving."),
    PilotContractFieldDesign("advisory_review_priority", "output", "required_string", "str", "human_review_priority_label_only", "must_not_authorize_execution_or_skip_review", "Review priority does not equal approval."),
    PilotContractFieldDesign("routing_effect", "output", "required_constant_none", "str", "assert_no_routing_effect", "must_not_be_computed_or_non_none", "Routing effect is fixed to none."),
    PilotContractFieldDesign("prompt_loading_effect", "output", "required_constant_none", "str", "assert_no_prompt_loading_effect", "must_not_be_computed_or_non_none", "Prompt loading effect is fixed to none."),
    PilotContractFieldDesign("runtime_effect", "output", "required_constant_none", "str", "assert_no_runtime_effect", "must_not_be_computed_or_non_none", "Runtime effect is fixed to none."),
    PilotContractFieldDesign("activation_effect", "output", "required_constant_none", "str", "assert_no_activation_effect", "must_not_be_computed_or_non_none", "Activation effect is fixed to none."),
    PilotContractFieldDesign("storage_status", "output", "required_constant_in_memory_only", "str", "assert_ephemeral_output", "must_not_be_persistent_cached_logged_or_serialized", "Storage status is fixed to in-memory only."),
)

_INPUT_VALIDATOR_RULES: Final[tuple[PilotValidatorRuleDesign, ...]] = (
    PilotValidatorRuleDesign("reject_unknown_input_keys", "input", "any_key_not_in_allowed_input_field_names", "reject_fail_closed", "Unknown keys can smuggle authority or live objects."),
    PilotValidatorRuleDesign("reject_missing_required_input_keys", "input", "required_field_absent", "reject_fail_closed", "Future validators must not invent missing case context."),
    PilotValidatorRuleDesign("reject_blank_required_strings", "input", "required_string_is_blank", "reject_fail_closed", "Blank required fields hide missing context."),
    PilotValidatorRuleDesign("reject_non_string_scalar_values", "input", "scalar_field_value_not_string", "reject_fail_closed", "Primitive string-only input prevents live object ingestion."),
    PilotValidatorRuleDesign("reject_non_tuple_boundary_flags", "input", "known_boundary_flags_not_tuple_of_strings", "reject_fail_closed", "Boundary flags must remain primitive labels."),
    PilotValidatorRuleDesign("reject_nested_objects", "input", "value_contains_dict_object_instance_or_nested_mutable_structure", "reject_fail_closed", "Nested objects can carry runtime state."),
    PilotValidatorRuleDesign("reject_callable_values", "input", "value_is_callable", "reject_fail_closed", "Callbacks would become execution hooks."),
    PilotValidatorRuleDesign("reject_file_handles", "input", "value_is_file_handle_or_stream", "reject_fail_closed", "File handles violate no file IO boundary."),
    PilotValidatorRuleDesign("reject_runtime_objects", "input", "value_resembles_router_prompt_registry_gold_or_provider_object", "reject_fail_closed", "Live project objects violate subsystem boundaries."),
    PilotValidatorRuleDesign("reject_path_or_url_execution_markers", "input", "string_contains_path_url_or_execution_marker", "reject_fail_closed", "Paths and URLs invite filesystem or network behavior."),
    PilotValidatorRuleDesign("reject_prompt_loading_instructions", "input", "string_requests_prompt_selection_loading_or_library_scan", "reject_fail_closed", "Prompt-loading leakage remains forbidden."),
    PilotValidatorRuleDesign("reject_route_execution_instructions", "input", "string_requests_route_execution_override_or_runtime_authority", "reject_fail_closed", "Routing remains authoritative outside Pilot."),
    PilotValidatorRuleDesign("reject_gold_registry_mutation_instructions", "input", "string_requests_gold_or_registry_write", "reject_fail_closed", "Gold and registry mutation remain forbidden."),
    PilotValidatorRuleDesign("reject_persistence_training_batch_activation_instructions", "input", "string_requests_persistence_training_batch_mode_or_activation", "reject_fail_closed", "Ephemeral opt-in non-training non-batch boundaries remain fixed."),
)

_OUTPUT_VALIDATOR_RULES: Final[tuple[PilotValidatorRuleDesign, ...]] = (
    PilotValidatorRuleDesign("reject_unknown_output_keys", "output", "any_key_not_in_allowed_output_field_names", "reject_fail_closed", "Unknown outputs can become automated actions."),
    PilotValidatorRuleDesign("reject_forbidden_output_names", "output", "any_output_key_in_forbidden_field_names", "reject_fail_closed", "Action-like names create authority drift."),
    PilotValidatorRuleDesign("require_exact_authority_notice", "output", "authority_notice_not_exact_future_constant", "reject_fail_closed", "Non-authority wording must be exact."),
    PilotValidatorRuleDesign("require_human_review_mandatory_true", "output", "human_review_mandatory_is_not_true", "reject_fail_closed", "Human review cannot be suppressed."),
    PilotValidatorRuleDesign("require_fixed_no_effect_constants", "output", "any_effect_field_not_exact_none", "reject_fail_closed", "Effect fields cannot become computed authority."),
    PilotValidatorRuleDesign("require_storage_status_in_memory_only", "output", "storage_status_not_in_memory_only", "reject_fail_closed", "Persistence remains forbidden."),
    PilotValidatorRuleDesign("require_divergence_type_from_p3_taxonomy", "output", "divergence_type_not_in_future_frozen_taxonomy", "reject_fail_closed", "Taxonomy must precede implementation."),
)

_FIXED_OUTPUT_INVARIANTS: Final[tuple[PilotOutputInvariantDesign, ...]] = (
    PilotOutputInvariantDesign("routing_effect_none", "routing_effect", ROUTING_EFFECT, "module_level_constant", "any_non_none_or_computed_value", "Pilot must never affect routing."),
    PilotOutputInvariantDesign("prompt_loading_effect_none", "prompt_loading_effect", PROMPT_LOADING_EFFECT, "module_level_constant", "any_non_none_or_computed_value", "Pilot must never load prompts."),
    PilotOutputInvariantDesign("runtime_effect_none", "runtime_effect", RUNTIME_EFFECT, "module_level_constant", "any_non_none_or_computed_value", "Pilot must never affect runtime."),
    PilotOutputInvariantDesign("activation_effect_none", "activation_effect", ACTIVATION_EFFECT, "module_level_constant", "any_non_none_or_computed_value", "Pilot must never activate Pilot or Copilot."),
    PilotOutputInvariantDesign("storage_status_in_memory_only", "storage_status", STORAGE_STATUS, "module_level_constant", "any_persistent_cached_logged_or_serialized_value", "Pilot output must remain ephemeral."),
    PilotOutputInvariantDesign("human_review_mandatory_true", "human_review_mandatory", "True", "module_level_constant", "False_or_optional_review", "Human review is mandatory and not approval."),
)

_FORBIDDEN_FIELD_NAMES: Final[tuple[PilotForbiddenNameDesign, ...]] = (
    PilotForbiddenNameDesign("candidate_prompt_groups", "prompt_loading_leakage", "input_output_fields", "use_task_classification_hints_summary", "Prompt-group wording implies prompt library awareness."),
    PilotForbiddenNameDesign("simulated_required_prompt_groups", "prompt_loading_leakage", "output_fields", "use_task_classification_projection_summary", "Required prompt-group wording implies prompt selection."),
    PilotForbiddenNameDesign("approved_route", "route_authority", "output_fields", "do_not_replace", "Approval wording delegates authority."),
    PilotForbiddenNameDesign("final_route", "route_authority", "output_fields", "do_not_replace", "Final-route wording suggests a decision."),
    PilotForbiddenNameDesign("execute_route", "route_execution", "input_output_fields", "do_not_replace", "Route execution is forbidden."),
    PilotForbiddenNameDesign("load_prompt", "prompt_loading", "input_output_fields", "do_not_replace", "Prompt loading is forbidden."),
    PilotForbiddenNameDesign("activate_pilot", "activation", "input_output_fields", "do_not_replace", "Pilot activation is forbidden."),
    PilotForbiddenNameDesign("activate_copilot", "activation", "input_output_fields", "do_not_replace", "Copilot activation is forbidden."),
    PilotForbiddenNameDesign("promote_candidate", "promotion", "input_output_fields", "do_not_replace", "Candidate promotion is forbidden."),
    PilotForbiddenNameDesign("write_gold", "mutation", "input_output_fields", "do_not_replace", "Gold mutation is forbidden."),
    PilotForbiddenNameDesign("write_registry", "mutation", "input_output_fields", "do_not_replace", "Registry mutation is forbidden."),
    PilotForbiddenNameDesign("record_human_decision", "human_review_authority", "input_output_fields", "do_not_replace", "Pilot must not record decisions."),
    PilotForbiddenNameDesign("persist_report", "persistence", "input_output_fields", "do_not_replace", "Persistence is forbidden."),
    PilotForbiddenNameDesign("runtime_authority", "runtime_authority", "input_output_fields", "do_not_replace", "Runtime authority is forbidden."),
    PilotForbiddenNameDesign("confidence", "false_precision", "output_fields", "use_advisory_review_priority_only", "Confidence scores can create overtrust."),
    PilotForbiddenNameDesign("score", "false_precision", "output_fields", "use_advisory_review_priority_only", "Scores can look like approval."),
    PilotForbiddenNameDesign("probability", "false_precision", "output_fields", "use_advisory_review_priority_only", "Probabilities can create overtrust."),
    PilotForbiddenNameDesign("recommendation", "recommendation_leakage", "output_fields", "use_projection_analysis_summary", "Pilot projects, it does not recommend."),
    PilotForbiddenNameDesign("suggested_route", "route_authority", "output_fields", "use_projection_analysis_summary", "Suggested route wording is prescriptive."),
    PilotForbiddenNameDesign("suggested_prompts", "prompt_loading_leakage", "output_fields", "do_not_replace", "Suggested prompt wording implies selection."),
    PilotForbiddenNameDesign("human_review_completed", "human_review_authority", "output_fields", "do_not_replace", "Pilot cannot complete review."),
    PilotForbiddenNameDesign("promotion_ready", "promotion", "output_fields", "do_not_replace", "Promotion readiness is not a Pilot output."),
    PilotForbiddenNameDesign("route_override", "route_execution", "input_output_fields", "do_not_replace", "Route override is forbidden."),
    PilotForbiddenNameDesign("prompt_to_load", "prompt_loading", "input_output_fields", "do_not_replace", "Prompt-to-load wording is direct prompt loading."),
    PilotForbiddenNameDesign("copilot_ready", "copilot_activation", "output_fields", "do_not_replace", "Copilot readiness requires P10/P11/P12 gates."),
    PilotForbiddenNameDesign("runtime_enabled", "runtime_activation", "output_fields", "do_not_replace", "Runtime enablement is outside P-series."),
    PilotForbiddenNameDesign("requires_human_review", "human_review_suppression", "output_fields", "use_human_review_mandatory", "A suppressible boolean may later become false."),
)

_CONTRACT_DESIGN_INVARIANTS: Final[tuple[str, ...]] = (
    "p2_is_design_only",
    "p2_defines_future_fields_and_validator_rules_only",
    "p2_does_not_implement_live_validation",
    "p2_does_not_process_input_payloads",
    "p2_does_not_generate_output_payloads",
    "allowed_inputs_are_primitive_strings_or_tuple_of_strings_only",
    "allowed_outputs_are_non_authoritative_human_review_support_only",
    "human_review_mandatory_is_fixed_true",
    "effect_fields_are_fixed_module_level_constants",
    "forbidden_field_names_are_banned_from_future_contract_payloads",
    "prompt_group_field_names_are_forbidden",
    "training_data_use_is_forbidden",
    "batch_mode_is_forbidden",
    "p3_taxonomy_required_before_divergence_type_use",
    "p6_gate_required_before_callable_projection",
)

_FORBIDDEN_OPERATIONS: Final[tuple[str, ...]] = (
    "implement_live_validator",
    "process_input_payloads",
    "generate_output_payloads",
    "run_pilot",
    "run_copilot",
    "implement_projection_logic",
    "execute_route_comparison",
    "select_route",
    "override_route",
    "execute_route",
    "select_prompt",
    "load_prompt",
    "scan_prompt_library",
    "import_runtime_router",
    "integrate_runtime_router",
    "read_project_source_tree",
    "write_files",
    "persist_output",
    "cache_output",
    "log_output",
    "write_report",
    "write_review_queue",
    "record_human_decision",
    "mutate_gold",
    "mutate_registry",
    "use_output_as_training_data",
    "run_batch_mode",
    "call_provider_or_model",
    "create_embeddings_or_vector_indexes",
    "activate_limited_shadow_runtime",
    "promote_candidate",
    "grant_runtime_authority",
)

_DESIGN = PilotIOContractValidatorDesign(
    feature_id=FEATURE_ID,
    schema_version=SCHEMA_VERSION,
    design_kind=DESIGN_KIND,
    milestone="P2",
    title="Routing Signal Scorer v3 Pilot Input Output Contract and Validator Design v1",
    authority_statement=AUTHORITY_STATEMENT,
    design_status="design_only",
    validator_status="design_only_no_live_validator",
    pilot_status="not_started_not_active",
    copilot_status="not_started_deferred",
    projection_status="not_implemented_blocked_until_p7_after_p6_gate",
    runtime_authority_status="not_granted",
    prompt_loading_authority_status="not_granted",
    persistence_authority_status="not_granted",
    training_data_use_status="forbidden",
    batch_mode_status="forbidden",
    limited_shadow_runtime_status="out_of_scope_separate_future_governed_scope_required",
    required_preconditions=_REQUIRED_PRECONDITIONS,
    allowed_input_fields=_ALLOWED_INPUT_FIELDS,
    allowed_output_fields=_ALLOWED_OUTPUT_FIELDS,
    input_validator_rules=_INPUT_VALIDATOR_RULES,
    output_validator_rules=_OUTPUT_VALIDATOR_RULES,
    fixed_output_invariants=_FIXED_OUTPUT_INVARIANTS,
    forbidden_field_names=_FORBIDDEN_FIELD_NAMES,
    contract_design_invariants=_CONTRACT_DESIGN_INVARIANTS,
    forbidden_operations=_FORBIDDEN_OPERATIONS,
    next_allowed_milestone=NEXT_ALLOWED_MILESTONE,
)


def build_pilot_io_contract_validator_design() -> PilotIOContractValidatorDesign:
    """Return the immutable static P2 Pilot I/O contract and validator design."""

    return _DESIGN


__all__ = (
    "AUTHORITY_STATEMENT",
    "ACTIVATION_EFFECT",
    "DESIGN_KIND",
    "FEATURE_ID",
    "HUMAN_REVIEW_MANDATORY",
    "NEXT_ALLOWED_MILESTONE",
    "PROMPT_LOADING_EFFECT",
    "ROUTING_EFFECT",
    "RUNTIME_EFFECT",
    "SCHEMA_VERSION",
    "STORAGE_STATUS",
    "PilotContractFieldDesign",
    "PilotForbiddenNameDesign",
    "PilotIOContractValidatorDesign",
    "PilotOutputInvariantDesign",
    "PilotValidatorRuleDesign",
    "build_pilot_io_contract_validator_design",
)
