# project-path: kanda_reasoner_app/routing_signal_scorer/models.py
"""Shared constants and small data structures for routing signal scoring."""

from __future__ import annotations
__all__: list[str] = []


from dataclasses import dataclass

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
