# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/contract.py
"""Contracts for the Phase 1a ML advisory signal boundary.

The objects in this module are intentionally small, frozen, and free of
provider, embedding, persistence, router-canon, prompt-library, and freeze
memory access. They carry advisory telemetry only. They cannot select a
route or bind a prompt.
"""

from __future__ import annotations


__all__ = [
    'AdvisoryFlag',
    'AdvisoryGroupObservation',
    'AdvisoryInput',
    'AdvisoryOutput',
    'AdvisoryReasonCode',
    'BoundaryStatus',
    'build_abstain_output',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple


class AdvisoryFlag(str, Enum):
    """Canned advisory flags without route authority."""

    AMBIGUITY_DETECTED = "AMBIGUITY_DETECTED"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    PROMPT_GAP_DETECTED = "PROMPT_GAP_DETECTED"
    BOUNDARY_RISK_DETECTED = "BOUNDARY_RISK_DETECTED"
    MANUAL_REVIEW_SUGGESTED = "MANUAL_REVIEW_SUGGESTED"
    ABSTAINED = "ABSTAINED"


class AdvisoryReasonCode(str, Enum):
    """Canned reason codes used instead of free-text explanations."""

    LOW_SIGNAL_INPUT = "LOW_SIGNAL_INPUT"
    MULTIPLE_CANDIDATE_GROUPS = "MULTIPLE_CANDIDATE_GROUPS"
    GROUP_OVERLAP_RISK = "GROUP_OVERLAP_RISK"
    PROMPT_GAP_RISK = "PROMPT_GAP_RISK"
    BOUNDARY_UNCERTAINTY = "BOUNDARY_UNCERTAINTY"
    MOCK_DETERMINISTIC_RULE = "MOCK_DETERMINISTIC_RULE"
    NULL_ADVISOR_DEFAULT = "NULL_ADVISOR_DEFAULT"


class BoundaryStatus(str, Enum):
    """Boundary status for non-authoritative advisory output."""

    SAFE_NON_AUTHORITATIVE = "SAFE_NON_AUTHORITATIVE"
    ABSTAINED = "ABSTAINED"
    REJECTED_BY_FIREWALL = "REJECTED_BY_FIREWALL"


@dataclass(frozen=True)
class AdvisoryInput:
    """Sanitized input envelope for an advisory-only signal.

    The input stores only caller-supplied, sanitized values. It is not a
    route request, not prompt text, not a dataset row, and not a source of
    router authority.
    """

    scenario_id: str
    sanitized_context_hash: str
    candidate_prompt_group_ids: Tuple[str, ...]
    ambiguity_score: float
    conflict_score: float
    risk_family_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("scenario_id", self.scenario_id)
        _require_text("sanitized_context_hash", self.sanitized_context_hash)
        _require_tuple_of_text("candidate_prompt_group_ids", self.candidate_prompt_group_ids)
        _require_score("ambiguity_score", self.ambiguity_score)
        _require_score("conflict_score", self.conflict_score)
        if self.risk_family_id is not None:
            _require_text("risk_family_id", self.risk_family_id)


@dataclass(frozen=True)
class AdvisoryGroupObservation:
    """Observation about a candidate prompt group without ranking it."""

    prompt_group_id: str
    observation_codes: Tuple[AdvisoryReasonCode, ...]
    normalized_score: float

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("prompt_group_id", self.prompt_group_id)
        _require_tuple_of_enum(
            "observation_codes",
            self.observation_codes,
            AdvisoryReasonCode,
        )
        _require_score("normalized_score", self.normalized_score)


@dataclass(frozen=True)
class AdvisoryOutput:
    """Advisory-only output with no route, winner, or ranking fields."""

    advisory_flags: Tuple[AdvisoryFlag, ...]
    advisory_group_observations: Tuple[AdvisoryGroupObservation, ...]
    advisory_should_abstain: bool
    non_authoritative_confidence: float
    advisory_reason_codes: Tuple[AdvisoryReasonCode, ...]
    boundary_status: BoundaryStatus
    is_mock: bool

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_tuple_of_enum("advisory_flags", self.advisory_flags, AdvisoryFlag)
        _require_tuple_of_type(
            "advisory_group_observations",
            self.advisory_group_observations,
            AdvisoryGroupObservation,
        )
        if not isinstance(self.advisory_should_abstain, bool):
            raise TypeError("advisory_should_abstain must be bool")
        _require_score("non_authoritative_confidence", self.non_authoritative_confidence)
        _require_tuple_of_enum(
            "advisory_reason_codes",
            self.advisory_reason_codes,
            AdvisoryReasonCode,
        )
        if not isinstance(self.boundary_status, BoundaryStatus):
            raise TypeError("boundary_status must be BoundaryStatus")
        if not isinstance(self.is_mock, bool):
            raise TypeError("is_mock must be bool")


def build_abstain_output(*, is_mock: bool = False) -> AdvisoryOutput:
    """Return the safe fallback advisory output."""

    return AdvisoryOutput(
        advisory_flags=(AdvisoryFlag.ABSTAINED,),
        advisory_group_observations=(),
        advisory_should_abstain=True,
        non_authoritative_confidence=0.0,
        advisory_reason_codes=(AdvisoryReasonCode.NULL_ADVISOR_DEFAULT,),
        boundary_status=BoundaryStatus.ABSTAINED,
        is_mock=is_mock,
    )


def _require_text(name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _require_score(name: str, value: float) -> None:
    """Support require score behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : float
        The input value.
    """
    
    if not isinstance(value, (float, int)) or isinstance(value, bool):
        raise TypeError(f"{name} must be a number")
    if float(value) < 0.0 or float(value) > 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


def _require_tuple_of_text(name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple of text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[str, ...]
        The input value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a tuple")
    for item in value:
        _require_text(name, item)


def _require_tuple_of_enum(name: str, value: tuple, enum_type: type[Enum]) -> None:
    """Support require tuple of enum behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : tuple
        The input value.
    enum_type : type[Enum]
        The enum type value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a tuple")
    for item in value:
        if not isinstance(item, enum_type):
            raise TypeError(f"{name} contains an invalid enum item")


def _require_tuple_of_type(name: str, value: tuple, item_type: type) -> None:
    """Support require tuple of type behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : tuple
        The input value.
    item_type : type
        The item type value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a tuple")
    for item in value:
        if not isinstance(item, item_type):
            raise TypeError(f"{name} contains an invalid item")
