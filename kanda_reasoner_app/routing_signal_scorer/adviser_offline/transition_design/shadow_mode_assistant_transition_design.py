# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/transition_design/shadow_mode_assistant_transition_design.py
"""Design-only Shadow Mode / Assistant transition plan.

M17 is the first post-Adviser phase milestone. It does not implement shadow
mode, Assistant behavior, runtime routing, candidate promotion, or any side
effecting machinery. It only returns a deterministic in-memory design record
that future work can review under separate governance.

Authority boundary:
- design-only;
- standard library only;
- pure over caller-supplied mappings;
- no file I/O;
- no case discovery;
- no source scanning;
- no prompt auto-loading;
- no artifact I/O;
- no persistence;
- no registry writer, scratch writer, run writer, or gate writer;
- no gold mutation;
- no candidate promotion;
- no shadow-mode enablement;
- no Assistant behavior;
- no model, provider, network, embedding, vector, or dependency behavior;
- no runtime router authority.
"""

from __future__ import annotations


__all__ = [
    'assert_shadow_mode_assistant_transition_design_valid',
    'build_shadow_mode_assistant_transition_design',
    'validate_shadow_mode_assistant_transition_design',
]
import hashlib
import json
from collections.abc import Mapping
from typing import Any

FEATURE_ID = "routing_signal_scorer_v3_shadow_mode_assistant_transition_design_v1"
SCHEMA_VERSION = "3.58-shadow-mode-assistant-transition-design"
DESIGN_KIND = "post_adviser_shadow_mode_assistant_transition_design_only"
AUTHORITY_STATEMENT = "design_only_no_runtime_authority"
RUNTIME_POLICY = "runtime_enablement_forbidden"
NEXT_PHASE = "future_governed_shadow_mode_design_review_only"

_FORBIDDEN_FLAGS = (
    "may_enable_shadow_mode",
    "may_enable_assistant_behavior",
    "may_promote_candidate",
    "may_mutate_gold",
    "may_persist_transition_record",
    "may_write_runtime_config",
    "may_modify_router",
    "may_auto_load_prompts",
    "may_call_provider",
    "may_use_embeddings",
)


def build_shadow_mode_assistant_transition_design(
    *,
    promotion_gate_report: Mapping[str, Any] | None = None,
    transition_policy: Mapping[str, Any] | None = None,
    design_id: str = "shadow-mode-assistant-transition-design-not-persisted",
    prepared_by: str = "human-review-pending",
) -> dict[str, object]:
    """Return a deterministic in-memory post-Adviser transition design record.

    All inputs are supplied by the caller. This function does not read files,
    discover cases, modify router code, persist anything, run a candidate, or
    grant any runtime authority.
    """

    if promotion_gate_report is not None and not isinstance(promotion_gate_report, Mapping):
        raise TypeError("promotion_gate_report must be a mapping when supplied")
    if transition_policy is not None and not isinstance(transition_policy, Mapping):
        raise TypeError("transition_policy must be a mapping when supplied")

    promotion_gate_report = promotion_gate_report or {}
    transition_policy = transition_policy or {}

    gate_decision = str(promotion_gate_report.get("gate_decision", "not_supplied"))
    gate_next_step = str(promotion_gate_report.get("next_allowed_step", "not_supplied"))
    gate_runtime_authority = str(promotion_gate_report.get("router_authority", "none"))

    eligible_for_design_review = (
        gate_decision == "eligible_for_future_shadow_mode_design_review_only"
        and gate_next_step == "future_governed_shadow_mode_design_review_only"
        and gate_runtime_authority == "none"
    )

    boundaries = {
        "design_only": True,
        "runtime_enablement": "forbidden",
        "shadow_mode_enablement": "forbidden",
        "assistant_behavior_enablement": "forbidden",
        "router_authority": "none",
        "candidate_promotion": "not_allowed",
        "gold_mutation": "not_allowed",
        "file_io": "forbidden",
        "source_scanning": "forbidden",
        "prompt_auto_loading": "forbidden",
        "provider_calls": "forbidden",
        "embeddings_or_vectors": "forbidden",
        "persistence": "forbidden",
    }

    required_future_governance = [
        "separate_shadow_mode_design_freeze",
        "separate_runtime_boundary_review",
        "separate_human_confirmation_for_any_runtime_wire",
        "separate_validation_for_no_prompt_auto_loading_or_router_authority",
        "separate rollback and kill-switch design before any shadow run",
    ]

    record: dict[str, object] = {
        "feature_id": FEATURE_ID,
        "schema_version": SCHEMA_VERSION,
        "design_kind": DESIGN_KIND,
        "authority_statement": AUTHORITY_STATEMENT,
        "design_id": str(design_id),
        "prepared_by": str(prepared_by),
        "phase_transition": "adviser_closed_to_future_shadow_mode_design_review_only",
        "source_policy": "caller_supplied_m16_gate_report_only_no_discovery",
        "runtime_policy": RUNTIME_POLICY,
        "router_authority": "none",
        "candidate_promotion": "not_performed",
        "shadow_mode_authority": "not_granted",
        "assistant_behavior_authority": "not_granted",
        "eligible_for_future_shadow_mode_design_review": eligible_for_design_review,
        "next_allowed_step": NEXT_PHASE,
        "future_phase_requires_separate_governance": True,
        "transition_boundaries": boundaries,
        "required_future_governance": required_future_governance,
        "promotion_gate_summary": {
            "gate_decision": gate_decision,
            "next_allowed_step": gate_next_step,
            "router_authority": gate_runtime_authority,
            "candidate_promotion": str(promotion_gate_report.get("candidate_promotion", "not_supplied")),
            "shadow_mode_authority": str(promotion_gate_report.get("shadow_mode_authority", "not_supplied")),
        },
        "policy_summary": _policy_summary(transition_policy),
        "closure_statement": "m17_design_only_no_runtime_enablement",
    }
    for flag in _FORBIDDEN_FLAGS:
        record[flag] = False
    record["design_hash"] = _hash_record_without_field(record, "design_hash")
    return record


def validate_shadow_mode_assistant_transition_design(record: Mapping[str, Any]) -> dict[str, object]:
    """Validate a design-only post-Adviser transition record."""

    errors: list[str] = []
    if not isinstance(record, Mapping):
        return {"ok": False, "errors": ["record must be a mapping"]}

    for field in (
        "feature_id",
        "schema_version",
        "design_kind",
        "authority_statement",
        "runtime_policy",
        "router_authority",
        "candidate_promotion",
        "shadow_mode_authority",
        "assistant_behavior_authority",
        "next_allowed_step",
        "future_phase_requires_separate_governance",
        "transition_boundaries",
        "required_future_governance",
        "design_hash",
    ):
        if field not in record:
            errors.append(f"missing {field}")

    if record.get("feature_id") != FEATURE_ID:
        errors.append("feature_id mismatch")
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if record.get("design_kind") != DESIGN_KIND:
        errors.append("design_kind mismatch")
    if record.get("authority_statement") != AUTHORITY_STATEMENT:
        errors.append("authority_statement mismatch")
    if record.get("runtime_policy") != RUNTIME_POLICY:
        errors.append("runtime_policy must forbid runtime enablement")
    if record.get("router_authority") != "none":
        errors.append("router_authority must be none")
    if record.get("candidate_promotion") != "not_performed":
        errors.append("candidate_promotion must not be performed")
    if record.get("shadow_mode_authority") != "not_granted":
        errors.append("shadow_mode_authority must not be granted")
    if record.get("assistant_behavior_authority") != "not_granted":
        errors.append("assistant_behavior_authority must not be granted")
    if record.get("next_allowed_step") != NEXT_PHASE:
        errors.append("next_allowed_step must be future governed design review only")
    if record.get("future_phase_requires_separate_governance") is not True:
        errors.append("future_phase_requires_separate_governance must be true")

    for flag in _FORBIDDEN_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{flag} must be false")

    boundaries = record.get("transition_boundaries")
    if not isinstance(boundaries, Mapping):
        errors.append("transition_boundaries must be a mapping")
    else:
        for boundary, expected in (
            ("runtime_enablement", "forbidden"),
            ("shadow_mode_enablement", "forbidden"),
            ("assistant_behavior_enablement", "forbidden"),
            ("router_authority", "none"),
            ("file_io", "forbidden"),
            ("prompt_auto_loading", "forbidden"),
            ("provider_calls", "forbidden"),
            ("embeddings_or_vectors", "forbidden"),
            ("persistence", "forbidden"),
        ):
            if boundaries.get(boundary) != expected:
                errors.append(f"transition boundary {boundary} must be {expected}")

    required = record.get("required_future_governance")
    if not isinstance(required, list) or len(required) < 3:
        errors.append("required_future_governance must be a non-empty list")
    elif "separate_human_confirmation_for_any_runtime_wire" not in required:
        errors.append("runtime wiring must require separate human confirmation")

    if "design_hash" in record:
        expected = _hash_record_without_field(record, "design_hash")
        if record.get("design_hash") != expected:
            errors.append("design_hash mismatch")

    return {"ok": not errors, "errors": errors}


def assert_shadow_mode_assistant_transition_design_valid(record: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return record when valid; raise ValueError otherwise."""

    result = validate_shadow_mode_assistant_transition_design(record)
    if not result["ok"]:
        raise ValueError("; ".join(str(error) for error in result["errors"]))
    return record


def _policy_summary(policy: Mapping[str, Any]) -> dict[str, object]:
    """Support policy summary behavior.
    
    Parameters
    ----------
    policy : Mapping[str, Any]
        The policy value.
    
    Returns
    -------
    dict[str, object]
        The mapped values.
    """
    
    return {
        "policy_version": str(policy.get("policy_version", "not_supplied")),
        "requires_human_confirmation": policy.get("requires_human_confirmation", True) is True,
        "requires_separate_shadow_design_freeze": policy.get("requires_separate_shadow_design_freeze", True) is True,
        "requires_runtime_boundary_review": policy.get("requires_runtime_boundary_review", True) is True,
        "allows_runtime_enablement_in_m17": False,
    }


def _hash_record_without_field(record: Mapping[str, Any], field: str) -> str:
    """Support hash record without field behavior.
    
    Parameters
    ----------
    record : Mapping[str, Any]
        The record value.
    field : str
        The field value.
    
    Returns
    -------
    str
        The string result.
    """
    
    payload = {key: value for key, value in record.items() if key != field}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
