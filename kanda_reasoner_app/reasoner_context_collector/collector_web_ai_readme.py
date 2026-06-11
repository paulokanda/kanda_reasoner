"""Build a compact web-AI routing guide for Project Reasoner JSON.

This module creates an additive top-level web_ai_readme section that tells web AI
which canonical collector sections to inspect for common project questions.

It does not replace any index. It is a routing guide over existing and newly
added indexes.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "build_web_ai_readme",
    "build_web_ai_readme_summary",
]


def _safe_len(value: Any) -> int:
    """Return len(value) for common containers, otherwise zero."""
    if isinstance(value, (dict, list, tuple, set)):
        return len(value)
    return 0


def _available(name: str, value: Any) -> dict[str, Any]:
    """Return availability metadata for one section."""
    return {
        "section": name,
        "available": bool(value),
        "item_count": _safe_len(value),
    }


def _route(
    question_type: str,
    sections: list[str],
    answer_rule: str,
) -> dict[str, Any]:
    """Build one question route record."""
    return {
        "question_type": question_type,
        "check_sections_in_order": sections,
        "answer_rule": answer_rule,
    }


def build_web_ai_readme_summary(web_ai_readme: dict[str, Any]) -> dict[str, Any]:
    """Build compact summary for web_ai_readme."""
    routes = web_ai_readme.get("question_routes", [])
    sections = web_ai_readme.get("available_sections", {})

    available_section_count = 0
    if isinstance(sections, dict):
        for value in sections.values():
            if isinstance(value, dict) and value.get("available"):
                available_section_count += 1

    return {
        "question_route_count": len(routes) if isinstance(routes, list) else 0,
        "available_section_count": available_section_count,
        "has_insufficient_evidence_rule": bool(
            web_ai_readme.get("insufficient_evidence_rule", "")
        ),
    }


def build_web_ai_readme(
    *,
    web_ai_symbol_index: dict[str, dict[str, Any]],
    primary_definition_index: dict[str, dict[str, Any]],
    stable_evidence_id_index: dict[str, dict[str, Any]],
    entry_points_detail: list[dict[str, Any]],
    web_ai_file_responsibility_index: dict[str, dict[str, Any]],
    web_ai_test_protection_index: dict[str, dict[str, Any]],
    enabled: bool = True,
) -> dict[str, Any]:
    """Build a compact top-level guide for web AI.

    The guide is intentionally small and deterministic. It gives web AI a
    reading order without duplicating existing indexes.
    """
    if not enabled:
        return {}

    available_sections = {
        "web_ai_symbol_index": _available("web_ai_symbol_index", web_ai_symbol_index),
        "primary_definition_index": _available(
            "primary_definition_index",
            primary_definition_index,
        ),
        "stable_evidence_id_index": _available(
            "stable_evidence_id_index",
            stable_evidence_id_index,
        ),
        "entry_points_detail": _available("entry_points_detail", entry_points_detail),
        "web_ai_file_responsibility_index": _available(
            "web_ai_file_responsibility_index",
            web_ai_file_responsibility_index,
        ),
        "web_ai_test_protection_index": _available(
            "web_ai_test_protection_index",
            web_ai_test_protection_index,
        ),
        "legacy_symbol_index": {
            "section": "symbol_index",
            "available": True,
            "item_count": 0,
            "note": "Use as fallback if web_ai_symbol_index is missing.",
        },
        "legacy_test_links": {
            "section": "test_links",
            "available": True,
            "item_count": 0,
            "note": "Use as fallback if web_ai_test_protection_index is missing.",
        },
    }

    question_routes = [
        _route(
            "symbol_responsibility",
            [
                "web_ai_symbol_index",
                "primary_definition_index",
                "stable_evidence_id_index",
                "files",
            ],
            (
                "Use docstring_first_line from web_ai_symbol_index when present. "
                "If duplicate symbols exist, check primary_definition_index before "
                "choosing the active definition."
            ),
        ),
        _route(
            "symbol_definition_location",
            [
                "primary_definition_index",
                "web_ai_symbol_index",
                "stable_evidence_id_index",
                "symbol_index",
            ],
            (
                "Prefer primary_definition_index for duplicate names. Otherwise use "
                "web_ai_symbol_index file and line_start."
            ),
        ),
        _route(
            "file_or_box_responsibility",
            [
                "web_ai_file_responsibility_index",
                "web_ai_symbol_index",
                "entry_points_detail",
                "files",
            ],
            (
                "Use owner_box and primary_responsibility. Check confidence and "
                "responsibility_source before treating it as implementation truth."
            ),
        ),
        _route(
            "test_protection",
            [
                "web_ai_test_protection_index",
                "test_links",
                "web_ai_symbol_index",
                "files",
            ],
            (
                "Use linked_tests and reason_parts. Existing test_links is fallback; "
                "web_ai_test_protection_index has stronger evidence labels."
            ),
        ),
        _route(
            "entry_point_or_startup_flow",
            [
                "entry_points_detail",
                "project_summary.entry_files",
                "files",
            ],
            (
                "Use entry_points_detail kind, role, confidence, and reason_parts. "
                "Do not assume every script is a primary entry point."
            ),
        ),
        _route(
            "citation_or_cross_chunk_evidence",
            [
                "stable_evidence_id_index",
                "web_ai_symbol_index",
                "primary_definition_index",
                "snippet_index",
            ],
            (
                "Use stable_evidence_id_index for deterministic evidence IDs and "
                "cross-reference paths, symbols, snippets, and primary definitions."
            ),
        ),
        _route(
            "local_ai_answer_flow",
            [
                "web_ai_file_responsibility_index",
                "call_edges",
                "execution_chains",
                "web_ai_symbol_index",
                "files",
            ],
            (
                "Start with file responsibility to identify owning boxes, then use "
                "call_edges and execution_chains for flow details."
            ),
        ),
    ]

    return {
        "purpose": (
            "Routing guide for web AI reading the canonical Step 4 Project "
            "Reasoner JSON export."
        ),
        "canonical_json_role": "web_ai_export",
        "reading_order": [
            "project_summary",
            "web_ai_readme",
            "web_ai_symbol_index",
            "primary_definition_index",
            "web_ai_file_responsibility_index",
            "web_ai_test_protection_index",
            "stable_evidence_id_index",
            "entry_points_detail",
            "files",
        ],
        "available_sections": available_sections,
        "question_routes": question_routes,
        "insufficient_evidence_rule": (
            "Say INSUFFICIENT_EVIDENCE only after checking the relevant route "
            "sections in order. For symbol questions, check web_ai_symbol_index "
            "and primary_definition_index before falling back to symbol_index or "
            "files. For test questions, check web_ai_test_protection_index before "
            "test_links."
        ),
        "source_truth_rule": (
            "Prefer source-derived fields such as docstring_first_line, "
            "module_docstring, symbol_docstring, source spans, stable evidence IDs, "
            "and explicit test import/symbol evidence over path-only heuristics."
        ),
        "do_not_do": [
            "Do not treat low-confidence path heuristics as source truth.",
            "Do not ignore primary_definition_index when duplicate symbols exist.",
            "Do not ignore web_ai_test_protection_index when answering test coverage questions.",
            "Do not say INSUFFICIENT_EVIDENCE before checking the route for the question type.",
        ],
    }
