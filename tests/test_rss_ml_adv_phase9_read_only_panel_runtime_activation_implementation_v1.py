from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_activation import (
    ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    ReadOnlyPanelRuntimeActivationEnvelopeState,
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
    build_read_only_advisory_panel_runtime_activation_envelope,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_ui import (
    build_phase8_read_only_advisory_panel_ui_probe,
)

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_V1.md")
BOUNDARY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_BOUNDARY_MODEL_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_IMPLEMENTATION_RESULT_REVIEW_READINESS_V1.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_CONTRACT_RESULT_REVIEW_GATE_V1.md")


def _policy(flag=True, enabled=True):
    return ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_surface_id="phase9_runtime_activation_envelope",
        activation_surface_label="Phase 9 Runtime Activation Envelope",
        source_review_feature_id="rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_result_review_gate_v1",
        enabled=enabled,
        feature_flag_enabled=flag,
    )


def test_phase9_runtime_activation_implementation_probe_is_safe_ready_envelope():
    envelope = build_phase9_read_only_panel_runtime_activation_implementation_probe()
    assert envelope.feature_id == "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1"
    assert envelope.state is ReadOnlyPanelRuntimeActivationEnvelopeState.READY_READ_ONLY_ACTIVATION_ENVELOPE
    assert envelope.runtime_activation_envelope_ready is True
    assert envelope.feature_flag_enabled is True
    assert envelope.source_panel_id == "phase8_read_only_advisory_panel_view_model"
    assert envelope.canonical_result_id == "synthetic_canonical_result_001"
    assert envelope.read_only is True
    assert envelope.telemetry_only is True
    assert envelope.in_memory_only is True
    assert envelope.route_invariant is True
    assert envelope.final_selection_invisible is True
    assert envelope.renderer_neutral is True
    assert envelope.non_authoritative is True
    assert envelope.phase8_panel_view_model_input_only is True
    assert envelope.actual_runtime_panel_activation_enabled is False
    assert envelope.renderer_activation_enabled is False
    assert envelope.mounted_panel_enabled is False
    assert envelope.runtime_ui_mutation_enabled is False
    assert envelope.runtime_telemetry_surface_wiring_enabled is False
    assert envelope.route_influence_enabled is False
    assert envelope.route_authority_enabled is False
    assert envelope.router_calls_enabled is False
    assert envelope.advisor_calls_enabled is False
    assert envelope.adapter_execution_enabled is False
    assert envelope.provider_calls_enabled is False
    assert envelope.persistence_enabled is False
    assert envelope.prompt_loading_enabled is False
    assert envelope.prompt_library_read_enabled is False
    assert envelope.router_canon_read_enabled is False
    assert envelope.route_override_button_enabled is False
    assert envelope.use_ml_route_button_enabled is False
    assert envelope.best_route_claim_enabled is False
    assert envelope.prompt_ranking_enabled is False
    assert envelope.free_text_route_advice_enabled is False
    assert envelope.runtime_copilot_decision_behavior_enabled is False
    assert envelope.critical_boundary_error_budget == 0


def test_phase9_runtime_activation_implementation_default_off_and_fail_open():
    view_model = build_phase8_read_only_advisory_panel_ui_probe()
    default_off = build_read_only_advisory_panel_runtime_activation_envelope(_policy(flag=False), view_model)
    assert default_off.state is ReadOnlyPanelRuntimeActivationEnvelopeState.DISABLED_NOOP
    assert default_off.runtime_activation_envelope_ready is False
    assert "feature_flag_default_off" in default_off.failure_state_codes
    assert default_off.actual_runtime_panel_activation_enabled is False
    assert default_off.route_authority_enabled is False

    missing = build_read_only_advisory_panel_runtime_activation_envelope(_policy(flag=True), None)
    assert missing.state is ReadOnlyPanelRuntimeActivationEnvelopeState.FAIL_OPEN_NO_VIEW_MODEL
    assert missing.runtime_activation_envelope_ready is False
    assert "missing_panel_view_model" in missing.failure_state_codes
    assert missing.mounted_panel_enabled is False

    invalid = build_read_only_advisory_panel_runtime_activation_envelope(_policy(flag=True), object())
    assert invalid.state is ReadOnlyPanelRuntimeActivationEnvelopeState.BLOCKED_UNSAFE_VIEW_MODEL
    assert invalid.runtime_activation_envelope_ready is False
    assert invalid.route_influence_enabled is False


def test_phase9_runtime_activation_policy_blocks_unsafe_toggles():
    unsafe_kwargs = [
        {"allow_actual_runtime_panel_activation": True},
        {"allow_renderer_activation": True},
        {"allow_mounted_panel": True},
        {"allow_runtime_ui_mutation": True},
        {"allow_runtime_telemetry_surface_wiring": True},
        {"allow_route_influence": True},
        {"allow_route_authority": True},
        {"allow_provider_calls": True},
        {"allow_persistence": True},
        {"allow_runtime_copilot_decision_behavior": True},
    ]
    for kwargs in unsafe_kwargs:
        try:
            ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
                activation_surface_id="phase9_runtime_activation_envelope",
                activation_surface_label="Phase 9 Runtime Activation Envelope",
                **kwargs,
            )
        except ValueError:
            pass
        else:
            raise AssertionError(f"unsafe policy unexpectedly accepted: {kwargs}")


def test_phase9_runtime_activation_implementation_docs_and_prerequisite():
    text = DOC.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    assert "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_implementation_v1" in text
    assert "Feature flag is default-off" in text
    assert "not** a renderer" in text
    assert "not a mounted panel" in text or "not** a mounted panel" in text
    assert "No renderer activation" in boundary
    assert "No route authority" in boundary
    assert "Probe returns a ready activation envelope" in readiness
    assert PREV.exists()


if __name__ == "__main__":
    test_phase9_runtime_activation_implementation_probe_is_safe_ready_envelope()
    test_phase9_runtime_activation_implementation_default_off_and_fail_open()
    test_phase9_runtime_activation_policy_blocks_unsafe_toggles()
    test_phase9_runtime_activation_implementation_docs_and_prerequisite()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation implementation")
