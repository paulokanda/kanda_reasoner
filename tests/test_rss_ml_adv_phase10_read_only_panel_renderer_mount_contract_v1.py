from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_renderer_mount_contract import (
    FORBIDDEN_RENDERER_MOUNT_CAPABILITIES,
    REQUIRED_RENDERER_MOUNT_CONTRACT_LABELS,
    ReadOnlyAdvisoryPanelRendererMountPolicy,
    ReadOnlyPanelRendererMountMode,
    ReadOnlyPanelRendererMountStatus,
    build_phase10_read_only_advisory_panel_renderer_mount_contract,
    build_phase10_read_only_panel_renderer_mount_contract_probe,
    evaluate_phase10_read_only_advisory_panel_renderer_mount_request,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_activation import (
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
)

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_CONTRACT_V1.md")
BOUNDARY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_BOUNDARY_MODEL_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_CONTRACT_RESULT_REVIEW_READINESS_V1.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE9_READ_ONLY_ADVISORY_PANEL_RUNTIME_ACTIVATION_COMPLETION_HANDOFF_V1.md")


def test_phase10_renderer_mount_contract_default_decision():
    decision = build_phase10_read_only_advisory_panel_renderer_mount_contract()
    assert decision.feature_id == "rss_ml_adv_phase10_read_only_advisory_panel_renderer_mount_contract_v1"
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelRendererMountStatus.ACCEPTED_CONTRACT_ONLY
    assert decision.mount_mode is ReadOnlyPanelRendererMountMode.CONTRACT_ONLY
    assert decision.contract_only is True
    assert decision.future_renderer_mount_contract_ready is False
    assert decision.phase9_activation_envelope_input_required is True
    assert decision.explicit_feature_flag_required is True
    assert decision.feature_flag_default_enabled is False
    assert decision.disabled_noop_control_required is True
    assert decision.fail_open_on_missing_envelope_required is True
    assert decision.route_invariant_mount_required is True
    assert decision.final_selection_invisible_mount_required is True
    assert decision.renderer_input_bounded_required is True
    assert decision.renderer_output_bounded_required is True
    assert decision.removable_noop_mount_required is True
    assert decision.non_training_feedback_slot_required is True
    assert decision.final_router_remains_authoritative is True
    assert decision.ml_advisory_signal_telemetry_only is True
    assert decision.critical_boundary_error_budget == 0
    assert decision.actual_runtime_panel_activation_enabled is False
    assert decision.actual_renderer_mount_enabled is False
    assert decision.renderer_activation_enabled is False
    assert decision.mounted_panel_enabled is False
    assert decision.runtime_ui_mutation_enabled is False
    assert decision.runtime_telemetry_surface_wiring_enabled is False
    assert decision.route_influence_enabled is False
    assert decision.route_authority_enabled is False


def test_phase10_renderer_mount_contract_accepts_future_contract_only_with_safe_envelope():
    envelope = build_phase9_read_only_panel_runtime_activation_implementation_probe()
    policy = ReadOnlyAdvisoryPanelRendererMountPolicy(
        mount_mode=ReadOnlyPanelRendererMountMode.FUTURE_READ_ONLY_RENDERER_MOUNT,
    )
    decision = evaluate_phase10_read_only_advisory_panel_renderer_mount_request(
        policy=policy,
        requested_capabilities={},
        activation_envelope=envelope,
    )
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelRendererMountStatus.ACCEPTED_FUTURE_READ_ONLY_RENDERER_MOUNT_CONTRACT
    assert decision.future_renderer_mount_contract_ready is True
    assert decision.actual_renderer_mount_enabled is False
    assert decision.renderer_activation_enabled is False
    assert decision.mounted_panel_enabled is False
    assert decision.route_authority_enabled is False


def test_phase10_renderer_mount_contract_blocks_missing_envelope_for_future_mount():
    policy = ReadOnlyAdvisoryPanelRendererMountPolicy(
        mount_mode=ReadOnlyPanelRendererMountMode.FUTURE_READ_ONLY_RENDERER_MOUNT,
    )
    decision = evaluate_phase10_read_only_advisory_panel_renderer_mount_request(
        policy=policy,
        requested_capabilities={},
        activation_envelope=None,
    )
    assert decision.accepted is False
    assert decision.status is ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_SOURCE_ENVELOPE
    assert decision.future_renderer_mount_contract_ready is False
    assert decision.actual_renderer_mount_enabled is False


def test_phase10_renderer_mount_contract_blocks_unsafe_capabilities():
    checks = [
        ("route_authority", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("route_influence", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("route_override_button", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("use_ml_route_button", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("best_route_claim", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("final_selection_hook", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("actual_runtime_panel_activation", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("actual_renderer_mount", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("renderer_activation", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("mounted_panel", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("runtime_ui_mutation", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("runtime_telemetry_surface_wiring", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_RUNTIME_WIRING),
        ("router_call", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("advisor_call", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("adapter_execution", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("provider_call", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("persistence_write", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("prompt_ranking", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
        ("free_text_route_advice", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
        ("free_text_explanation", ReadOnlyPanelRendererMountStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
    ]
    envelope = build_phase9_read_only_panel_runtime_activation_implementation_probe()
    for capability, expected_status in checks:
        decision = evaluate_phase10_read_only_advisory_panel_renderer_mount_request(
            requested_capabilities={capability: True},
            activation_envelope=envelope,
        )
        assert decision.accepted is False
        assert decision.status is expected_status
        assert decision.route_authority_enabled is False
        assert decision.actual_renderer_mount_enabled is False


def test_phase10_renderer_mount_contract_probe_and_docs():
    probe = build_phase10_read_only_panel_renderer_mount_contract_probe()
    assert probe.accepted is True
    assert probe.future_renderer_mount_contract_ready is True
    text = DOC.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    assert "renderer/mount contract only" in text
    assert "does not activate a renderer" in text
    assert "actual renderer mount" in text
    assert "runtime Copilot decision behavior" in text
    assert "not visible ML integration" in boundary
    assert "no actual renderer mount" in boundary
    assert "must verify that this patch is only a contract" in readiness
    assert PREV.exists()


def test_phase10_renderer_mount_constant_sets():
    assert "read_only_panel_label" in REQUIRED_RENDERER_MOUNT_CONTRACT_LABELS
    assert "canonical_route_unchanged_label" in REQUIRED_RENDERER_MOUNT_CONTRACT_LABELS
    assert "no_route_authority_label" in REQUIRED_RENDERER_MOUNT_CONTRACT_LABELS
    assert "actual_renderer_mount" in FORBIDDEN_RENDERER_MOUNT_CAPABILITIES
    assert "runtime_copilot_decision_behavior" in FORBIDDEN_RENDERER_MOUNT_CAPABILITIES
    assert "router_call" in FORBIDDEN_RENDERER_MOUNT_CAPABILITIES


if __name__ == "__main__":
    test_phase10_renderer_mount_contract_default_decision()
    test_phase10_renderer_mount_contract_accepts_future_contract_only_with_safe_envelope()
    test_phase10_renderer_mount_contract_blocks_missing_envelope_for_future_mount()
    test_phase10_renderer_mount_contract_blocks_unsafe_capabilities()
    test_phase10_renderer_mount_contract_probe_and_docs()
    test_phase10_renderer_mount_constant_sets()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount contract")
