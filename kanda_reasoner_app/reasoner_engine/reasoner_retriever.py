# developer_tools/kanda_reasoner_app/project_reasoner_v10/reasoner_retriever.py
"""Project retriever public entry point.

This module is the public ProjectRetriever shell. Helper logic lives under
reasoner_retriever_help. Read the helper manifest before editing shared logic.
"""

from __future__ import annotations

from typing import Any

from .core import get_section_priority
from .index_loader import JsonProjectIndex
from .v10_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem
from .project_profile import ProjectProfile
from .reasoner_retriever_help.bundle_merge import merge_retrieval_bundles
from .reasoner_retriever_help.file_context_scoring import (
    collect_file_context_blobs,
    get_runtime_anchor_summary,
    score_advanced_file_context,
    score_runtime_signal_matches,
)
from .reasoner_retriever_help.file_retrieval import (
    build_compact_file_evidence,
    retrieve_files,
)
from .reasoner_retriever_help.live_source_fallback import (
    augment_bundle_with_live_source_fallback,
)
from .reasoner_retriever_help.profile_support import (
    get_profile_alias_terms,
    get_profile_owner_paths,
    question_has_profile_alias,
    resolve_project_profile,
    text_has_profile_alias,
)
from .reasoner_retriever_help.query_intents import (
    detect_query_intents,
    is_code_localized_explanation_question,
    is_documentation_intent_question,
    is_explain_chain_question,
    is_explanatory_question,
    is_explicit_call_chain_question,
    is_main_window_show_responsibility_question,
    is_packaging_metadata_question,
    is_qtimer_showmaximized_question,
    is_runtime_heavy_question,
    is_startup_question,
    is_topomap_explanation_question,
    is_topomap_implementation_question,
    is_where_is_called_question,
    is_where_is_question,
    is_which_method_calls_question,
)
from .reasoner_retriever_help.query_text import (
    file_name_from_path,
    is_allowed_project_path,
    is_auxiliary_ui_path,
    last_part_match_in_query,
    norm_text,
    safe_read_text,
    tokenize_query,
)
from .reasoner_retriever_help.section_retrieval import (
    retrieve_documentation_intent,
    retrieve_packaging_metadata,
)
from .reasoner_retriever_help.snippet_expansion import _extract_named_callees
from .reasoner_retriever_help.snippet_retrieval import (
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
from .reasoner_retriever_help.symbol_retrieval import (
    build_symbol_evidence,
    retrieve_symbols,
)
from .reasoner_retriever_help.retriever_routing_private_impl import _build_canonical_section_bundle_impl, _collect_section_file_evidence_impl, _is_section_only_intent_impl, _merge_section_file_evidence_impl, _resolve_effective_limits_impl, _resolve_query_kind_impl
from .reasoner_retriever_help.retriever_consensus_private_impl import _expand_bundle_with_named_callees_impl, _rerank_file_evidence_with_consensus_impl

__all__ = [
    "ProjectRetriever",
    "norm_text",
    "tokenize_query",
    "safe_read_text",
    "file_name_from_path",
    "is_allowed_project_path",
    "is_auxiliary_ui_path",
    "is_startup_question",
    "is_explicit_call_chain_question",
    "is_main_window_show_responsibility_question",
    "is_qtimer_showmaximized_question",
    "is_where_is_called_question",
    "is_where_is_question",
    "is_explain_chain_question",
    "is_code_localized_explanation_question",
    "is_topomap_explanation_question",
    "is_topomap_implementation_question",
    "is_runtime_heavy_question",
    "is_packaging_metadata_question",
    "is_documentation_intent_question",
    "detect_query_intents",
    "last_part_match_in_query",
]


class ProjectRetriever:
    """Represent project retriever."""
    
    def __init__(
        self,
        project_index: JsonProjectIndex,
        project_profile: ProjectProfile | None = None,
    ) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        project_index : JsonProjectIndex
            The project index value.
        project_profile : ProjectProfile | None, optional
            The optional project profile value.
        """
        
        self.idx = project_index
        self.project_profile = self._resolve_project_profile(project_profile)
        self.project_profile_name = self.project_profile.name
        self.project_profile_domain_scope = self.project_profile.domain_scope

    def _resolve_project_profile(
        self,
        project_profile: ProjectProfile | None,
    ) -> ProjectProfile:
        """Support resolve project profile behavior.
        
        Parameters
        ----------
        project_profile : ProjectProfile | None
            The project profile value.
        
        Returns
        -------
        ProjectProfile
            The project profile result.
        """
        
        return resolve_project_profile(self.idx, project_profile)

    def get_active_project_profile(self) -> ProjectProfile:
        """Return the active project profile."""
        return self.project_profile

    def _resolve_query_kind(self, intents: dict[str, bool]) -> str:
        """Support resolve query kind behavior.
        
        Parameters
        ----------
        intents : dict[str, bool]
            The intents value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return _resolve_query_kind_impl(self, intents)

    def _resolve_effective_limits(self, q: str, intents: dict[str, bool], file_limit: int, symbol_limit: int, snippet_limit: int) -> tuple[int, int, int]:
        """Support resolve effective limits behavior.
        
        Parameters
        ----------
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
        
        return _resolve_effective_limits_impl(self, q, intents, file_limit, symbol_limit, snippet_limit)

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

    def _collect_section_file_evidence(self, question: str, section_priority: list[str]) -> list[EvidenceItem]:
        """Support collect section file evidence behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        section_priority : list[str]
            The section priority value.
        
        Returns
        -------
        list[EvidenceItem]
            The list of values.
        """
        
        return _collect_section_file_evidence_impl(self, question, section_priority)

    def _merge_section_file_evidence(self, section_file_evidence: list[EvidenceItem], file_evidence: list[EvidenceItem], effective_file_limit: int) -> list[EvidenceItem]:
        """Support merge section file evidence behavior.
        
        Parameters
        ----------
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
        
        return _merge_section_file_evidence_impl(self, section_file_evidence, file_evidence, effective_file_limit)

    def _build_canonical_section_bundle(self, section_file_evidence: list[EvidenceItem], effective_file_limit: int) -> RetrievalBundle:
        """Support build canonical section bundle behavior.
        
        Parameters
        ----------
        section_file_evidence : list[EvidenceItem]
            The section file evidence value.
        effective_file_limit : int
            The effective file limit value.
        
        Returns
        -------
        RetrievalBundle
            The retrieval bundle result.
        """
        
        return _build_canonical_section_bundle_impl(self, section_file_evidence, effective_file_limit)

    def _is_section_only_intent(self, intents: dict[str, bool]) -> bool:
        """Support is section only intent behavior.
        
        Parameters
        ----------
        intents : dict[str, bool]
            The intents value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return _is_section_only_intent_impl(self, intents)

    def retrieve(
        self,
        question: str,
        *,
        file_limit: int = 10,
        symbol_limit: int = 10,
        snippet_limit: int = 6,
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
        return augment_bundle_with_live_source_fallback(
            self,
            question,
            bundle,
            max_files=effective_file_limit,
            max_snippets=effective_snippet_limit,
        )

    def _normalize_evidence_path(self, path: str) -> str:
        """Support normalize evidence path behavior.
        
        Parameters
        ----------
        path : str
            The file or folder path.
        
        Returns
        -------
        str
            The string result.
        """
        
        return str(path or "").replace("\\", "/").strip()

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

    def _retrieve_packaging_metadata(
        self,
        question: str,
    ) -> list[EvidenceItem]:
        """Support retrieve packaging metadata behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        
        Returns
        -------
        list[EvidenceItem]
            The list of values.
        """
        
        return retrieve_packaging_metadata(self.idx, question)

    def _retrieve_documentation_intent(
        self,
        question: str,
    ) -> list[EvidenceItem]:
        """Support retrieve documentation intent behavior.
        
        Parameters
        ----------
        question : str
            The question value.
        
        Returns
        -------
        list[EvidenceItem]
            The list of values.
        """
        
        return retrieve_documentation_intent(self.idx, question)

    def _profile_alias_terms(self, alias_key: str) -> tuple[str, ...]:
        """Support profile alias terms behavior.
        
        Parameters
        ----------
        alias_key : str
            The alias key value.
        
        Returns
        -------
        tuple[str, ...]
            The tuple of values.
        """
        
        return get_profile_alias_terms(self.project_profile, alias_key)

    def _question_has_profile_alias(self, q: str, alias_key: str) -> bool:
        """Support question has profile alias behavior.
        
        Parameters
        ----------
        q : str
            The q value.
        alias_key : str
            The alias key value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return question_has_profile_alias(self.project_profile, q, alias_key)

    def _text_has_profile_alias(self, text: str, alias_key: str) -> bool:
        """Support text has profile alias behavior.
        
        Parameters
        ----------
        text : str
            The text value.
        alias_key : str
            The alias key value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return text_has_profile_alias(self.project_profile, text, alias_key)

    def _profile_owner_paths(self, alias_key: str) -> tuple[str, ...]:
        """Support profile owner paths behavior.
        
        Parameters
        ----------
        alias_key : str
            The alias key value.
        
        Returns
        -------
        tuple[str, ...]
            The tuple of values.
        """
        
        return get_profile_owner_paths(self.project_profile, alias_key)

    def _get_runtime_anchor_summary(
        self,
        path: str,
        limit: int = 12,
    ) -> tuple[list[str], list[str]]:
        """Support get runtime anchor summary behavior.
        
        Parameters
        ----------
        path : str
            The file or folder path.
        limit : int, optional
            The optional limit value.
        
        Returns
        -------
        tuple[list[str], list[str]]
            The tuple of values.
        """
        
        return get_runtime_anchor_summary(self.idx, path, limit)

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

