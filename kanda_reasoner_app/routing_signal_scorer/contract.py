"""Diagnostic routing signal scorer for KANDA prompt-call accuracy.

This box is intentionally diagnostic only. It detects likely task families,
high-risk artifact types, and useful hooks before deterministic routing runs.
It never decides the final route, never decides whether work may proceed, and
never overrides the KANDA routing canon.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Iterable, Mapping, Sequence

SCHEMA_VERSION = "1.0"
FEATURE_ID = "routing_signal_scorer_v1_diagnostic"
ADVISORY_FEATURE_ID = "routing_signal_scorer_v1_advisory"
SIMILARITY_RUNTIME_LITE_FEATURE_ID = "routing_signal_scorer_v2_similarity_runtime_lite"
SIMILARITY_THRESHOLD_POLICY_FEATURE_ID = "routing_signal_scorer_v2_similarity_threshold_policy_v1"
SIMILARITY_EXPLAINABILITY_FEATURE_ID = "routing_signal_scorer_v2_similarity_explainability_v1"
SIMILARITY_DECISION_REPORT_FEATURE_ID = "routing_signal_scorer_v2_similarity_decision_report_v1"
SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID = "routing_signal_scorer_v2_similarity_ui_preview_adapter_v1"
SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID = "routing_signal_scorer_v2_similarity_prompt_context_preview_v1"
SIMILARITY_BOX_SHIELD_FEATURE_ID = "routing_signal_scorer_v2_similarity_box_shield_v1"
SIMILARITY_VISIBILITY_THRESHOLD = 0.18
SIMILARITY_PROMOTION_THRESHOLD = 0.30
SIMILARITY_HIGH_THRESHOLD = 0.55
AUTHORITY = "diagnostic_only"
ADVISORY_AUTHORITY = "advisory_only"
SIMILARITY_RUNTIME_LITE_AUTHORITY = "advisory_only"
PRE_OUTPUT_HOOK = "pre_output_contract_gates"

SIGNAL_NAMES = (
    "fast_path_simple_explanation",
    "governed_prompt_library_update",
    "patch_delivery",
    "terminal_install_output",
    "terminal_validation_output",
    "freeze_form_json",
    "freeze_hint_sidecar",
    "freeze_memory_write",
    "external_project_root_sensitive",
    "ambiguous_or_needs_router_context",
    "pre_output_contract_gate_required",
    "confirmation_gate_bypass_risk",
    "startup_delivery_change",
)

PRE_OUTPUT_TRIGGER_SIGNALS = (
    "patch_delivery",
    "terminal_install_output",
    "terminal_validation_output",
    "freeze_form_json",
    "freeze_hint_sidecar",
    "freeze_memory_write",
    "external_project_root_sensitive",
)


@dataclass(frozen=True)
class SignalRule:
    """One keyword or pattern rule for one diagnostic signal."""

    signal: str
    weight: float
    patterns: tuple[str, ...]
    note: str


def score_routing_signals(text: str, *, max_evidence_per_signal: int = 5) -> dict[str, object]:
    """Score diagnostic routing signals for a user request or planned output.

    The returned data is suitable for logs, tests, or a diagnostics panel. It is
    not a routing decision and must not be treated as permission to proceed.
    """

    source_text = str(text or "")
    normalized = _normalize(source_text)
    scores = {name: 0.0 for name in SIGNAL_NAMES}
    evidence: dict[str, list[str]] = {name: [] for name in SIGNAL_NAMES}
    notes: list[str] = []

    for rule in _rules():
        matches = _matched_patterns(normalized, rule.patterns)
        if not matches:
            continue
        _add_score(scores, rule.signal, rule.weight)
        for item in matches[:max_evidence_per_signal]:
            _add_evidence(evidence, rule.signal, item, max_evidence_per_signal)
        if rule.note not in notes:
            notes.append(rule.note)

    _apply_combination_rules(normalized, scores, evidence, notes, max_evidence_per_signal)

    recommended_hooks = _recommended_hooks(scores)
    signal_levels = {name: _level(value) for name, value in scores.items()}

    return {
        "schema_version": SCHEMA_VERSION,
        "feature_id": FEATURE_ID,
        "authority": AUTHORITY,
        "does_not_override_router": True,
        "input_length": len(source_text),
        "input_excerpt": _excerpt(source_text),
        "signals": {name: round(scores[name], 3) for name in SIGNAL_NAMES},
        "signal_levels": signal_levels,
        "evidence": {name: items for name, items in evidence.items() if items},
        "recommended_hooks": recommended_hooks,
        "diagnostic_notes": notes,
    }


def summarize_signal_result(result: Mapping[str, object]) -> str:
    """Build a compact human-readable diagnostic summary."""

    signals = result.get("signals", {})
    if not isinstance(signals, Mapping):
        signals = {}

    high = []
    medium = []
    for name, value in signals.items():
        try:
            score = float(value)
        except (TypeError, ValueError):
            continue
        if score >= 0.7:
            high.append(str(name))
        elif score >= 0.3:
            medium.append(str(name))

    hooks = result.get("recommended_hooks", [])
    if not isinstance(hooks, Sequence) or isinstance(hooks, (str, bytes)):
        hooks = []

    lines = [
        "Routing signal scorer diagnostic summary",
        "authority=diagnostic_only",
        "does_not_override_router=True",
        "high_signals=" + (", ".join(high) if high else "none"),
        "medium_signals=" + (", ".join(medium) if medium else "none"),
        "recommended_hooks=" + (", ".join(str(item) for item in hooks) if hooks else "none"),
    ]
    return "\n".join(lines)


def build_routing_advisory(text: str, *, max_suggestions: int = 5) -> dict[str, object]:
    """Build non-authoritative routing advisory recommendations.

    The advisory is intentionally weaker than the deterministic KANDA router. It
    may suggest likely route families, hooks, and caution flags, but it never
    decides the final route, never decides May proceed now, and never overrides
    the canon.
    """

    signal_result = score_routing_signals(text)
    signals = signal_result.get("signals", {})
    if not isinstance(signals, Mapping):
        signals = {}

    suggestions = _route_family_suggestions(signals, max_suggestions=max_suggestions)
    caution_flags = _caution_flags(signals)
    recommended_hooks = signal_result.get("recommended_hooks", [])
    if not isinstance(recommended_hooks, Sequence) or isinstance(recommended_hooks, (str, bytes)):
        recommended_hooks = []

    return {
        "schema_version": "1.1",
        "feature_id": ADVISORY_FEATURE_ID,
        "authority": ADVISORY_AUTHORITY,
        "does_not_override_router": True,
        "canon_decides_final_route": True,
        "may_proceed_now_decision": "not_provided_by_advisory",
        "route_override": None,
        "source_diagnostic": signal_result,
        "suggested_route_families": suggestions,
        "recommended_hooks": list(recommended_hooks),
        "caution_flags": caution_flags,
        "advisory_notes": _advisory_notes(suggestions, caution_flags, recommended_hooks),
    }


def summarize_advisory(advisory: Mapping[str, object]) -> str:
    """Build a compact summary for the advisory result."""

    suggestions = advisory.get("suggested_route_families", [])
    if not isinstance(suggestions, Sequence) or isinstance(suggestions, (str, bytes)):
        suggestions = []

    families: list[str] = []
    for item in suggestions:
        if not isinstance(item, Mapping):
            continue
        family = str(item.get("family", ""))
        confidence = str(item.get("confidence", ""))
        if family:
            families.append(family + "(" + confidence + ")")

    hooks = advisory.get("recommended_hooks", [])
    if not isinstance(hooks, Sequence) or isinstance(hooks, (str, bytes)):
        hooks = []

    flags = advisory.get("caution_flags", [])
    if not isinstance(flags, Sequence) or isinstance(flags, (str, bytes)):
        flags = []

    lines = [
        "Routing signal scorer advisory summary",
        "authority=advisory_only",
        "does_not_override_router=True",
        "canon_decides_final_route=True",
        "may_proceed_now_decision=not_provided_by_advisory",
        "suggested_route_families=" + (", ".join(families) if families else "none"),
        "recommended_hooks=" + (", ".join(str(item) for item in hooks) if hooks else "none"),
        "caution_flags=" + (", ".join(str(item) for item in flags) if flags else "none"),
    ]
    return "\n".join(lines)



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
            "route_family_suggestion_eligible": similarity >= SIMILARITY_PROMOTION_THRESHOLD,
            "matched_terms": _matched_terms_from_profiles(query_profile, case_profile),
            "expected_route_families": route_families,
            "matched_route_families": route_families,
            "expected_hooks": list(case.get("expected_hooks") or []),
            "expected_caution_flags": list(case.get("expected_caution_flags") or []),
            "notes": str(case.get("notes") or ""),
        }
        match["explainability"] = _similarity_match_explainability(match)
        matches.append(match)

    matches.sort(key=lambda item: float(item["similarity_score"]), reverse=True)
    matches = matches[:max(1, max_matches)]

    similarity_families = _similarity_route_family_suggestions(matches)
    rule_families = source_advisory.get("suggested_route_families", [])
    if not isinstance(rule_families, Sequence) or isinstance(rule_families, (str, bytes)):
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
        "similarity_decision_report": _similarity_decision_report(matches, recommended_hooks),
        "similarity_decision_report_summary": _similarity_decision_report_summary(),
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
        "suggested_route_families": _merge_route_family_suggestions(rule_families, similarity_families),
        "recommended_hooks": recommended_hooks,
        "caution_flags": caution_flags,
        "similarity_notes": _similarity_notes(matches),
    }


def summarize_similarity_runtime_lite_advisory(advisory: Mapping[str, object]) -> str:
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
        "similar_cases=" + (", ".join(match_parts) if match_parts else "none"),
        "decision_report=" + ("present" if advisory.get("similarity_decision_report") else "none"),
        "recommended_hooks=" + (", ".join(str(item) for item in hooks) if hooks else "none"),
    ]
    return "\n".join(lines)


def build_similarity_ui_preview_adapter(
    text: str,
    *,
    max_matches: int = 3,
    min_similarity: float = SIMILARITY_VISIBILITY_THRESHOLD,
) -> dict[str, object]:
    """Build a GUI/log preview payload for advisory similarity output.

    This adapter is intentionally presentation-only. It formats the existing
    runtime-lite decision report for logs or GUI preview panes without adding
    router authority, prompt-loading behavior, May proceed now decisions, or
    stronger machine-learning behavior.
    """

    advisory = build_similarity_runtime_lite_advisory(
        text,
        max_matches=max_matches,
        min_similarity=min_similarity,
    )
    preview_lines = _similarity_ui_preview_lines(advisory)

    return {
        "schema_version": "2.1",
        "feature_id": SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
        "decision_report_feature_id": SIMILARITY_DECISION_REPORT_FEATURE_ID,
        "source_feature_id": str(advisory.get("feature_id") or ""),
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "adapter_scope": "gui_log_preview_only",
        "preview_format": "plain_text_lines",
        "does_not_override_router": True,
        "canon_decides_final_route": True,
        "may_proceed_now_decision": "not_provided_by_similarity",
        "route_override": None,
        "required_prompts_final_decision": "not_provided_by_similarity",
        "automatic_prompt_loading": False,
        "self_learning_enabled": False,
        "external_dependencies": [],
        "preview_lines": preview_lines,
        "preview_text": "\n".join(preview_lines),
        "source_advisory": advisory,
        "ui_notes": [
            "This preview renders advisory similarity lines only.",
            "The deterministic KANDA routing canon still decides final routing behavior.",
            "The preview must not auto-load prompts or enable Confirm/May-proceed decisions.",
        ],
    }


def render_similarity_ui_preview_text(preview: Mapping[str, object]) -> str:
    """Render a similarity UI preview payload as plain log text."""

    lines = preview.get("preview_lines", [])
    if isinstance(lines, Sequence) and not isinstance(lines, (str, bytes)):
        return "\n".join(str(item) for item in lines)
    return str(preview.get("preview_text") or "")


def build_similarity_prompt_context_preview(
    text: str,
    *,
    max_matches: int = 3,
    min_similarity: float = SIMILARITY_VISIBILITY_THRESHOLD,
) -> dict[str, object]:
    """Build candidate prompt-context preview hints from similarity output.

    This is a display and planning adapter, not a router. It converts advisory
    route-family and hook signals into candidate context labels so a human or
    later deterministic router can inspect likely context needs. It must not
    decide final required prompts, load prompts automatically, or decide May
    proceed now.
    """

    ui_preview = build_similarity_ui_preview_adapter(
        text,
        max_matches=max_matches,
        min_similarity=min_similarity,
    )
    advisory = ui_preview.get("source_advisory", {})
    if not isinstance(advisory, Mapping):
        advisory = {}

    suggestions = advisory.get("suggested_route_families", [])
    if not isinstance(suggestions, Sequence) or isinstance(suggestions, (str, bytes)):
        suggestions = []

    route_families: list[str] = []
    for item in suggestions:
        if not isinstance(item, Mapping):
            continue
        family = str(item.get("family") or "")
        if family and family not in route_families:
            route_families.append(family)

    hooks = advisory.get("recommended_hooks", [])
    if not isinstance(hooks, Sequence) or isinstance(hooks, (str, bytes)):
        hooks = []

    caution_flags = advisory.get("caution_flags", [])
    if not isinstance(caution_flags, Sequence) or isinstance(caution_flags, (str, bytes)):
        caution_flags = []

    candidate_contexts = _candidate_prompt_contexts_for_route_families(route_families, hooks, caution_flags)
    preview_lines = _similarity_prompt_context_preview_lines(route_families, candidate_contexts, hooks, caution_flags)

    return {
        "schema_version": "2.2",
        "feature_id": SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
        "source_feature_id": str(ui_preview.get("feature_id") or ""),
        "decision_report_feature_id": SIMILARITY_DECISION_REPORT_FEATURE_ID,
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "adapter_scope": "candidate_prompt_context_preview_only",
        "preview_format": "plain_text_lines",
        "candidate_contexts_only": True,
        "does_not_override_router": True,
        "canon_decides_final_route": True,
        "may_proceed_now_decision": "not_provided_by_similarity",
        "route_override": None,
        "required_prompts_final_decision": "not_provided_by_similarity",
        "automatic_prompt_loading": False,
        "self_learning_enabled": False,
        "external_dependencies": [],
        "route_family_candidates": route_families,
        "candidate_prompt_contexts": candidate_contexts,
        "recommended_hooks": [str(item) for item in hooks if str(item)],
        "caution_flags": [str(item) for item in caution_flags if str(item)],
        "preview_lines": preview_lines,
        "preview_text": "\n".join(preview_lines),
        "source_ui_preview": ui_preview,
        "context_notes": [
            "Candidate prompt contexts are hints only.",
            "The deterministic KANDA routing canon still decides required prompts and final route.",
            "This adapter must not auto-load prompts or enable May-proceed decisions.",
        ],
    }


def render_similarity_prompt_context_preview_text(preview: Mapping[str, object]) -> str:
    """Render candidate prompt-context preview lines as plain text."""

    lines = preview.get("preview_lines", [])
    if isinstance(lines, Sequence) and not isinstance(lines, (str, bytes)):
        return "\n".join(str(item) for item in lines)
    return str(preview.get("preview_text") or "")


def build_similarity_box_shield_status(text: str = "") -> dict[str, object]:
    """Return the KBSC shield contract for the similarity chain.

    This is an architectural fitness-function payload for the
    ``routing_signal_scorer`` bounded context. It exposes the invariants that
    must remain true before stronger ML, embeddings, TF-IDF, vector stores,
    self-learning, dispatcher automation, or prompt auto-loading are added. It
    is intentionally a shield contract, not a router and not a prompt loader.
    """

    source_text = str(text or "")
    sample_preview = build_similarity_prompt_context_preview(source_text)
    sample_advisory = sample_preview.get("source_ui_preview", {})
    if isinstance(sample_advisory, Mapping):
        runtime_advisory = sample_advisory.get("source_advisory", {})
    else:
        runtime_advisory = {}
    if not isinstance(runtime_advisory, Mapping):
        runtime_advisory = {}

    return {
        "schema_version": "2.3",
        "feature_id": SIMILARITY_BOX_SHIELD_FEATURE_ID,
        "shield_name": "Routing Signal Scorer v2 Similarity Box Shield v1",
        "shield_type": "architectural_fitness_function_suite",
        "owning_bounded_context": "kanda_reasoner_app/routing_signal_scorer",
        "authority": "shield_contract_only",
        "does_not_override_router": True,
        "canon_decides_final_route": True,
        "may_proceed_now_decision": "not_provided_by_similarity",
        "route_override": None,
        "required_prompts_final_decision": "not_provided_by_similarity",
        "automatic_prompt_loading": False,
        "self_learning_enabled": False,
        "external_dependencies": [],
        "stronger_ml_enabled": False,
        "embeddings_enabled": False,
        "tfidf_dependency_enabled": False,
        "vector_store_enabled": False,
        "protected_feature_ids": [
            FEATURE_ID,
            ADVISORY_FEATURE_ID,
            SIMILARITY_RUNTIME_LITE_FEATURE_ID,
            SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
            SIMILARITY_EXPLAINABILITY_FEATURE_ID,
            SIMILARITY_DECISION_REPORT_FEATURE_ID,
            SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
            SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
        ],
        "allowed_public_contracts": [
            "score_routing_signals",
            "summarize_signal_result",
            "build_routing_advisory",
            "summarize_advisory",
            "build_similarity_runtime_lite_advisory",
            "summarize_similarity_runtime_lite_advisory",
            "build_similarity_ui_preview_adapter",
            "render_similarity_ui_preview_text",
            "build_similarity_prompt_context_preview",
            "render_similarity_prompt_context_preview_text",
            "build_similarity_box_shield_status",
            "render_similarity_box_shield_status_text",
        ],
        "forbidden_neighboring_boxes": [
            "kanda_prompt_workspace",
            "kanda_reasoner_app/freeze_hint_intake",
            "kanda_reasoner_app/freeze_after_update",
            "kanda_reasoner_app/freeze_after_update_gui",
            "project_freeze_ledger",
            "project_freeze_after_update",
            "startup_delivery",
            "prompt_library_runtime_loading",
        ],
        "dependency_direction_rule": (
            "routing_signal_scorer may expose advisory data outward through its "
            "public contract, but must not import, mutate, or decide for prompt "
            "library, freeze, GUI, startup, or project-memory boxes."
        ),
        "truth_source_priority_ladder": [
            "deterministic KANDA routing canon decides final route, required prompts, missing context, and May proceed now",
            "routing_signal_scorer similarity chain provides advisory evidence only",
            "runtime-lite corpus anchors provide deterministic lexical hints only",
            "UI and prompt-context previews display candidate evidence only",
        ],
        "protected_architecture_characteristics": [
            "advisory_only",
            "deterministic",
            "side_effect_free",
            "bounded_execution",
            "schema_validated_output",
            "no_authority_escalation",
            "no_cross_box_mutation",
            "stdlib_only_runtime_lite",
            "candidate_context_only",
            "presentation_only_ui_preview",
        ],
        "forbidden_authority_fields": [
            "final_route",
            "may_proceed",
            "may_proceed_now",
            "required_prompts",
            "required_prompt_files",
            "auto_load_prompts",
            "load_prompts_now",
            "router_override",
            "freeze_write",
            "startup_mutation",
            "prompt_library_mutation",
        ],
        "state_machine": {
            "NO_MATCH": "No visible similarity case; advisory output still contains no authority.",
            "WEAK_MATCH": "Visible-low match; not eligible for route-family suggestion promotion.",
            "STRONG_ADVISORY": "Promoted-medium match; still advisory and candidate-only.",
            "HIGH_SIGNAL": "High similarity anchor; still no final route, prompt, or May-proceed authority.",
            "AMBIGUOUS_MATCH": "Close competing anchors must be treated as ambiguous advisory evidence.",
            "ERROR_STATE": "Malformed input must degrade to deterministic safe advisory output, not authority.",
        },
        "regression_matrix": [
            "SM-25 deterministic snapshot baseline",
            "SM-26 idempotency",
            "SM-27 ambiguous match visibility without authority",
            "SM-28 error resilience",
            "SM-29 forbidden authority fields absent",
            "SM-30 schema version and feature id",
            "SM-31 no placeholder commitment",
            "SM-32 input sanitization boundary",
            "SM-33 no side effects",
            "SM-34 dependency ceiling",
            "SM-35 decision report language guard",
            "SM-36 candidate label control",
            "SM-37 high-score authority cap",
            "SM-38 box invasion audit",
            "SM-39 bounded execution/model-DoS guard",
            "SM-40 no actionable command surface",
            "SM-41 OWASP-style threat coverage declaration",
            "SM-42 KANDA scorer shield card exists",
            "SM-43 stdlib-only fuzz/property loop",
            "SM-44 runtime forbidden dependency scan",
            "SM-45 dependency direction guard",
            "SM-46 architecture fitness metadata",
            "SM-47 bounded context map",
            "SM-48 trade-off record",
            "SM-49 public-contract-only integration",
        ],
        "sample_input_length": len(source_text),
        "sample_preview_feature_id": str(sample_preview.get("feature_id") or ""),
        "sample_runtime_feature_id": str(runtime_advisory.get("feature_id") or ""),
        "sample_candidate_context_count": len(sample_preview.get("candidate_prompt_contexts", []))
        if isinstance(sample_preview.get("candidate_prompt_contexts", []), Sequence)
        else 0,
        "shield_notes": [
            "This shield freezes the current runtime-lite similarity chain boundary before stronger ML.",
            "The shield does not add embeddings, TF-IDF, vector stores, or self-learning.",
            "The shield does not auto-load prompts or decide May proceed now.",
            "The shield belongs only to kanda_reasoner_app/routing_signal_scorer.",
        ],
    }


def render_similarity_box_shield_status_text(status: Mapping[str, object]) -> str:
    """Render the similarity box shield status as compact plain text."""

    feature_id = str(status.get("feature_id") or "")
    characteristics = status.get("protected_architecture_characteristics", [])
    if not isinstance(characteristics, Sequence) or isinstance(characteristics, (str, bytes)):
        characteristics = []
    forbidden_boxes = status.get("forbidden_neighboring_boxes", [])
    if not isinstance(forbidden_boxes, Sequence) or isinstance(forbidden_boxes, (str, bytes)):
        forbidden_boxes = []
    return "\n".join(
        [
            "Routing Signal Scorer v2 Similarity Box Shield",
            "feature_id=" + feature_id,
            "shield_type=" + str(status.get("shield_type") or ""),
            "owning_bounded_context=" + str(status.get("owning_bounded_context") or ""),
            "authority=" + str(status.get("authority") or ""),
            "does_not_override_router=" + str(status.get("does_not_override_router") is True),
            "canon_decides_final_route=" + str(status.get("canon_decides_final_route") is True),
            "may_proceed_now_decision=" + str(status.get("may_proceed_now_decision") or ""),
            "required_prompts_final_decision=" + str(status.get("required_prompts_final_decision") or ""),
            "automatic_prompt_loading=" + str(status.get("automatic_prompt_loading") is True),
            "self_learning_enabled=" + str(status.get("self_learning_enabled") is True),
            "stronger_ml_enabled=" + str(status.get("stronger_ml_enabled") is True),
            "external_dependencies=none",
            "protected_architecture_characteristics=" + (", ".join(str(item) for item in characteristics) if characteristics else "none"),
            "forbidden_neighboring_boxes=" + (", ".join(str(item) for item in forbidden_boxes) if forbidden_boxes else "none"),
            "shield_note=architectural fitness-function suite only; no routing authority",
        ]
    )


def _candidate_prompt_contexts_for_route_families(
    route_families: Sequence[str],
    hooks: Sequence[object],
    caution_flags: Sequence[object],
) -> list[dict[str, object]]:
    candidate_map: dict[str, tuple[str, ...]] = {
        "fast_path_simple_explanation": (
            "fast_path_explanation_only_candidate",
        ),
        "patch_delivery_or_code_update": (
            "05_patch_delivery_and_validation_candidate",
            "08_python_engineering_core_candidate",
            "09_python_quality_security_observability_candidate",
        ),
        "terminal_install_artifact": (
            "pre_output_contract_gates_candidate",
            "05_patch_delivery_and_validation_candidate",
        ),
        "validation_artifact": (
            "pre_output_contract_gates_candidate",
            "05_patch_delivery_and_validation_candidate",
        ),
        "freeze_form_json_artifact": (
            "pre_output_contract_gates_candidate",
            "freeze_code_intake_and_form_protocol_candidate",
        ),
        "freeze_memory_workflow": (
            "freeze_code_intake_and_form_protocol_candidate",
            "09_active_project_freeze_context_candidate",
        ),
        "freeze_hint_sidecar_or_intake": (
            "freeze_code_intake_and_form_protocol_candidate",
            "pre_output_contract_gates_candidate",
        ),
        "prompt_library_or_routing_update": (
            "07_prompt_authoring_and_audit_candidate",
            "02_prompt_routing_and_indexing_candidate",
        ),
        "startup_delivery_update": (
            "paste_if_modify_startup_delivery_candidate",
            "startup_delivery_maintenance_protocol_candidate",
        ),
        "ambiguous_request_needs_router_check": (
            "router_context_check_candidate",
            "ask_for_or_inspect_required_context_candidate",
        ),
        "external_project_root_sensitive": (
            "active_project_root_boundary_check_candidate",
            "pre_output_contract_gates_candidate",
        ),
    }

    contexts: list[dict[str, object]] = []
    seen: set[str] = set()
    for family in route_families:
        for label in candidate_map.get(str(family), ()):
            if label in seen:
                continue
            seen.add(label)
            contexts.append(
                {
                    "context_label": label,
                    "source_route_family": str(family),
                    "candidate_only": True,
                    "final_required_prompt_decision": "not_provided_by_similarity",
                    "automatic_prompt_loading": False,
                    "reason": "Candidate context derived from advisory route-family preview.",
                }
            )

    for hook in hooks:
        value = str(hook or "")
        if value != PRE_OUTPUT_HOOK or "pre_output_contract_gates_candidate" in seen:
            continue
        seen.add("pre_output_contract_gates_candidate")
        contexts.append(
            {
                "context_label": "pre_output_contract_gates_candidate",
                "source_route_family": "recommended_hook",
                "candidate_only": True,
                "final_required_prompt_decision": "not_provided_by_similarity",
                "automatic_prompt_loading": False,
                "reason": "High-risk advisory hook should be visible before artifact output.",
            }
        )

    for flag in caution_flags:
        value = str(flag or "")
        if value == "startup_delivery_governance_needed" and "paste_if_modify_startup_delivery_candidate" not in seen:
            seen.add("paste_if_modify_startup_delivery_candidate")
            contexts.append(
                {
                    "context_label": "paste_if_modify_startup_delivery_candidate",
                    "source_route_family": "caution_flag",
                    "candidate_only": True,
                    "final_required_prompt_decision": "not_provided_by_similarity",
                    "automatic_prompt_loading": False,
                    "reason": "Startup delivery caution flag surfaced by advisory diagnostics.",
                }
            )

    return contexts


def _similarity_prompt_context_preview_lines(
    route_families: Sequence[str],
    candidate_contexts: Sequence[Mapping[str, object]],
    hooks: Sequence[object],
    caution_flags: Sequence[object],
) -> list[str]:
    labels = [str(item.get("context_label") or "") for item in candidate_contexts if isinstance(item, Mapping)]
    labels = [item for item in labels if item]
    route_text = ", ".join(str(item) for item in route_families if str(item)) or "none"
    label_text = ", ".join(labels) if labels else "none"
    hook_text = ", ".join(str(item) for item in hooks if str(item)) or "none"
    flag_text = ", ".join(str(item) for item in caution_flags if str(item)) or "none"

    return [
        "Routing Signal Scorer v2 Prompt Context Preview",
        "feature_id=" + SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
        "adapter_scope=candidate_prompt_context_preview_only",
        "authority=advisory_only",
        "candidate_contexts_only=True",
        "does_not_override_router=True",
        "canon_decides_final_route=True",
        "may_proceed_now_decision=not_provided_by_similarity",
        "route_override=None",
        "required_prompts_final_decision=not_provided_by_similarity",
        "automatic_prompt_loading=False",
        "self_learning_enabled=False",
        "external_dependencies=none",
        "route_family_candidates=" + route_text,
        "candidate_prompt_contexts=" + label_text,
        "recommended_hooks=" + hook_text,
        "caution_flags=" + flag_text,
        "preview_note=candidate contexts are not final required prompts",
        "preview_note=the canon decides required prompts, final route, missing context, and May proceed now",
    ]


def _similarity_ui_preview_lines(advisory: Mapping[str, object]) -> list[str]:
    report = advisory.get("similarity_decision_report", [])
    if not isinstance(report, Sequence) or isinstance(report, (str, bytes)):
        report = []

    lines = [
        "Routing Signal Scorer v2 Similarity Preview",
        "feature_id=" + SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
        "adapter_scope=gui_log_preview_only",
        "authority=advisory_only",
        "does_not_override_router=True",
        "canon_decides_final_route=True",
        "may_proceed_now_decision=not_provided_by_similarity",
        "route_override=None",
        "required_prompts_final_decision=not_provided_by_similarity",
        "automatic_prompt_loading=False",
        "self_learning_enabled=False",
        "external_dependencies=none",
        "decision_report_begin",
    ]
    lines.extend(str(item) for item in report)
    lines.extend(
        [
            "decision_report_end",
            "preview_note=advisory only; display this in logs or GUI preview panes only",
            "preview_note=the canon decides required prompts, final route, missing context, and May proceed now",
        ]
    )
    return lines


def _load_similarity_corpus() -> dict[str, object]:
    corpus_path = (
        Path(__file__).resolve().parent
        / "design"
        / "routing_signal_scorer_v2_similarity_test_corpus.json"
    )
    data = json.loads(corpus_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"cases": []}
    return data


def _text_profile(text: str) -> dict[str, set[str]]:
    tokens = _tokenize_for_similarity(text)
    bigrams = {tokens[index] + " " + tokens[index + 1] for index in range(max(0, len(tokens) - 1))}
    return {
        "tokens": set(tokens),
        "bigrams": bigrams,
    }


def _tokenize_for_similarity(text: str) -> list[str]:
    raw = re.findall(r"[a-z0-9_]+", str(text or "").lower())
    stop_words = {
        "a", "an", "and", "are", "as", "be", "by", "for", "from", "give",
        "i", "if", "in", "include", "is", "it", "me", "must", "of", "on",
        "or", "the", "this", "to", "use", "what", "when", "with", "you",
    }
    return [item for item in raw if len(item) > 1 and item not in stop_words]


def _profile_similarity(left: Mapping[str, set[str]], right: Mapping[str, set[str]]) -> float:
    left_tokens = set(left.get("tokens", set()))
    right_tokens = set(right.get("tokens", set()))
    left_bigrams = set(left.get("bigrams", set()))
    right_bigrams = set(right.get("bigrams", set()))

    token_score = _jaccard(left_tokens, right_tokens)
    bigram_score = _jaccard(left_bigrams, right_bigrams)
    containment = _containment(left_tokens, right_tokens)
    return (0.5 * token_score) + (0.25 * bigram_score) + (0.25 * containment)


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _containment(query: set[str], candidate: set[str]) -> float:
    if not query or not candidate:
        return 0.0
    return len(query & candidate) / len(query)


def _similarity_level(value: float) -> str:
    if value >= SIMILARITY_HIGH_THRESHOLD:
        return "high"
    if value >= SIMILARITY_PROMOTION_THRESHOLD:
        return "medium"
    return "low"


def _similarity_threshold_level(value: float) -> str:
    if value < SIMILARITY_VISIBILITY_THRESHOLD:
        return "hidden"
    if value < SIMILARITY_PROMOTION_THRESHOLD:
        return "visible_low"
    if value < SIMILARITY_HIGH_THRESHOLD:
        return "promoted_medium"
    return "high"


def _similarity_advisory_only_reason() -> str:
    return (
        "Similarity matches are corpus anchors only. The deterministic KANDA "
        "routing canon decides final route, required prompts, and May proceed now."
    )


def _similarity_rule_hook_independence_reason() -> str:
    return (
        "Rule-based diagnostic hooks remain independent of similarity matches; "
        "high-risk patch, freeze, terminal, and project-root signals still come "
        "from rule diagnostics and governed pre-output gates."
    )


def _similarity_match_explainability(match: Mapping[str, object]) -> dict[str, object]:
    score = _coerce_score(match.get("similarity_score", 0.0))
    route_families = match.get("matched_route_families", [])
    if not isinstance(route_families, Sequence) or isinstance(route_families, (str, bytes)):
        route_families = []
    return {
        "feature_id": SIMILARITY_EXPLAINABILITY_FEATURE_ID,
        "matched_corpus_item_id": str(match.get("matched_corpus_item_id") or match.get("case_id") or ""),
        "matched_route_families": [str(item) for item in route_families],
        "similarity_score": round(score, 3),
        "threshold_level": _similarity_threshold_level(score),
        "route_family_suggestion_eligible": score >= SIMILARITY_PROMOTION_THRESHOLD,
        "threshold_policy_feature_id": SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
        "authority": SIMILARITY_RUNTIME_LITE_AUTHORITY,
        "does_not_override_router": True,
        "may_proceed_now_decision": "not_provided_by_similarity",
        "final_route_decision": "not_provided_by_similarity",
        "advisory_only_reason": _similarity_advisory_only_reason(),
        "rule_hook_independence": _similarity_rule_hook_independence_reason(),
    }


def _similarity_explainability_summary() -> dict[str, object]:
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
        if not isinstance(route_families, Sequence) or isinstance(route_families, (str, bytes)):
            route_families = []
        family_text = ", ".join(str(item) for item in route_families if str(item)) or "none"
        lines.extend(
            [
                "top_match=" + str(top_match.get("matched_corpus_item_id") or top_match.get("case_id") or ""),
                "top_match_score=" + f"{score:.3f}",
                "top_match_threshold_level=" + _similarity_threshold_level(score),
                "route_family_suggestion_eligible=" + str(score >= SIMILARITY_PROMOTION_THRESHOLD),
                "matched_route_families=" + family_text,
            ]
        )

    hooks = [str(item) for item in recommended_hooks if str(item)]
    lines.extend(
        [
            "advisory_only_reason=" + _similarity_advisory_only_reason(),
            "rule_hook_independence=" + _similarity_rule_hook_independence_reason(),
            "recommended_hooks=" + (", ".join(hooks) if hooks else "none"),
        ]
    )
    return lines


def _similarity_threshold_policy() -> dict[str, object]:
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


def _matched_terms_from_profiles(left: Mapping[str, set[str]], right: Mapping[str, set[str]], limit: int = 8) -> list[str]:
    terms = sorted(set(left.get("tokens", set())) & set(right.get("tokens", set())))
    return terms[:limit]


def _similarity_route_family_suggestions(matches: Sequence[Mapping[str, object]]) -> list[dict[str, object]]:
    suggestions: list[dict[str, object]] = []
    seen: set[str] = set()
    for match in matches:
        score = _coerce_score(match.get("similarity_score", 0.0))
        if score < SIMILARITY_PROMOTION_THRESHOLD:
            continue
        families = match.get("expected_route_families", [])
        if not isinstance(families, Sequence) or isinstance(families, (str, bytes)):
            continue
        for family in families:
            family_text = str(family)
            if not family_text or family_text in seen:
                continue
            seen.add(family_text)
            suggestions.append(
                {
                    "family": family_text,
                    "confidence": _similarity_level(score),
                    "score": round(score, 3),
                    "source_signal": "similarity_runtime_lite",
                    "source_case_id": str(match.get("case_id") or ""),
                    "matched_corpus_item_id": str(match.get("matched_corpus_item_id") or match.get("case_id") or ""),
                    "threshold_level": _similarity_threshold_level(score),
                    "advisory_only_reason": _similarity_advisory_only_reason(),
                    "rule_hook_independence": _similarity_rule_hook_independence_reason(),
                    "reason": "Similar frozen corpus scenario detected. Advisory only.",
                }
            )
    return suggestions


def _similarity_expected_values(matches: Sequence[Mapping[str, object]], key: str) -> list[str]:
    values: list[str] = []
    for match in matches:
        if _coerce_score(match.get("similarity_score", 0.0)) < SIMILARITY_PROMOTION_THRESHOLD:
            continue
        raw_values = match.get(key, [])
        if not isinstance(raw_values, Sequence) or isinstance(raw_values, (str, bytes)):
            continue
        values.extend(str(item) for item in raw_values if str(item))
    return values


def _merge_string_lists(*items: object) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in items:
        if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
            continue
        for item in raw:
            value = str(item)
            if not value or value in seen:
                continue
            seen.add(value)
            result.append(value)
    return result


def _merge_route_family_suggestions(*groups: object) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    seen: set[str] = set()
    for group in groups:
        if not isinstance(group, Sequence) or isinstance(group, (str, bytes)):
            continue
        for item in group:
            if not isinstance(item, Mapping):
                continue
            family = str(item.get("family") or "")
            if not family or family in seen:
                continue
            seen.add(family)
            result.append(dict(item))
    return result


def _similarity_notes(matches: Sequence[Mapping[str, object]]) -> list[str]:
    notes = [
        "Runtime-lite similarity is advisory only and must not replace deterministic KANDA routing.",
        "The canon decides final route, required prompts, missing context, and May proceed now.",
        "No embeddings, TF-IDF dependency, vector store, self-learning, or cross-project memory is used.",
    ]
    if matches:
        notes.append("Similar corpus cases are scenario anchors, not final route decisions.")
    else:
        notes.append("No corpus case met the conservative similarity threshold.")
    return notes

def _rules() -> tuple[SignalRule, ...]:
    return (
        SignalRule(
            "fast_path_simple_explanation",
            0.8,
            (
                "explain in simple terms",
                "simple explanation",
                "no patch",
                "no code",
                "just explain",
                "explain what",
                "what does",
                "help me understand",
            ),
            "Simple explanation wording detected.",
        ),
        SignalRule(
            "governed_prompt_library_update",
            0.8,
            (
                "create a prompt",
                "add a prompt",
                "register a prompt",
                "prompt library",
                "active_prompts",
                "prompt_navigation_index",
                "group_assimilation_index",
                "folder_assimilation",
                "metadata",
            ),
            "Prompt-library or routing-index update wording detected.",
        ),
        SignalRule(
            "patch_delivery",
            0.8,
            (
                "patch zip",
                "create patch",
                "deliver patch",
                "install block",
                "validation block",
                "download the zip",
                "save the zip",
                "extract fresh",
                "delete_after_daily_work",
            ),
            "Patch delivery wording detected.",
        ),
        SignalRule(
            "terminal_install_output",
            0.7,
            (
                "powershell",
                "$project_root",
                "copy-item",
                "move-item",
                "expand-archive",
                "install ok",
                "install failed",
                "start-sleep",
                "clear-host",
            ),
            "Terminal or PowerShell install artifact wording detected.",
        ),
        SignalRule(
            "terminal_validation_output",
            0.75,
            (
                "validation ok",
                "validation failed",
                "contract_test_ok",
                "status: in_sync",
                "py_compile",
                "python tests",
                "run validation",
                "validate",
            ),
            "Validation artifact wording detected.",
        ),
        SignalRule(
            "freeze_form_json",
            0.9,
            (
                "kanda_freeze_form_json_begin",
                "kanda_freeze_form_json_end",
                "freeze-form json",
                "freeze form json",
                "formulary",
                "validation_evidence_summary",
            ),
            "Freeze-form JSON wording detected.",
        ),
        SignalRule(
            "freeze_hint_sidecar",
            0.85,
            (
                "kanda_freeze_hint.json",
                "freeze hint",
                "sidecar",
                "freeze-intake",
                "freeze_hint_intake",
                "latest_freeze_hint.json",
            ),
            "Freeze hint sidecar or intake wording detected.",
        ),
        SignalRule(
            "freeze_memory_write",
            0.8,
            (
                "confirm and write",
                "frozen_features_memory",
                "freeze entry",
                "freeze code",
                "freeze a validated feature",
                "local freeze",
                "preview freeze entry",
            ),
            "Freeze memory or local freeze workflow wording detected.",
        ),
        SignalRule(
            "external_project_root_sensitive",
            0.8,
            (
                "active project root",
                "selected active project",
                "<any_project>",
                "any_project",
                "project_freeze_after_update",
                "do not hardcode",
                "hardcode e:",
                "multiple projects",
            ),
            "Multi-project or active-project-root sensitive wording detected.",
        ),
        SignalRule(
            "ambiguous_or_needs_router_context",
            0.55,
            (
                "go",
                "continue",
                "do it",
                "update logic",
                "fix logic",
                "correct it",
                "not sure",
                "maybe",
            ),
            "Ambiguous or broad implementation wording detected.",
        ),
        SignalRule(
            "confirmation_gate_bypass_risk",
            0.9,
            (
                "without asking me to confirm",
                "without confirm",
                "bypass confirmation",
                "automatically write local freeze",
                "remove confirm and write",
                "skip confirm",
            ),
            "Possible protected confirmation-gate bypass wording detected.",
        ),
        SignalRule(
            "startup_delivery_change",
            0.8,
            (
                "paste_after_first_prompts_to_ai.md",
                "paste_after_uploading_startup_zip.md",
                "startup zip",
                "first_prompts_to_ai.zip",
                "sync_startup_routing_kernel_pack.py",
                "startup delivery",
                "startup routing kernel",
            ),
            "Startup delivery or startup routing kernel wording detected.",
        ),
    )


def _apply_combination_rules(
    normalized: str,
    scores: dict[str, float],
    evidence: dict[str, list[str]],
    notes: list[str],
    max_evidence_per_signal: int,
) -> None:
    high_risk = any(scores[name] >= 0.3 for name in PRE_OUTPUT_TRIGGER_SIGNALS)
    if high_risk:
        _add_score(scores, "pre_output_contract_gate_required", 0.9)
        _add_evidence(
            evidence,
            "pre_output_contract_gate_required",
            "high-risk artifact signal detected",
            max_evidence_per_signal,
        )
        notes.append("Pre-output contract gate is recommended before final artifact output.")

    if scores["fast_path_simple_explanation"] > 0.0 and high_risk:
        _add_score(scores, "fast_path_simple_explanation", -0.5)
        notes.append("Fast Path explanation signal was reduced because high-risk artifact signals are present.")

    if scores["confirmation_gate_bypass_risk"] >= 0.7:
        _add_score(scores, "freeze_memory_write", 0.4)
        _add_score(scores, "external_project_root_sensitive", 0.2)
        _add_score(scores, "pre_output_contract_gate_required", 0.3)

    if scores["startup_delivery_change"] >= 0.7:
        _add_score(scores, "governed_prompt_library_update", 0.7)
        _add_score(scores, "pre_output_contract_gate_required", 0.2)

    if re.search(r"\brg-?0?2[89]\b", normalized):
        _add_score(scores, "ambiguous_or_needs_router_context", 0.2)
        _add_evidence(evidence, "ambiguous_or_needs_router_context", "RG-028/RG-029 style route", max_evidence_per_signal)


def _route_family_suggestions(
    signals: Mapping[str, object],
    *,
    max_suggestions: int,
) -> list[dict[str, object]]:
    candidates = (
        (
            "fast_path_simple_explanation",
            "fast_path_simple_explanation",
            "Likely explanation-only request. Deterministic router should still verify no governed artifact is requested.",
        ),
        (
            "patch_delivery",
            "patch_delivery_or_code_update",
            "Patch or ZIP delivery language detected. Pre-output contract gates are likely relevant.",
        ),
        (
            "terminal_install_output",
            "terminal_install_artifact",
            "PowerShell or install artifact language detected. Terminal output contract should be checked.",
        ),
        (
            "terminal_validation_output",
            "validation_artifact",
            "Validation output language detected. Validation terminal contract and evidence markers should be checked.",
        ),
        (
            "freeze_form_json",
            "freeze_form_json_artifact",
            "Freeze-form JSON language detected. Strict marker and JSON contract should be checked.",
        ),
        (
            "freeze_hint_sidecar",
            "freeze_hint_sidecar_or_intake",
            "KANDA_FREEZE_HINT or intake language detected. Current-feature sidecar contract should be checked.",
        ),
        (
            "freeze_memory_write",
            "freeze_memory_workflow",
            "Freeze memory language detected. Human confirmation and project-local memory boundaries should be checked.",
        ),
        (
            "governed_prompt_library_update",
            "prompt_library_or_routing_update",
            "Prompt-library or routing-index language detected. Prompt governance should be checked.",
        ),
        (
            "startup_delivery_change",
            "startup_delivery_update",
            "Startup delivery language detected. Startup maintenance protocol should be checked.",
        ),
        (
            "external_project_root_sensitive",
            "multi_project_path_sensitive",
            "Active project root language detected. Multi-project path canon should be checked.",
        ),
        (
            "confirmation_gate_bypass_risk",
            "protected_confirmation_gate_risk",
            "Possible attempt to bypass Confirm and Write or another human confirmation gate.",
        ),
        (
            "ambiguous_or_needs_router_context",
            "ambiguous_request_needs_router_check",
            "Broad or ambiguous wording detected. Deterministic router should ask for or inspect required context.",
        ),
    )

    suggestions: list[dict[str, object]] = []
    for signal_name, family, reason in candidates:
        score = _coerce_score(signals.get(signal_name, 0.0))
        if score < 0.3:
            continue
        suggestions.append(
            {
                "family": family,
                "confidence": _level(score),
                "score": round(score, 3),
                "source_signal": signal_name,
                "reason": reason,
            }
        )

    suggestions.sort(key=lambda item: float(item["score"]), reverse=True)
    return suggestions[:max(1, max_suggestions)]


def _caution_flags(signals: Mapping[str, object]) -> list[str]:
    flags: list[str] = []

    if _coerce_score(signals.get("confirmation_gate_bypass_risk", 0.0)) >= 0.7:
        flags.append("confirmation_gate_bypass_risk")
    if _coerce_score(signals.get("external_project_root_sensitive", 0.0)) >= 0.7:
        flags.append("multi_project_path_sensitive")
    if _coerce_score(signals.get("pre_output_contract_gate_required", 0.0)) >= 0.7:
        flags.append("pre_output_contract_gate_recommended")
    if _coerce_score(signals.get("startup_delivery_change", 0.0)) >= 0.7:
        flags.append("startup_delivery_governance_needed")
    if _coerce_score(signals.get("governed_prompt_library_update", 0.0)) >= 0.7:
        flags.append("prompt_library_governance_needed")
    if _coerce_score(signals.get("fast_path_simple_explanation", 0.0)) >= 0.7:
        flags.append("fast_path_candidate_only")

    return flags


def _advisory_notes(
    suggestions: Sequence[object],
    caution_flags: Sequence[object],
    recommended_hooks: Sequence[object],
) -> list[str]:
    notes = [
        "Advisory output is non-authoritative and must not replace deterministic KANDA routing.",
        "The canon decides final route, required prompts, missing context, and May proceed now.",
    ]
    if suggestions:
        notes.append("Use suggestions as pre-router hints only.")
    if caution_flags:
        notes.append("Caution flags identify risks to re-check before implementation or artifact output.")
    if recommended_hooks:
        notes.append("Recommended hooks should be requested or applied only when the governing prompt canon allows it.")
    return notes


def _coerce_score(value: object) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _recommended_hooks(scores: Mapping[str, float]) -> list[str]:
    hooks: list[str] = []
    if float(scores.get("pre_output_contract_gate_required", 0.0)) >= 0.7:
        hooks.append(PRE_OUTPUT_HOOK)
    return hooks


def _normalize(text: str) -> str:
    lowered = text.lower()
    return re.sub(r"\s+", " ", lowered).strip()


def _matched_patterns(normalized: str, patterns: Iterable[str]) -> list[str]:
    matches: list[str] = []
    for pattern in patterns:
        needle = pattern.lower().strip()
        if not needle:
            continue
        if needle in normalized:
            matches.append(pattern)
    return matches


def _add_score(scores: dict[str, float], signal: str, value: float) -> None:
    if signal not in scores:
        return
    scores[signal] = max(0.0, min(1.0, scores[signal] + value))


def _add_evidence(
    evidence: dict[str, list[str]],
    signal: str,
    item: str,
    max_items: int,
) -> None:
    if signal not in evidence:
        return
    if item in evidence[signal]:
        return
    if len(evidence[signal]) >= max_items:
        return
    evidence[signal].append(item)


def _level(value: float) -> str:
    if value >= 0.7:
        return "high"
    if value >= 0.3:
        return "medium"
    return "low"


def _excerpt(text: str, limit: int = 240) -> str:
    compact = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
