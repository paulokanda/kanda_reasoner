# project-path: kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_session_capture.py
"""Runtime capture adapter for Prompt Router Reasoner.

This module bridges the existing SessionService execution flow to the
Prompt Router Reasoner shadow review store. It records the authoritative
heuristic/default prompt snapshot and a deterministic advisory ML/context
snapshot for later human review, while returning the original SessionService
result unchanged.

Authority boundary:
- no final router or prompt-selection mutation;
- no provider calls;
- no prompt-library writes;
- no freeze-memory writes;
- ML/context preview remains advisory-only evidence.
"""

from __future__ import annotations


__all__ = [
    'build_heuristic_prompt_snapshot',
    'build_ml_advisory_prompt_context_snapshot',
    'capture_session_prompt_router_reasoner_review',
    'summarize_session_capture_result',
]
import json
import re
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    PromptSnapshot,
    ROUTER_WITH_HEURISTICS,
    compact_generator_text,
    sha256_text,
)
from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_shadow_bridge import (
    ShadowBridgeCaptureResult,
    capture_shadow_prompt_selection,
)

SESSION_CAPTURE_SCHEMA_VERSION = "1.0"
SESSION_CAPTURE_FEATURE_ID = "prompt_router_reasoner_session_service_runtime_capture_wiring_v1"
ML_CONTEXT_PREVIEW_VERSION = "routing_signal_scorer_similarity_prompt_context_preview_shadow_v1"
HEURISTIC_PROMPT_VERSION = "session_service_authoritative_prompt_snapshot_v1"


def capture_session_prompt_router_reasoner_review(
    *,
    project_root: str | Path | None,
    question: str,
    decision: Any,
    bundle: Any,
    prompt: str,
    final_session_result: Any,
    selected_model: str = "",
    prefer_code: bool = False,
    verbosity: str = "",
    enabled: bool = True,
) -> ShadowBridgeCaptureResult:
    """Capture one runtime review row and return the bridge result.

    The final SessionExecutionResult object is passed through the shadow bridge
    as final_router_output. Callers should continue returning the original
    result object; this adapter is observation-only.
    """
    heuristic_snapshot = build_heuristic_prompt_snapshot(
        question=question,
        decision=decision,
        bundle=bundle,
        prompt=prompt,
        selected_model=selected_model,
        prefer_code=prefer_code,
        verbosity=verbosity,
    )
    ml_snapshot = build_ml_advisory_prompt_context_snapshot(question=question)
    return capture_shadow_prompt_selection(
        full_generator_text=question,
        short_generator_text=compact_generator_text(question),
        heuristic_prompt=heuristic_snapshot,
        ml_prompt=ml_snapshot,
        final_router_output=final_session_result,
        project_root=project_root,
        enabled=enabled,
        router_mode_at_capture=ROUTER_WITH_HEURISTICS,
        app_version=SESSION_CAPTURE_FEATURE_ID,
        router_version=_decision_text(decision, "route") + ":" + _decision_text(decision, "intent_name"),
        retriever_version="session_service_retrieval_bundle_snapshot_v1",
        ml_version=ML_CONTEXT_PREVIEW_VERSION,
        prompt_library_version="prompt_builder_final_prompt_hash",
        safety_violation=False,
        notes=(
            "Runtime capture wiring only. Heuristic prompt snapshot is the authoritative "
            "SessionService/prompt_builder output. ML snapshot is deterministic local "
            "advisory prompt-context preview from routing_signal_scorer; it is not a router."
        ),
    )


def build_heuristic_prompt_snapshot(
    *,
    question: str,
    decision: Any,
    bundle: Any,
    prompt: str,
    selected_model: str = "",
    prefer_code: bool = False,
    verbosity: str = "",
) -> PromptSnapshot:
    """Build the authoritative heuristic/default prompt snapshot."""
    route = _decision_text(decision, "route") or "unknown_route"
    intent = _decision_text(decision, "intent_name") or "unknown_intent"
    reason = _decision_text(decision, "reason") or "No router reason recorded."
    file_count = len(list(getattr(bundle, "file_evidence", []) or []))
    symbol_count = len(list(getattr(bundle, "symbol_evidence", []) or []))
    snippet_count = len(list(getattr(bundle, "snippet_evidence", []) or []))
    prompt_text = str(prompt or "")
    hash_source = json.dumps(
        {
            "question_hash": sha256_text(str(question or "")),
            "route": route,
            "intent": intent,
            "prompt": prompt_text,
            "file_count": file_count,
            "symbol_count": symbol_count,
            "snippet_count": snippet_count,
        },
        sort_keys=True,
        ensure_ascii=True,
    )
    return PromptSnapshot(
        prompt_id="heuristic_session_prompt_" + _safe_identifier(route + "_" + intent),
        prompt_name="Heuristic/default SessionService prompt: " + route,
        prompt_path="kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/session_service.py::SessionService.execute",
        prompt_hash=sha256_text(hash_source),
        prompt_summary=(
            "Authoritative prompt/result assembled by the existing deterministic SessionService "
            "flow for route " + route + " and intent " + intent + "."
        ),
        prompt_group="reasoner_engine",
        prompt_version=HEURISTIC_PROMPT_VERSION,
        score=float(file_count + symbol_count + snippet_count),
        confidence=None,
        explanation=(
            "The current heuristic/default flow selected this route and assembled the final "
            "prompt using route_query_intent, retriever evidence, and PromptBuilder. "
            "Router reason: " + reason
        ),
        keywords=tuple(
            item
            for item in (
                route,
                intent,
                "prefer_code" if prefer_code else "prefer_prose",
                "verbosity=" + str(verbosity or ""),
                "model=" + str(selected_model or ""),
            )
            if item
        ),
        route=route,
        semantic_match="authoritative_deterministic_session_service_flow",
        inferred_intent=intent,
        disagreement_reason="Heuristics remain authoritative; this is the baseline candidate.",
        safety_status="authoritative_heuristic_baseline",
    )


def build_ml_advisory_prompt_context_snapshot(*, question: str) -> PromptSnapshot:
    """Build an advisory ML/context snapshot using local deterministic scorer data.

    The underlying scorer is runtime-lite lexical similarity and routing advisory
    evidence. It is used here as the current shadow ML/context candidate source
    and never as a final router or prompt loader.
    """
    preview: dict[str, Any]
    try:
        from kanda_reasoner_app.routing_signal_scorer.contract import (  # noqa: PLC0415
            build_similarity_prompt_context_preview,
        )

        loaded = build_similarity_prompt_context_preview(str(question or ""))
        preview = dict(loaded) if isinstance(loaded, Mapping) else {}
    except Exception as exc:  # pragma: no cover - defensive runtime fail-open data
        preview = {
            "schema_version": "fallback",
            "feature_id": "routing_signal_scorer_unavailable",
            "candidate_prompt_contexts": [],
            "route_family_candidates": [],
            "recommended_hooks": [],
            "caution_flags": ["advisory_preview_unavailable"],
            "preview_text": "Advisory preview unavailable: " + str(exc),
        }

    contexts = preview.get("candidate_prompt_contexts", [])
    if not isinstance(contexts, list):
        contexts = []
    first_context = contexts[0] if contexts and isinstance(contexts[0], Mapping) else {}
    context_label = str(first_context.get("context_label") or "ml_shadow_no_context_candidate")
    source_route_family = str(first_context.get("source_route_family") or "none")
    reason = str(first_context.get("reason") or "No advisory context reason recorded.")

    source_ui_preview = preview.get("source_ui_preview", {})
    if not isinstance(source_ui_preview, Mapping):
        source_ui_preview = {}
    source_advisory = source_ui_preview.get("source_advisory", {})
    if not isinstance(source_advisory, Mapping):
        source_advisory = {}
    top_score = _extract_top_advisory_score(source_advisory)
    similar_text = _extract_similar_case_text(source_advisory)
    route_families = _string_list(preview.get("route_family_candidates"))
    hooks = _string_list(preview.get("recommended_hooks"))
    caution_flags = _string_list(preview.get("caution_flags"))
    preview_text = str(preview.get("preview_text") or "")
    hash_source = json.dumps(preview, sort_keys=True, ensure_ascii=True, default=str)

    return PromptSnapshot(
        prompt_id="ml_shadow_context_" + _safe_identifier(context_label),
        prompt_name="ML shadow/advisory context: " + context_label,
        prompt_path="kanda_reasoner_app/routing_signal_scorer/contract.py::build_similarity_prompt_context_preview",
        prompt_hash=sha256_text(hash_source),
        prompt_summary=(
            "Advisory-only prompt-context candidate derived from deterministic local "
            "routing_signal_scorer similarity/context preview."
        ),
        prompt_group="routing_signal_scorer",
        prompt_version=ML_CONTEXT_PREVIEW_VERSION,
        score=top_score,
        confidence=top_score,
        explanation=preview_text or reason,
        keywords=tuple(route_families + hooks + caution_flags)[:20],
        route=source_route_family,
        semantic_match=similar_text,
        inferred_intent=", ".join(route_families) if route_families else context_label,
        disagreement_reason=(
            "This is a shadow/advisory ML-context candidate only. It may disagree with the "
            "heuristic prompt snapshot, but it has no router authority and cannot load prompts."
        ),
        safety_status="advisory_only_no_router_authority",
    )


def summarize_session_capture_result(result: ShadowBridgeCaptureResult) -> str:
    """Return one compact log line for SessionService."""
    if not result:
        return "Prompt Router Reasoner capture: unavailable"
    parts = [
        "Prompt Router Reasoner capture: " + str(result.shadow_status),
        "reason=" + str(result.reason),
    ]
    if result.review_item_id:
        parts.append("review_item_id=" + result.review_item_id)
    if result.agreement_status:
        parts.append("agreement=" + result.agreement_status)
    parts.append("authoritative_output_unchanged=" + str(result.final_router_output_unchanged))
    return " | ".join(parts)


def _decision_text(decision: Any, name: str) -> str:
    """Support decision text behavior.
    
    Parameters
    ----------
    decision : Any
        The decision value.
    name : str
        The name value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(getattr(decision, name, "") or "")


def _safe_identifier(text: str) -> str:
    """Support safe identifier behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    safe = re.sub(r"[^a-zA-Z0-9_]+", "_", str(text or "").lower()).strip("_")
    return safe[:80] or "unknown"


def _string_list(value: Any) -> list[str]:
    """Support string list behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    if not isinstance(value, list | tuple):
        return []
    result: list[str] = []
    for item in value:
        text = str(item or "").strip()
        if text:
            result.append(text)
    return result


def _extract_top_advisory_score(advisory: Mapping[str, Any]) -> float | None:
    """Support extract top advisory score behavior.
    
    Parameters
    ----------
    advisory : Mapping[str, Any]
        The advisory value.
    
    Returns
    -------
    float | None
        The floating-point result.
    """
    
    suggestions = advisory.get("suggested_route_families", [])
    if not isinstance(suggestions, list):
        return None
    best: float | None = None
    for item in suggestions:
        if not isinstance(item, Mapping):
            continue
        try:
            score = float(item.get("score"))
        except (TypeError, ValueError):
            continue
        if best is None or score > best:
            best = score
    return best


def _extract_similar_case_text(advisory: Mapping[str, Any]) -> str:
    """Support extract similar case text behavior.
    
    Parameters
    ----------
    advisory : Mapping[str, Any]
        The advisory value.
    
    Returns
    -------
    str
        The string result.
    """
    
    cases = advisory.get("similar_cases", [])
    if not isinstance(cases, list):
        return ""
    parts: list[str] = []
    for item in cases[:3]:
        if not isinstance(item, Mapping):
            continue
        case_id = str(item.get("case_id") or "")
        score = str(item.get("similarity_score") or "")
        level = str(item.get("threshold_level") or "")
        text = case_id
        if score:
            text += " score=" + score
        if level:
            text += " level=" + level
        if text.strip():
            parts.append(text)
    return "; ".join(parts)
