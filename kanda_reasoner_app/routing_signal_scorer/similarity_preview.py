# project-path: kanda_reasoner_app/routing_signal_scorer/similarity_preview.py
"""Presentation adapters for routing similarity output."""

from __future__ import annotations
__all__: list[str] = []


from typing import Mapping, Sequence

from .models import (
    PRE_OUTPUT_HOOK,
    SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
    SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
    SIMILARITY_VISIBILITY_THRESHOLD,
)
from .similarity_runtime import build_similarity_runtime_lite_advisory

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

def _candidate_prompt_contexts_for_route_families(
    route_families: Sequence[str],
    hooks: Sequence[object],
    caution_flags: Sequence[object],
) -> list[dict[str, object]]:
    """Support candidate prompt contexts for route families behavior.
    
    Parameters
    ----------
    route_families : Sequence[str]
        The route families value.
    hooks : Sequence[object]
        The hooks value.
    caution_flags : Sequence[object]
        The caution flags value.
    
    Returns
    -------
    list[dict[str, object]]
        The list of values.
    """
    
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
    """Support similarity prompt context preview lines behavior.
    
    Parameters
    ----------
    route_families : Sequence[str]
        The route families value.
    candidate_contexts : Sequence[Mapping[str, object]]
        The candidate contexts value.
    hooks : Sequence[object]
        The hooks value.
    caution_flags : Sequence[object]
        The caution flags value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
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
    """Support similarity ui preview lines behavior.
    
    Parameters
    ----------
    advisory : Mapping[str, object]
        The advisory value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
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
