# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/prompt_extraction.py
"""Public prompt parsing contract for Project Reasoner AI bridge."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.reasoner_engine.ai_bridge_help._prompt_extraction_allowed import (
    extract_allowed_file_paths as _extract_allowed_file_paths,
    extract_allowed_ids as _extract_allowed_ids,
    extract_allowed_symbols as _extract_allowed_symbols,
    extract_cited_ids as _extract_cited_ids,
    extract_path_like_mentions as _extract_path_like_mentions,
    extract_symbol_like_mentions as _extract_symbol_like_mentions,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge_help._prompt_extraction_blocks import (
    extract_file_evidence_blocks as _extract_file_evidence_blocks,
    extract_runtime_anchors_from_detail as _extract_runtime_anchors_from_detail,
    extract_snippet_blocks as _extract_snippet_blocks,
    extract_snippet_text_blob as _extract_snippet_text_blob,
    extract_symbol_evidence_blocks as _extract_symbol_evidence_blocks,
    extract_user_question as _extract_user_question,
)
from kanda_reasoner_app.reasoner_engine.ai_bridge_help._prompt_extraction_maps import (
    extract_file_id_map as _extract_file_id_map,
    extract_file_score_map as _extract_file_score_map,
    extract_locator_target as _extract_locator_target,
    extract_one_line_triplet as _extract_one_line_triplet,
    extract_symbol_id_map as _extract_symbol_id_map,
    extract_symbol_score_map as _extract_symbol_score_map,
)

__all__ = [
    "extract_runtime_anchors_from_detail",
    "extract_snippet_text_blob",
    "extract_snippet_blocks",
    "extract_file_evidence_blocks",
    "extract_symbol_evidence_blocks",
    "extract_user_question",
    "extract_allowed_ids",
    "extract_cited_ids",
    "extract_allowed_symbols",
    "extract_allowed_file_paths",
    "extract_path_like_mentions",
    "extract_symbol_like_mentions",
    "extract_symbol_id_map",
    "extract_file_id_map",
    "extract_symbol_score_map",
    "extract_file_score_map",
    "extract_locator_target",
    "extract_one_line_triplet",
]


def extract_runtime_anchors_from_detail(detail_text: str) -> list[str]:
    """Extract the runtime anchors from detail."""
    return _extract_runtime_anchors_from_detail(detail_text)


def extract_snippet_text_blob(prompt: str) -> str:
    """Return concatenated snippet text, including live-source snippets."""
    return _extract_snippet_text_blob(prompt)


def extract_snippet_blocks(prompt: str) -> list[dict[str, Any]]:
    """Extract SOURCE SNIPPETS and LIVE SOURCE EVIDENCE snippet blocks."""
    return _extract_snippet_blocks(prompt)


def extract_file_evidence_blocks(prompt: str) -> list[dict[str, Any]]:
    """Extract the file evidence blocks."""
    return _extract_file_evidence_blocks(prompt)


def extract_symbol_evidence_blocks(prompt: str) -> list[dict[str, Any]]:
    """Extract the symbol evidence blocks."""
    return _extract_symbol_evidence_blocks(prompt)


def extract_user_question(prompt: str) -> str:
    """Extract the user question."""
    return _extract_user_question(prompt)


def extract_allowed_ids(prompt: str) -> set[str]:
    """Extract the allowed ids."""
    return _extract_allowed_ids(prompt)


def extract_cited_ids(text: str) -> set[str]:
    """Extract the cited ids."""
    return _extract_cited_ids(text)


def extract_allowed_symbols(prompt: str) -> set[str]:
    """Extract the allowed symbols."""
    return _extract_allowed_symbols(prompt)


def extract_allowed_file_paths(prompt: str) -> set[str]:
    """Extract the allowed file paths."""
    return _extract_allowed_file_paths(prompt)


def extract_path_like_mentions(text: str) -> set[str]:
    """Extract slash or backslash path-like mentions from answer text."""
    return _extract_path_like_mentions(text)


def extract_symbol_like_mentions(text: str) -> set[str]:
    """Extract the symbol like mentions."""
    return _extract_symbol_like_mentions(text)


def extract_symbol_id_map(prompt: str) -> dict[str, str]:
    """Extract the symbol id map."""
    return _extract_symbol_id_map(prompt)


def extract_file_id_map(prompt: str) -> dict[str, str]:
    """Extract the file id map."""
    return _extract_file_id_map(prompt)


def extract_symbol_score_map(prompt: str) -> list[tuple[str, str, str, int]]:
    """Extract the symbol score map."""
    return _extract_symbol_score_map(prompt)


def extract_file_score_map(prompt: str) -> list[tuple[str, str, int]]:
    """Extract the file score map."""
    return _extract_file_score_map(prompt)


def extract_locator_target(question: str) -> str:
    """Extract the locator target."""
    return _extract_locator_target(question)


def extract_one_line_triplet(text: str) -> str:
    """Extract the one line triplet."""
    return _extract_one_line_triplet(text)
