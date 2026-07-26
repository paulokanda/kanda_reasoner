from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_renderer_mount import (
    ReadOnlyAdvisoryPanelRendererMountPolicy,
    ReadOnlyPanelRendererMountImplementationState,
    build_phase10_read_only_panel_renderer_mount_implementation_probe,
    build_read_only_advisory_panel_renderer_mount_descriptor,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_activation import (
    ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
    build_read_only_advisory_panel_runtime_activation_envelope,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_ui import (
    build_phase8_read_only_advisory_panel_ui_probe,
)

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_IMPLEMENTATION_V1.md")
BOUNDARY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_IMPLEMENTATION_BOUNDARY_MODEL_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_IMPLEMENTATION_RESULT_REVIEW_READINESS_V1.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_CONTRACT_RESULT_REVIEW_GATE_V1.md")


def _policy(flag=True, enabled=True):
    return ReadOnlyAdvisoryPanelRendererMountPolicy(
        mount_surface_id="phase10_read_only_panel_renderer_mount_descriptor",
        mount_surface_label="Phase 10 Read-Only Advisory Panel Renderer Mount",
        enabled=enabled,
        feature_flag_enabled=flag,
    )


def test_phase10_renderer_mount_implementation_probe_is_safe_ready_descriptor():
    descriptor = build_phase10_read_only_panel_renderer_mount_implementation_probe()
    assert descriptor.feature_id == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1"
    assert descriptor.state is ReadOnlyPanelRendererMountImplementationState.READ_ONLY_MOUNT_DESCRIPTOR_READY
    assert descriptor.read_only_mount_descriptor_ready is True
    assert descriptor.visible_read_only_panel_ready is True
    assert descriptor.feature_flag_enabled is True
    assert descriptor.source_activation_surface_id == "phase9_read_only_panel_runtime_activation_envelope"
    assert descriptor.source_panel_id == "phase8_read_only_advisory_panel_view_model"
    assert descriptor.canonical_result_id == "synthetic_canonical_result_001"
    assert descriptor.read_only is True
    assert descriptor.telemetry_only is True
    assert descriptor.in_memory_only is True
    assert descriptor.bounded is True
    assert descriptor.fail_open is True
    assert descriptor.removable_noop is True
    assert descriptor.route_invariant is True
    assert descriptor.final_selection_invisible is True
    assert descriptor.non_authoritative is True
    assert descriptor.consumes_phase9_activation_envelope_only is True
    assert descriptor.runtime_ui_mutation_enabled is False
    assert descriptor.runtime_telemetry_surface_wiring_enabled is False
    assert descriptor.route_influence_enabled is False
    assert descriptor.route_authority_enabled is False
    assert descriptor.router_calls_enabled is False
    assert descriptor.advisor_calls_enabled is False
    assert descriptor.adapter_execution_enabled is False
    assert descriptor.provider_calls_enabled is False
    assert descriptor.persistence_enabled is False
    assert descriptor.prompt_loading_enabled is False
    assert descriptor.prompt_library_read_enabled is False
    assert descriptor.freeze_memory_read_enabled is False
    assert descriptor.router_canon_read_enabled is False
    assert descriptor.route_override_button_enabled is False
    assert descriptor.use_ml_route_button_enabled is False
    assert descriptor.best_route_claim_enabled is False
    assert descriptor.prompt_ranking_enabled is False
    assert descriptor.advisory_ranking_enabled is False
    assert descriptor.free_text_route_advice_enabled is False
    assert descriptor.runtime_copilot_decision_behavior_enabled is False
    assert descriptor.critical_boundary_error_budget == 0


def test_phase10_renderer_mount_implementation_sections_are_bounded_read_only():
    descriptor = build_phase10_read_only_panel_renderer_mount_implementation_probe()
    keys = {section.section_key for section in descriptor.rendered_sections}
    assert "advisory_role_label" in keys
    assert "canonical_route_unchanged_label" in keys
    assert "no_route_authority_label" in keys
    assert 1 <= len(descriptor.rendered_sections) <= 11
    for section in descriptor.rendered_sections:
        assert section.read_only is True
        assert section.action_enabled is False
        assert section.route_authority_enabled is False
        assert section.route_influence_enabled is False
        assert section.free_text_route_advice_enabled is False
        assert len(section.label) <= 96
        assert len(section.value) <= 240


def test_phase10_renderer_mount_implementation_default_off_and_fail_open():
    envelope = build_phase9_read_only_panel_runtime_activation_implementation_probe()
    default_off = build_read_only_advisory_panel_renderer_mount_descriptor(_policy(flag=False), envelope)
    assert default_off.state is ReadOnlyPanelRendererMountImplementationState.DISABLED_NOOP
    assert default_off.read_only_mount_descriptor_ready is False
    assert default_off.visible_read_only_panel_ready is False
    assert "feature_flag_default_off" in default_off.failure_state_codes
    assert default_off.route_authority_enabled is False

    missing = build_read_only_advisory_panel_renderer_mount_descriptor(_policy(flag=True), None)
    assert missing.state is ReadOnlyPanelRendererMountImplementationState.FAIL_OPEN_NO_ENVELOPE
    assert missing.read_only_mount_descriptor_ready is False
    assert "missing_or_invalid_activation_envelope" in missing.failure_state_codes
    assert missing.runtime_ui_mutation_enabled is False

    invalid = build_read_only_advisory_panel_renderer_mount_descriptor(_policy(flag=True), object())
    assert invalid.state is ReadOnlyPanelRendererMountImplementationState.FAIL_OPEN_NO_ENVELOPE
    assert invalid.route_influence_enabled is False


def test_phase10_renderer_mount_implementation_blocks_unsafe_envelope():
    view_model = build_phase8_read_only_advisory_panel_ui_probe()
    unsafe_policy = ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_surface_id="phase9_runtime_activation_envelope",
        activation_surface_label="Phase 9 Runtime Activation Envelope",
        feature_flag_enabled=False,
    )
    unsafe_envelope = build_read_only_advisory_panel_runtime_activation_envelope(unsafe_policy, view_model)
    descriptor = build_read_only_advisory_panel_renderer_mount_descriptor(_policy(flag=True), unsafe_envelope)
    assert descriptor.state is ReadOnlyPanelRendererMountImplementationState.BLOCKED_UNSAFE_ENVELOPE
    assert descriptor.read_only_mount_descriptor_ready is False
    assert "unsafe_activation_envelope_rejected" in descriptor.failure_state_codes
    assert descriptor.route_authority_enabled is False


def test_phase10_renderer_mount_policy_blocks_unsafe_toggles():
    unsafe_kwargs = [
        {"allow_runtime_ui_mutation": True},
        {"allow_runtime_telemetry_surface_wiring": True},
        {"allow_route_influence": True},
        {"allow_route_authority": True},
        {"allow_router_calls": True},
        {"allow_advisor_calls": True},
        {"allow_adapter_execution": True},
        {"allow_provider_calls": True},
        {"allow_persistence": True},
        {"allow_prompt_loading": True},
        {"allow_freeze_memory_read": True},
        {"allow_router_canon_read": True},
        {"allow_route_override_button": True},
        {"allow_use_ml_route_button": True},
        {"allow_best_route_claim": True},
        {"allow_runtime_copilot_decision_behavior": True},
    ]
    for kwargs in unsafe_kwargs:
        try:
            ReadOnlyAdvisoryPanelRendererMountPolicy(
                mount_surface_id="phase10_read_only_panel_renderer_mount_descriptor",
                mount_surface_label="Phase 10 Read-Only Advisory Panel Renderer Mount",
                **kwargs,
            )
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe policy unexpectedly accepted: {kwargs}")


def test_phase10_renderer_mount_implementation_docs_and_prerequisite():
    text = DOC.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_implementation_v1" in text
    assert "feature-flagged, default-off" in text
    assert "in-memory read-only mount descriptor" in text
    assert "does not mutate runtime UI" in boundary
    assert "No route authority" in boundary or "route authority" in boundary
    assert "The next review gate must verify" in readiness
    assert PREV.exists()


if __name__ == "__main__":
    test_phase10_renderer_mount_implementation_probe_is_safe_ready_descriptor()
    test_phase10_renderer_mount_implementation_sections_are_bounded_read_only()
    test_phase10_renderer_mount_implementation_default_off_and_fail_open()
    test_phase10_renderer_mount_implementation_blocks_unsafe_envelope()
    test_phase10_renderer_mount_policy_blocks_unsafe_toggles()
    test_phase10_renderer_mount_implementation_docs_and_prerequisite()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount implementation")
