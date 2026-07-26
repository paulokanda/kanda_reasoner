# project-path: kanda_reasoner_app/routing_signal_scorer/shield.py
"""Shield-status contract for the routing similarity bounded context."""

from __future__ import annotations
__all__: list[str] = []


from typing import Mapping, Sequence

from .models import (
    ADVISORY_FEATURE_ID,
    FEATURE_ID,
    SIMILARITY_BOX_SHIELD_FEATURE_ID,
    SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_EXPLAINABILITY_FEATURE_ID,
    SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
    SIMILARITY_RUNTIME_LITE_FEATURE_ID,
    SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
    SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
)
from .similarity_preview import build_similarity_prompt_context_preview

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
