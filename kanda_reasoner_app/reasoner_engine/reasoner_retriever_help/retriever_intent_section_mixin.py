# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/retriever_intent_section_mixin.py
"""Intent, profile, and section wrapper methods for ProjectRetriever."""

from __future__ import annotations

from ..project_profile import ProjectProfile
from ..v10_models import EvidenceItem, RetrievalBundle
from .file_context_scoring import get_runtime_anchor_summary
from .profile_support import (
    get_profile_alias_terms,
    get_profile_owner_paths,
    question_has_profile_alias,
    resolve_project_profile,
    text_has_profile_alias,
)
from .retriever_routing_private_impl import (
    _build_canonical_section_bundle_impl,
    _collect_section_file_evidence_impl,
    _is_section_only_intent_impl,
    _merge_section_file_evidence_impl,
    _resolve_effective_limits_impl,
    _resolve_query_kind_impl,
)
from .section_retrieval import (
    retrieve_documentation_intent,
    retrieve_packaging_metadata,
)

__all__ = ["ProjectRetrieverIntentSectionMixin"]


class ProjectRetrieverIntentSectionMixin:
    """Project profile, intent-routing, and section-retrieval adapters."""

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
