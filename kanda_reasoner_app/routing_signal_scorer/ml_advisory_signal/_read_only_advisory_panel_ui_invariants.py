# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/_read_only_advisory_panel_ui_invariants.py
"""Explicit invariant validation for the Phase 8 read-only panel UI model.

This private helper owns validation mechanics only. It deliberately avoids
reflection and does not import the public facade, preserving one-way dependency
flow from the facade into this invariant owner.
"""

from __future__ import annotations

from typing import Any

__all__: list[str] = []


def validate_ui_policy(
    policy: Any,
    *,
    source_review_feature_id: str,
    section_kind_type: type,
) -> None:
    """Validate the immutable UI policy with explicit field access."""
    _require_text("panel_id", policy.panel_id)
    _require_text("panel_label", policy.panel_label)
    if policy.source_review_feature_id != source_review_feature_id:
        raise ValueError("source_review_feature_id must match Phase 8 contract review gate")
    _require_tuple_of_enum(
        "allowed_section_kinds",
        policy.allowed_section_kinds,
        section_kind_type,
    )
    _require_positive_int("max_sections", policy.max_sections)

    _require_true("read_only", policy.read_only)
    _require_true("telemetry_only", policy.telemetry_only)
    _require_true("renderer_neutral", policy.renderer_neutral)
    _require_true("in_memory_only", policy.in_memory_only)
    _require_true("bounded", policy.bounded)
    _require_true("fail_open", policy.fail_open)
    _require_true("removable_noop", policy.removable_noop)
    _require_true("route_invariant", policy.route_invariant)
    _require_true("final_selection_invisible", policy.final_selection_invisible)
    _require_true("non_authoritative", policy.non_authoritative)
    _require_true(
        "consumes_phase7_surface_envelope_only",
        policy.consumes_phase7_surface_envelope_only,
    )
    _require_true(
        "section_values_are_bounded_status_only",
        policy.section_values_are_bounded_status_only,
    )
    _require_true(
        "require_advisory_role_label",
        policy.require_advisory_role_label,
    )
    _require_true(
        "require_canonical_route_unchanged_label",
        policy.require_canonical_route_unchanged_label,
    )
    _require_true(
        "require_no_route_authority_label",
        policy.require_no_route_authority_label,
    )
    _require_true(
        "require_confidence_not_correctness_label",
        policy.require_confidence_not_correctness_label,
    )
    _require_true(
        "non_training_feedback_only",
        policy.non_training_feedback_only,
    )

    _require_false(
        "route_override_button_enabled",
        policy.route_override_button_enabled,
    )
    _require_false("use_ml_route_button_enabled", policy.use_ml_route_button_enabled)
    _require_false("best_route_claim_enabled", policy.best_route_claim_enabled)
    _require_false("prompt_ranking_enabled", policy.prompt_ranking_enabled)
    _require_false(
        "free_text_route_advice_enabled",
        policy.free_text_route_advice_enabled,
    )
    _require_false(
        "free_text_explanations_enabled",
        policy.free_text_explanations_enabled,
    )
    _require_false(
        "runtime_panel_activation_enabled",
        policy.runtime_panel_activation_enabled,
    )
    _require_false("runtime_ui_mutation_enabled", policy.runtime_ui_mutation_enabled)
    _require_false(
        "runtime_telemetry_surface_wired",
        policy.runtime_telemetry_surface_wired,
    )
    _require_false("route_influence_enabled", policy.route_influence_enabled)
    _require_false("route_authority_enabled", policy.route_authority_enabled)
    _require_false("router_calls_enabled", policy.router_calls_enabled)
    _require_false("advisor_calls_enabled", policy.advisor_calls_enabled)
    _require_false("adapter_execution_enabled", policy.adapter_execution_enabled)
    _require_false("provider_calls_enabled", policy.provider_calls_enabled)
    _require_false("persistence_enabled", policy.persistence_enabled)
    _require_false("prompt_loading_enabled", policy.prompt_loading_enabled)
    _require_false(
        "prompt_registry_mutation_enabled",
        policy.prompt_registry_mutation_enabled,
    )
    _require_false(
        "prompt_library_read_enabled",
        policy.prompt_library_read_enabled,
    )
    _require_false("freeze_memory_read_enabled", policy.freeze_memory_read_enabled)
    _require_false(
        "freeze_memory_write_enabled",
        policy.freeze_memory_write_enabled,
    )
    _require_false("router_canon_read_enabled", policy.router_canon_read_enabled)
    _require_false("runtime_shadow_mode_enabled", policy.runtime_shadow_mode_enabled)
    _require_false("training_enabled", policy.training_enabled)
    _require_false("calibration_enabled", policy.calibration_enabled)
    _require_false("model_improvement_enabled", policy.model_improvement_enabled)
    _require_false(
        "runtime_pilot_behavior_enabled",
        policy.runtime_pilot_behavior_enabled,
    )
    _require_false(
        "runtime_copilot_decision_behavior_enabled",
        policy.runtime_copilot_decision_behavior_enabled,
    )


def validate_panel_section(
    section: Any,
    *,
    section_kind_type: type,
) -> None:
    """Validate one bounded read-only panel section explicitly."""
    if not isinstance(section.kind, section_kind_type):
        raise TypeError("kind must be ReadOnlyPanelSectionKind")
    _require_text("label", section.label)
    _require_text("value", section.value)
    _require_text("severity", section.severity)
    if len(section.label) > 96:
        raise ValueError("label must remain bounded")
    if len(section.value) > 240:
        raise ValueError("value must remain bounded")
    if section.read_only is not True:
        raise ValueError("section must remain read-only")
    if section.action_enabled is not False:
        raise ValueError("section actions are forbidden")
    if section.route_authority_enabled is not False:
        raise ValueError("section route authority is forbidden")
    if section.route_influence_enabled is not False:
        raise ValueError("section route influence is forbidden")
    if section.free_text_route_advice is not False:
        raise ValueError("section free-text route advice is forbidden")


def validate_view_model(
    view_model: Any,
    *,
    feature_id: str,
    state_type: type,
    render_mode_type: type,
    attachment_state_type: type,
    section_type: type,
) -> None:
    """Validate the public view model without reflective field access."""
    if view_model.feature_id != feature_id:
        raise ValueError("feature_id must match Phase 8 panel UI implementation")
    _require_text("panel_id", view_model.panel_id)
    _require_text("panel_label", view_model.panel_label)
    if not isinstance(view_model.state, state_type):
        raise TypeError("state must be ReadOnlyAdvisoryPanelUIState")
    if not isinstance(view_model.render_mode, render_mode_type):
        raise TypeError("render_mode must be ReadOnlyPanelRenderMode")

    _require_optional_text("source_surface_id", view_model.source_surface_id)
    _require_optional_text("source_surface_label", view_model.source_surface_label)
    _require_optional_text("canonical_result_id", view_model.canonical_result_id)
    _require_optional_text(
        "canonical_dispatch_label",
        view_model.canonical_dispatch_label,
    )
    _require_optional_text("final_selection_hash", view_model.final_selection_hash)

    if (
        view_model.source_attachment_state is not None
        and not isinstance(view_model.source_attachment_state, attachment_state_type)
    ):
        raise TypeError(
            "source_attachment_state must be ReadOnlySurfaceAttachmentState or None"
        )
    _require_tuple_of_enum("sections", view_model.sections, section_type)
    _require_tuple_of_text("failure_state_codes", view_model.failure_state_codes)

    _require_true("read_only", view_model.read_only)
    _require_true("telemetry_only", view_model.telemetry_only)
    _require_true("renderer_neutral", view_model.renderer_neutral)
    _require_true("in_memory_only", view_model.in_memory_only)
    _require_true("bounded", view_model.bounded)
    _require_true("fail_open", view_model.fail_open)
    _require_true("removable_noop", view_model.removable_noop)
    _require_true("route_invariant", view_model.route_invariant)
    _require_true(
        "final_selection_invisible",
        view_model.final_selection_invisible,
    )
    _require_true("non_authoritative", view_model.non_authoritative)

    _require_false(
        "runtime_panel_activation_enabled",
        view_model.runtime_panel_activation_enabled,
    )
    _require_false(
        "runtime_ui_mutation_enabled",
        view_model.runtime_ui_mutation_enabled,
    )
    _require_false(
        "runtime_telemetry_surface_wired",
        view_model.runtime_telemetry_surface_wired,
    )
    _require_false("route_influence_enabled", view_model.route_influence_enabled)
    _require_false("route_authority_enabled", view_model.route_authority_enabled)
    _require_false(
        "route_override_button_enabled",
        view_model.route_override_button_enabled,
    )
    _require_false(
        "use_ml_route_button_enabled",
        view_model.use_ml_route_button_enabled,
    )
    _require_false("prompt_ranking_enabled", view_model.prompt_ranking_enabled)
    _require_false(
        "free_text_route_advice_enabled",
        view_model.free_text_route_advice_enabled,
    )
    _require_false(
        "free_text_explanations_enabled",
        view_model.free_text_explanations_enabled,
    )
    _require_false(
        "runtime_copilot_decision_behavior_enabled",
        view_model.runtime_copilot_decision_behavior_enabled,
    )


def _require_text(name: str, value: str) -> None:
    """Require non-empty text with the legacy error contract."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be non-empty text")


def _require_optional_text(name: str, value: Any) -> None:
    """Validate optional text without reflection."""
    if value is not None:
        _require_text(name, value)


def _require_positive_int(name: str, value: int) -> None:
    """Require a positive integer with the legacy error contract."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError(name + " must be a positive integer")


def _require_tuple_of_text(name: str, value: Any) -> None:
    """Require a tuple of non-empty text values."""
    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    for item in value:
        _require_text(name + " item", item)


def _require_tuple_of_enum(name: str, value: Any, enum_type: type) -> None:
    """Require a non-empty tuple whose items match one explicit type."""
    if not isinstance(value, tuple):
        raise TypeError(name + " must be a tuple")
    if not value:
        raise ValueError(name + " must not be empty")
    for item in value:
        if not isinstance(item, enum_type):
            raise TypeError(name + " item must be " + enum_type.__name__)


def _require_true(name: str, value: Any) -> None:
    """Require the exact True singleton."""
    if value is not True:
        raise ValueError(name + " must remain True")


def _require_false(name: str, value: Any) -> None:
    """Require the exact False singleton."""
    if value is not False:
        raise ValueError(name + " must remain False")
