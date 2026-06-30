# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/evaluation/__init__.py
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
