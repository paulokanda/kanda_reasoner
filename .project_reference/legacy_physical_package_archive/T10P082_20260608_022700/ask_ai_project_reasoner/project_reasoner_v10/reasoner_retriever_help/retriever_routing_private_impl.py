"""Private routing helpers for reasoner_retriever."""
from __future__ import annotations

from ..v10_models import EvidenceItem, RetrievalBundle

__all__ = []


def _resolve_query_kind_impl(retriever, intents: dict[str, bool]) -> str:
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
    if not section_file_evidence:
        return file_evidence
    return (section_file_evidence + file_evidence)[:effective_file_limit]

def _build_canonical_section_bundle_impl(
    retriever,
    section_file_evidence: list[EvidenceItem],
    effective_file_limit: int,
) -> RetrievalBundle:
    canonical_section_files = section_file_evidence[:effective_file_limit]
    return RetrievalBundle(
        file_evidence=retriever._reindex_file_evidence(canonical_section_files),
        symbol_evidence=[],
        snippet_evidence=[],
    )

def _is_section_only_intent_impl(retriever, intents: dict[str, bool]) -> bool:
    return intents["packaging_metadata"] or intents["documentation_intent"]
