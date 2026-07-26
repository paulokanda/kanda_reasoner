# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_passive_visibility_activation_invariants.py
"""Invariant field helpers for passive visibility activation descriptors."""

from __future__ import annotations

from typing import Tuple

__all__ = []


def _policy_required_true_fields() -> Tuple[str, ...]:
    """Support policy required true fields behavior.

    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """

    return (
        "require_phase12_runtime_app_host_visibility_descriptor_input",
        "require_disable_noop_control",
        "require_fail_open_on_missing_descriptor",
        "require_block_unsafe_descriptor",
        "require_bounded_passive_visibility_slots",
        "require_read_only_passive_visibility_slot",
        "require_removable_noop_activation",
        "require_route_invariant_activation",
        "require_final_selection_invisible_activation",
        "require_non_training_feedback_slot",
        "allow_read_only_passive_visibility_activation_descriptor",
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
        "allow_actual_passive_visibility_activation",
        "allow_passive_visibility_slot_registration",
        "allow_passive_visibility_slot_mutation",
        "allow_actual_runtime_app_host_visibility",
        "allow_visibility_activation",
        "allow_mounted_runtime_panel",
        "allow_runtime_panel_mount_side_effects",
        "allow_host_event_subscription",
        "allow_host_callback_registration",
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
        "allow_runtime_pilot_behavior",
        "allow_runtime_copilot_decision_behavior",
        "allow_autonomous_ml_router",
    )


def _descriptor_required_true_fields() -> Tuple[str, ...]:
    """Support descriptor required true fields behavior.

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
        "non_authoritative",
        "consumes_phase12_runtime_app_host_visibility_descriptor_only",
    )


def _descriptor_forbidden_true_fields() -> Tuple[str, ...]:
    """Support descriptor forbidden true fields behavior.

    Returns
    -------
    Tuple[str, ...]
        The tuple result.
    """

    return (
        "actual_passive_visibility_activation_enabled",
        "passive_visibility_slot_registration_enabled",
        "passive_visibility_slot_mutation_enabled",
        "actual_runtime_app_host_visibility_enabled",
        "visibility_activation_enabled",
        "mounted_runtime_panel_enabled",
        "runtime_panel_mount_side_effects_enabled",
        "host_event_subscription_enabled",
        "host_callback_registration_enabled",
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
        "runtime_pilot_behavior_enabled",
        "runtime_copilot_decision_behavior_enabled",
        "autonomous_ml_router_enabled",
        "visible_ml_integration_complete",
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
