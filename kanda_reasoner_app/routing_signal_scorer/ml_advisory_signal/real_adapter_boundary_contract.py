# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/real_adapter_boundary_contract.py
"""Phase 5 offline real-adapter boundary contracts.

This module describes a possible future real adapter without enabling one.
It is intentionally descriptor-only, in-memory, non-runtime, and
non-authoritative. It cannot call providers, use credentials, read prompts,
read freeze memory, read router canon, persist reports, train models,
calibrate models, improve models, modify router logic, or select routes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


FEATURE_ID = "rss_ml_adv_phase5_offline_real_adapter_boundary_contract_v1"


class RealAdapterBoundaryStatus(str, Enum):
    """Finite statuses for the offline adapter boundary decision."""

    ACCEPTED_DESCRIPTOR_ONLY = "ACCEPTED_DESCRIPTOR_ONLY"
    REJECTED_FORBIDDEN_CAPABILITY = "REJECTED_FORBIDDEN_CAPABILITY"


@dataclass(frozen=True)
class RealAdapterDescriptor:
    """Descriptor for a possible future adapter, not an executable adapter."""

    adapter_label: str
    adapter_kind: str
    declared_input_contract_id: str
    declared_output_contract_id: str
    offline_descriptor_only: bool = True
    non_runtime: bool = True
    non_authoritative: bool = True
    adapter_execution_enabled: bool = False
    provider_calls_enabled: bool = False
    network_calls_enabled: bool = False
    api_keys_enabled: bool = False
    embeddings_enabled: bool = False
    vector_store_enabled: bool = False
    persistence_enabled: bool = False
    prompt_loading_enabled: bool = False
    prompt_library_read_enabled: bool = False
    freeze_memory_read_enabled: bool = False
    router_canon_read_enabled: bool = False
    router_prompt_logic_modified: bool = False
    router_final_selection_modified: bool = False
    route_authority_enabled: bool = False
    advisory_rankings_enabled: bool = False
    free_text_explanations_enabled: bool = False
    training_enabled: bool = False
    calibration_enabled: bool = False
    model_improvement_enabled: bool = False
    runtime_pilot_behavior_enabled: bool = False
    runtime_copilot_behavior_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("adapter_label", self.adapter_label)
        _require_text("adapter_kind", self.adapter_kind)
        _require_text("declared_input_contract_id", self.declared_input_contract_id)
        _require_text("declared_output_contract_id", self.declared_output_contract_id)
        if self.offline_descriptor_only is not True:
            raise ValueError("offline_descriptor_only must remain True")
        if self.non_runtime is not True:
            raise ValueError("non_runtime must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")


@dataclass(frozen=True)
class RealAdapterBoundaryDecision:
    """In-memory decision for a descriptor-only adapter boundary check."""

    feature_id: str
    adapter_label: str
    status: RealAdapterBoundaryStatus
    accepted: bool
    forbidden_capabilities: Tuple[str, ...]
    boundary_notes: Tuple[str, ...]
    offline_descriptor_only: bool = True
    non_runtime: bool = True
    non_authoritative: bool = True

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("feature_id", self.feature_id)
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 5 adapter boundary")
        _require_text("adapter_label", self.adapter_label)
        if not isinstance(self.status, RealAdapterBoundaryStatus):
            raise TypeError("status must be RealAdapterBoundaryStatus")
        if not isinstance(self.accepted, bool):
            raise TypeError("accepted must be bool")
        _require_tuple_of_text("forbidden_capabilities", self.forbidden_capabilities)
        _require_tuple_of_text("boundary_notes", self.boundary_notes)
        if self.accepted and self.forbidden_capabilities:
            raise ValueError("accepted decision cannot list forbidden capabilities")
        if self.status == RealAdapterBoundaryStatus.ACCEPTED_DESCRIPTOR_ONLY:
            if not self.accepted:
                raise ValueError("accepted descriptor-only status must be accepted")
        if self.status == RealAdapterBoundaryStatus.REJECTED_FORBIDDEN_CAPABILITY:
            if self.accepted:
                raise ValueError("rejected status cannot be accepted")
            if not self.forbidden_capabilities:
                raise ValueError("rejected status requires forbidden capabilities")
        if self.offline_descriptor_only is not True:
            raise ValueError("offline_descriptor_only must remain True")
        if self.non_runtime is not True:
            raise ValueError("non_runtime must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")


def evaluate_real_adapter_boundary(
    descriptor: RealAdapterDescriptor,
) -> RealAdapterBoundaryDecision:
    """Evaluate a descriptor without executing any adapter behavior."""

    if not isinstance(descriptor, RealAdapterDescriptor):
        raise TypeError("descriptor must be RealAdapterDescriptor")

    forbidden = _enabled_forbidden_capabilities(descriptor)
    notes = [
        "offline_descriptor_only",
        "no_adapter_execution",
        "no_provider_calls",
        "no_route_authority",
        "no_router_prompt_logic_change",
    ]

    if forbidden:
        return RealAdapterBoundaryDecision(
            feature_id=FEATURE_ID,
            adapter_label=descriptor.adapter_label,
            status=RealAdapterBoundaryStatus.REJECTED_FORBIDDEN_CAPABILITY,
            accepted=False,
            forbidden_capabilities=forbidden,
            boundary_notes=tuple(notes + ["forbidden_capability_rejected"]),
        )

    return RealAdapterBoundaryDecision(
        feature_id=FEATURE_ID,
        adapter_label=descriptor.adapter_label,
        status=RealAdapterBoundaryStatus.ACCEPTED_DESCRIPTOR_ONLY,
        accepted=True,
        forbidden_capabilities=(),
        boundary_notes=tuple(notes),
    )


def _enabled_forbidden_capabilities(
    descriptor: RealAdapterDescriptor,
) -> Tuple[str, ...]:
    """Support enabled forbidden capabilities behavior.
    
    Parameters
    ----------
    descriptor : RealAdapterDescriptor
        The descriptor value.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    forbidden_fields = (
        "adapter_execution_enabled",
        "provider_calls_enabled",
        "network_calls_enabled",
        "api_keys_enabled",
        "embeddings_enabled",
        "vector_store_enabled",
        "persistence_enabled",
        "prompt_loading_enabled",
        "prompt_library_read_enabled",
        "freeze_memory_read_enabled",
        "router_canon_read_enabled",
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_explanations_enabled",
        "training_enabled",
        "calibration_enabled",
        "model_improvement_enabled",
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
