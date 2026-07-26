"""Threshold, explainability, and decision-reporting helpers."""

from __future__ import annotations

from typing import Mapping, Sequence

from .advisory import _coerce_score
from .models import (
    SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_EXPLAINABILITY_FEATURE_ID,
    SIMILARITY_HIGH_THRESHOLD,
    SIMILARITY_PROMOTION_THRESHOLD,
    SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
    SIMILARITY_VISIBILITY_THRESHOLD,
)


def _similarity_level(value: float) -> str:
    """Classify a score as low, medium, or high."""

    if value >= SIMILARITY_HIGH_THRESHOLD:
        return "high"
    if value >= SIMILARITY_PROMOTION_THRESHOLD:
        return "medium"
    return "low"


def _similarity_threshold_level(value: float) -> str:
    """Classify a score against visibility and promotion thresholds."""

    if value < SIMILARITY_VISIBILITY_THRESHOLD:
        return "hidden"
    if value < SIMILARITY_PROMOTION_THRESHOLD:
        return "visible_low"
    if value < SIMILARITY_HIGH_THRESHOLD:
        return "promoted_medium"
    return "high"


def _similarity_advisory_only_reason() -> str:
    """Describe why similarity evidence cannot decide the final route."""

    return (
        "Similarity matches are corpus anchors only. The deterministic KANDA "
        "routing canon decides final route, required prompts, and May proceed now."
    )


def _similarity_rule_hook_independence_reason() -> str:
    """Describe the independence of rule diagnostics from similarity."""

    return (
        "Rule-based diagnostic hooks remain independent of similarity matches; "
        "high-risk patch, freeze, terminal, and project-root signals still come "
        "from rule diagnostics and governed pre-output gates."
    )


def _similarity_match_explainability(
    match: Mapping[str, object],
) -> dict[str, object]:
    """Build explainability metadata for one similarity match."""

    score = _coerce_score(match.get("similarity_score", 0.0))
    route_families = match.get("matched_route_families", [])
    if not isinstance(route_families, Sequence) or isinstance(
        route_families,
        (str, bytes),
    ):
        route_families = []
    corpus_item_id = str(
        match.get("matched_corpus_item_id") or match.get("case_id") or ""
    )
    return {
        "feature_id": SIMILARITY_EXPLAINABILITY_FEATURE_ID,
        "matched_corpus_item_id": corpus_item_id,
        "matched_route_families": [str(item) for item in route_families],
        "similarity_score": round(score, 3),
        "threshold_level": _similarity_threshold_level(score),
        "route_family_suggestion_eligible": score
        >= SIMILARITY_PROMOTION_THRESHOLD,
        "threshold_policy_feature_id": SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "does_not_override_router": True,
        "may_proceed_now_decision": "not_provided_by_similarity",
        "final_route_decision": "not_provided_by_similarity",
        "advisory_only_reason": _similarity_advisory_only_reason(),
        "rule_hook_independence": _similarity_rule_hook_independence_reason(),
    }


def _similarity_explainability_summary() -> dict[str, object]:
    """Describe the explainability contract for similarity matches."""

    return {
        "feature_id": SIMILARITY_EXPLAINABILITY_FEATURE_ID,
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "does_not_override_router": True,
        "threshold_policy_feature_id": SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
        "threshold_levels": {
            "hidden": "score < visibility_threshold",
            "visible_low": "visibility_threshold <= score < promotion_threshold",
            "promoted_medium": "promotion_threshold <= score < high_threshold",
            "high": "score >= high_threshold",
        },
        "match_fields": [
            "matched_corpus_item_id",
            "matched_route_families",
            "similarity_score",
            "threshold_level",
            "route_family_suggestion_eligible",
            "advisory_only_reason",
            "rule_hook_independence",
        ],
        "advisory_only_reason": _similarity_advisory_only_reason(),
        "rule_hook_independence": _similarity_rule_hook_independence_reason(),
    }


def _similarity_decision_report_summary() -> dict[str, object]:
    """Describe the compact human-readable decision report contract."""

    return {
        "feature_id": SIMILARITY_DECISION_REPORT_FEATURE_ID,
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "does_not_override_router": True,
        "format": "compact_human_readable_lines",
        "fields": [
            "top_match",
            "top_match_score",
            "top_match_threshold_level",
            "route_family_suggestion_eligible",
            "matched_route_families",
            "advisory_only_reason",
            "rule_hook_independence",
        ],
        "advisory_only_reason": _similarity_advisory_only_reason(),
        "rule_hook_independence": _similarity_rule_hook_independence_reason(),
    }


def _similarity_decision_report(
    matches: Sequence[Mapping[str, object]],
    recommended_hooks: Sequence[object],
) -> list[str]:
    """Build compact decision-report lines for a similarity result."""

    top_match: Mapping[str, object] | None = None
    for item in matches:
        if isinstance(item, Mapping):
            top_match = item
            break

    lines = [
        "Similarity decision report",
        "feature_id=" + SIMILARITY_DECISION_REPORT_FEATURE_ID,
        "authority=" + SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "does_not_override_router=True",
        "may_proceed_now_decision=not_provided_by_similarity",
        "route_override=None",
    ]

    if top_match is None:
        lines.extend(
            [
                "top_match=none",
                "top_match_score=0.000",
                "top_match_threshold_level=hidden",
                "route_family_suggestion_eligible=False",
                "matched_route_families=none",
            ]
        )
    else:
        score = _coerce_score(top_match.get("similarity_score", 0.0))
        route_families = top_match.get("matched_route_families", [])
        if not isinstance(route_families, Sequence) or isinstance(
            route_families,
            (str, bytes),
        ):
            route_families = []
        family_text = (
            ", ".join(str(item) for item in route_families if str(item))
            or "none"
        )
        top_match_id = str(
            top_match.get("matched_corpus_item_id")
            or top_match.get("case_id")
            or ""
        )
        lines.extend(
            [
                "top_match=" + top_match_id,
                "top_match_score=" + f"{score:.3f}",
                "top_match_threshold_level="
                + _similarity_threshold_level(score),
                "route_family_suggestion_eligible="
                + str(score >= SIMILARITY_PROMOTION_THRESHOLD),
                "matched_route_families=" + family_text,
            ]
        )

    hooks = [str(item) for item in recommended_hooks if str(item)]
    lines.extend(
        [
            "advisory_only_reason=" + _similarity_advisory_only_reason(),
            "rule_hook_independence="
            + _similarity_rule_hook_independence_reason(),
            "recommended_hooks=" + (", ".join(hooks) if hooks else "none"),
        ]
    )
    return lines


def _similarity_threshold_policy() -> dict[str, object]:
    """Return the deterministic similarity threshold policy."""

    return {
        "policy_feature_id": SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
        "visibility_threshold": SIMILARITY_VISIBILITY_THRESHOLD,
        "promotion_threshold": SIMILARITY_PROMOTION_THRESHOLD,
        "high_threshold": SIMILARITY_HIGH_THRESHOLD,
        "hidden_range": "score < visibility_threshold",
        "low_range": "visibility_threshold <= score < promotion_threshold",
        "medium_range": "promotion_threshold <= score < high_threshold",
        "high_range": "score >= high_threshold",
        "route_family_suggestion_minimum": SIMILARITY_PROMOTION_THRESHOLD,
        "rule_hooks_independent": True,
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "does_not_override_router": True,
        "may_proceed_now_decision": "not_provided_by_similarity",
    }


def _matched_terms_from_profiles(
    left: Mapping[str, set[str]],
    right: Mapping[str, set[str]],
    limit: int = 8,
) -> list[str]:
    """Return sorted shared token terms, bounded by the requested limit."""

    terms = sorted(
        set(left.get("tokens", set())) & set(right.get("tokens", set()))
    )
    return terms[:limit]


def _similarity_route_family_suggestions(
    matches: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    """Build deduplicated route-family suggestions from promoted matches."""

    suggestions: list[dict[str, object]] = []
    seen: set[str] = set()
    for match in matches:
        score = _coerce_score(match.get("similarity_score", 0.0))
        if score < SIMILARITY_PROMOTION_THRESHOLD:
            continue
        families = match.get("expected_route_families", [])
        if not isinstance(families, Sequence) or isinstance(
            families,
            (str, bytes),
        ):
            continue
        for family in families:
            family_text = str(family)
            if not family_text or family_text in seen:
                continue
            seen.add(family_text)
            matched_item_id = str(
                match.get("matched_corpus_item_id")
                or match.get("case_id")
                or ""
            )
            suggestions.append(
                {
                    "family": family_text,
                    "confidence": _similarity_level(score),
                    "score": round(score, 3),
                    "source_signal": "similarity_runtime_lite",
                    "source_case_id": str(match.get("case_id") or ""),
                    "matched_corpus_item_id": matched_item_id,
                    "threshold_level": _similarity_threshold_level(score),
                    "advisory_only_reason": _similarity_advisory_only_reason(),
                    "rule_hook_independence": (
                        _similarity_rule_hook_independence_reason()
                    ),
                    "reason": (
                        "Similar frozen corpus scenario detected. Advisory only."
                    ),
                }
            )
    return suggestions
