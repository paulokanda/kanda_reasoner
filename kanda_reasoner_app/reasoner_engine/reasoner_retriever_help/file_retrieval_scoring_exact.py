r"""Exact-match, call-site, and graph-shape scoring for file retrieval."""
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.exact_code_anchors import (
    extract_question_file_names,
    extract_strict_requested_file_paths,
    path_is_project_qa_run_analysis_distractor,
    path_matches_project_qa_run_analysis_trace_file,
    path_matches_requested_file,
    path_matches_strict_requested_path,
    project_qa_run_analysis_trace_requested,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_context import (
    CandidateFileContext,
    RetrievalQueryContext,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import (
    last_part_match_in_query,
    norm_text,
)

__all__ = [
    'apply_exact_and_call_scoring',
]



def apply_exact_and_call_scoring(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    q = query.q
    path = candidate.path
    file_record = candidate.file_record
    haystack = candidate.haystack
    normalized_path = candidate.normalized_path
    base_name = candidate.base_name
    function_names = candidate.function_names
    class_names = candidate.class_names
    called_symbols = candidate.called_symbols

    if query.reset_runtime_query:
        asks_amplitude_map = (
            "amplitude map" in q
            or "amplitude-map" in q
            or "amp map" in q
            or "topomap" in q
        )

        amplitude_map_side_file = (
            "eeg_amplitude_map_initializer.py" in normalized_path
            or "/amplitude_map/" in normalized_path
            or "amplitude_map" in base_name
        )

        core_reset_runtime_file = (
            normalized_path.startswith("shell/viewer/eeg_visualizer_core.py")
            or normalized_path.startswith("core/snapshot/eeg_pipeline_reset.py")
            or normalized_path.startswith("core/snapshot/eeg_session_snapshot.py")
        )

        if (
            amplitude_map_side_file
            and not asks_amplitude_map
            and not core_reset_runtime_file
        ):
            score -= 220
            reasons.append("reset-runtime-amplitude-map-file-penalty")

    strict_requested_paths = extract_strict_requested_file_paths(q)
    strict_path_match = path_matches_strict_requested_path(path, strict_requested_paths)
    requested_file_names = extract_question_file_names(q)
    requested_file_match = path_matches_requested_file(path, requested_file_names)

    if strict_requested_paths:
        if strict_path_match:
            score += 5000
            reasons.append("strict-requested-path-allowlist-boost")
        else:
            score -= 10000
            reasons.append("outside-strict-requested-path-allowlist-penalty")

    if normalized_path in q:
        score += 1200
        reasons.append("exact-path-match")

    if base_name and base_name in q:
        score += 1200
        reasons.append("exact-filename-match")

    for file_name in query.question_file_names:
        if base_name == file_name.lower():
            score += 1400
            reasons.append("question-filename-match")

    if requested_file_match:
        score += 2600
        reasons.append("required-exact-filename-anchor")
    elif requested_file_names:
        score -= 120
        reasons.append("outside-requested-filename-anchor")

    if project_qa_run_analysis_trace_requested(q):
        if path_matches_project_qa_run_analysis_trace_file(path):
            score += 2800
            reasons.append("project-qa-run-analysis-trace-file-boost")
        elif path_is_project_qa_run_analysis_distractor(path):
            score -= 1800
            reasons.append("project-qa-run-analysis-distractor-penalty")

    for token in query.tokens:
        if token in haystack:
            score += 3
            reasons.append("token:" + token)

    if query.intents["packaging_metadata"] and path in query.packaging_files:
        score += 220
        reasons.append("packaging-file-boost")

    if query.intents["documentation_intent"] and path in query.documentation_files:
        score += 220
        reasons.append("documentation-file-boost")

    score = _score_exact_class_and_call_symbols(
        q,
        class_names,
        called_symbols,
        score,
        reasons,
    )

    if query.exact_reference_query:
        score = _score_exact_references(
            retriever,
            query,
            candidate,
            score,
            reasons,
        )

    if query.wants_call_site:
        score = _score_call_sites(
            retriever,
            query,
            candidate,
            score,
            reasons,
        )

    if query.intents["explicit_call_chain"] and "retriever.v.main_window.show" in haystack:
        score += 220
        reasons.append("exact-call-chain-match")

    if query.intents["main_window_show"]:
        score = _score_main_window_show(candidate, score, reasons)

    if query.intents["qtimer_showmaximized"]:
        score = _score_qtimer_showmaximized(candidate, score, reasons)

    if query.intents["where_is"]:
        score = _score_where_is(query, candidate, score, reasons)

    if query.intents["which_calls"]:
        score = _score_which_calls(query, candidate, score, reasons)

    return score


def _score_exact_class_and_call_symbols(
    q: str,
    class_names: list[str],
    called_symbols: list[str],
    score: int,
    reasons: list[str],
) -> int:
    for class_name in class_names:
        class_name_norm = norm_text(class_name)
        if class_name_norm and class_name_norm in q:
            score += 180
            reasons.append("exact-class-match")

        class_tail = class_name_norm.split(".")[-1]
        if class_tail and class_tail in q:
            score += 100
            reasons.append("exact-class-tail-match")

    for called_symbol in called_symbols:
        called_symbol_norm = norm_text(called_symbol)
        if called_symbol_norm and called_symbol_norm in q:
            score += 20
            reasons.append("exact-called-symbol-match")

    return score


def _score_exact_references(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    import_blob = " ".join(candidate.file_record.get("imports", []))
    import_blob_low = norm_text(import_blob)
    full_source = norm_text(candidate.file_record.get("full_source", ""))

    for target in query.exact_symbol_targets:
        if not target:
            continue

        token_hit = target in candidate.haystack
        import_hit = target in import_blob_low
        call_hit = full_source and f"{target}(" in full_source

        if token_hit:
            score += 120
            reasons.append("exact-reference-token-match:" + target)

        if import_hit:
            score += 180
            reasons.append("exact-reference-import-boost:" + target)

        if call_hit:
            score += 360
            reasons.append("exact-reference-callsite-boost:" + target)

        if full_source and f"import {target}" in full_source:
            score += 120
            reasons.append("exact-reference-import-line-boost:" + target)

        if full_source and "from " in full_source and target in full_source:
            score += 80
            reasons.append("exact-reference-from-import-boost:" + target)

        if import_hit and call_hit:
            score += 320
            reasons.append("exact-reference-import-plus-call-boost:" + target)

        timeline_target_match = (
            "timeline" in target
            or any(
                term in target
                for term in retriever._profile_alias_terms("timeline_symbol_terms")
            )
        )
        if timeline_target_match:
            if any(
                owner_path in candidate.normalized_path
                for owner_path in retriever._profile_owner_paths("timeline_owner_paths")
            ):
                score += 180
                reasons.append("timeline-exact-caller-owner-path-boost")

    return score


def _score_call_sites(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    haystack = candidate.haystack
    normalized_path = candidate.normalized_path
    if "build_and_show" in haystack:
        score += 120
        reasons.append("call-site-build-and-show-boost")

    if any(term in normalized_path for term in ["main_window_builder", "viewer"]):
        score += 80
        reasons.append("call-site-main-window-path-boost")

    navbar_callsite_match = query.asks_for_navbar_builder and (
        retriever._text_has_profile_alias(haystack, "navbar_builder_terms")
    )
    notebook_callsite_match = query.asks_for_notebook_builder and (
        retriever._text_has_profile_alias(haystack, "notebook_builder_terms")
    )

    if navbar_callsite_match:
        score += 180
        reasons.append("call-site-navbar-builder-boost")

    if notebook_callsite_match:
        score += 180
        reasons.append("call-site-notebook-builder-boost")

    if (
        query.asks_for_navbar_builder
        and query.asks_for_notebook_builder
        and "build_and_show" in haystack
        and navbar_callsite_match
        and notebook_callsite_match
    ):
        score += 260
        reasons.append("call-site-combined-builder-chain-boost")

    if any(
        term in haystack
        for term in retriever._profile_alias_terms("builder_callsite_markers")
    ):
        score += 140
        reasons.append("call-site-builder-marker-family-boost")

    return score


def _score_main_window_show(
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    haystack = candidate.haystack
    normalized_path = candidate.normalized_path
    if "retriever.v.main_window.show" in haystack:
        score += 260
        reasons.append("main-window-show-call-boost")

    if "build_and_show" in haystack:
        score += 180
        reasons.append("main-window-show-build-and-show-boost")

    if any(term in normalized_path for term in ["main_window", "viewer", "launcher"]):
        score += 50
        reasons.append("main-window-show-path-boost")

    if any(
        term in normalized_path
        for term in ["migration_", "legacy_import", "auditor", "scanner"]
    ):
        score -= 180
        reasons.append("main-window-show-non-ui-penalty")
    return score


def _score_qtimer_showmaximized(
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    haystack = candidate.haystack
    normalized_path = candidate.normalized_path
    if (
        "qtimer.singleshot" in haystack
        and "retriever.v.main_window.showmaximized" in haystack
    ):
        score += 320
        reasons.append("qtimer-showmaximized-exact-call-boost")

    if "showmaximized" in haystack and "qtimer.singleshot" not in haystack:
        score -= 180
        reasons.append("direct-showmaximized-without-qtimer-penalty")

    if any(term in normalized_path for term in ["main_window", "viewer", "launcher"]):
        score += 40
        reasons.append("qtimer-showmaximized-path-boost")
    return score


def _score_where_is(
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if any(name in query.q for name in candidate.class_names):
        score += 220
        reasons.append("where-is-class-definition-boost")

    if any(name in query.q for name in candidate.function_names):
        score += 160
        reasons.append("where-is-function-definition-boost")

    if last_part_match_in_query(candidate.function_names, query.q):
        score += 60
        reasons.append("where-is-function-tail-boost")

    if last_part_match_in_query(candidate.class_names, query.q):
        score += 80
        reasons.append("where-is-class-tail-boost")
    return score


def _score_which_calls(
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if candidate.called_symbols:
        score += 20
        reasons.append("which-calls-has-call-graph")

    if any(token in " ".join(candidate.called_symbols) for token in query.tokens):
        score += 120
        reasons.append("which-calls-called-symbol-boost")

    if not candidate.called_symbols:
        score -= 40
        reasons.append("which-calls-no-calls-penalty")
    return score
