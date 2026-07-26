# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/null_advisor.py
"""Null advisor for safe Phase 1a fallback behavior."""

from __future__ import annotations

from .contract import AdvisoryInput, AdvisoryOutput, build_abstain_output
from .output_firewall import validate_advisory_output


class NullAdvisor:
    """Always abstain without side effects or authority."""

    def advise(self, advisory_input: AdvisoryInput) -> AdvisoryOutput:
        """Support advise behavior.
        
        Parameters
        ----------
        advisory_input : AdvisoryInput
            The advisory input value.
        
        Returns
        -------
        AdvisoryOutput
            The advisory output result.
        """
        
        del advisory_input
        output = build_abstain_output(is_mock=False)
        validate_advisory_output(output)
        return output
