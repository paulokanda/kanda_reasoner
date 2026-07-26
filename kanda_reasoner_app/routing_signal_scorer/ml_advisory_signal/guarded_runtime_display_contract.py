# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/guarded_runtime_display_contract.py
"""Phase 6 guarded runtime advisory display contracts.

This module defines only a contract for a future guarded display surface. It is
not a runtime display implementation. It never executes a model, calls a
provider, opens the network, uses credentials, uses embeddings, reads prompts,
reads freeze memory, reads router canon, persists reports, trains, calibrates,
modifies router logic, changes final route selection, or grants route authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


FEATURE_ID = "rss_ml_adv_phase6_guarded_runtime_advisory_display_contract_v1"


class GuardedRuntimeAdvisoryDisplayStatus(str, Enum):
    """Finite statuses for guarded display contract decisions."""

    ACCEPTED_CONTRACT_ONLY = "ACCEPTED_CONTRACT_ONLY"
    REJECTED_REQUIRED_GUARD_MISSING = "REJECTED_REQUIRED_GUARD_MISSING"
    REJECTED_FORBIDDEN_CAPABILITY = "REJECTED_FORBIDDEN_CAPABILITY"


@dataclass(frozen=True)
class GuardedRuntimeAdvisoryDisplayPolicy:
    """Policy descriptor for a future read-only telemetry surface."""

    display_label: str
    source_contract_id: str
    prerequisite_feature_id: str
    allowed_surface: str
    allowed_display_fields: Tuple[str, ...]
    allowed_failure_states: Tuple[str, ...]
    contract_only: bool = True
    read_only: bool = True
    telemetry_only: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    removable_noop: bool = True
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
    runtime_shadow_mode_enabled: bool = False
    runtime_display_implementation_enabled: bool = False
    runtime_advisory_panel_enabled: bool = False
    runtime_telemetry_surface_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
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
        
        _require_text("display_label", self.display_label)
        _require_text("source_contract_id", self.source_contract_id)
        _require_text("prerequisite_feature_id", self.prerequisite_feature_id)
        _require_text("allowed_surface", self.allowed_surface)
        _require_tuple_of_text("allowed_display_fields", self.allowed_display_fields)
        _require_tuple_of_text("allowed_failure_states", self.allowed_failure_states)
        if self.contract_only is not True:
            raise ValueError("contract_only must remain True")
        if self.read_only is not True:
            raise ValueError("read_only must remain True")
        if self.telemetry_only is not True:
            raise ValueError("telemetry_only must remain True")
        if self.route_invariant is not True:
            raise ValueError("route_invariant must remain True")
        if self.final_selection_invisible is not True:
            raise ValueError("final_selection_invisible must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")
        if self.removable_noop is not True:
            raise ValueError("removable_noop must remain True")


@dataclass(frozen=True)
class GuardedRuntimeAdvisoryDisplayDecision:
    """In-memory decision for a guarded display contract check."""

    feature_id: str
    display_label: str
    status: GuardedRuntimeAdvisoryDisplayStatus
    accepted: bool
    forbidden_capabilities: Tuple[str, ...]
    boundary_notes: Tuple[str, ...]
    contract_only: bool = True
    read_only: bool = True
    telemetry_only: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    runtime_display_enabled: bool = False
    runtime_advisory_panel_enabled: bool = False
    route_authority_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("feature_id", self.feature_id)
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 6 display contract")
        _require_text("display_label", self.display_label)
        if not isinstance(self.status, GuardedRuntimeAdvisoryDisplayStatus):
            raise TypeError("status must be GuardedRuntimeAdvisoryDisplayStatus")
        if not isinstance(self.accepted, bool):
            raise TypeError("accepted must be bool")
        _require_tuple_of_text("forbidden_capabilities", self.forbidden_capabilities)
        _require_tuple_of_text("boundary_notes", self.boundary_notes)
        if self.accepted and self.forbidden_capabilities:
            raise ValueError("accepted decision cannot list forbidden capabilities")
        if self.status == GuardedRuntimeAdvisoryDisplayStatus.ACCEPTED_CONTRACT_ONLY:
            if not self.accepted:
                raise ValueError("accepted contract status must be accepted")
        if self.status != GuardedRuntimeAdvisoryDisplayStatus.ACCEPTED_CONTRACT_ONLY:
            if self.accepted:
                raise ValueError("rejected status cannot be accepted")
            if not self.forbidden_capabilities:
                raise ValueError("rejected status requires forbidden capabilities")
        if self.contract_only is not True:
            raise ValueError("contract_only must remain True")
        if self.read_only is not True:
            raise ValueError("read_only must remain True")
        if self.telemetry_only is not True:
            raise ValueError("telemetry_only must remain True")
        if self.route_invariant is not True:
            raise ValueError("route_invariant must remain True")
        if self.final_selection_invisible is not True:
            raise ValueError("final_selection_invisible must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")
        if self.runtime_display_enabled is not False:
            raise ValueError("runtime_display_enabled must remain False in contract phase")
        if self.runtime_advisory_panel_enabled is not False:
            raise ValueError("runtime_advisory_panel_enabled must remain False")
        if self.route_authority_enabled is not False:
            raise ValueError("route_authority_enabled must remain False")


def evaluate_guarded_runtime_display_contract(
    policy: GuardedRuntimeAdvisoryDisplayPolicy,
) -> GuardedRuntimeAdvisoryDisplayDecision:
    """Evaluate a display contract without implementing runtime display."""

    if not isinstance(policy, GuardedRuntimeAdvisoryDisplayPolicy):
        raise TypeError("policy must be GuardedRuntimeAdvisoryDisplayPolicy")

    required = _missing_required_guards(policy)
    notes = (
        "contract_only",
        "read_only",
        "telemetry_only",
        "route_invariant",
        "final_selection_invisible",
        "removable_noop",
        "no_runtime_display_implementation",
        "no_route_authority",
    )
    if required:
        return GuardedRuntimeAdvisoryDisplayDecision(
            feature_id=FEATURE_ID,
            display_label=policy.display_label,
            status=GuardedRuntimeAdvisoryDisplayStatus.REJECTED_REQUIRED_GUARD_MISSING,
            accepted=False,
            forbidden_capabilities=required,
            boundary_notes=notes + ("required_guard_missing",),
        )

    forbidden = _enabled_forbidden_capabilities(policy)
    if forbidden:
        return GuardedRuntimeAdvisoryDisplayDecision(
            feature_id=FEATURE_ID,
            display_label=policy.display_label,
            status=GuardedRuntimeAdvisoryDisplayStatus.REJECTED_FORBIDDEN_CAPABILITY,
            accepted=False,
            forbidden_capabilities=forbidden,
            boundary_notes=notes + ("forbidden_capability_rejected",),
        )

    return GuardedRuntimeAdvisoryDisplayDecision(
        feature_id=FEATURE_ID,
        display_label=policy.display_label,
        status=GuardedRuntimeAdvisoryDisplayStatus.ACCEPTED_CONTRACT_ONLY,
        accepted=True,
        forbidden_capabilities=(),
        boundary_notes=notes,
    )


def _missing_required_guards(
    policy: GuardedRuntimeAdvisoryDisplayPolicy,
) -> Tuple[str, ...]:
    """Support missing required guards behavior.
    
    Parameters
    ----------
    policy : GuardedRuntimeAdvisoryDisplayPolicy
        The policy value.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    required_true_fields = (
        "contract_only",
        "read_only",
        "telemetry_only",
        "route_invariant",
        "final_selection_invisible",
        "non_authoritative",
        "removable_noop",
    )
    return tuple(
        field_name for field_name in required_true_fields
        if getattr(policy, field_name) is not True
    )


def _enabled_forbidden_capabilities(
    policy: GuardedRuntimeAdvisoryDisplayPolicy,
) -> Tuple[str, ...]:
    """Support enabled forbidden capabilities behavior.
    
    Parameters
    ----------
    policy : GuardedRuntimeAdvisoryDisplayPolicy
        The policy value.
    
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
        "runtime_shadow_mode_enabled",
        "runtime_display_implementation_enabled",
        "runtime_advisory_panel_enabled",
        "runtime_telemetry_surface_enabled",
        "runtime_ui_mutation_enabled",
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
    return tuple(
        field_name for field_name in forbidden_fields
        if getattr(policy, field_name) is not False
    )


def _require_text(field_name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    field_name : str
        The field name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str):
        raise TypeError(field_name + " must be str")
    if not value.strip():
        raise ValueError(field_name + " must not be empty")


def _require_tuple_of_text(field_name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple of text behavior.
    
    Parameters
    ----------
    field_name : str
        The field name value.
    value : Tuple[str, ...]
        The input value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(field_name + " must be tuple")
    for item in value:
        _require_text(field_name + " item", item)
