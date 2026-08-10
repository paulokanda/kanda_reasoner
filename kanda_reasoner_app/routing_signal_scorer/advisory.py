# project-path: kanda_reasoner_app/routing_signal_scorer/advisory.py
"""Advisory-only route-family summaries built from diagnostic signals."""

from __future__ import annotations
__all__: list[str] = []


from typing import Mapping, Sequence

from .models import ADVISORY_AUTHORITY, ADVISORY_FEATURE_ID
from .scoring import _level, score_routing_signals

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

def _route_family_suggestions(
    signals: Mapping[str, object],
    *,
    max_suggestions: int,
) -> list[dict[str, object]]:
    """Support route family suggestions behavior.
    
    Parameters
    ----------
    signals : Mapping[str, object]
        The signals value.
    max_suggestions : int
        The max suggestions value.
    
    Returns
    -------
    list[dict[str, object]]
        The list of values.
    """
    
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
    """Support caution flags behavior.
    
    Parameters
    ----------
    signals : Mapping[str, object]
        The signals value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
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
    """Support advisory notes behavior.
    
    Parameters
    ----------
    suggestions : Sequence[object]
        The suggestions value.
    caution_flags : Sequence[object]
        The caution flags value.
    recommended_hooks : Sequence[object]
        The recommended hooks value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
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
    """Support coerce score behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
