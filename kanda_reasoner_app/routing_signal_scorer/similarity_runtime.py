# project-path: kanda_reasoner_app/routing_signal_scorer/similarity_runtime.py
"""Runtime-lite lexical similarity advisory chain for routing signals."""

from __future__ import annotations

import json as json
from pathlib import Path as Path
import re as re
from typing import Mapping, Sequence

from ._similarity_runtime_cohesive_operations_2 import (
    _merge_route_family_suggestions,
    _merge_string_lists,
    _similarity_expected_values,
    _similarity_notes,
)
from ._similarity_runtime_decision_reporting import (
    _matched_terms_from_profiles,
    _similarity_advisory_only_reason as _similarity_advisory_only_reason,
    _similarity_decision_report,
    _similarity_decision_report_summary,
    _similarity_explainability_summary,
    _similarity_level,
    _similarity_match_explainability,
    _similarity_route_family_suggestions,
    _similarity_rule_hook_independence_reason as _rule_hook_independence_reason,
    _similarity_threshold_level,
    _similarity_threshold_policy,
)
from ._similarity_runtime_serialization import (
    _containment as _containment,
    _jaccard as _jaccard,
    _load_similarity_corpus,
    _profile_similarity,
    _text_profile,
    _tokenize_for_similarity as _tokenize_for_similarity,
)
from .advisory import build_routing_advisory
from .models import (
    SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_EXPLAINABILITY_FEATURE_ID,
    SIMILARITY_HIGH_THRESHOLD,
    SIMILARITY_PROMOTION_THRESHOLD,
    SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_RUNTIME_LITE_FEATURE_ID,
    SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
    SIMILARITY_VISIBILITY_THRESHOLD,
)

_similarity_rule_hook_independence_reason = _rule_hook_independence_reason


def build_similarity_runtime_lite_advisory(
    text: str,
    *,
    max_matches: int = 3,
    min_similarity: float = SIMILARITY_VISIBILITY_THRESHOLD,
) -> dict[str, object]:
    """Build advisory-only lexical similarity hints from the frozen corpus.

    Runtime-lite similarity is deterministic and local. It uses token overlap
    against the curated v2 corpus to surface similar scenario anchors. It does
    not use embeddings, TF-IDF, external dependencies, self-learning, global
    state, or router authority.
    """

    source_text = str(text or "")
    source_advisory = build_routing_advisory(source_text, max_suggestions=12)
    corpus = _load_similarity_corpus()
    cases = corpus.get("cases", [])
    if not isinstance(cases, Sequence) or isinstance(cases, (str, bytes)):
        cases = []

    query_profile = _text_profile(source_text)
    matches: list[dict[str, object]] = []

    for case in cases:
        if not isinstance(case, Mapping):
            continue
        case_text = str(case.get("text") or "")
        case_profile = _text_profile(case_text)
        similarity = _profile_similarity(query_profile, case_profile)
        if similarity < min_similarity:
            continue
        route_families = list(case.get("expected_route_families") or [])
        match = {
            "case_id": str(case.get("id") or ""),
            "matched_corpus_item_id": str(case.get("id") or ""),
            "category": str(case.get("category") or ""),
            "similarity_score": round(similarity, 3),
            "similarity_level": _similarity_level(similarity),
            "threshold_level": _similarity_threshold_level(similarity),
            "route_family_suggestion_eligible": similarity
            >= SIMILARITY_PROMOTION_THRESHOLD,
            "matched_terms": _matched_terms_from_profiles(
                query_profile,
                case_profile,
            ),
            "expected_route_families": route_families,
            "matched_route_families": route_families,
            "expected_hooks": list(case.get("expected_hooks") or []),
            "expected_caution_flags": list(
                case.get("expected_caution_flags") or []
            ),
            "notes": str(case.get("notes") or ""),
        }
        match["explainability"] = _similarity_match_explainability(match)
        matches.append(match)

    matches.sort(
        key=lambda item: float(item["similarity_score"]),
        reverse=True,
    )
    matches = matches[: max(1, max_matches)]

    similarity_families = _similarity_route_family_suggestions(matches)
    rule_families = source_advisory.get("suggested_route_families", [])
    if not isinstance(rule_families, Sequence) or isinstance(
        rule_families,
        (str, bytes),
    ):
        rule_families = []

    recommended_hooks = _merge_string_lists(
        source_advisory.get("recommended_hooks", []),
        _similarity_expected_values(matches, "expected_hooks"),
    )
    caution_flags = _merge_string_lists(
        source_advisory.get("caution_flags", []),
        _similarity_expected_values(matches, "expected_caution_flags"),
    )

    return {
        "schema_version": "2.0",
        "feature_id": SIMILARITY_RUNTIME_LITE_FEATURE_ID,
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "runtime_status": "RUNTIME_LITE",
        "similarity_method": "deterministic_token_overlap",
        "threshold_policy_feature_id": SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
        "similarity_visibility_threshold": SIMILARITY_VISIBILITY_THRESHOLD,
        "similarity_promotion_threshold": SIMILARITY_PROMOTION_THRESHOLD,
        "similarity_high_threshold": SIMILARITY_HIGH_THRESHOLD,
        "similarity_threshold_policy": _similarity_threshold_policy(),
        "similarity_explainability": _similarity_explainability_summary(),
        "explainability_feature_id": SIMILARITY_EXPLAINABILITY_FEATURE_ID,
        "decision_report_feature_id": SIMILARITY_DECISION_REPORT_FEATURE_ID,
        "similarity_decision_report": _similarity_decision_report(
            matches,
            recommended_hooks,
        ),
        "similarity_decision_report_summary": (
            _similarity_decision_report_summary()
        ),
        "does_not_override_router": True,
        "canon_decides_final_route": True,
        "may_proceed_now_decision": "not_provided_by_similarity",
        "route_override": None,
        "required_prompts_final_decision": "not_provided_by_similarity",
        "automatic_prompt_loading": False,
        "self_learning_enabled": False,
        "external_dependencies": [],
        "corpus_feature_id": str(corpus.get("feature_id") or ""),
        "corpus_case_count": len(cases),
        "source_advisory": source_advisory,
        "similar_cases": matches,
        "suggested_route_families": _merge_route_family_suggestions(
            rule_families,
            similarity_families,
        ),
        "recommended_hooks": recommended_hooks,
        "caution_flags": caution_flags,
        "similarity_notes": _similarity_notes(matches),
    }


def summarize_similarity_runtime_lite_advisory(
    advisory: Mapping[str, object],
) -> str:
    """Build a compact summary for the runtime-lite similarity advisory."""

    matches = advisory.get("similar_cases", [])
    if not isinstance(matches, Sequence) or isinstance(matches, (str, bytes)):
        matches = []

    match_parts = []
    for item in matches:
        if not isinstance(item, Mapping):
            continue
        case_id = str(item.get("case_id") or "")
        score = str(item.get("similarity_score") or "")
        threshold_level = str(item.get("threshold_level") or "")
        if case_id:
            label = case_id + "(" + score + ")"
            if threshold_level:
                label += "[" + threshold_level + "]"
            match_parts.append(label)

    hooks = advisory.get("recommended_hooks", [])
    if not isinstance(hooks, Sequence) or isinstance(hooks, (str, bytes)):
        hooks = []

    lines = [
        "Routing signal scorer runtime-lite similarity summary",
        "authority=advisory_only",
        "runtime_status=RUNTIME_LITE",
        "does_not_override_router=True",
        "canon_decides_final_route=True",
        "may_proceed_now_decision=not_provided_by_similarity",
        "route_override=None",
        "self_learning_enabled=False",
        "similar_cases="
        + (", ".join(match_parts) if match_parts else "none"),
        "decision_report="
        + ("present" if advisory.get("similarity_decision_report") else "none"),
        "recommended_hooks="
        + (", ".join(str(item) for item in hooks) if hooks else "none"),
    ]
    return "\n".join(lines)
