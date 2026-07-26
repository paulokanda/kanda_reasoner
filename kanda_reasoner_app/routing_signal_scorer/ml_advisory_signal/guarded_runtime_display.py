# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/guarded_runtime_display.py
"""Read-only guarded runtime advisory display payload builder.

This is the first implementation-shaped Phase 6 display component. It builds
immutable telemetry payloads from already computed advisory output. It does
not execute ML, execute adapters, call providers, open the network, use API
keys, use embeddings, persist reports, read prompts, read prompt libraries,
read freeze memory, read router canon, mutate UI, modify router logic, modify
final route selection, or grant route authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .contract import (
    AdvisoryFlag,
    AdvisoryOutput,
    AdvisoryReasonCode,
    BoundaryStatus,
)
from .mock_advisor import MockAdvisor
from .contract import AdvisoryInput
from .output_firewall import validate_advisory_output


FEATURE_ID = (
    "rss_ml_adv_phase6_guarded_runtime_advisory_display_implementation_v1"
)


@dataclass(frozen=True)
class GuardedRuntimeAdvisoryDisplaySurfacePolicy:
    """Policy for read-only advisory telemetry payload construction."""

    surface_id: str
    display_label: str
    source_feature_id: str
    allowed_field_codes: Tuple[str, ...]
    allowed_failure_state_codes: Tuple[str, ...]
    max_flags: int = 4
    max_reason_codes: int = 6
    read_only: bool = True
    telemetry_only: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    removable_noop: bool = True
    runtime_display_implementation_enabled: bool = True
    runtime_telemetry_payload_builder_enabled: bool = True
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
    runtime_advisory_panel_enabled: bool = False
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
        
        _require_text("surface_id", self.surface_id)
        _require_text("display_label", self.display_label)
        _require_text("source_feature_id", self.source_feature_id)
        _require_tuple_of_text("allowed_field_codes", self.allowed_field_codes)
        _require_tuple_of_text(
            "allowed_failure_state_codes",
            self.allowed_failure_state_codes,
        )
        _require_positive_int("max_flags", self.max_flags)
        _require_positive_int("max_reason_codes", self.max_reason_codes)
        for field_name in _required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


@dataclass(frozen=True)
class GuardedRuntimeAdvisoryDisplayPayload:
    """Immutable read-only advisory telemetry payload."""

    feature_id: str
    surface_id: str
    display_label: str
    advisory_flags: Tuple[AdvisoryFlag, ...]
    advisory_reason_codes: Tuple[AdvisoryReasonCode, ...]
    boundary_status: BoundaryStatus
    advisory_should_abstain: bool
    non_authoritative_confidence: float
    advisory_source_kind: str
    visible_field_codes: Tuple[str, ...]
    display_failure_state_codes: Tuple[str, ...]
    read_only: bool = True
    telemetry_only: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    removable_noop: bool = True
    runtime_display_implementation_enabled: bool = True
    runtime_telemetry_payload_builder_enabled: bool = True
    runtime_advisory_panel_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    router_prompt_logic_modified: bool = False
    router_final_selection_modified: bool = False
    route_authority_enabled: bool = False
    advisory_rankings_enabled: bool = False
    free_text_explanations_enabled: bool = False
    runtime_copilot_behavior_enabled: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("feature_id", self.feature_id)
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 6 implementation")
        _require_text("surface_id", self.surface_id)
        _require_text("display_label", self.display_label)
        _require_tuple_of_enum(
            "advisory_flags",
            self.advisory_flags,
            AdvisoryFlag,
        )
        _require_tuple_of_enum(
            "advisory_reason_codes",
            self.advisory_reason_codes,
            AdvisoryReasonCode,
        )
        if not isinstance(self.boundary_status, BoundaryStatus):
            raise TypeError("boundary_status must be BoundaryStatus")
        if not isinstance(self.advisory_should_abstain, bool):
            raise TypeError("advisory_should_abstain must be bool")
        _require_score(
            "non_authoritative_confidence",
            self.non_authoritative_confidence,
        )
        _require_text("advisory_source_kind", self.advisory_source_kind)
        _require_tuple_of_text("visible_field_codes", self.visible_field_codes)
        _require_tuple_of_text(
            "display_failure_state_codes",
            self.display_failure_state_codes,
        )
        for field_name in _payload_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _payload_forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


def build_guarded_runtime_advisory_display_payload(
    policy: GuardedRuntimeAdvisoryDisplaySurfacePolicy,
    advisory_output: AdvisoryOutput,
) -> GuardedRuntimeAdvisoryDisplayPayload:
    """Build a bounded read-only advisory telemetry payload."""

    if not isinstance(policy, GuardedRuntimeAdvisoryDisplaySurfacePolicy):
        raise TypeError(
            "policy must be GuardedRuntimeAdvisoryDisplaySurfacePolicy"
        )
    if not isinstance(advisory_output, AdvisoryOutput):
        raise TypeError("advisory_output must be AdvisoryOutput")

    validate_advisory_output(advisory_output)
    flags = advisory_output.advisory_flags[:policy.max_flags]
    reasons = advisory_output.advisory_reason_codes[:policy.max_reason_codes]
    failure_codes = _build_failure_codes(policy, advisory_output)
    source_kind = "mock_advisor" if advisory_output.is_mock else "non_mock_advisor"

    payload = GuardedRuntimeAdvisoryDisplayPayload(
        feature_id=FEATURE_ID,
        surface_id=policy.surface_id,
        display_label=policy.display_label,
        advisory_flags=flags,
        advisory_reason_codes=reasons,
        boundary_status=advisory_output.boundary_status,
        advisory_should_abstain=advisory_output.advisory_should_abstain,
        non_authoritative_confidence=float(
            advisory_output.non_authoritative_confidence
        ),
        advisory_source_kind=source_kind,
        visible_field_codes=policy.allowed_field_codes,
        display_failure_state_codes=failure_codes,
    )
    validate_advisory_output(payload)
    return payload


def build_phase6_guarded_runtime_display_payload_probe(
) -> GuardedRuntimeAdvisoryDisplayPayload:
    """Build a safe in-memory display payload probe for tests."""

    policy = GuardedRuntimeAdvisoryDisplaySurfacePolicy(
        surface_id="phase6_read_only_telemetry_payload",
        display_label="phase6_guarded_runtime_advisory_display_v1",
        source_feature_id=FEATURE_ID,
        allowed_field_codes=(
            "advisory_flags",
            "advisory_reason_codes",
            "boundary_status",
            "advisory_should_abstain",
            "non_authoritative_confidence",
        ),
        allowed_failure_state_codes=(
            "advisor_abstained",
            "boundary_rejected",
            "display_payload_truncated",
        ),
    )
    advisory_input = AdvisoryInput(
        scenario_id="phase6_probe_synthetic_case",
        sanitized_context_hash="phase6_probe_hash",
        candidate_prompt_group_ids=("synthetic_group_alpha",),
        ambiguity_score=0.70,
        conflict_score=0.20,
        risk_family_id=None,
    )
    advisory_output = MockAdvisor().advise(advisory_input)
    return build_guarded_runtime_advisory_display_payload(
        policy,
        advisory_output,
    )


def _build_failure_codes(
    policy: GuardedRuntimeAdvisoryDisplaySurfacePolicy,
    advisory_output: AdvisoryOutput,
) -> Tuple[str, ...]:
    """Support build failure codes behavior.
    
    Parameters
    ----------
    policy : GuardedRuntimeAdvisoryDisplaySurfacePolicy
        The policy value.
    advisory_output : AdvisoryOutput
        The advisory output value.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    codes = []
    if advisory_output.advisory_should_abstain:
        codes.append("advisor_abstained")
    if advisory_output.boundary_status != BoundaryStatus.SAFE_NON_AUTHORITATIVE:
        codes.append("boundary_rejected")
    if len(advisory_output.advisory_flags) > policy.max_flags:
        codes.append("display_payload_truncated")
    if len(advisory_output.advisory_reason_codes) > policy.max_reason_codes:
        codes.append("display_payload_truncated")
    return tuple(dict.fromkeys(codes))


def _required_true_fields() -> Tuple[str, ...]:
    """Support required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "read_only",
        "telemetry_only",
        "route_invariant",
        "final_selection_invisible",
        "non_authoritative",
        "removable_noop",
        "runtime_display_implementation_enabled",
        "runtime_telemetry_payload_builder_enabled",
    )


def _payload_required_true_fields() -> Tuple[str, ...]:
    """Support payload required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "read_only",
        "telemetry_only",
        "route_invariant",
        "final_selection_invisible",
        "non_authoritative",
        "removable_noop",
        "runtime_display_implementation_enabled",
        "runtime_telemetry_payload_builder_enabled",
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
        "prompt_library_read_enabled",
        "prompt_registry_mutation_enabled",
        "freeze_memory_read_enabled",
        "freeze_memory_write_enabled",
        "router_canon_read_enabled",
        "runtime_shadow_mode_enabled",
        "runtime_advisory_panel_enabled",
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


def _payload_forbidden_true_fields() -> Tuple[str, ...]:
    """Support payload forbidden true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "runtime_advisory_panel_enabled",
        "runtime_ui_mutation_enabled",
        "router_prompt_logic_modified",
        "router_final_selection_modified",
        "route_authority_enabled",
        "advisory_rankings_enabled",
        "free_text_explanations_enabled",
        "runtime_copilot_behavior_enabled",
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


def _require_score(name: str, value: float) -> None:
    """Support require score behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : float
        The input value.
    """
    
    if not isinstance(value, (float, int)) or isinstance(value, bool):
        raise TypeError(name + " must be number")
    if float(value) < 0.0 or float(value) > 1.0:
        raise ValueError(name + " must be between 0.0 and 1.0")


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


def _require_tuple_of_enum(name: str, value: tuple, enum_type: type) -> None:
    """Support require tuple of enum behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : tuple
        The input value.
    enum_type : type
        The enum type value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(name + " must be tuple")
    for item in value:
        if not isinstance(item, enum_type):
            raise TypeError(name + " contains invalid enum")
