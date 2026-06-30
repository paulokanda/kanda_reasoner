# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_auxiliar_assistant_non_runtime_assistance.py
"""M31 non-runtime Auxiliar/Assistant assistance implementation.

M31 introduces a narrow in-memory helper for non-authoritative human-review
support. It accepts only caller-supplied JSON-safe primitive input matching the
M27 contract shape, performs local fail-closed contract checks, and returns one
in-memory assistance record.

This is not live Assistant behavior, not Auxiliar behavior, not shadow-mode
activation, not runtime routing integration, not route comparison, not route
selection, not prompt selection or loading, not persistence, not human decision
recording, not a provider/model call, not embeddings, and not candidate
promotion. The helper has no file I/O, console I/O, network access, subprocess
use, dynamic import, runtime authority, or project mutation authority.
"""

from __future__ import annotations

from typing import Final

FEATURE_ID: Final[str] = "routing_signal_scorer_v3_auxiliar_assistant_non_runtime_assistance_v1"
SCHEMA_VERSION: Final[str] = "3.72-auxiliar-assistant-non-runtime-assistance"
ASSISTANCE_RECORD_KIND: Final[str] = "non_runtime_auxiliar_assistant_assistance_v1"
NEXT_ALLOWED_MILESTONE: Final[str] = (
    "M32 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Review Evidence Design v1"
)
AUTHORITY_NOTICE: Final[str] = (
    "This is non-runtime in-memory Auxiliar/Assistant human-review support only. "
    "It has no routing effect, no route-selection effect, no prompt-loading effect, "
    "no persistence effect, no human-decision effect, no candidate-promotion effect, "
    "no shadow-mode activation effect, no Assistant activation effect, no runtime "
    "authority, and no Copilot/Pilot behavior."
)

_REQUIRED_STRING_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "assistant_case_id",
        "boundary_context_summary",
        "validated_shadow_observation_summary",
        "review_evidence_summary",
        "current_router_outcome_summary",
        "requested_support_kind",
        "caller_generated_timestamp_utc",
    }
)
_OPTIONAL_STRING_FIELDS: Final[frozenset[str]] = frozenset({"known_boundary_flags_summary"})
_ALLOWED_INPUT_FIELDS: Final[frozenset[str]] = _REQUIRED_STRING_FIELDS | _OPTIONAL_STRING_FIELDS
_ALLOWED_SUPPORT_KINDS: Final[frozenset[str]] = frozenset(
    {
        "boundary_review",
        "evidence_summary",
        "safety_question_generation",
        "missing_information_review",
    }
)
_FORBIDDEN_AUTHORITY_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "final_route",
        "route_override",
        "route_to_use",
        "selected_route",
        "selected_prompt",
        "prompt_to_load",
        "prompts_to_load",
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
        "human_review_completed",
        "human_decision",
        "human_decision_recorded",
        "confidence",
        "score",
        "probability",
        "recommendation",
        "suggested_route",
        "suggested_prompts",
        "execute_patch",
        "write_gold",
        "write_registry",
        "write_review_queue",
        "write_freeze",
        "confirm_and_write",
        "persist_record",
        "router_authority_granted",
        "runtime_effect",
    }
)
_OUTPUT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "assistance_record_kind",
        "assistant_case_id",
        "contract_schema_version",
        "authority_notice",
        "human_review_context_summary",
        "boundary_questions_for_human_review",
        "safety_flags_for_human_review",
        "missing_information_summary",
        "requires_separate_human_review",
        "storage_status",
        "routing_effect",
        "prompt_loading_effect",
        "assistant_activation_effect",
    }
)


class AuxiliarAssistantAssistanceContractError(ValueError):
    """Raised when caller-supplied M31 assistance input violates the local contract."""


def _validate_mapping(payload: object) -> dict[str, object]:
    """Support validate mapping behavior.
    
    Parameters
    ----------
    payload : object
        The payload value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    if not isinstance(payload, dict):
        raise AuxiliarAssistantAssistanceContractError("input_must_be_dict")
    validated: dict[str, object] = {}
    for key, value in payload.items():
        if not isinstance(key, str):
            raise AuxiliarAssistantAssistanceContractError("input_keys_must_be_strings")
        if key in _FORBIDDEN_AUTHORITY_FIELDS:
            raise AuxiliarAssistantAssistanceContractError(f"authority_field_is_forbidden:{key}")
        if key not in _ALLOWED_INPUT_FIELDS:
            raise AuxiliarAssistantAssistanceContractError(f"unknown_input_field:{key}")
        validated[key] = value
    return validated


def _required_string(payload: dict[str, object], key: str) -> str:
    """Support required string behavior.
    
    Parameters
    ----------
    payload : dict[str, object]
        The payload value.
    key : str
        The key value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if key not in payload:
        raise AuxiliarAssistantAssistanceContractError(f"missing_required_input_field:{key}")
    value = payload[key]
    if not isinstance(value, str):
        raise AuxiliarAssistantAssistanceContractError(f"input_field_must_be_string:{key}")
    if not value.strip():
        raise AuxiliarAssistantAssistanceContractError(f"required_input_field_must_not_be_blank:{key}")
    return value


def _optional_string(payload: dict[str, object], key: str) -> str:
    """Support optional string behavior.
    
    Parameters
    ----------
    payload : dict[str, object]
        The payload value.
    key : str
        The key value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if key not in payload:
        return ""
    value = payload[key]
    if not isinstance(value, str):
        raise AuxiliarAssistantAssistanceContractError(f"input_field_must_be_string:{key}")
    return value


def _validate_requested_support_kind(value: str) -> str:
    """Support validate requested support kind behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    normalized = value.strip()
    if normalized not in _ALLOWED_SUPPORT_KINDS:
        raise AuxiliarAssistantAssistanceContractError(
            f"unsupported_non_authoritative_support_kind:{normalized}"
        )
    return normalized


def _build_human_review_context(
    assistant_case_id: str,
    requested_support_kind: str,
    boundary_context_summary: str,
    review_evidence_summary: str,
    current_router_outcome_summary: str,
) -> str:
    """Support build human review context behavior.
    
    Parameters
    ----------
    assistant_case_id : str
        The assistant case id value.
    requested_support_kind : str
        The requested support kind value.
    boundary_context_summary : str
        The boundary context summary value.
    review_evidence_summary : str
        The review evidence summary value.
    current_router_outcome_summary : str
        The current router outcome summary value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return (
        "Non-runtime Auxiliar/Assistant support envelope for human review only. "
        f"Case `{assistant_case_id}` requested `{requested_support_kind}` support. "
        "Boundary context, review evidence, and current router outcome are caller-supplied summaries only. "
        f"Boundary context: {boundary_context_summary} "
        f"Review evidence: {review_evidence_summary} "
        f"Current router outcome: {current_router_outcome_summary} "
        "No route, prompt, persistence, activation, candidate-promotion, or human-decision action was taken."
    )


def _build_boundary_questions(requested_support_kind: str) -> tuple[str, ...]:
    """Support build boundary questions behavior.
    
    Parameters
    ----------
    requested_support_kind : str
        The requested support kind value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    common = (
        "Does the human reviewer agree that this assistance record is non-authoritative evidence only?",
        "Is any separate governed patch, freeze, route, prompt, or human-decision action required outside this helper?",
    )
    kind_specific = {
        "boundary_review": (
            "Which boundary, if any, needs separate human clarification before a later governed milestone?",
        ),
        "evidence_summary": (
            "Is the supplied evidence summary sufficient for human review without additional source discovery?",
        ),
        "safety_question_generation": (
            "Which safety question should be answered by a human before any governed continuation?",
        ),
        "missing_information_review": (
            "What information is missing and must be supplied externally before any governed continuation?",
        ),
    }
    return common + kind_specific[requested_support_kind]


def _build_safety_flags(known_boundary_flags_summary: str) -> tuple[str, ...]:
    """Support build safety flags behavior.
    
    Parameters
    ----------
    known_boundary_flags_summary : str
        The known boundary flags summary value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    base = (
        "non_runtime_in_memory_assistance_only",
        "requires_separate_human_review",
        "no_routing_effect",
        "no_route_selection_effect",
        "no_prompt_loading_effect",
        "no_persistence_effect",
        "no_human_decision_effect",
        "no_candidate_promotion_effect",
        "no_shadow_mode_activation_effect",
        "no_assistant_activation_effect",
        "no_runtime_authority",
    )
    if known_boundary_flags_summary.strip():
        return base + ("caller_supplied_boundary_flags_present_for_human_review",)
    return base


def _build_missing_information_summary(
    requested_support_kind: str,
    known_boundary_flags_summary: str,
) -> str:
    """Support build missing information summary behavior.
    
    Parameters
    ----------
    requested_support_kind : str
        The requested support kind value.
    known_boundary_flags_summary : str
        The known boundary flags summary value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if requested_support_kind == "missing_information_review":
        return (
            "Human reviewer must determine missing information from the caller-supplied summaries; "
            "this helper does not scan files, discover cases, or inspect runtime state."
        )
    if known_boundary_flags_summary.strip():
        return (
            "Caller supplied boundary flags for human review. No missing information was inferred by this helper."
        )
    return "No missing information was inferred; this helper does not perform source discovery."


def _assert_output_contract(record: dict[str, object]) -> None:
    """Support assert output contract behavior.
    
    Parameters
    ----------
    record : dict[str, object]
        The record value.
    """
    
    keys = set(record)
    if keys != _OUTPUT_FIELDS:
        raise AuxiliarAssistantAssistanceContractError("output_contract_shape_violation")
    for key in keys:
        if key in _FORBIDDEN_AUTHORITY_FIELDS:
            raise AuxiliarAssistantAssistanceContractError(f"forbidden_output_field:{key}")


def build_non_runtime_auxiliar_assistant_assistance(payload: object) -> dict[str, object]:
    """Build one in-memory, non-authoritative M31 assistance record.

    The function accepts only caller-supplied primitive strings matching the M27
    assistance contract. It does not read files, discover cases, inspect runtime
    state, call models, compare routes, select prompts, persist records, record
    human decisions, activate shadow mode, start Assistant behavior, or promote
    candidates.
    """

    data = _validate_mapping(payload)
    assistant_case_id = _required_string(data, "assistant_case_id")
    boundary_context_summary = _required_string(data, "boundary_context_summary")
    validated_shadow_observation_summary = _required_string(
        data, "validated_shadow_observation_summary"
    )
    review_evidence_summary = _required_string(data, "review_evidence_summary")
    current_router_outcome_summary = _required_string(data, "current_router_outcome_summary")
    requested_support_kind = _validate_requested_support_kind(
        _required_string(data, "requested_support_kind")
    )
    _required_string(data, "caller_generated_timestamp_utc")
    known_boundary_flags_summary = _optional_string(data, "known_boundary_flags_summary")

    context_summary = _build_human_review_context(
        assistant_case_id=assistant_case_id,
        requested_support_kind=requested_support_kind,
        boundary_context_summary=boundary_context_summary,
        review_evidence_summary=review_evidence_summary,
        current_router_outcome_summary=current_router_outcome_summary,
    )
    if validated_shadow_observation_summary.strip():
        context_summary = (
            context_summary
            + " Validated shadow observation summary: "
            + validated_shadow_observation_summary
        )

    record: dict[str, object] = {
        "assistance_record_kind": ASSISTANCE_RECORD_KIND,
        "assistant_case_id": assistant_case_id,
        "contract_schema_version": SCHEMA_VERSION,
        "authority_notice": AUTHORITY_NOTICE,
        "human_review_context_summary": context_summary,
        "boundary_questions_for_human_review": _build_boundary_questions(requested_support_kind),
        "safety_flags_for_human_review": _build_safety_flags(known_boundary_flags_summary),
        "missing_information_summary": _build_missing_information_summary(
            requested_support_kind, known_boundary_flags_summary
        ),
        "requires_separate_human_review": True,
        "storage_status": "not_persisted_by_auxiliar_assistant_assistance",
        "routing_effect": "none",
        "prompt_loading_effect": "none",
        "assistant_activation_effect": "none",
    }
    _assert_output_contract(record)
    return record


__all__ = [
    "AuxiliarAssistantAssistanceContractError",
    "build_non_runtime_auxiliar_assistant_assistance",
]
