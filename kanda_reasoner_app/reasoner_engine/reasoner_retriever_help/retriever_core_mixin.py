# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/retriever_core_mixin.py
"""Core retrieval orchestration methods for ProjectRetriever."""

from __future__ import annotations

from typing import Any

from ..core import get_section_priority
from ..v10_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem
from .bundle_merge import merge_retrieval_bundles
from .file_retrieval import retrieve_files
from .exact_code_anchors import filter_bundle_to_requested_files, strict_evidence_requested
from .live_source_fallback import augment_bundle_with_live_source_fallback
from .query_intents import detect_query_intents
from .query_text import norm_text
from .retriever_consensus_private_impl import (
    _expand_bundle_with_named_callees_impl,
    _rerank_file_evidence_with_consensus_impl,
)
from .symbol_retrieval import retrieve_symbols

__all__ = ["ProjectRetrieverCoreMixin"]


class ProjectRetrieverCoreMixin:
    """High-level retrieval flow and bundle merging adapters."""

    def _expand_bundle_with_named_callees(self, question: str, which_calls_query: bool, file_evidence: list[EvidenceItem], symbol_evidence: list[SymbolEvidenceItem], snippet_evidence: list[dict[str, Any]], effective_file_limit: int, effective_symbol_limit: int, effective_snippet_limit: int, file_limit: int, symbol_limit: int, snippet_limit: int) -> tuple[list[EvidenceItem], list[SymbolEvidenceItem], list[dict[str, Any]]]:
        """Support expand bundle with named callees behavior.
        
        Parameters
        ----------
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
        
        return _expand_bundle_with_named_callees_impl(self, question, which_calls_query, file_evidence, symbol_evidence, snippet_evidence, effective_file_limit, effective_symbol_limit, effective_snippet_limit, file_limit, symbol_limit, snippet_limit)

    def retrieve(
        self,
        question: str,
        *,
        file_limit: int = 10,
        symbol_limit: int = 10,
        snippet_limit: int = 6,
        project_root_override: str = "",
    ) -> RetrievalBundle:
        """Support retrieve behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        file_limit : int, optional
            The optional file limit value.
        symbol_limit : int, optional
            The optional symbol limit value.
        snippet_limit : int, optional
            The optional snippet limit value.
        
        Returns
        -------
        RetrievalBundle
            The retrieval bundle result.
        """
        
        q = norm_text(question)
        intents = detect_query_intents(q)
        which_calls_query = intents["which_calls"]

        query_kind = self._resolve_query_kind(intents)
        section_priority = get_section_priority(query_kind)

        (
            effective_file_limit,
            effective_symbol_limit,
            effective_snippet_limit,
        ) = self._resolve_effective_limits(
            q,
            intents,
            file_limit,
            symbol_limit,
            snippet_limit,
        )

        file_evidence = self._retrieve_files(question, effective_file_limit)
        symbol_evidence = self._retrieve_symbols(question, effective_symbol_limit)
        snippet_evidence = self._retrieve_snippets(
            question,
            file_evidence,
            symbol_evidence,
            effective_snippet_limit,
        )

        (
            file_evidence,
            symbol_evidence,
            snippet_evidence,
        ) = self._expand_bundle_with_named_callees(
            question,
            which_calls_query,
            file_evidence,
            symbol_evidence,
            snippet_evidence,
            effective_file_limit,
            effective_symbol_limit,
            effective_snippet_limit,
            file_limit,
            symbol_limit,
            snippet_limit,
        )

        section_file_evidence = self._collect_section_file_evidence(
            question,
            section_priority,
        )
        file_evidence = self._merge_section_file_evidence(
            section_file_evidence,
            file_evidence,
            effective_file_limit,
        )

        if self._is_section_only_intent(intents):
            return self._build_canonical_section_bundle(
                section_file_evidence,
                effective_file_limit,
            )

        file_evidence = self._rerank_file_evidence_with_consensus(
            question,
            file_evidence,
            symbol_evidence,
            snippet_evidence,
            limit=effective_file_limit,
        )

        bundle = RetrievalBundle(
            file_evidence=file_evidence,
            symbol_evidence=symbol_evidence,
            snippet_evidence=snippet_evidence,
        )
        bundle = augment_bundle_with_live_source_fallback(
            self,
            question,
            bundle,
            max_files=effective_file_limit,
            max_snippets=effective_snippet_limit,
            project_root_override=project_root_override,
        )
        if strict_evidence_requested(question):
            bundle = filter_bundle_to_requested_files(question, bundle)
        return bundle

    def _reindex_file_evidence(
        self,
        file_evidence: list[EvidenceItem],
    ) -> list[EvidenceItem]:
        """Support reindex file evidence behavior.
        
        Parameters
        ----------
        file_evidence : list[EvidenceItem]
            The file evidence value.
        
        Returns
        -------
        list[EvidenceItem]
            The list of values.
        """
        
        reindexed: list[EvidenceItem] = []
        for idx, item in enumerate(file_evidence, start=1):
            reindexed.append(
                EvidenceItem(
                    evidence_id="F" + str(idx).zfill(2),
                    score=item.score,
                    path=item.path,
                    module_name=item.module_name,
                    reason=item.reason,
                    detail=item.detail,
                )
            )
        return reindexed

    def _rerank_file_evidence_with_consensus(self, question: str, file_evidence: list[EvidenceItem], symbol_evidence: list[SymbolEvidenceItem], snippet_evidence: list[dict[str, Any]], *, limit: int) -> list[EvidenceItem]:
        """Support rerank file evidence with consensus behavior.
        
        Parameters
        ----------
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
        
        return _rerank_file_evidence_with_consensus_impl(self, question, file_evidence, symbol_evidence, snippet_evidence, limit=limit)

    def merge_with_previous(
        self,
        current_bundle: RetrievalBundle,
        previous_bundle: RetrievalBundle,
        *,
        max_files: int = 14,
        max_symbols: int = 14,
        max_snippets: int = 10,
    ) -> RetrievalBundle:
        """Support merge with previous behavior.
        
        Parameters
        ----------
        current_bundle : RetrievalBundle
            The current bundle value.
        previous_bundle : RetrievalBundle
            The previous bundle value.
        max_files : int, optional
            The optional max files value.
        max_symbols : int, optional
            The optional max symbols value.
        max_snippets : int, optional
            The optional max snippets value.
        
        Returns
        -------
        RetrievalBundle
            The retrieval bundle result.
        """
        
        return merge_retrieval_bundles(
            current_bundle=current_bundle,
            previous_bundle=previous_bundle,
            max_files=max_files,
            max_symbols=max_symbols,
            max_snippets=max_snippets,
        )

    def _retrieve_files(self, question: str, limit: int) -> list[EvidenceItem]:
        """Support retrieve files behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        limit : int
            The limit value.
        
        Returns
        -------
        list[EvidenceItem]
            The list of values.
        """
        
        return retrieve_files(self, question, limit)

    def _retrieve_symbols(
        self,
        question: str,
        limit: int,
    ) -> list[SymbolEvidenceItem]:
        """Support retrieve symbols behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        limit : int
            The limit value.
        
        Returns
        -------
        list[SymbolEvidenceItem]
            The list of values.
        """
        
        return retrieve_symbols(self, question, limit)
