# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/deterministic_answers.py
"""Deterministic evidence-backed answer helpers for Project Reasoner V10."""

from __future__ import annotations

import re
from typing import Any
from .prompt_extraction import (
    extract_file_evidence_blocks,
    extract_file_id_map,
    extract_file_score_map,
    extract_locator_target,
    extract_runtime_anchors_from_detail,
    extract_snippet_blocks,
    extract_symbol_evidence_blocks,
    extract_symbol_id_map,
    extract_symbol_score_map,
    extract_user_question,
)
from .prompt_modes import is_one_line_prompt

from .deterministic_answer_parts import (
    _answer_one_line_from_prompt_impl,
    _repair_one_line_symbol_ids_impl,
    _score_file_locator_candidate_impl,
)

from .deterministic_answer_core import (
    _answer_deterministic_from_prompt_impl,
)

def score_file_locator_candidate(*args: object, **kwargs: object) -> object:
    """Delegate to the internal deterministic answer implementation."""
    return _score_file_locator_candidate_impl(*args, **kwargs)
def repair_one_line_symbol_ids(*args: object, **kwargs: object) -> object:
    """Delegate to the internal deterministic answer implementation."""
    return _repair_one_line_symbol_ids_impl(*args, **kwargs)
def answer_one_line_from_prompt(*args: object, **kwargs: object) -> object:
    """Delegate to the internal deterministic answer implementation."""
    return _answer_one_line_from_prompt_impl(*args, **kwargs)

def answer_deterministic_from_prompt(*args: object, **kwargs: object) -> object:
    """Delegate to the internal deterministic answer implementation."""
    return _answer_deterministic_from_prompt_impl(*args, **kwargs)

__all__ = [
    'score_file_locator_candidate',
    'answer_deterministic_from_prompt',
    'repair_one_line_symbol_ids',
    'answer_one_line_from_prompt',
]
