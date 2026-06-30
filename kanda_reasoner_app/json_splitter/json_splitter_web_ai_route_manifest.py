# project-path: kanda_reasoner_app/json_splitter/json_splitter_web_ai_route_manifest.py
"""Build a web-AI route manifest for split Project Reasoner JSON.

The route manifest is a compact navigation layer over existing split parts. It
does not change chunk payloads, the split manifest, or reassembly logic.

It helps web AI decide which uploaded chunk to inspect for symbol lookup,
primary definitions, stable evidence IDs, file responsibility, test protection,
entry/startup flow, UI flow, file corpus, and large graph sections.
"""

from __future__ import annotations

import os
from typing import Any

__all__ = [
    "WEB_AI_ROUTE_MANIFEST_SCHEMA",
    "QUESTION_ROUTE_DEFINITIONS",
    "build_web_ai_route_manifest",
    "web_ai_route_manifest_filename",
]

WEB_AI_ROUTE_MANIFEST_SCHEMA = "project-reasoner-web-ai-route-manifest/v1"

QUESTION_ROUTE_DEFINITIONS: dict[str, list[str]] = {
    "web_ai_readme": [
        "web_ai_readme",
        "web_ai_readme_summary",
    ],
    "symbol_lookup": [
        "web_ai_symbol_index",
        "web_ai_symbol_summary",
        "primary_definition_index",
        "primary_definition_summary",
        "stable_evidence_id_index",
        "stable_evidence_id_summary",
        "symbol_index",
        "edit_ready_symbol_index",
        "snippet_index",
    ],
    "symbol_definition_location": [
        "primary_definition_index",
        "web_ai_symbol_index",
        "stable_evidence_id_index",
        "symbol_index",
        "edit_ready_symbol_index",
    ],
    "file_or_box_responsibility": [
        "web_ai_file_responsibility_index",
        "web_ai_file_responsibility_summary",
        "web_ai_symbol_index",
        "entry_points_detail",
        "files",
    ],
    "test_protection": [
        "web_ai_test_protection_index",
        "web_ai_test_protection_summary",
        "test_links",
        "web_ai_symbol_index",
        "files",
    ],
    "entry_point_or_startup_flow": [
        "entry_points_detail",
        "entry_points_detail_summary",
        "project_summary",
        "files",
    ],
    "citation_or_cross_chunk_evidence": [
        "stable_evidence_id_index",
        "stable_evidence_id_summary",
        "web_ai_symbol_index",
        "primary_definition_index",
        "snippet_index",
    ],
    "local_ai_answer_flow": [
        "web_ai_file_responsibility_index",
        "call_edges",
        "execution_chains",
        "web_ai_symbol_index",
        "files",
    ],
    "ui_flow": [
        "widget_registry",
        "widget_summary",
        "widget_text_index",
        "widget_layout_index",
        "widget_ui_action_bridge",
        "ui_action_index",
        "qt_signal_map",
    ],
    "file_corpus": [
        "files",
        "source_file_index",
        "edit_ready_symbol_index",
        "snippet_index",
    ],
    "large_graph_sections": [
        "call_edges",
        "attribute_state_map",
        "execution_chains",
        "responsibility_overlap_index",
        "object_ownership",
    ],
}


def _safe_text(value: Any) -> str:
    """Return safe stripped text."""
    return str(value or "").strip()


def _safe_list(value: Any) -> list[Any]:
    """Return a list value or an empty list."""
    return value if isinstance(value, list) else []


def _safe_int(value: Any) -> int:
    """Return int(value), or zero if conversion fails."""
    try:
        return int(value)
    except Exception:
        return 0


def _top_level_sections_for_part(part: dict[str, Any]) -> set[str]:
    """Infer top-level JSON sections represented by one split part."""
    path_parts = _safe_list(part.get("path_parts", []))
    entry_keys = _safe_list(part.get("entry_keys", []))

    sections: set[str] = set()

    if path_parts:
        first = _safe_text(path_parts[0])
        if first:
            sections.add(first)
        return sections

    for key in entry_keys:
        text = _safe_text(key)
        if text:
            sections.add(text)

    return sections


def _route_entry_for_part(
    part: dict[str, Any],
    matched_sections: list[str],
) -> dict[str, Any]:
    """Build a compact route entry for one part."""
    return {
        "index": _safe_int(part.get("index", 0)),
        "filename": _safe_text(part.get("filename", "")),
        "path_parts": _safe_list(part.get("path_parts", [])),
        "path": ".".join(
            _safe_text(item) for item in _safe_list(part.get("path_parts", []))
        ) or "<root>",
        "matched_sections": matched_sections,
        "entry_count": _safe_int(part.get("entries", 0)),
        "size_bytes": _safe_int(part.get("size_bytes", 0)),
        "token_estimate": _safe_int(part.get("token_estimate", 0)),
    }


def _dedupe_route_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate and sort route entries by part index and filename."""
    by_key: dict[tuple[int, str], dict[str, Any]] = {}
    for item in entries:
        key = (_safe_int(item.get("index", 0)), _safe_text(item.get("filename", "")))
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = item
            continue

        merged = sorted(
            set(_safe_list(existing.get("matched_sections", [])))
            | set(_safe_list(item.get("matched_sections", [])))
        )
        existing["matched_sections"] = merged

    return [
        by_key[key]
        for key in sorted(by_key, key=lambda item: (item[0], item[1]))
    ]


def _section_index(parts: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Build top-level section to part route records."""
    output: dict[str, list[dict[str, Any]]] = {}

    for part in parts:
        sections = sorted(_top_level_sections_for_part(part))
        for section in sections:
            output.setdefault(section, []).append(
                _route_entry_for_part(part, [section])
            )

    return {
        section: _dedupe_route_entries(rows)
        for section, rows in sorted(output.items())
    }


def _question_routes(
    section_index: dict[str, list[dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    """Build question-type routes from section index."""
    routes: dict[str, dict[str, Any]] = {}

    for question_type, sections in QUESTION_ROUTE_DEFINITIONS.items():
        entries: list[dict[str, Any]] = []
        matched_sections: list[str] = []

        for section in sections:
            section_entries = section_index.get(section, [])
            if section_entries:
                matched_sections.append(section)
            for item in section_entries:
                cloned = dict(item)
                cloned["matched_sections"] = [section]
                entries.append(cloned)

        route_entries = _dedupe_route_entries(entries)
        routes[question_type] = {
            "question_type": question_type,
            "preferred_sections": sections,
            "matched_sections": matched_sections,
            "chunks": route_entries,
            "chunk_count": len(route_entries),
        }

    return routes


def web_ai_route_manifest_filename(source_filename: str) -> str:
    """Return route manifest filename for a source JSON filename."""
    base_name = os.path.splitext(os.path.basename(source_filename))[0]
    return base_name + "__web_ai_route_manifest.json"


def build_web_ai_route_manifest(split_manifest: dict[str, Any]) -> dict[str, Any]:
    """Build a web-AI route manifest from an existing split manifest."""
    parts = _safe_list(split_manifest.get("parts", []))
    section_index = _section_index(parts)
    routes = _question_routes(section_index)

    routed_chunk_names: set[str] = set()
    for route in routes.values():
        for item in route.get("chunks", []):
            filename = _safe_text(item.get("filename", ""))
            if filename:
                routed_chunk_names.add(filename)

    return {
        "schema": WEB_AI_ROUTE_MANIFEST_SCHEMA,
        "source_file": _safe_text(split_manifest.get("source_file", "")),
        "source_sha256": _safe_text(split_manifest.get("source_sha256", "")),
        "splitter_version": _safe_text(split_manifest.get("splitter_version", "")),
        "part_format": _safe_text(split_manifest.get("part_format", "")),
        "part_count": _safe_int(split_manifest.get("part_count", len(parts))),
        "section_index": section_index,
        "question_routes": routes,
        "route_summary": {
            "section_count": len(section_index),
            "question_route_count": len(routes),
            "routed_chunk_count": len(routed_chunk_names),
            "unrouted_chunk_count": max(0, len(parts) - len(routed_chunk_names)),
        },
        "usage": {
            "symbol_questions": "Start with question_routes.symbol_lookup.",
            "definition_questions": "Start with question_routes.symbol_definition_location.",
            "file_or_box_questions": "Start with question_routes.file_or_box_responsibility.",
            "test_questions": "Start with question_routes.test_protection.",
            "entry_flow_questions": "Start with question_routes.entry_point_or_startup_flow.",
            "insufficient_evidence_rule": (
                "Do not say INSUFFICIENT_EVIDENCE until checking the route for "
                "the relevant question type."
            ),
        },
    }
