import inspect

from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal import read_only_advisory_panel_runtime_app_host_visibility as module
from kanda_reasoner_app.routing_signal_scorer.ml_advisory_signal.read_only_advisory_panel_runtime_app_host_visibility import (
    build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe,
)


def test_phase12_visibility_implementation_import_boundary_has_no_forbidden_dependencies():
    source = inspect.getsource(module).lower()
    forbidden_fragments = (
        "requests",
        "urllib",
        "socket",
        "subprocess",
        "openai",
        "chromadb",
        "faiss",
        "sqlite3",
        "pickle",
        "pathlib",
        "open(",
        "host_event_subscription_enabled = true",
        "host_callback_registration_enabled = true",
        "runtime_ui_mutation_enabled = true",
        "runtime_telemetry_surface_wiring_enabled = true",
    )
    for fragment in forbidden_fragments:
        assert fragment not in source


def test_phase12_visibility_implementation_probe_is_pure_descriptor():
    descriptor = build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe()
    assert descriptor.read_only_runtime_app_host_visibility_descriptor_ready is True
    assert descriptor.actual_runtime_app_host_visibility_enabled is False
    assert descriptor.visibility_activation_enabled is False
    assert descriptor.runtime_ui_mutation_enabled is False
    assert descriptor.runtime_telemetry_surface_wiring_enabled is False
    assert descriptor.host_event_subscription_enabled is False
    assert descriptor.host_callback_registration_enabled is False
    assert descriptor.route_authority_enabled is False
    assert descriptor.runtime_copilot_decision_behavior_enabled is False
    assert descriptor.autonomous_ml_router_enabled is False


if __name__ == "__main__":
    test_phase12_visibility_implementation_import_boundary_has_no_forbidden_dependencies()
    test_phase12_visibility_implementation_probe_is_pure_descriptor()
    print("VALIDATION OK: phase12 read-only advisory panel runtime app-host visibility implementation import boundary")
