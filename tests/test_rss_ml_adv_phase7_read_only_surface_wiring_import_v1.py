from __future__ import annotations

import importlib


def test_phase7_read_only_surface_wiring_import_boundary() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_surface_wiring"
    )
    assert module.FEATURE_ID == "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_v1"
    assert module.SOURCE_REVIEW_FEATURE_ID == "rss_ml_adv_phase7_guarded_advisory_surface_wiring_contract_result_review_gate_v1"
    envelope = module.build_phase7_read_only_surface_wiring_probe()
    assert envelope.feature_id == "rss_ml_adv_phase7_read_only_advisory_surface_wiring_implementation_v1"
    assert envelope.route_authority_enabled is False
    assert envelope.runtime_advisory_panel_enabled is False
    assert envelope.runtime_telemetry_surface_wired is False


def test_package_exports_phase7_read_only_surface_wiring() -> None:
    pkg = importlib.import_module(
        "kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal"
    )
    assert hasattr(pkg, "CanonicalDispatchSnapshot")
    assert hasattr(pkg, "ReadOnlyAdvisorySurfaceWiringPolicy")
    assert hasattr(pkg, "ReadOnlyAdvisorySurfaceWiringEnvelope")
    assert hasattr(pkg, "build_read_only_advisory_surface_wiring_envelope")


if __name__ == "__main__":
    test_phase7_read_only_surface_wiring_import_boundary()
    test_package_exports_phase7_read_only_surface_wiring()
    print("VALIDATION OK: phase7 read-only advisory surface wiring import boundary")
