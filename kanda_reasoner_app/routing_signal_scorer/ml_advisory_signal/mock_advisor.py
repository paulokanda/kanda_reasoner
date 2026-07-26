# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/mock_advisor.py
"""Deterministic mock advisor for Phase 1a tests.

This class is not real ML. It uses simple caller-supplied scores to produce
stable advisory flags for boundary tests.
"""

from __future__ import annotations

from .contract import (
    AdvisoryFlag,
    AdvisoryGroupObservation,
    AdvisoryInput,
    AdvisoryOutput,
    AdvisoryReasonCode,
    BoundaryStatus,
)
from .output_firewall import validate_advisory_output


class MockAdvisor:
    """Deterministic advisory-only implementation."""

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
        
        flags: list[AdvisoryFlag] = []
        reasons: list[AdvisoryReasonCode] = [AdvisoryReasonCode.MOCK_DETERMINISTIC_RULE]

        if advisory_input.ambiguity_score >= 0.50:
            flags.append(AdvisoryFlag.AMBIGUITY_DETECTED)
            reasons.append(AdvisoryReasonCode.MULTIPLE_CANDIDATE_GROUPS)
        if advisory_input.conflict_score >= 0.50:
            flags.append(AdvisoryFlag.CONFLICT_DETECTED)
            reasons.append(AdvisoryReasonCode.GROUP_OVERLAP_RISK)
        if advisory_input.risk_family_id == "prompt_gap":
            flags.append(AdvisoryFlag.PROMPT_GAP_DETECTED)
            reasons.append(AdvisoryReasonCode.PROMPT_GAP_RISK)

        if not flags:
            flags.append(AdvisoryFlag.MANUAL_REVIEW_SUGGESTED)
            reasons.append(AdvisoryReasonCode.LOW_SIGNAL_INPUT)

        observations = tuple(
            AdvisoryGroupObservation(
                prompt_group_id=group_id,
                observation_codes=(AdvisoryReasonCode.MOCK_DETERMINISTIC_RULE,),
                normalized_score=max(
                    advisory_input.ambiguity_score,
                    advisory_input.conflict_score,
                ),
            )
            for group_id in advisory_input.candidate_prompt_group_ids
        )

        confidence = min(
            1.0,
            max(advisory_input.ambiguity_score, advisory_input.conflict_score),
        )
        output = AdvisoryOutput(
            advisory_flags=tuple(flags),
            advisory_group_observations=observations,
            advisory_should_abstain=False,
            non_authoritative_confidence=confidence,
            advisory_reason_codes=tuple(dict.fromkeys(reasons)),
            boundary_status=BoundaryStatus.SAFE_NON_AUTHORITATIVE,
            is_mock=True,
        )
        validate_advisory_output(output)
        return output
