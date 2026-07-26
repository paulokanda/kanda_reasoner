# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/retriever_snippet_evidence_mixin.py
"""Snippet, path, and evidence-builder methods for ProjectRetriever."""

from __future__ import annotations

from typing import Any

from ..v10_models import EvidenceItem, SymbolEvidenceItem
from .file_context_scoring import (
    collect_file_context_blobs,
    score_advanced_file_context,
    score_runtime_signal_matches,
)
from .file_retrieval import build_compact_file_evidence
from .snippet_retrieval import (
    build_runtime_anchor_snippets,
    extract_runtime_anchors_from_detail,
    find_anchor_line_in_file,
    read_snippet,
    resolve_existing_project_file_path,
    retrieve_snippets,
    score_file_snippet_candidate,
    score_runtime_anchor_for_question,
    score_symbol_snippet_candidate,
    snippet_radius_for_symbol,
)
from .symbol_retrieval import build_symbol_evidence

__all__ = ["ProjectRetrieverSnippetEvidenceMixin"]


class ProjectRetrieverSnippetEvidenceMixin:
    """Snippet retrieval, path resolution, and compact evidence adapters."""

    def _score_runtime_anchor_for_question(
        self,
        question: str,
        anchor: str,
    ) -> int:
        """Support score runtime anchor for question behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        anchor : str
            The anchor value.
        
        Returns
        -------
        int
            The integer result.
        """
        
        return score_runtime_anchor_for_question(self, question, anchor)

    def _find_anchor_line_in_file(self, abs_path: str, anchor: str) -> int | None:
        """Support find anchor line in file behavior.
        
        Parameters
        ----------
        abs_path : str
            The abs path value.
        anchor : str
            The anchor value.
        
        Returns
        -------
        int | None
            The integer result.
        """
        
        return find_anchor_line_in_file(self, abs_path, anchor)

    def _resolve_existing_project_file_path(
        self,
        logical_path: str,
    ) -> tuple[str, str] | tuple[None, None]:
        """Support resolve existing project file path behavior.
        
        Parameters
        ----------
        logical_path : str
            The logical path value.
        
        Returns
        -------
        tuple[str, str] | tuple[None, None]
            The tuple of values.
        """
        
        return resolve_existing_project_file_path(self, logical_path)

    def _build_runtime_anchor_snippets(
        self,
        question: str,
        file_evidence: list[EvidenceItem],
        limit: int,
    ) -> list[dict[str, Any]]:
        """Support build runtime anchor snippets behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        file_evidence : list[EvidenceItem]
            The file evidence value.
        limit : int
            The limit value.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        return build_runtime_anchor_snippets(self, question, file_evidence, limit)

    def _extract_runtime_anchors_from_detail(self, detail_text: str) -> list[str]:
        """Support extract runtime anchors from detail behavior.
        
        Parameters
        ----------
        detail_text : str
            The detail text value.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        return extract_runtime_anchors_from_detail(self, detail_text)

    def _retrieve_snippets(
        self,
        question: str,
        file_evidence: list[EvidenceItem],
        symbol_evidence: list[SymbolEvidenceItem],
        limit: int,
    ) -> list[dict[str, Any]]:
        """Support retrieve snippets behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        file_evidence : list[EvidenceItem]
            The file evidence value.
        symbol_evidence : list[SymbolEvidenceItem]
            The symbol evidence value.
        limit : int
            The limit value.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        return retrieve_snippets(
            self,
            question,
            file_evidence,
            symbol_evidence,
            limit,
        )

    def _score_symbol_snippet_candidate(
        self,
        q: str,
        intents: dict[str, bool],
        item: SymbolEvidenceItem,
        file_rank: dict[str, int],
    ) -> int:
        """Support score symbol snippet candidate behavior.
        
        Parameters
        ----------
        q : str
            The q value.
        intents : dict[str, bool]
            The intents value.
        item : SymbolEvidenceItem
            The item value.
        file_rank : dict[str, int]
            The file rank value.
        
        Returns
        -------
        int
            The integer result.
        """
        
        return score_symbol_snippet_candidate(self, q, intents, item, file_rank)

    def _score_file_snippet_candidate(
        self,
        q: str,
        intents: dict[str, bool],
        item: EvidenceItem,
    ) -> int:
        """Support score file snippet candidate behavior.
        
        Parameters
        ----------
        q : str
            The q value.
        intents : dict[str, bool]
            The intents value.
        item : EvidenceItem
            The item value.
        
        Returns
        -------
        int
            The integer result.
        """
        
        return score_file_snippet_candidate(self, q, intents, item)

    def _snippet_radius_for_symbol(
        self,
        q: str,
        intents: dict[str, bool],
        item: SymbolEvidenceItem,
    ) -> int:
        """Support snippet radius for symbol behavior.
        
        Parameters
        ----------
        q : str
            The q value.
        intents : dict[str, bool]
            The intents value.
        item : SymbolEvidenceItem
            The item value.
        
        Returns
        -------
        int
            The integer result.
        """
        
        return snippet_radius_for_symbol(self, q, intents, item)

    def _read_snippet(self, abs_path: str, line: int, radius: int) -> str:
        """Support read snippet behavior.
        
        Parameters
        ----------
        abs_path : str
            The abs path value.
        line : int
            The line value.
        radius : int
            The radius value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return read_snippet(self, abs_path, line, radius)

    def _collect_file_context_blobs(self, path: str) -> dict[str, str]:
        """Support collect file context blobs behavior.
        
        Parameters
        ----------
        path : str
            The file or folder path.
        
        Returns
        -------
        dict[str, str]
            The mapped values.
        """
        
        return collect_file_context_blobs(self.idx, path)

    def _score_advanced_file_context(
        self,
        q: str,
        path: str,
        tokens: list[str],
        reasons: list[str],
    ) -> int:
        """Support score advanced file context behavior.
        
        Parameters
        ----------
        q : str
            The q value.
        path : str
            The file or folder path.
        tokens : list[str]
            The tokens value.
        reasons : list[str]
            The reasons value.
        
        Returns
        -------
        int
            The integer result.
        """
        
        return score_advanced_file_context(self.idx, q, path, tokens, reasons)

    def _score_runtime_signal_matches(
        self,
        q: str,
        reasons: list[str],
    ) -> tuple[int, set[str]]:
        """Support score runtime signal matches behavior.
        
        Parameters
        ----------
        q : str
            The q value.
        reasons : list[str]
            The reasons value.
        
        Returns
        -------
        tuple[int, set[str]]
            The tuple of values.
        """
        
        return score_runtime_signal_matches(self.idx, q, reasons)

    def _build_compact_file_evidence(
        self,
        path: str,
        reasons: list[str],
    ) -> str:
        """Support build compact file evidence behavior.
        
        Parameters
        ----------
        path : str
            The file or folder path.
        reasons : list[str]
            The reasons value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return build_compact_file_evidence(self, path, reasons)

    def _build_symbol_evidence(self, symbol_name: str) -> str:
        """Support build symbol evidence behavior.
        
        Parameters
        ----------
        symbol_name : str
            The symbol name value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return build_symbol_evidence(self, symbol_name)
