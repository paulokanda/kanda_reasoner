# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/offline_real_adapter_boundary.py
"""Offline helper for Phase 5 real-adapter boundary probes.

The helper builds descriptor-only boundary checks. It never executes an
adapter and never calls a provider.
"""

from __future__ import annotations

from .real_adapter_boundary_contract import (
    RealAdapterBoundaryDecision,
    RealAdapterDescriptor,
    evaluate_real_adapter_boundary,
)


PHASE5_PROBE_LABEL = "phase5_offline_real_adapter_boundary_probe"


def build_phase5_offline_real_adapter_boundary_probe() -> RealAdapterBoundaryDecision:
    """Build a safe descriptor-only probe decision for Phase 5."""

    descriptor = RealAdapterDescriptor(
        adapter_label=PHASE5_PROBE_LABEL,
        adapter_kind="descriptor_only_future_adapter_boundary",
        declared_input_contract_id="advisory_input_v1_offline_only",
        declared_output_contract_id="advisory_output_v1_bounded_flags_only",
    )
    return evaluate_real_adapter_boundary(descriptor)
