# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/advisor_interface.py
"""Advisor protocol for Phase 1a non-authoritative signals."""

from __future__ import annotations

from typing import Protocol

from .contract import AdvisoryInput, AdvisoryOutput


class AdvisorProtocol(Protocol):
    """Protocol for advisory-only implementations.

    Implementations may emit advisory flags only. They must not choose a
    final route, load prompts, call providers, persist outputs, or mutate a
    registry.
    """

    def advise(self, advisory_input: AdvisoryInput) -> AdvisoryOutput:
        """Return advisory telemetry for the supplied sanitized input."""
