"""Offline Adviser evaluation package.

This package contains pure in-memory evaluation helpers for Adviser-only
candidate comparison. It is not part of runtime routing.
"""

from .candidate_v0_evaluation_runner import (
    FEATURE_ID,
    SCHEMA_VERSION,
    evaluate_candidate_v0_against_gold_cases,
)

__all__ = [
    "FEATURE_ID",
    "SCHEMA_VERSION",
    "evaluate_candidate_v0_against_gold_cases",
]
