from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_activation_contract import (
    FORBIDDEN_RUNTIME_ACTIVATION_CAPABILITIES,
    REQUIRED_SAFE_RUNTIME_CONTRACT_LABELS,
    ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    ReadOnlyPanelRuntimeActivationMode,
    ReadOnlyPanelRuntimeActivationStatus,
    build_phase9_read_only_advisory_panel_runtime_activation_contract,
    build_phase9_read_only_panel_runtime_activation_contract_probe,
    evaluate_phase9_read_only_advisory_panel_runtime_activation_request,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_ui import (
    build_phase8_read_only_advisory_panel_ui_probe,
)

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_CONTRACT_V1.md")
BOUNDARY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_BOUNDARY_MODEL_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_CONTRACT_RESULT_REVIEW_READINESS_V1.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE8_READ_ONLY_ADVISORY_PANEL_UI_COMPLETION_HANDOFF_V1.md")


def test_phase9_runtime_activation_contract_default_decision():
    decision = build_phase9_read_only_advisory_panel_runtime_activation_contract()
    assert decision.feature_id == "rss_ml_adv_phase9_read_only_advisory_panel_runtime_activation_contract_v1"
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelRuntimeActivationStatus.ACCEPTED_CONTRACT_ONLY
    assert decision.contract_only is True
    assert decision.future_runtime_panel_contract_ready is False
    assert decision.actual_runtime_panel_activation_enabled is False
    assert decision.renderer_activation_enabled is False
    assert decision.mounted_panel_enabled is False
    assert decision.runtime_ui_mutation_enabled is False
    assert decision.runtime_telemetry_surface_wiring_enabled is False
    assert decision.route_influence_enabled is False
    assert decision.route_authority_enabled is False
    assert decision.router_calls_enabled is False
    assert decision.advisor_calls_enabled is False
    assert decision.adapter_execution_enabled is False
    assert decision.provider_calls_enabled is False
    assert decision.persistence_enabled is False
    assert decision.phase8_view_model_input_required is True
    assert decision.explicit_feature_flag_required is True
    assert decision.feature_flag_default_enabled is False
    assert decision.fail_open_on_missing_view_model_required is True
    assert decision.renderer_adapter_separate_future_contract_required is True
    assert decision.final_router_remains_authoritative is True
    assert decision.ml_advisory_signal_telemetry_only is True
    assert decision.critical_boundary_error_budget == 0


def test_phase9_runtime_activation_contract_accepts_future_contract_only_with_safe_view_model():
    panel_view_model = build_phase8_read_only_advisory_panel_ui_probe()
    policy = ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_mode=ReadOnlyPanelRuntimeActivationMode.FUTURE_READ_ONLY_RUNTIME_PANEL,
    )
    decision = evaluate_phase9_read_only_advisory_panel_runtime_activation_request(
        policy=policy,
        requested_capabilities={},
        panel_view_model=panel_view_model,
    )
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelRuntimeActivationStatus.ACCEPTED_FUTURE_READ_ONLY_RUNTIME_PANEL_CONTRACT
    assert decision.future_runtime_panel_contract_ready is True
    assert decision.actual_runtime_panel_activation_enabled is False
    assert decision.mounted_panel_enabled is False
    assert decision.route_authority_enabled is False


def test_phase9_runtime_activation_contract_blocks_missing_view_model_for_future_activation():
    policy = ReadOnlyAdvisoryPanelRuntimeActivationPolicy(
        activation_mode=ReadOnlyPanelRuntimeActivationMode.FUTURE_READ_ONLY_RUNTIME_PANEL,
    )
    decision = evaluate_phase9_read_only_advisory_panel_runtime_activation_request(
        policy=policy,
        requested_capabilities={},
        panel_view_model=None,
    )
    assert decision.accepted is False
    assert decision.status is ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_SOURCE_MODEL
    assert decision.future_runtime_panel_contract_ready is False
    assert decision.actual_runtime_panel_activation_enabled is False


def test_phase9_runtime_activation_contract_blocks_unsafe_capabilities():
    checks = [
        ("route_authority", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("route_influence", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("route_override_button", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("use_ml_route_button", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("best_route_claim", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("actual_runtime_panel_activation", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("renderer_activation", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("mounted_panel", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("runtime_ui_mutation", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("runtime_telemetry_surface_wiring", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("router_call", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("advisor_call", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("adapter_execution", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("provider_call", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("persistence_write", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("prompt_ranking", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
        ("free_text_route_advice", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
        ("free_text_explanation", ReadOnlyPanelRuntimeActivationStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
    ]
    for capability, expected_status in checks:
        decision = evaluate_phase9_read_only_advisory_panel_runtime_activation_request(
            requested_capabilities={capability: True},
            panel_view_model=build_phase8_read_only_advisory_panel_ui_probe(),
        )
        assert decision.accepted is False
        assert decision.status is expected_status
        assert decision.route_authority_enabled is False
        assert decision.actual_runtime_panel_activation_enabled is False


def test_phase9_runtime_activation_contract_probe_and_docs():
    probe = build_phase9_read_only_panel_runtime_activation_contract_probe()
    assert probe.accepted is True
    assert probe.future_runtime_panel_contract_ready is True
    text = DOC.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    assert "runtime-visible panel track as a **contract only**" in text
    assert "does not activate a runtime panel" in text
    assert "feature-flagged, default-off" in text
    assert "route override button" in text
    assert "runtime Copilot decision behavior" in text
    assert "not runtime activation and not a renderer" in boundary
    assert "feature flag default must be disabled" in boundary
    assert "no actual runtime panel activation" in boundary
    assert "must not activate a runtime panel" in readiness
    assert PREV.exists()


def test_phase9_runtime_activation_constant_sets():
    assert "advisory_role_label" in REQUIRED_SAFE_RUNTIME_CONTRACT_LABELS
    assert "canonical_route_unchanged_label" in REQUIRED_SAFE_RUNTIME_CONTRACT_LABELS
    assert "no_route_authority_label" in REQUIRED_SAFE_RUNTIME_CONTRACT_LABELS
    assert "route_override_button" in FORBIDDEN_RUNTIME_ACTIVATION_CAPABILITIES
    assert "runtime_copilot_decision_behavior" in FORBIDDEN_RUNTIME_ACTIVATION_CAPABILITIES
    assert "router_call" in FORBIDDEN_RUNTIME_ACTIVATION_CAPABILITIES


if __name__ == "__main__":
    test_phase9_runtime_activation_contract_default_decision()
    test_phase9_runtime_activation_contract_accepts_future_contract_only_with_safe_view_model()
    test_phase9_runtime_activation_contract_blocks_missing_view_model_for_future_activation()
    test_phase9_runtime_activation_contract_blocks_unsafe_capabilities()
    test_phase9_runtime_activation_contract_probe_and_docs()
    test_phase9_runtime_activation_constant_sets()
    print("VALIDATION OK: phase9 read-only advisory panel runtime activation contract")
