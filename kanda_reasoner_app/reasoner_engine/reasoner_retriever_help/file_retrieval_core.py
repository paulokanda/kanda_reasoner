# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/file_retrieval_core.py
r"""Public retrieve_files implementation split from the large file_retrieval facade."""
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.v10_models import EvidenceItem
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_context import (
    build_candidate_context,
    build_query_context,
    candidate_file_paths,
    reindex_file_evidence,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_exact import (
    apply_exact_and_call_scoring,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_runtime import (
    apply_advanced_and_runtime_scoring,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_semantic import (
    apply_semantic_scoring,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import (
    is_allowed_project_path,
)

__all__ = []


def retrieve_files(retriever, question: str, limit: int) -> list[EvidenceItem]:
    """Return ranked file evidence for a ProjectRetriever question.

    The orchestration remains intentionally thin: query normalization and
    candidate context building are delegated to file_retrieval_context, scoring
    is delegated to cohesive scoring modules, and compact evidence rendering
    remains behind the retriever public helper. This keeps the public behavior
    equivalent to the former monolithic implementation while avoiding a new
    thousand-line helper.
    """
    query = build_query_context(retriever, question)
    scored: list[EvidenceItem] = []

    # runtime_signal_connections are collector-internal probe signals.
    # Do not add their source files to candidate_paths - they are not
    # EEG project files and would inject empty-content noise into evidence.
    for path in sorted(candidate_file_paths(retriever, query)):
        if not is_allowed_project_path(path):
            continue

        candidate = build_candidate_context(retriever, path)
        score = 0
        reasons: list[str] = []

        score = apply_exact_and_call_scoring(
            retriever,
            query,
            candidate,
            score,
            reasons,
        )
        score = apply_semantic_scoring(
            retriever,
            query,
            candidate,
            score,
            reasons,
        )
        score = apply_advanced_and_runtime_scoring(
            retriever,
            query,
            candidate,
            score,
            reasons,
        )

        if score <= 0:
            continue

        detail = retriever._build_compact_file_evidence(path, reasons)
        scored.append(
            EvidenceItem(
                evidence_id="",
                score=score,
                path=path,
                module_name=candidate.module_name,
                reason=", ".join(sorted(set(reasons))),
                detail=detail,
            )
        )

    return reindex_file_evidence(scored, limit)
