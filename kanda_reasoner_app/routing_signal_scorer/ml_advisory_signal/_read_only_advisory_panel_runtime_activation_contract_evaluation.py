# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_runtime_activation_contract_evaluation.py
"""Private pure evaluation helpers for the Phase 9 runtime activation contract."""

from __future__ import annotations

from typing import Any, Mapping, Optional

from .read_only_advisory_panel_ui import (
    ReadOnlyAdvisoryPanelUIState,
    ReadOnlyAdvisoryPanelViewModel,
)

__all__: list[str] = []


def _status_for_requested_capabilities(
    requested: Mapping[str, bool],
    status_type: Any = None,
) -> Optional[Any]:
    """Return the blocking status for requested capabilities, when any."""
    if status_type is None:
        raise TypeError("status_type is required")

    authority = {
        "route_authority",
        "route_influence",
        "route_override_button",
        "use_ml_route_button",
        "best_route_claim",
        "final_selection_hook",
        "prompt_selection_hook",
        "runtime_copilot_decision_behavior",
    }
    runtime_wiring = {
        "actual_runtime_panel_activation",
        "renderer_activation",
        "mounted_panel",
        "runtime_ui_mutation",
        "runtime_telemetry_surface_wiring",
    }
    data_or_side_effect = {
        "router_call",
        "advisor_call",
        "adapter_execution",
        "provider_call",
        "persistence_write",
        "prompt_loading",
        "prompt_registry_mutation",
        "prompt_library_read",
        "freeze_memory_read",
        "freeze_memory_write",
        "router_canon_read",
    }
    text_or_controls = {
        "prompt_ranking",
        "advisory_ranking",
        "free_text_route_advice",
        "free_text_explanation",
    }

    for key, enabled in requested.items():
        if enabled is not True:
            continue
        if key in authority:
            return status_type.BLOCKED_UNSAFE_AUTHORITY
        if key in runtime_wiring:
            return status_type.BLOCKED_UNSAFE_RUNTIME_WIRING
        if key in data_or_side_effect:
            return status_type.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT
        if key in text_or_controls:
            return status_type.BLOCKED_UNSAFE_TEXT_OR_CONTROLS
    return None


def _view_model_is_safe(
    view_model: Optional[ReadOnlyAdvisoryPanelViewModel],
) -> bool:
    """Return whether the Phase 8 view model is safe for contract readiness."""
    if view_model is None:
        return False
    return (
        isinstance(view_model, ReadOnlyAdvisoryPanelViewModel)
        and view_model.state is ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY
        and view_model.read_only is True
        and view_model.telemetry_only is True
        and view_model.renderer_neutral is True
        and view_model.route_invariant is True
        and view_model.final_selection_invisible is True
        and view_model.non_authoritative is True
        and view_model.runtime_panel_activation_enabled is False
        and view_model.runtime_ui_mutation_enabled is False
        and view_model.runtime_telemetry_surface_wired is False
        and view_model.route_influence_enabled is False
        and view_model.route_authority_enabled is False
    )

# Responsibility boundary:
# - capability classification is deterministic and read-only;
# - view-model safety checks consume Phase 8 contract fields only;
# - no facade symbols are imported here;
# - no router, advisor, adapter, provider, persistence, or UI side effects occur;
# - the facade remains the owner of public decision construction and enums.
