# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/real_adapter_candidate_contract.py
"""Phase 5 offline real-adapter candidate contracts.

This module defines only an offline, fixture-bound candidate envelope for a
possible future real adapter. It is not an adapter implementation. It never
executes a model, calls a provider, opens the network, uses credentials, uses
embeddings, reads prompts, reads freeze memory, reads router canon, persists
reports, trains, calibrates, modifies router logic, or selects routes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from .real_adapter_boundary_contract import RealAdapterBoundaryDecision


FEATURE_ID = "rss_ml_adv_phase5_offline_real_adapter_candidate_contract_v1"


class RealAdapterCandidateStatus(str, Enum):
    """Finite statuses for offline candidate boundary decisions."""

    ACCEPTED_OFFLINE_CANDIDATE = "ACCEPTED_OFFLINE_CANDIDATE"
    REJECTED_BOUNDARY_DECISION = "REJECTED_BOUNDARY_DECISION"
    REJECTED_FORBIDDEN_CAPABILITY = "REJECTED_FORBIDDEN_CAPABILITY"


@dataclass(frozen=True)
class RealAdapterCandidateDescriptor:
    """Descriptor for a fixture-bound offline real-adapter candidate."""

    candidate_label: str
    candidate_family: str
    boundary_decision: RealAdapterBoundaryDecision
    declared_fixture_scope: str
    declared_evaluation_contract_id: str
    allowed_output_contract_id: str
    allowed_reason_codes: Tuple[str, ...]
    offline_fixture_bound_only: bool = True
    offline_descriptor_only: bool = True
    non_runtime: bool = True
    non_authoritative: bool = True
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
    prompt_library_read_enabled: bool = False
    prompt_registry_mutation_enabled: bool = False
    freeze_memory_read_enabled: bool = False
    freeze_memory_write_enabled: bool = False
    router_canon_read_enabled: bool = False
    router_prompt_logic_modified: bool = False
    router_final_selection_modified: bool = False
    route_authority_enabled: bool = False
    advisory_rankings_enabled: bool = False
    free_text_explanations_enabled: bool = False
    training_enabled: bool = False
    calibration_enabled: bool = False
    model_improvement_enabled: bool = False
    runtime_shadow_mode_enabled: bool = False
    runtime_pilot_behavior_enabled: bool = False
    runtime_copilot_behavior_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("candidate_label", self.candidate_label)
        _require_text("candidate_family", self.candidate_family)
        if not isinstance(self.boundary_decision, RealAdapterBoundaryDecision):
            raise TypeError("boundary_decision must be RealAdapterBoundaryDecision")
        _require_text("declared_fixture_scope", self.declared_fixture_scope)
        _require_text(
            "declared_evaluation_contract_id",
            self.declared_evaluation_contract_id,
        )
        _require_text("allowed_output_contract_id", self.allowed_output_contract_id)
        _require_tuple_of_text("allowed_reason_codes", self.allowed_reason_codes)
        if self.offline_fixture_bound_only is not True:
            raise ValueError("offline_fixture_bound_only must remain True")
        if self.offline_descriptor_only is not True:
            raise ValueError("offline_descriptor_only must remain True")
        if self.non_runtime is not True:
            raise ValueError("non_runtime must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")


@dataclass(frozen=True)
class RealAdapterCandidateDecision:
    """In-memory decision for a candidate descriptor boundary check."""

    feature_id: str
    candidate_label: str
    status: RealAdapterCandidateStatus
    accepted: bool
    forbidden_capabilities: Tuple[str, ...]
    boundary_notes: Tuple[str, ...]
    offline_fixture_bound_only: bool = True
    offline_descriptor_only: bool = True
    non_runtime: bool = True
    non_authoritative: bool = True

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("feature_id", self.feature_id)
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 5 candidate contract")
        _require_text("candidate_label", self.candidate_label)
        if not isinstance(self.status, RealAdapterCandidateStatus):
            raise TypeError("status must be RealAdapterCandidateStatus")
        if not isinstance(self.accepted, bool):
            raise TypeError("accepted must be bool")
        _require_tuple_of_text("forbidden_capabilities", self.forbidden_capabilities)
        _require_tuple_of_text("boundary_notes", self.boundary_notes)
        if self.accepted and self.forbidden_capabilities:
            raise ValueError("accepted decision cannot list forbidden capabilities")
        if self.status == RealAdapterCandidateStatus.ACCEPTED_OFFLINE_CANDIDATE:
            if not self.accepted:
                raise ValueError("accepted candidate status must be accepted")
        if self.status != RealAdapterCandidateStatus.ACCEPTED_OFFLINE_CANDIDATE:
            if self.accepted:
                raise ValueError("rejected status cannot be accepted")
            if not self.forbidden_capabilities:
                raise ValueError("rejected status requires forbidden capabilities")
        if self.offline_fixture_bound_only is not True:
            raise ValueError("offline_fixture_bound_only must remain True")
        if self.offline_descriptor_only is not True:
            raise ValueError("offline_descriptor_only must remain True")
        if self.non_runtime is not True:
            raise ValueError("non_runtime must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")


def evaluate_real_adapter_candidate(
    descriptor: RealAdapterCandidateDescriptor,
) -> RealAdapterCandidateDecision:
    """Evaluate a candidate descriptor without executing an adapter."""

    if not isinstance(descriptor, RealAdapterCandidateDescriptor):
        raise TypeError("descriptor must be RealAdapterCandidateDescriptor")

    notes = [
        "offline_fixture_bound_only",
        "offline_descriptor_only",
        "no_candidate_execution",
        "no_provider_calls",
        "no_route_authority",
        "no_router_prompt_logic_change",
    ]

    if not descriptor.boundary_decision.accepted:
        return RealAdapterCandidateDecision(
            feature_id=FEATURE_ID,
            candidate_label=descriptor.candidate_label,
            status=RealAdapterCandidateStatus.REJECTED_BOUNDARY_DECISION,
            accepted=False,
            forbidden_capabilities=("boundary_decision_not_accepted",),
            boundary_notes=tuple(notes + ["boundary_decision_rejected"]),
        )

    forbidden = _enabled_forbidden_capabilities(descriptor)
    if forbidden:
        return RealAdapterCandidateDecision(
            feature_id=FEATURE_ID,
            candidate_label=descriptor.candidate_label,
            status=RealAdapterCandidateStatus.REJECTED_FORBIDDEN_CAPABILITY,
            accepted=False,
            forbidden_capabilities=forbidden,
            boundary_notes=tuple(notes + ["forbidden_capability_rejected"]),
        )

    return RealAdapterCandidateDecision(
        feature_id=FEATURE_ID,
        candidate_label=descriptor.candidate_label,
        status=RealAdapterCandidateStatus.ACCEPTED_OFFLINE_CANDIDATE,
        accepted=True,
        forbidden_capabilities=(),
        boundary_notes=tuple(notes),
    )


def _enabled_forbidden_capabilities(
    descriptor: RealAdapterCandidateDescriptor,
) -> Tuple[str, ...]:
    """Support enabled forbidden capabilities behavior.
    
    Parameters
    ----------
    descriptor : RealAdapterCandidateDescriptor
        The descriptor value.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    forbidden_fields = (
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
        "prompt_library_read_enabled",
        "prompt_registry_mutation_enabled",
        "freeze_memory_read_enabled",
        "freeze_memory_write_enabled",
        "router_canon_read_enabled",
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_explanations_enabled",
        "training_enabled",
        "calibration_enabled",
        "model_improvement_enabled",
        "runtime_shadow_mode_enabled",
        "runtime_pilot_behavior_enabled",
        "runtime_copilot_behavior_enabled",
    )
    enabled = []
    for field_name in forbidden_fields:
        value = getattr(descriptor, field_name)
        if not isinstance(value, bool):
            raise TypeError(f"{field_name} must be bool")
        if value:
            enabled.append(field_name)
    return tuple(enabled)


def _require_text(name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


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
        raise TypeError(f"{name} must be tuple")
    for item in value:
        _require_text(name, item)
