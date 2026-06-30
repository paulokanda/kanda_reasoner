# project-path: kanda_reasoner_app/routing_signal_scorer/contract.py
"""Public compatibility facade for the KANDA routing signal scorer.

The implementation is split into cohesive ordinary Python modules. This facade
keeps the original public API and compatibility private helper names available
from ``kanda_reasoner_app.routing_signal_scorer.contract``.
"""

from __future__ import annotations

from .advisory import (
    _advisory_notes,
    _caution_flags,
    _coerce_score,
    _route_family_suggestions,
    build_routing_advisory,
    summarize_advisory,
)
from .models import (
    ADVISORY_AUTHORITY,
    ADVISORY_FEATURE_ID,
    AUTHORITY,
    FEATURE_ID,
    PRE_OUTPUT_HOOK,
    PRE_OUTPUT_TRIGGER_SIGNALS,
    SCHEMA_VERSION,
    SIGNAL_NAMES,
    SIMILARITY_BOX_SHIELD_FEATURE_ID,
    SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_EXPLAINABILITY_FEATURE_ID,
    SIMILARITY_HIGH_THRESHOLD,
    SIMILARITY_PROMOTION_THRESHOLD,
    SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
    SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_RUNTIME_LITE_FEATURE_ID,
    SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
    SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
    SIMILARITY_VISIBILITY_THRESHOLD,
    SignalRule,
)
from .scoring import (
    _add_evidence,
    _add_score,
    _apply_combination_rules,
    _excerpt,
    _level,
    _matched_patterns,
    _normalize,
    _recommended_hooks,
    _rules,
    score_routing_signals,
    summarize_signal_result,
)
from .shield import (
    build_similarity_box_shield_status,
    render_similarity_box_shield_status_text,
)
from .similarity_preview import (
    _candidate_prompt_contexts_for_route_families,
    _similarity_prompt_context_preview_lines,
    _similarity_ui_preview_lines,
    build_similarity_prompt_context_preview,
    build_similarity_ui_preview_adapter,
    render_similarity_prompt_context_preview_text,
    render_similarity_ui_preview_text,
)
from .similarity_runtime import (
    _containment,
    _jaccard,
    _load_similarity_corpus,
    _matched_terms_from_profiles,
    _merge_route_family_suggestions,
    _merge_string_lists,
    _profile_similarity,
    _similarity_advisory_only_reason,
    _similarity_decision_report,
    _similarity_decision_report_summary,
    _similarity_expected_values,
    _similarity_explainability_summary,
    _similarity_level,
    _similarity_match_explainability,
    _similarity_notes,
    _similarity_route_family_suggestions,
    _similarity_rule_hook_independence_reason,
    _similarity_threshold_level,
    _similarity_threshold_policy,
    _text_profile,
    _tokenize_for_similarity,
    build_similarity_runtime_lite_advisory,
    summarize_similarity_runtime_lite_advisory,
)

__all__ = [
    "build_routing_advisory",
    "build_similarity_box_shield_status",
    "build_similarity_prompt_context_preview",
    "build_similarity_runtime_lite_advisory",
    "build_similarity_ui_preview_adapter",
    "render_similarity_box_shield_status_text",
    "render_similarity_prompt_context_preview_text",
    "render_similarity_ui_preview_text",
    "score_routing_signals",
    "SignalRule",
    "summarize_advisory",
    "summarize_signal_result",
    "summarize_similarity_runtime_lite_advisory",
]
