# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_runtime_activation.py
"""Phase 9 read-only advisory panel runtime activation implementation.

This module implements a guarded in-memory runtime activation envelope for a
future visible read-only advisory panel. It does not render UI, mount a panel,
mutate UI, wire telemetry into app runtime surfaces, call the router, call an
advisor, execute adapters, call providers, persist data, influence routes, or
grant ML route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase9_read_only_panel_runtime_activation_implementation_probe',
    'build_read_only_advisory_panel_runtime_activation_envelope',
    'ReadOnlyAdvisoryPanelRuntimeActivationEnvelope',
    'ReadOnlyPanelRuntimeActivationEnvelopeState',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from .read_only_advisory_panel_ui import (
    ReadOnlyAdvisoryPanelUIState,
    ReadOnlyAdvisoryPanelViewModel,
    build_phase8_read_only_advisory_panel_ui_probe,
)


FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1"
SOURCE_REVIEW_FEATURE_ID = "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_result_review_gate_v1"


class ReadOnlyPanelRuntimeActivationEnvelopeState(str, Enum):
    """Safe in-memory activation-envelope states."""

    DISABLED_NOOP = "disabled_noop"
    FAIL_OPEN_NO_VIEW_MODEL = "fail_open_no_view_model"
    BLOCKED_UNSAFE_VIEW_MODEL = "blocked_unsafe_view_model"
    READY_READ_ONLY_ACTIVATION_ENVELOPE = "ready_read_only_activation_envelope"


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeActivationPolicy:
    """Policy for building a safe runtime activation envelope.

    The feature flag is intentionally default-off. Enabling the flag may only
    produce an in-memory activation envelope; it still cannot mount a panel,
    activate a renderer, mutate UI, wire runtime telemetry, or influence routing.
    """

    activation_surface_id: str
    activation_surface_label: str
    source_review_feature_id: str = SOURCE_REVIEW_FEATURE_ID
    enabled: bool = True
    feature_flag_name: str = "ml_advisory_read_only_panel_runtime_visible"
    feature_flag_enabled: bool = False
    feature_flag_default_enabled: bool = False
    require_phase8_panel_view_model_input: bool = True
    require_disable_noop_control: bool = True
    require_fail_open_on_missing_view_model: bool = True
    require_route_invariant_activation: bool = True
    require_final_selection_invisible_activation: bool = True
    require_renderer_adapter_to_be_separate_future_contract: bool = True
    require_non_training_feedback_slot: bool = True
    allow_runtime_activation_envelope: bool = True
    allow_actual_runtime_panel_activation: bool = False
    allow_renderer_activation: bool = False
    allow_mounted_panel: bool = False
    allow_runtime_ui_mutation: bool = False
    allow_runtime_telemetry_surface_wiring: bool = False
    allow_route_influence: bool = False
    allow_route_authority: bool = False
    allow_router_calls: bool = False
    allow_advisor_calls: bool = False
    allow_adapter_execution: bool = False
    allow_provider_calls: bool = False
    allow_persistence: bool = False
    allow_prompt_loading: bool = False
    allow_prompt_registry_mutation: bool = False
    allow_prompt_library_read: bool = False
    allow_freeze_memory_read: bool = False
    allow_freeze_memory_write: bool = False
    allow_router_canon_read: bool = False
    allow_route_override_button: bool = False
    allow_use_ml_route_button: bool = False
    allow_best_route_claim: bool = False
    allow_prompt_ranking: bool = False
    allow_advisory_ranking: bool = False
    allow_free_text_route_advice: bool = False
    allow_free_text_explanations: bool = False
    allow_runtime_copilot_decision_behavior: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("activation_surface_id", self.activation_surface_id)
        _require_text("activation_surface_label", self.activation_surface_label)
        _require_text("feature_flag_name", self.feature_flag_name)
        if self.source_review_feature_id != SOURCE_REVIEW_FEATURE_ID:
            raise ValueError("source_review_feature_id must match Phase 9 contract result review gate")
        for field_name in _policy_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _policy_required_false_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelRuntimeActivationEnvelope:
    """Renderer-neutral runtime activation envelope.

    This is not a renderer and not a mounted panel. It is a bounded in-memory
    object that a later governed renderer contract may consume.
    """

    feature_id: str
    activation_surface_id: str
    activation_surface_label: str
    state: ReadOnlyPanelRuntimeActivationEnvelopeState
    feature_flag_name: str
    feature_flag_enabled: bool
    source_panel_id: Optional[str]
    source_panel_label: Optional[str]
    source_panel_state: Optional[ReadOnlyAdvisoryPanelUIState]
    canonical_result_id: Optional[str]
    canonical_dispatch_label: Optional[str]
    final_selection_hash: Optional[str]
    panel_view_model: Optional[ReadOnlyAdvisoryPanelViewModel]
    failure_state_codes: Tuple[str, ...]
    non_training_feedback_slot_enabled: bool
    runtime_activation_envelope_ready: bool
    read_only: bool = True
    telemetry_only: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    renderer_neutral: bool = True
    non_authoritative: bool = True
    phase8_panel_view_model_input_only: bool = True
    actual_runtime_panel_activation_enabled: bool = False
    renderer_activation_enabled: bool = False
    mounted_panel_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    runtime_telemetry_surface_wiring_enabled: bool = False
    route_influence_enabled: bool = False
    route_authority_enabled: bool = False
    router_calls_enabled: bool = False
    advisor_calls_enabled: bool = False
    adapter_execution_enabled: bool = False
    provider_calls_enabled: bool = False
    persistence_enabled: bool = False
    prompt_loading_enabled: bool = False
    prompt_registry_mutation_enabled: bool = False
    prompt_library_read_enabled: bool = False
    freeze_memory_read_enabled: bool = False
    freeze_memory_write_enabled: bool = False
    router_canon_read_enabled: bool = False
    route_override_button_enabled: bool = False
    use_ml_route_button_enabled: bool = False
    best_route_claim_enabled: bool = False
    prompt_ranking_enabled: bool = False
    advisory_ranking_enabled: bool = False
    free_text_route_advice_enabled: bool = False
    free_text_explanations_enabled: bool = False
    runtime_copilot_decision_behavior_enabled: bool = False
    critical_boundary_error_budget: int = 0

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 9 runtime activation implementation")
        _require_text("activation_surface_id", self.activation_surface_id)
        _require_text("activation_surface_label", self.activation_surface_label)
        _require_text("feature_flag_name", self.feature_flag_name)
        if not isinstance(self.state, ReadOnlyPanelRuntimeActivationEnvelopeState):
            raise TypeError("state must be ReadOnlyPanelRuntimeActivationEnvelopeState")
        if self.source_panel_state is not None and not isinstance(self.source_panel_state, ReadOnlyAdvisoryPanelUIState):
            raise TypeError("source_panel_state must be ReadOnlyAdvisoryPanelUIState or None")
        if self.panel_view_model is not None and not isinstance(self.panel_view_model, ReadOnlyAdvisoryPanelViewModel):
            raise TypeError("panel_view_model must be ReadOnlyAdvisoryPanelViewModel or None")
        for optional_text in (
            "source_panel_id", "source_panel_label", "canonical_result_id",
            "canonical_dispatch_label", "final_selection_hash",
        ):
            value = getattr(self, optional_text)
            if value is not None:
                _require_text(optional_text, value)
        _require_tuple_of_text("failure_state_codes", self.failure_state_codes)
        for field_name in _envelope_required_true_fields():
            if getattr(self, field_name) is not True:
                raise ValueError(field_name + " must remain True")
        for field_name in _envelope_forbidden_true_fields():
            if getattr(self, field_name) is not False:
                raise ValueError(field_name + " must remain False")
        if self.critical_boundary_error_budget != 0:
            raise ValueError("critical_boundary_error_budget must remain zero")
        if self.runtime_activation_envelope_ready is True:
            if self.state is not ReadOnlyPanelRuntimeActivationEnvelopeState.READY_READ_ONLY_ACTIVATION_ENVELOPE:
                raise ValueError("ready envelope must use READY_READ_ONLY_ACTIVATION_ENVELOPE state")
            if self.panel_view_model is None:
                raise ValueError("ready envelope requires a panel_view_model")
        else:
            if self.state is ReadOnlyPanelRuntimeActivationEnvelopeState.READY_READ_ONLY_ACTIVATION_ENVELOPE:
                raise ValueError("READY state requires runtime_activation_envelope_ready=True")


def build_read_only_advisory_panel_runtime_activation_envelope(
    policy: ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    panel_view_model: object | None,
) -> ReadOnlyAdvisoryPanelRuntimeActivationEnvelope:
    """Build a guarded runtime activation envelope.

    The only successful path returns an in-memory read-only activation envelope
    when the feature flag is explicitly enabled and the Phase 8 view model is
    safe. The function never renders, mounts, mutates UI, wires runtime telemetry,
    calls router/advisor/adapters/providers, persists data, or influences routes.
    """

    if not isinstance(policy, ReadOnlyAdvisoryPanelRuntimeActivationPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelRuntimeActivationPolicy")

    if not policy.enabled:
        return _build_envelope(policy, None, ReadOnlyPanelRuntimeActivationEnvelopeState.DISABLED_NOOP, ("disabled_noop",), ready=False)

    if policy.feature_flag_enabled is not True:
        return _build_envelope(policy, None, ReadOnlyPanelRuntimeActivationEnvelopeState.DISABLED_NOOP, ("feature_flag_default_off",), ready=False)

    if panel_view_model is None:
        return _build_envelope(policy, None, ReadOnlyPanelRuntimeActivationEnvelopeState.FAIL_OPEN_NO_VIEW_MODEL, ("missing_panel_view_model",), ready=False)

    if not _panel_view_model_is_safe(panel_view_model):
        return _build_envelope(policy, None, ReadOnlyPanelRuntimeActivationEnvelopeState.BLOCKED_UNSAFE_VIEW_MODEL, ("unsafe_panel_view_model",), ready=False)

    return _build_envelope(policy, panel_view_model, ReadOnlyPanelRuntimeActivationEnvelopeState.READY_READ_ONLY_ACTIVATION_ENVELOPE, (), ready=True)


def build_phase9_read_only_panel_runtime_activation_implementation_probe() -> ReadOnlyAdvisoryPanelRuntimeActivationEnvelope:
    """Build a safe in-memory activation-envelope probe for validation."""

    policy = ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_surface_id="phase9_read_only_panel_runtime_activation_envelope",
        activation_surface_label="phase9_read_only_advisory_panel_runtime_activation_v1",
        feature_flag_enabled=True,
    )
    return build_read_only_advisory_panel_runtime_activation_envelope(
        policy,
        build_phase8_read_only_advisory_panel_ui_probe(),
    )


def _panel_view_model_is_safe(model: object | None) -> bool:
    """Support panel view model is safe behavior.
    
    Parameters
    ----------
    model : object | None
        The model value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        isinstance(model, ReadOnlyAdvisoryPanelViewModel)
        and model.state is ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY
        and model.read_only is True
        and model.telemetry_only is True
        and model.renderer_neutral is True
        and model.route_invariant is True
        and model.final_selection_invisible is True
        and model.non_authoritative is True
        and model.runtime_panel_activation_enabled is False
        and model.runtime_ui_mutation_enabled is False
        and model.runtime_telemetry_surface_wired is False
        and model.route_influence_enabled is False
        and model.route_authority_enabled is False
    )


def _build_envelope(
    policy: ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    model: Optional[ReadOnlyAdvisoryPanelViewModel],
    state: ReadOnlyPanelRuntimeActivationEnvelopeState,
    failure_codes: Tuple[str, ...],
    *,
    ready: bool,
) -> ReadOnlyAdvisoryPanelRuntimeActivationEnvelope:
    """Support build envelope behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelRuntimeActivationPolicy
        The policy value.
    model : Optional[ReadOnlyAdvisoryPanelViewModel]
        The model value.
    state : ReadOnlyPanelRuntimeActivationEnvelopeState
        The state value.
    failure_codes : Tuple[str, ...]
        The failure codes value.
    ready : bool
        The ready value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelope
        The read only advisory panel runtime activation envelope result.
    """
    
    return ReadOnlyAdvisoryPanelRuntimeActivationEnvelope(
        feature_id=FEATURE_ID,
        activation_surface_id=policy.activation_surface_id,
        activation_surface_label=policy.activation_surface_label,
        state=state,
        feature_flag_name=policy.feature_flag_name,
        feature_flag_enabled=policy.feature_flag_enabled,
        source_panel_id=model.panel_id if model else None,
        source_panel_label=model.panel_label if model else None,
        source_panel_state=model.state if model else None,
        canonical_result_id=model.canonical_result_id if model else None,
        canonical_dispatch_label=model.canonical_dispatch_label if model else None,
        final_selection_hash=model.final_selection_hash if model else None,
        panel_view_model=model,
        failure_state_codes=failure_codes,
        non_training_feedback_slot_enabled=bool(model and model.non_training_feedback_slot_enabled),
        runtime_activation_envelope_ready=ready,
    )


def _policy_required_true_fields() -> Tuple[str, ...]:
    """Support policy required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "require_phase8_panel_view_model_input",
        "require_disable_noop_control",
        "require_fail_open_on_missing_view_model",
        "require_route_invariant_activation",
        "require_final_selection_invisible_activation",
        "require_renderer_adapter_to_be_separate_future_contract",
        "require_non_training_feedback_slot",
        "allow_runtime_activation_envelope",
    )


def _policy_required_false_fields() -> Tuple[str, ...]:
    """Support policy required false fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "feature_flag_default_enabled",
        "allow_actual_runtime_panel_activation",
        "allow_renderer_activation",
        "allow_mounted_panel",
        "allow_runtime_ui_mutation",
        "allow_runtime_telemetry_surface_wiring",
        "allow_route_influence",
        "allow_route_authority",
        "allow_router_calls",
        "allow_advisor_calls",
        "allow_adapter_execution",
        "allow_provider_calls",
        "allow_persistence",
        "allow_prompt_loading",
        "allow_prompt_registry_mutation",
        "allow_prompt_library_read",
        "allow_freeze_memory_read",
        "allow_freeze_memory_write",
        "allow_router_canon_read",
        "allow_route_override_button",
        "allow_use_ml_route_button",
        "allow_best_route_claim",
        "allow_prompt_ranking",
        "allow_advisory_ranking",
        "allow_free_text_route_advice",
        "allow_free_text_explanations",
        "allow_runtime_copilot_decision_behavior",
    )


def _envelope_required_true_fields() -> Tuple[str, ...]:
    """Support envelope required true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "read_only",
        "telemetry_only",
        "in_memory_only",
        "bounded",
        "fail_open",
        "removable_noop",
        "route_invariant",
        "final_selection_invisible",
        "renderer_neutral",
        "non_authoritative",
        "phase8_panel_view_model_input_only",
    )


def _envelope_forbidden_true_fields() -> Tuple[str, ...]:
    """Support envelope forbidden true fields behavior.
    
    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """
    
    return (
        "actual_runtime_panel_activation_enabled",
        "renderer_activation_enabled",
        "mounted_panel_enabled",
        "runtime_ui_mutation_enabled",
        "runtime_telemetry_surface_wiring_enabled",
        "route_influence_enabled",
        "route_authority_enabled",
        "router_calls_enabled",
        "advisor_calls_enabled",
        "adapter_execution_enabled",
        "provider_calls_enabled",
        "persistence_enabled",
        "prompt_loading_enabled",
        "prompt_registry_mutation_enabled",
        "prompt_library_read_enabled",
        "freeze_memory_read_enabled",
        "freeze_memory_write_enabled",
        "router_canon_read_enabled",
        "route_override_button_enabled",
        "use_ml_route_button_enabled",
        "best_route_claim_enabled",
        "prompt_ranking_enabled",
        "advisory_ranking_enabled",
        "free_text_route_advice_enabled",
        "free_text_explanations_enabled",
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
    
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be non-empty text")


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
        raise TypeError(name + " must be a tuple")
    for item in value:
        _require_text(name + " item", item)
