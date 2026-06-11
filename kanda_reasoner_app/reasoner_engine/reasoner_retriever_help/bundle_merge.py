"""Support V10 project reasoning and evidence handling."""

# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help
# PURPOSE       : Merge retrieval bundles and reindex evidence identifiers deterministically.
# EXPORTS       : merge_retrieval_bundles
# DEPENDS ON    : query_text.py
# REFACTOR DATE : 2026-04-10
# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
from __future__ import annotations

from typing import Any

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import is_allowed_project_path
from kanda_reasoner_app.reasoner_engine.v10_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem

__all__ = ["merge_retrieval_bundles"]


def merge_retrieval_bundles(
    current_bundle: RetrievalBundle,
    previous_bundle: RetrievalBundle,
    *,
    max_files: int = 14,
    max_symbols: int = 14,
    max_snippets: int = 10,
) -> RetrievalBundle:
    file_map: dict[str, EvidenceItem] = {}
    for item in current_bundle.file_evidence + previous_bundle.file_evidence:
        if not is_allowed_project_path(item.path):
            continue
        key = item.path
        old = file_map.get(key)
        if old is None or item.score > old.score:
            file_map[key] = item

    symbol_map: dict[str, SymbolEvidenceItem] = {}
    for item in current_bundle.symbol_evidence + previous_bundle.symbol_evidence:
        if not is_allowed_project_path(item.path):
            continue
        key = item.symbol_name + "|" + item.path
        old = symbol_map.get(key)
        if old is None or item.score > old.score:
            symbol_map[key] = item

    snippet_map: dict[tuple[str, int, str], dict[str, Any]] = {}
    for item in current_bundle.snippet_evidence + previous_bundle.snippet_evidence:
        path = str(item.get("path", ""))
        if not is_allowed_project_path(path):
            continue
        key = (path, int(item.get("line", 0)), str(item.get("anchor", "")))
        snippet_map[key] = item

    merged_files = sorted(file_map.values(), key=lambda x: (-x.score, x.path))[:max_files]
    merged_symbols = sorted(
        symbol_map.values(),
        key=lambda x: (-x.score, x.symbol_name, x.path),
    )[:max_symbols]
    merged_snippets = list(snippet_map.values())[:max_snippets]

    for idx, item in enumerate(merged_files, start=1):
        item.evidence_id = "F" + str(idx).zfill(2)

    for idx, item in enumerate(merged_symbols, start=1):
        item.evidence_id = "S" + str(idx).zfill(2)

    for idx, item in enumerate(merged_snippets, start=1):
        item["snippet_id"] = "SN" + str(idx).zfill(2)

    return RetrievalBundle(
        file_evidence=merged_files,
        symbol_evidence=merged_symbols,
        snippet_evidence=merged_snippets,
    )






