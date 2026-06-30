# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/retriever_routing_private_impl.py
"""Private routing helpers for reasoner_retriever."""
from __future__ import annotations

from ..v10_models import EvidenceItem, RetrievalBundle

__all__ = []


def _resolve_query_kind_impl(retriever, intents: dict[str, bool]) -> str:
    """Support resolve query kind impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    intents : dict[str, bool]
        The intents value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if intents["packaging_metadata"]:
        return "packaging_metadata"
    if intents["documentation_intent"]:
        return "documentation_intent"
    if intents["runtime_heavy"]:
        return "runtime_heavy"
    if intents["startup"]:
        return "startup"
    if intents["explain_chain"]:
        return "explain_chain"
    if intents["explanatory"]:
        return "explanatory"
    return "default"

def _resolve_effective_limits_impl(
    retriever,
    q: str,
    intents: dict[str, bool],
    file_limit: int,
    symbol_limit: int,
    snippet_limit: int,
) -> tuple[int, int, int]:
    """Support resolve effective limits impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    q : str
        The q value.
    intents : dict[str, bool]
        The intents value.
    file_limit : int
        The file limit value.
    symbol_limit : int
        The symbol limit value.
    snippet_limit : int
        The snippet limit value.
    
    Returns
    -------
    tuple[int, int, int]
        The tuple of values.
    """
    
    effective_file_limit = file_limit
    effective_symbol_limit = symbol_limit
    effective_snippet_limit = snippet_limit

    asks_topomap_explanation = (
        retriever._question_has_profile_alias(q, "topomap_explanation")
        or intents["topomap_explanation"]
    )

    if asks_topomap_explanation:
        effective_file_limit = max(file_limit, 12)
        effective_symbol_limit = max(symbol_limit, 12)
        effective_snippet_limit = max(snippet_limit, 10)

    if (
        intents["explanatory"]
        or intents["code_localized_explanation"]
        or intents["explain_chain"]
    ):
        effective_file_limit = max(effective_file_limit, 12)
        effective_symbol_limit = max(effective_symbol_limit, 12)
        effective_snippet_limit = max(effective_snippet_limit, 8)

    if intents["runtime_heavy"] and (
        intents["explanatory"]
        or intents["code_localized_explanation"]
        or intents["explain_chain"]
    ):
        effective_file_limit = max(effective_file_limit, 14)
        effective_symbol_limit = max(effective_symbol_limit, 14)
        effective_snippet_limit = max(effective_snippet_limit, 10)

    return (
        effective_file_limit,
        effective_symbol_limit,
        effective_snippet_limit,
    )

def _collect_section_file_evidence_impl(
    retriever,
    question: str,
    section_priority: list[str],
) -> list[EvidenceItem]:
    """Support collect section file evidence impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    question : str
        The question value.
    section_priority : list[str]
        The section priority value.
    
    Returns
    -------
    list[EvidenceItem]
        The list of values.
    """
    
    section_file_evidence: list[EvidenceItem] = []

    for section_name in section_priority:
        if section_name == "packaging_metadata":
            section_file_evidence.extend(
                retriever._retrieve_packaging_metadata(question)
            )
        elif section_name == "documentation_intent":
            section_file_evidence.extend(
                retriever._retrieve_documentation_intent(question)
            )

    return section_file_evidence

def _merge_section_file_evidence_impl(
    retriever,
    section_file_evidence: list[EvidenceItem],
    file_evidence: list[EvidenceItem],
    effective_file_limit: int,
) -> list[EvidenceItem]:
    """Support merge section file evidence impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    section_file_evidence : list[EvidenceItem]
        The section file evidence value.
    file_evidence : list[EvidenceItem]
        The file evidence value.
    effective_file_limit : int
        The effective file limit value.
    
    Returns
    -------
    list[EvidenceItem]
        The list of values.
    """
    
    if not section_file_evidence:
        return file_evidence
    return (section_file_evidence + file_evidence)[:effective_file_limit]

def _build_canonical_section_bundle_impl(
    retriever,
    section_file_evidence: list[EvidenceItem],
    effective_file_limit: int,
) -> RetrievalBundle:
    """Support build canonical section bundle impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    section_file_evidence : list[EvidenceItem]
        The section file evidence value.
    effective_file_limit : int
        The effective file limit value.
    
    Returns
    -------
    RetrievalBundle
        The retrieval bundle result.
    """
    
    canonical_section_files = section_file_evidence[:effective_file_limit]
    return RetrievalBundle(
        file_evidence=retriever._reindex_file_evidence(canonical_section_files),
        symbol_evidence=[],
        snippet_evidence=[],
    )

def _is_section_only_intent_impl(retriever, intents: dict[str, bool]) -> bool:
    """Support is section only intent impl behavior.
    
    Parameters
    ----------
    retriever : object
        The retriever value.
    intents : dict[str, bool]
        The intents value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return intents["packaging_metadata"] or intents["documentation_intent"]
