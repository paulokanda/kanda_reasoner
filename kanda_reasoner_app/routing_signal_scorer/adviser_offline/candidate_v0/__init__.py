"""Offline Adviser Candidate v0 package.

This package is intentionally not exported by runtime routing modules. It is an
adviser-only, offline, standard-library-only candidate implementation.
"""

from .offline_lexical_scorer import build_candidate_answer, classify_input

__all__ = ["build_candidate_answer", "classify_input"]
