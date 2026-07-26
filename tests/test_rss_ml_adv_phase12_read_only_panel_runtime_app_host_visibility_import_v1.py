import importlib


def test_phase12_runtime_app_host_visibility_contract_import_boundary():
    module = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_app_host_visibility_contract"
    )
    assert module.FEATURE_ID == "rss_ml_adv_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract_v1"
    forbidden = module.FORBIDDEN_RUNTIME_APP_HOST_VISIBILITY_CAPABILITIES
    assert "actual_runtime_app_host_visibility" in forbidden
    assert "runtime_ui_mutation" in forbidden
    assert "route_authority" in forbidden
    assert "runtime_copilot_decision_behavior" in forbidden
    assert hasattr(module, "build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract")
    assert hasattr(module, "evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request")


if __name__ == "__main__":
    test_phase12_runtime_app_host_visibility_contract_import_boundary()
    print("VALIDATION OK: phase12 read-only advisory panel runtime app-host visibility contract import boundary")
