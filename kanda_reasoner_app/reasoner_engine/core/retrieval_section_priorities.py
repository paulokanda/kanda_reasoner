# project-path: kanda_reasoner_app/reasoner_engine/core/retrieval_section_priorities.py
"""Section-priority rules for reasoner engine retrieval."""

from __future__ import annotations

from typing import Any


SECTION_PRIORITY_BY_QUERY_KIND: dict[str, tuple[str, ...]] = {
    "packaging_metadata": (
        "packaging_metadata",
        "project_summary",
        "files",
        "symbol_index",
        "line_level_source_truth",
    ),
    "documentation_intent": (
        "documentation_intent",
        "project_summary",
        "files",
        "line_level_source_truth",
    ),
    "startup": (
        "project_summary",
        "files",
        "symbol_index",
        "execution_chains",
        "line_level_source_truth",
    ),
    "runtime_heavy": (
        "runtime",
        "files",
        "symbol_index",
        "line_level_source_truth",
    ),
    "default": (
        "project_summary",
        "files",
        "symbol_index",
        "line_level_source_truth",
    ),
}

__all__ = [
    "SECTION_PRIORITY_BY_QUERY_KIND",
    "get_section_priority",
    "normalize_query_kind",
]


def normalize_query_kind(value: Any) -> str:
    """Return the normalized query kind used for section-priority lookup."""
    text = str(value).strip().lower() if value is not None else ""
    return text or "default"


def get_section_priority(query_kind: Any) -> tuple[str, ...]:
    """Return retrieval section priorities for a query kind."""
    normalized = normalize_query_kind(query_kind)
    return SECTION_PRIORITY_BY_QUERY_KIND.get(
        normalized,
        SECTION_PRIORITY_BY_QUERY_KIND["default"],
    )
