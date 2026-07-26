from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_host_binding_contract import (
    FORBIDDEN_HOST_BINDING_CAPABILITIES,
    REQUIRED_HOST_BINDING_CONTRACT_LABELS,
    ReadOnlyAdvisoryPanelHostBindingPolicy,
    ReadOnlyPanelHostBindingMode,
    ReadOnlyPanelHostBindingStatus,
    build_phase11_read_only_advisory_panel_host_binding_contract,
    build_phase11_read_only_panel_host_binding_contract_probe,
    evaluate_phase11_read_only_advisory_panel_host_binding_request,
)
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_renderer_mount import (
    build_phase10_read_only_panel_renderer_mount_implementation_probe,
)

DOC = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_CONTRACT_V1.md")
BOUNDARY = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_BOUNDARY_MODEL_V1.md")
READINESS = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE11_READ_ONLY_ADVISORY_PANEL_HOST_BINDING_CONTRACT_RESULT_REVIEW_READINESS_V1.md")
PREV = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/ML_ADVISORY_PHASE10_READ_ONLY_ADVISORY_PANEL_RENDERER_MOUNT_COMPLETION_HANDOFF_V1.md")


def test_phase11_host_binding_contract_default_decision():
    decision = build_phase11_read_only_advisory_panel_host_binding_contract()
    assert decision.feature_id == "rss_ml_adv_phase11_read_only_advisory_panel_host_binding_contract_v1"
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelHostBindingStatus.ACCEPTED_CONTRACT_ONLY
    assert decision.host_binding_mode is ReadOnlyPanelHostBindingMode.CONTRACT_ONLY
    assert decision.contract_only is True
    assert decision.future_host_binding_contract_ready is False
    assert decision.phase10_renderer_mount_descriptor_input_required is True
    assert decision.explicit_feature_flag_required is True
    assert decision.feature_flag_default_enabled is False
    assert decision.disabled_noop_control_required is True
    assert decision.fail_open_on_missing_descriptor_required is True
    assert decision.block_unsafe_descriptor_required is True
    assert decision.route_invariant_host_binding_required is True
    assert decision.final_selection_invisible_host_binding_required is True
    assert decision.host_input_bounded_required is True
    assert decision.host_output_bounded_required is True
    assert decision.removable_noop_host_binding_required is True
    assert decision.non_training_feedback_slot_required is True
    assert decision.final_router_remains_authoritative is True
    assert decision.ml_advisory_signal_telemetry_only is True
    assert decision.critical_boundary_error_budget == 0
    assert decision.actual_host_binding_enabled is False
    assert decision.host_binding_activation_enabled is False
    assert decision.runtime_app_host_visibility_enabled is False
    assert decision.mounted_runtime_panel_enabled is False
    assert decision.host_event_subscription_enabled is False
    assert decision.host_callback_registration_enabled is False
    assert decision.runtime_ui_mutation_enabled is False
    assert decision.runtime_telemetry_surface_wiring_enabled is False
    assert decision.route_influence_enabled is False
    assert decision.route_authority_enabled is False


def test_phase11_host_binding_contract_accepts_future_contract_only_with_safe_descriptor():
    descriptor = build_phase10_read_only_panel_renderer_mount_implementation_probe()
    policy = ReadOnlyAdvisoryPanelHostBindingPolicy(
        host_binding_mode=ReadOnlyPanelHostBindingMode.FUTURE_READ_ONLY_HOST_BINDING,
    )
    decision = evaluate_phase11_read_only_advisory_panel_host_binding_request(
        policy=policy,
        requested_capabilities={},
        renderer_mount_descriptor=descriptor,
    )
    assert decision.accepted is True
    assert decision.status is ReadOnlyPanelHostBindingStatus.ACCEPTED_FUTURE_READ_ONLY_HOST_BINDING_CONTRACT
    assert decision.future_host_binding_contract_ready is True
    assert decision.actual_host_binding_enabled is False
    assert decision.runtime_app_host_visibility_enabled is False
    assert decision.runtime_ui_mutation_enabled is False
    assert decision.route_authority_enabled is False


def test_phase11_host_binding_contract_blocks_missing_descriptor_for_future_binding():
    policy = ReadOnlyAdvisoryPanelHostBindingPolicy(
        host_binding_mode=ReadOnlyPanelHostBindingMode.FUTURE_READ_ONLY_HOST_BINDING,
    )
    decision = evaluate_phase11_read_only_advisory_panel_host_binding_request(
        policy=policy,
        requested_capabilities={},
        renderer_mount_descriptor=None,
    )
    assert decision.accepted is False
    assert decision.status is ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_SOURCE_DESCRIPTOR
    assert decision.future_host_binding_contract_ready is False
    assert decision.actual_host_binding_enabled is False


def test_phase11_host_binding_contract_blocks_unsafe_capabilities():
    checks = [
        ("route_authority", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("route_influence", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("route_override_button", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("use_ml_route_button", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("best_route_claim", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("final_selection_hook", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_AUTHORITY),
        ("actual_host_binding", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("host_binding_activation", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("runtime_app_host_visibility", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("mounted_runtime_panel", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("host_event_subscription", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("host_callback_registration", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("runtime_ui_mutation", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("runtime_telemetry_surface_wiring", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_RUNTIME_HOST_BINDING),
        ("router_call", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("advisor_call", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("adapter_execution", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("provider_call", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("persistence_write", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_DATA_OR_SIDE_EFFECT),
        ("prompt_ranking", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
        ("free_text_route_advice", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
        ("free_text_explanation", ReadOnlyPanelHostBindingStatus.BLOCKED_UNSAFE_TEXT_OR_CONTROLS),
    ]
    descriptor = build_phase10_read_only_panel_renderer_mount_implementation_probe()
    for capability, expected_status in checks:
        decision = evaluate_phase11_read_only_advisory_panel_host_binding_request(
            requested_capabilities={capability: True},
            renderer_mount_descriptor=descriptor,
        )
        assert decision.accepted is False
        assert decision.status is expected_status
        assert decision.route_authority_enabled is False
        assert decision.actual_host_binding_enabled is False
        assert decision.runtime_app_host_visibility_enabled is False


def test_phase11_host_binding_contract_probe_and_docs():
    probe = build_phase11_read_only_panel_host_binding_contract_probe()
    assert probe.accepted is True
    assert probe.future_host_binding_contract_ready is True
    text = DOC.read_text(encoding="utf-8")
    boundary = BOUNDARY.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    assert "host-binding contract only" in text
    assert "does not perform actual host binding" in text
    assert "runtime app-host visibility" in text
    assert "runtime Copilot decision behavior" in text
    assert "Phase 11 is contract-only" in boundary
    assert "must not attach anything to the runtime app host" in boundary
    assert "must verify that this patch is only a contract" in readiness
    assert PREV.exists()


def test_phase11_host_binding_constant_sets():
    assert "host_binding_default_off_label" in REQUIRED_HOST_BINDING_CONTRACT_LABELS
    assert "canonical_route_unchanged_label" in REQUIRED_HOST_BINDING_CONTRACT_LABELS
    assert "no_route_authority_label" in REQUIRED_HOST_BINDING_CONTRACT_LABELS
    assert "actual_host_binding" in FORBIDDEN_HOST_BINDING_CAPABILITIES
    assert "runtime_app_host_visibility" in FORBIDDEN_HOST_BINDING_CAPABILITIES
    assert "runtime_copilot_decision_behavior" in FORBIDDEN_HOST_BINDING_CAPABILITIES


if __name__ == "__main__":
    test_phase11_host_binding_contract_default_decision()
    test_phase11_host_binding_contract_accepts_future_contract_only_with_safe_descriptor()
    test_phase11_host_binding_contract_blocks_missing_descriptor_for_future_binding()
    test_phase11_host_binding_contract_blocks_unsafe_capabilities()
    test_phase11_host_binding_contract_probe_and_docs()
    test_phase11_host_binding_constant_sets()
    print("VALIDATION OK: phase11 read-only advisory panel host binding contract")
