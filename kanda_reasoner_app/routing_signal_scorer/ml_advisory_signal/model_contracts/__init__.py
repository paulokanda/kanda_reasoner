# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/model_contracts/__init__.py
"""Stable public model contracts for ML advisory signal implementations."""

from __future__ import annotations

from .passive_visibility_activation import (
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor,
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy,
    ReadOnlyAdvisoryPanelPassiveVisibilitySlot,
    ReadOnlyPanelPassiveVisibilityActivationImplementationState,
)

__all__ = [
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor",
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy",
    "ReadOnlyAdvisoryPanelPassiveVisibilitySlot",
    "ReadOnlyPanelPassiveVisibilityActivationImplementationState",
]
