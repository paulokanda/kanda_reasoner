import importlib


def test_phase13_passive_visibility_activation_contract_import_boundary():
    module = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_passive_visibility_activation_contract"
    )
    assert module.FEATURE_ID == "rss_ml_adv_phase13_read_only_advisory_panel_passive_visibility_activation_contract_v1"
    forbidden = module.FORBIDDEN_PASSIVE_VISIBILITY_ACTIVATION_CAPABILITIES
    assert "passive_visibility_activation" in forbidden
    assert "passive_visibility_slot_registration" in forbidden
    assert "runtime_ui_mutation" in forbidden
    assert "route_authority" in forbidden
    assert "runtime_copilot_decision_behavior" in forbidden
    assert hasattr(module, "build_phase13_read_only_advisory_panel_passive_visibility_activation_contract")
    assert hasattr(module, "evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request")


if __name__ == "__main__":
    test_phase13_passive_visibility_activation_contract_import_boundary()
    print("VALIDATION OK: phase13 read-only advisory panel passive visibility activation contract import boundary")
