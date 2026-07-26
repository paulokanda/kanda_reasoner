# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_surface_wiring.py
"""Read-only Phase 7 advisory surface wiring implementation.

This module implements a bounded in-memory envelope builder. It may attach an
already-built guarded advisory display payload to a separate telemetry surface
section after a canonical dispatch snapshot already exists. It does not call the
router, execute advisors, execute adapters, call providers, read prompt assets,
read freeze memory, read router canon, persist data, mutate UI, activate an
advisory panel, alter final selection, or grant authority to ML.
"""

from __future__ import annotations


__all__ = [
    'build_phase7_read_only_surface_wiring_probe',
    'build_read_only_advisory_surface_wiring_envelope',
    'CanonicalDispatchSnapshot',
    'ReadOnlyAdvisorySurfaceWiringEnvelope',
    'ReadOnlyAdvisorySurfaceWiringPolicy',
    'ReadOnlySurfaceAttachmentState',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from .guarded_runtime_display import (
    GuardedRuntimeAdvisoryDisplayPayload,
    build_phase6_guarded_runtime_display_payload_probe,
)
from .output_firewall import validate_advisory_output


FEATURE_ID = "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_v1"
SOURCE_REVIEW_FEATURE_ID = "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1"


class ReadOnlySurfaceAttachmentState(str, Enum):
    """State codes for the read-only surface envelope."""

    ATTACHED_READ_ONLY = "ATTACHED_READ_ONLY"
    DISABLED_NOOP = "DISABLED_NOOP"
    FAIL_OPEN_NO_ADVISORY = "FAIL_OPEN_NO_ADVISORY"


@dataclass(frozen=True)
class CanonicalDispatchSnapshot:
    """Immutable caller-supplied snapshot of the already-final canonical output."""

    canonical_result_id: str
    canonical_dispatch_label: str
    final_selection_hash: str
    final_selection_locked: bool = True

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("canonical_result_id", self.canonical_result_id)
        _require_text("canonical_dispatch_label", self.canonical_dispatch_label)
        _require_text("final_selection_hash", self.final_selection_hash)
        if self.final_selection_locked is not True:
            raise ValueError("final_selection_locked must remain True")


@dataclass(frozen=True)
class ReadOnlyAdvisorySurfaceWiringPolicy:
    """Policy for safe in-memory advisory surface envelope construction."""

    surface_id: str
    surface_label: str
    source_review_feature_id: str
    allowed_surface_section_codes: Tuple[str, ...]
    enabled: bool = True
    max_surface_sections: int = 6
    read_only: bool = True
    telemetry_only: bool = True
    route_invariant: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    copies_canonical_snapshot_unchanged: bool = True
    consumes_already_computed_display_payload_only: bool = True
    separate_surface_section_only: bool = True
    no_free_text_route_advice: bool = True
    no_advisory_rankings: bool = True
    disable_noop_control_enabled: bool = True
    non_training_feedback_only: bool = True
    real_ml_enabled: bool = False
    adapter_execution_enabled: bool = False
    candidate_execution_enabled: bool = False
    provider_calls_enabled: bool = False
    network_calls_enabled: bool = False
    api_keys_enabled: bool = False
    embeddings_enabled: bool = False
    vector_store_enabled: bool = False
    persistence_enabled: bool = False
    report_persistence_enabled: bool = False
    prompt_loading_enabled: bool = False
    prompt_registry_mutation_enabled: bool = False
    prompt_library_read_enabled: bool = False
    freeze_memory_read_enabled: bool = False
    freeze_memory_write_enabled: bool = False
    router_canon_read_enabled: bool = False
    runtime_shadow_mode_enabled: bool = False
    runtime_advisory_panel_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    runtime_telemetry_surface_wired: bool = False
    router_prompt_logic_modified: bool = False
    router_final_selection_modified: bool = False
    route_authority_enabled: bool = False
    advisory_rankings_enabled: bool = False
    free_text_route_advice_enabled: bool = False
    free_text_explanations_enabled: bool = False
    training_enabled: bool = False
    calibration_enabled: bool = False
    model_improvement_enabled: bool = False
    runtime_pilot_behavior_enabled: bool = False
    runtime_copilot_decision_behavior_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("surface_id", self.surface_id)
        _require_text("surface_label", self.surface_label)
        if self.source_review_feature_id != SOURCE_REVIEW_FEATURE_ID:
            raise ValueError("source_review_feature_id must match Phase 7 review gate")
        _require_tuple_of_text("allowed_surface_section_codes", self.allowed_surface_section_codes)
        _require_positive_int("max_surface_sections", self.max_surface_sections)
        for field_name in _policy_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


@dataclass(frozen=True)
class ReadOnlyAdvisorySurfaceWiringEnvelope:
    """Immutable output envelope that keeps canonical and advisory sections separate."""

    feature_id: str
    surface_id: str
    surface_label: str
    attachment_state: ReadOnlySurfaceAttachmentState
    canonical_snapshot_before: CanonicalDispatchSnapshot
    canonical_snapshot_after: CanonicalDispatchSnapshot
    advisory_display_payload: Optional[GuardedRuntimeAdvisoryDisplayPayload]
    visible_surface_section_codes: Tuple[str, ...]
    failure_state_codes: Tuple[str, ...]
    non_training_feedback_slot_enabled: bool = True
    read_only: bool = True
    telemetry_only: bool = True
    route_invariant: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    runtime_advisory_panel_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    runtime_telemetry_surface_wired: bool = False
    router_prompt_logic_modified: bool = False
    router_final_selection_modified: bool = False
    route_authority_enabled: bool = False
    advisory_rankings_enabled: bool = False
    free_text_route_advice_enabled: bool = False
    free_text_explanations_enabled: bool = False
    runtime_pilot_behavior_enabled: bool = False
    runtime_copilot_decision_behavior_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 7 read-only wiring implementation")
        _require_text("surface_id", self.surface_id)
        _require_text("surface_label", self.surface_label)
        if not isinstance(self.attachment_state, ReadOnlySurfaceAttachmentState):
            raise TypeError("attachment_state must be ReadOnlySurfaceAttachmentState")
        if not isinstance(self.canonical_snapshot_before, CanonicalDispatchSnapshot):
            raise TypeError("canonical_snapshot_before must be CanonicalDispatchSnapshot")
        if not isinstance(self.canonical_snapshot_after, CanonicalDispatchSnapshot):
            raise TypeError("canonical_snapshot_after must be CanonicalDispatchSnapshot")
        if self.canonical_snapshot_before != self.canonical_snapshot_after:
            raise ValueError("canonical snapshots must remain unchanged")
        if self.advisory_display_payload is not None:
            if not isinstance(self.advisory_display_payload, GuardedRuntimeAdvisoryDisplayPayload):
                raise TypeError("advisory_display_payload must be guarded display payload or None")
            validate_advisory_output(self.advisory_display_payload)
        _require_tuple_of_text("visible_surface_section_codes", self.visible_surface_section_codes)
        _require_tuple_of_text("failure_state_codes", self.failure_state_codes)
        for field_name in _envelope_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _envelope_forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


def build_read_only_advisory_surface_wiring_envelope(
    policy: ReadOnlyAdvisorySurfaceWiringPolicy,
    canonical_snapshot: CanonicalDispatchSnapshot,
    advisory_display_payload: object | None,
) -> ReadOnlyAdvisorySurfaceWiringEnvelope:
    """Build a separate read-only advisory surface envelope.

    The canonical snapshot is copied through unchanged. Advisory data must already
    be computed and already firewall-valid. Invalid or missing advisory data
    fails open without changing the canonical snapshot.
    """

    if not isinstance(policy, ReadOnlyAdvisorySurfaceWiringPolicy):
        raise TypeError("policy must be ReadOnlyAdvisorySurfaceWiringPolicy")
    if not isinstance(canonical_snapshot, CanonicalDispatchSnapshot):
        raise TypeError("canonical_snapshot must be CanonicalDispatchSnapshot")

    if not policy.enabled:
        return _build_envelope(policy, canonical_snapshot, None, ReadOnlySurfaceAttachmentState.DISABLED_NOOP, ("disabled_noop",))

    if advisory_display_payload is None:
        return _build_envelope(policy, canonical_snapshot, None, ReadOnlySurfaceAttachmentState.FAIL_OPEN_NO_ADVISORY, ("missing_advisory_payload",))

    if not isinstance(advisory_display_payload, GuardedRuntimeAdvisoryDisplayPayload):
        return _build_envelope(policy, canonical_snapshot, None, ReadOnlySurfaceAttachmentState.FAIL_OPEN_NO_ADVISORY, ("invalid_advisory_payload",))

    try:
        validate_advisory_output(advisory_display_payload)
    except Exception:
        return _build_envelope(policy, canonical_snapshot, None, ReadOnlySurfaceAttachmentState.FAIL_OPEN_NO_ADVISORY, ("advisory_payload_rejected",))

    return _build_envelope(policy, canonical_snapshot, advisory_display_payload, ReadOnlySurfaceAttachmentState.ATTACHED_READ_ONLY, ())


def build_phase7_read_only_surface_wiring_probe() -> ReadOnlyAdvisorySurfaceWiringEnvelope:
    """Build a safe in-memory probe for validation tests."""

    policy = ReadOnlyAdvisorySurfaceWiringPolicy(
        surface_id="phase7_read_only_surface_envelope",
        surface_label="phase7_read_only_advisory_surface_wiring_v1",
        source_review_feature_id=SOURCE_REVIEW_FEATURE_ID,
        allowed_surface_section_codes=(
            "canonical_snapshot",
            "advisory_display_payload",
            "attachment_state",
            "failure_state_codes",
            "non_training_feedback_slot",
        ),
    )
    snapshot = CanonicalDispatchSnapshot(
        canonical_result_id="synthetic_canonical_result_001",
        canonical_dispatch_label="governed_router_completed",
        final_selection_hash="synthetic_final_selection_hash_001",
    )
    payload = build_phase6_guarded_runtime_display_payload_probe()
    return build_read_only_advisory_surface_wiring_envelope(policy, snapshot, payload)


def _build_envelope(
    policy: ReadOnlyAdvisorySurfaceWiringPolicy,
    snapshot: CanonicalDispatchSnapshot,
    payload: Optional[GuardedRuntimeAdvisoryDisplayPayload],
    state: ReadOnlySurfaceAttachmentState,
    failure_codes: Tuple[str, ...],
) -> ReadOnlyAdvisorySurfaceWiringEnvelope:
    """Support build envelope behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisorySurfaceWiringPolicy
        The policy value.
    snapshot : CanonicalDispatchSnapshot
        The snapshot value.
    payload : Optional[GuardedRuntimeAdvisoryDisplayPayload]
        The payload value.
    state : ReadOnlySurfaceAttachmentState
        The state value.
    failure_codes : Tuple[str, ...]
        The failure codes value.
    
    Returns
    -------
    ReadOnlyAdvisorySurfaceWiringEnvelope
        The read only advisory surface wiring envelope result.
    """
    
    return ReadOnlyAdvisorySurfaceWiringEnvelope(
        feature_id=FEATURE_ID,
        surface_id=policy.surface_id,
        surface_label=policy.surface_label,
        attachment_state=state,
        canonical_snapshot_before=snapshot,
        canonical_snapshot_after=snapshot,
        advisory_display_payload=payload,
        visible_surface_section_codes=policy.allowed_surface_section_codes[: policy.max_surface_sections],
        failure_state_codes=failure_codes,
    )


def _policy_required_true_fields() -> Tuple[str, ...]:
    """Support policy required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "read_only",
        "telemetry_only",
        "route_invariant",
        "in_memory_only",
        "bounded",
        "fail_open",
        "removable_noop",
        "final_selection_invisible",
        "non_authoritative",
        "copies_canonical_snapshot_unchanged",
        "consumes_already_computed_display_payload_only",
        "separate_surface_section_only",
        "no_free_text_route_advice",
        "no_advisory_rankings",
        "disable_noop_control_enabled",
        "non_training_feedback_only",
    )


def _envelope_required_true_fields() -> Tuple[str, ...]:
    """Support envelope required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "non_training_feedback_slot_enabled",
        "read_only",
        "telemetry_only",
        "route_invariant",
        "in_memory_only",
        "bounded",
        "fail_open",
        "removable_noop",
        "final_selection_invisible",
        "non_authoritative",
    )


def _forbidden_true_fields() -> Tuple[str, ...]:
    """Support forbidden true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "real_ml_enabled",
        "adapter_execution_enabled",
        "candidate_execution_enabled",
        "provider_calls_enabled",
        "network_calls_enabled",
        "api_keys_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "report_persistence_enabled",
        "prompt_loading_enabled",
        "prompt_registry_mutation_enabled",
        "prompt_library_read_enabled",
        "freeze_memory_read_enabled",
        "freeze_memory_write_enabled",
        "router_canon_read_enabled",
        "runtime_shadow_mode_enabled",
        "runtime_advisory_panel_enabled",
        "runtime_ui_mutation_enabled",
        "runtime_telemetry_surface_wired",
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_route_advice_enabled",
        "free_text_explanations_enabled",
        "training_enabled",
        "calibration_enabled",
        "model_improvement_enabled",
        "runtime_pilot_behavior_enabled",
        "runtime_copilot_decision_behavior_enabled",
    )


def _envelope_forbidden_true_fields() -> Tuple[str, ...]:
    """Support envelope forbidden true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "runtime_advisory_panel_enabled",
        "runtime_ui_mutation_enabled",
        "runtime_telemetry_surface_wired",
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_route_advice_enabled",
        "free_text_explanations_enabled",
        "runtime_pilot_behavior_enabled",
        "runtime_copilot_decision_behavior_enabled",
    )


def _require_text(name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str):
        raise TypeError(name + " must be str")
    if not value.strip():
        raise ValueError(name + " must not be empty")


def _require_positive_int(name: str, value: int) -> None:
    """Support require positive int behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : int
        The input value.
    """
    
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(name + " must be int")
    if value < 1:
        raise ValueError(name + " must be positive")


def _require_tuple_of_text(name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple of text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[str, ...]
        The input value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(name + " must be tuple")
    for item in value:
        _require_text(name + " item", item)
