"""M23 non-runtime shadow observation implementation.

M23 is the first implementation milestone after the design-only M18-M22
boundary chain. It builds a single in-memory shadow observation dictionary from
caller-supplied JSON-safe primitive data. It does not import runtime routing,
load prompts, read or write files, persist observations, compare routes,
activate shadow mode, start Auxiliar/Assistant behavior, or promote candidates.

The implementation is intentionally fail-closed: unknown fields, authority-like
field names, missing required fields, and non-primitive values are rejected
before an observation record is returned.
"""

from __future__ import annotations

from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_shadow_mode_non_runtime_observation_v1"
SCHEMA_VERSION: Final[str] = "3.64-shadow-mode-non-runtime-observation"
OBSERVATION_RECORD_KIND: Final[str] = "non_runtime_shadow_observation_v1"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M24 - Routing Signal Scorer v3 Shadow Observation Review Evidence Design v1"
)
AUTHORITY_NOTICE: Final[str] = (
    "This is non-runtime in-memory shadow observation evidence only. It has no routing effect, "
    "no prompt-loading effect, no persistence effect, no candidate-promotion effect, "
    "no runtime authority, and no Auxiliar/Assistant behavior."
)

_REQUIRED_FIELDS: Final[tuple[str, ...]] = (
    "routing_case_id",
    "user_request_summary",
    "current_router_summary",
)

_OPTIONAL_STRING_FIELDS: Final[tuple[str, ...]] = (
    "current_router_path_summary",
    "scorer_candidate_summary",
    "boundary_context_summary",
    "caller_generated_timestamp_utc",
)

_LIST_OF_STRING_FIELDS: Final[tuple[str, ...]] = (
    "current_prompt_group_summary",
    "scorer_constraint_flags_summary",
)

_ALLOWED_INPUT_FIELDS: Final[frozenset[str]] = frozenset(
    _REQUIRED_FIELDS + _OPTIONAL_STRING_FIELDS + _LIST_OF_STRING_FIELDS
)

_FORBIDDEN_AUTHORITY_FIELDS: Final[frozenset[str]] = frozenset(
    (
        "final_route",
        "route_override",
        "route_to_use",
        "selected_route",
        "selected_prompt",
        "prompt_to_load",
        "prompts_to_load",
        "approved",
        "enabled",
        "activated",
        "promoted",
        "assistant_ready",
        "auxiliar_ready",
        "candidate_promoted",
        "promotion_ready",
        "human_review_completed",
        "confidence",
        "score",
        "probability",
        "suggested_route",
        "suggested_prompts",
        "execute_patch",
        "write_gold",
        "write_registry",
        "write_freeze",
        "confirm_and_write",
    )
)

_REQUIRED_OUTPUT_FIELDS: Final[tuple[str, ...]] = (
    "observation_record_kind",
    "routing_case_id",
    "contract_schema_version",
    "authority_notice",
    "route_path_difference_observed",
    "constraint_flags_observed",
    "requires_separate_human_review",
    "human_review_reason_summary",
    "storage_status",
    "routing_effect",
    "prompt_loading_effect",
    "candidate_promotion_effect",
    "runtime_authority",
    "shadow_mode_status",
    "assistant_status",
)

_FIXED_NO_EFFECT_VALUE: Final[str] = "none"
_FIXED_NOT_GRANTED_VALUE: Final[str] = "not_granted"
_FIXED_NOT_ACTIVE_VALUE: Final[str] = "not_active"
_FIXED_NOT_STARTED_VALUE: Final[str] = "not_started"
_FIXED_NOT_PERSISTED_VALUE: Final[str] = "not_persisted_by_shadow_observation"


class ShadowObservationContractError(ValueError):
    """Raised when caller-supplied M23 input violates the non-runtime contract."""


def _fail(reason: str) -> None:
    raise ShadowObservationContractError(reason)


def _require_plain_input_dict(shadow_input: object) -> dict[str, object]:
    if type(shadow_input) is not dict:
        _fail("shadow_input_must_be_plain_dict")
    return shadow_input


def _require_allowed_keys(shadow_input: dict[str, object]) -> None:
    for key in shadow_input:
        if type(key) is not str:
            _fail("input_keys_must_be_strings")
        if key in _FORBIDDEN_AUTHORITY_FIELDS:
            _fail("authority_field_is_forbidden:" + key)
        if key not in _ALLOWED_INPUT_FIELDS:
            _fail("unknown_input_field:" + key)
    for required in _REQUIRED_FIELDS:
        if required not in shadow_input:
            _fail("missing_required_input_field:" + required)


def _require_string_field(shadow_input: dict[str, object], field_name: str) -> str:
    value = shadow_input[field_name]
    if type(value) is not str:
        _fail("input_field_must_be_string:" + field_name)
    if field_name in _REQUIRED_FIELDS and value.strip() == "":
        _fail("required_input_field_must_not_be_blank:" + field_name)
    return value


def _copy_optional_string_field(shadow_input: dict[str, object], field_name: str) -> str:
    if field_name not in shadow_input:
        return ""
    return _require_string_field(shadow_input, field_name)


def _copy_list_of_strings_field(shadow_input: dict[str, object], field_name: str) -> list[str]:
    if field_name not in shadow_input:
        return []
    value = shadow_input[field_name]
    if type(value) is not list:
        _fail("input_field_must_be_list_of_strings:" + field_name)
    copied: list[str] = []
    for item in value:
        if type(item) is not str:
            _fail("input_list_items_must_be_strings:" + field_name)
        copied.append(item)
    return copied


def _validated_shadow_input_copy(shadow_input: object) -> dict[str, object]:
    checked = _require_plain_input_dict(shadow_input)
    _require_allowed_keys(checked)
    copied: dict[str, object] = {
        "routing_case_id": _require_string_field(checked, "routing_case_id"),
        "user_request_summary": _require_string_field(checked, "user_request_summary"),
        "current_router_summary": _require_string_field(checked, "current_router_summary"),
    }
    for field_name in _OPTIONAL_STRING_FIELDS:
        if field_name in checked:
            copied[field_name] = _copy_optional_string_field(checked, field_name)
    for field_name in _LIST_OF_STRING_FIELDS:
        if field_name in checked:
            copied[field_name] = _copy_list_of_strings_field(checked, field_name)
    return copied


def _human_review_reason_summary(validated_input: dict[str, object]) -> str:
    reasons = [
        "non_runtime_shadow_observation_requires_separate_human_review",
        "m23_has_no_routing_prompt_loading_persistence_or_promotion_effect",
    ]
    if "scorer_candidate_summary" in validated_input:
        reasons.append("candidate_summary_present_as_non_authoritative_evidence")
    if validated_input.get("scorer_constraint_flags_summary", []):
        reasons.append("constraint_flags_present_as_non_authoritative_evidence")
    return "; ".join(reasons)


def build_non_runtime_shadow_observation(shadow_input: object) -> dict[str, object]:
    """Build one non-runtime in-memory shadow observation dictionary.

    The input must be a plain dictionary containing only M19-style
    caller-supplied JSON-safe primitive fields. The returned observation is
    non-authoritative evidence and must be stored or reviewed by a caller only
    through a separately governed future milestone.
    """

    validated_input = _validated_shadow_input_copy(shadow_input)
    constraint_flags = _copy_list_of_strings_field(
        validated_input,
        "scorer_constraint_flags_summary",
    )
    observation = {
        "observation_record_kind": OBSERVATION_RECORD_KIND,
        "routing_case_id": validated_input["routing_case_id"],
        "contract_schema_version": SCHEMA_VERSION,
        "authority_notice": AUTHORITY_NOTICE,
        "route_path_difference_observed": False,
        "constraint_flags_observed": constraint_flags,
        "requires_separate_human_review": True,
        "human_review_reason_summary": _human_review_reason_summary(validated_input),
        "storage_status": _FIXED_NOT_PERSISTED_VALUE,
        "routing_effect": _FIXED_NO_EFFECT_VALUE,
        "prompt_loading_effect": _FIXED_NO_EFFECT_VALUE,
        "candidate_promotion_effect": _FIXED_NO_EFFECT_VALUE,
        "runtime_authority": _FIXED_NOT_GRANTED_VALUE,
        "shadow_mode_status": _FIXED_NOT_ACTIVE_VALUE,
        "assistant_status": _FIXED_NOT_STARTED_VALUE,
    }
    return observation


__all__ = ["ShadowObservationContractError", "build_non_runtime_shadow_observation"]
