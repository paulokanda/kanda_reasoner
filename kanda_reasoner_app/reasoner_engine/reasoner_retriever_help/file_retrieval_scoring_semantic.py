r"""Semantic, startup, and explanation scoring for file retrieval."""
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_context import (
    CandidateFileContext,
    RetrievalQueryContext,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_explain import (
    apply_explanation_heavy_scoring,
    apply_startup_scoring,
)

__all__ = [
    'apply_semantic_scoring',
]



def apply_semantic_scoring(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if query.intents["explain_chain"]:
        score = _score_explain_chain(retriever, query, candidate, score, reasons)

    if (
        retriever._question_has_profile_alias(query.q, "topomap_explanation")
        or query.intents["topomap_explanation"]
    ):
        score = _score_topomap_explanation(
            retriever,
            query,
            candidate,
            score,
            reasons,
        )

    if query.reset_cleanup_query:
        score = _score_reset_cleanup(retriever, candidate, score, reasons)

    score = _score_explicit_call_chain_penalties(query, candidate, score, reasons)
    score = _score_light_topical_terms(retriever, query, candidate, score, reasons)
    score = _score_subsystems(retriever, query, candidate, score, reasons)

    if query.intents["startup"]:
        score = apply_startup_scoring(retriever, query, candidate, score, reasons)

    if query.explanation_heavy:
        score = apply_explanation_heavy_scoring(query, candidate, score, reasons)

    return score


def _score_explain_chain(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if candidate.path in query.entry_files:
        score += 80
        reasons.append("explain-chain-entry-file-boost")

    if any(
        term in candidate.normalized_path
        for term in ["main", "builder", "launcher", "interface_manager", "viewer"]
    ):
        score += 50
        reasons.append("explain-chain-orchestrator-path-boost")

    orchestration_terms = [
        "qapplication",
        "build_and_show",
        "create_main_window",
        "create_main_widget",
        "addtab",
        "setcentralwidget",
        "show(",
        "showmaximized",
    ]
    if any(term in candidate.haystack for term in orchestration_terms):
        score += 60
        reasons.append("explain-chain-orchestration-boost")

    chain_key = None
    if "startup" in query.q:
        chain_key = "startup_chain"
    elif "timeline" in query.q or retriever._question_has_profile_alias(
        query.q, "timeline"
    ):
        chain_key = "timeline_chain"
    elif "topomap" in query.q or "amplitude" in query.q:
        chain_key = "topomap_chain"
    elif query.reset_cleanup_query:
        chain_key = "reset_chain"

    if chain_key:
        chain_steps = retriever.idx.execution_chains.get(chain_key, [])
        chain_files = {
            str(step.get("file", "")).strip()
            for step in chain_steps
            if isinstance(step, dict) and str(step.get("file", "")).strip()
        }
        if candidate.path in chain_files:
            score += 180
            reasons.append("named-chain-step-boost")

    if any(
        marker in candidate.normalized_path
        for marker in [
            "common/templates/tables",
            "core/snapshot",
        ]
    ):
        score -= 120
        reasons.append("topomap-implementation-non-owner-penalty")

    return score


def _score_topomap_explanation(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    topomap_implementation_query = any(
        term in query.q
        for term in [
            "implement",
            "implements",
            "implemented",
            "implementation",
            "creating",
            "updating",
            "participate in creating",
            "participate in updating",
            "modules participate",
            "which code implements",
            "which modules participate",
        ]
    )

    if "topomap" in candidate.haystack or retriever._text_has_profile_alias(
        candidate.haystack, "topomap"
    ):
        score += 220
        reasons.append("topomap-explanation-core-boost")

    if "amplitude_map" in candidate.haystack or any(
        term in candidate.haystack
        for term in retriever._profile_alias_terms("topomap_symbol_terms")
    ):
        score += 140
        reasons.append("topomap-explanation-amplitude-map-boost")

    if any(
        marker in candidate.haystack
        for marker in [
            "render",
            "renderer",
            "draw",
            "plot",
            "topography",
            "topographic",
        ]
    ) or any(
        term in candidate.haystack
        for term in retriever._profile_alias_terms("topomap_symbol_terms")
    ):
        score += 120
        reasons.append("topomap-explanation-render-boost")

    if any(
        owner_path in candidate.normalized_path
        for owner_path in retriever._profile_owner_paths("topomap_owner_paths")
    ):
        score += 80
        reasons.append("topomap-explanation-path-boost")

    if topomap_implementation_query:
        score = _score_topomap_implementation(retriever, candidate, score, reasons)

    return score


def _score_topomap_implementation(
    retriever,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    owner_path_hit = any(
        owner_path in candidate.normalized_path
        for owner_path in retriever._profile_owner_paths("topomap_owner_paths")
    )

    symbol_family_hit = any(
        term in candidate.haystack
        for term in retriever._profile_alias_terms("topomap_symbol_terms")
    )

    core_symbol_hit = (
        "eegamplitudemap" in candidate.haystack or "toporenderer" in candidate.haystack
    )

    if owner_path_hit:
        score += 300
        reasons.append("topomap-implementation-owner-path-boost")

    if symbol_family_hit:
        score += 220
        reasons.append("topomap-implementation-symbol-family-boost")

    if core_symbol_hit:
        score += 260
        reasons.append("topomap-implementation-core-symbol-boost")

    if owner_path_hit and symbol_family_hit:
        score += 220
        reasons.append("topomap-implementation-owner-plus-symbol-boost")

    if owner_path_hit and core_symbol_hit:
        score += 240
        reasons.append("topomap-implementation-owner-plus-core-boost")

    if any(
        marker in candidate.normalized_path
        for marker in [
            "common/templates/tables",
            "core/snapshot",
            "migration_",
            "legacy_import",
            "auditor",
            "scanner",
        ]
    ):
        score -= 220
        reasons.append("topomap-implementation-non-owner-penalty")

    if (
        "label_renderer" in candidate.normalized_path
        and "topomap_renderer" not in candidate.normalized_path
    ):
        score -= 80
        reasons.append("topomap-implementation-adjacent-renderer-penalty")

    return score


def _score_reset_cleanup(
    retriever,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if any(
        owner_path in candidate.normalized_path
        for owner_path in retriever._profile_owner_paths("reset_cleanup_owner_paths")
    ):
        score += 160
        reasons.append("reset-cleanup-owner-path-boost")

    if any(
        term in candidate.haystack
        for term in retriever._profile_alias_terms("reset_cleanup_symbol_terms")
    ):
        score += 140
        reasons.append("reset-cleanup-symbol-family-boost")

    if retriever._text_has_profile_alias(candidate.haystack, "reset_cleanup"):
        score += 80
        reasons.append("reset-cleanup-alias-boost")
    return score


def _score_explicit_call_chain_penalties(
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if query.intents["explicit_call_chain"]:
        if any(
            term in candidate.normalized_path
            for term in ["migration_", "legacy_import", "auditor", "scanner"]
        ):
            score -= 160
            reasons.append("non-ui-callchain-penalty")

        if any(
            term in candidate.normalized_path
            for term in ["main_window", "viewer", "launcher"]
        ):
            score += 40
            reasons.append("ui-callchain-path-boost")
    return score


def _score_light_topical_terms(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if candidate.path in query.entry_files and any(
        key in query.q for key in ["start", "startup", "main", "launch", "open", "show"]
    ):
        score += 14
        reasons.append("entry-file")

    if "topomap" in query.q and (
        "topomap" in candidate.haystack
        or "amplitude_map" in candidate.haystack
        or retriever._text_has_profile_alias(candidate.haystack, "topomap")
        or any(
            term in candidate.haystack
            for term in retriever._profile_alias_terms("topomap_symbol_terms")
        )
    ):
        score += 12
        reasons.append("topomap-related")

    if "timeline" in query.q and "timeline" in candidate.haystack:
        score += 12
        reasons.append("timeline-related")

    if retriever._question_has_profile_alias(query.q, "timeline"):
        if any(
            owner_path in candidate.normalized_path
            for owner_path in retriever._profile_owner_paths("timeline_owner_paths")
        ):
            score += 80
            reasons.append("timeline-owner-path-boost")

        if any(
            term in candidate.haystack
            for term in retriever._profile_alias_terms("timeline_symbol_terms")
        ):
            score += 120
            reasons.append("timeline-symbol-family-boost")

    if "splash" in query.q and "splash" in candidate.haystack:
        score += 12
        reasons.append("splash-related")

    if "tab" in query.q and (
        "tab" in candidate.haystack or "notebook" in candidate.haystack or "addtab" in candidate.haystack
    ):
        score += 12
        reasons.append("tab-related")

    if query.reset_cleanup_query and (
        "reset" in candidate.haystack
        or "snapshot" in candidate.haystack
        or "cleanup" in candidate.haystack
        or "close" in candidate.haystack
        or retriever._text_has_profile_alias(candidate.haystack, "reset_cleanup")
        or any(
            term in candidate.haystack
            for term in retriever._profile_alias_terms("reset_cleanup_symbol_terms")
        )
    ):
        score += 12
        reasons.append("reset-related")

    if "responsibility" in query.q and (
        "manager" in candidate.haystack
        or "builder" in candidate.haystack
        or "controller" in candidate.haystack
    ):
        score += 10
        reasons.append("responsibility-related")

    if "uncertainty" in query.q and (
        "warning" in candidate.haystack
        or "try" in candidate.haystack
        or "exception" in candidate.haystack
    ):
        score += 8
        reasons.append("uncertainty-related")

    return score


def _score_subsystems(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    for sub in retriever.idx.subsystems:
        sub_name = str(sub.get("name", "")).strip().lower()
        if not sub_name:
            continue

        if sub_name in query.q:
            sub_files = sub.get("files", [])
            if isinstance(sub_files, list) and candidate.path in sub_files:
                score += 60
                reasons.append("subsystem-member-boost:" + sub_name)
            break
    return score

