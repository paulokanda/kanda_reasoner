# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/retriever_consensus_private_impl.py
"""Private consensus helpers for reasoner_retriever."""
from __future__ import annotations

from typing import Any

from ..v10_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem
from .query_intents import detect_query_intents
from .query_text import norm_text
from .snippet_expansion import _extract_named_callees

__all__ = []


def _expand_bundle_with_named_callees_impl(
    retriever,
    question: str,
    which_calls_query: bool,
    file_evidence: list[EvidenceItem],
    symbol_evidence: list[SymbolEvidenceItem],
    snippet_evidence: list[dict[str, Any]],
    effective_file_limit: int,
    effective_symbol_limit: int,
    effective_snippet_limit: int,
    file_limit: int,
    symbol_limit: int,
    snippet_limit: int,
) -> tuple[list[EvidenceItem], list[SymbolEvidenceItem], list[dict[str, Any]]]:
    """Support expand bundle with named callees impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    question : str
        The question value.
    which_calls_query : bool
        The which calls query value.
    file_evidence : list[EvidenceItem]
        The file evidence value.
    symbol_evidence : list[SymbolEvidenceItem]
        The symbol evidence value.
    snippet_evidence : list[dict[str, Any]]
        The snippet evidence value.
    effective_file_limit : int
        The effective file limit value.
    effective_symbol_limit : int
        The effective symbol limit value.
    effective_snippet_limit : int
        The effective snippet limit value.
    file_limit : int
        The file limit value.
    symbol_limit : int
        The symbol limit value.
    snippet_limit : int
        The snippet limit value.
    
    Returns
    -------
    tuple[list[EvidenceItem], list[SymbolEvidenceItem], list[dict[str, Any]]]
        The tuple of values.
    """
    
    top_snippets = snippet_evidence[:8]
    candidate_callees: set[str] = set()

    for snippet in top_snippets:
        candidate_callees |= _extract_named_callees(
            str(snippet.get("text", "") or snippet.get("content", ""))
        )

    candidate_callees = {
        name
        for name in candidate_callees
        if any(
            name == symbol.split(".")[-1] or name == symbol
            for symbol in retriever.idx.symbol_details.keys()
        )
    }

    if not candidate_callees or which_calls_query:
        return file_evidence, symbol_evidence, snippet_evidence

    expanded_question = question + " " + " ".join(sorted(candidate_callees))
    expanded_symbol_evidence = retriever._retrieve_symbols(
        expanded_question,
        max(effective_symbol_limit, symbol_limit + 4),
    )
    expanded_snippet_evidence = retriever._retrieve_snippets(
        expanded_question,
        file_evidence,
        expanded_symbol_evidence,
        max(effective_snippet_limit, snippet_limit + 4),
    )

    matched_snippets: list[dict[str, Any]] = []
    other_snippets: list[dict[str, Any]] = []

    for snippet in expanded_snippet_evidence:
        symbol_name = str(
            snippet.get("symbol", "") or snippet.get("anchor", "") or ""
        )
        short_symbol = symbol_name.split(".")[-1]

        if short_symbol in candidate_callees or symbol_name in candidate_callees:
            matched_snippets.append(snippet)
        else:
            other_snippets.append(snippet)

    merged = retriever.merge_with_previous(
        RetrievalBundle(
            file_evidence=file_evidence,
            symbol_evidence=expanded_symbol_evidence,
            snippet_evidence=matched_snippets + other_snippets,
        ),
        RetrievalBundle(
            file_evidence=file_evidence,
            symbol_evidence=symbol_evidence,
            snippet_evidence=snippet_evidence,
        ),
        max_files=max(effective_file_limit, file_limit),
        max_symbols=max(effective_symbol_limit, symbol_limit + 4),
        max_snippets=max(effective_snippet_limit, snippet_limit + 4),
    )

    return merged.file_evidence, merged.symbol_evidence, merged.snippet_evidence

def _rerank_file_evidence_with_consensus_impl(
    retriever,
    question: str,
    file_evidence: list[EvidenceItem],
    symbol_evidence: list[SymbolEvidenceItem],
    snippet_evidence: list[dict[str, Any]],
    *,
    limit: int,
) -> list[EvidenceItem]:
    """Support rerank file evidence with consensus impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    question : str
        The question value.
    file_evidence : list[EvidenceItem]
        The file evidence value.
    symbol_evidence : list[SymbolEvidenceItem]
        The symbol evidence value.
    snippet_evidence : list[dict[str, Any]]
        The snippet evidence value.
    limit : int
        The limit value.
    
    Returns
    -------
    list[EvidenceItem]
        The list of values.
    """
    
    if not file_evidence:
        return []

    q = norm_text(question)
    intents = detect_query_intents(q)

    symbol_support: dict[str, int] = {}
    snippet_support: dict[str, int] = {}

    for rank, item in enumerate(symbol_evidence[:12], start=1):
        path = retriever._normalize_evidence_path(getattr(item, "path", ""))
        if not path:
            continue
        symbol_support[path] = symbol_support.get(path, 0) + max(
            10,
            54 - ((rank - 1) * 4),
        )

    for rank, item in enumerate(snippet_evidence[:12], start=1):
        path = retriever._normalize_evidence_path(item.get("path", ""))
        if not path:
            continue
        snippet_support[path] = snippet_support.get(path, 0) + max(
            8,
            48 - ((rank - 1) * 4),
        )

    corroborated_paths = set(symbol_support) | set(snippet_support)
    if len(corroborated_paths) < 2:
        return retriever._reindex_file_evidence(file_evidence[:limit])

    reranked: list[tuple[int, int, EvidenceItem]] = []

    for original_rank, item in enumerate(file_evidence, start=1):
        path = retriever._normalize_evidence_path(item.path)
        adjusted_score = int(item.score)

        symbol_bonus = symbol_support.get(path, 0)
        snippet_bonus = snippet_support.get(path, 0)

        adjusted_score += symbol_bonus
        adjusted_score += snippet_bonus

        if symbol_bonus and snippet_bonus:
            adjusted_score += 36

        if original_rank <= 4 and symbol_bonus and snippet_bonus:
            adjusted_score += 20

        if (
            not intents["packaging_metadata"]
            and not intents["documentation_intent"]
            and original_rank >= 5
            and not symbol_bonus
            and not snippet_bonus
        ):
            adjusted_score -= 80

        reranked.append(
            (
                adjusted_score,
                original_rank,
                EvidenceItem(
                    evidence_id=item.evidence_id,
                    score=adjusted_score,
                    path=item.path,
                    module_name=item.module_name,
                    reason=item.reason,
                    detail=item.detail,
                ),
            )
        )

    reranked.sort(key=lambda entry: (-entry[0], entry[1], entry[2].path))
    return retriever._reindex_file_evidence([entry[2] for entry in reranked[:limit]])
