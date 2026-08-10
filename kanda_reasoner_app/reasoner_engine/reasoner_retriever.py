# developer_tools/kanda_reasoner_app/project_reasoner_v10/reasoner_retriever.py
"""Project retriever public entry point.

This module is the public ProjectRetriever shell. Helper logic lives under
reasoner_retriever_help. Read the helper manifest before editing shared logic.
"""

from __future__ import annotations

from .index_loader import JsonProjectIndex
from .project_profile import ProjectProfile
from .reasoner_retriever_help.query_intents import (
    detect_query_intents,
    is_code_localized_explanation_question,
    is_documentation_intent_question,
    is_explain_chain_question,
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
from .reasoner_retriever_help.retriever_core_mixin import ProjectRetrieverCoreMixin
from .reasoner_retriever_help.retriever_intent_section_mixin import (
    ProjectRetrieverIntentSectionMixin,
)
from .reasoner_retriever_help.retriever_snippet_evidence_mixin import (
    ProjectRetrieverSnippetEvidenceMixin,
)

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


class ProjectRetriever(
    ProjectRetrieverCoreMixin,
    ProjectRetrieverIntentSectionMixin,
    ProjectRetrieverSnippetEvidenceMixin,
):
    """Retrieve project evidence for Project Q&A."""

    def __init__(
        self,
        project_index: JsonProjectIndex,
        project_profile: ProjectProfile | None = None,
    ) -> None:
        """Initialize the retriever with an index and resolved project profile."""

        self.idx = project_index
        self.project_profile = self._resolve_project_profile(project_profile)
        self.project_profile_name = self.project_profile.name
        self.project_profile_domain_scope = self.project_profile.domain_scope
