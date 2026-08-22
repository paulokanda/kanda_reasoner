# project-path: kanda_reasoner_app/routing_signal_scorer/scoring.py
"""Rule-based diagnostic signal scoring for KANDA routing requests."""

from __future__ import annotations
__all__: list[str] = []


import re
from typing import Iterable, Mapping, Sequence

from .models import (
    AUTHORITY,
    FEATURE_ID,
    PRE_OUTPUT_HOOK,
    PRE_OUTPUT_TRIGGER_SIGNALS,
    SCHEMA_VERSION,
    SIGNAL_NAMES,
    SignalRule,
)

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

def _rules() -> tuple[SignalRule, ...]:
    """Support rules behavior.
    
    Returns
    -------
    tuple[SignalRule, ...]
        The tuple of values.
    """
    
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
    """Support apply combination rules behavior.
    
    Parameters
    ----------
    normalized : str
        The normalized value.
    scores : dict[str, float]
        The scores value.
    evidence : dict[str, list[str]]
        The evidence value.
    notes : list[str]
        The notes value.
    max_evidence_per_signal : int
        The max evidence per signal value.
    """
    
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

def _recommended_hooks(scores: Mapping[str, float]) -> list[str]:
    """Support recommended hooks behavior.
    
    Parameters
    ----------
    scores : Mapping[str, float]
        The scores value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    hooks: list[str] = []
    if float(scores.get("pre_output_contract_gate_required", 0.0)) >= 0.7:
        hooks.append(PRE_OUTPUT_HOOK)
    return hooks

def _normalize(text: str) -> str:
    """Support normalize behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    lowered = text.lower()
    return re.sub(r"\s+", " ", lowered).strip()

def _matched_patterns(normalized: str, patterns: Iterable[str]) -> list[str]:
    """Support matched patterns behavior.
    
    Parameters
    ----------
    normalized : str
        The normalized value.
    patterns : Iterable[str]
        The patterns value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    matches: list[str] = []
    for pattern in patterns:
        needle = pattern.lower().strip()
        if not needle:
            continue
        if needle in normalized:
            matches.append(pattern)
    return matches

def _add_score(scores: dict[str, float], signal: str, value: float) -> None:
    """Support add score behavior.
    
    Parameters
    ----------
    scores : dict[str, float]
        The scores value.
    signal : str
        The signal value.
    value : float
        The input value.
    """
    
    if signal not in scores:
        return
    scores[signal] = max(0.0, min(1.0, scores[signal] + value))

def _add_evidence(
    evidence: dict[str, list[str]],
    signal: str,
    item: str,
    max_items: int,
) -> None:
    """Support add evidence behavior.
    
    Parameters
    ----------
    evidence : dict[str, list[str]]
        The evidence value.
    signal : str
        The signal value.
    item : str
        The item value.
    max_items : int
        The max items value.
    """
    
    if signal not in evidence:
        return
    if item in evidence[signal]:
        return
    if len(evidence[signal]) >= max_items:
        return
    evidence[signal].append(item)

def _level(value: float) -> str:
    """Support level behavior.
    
    Parameters
    ----------
    value : float
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if value >= 0.7:
        return "high"
    if value >= 0.3:
        return "medium"
    return "low"

def _excerpt(text: str, limit: int = 240) -> str:
    """Support excerpt behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    str
        The string result.
    """
    
    compact = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
