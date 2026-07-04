# developer_tools/kanda_reasoner_app/project_reasoner_v10/reasoner_retriever.py
"""Project retriever public entry point.

This module is the public ProjectRetriever shell. Helper logic lives under
reasoner_retriever_help. Read the helper manifest before editing shared logic.
"""

from __future__ import annotations

from .core import get_section_priority
from .index_loader import JsonProjectIndex
from .project_profile import ProjectProfile
from .v10_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem
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
from .reasoner_retriever_help.retriever_consensus_private_impl import (
    _expand_bundle_with_named_callees_impl,
    _rerank_file_evidence_with_consensus_impl,
)
from .reasoner_retriever_help.retriever_core_mixin import ProjectRetrieverCoreMixin
from .reasoner_retriever_help.retriever_intent_section_mixin import (
    ProjectRetrieverIntentSectionMixin,
)
from .reasoner_retriever_help.retriever_routing_private_impl import (
    _build_canonical_section_bundle_impl,
    _collect_section_file_evidence_impl,
    _is_section_only_intent_impl,
    _merge_section_file_evidence_impl,
    _resolve_effective_limits_impl,
    _resolve_query_kind_impl,
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
