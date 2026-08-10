# project-path: kanda_reasoner_app/routing_signal_scorer/contract.py
"""Public compatibility facade for the KANDA routing signal scorer.

The implementation is split into cohesive ordinary Python modules. This facade
keeps the original public API and compatibility private helper names available
from ``kanda_reasoner_app.routing_signal_scorer.contract``.
"""

from __future__ import annotations

from .advisory import (
    build_routing_advisory as _public_build_routing_advisory,
    summarize_advisory as _public_summarize_advisory,
)
from .models import (
    ADVISORY_AUTHORITY as _public_ADVISORY_AUTHORITY,
    ADVISORY_FEATURE_ID as _public_ADVISORY_FEATURE_ID,
    AUTHORITY as _public_AUTHORITY,
    FEATURE_ID as _public_FEATURE_ID,
    PRE_OUTPUT_HOOK as _public_PRE_OUTPUT_HOOK,
    PRE_OUTPUT_TRIGGER_SIGNALS as _public_PRE_OUTPUT_TRIGGER_SIGNALS,
    SCHEMA_VERSION as _public_SCHEMA_VERSION,
    SIGNAL_NAMES as _public_SIGNAL_NAMES,
    SIMILARITY_BOX_SHIELD_FEATURE_ID as _public_SIMILARITY_BOX_SHIELD_FEATURE_ID,
    SIMILARITY_DECISION_REPORT_FEATURE_ID as _public_SIMILARITY_DECISION_REPORT_FEATURE_ID,
    SIMILARITY_EXPLAINABILITY_FEATURE_ID as _public_SIMILARITY_EXPLAINABILITY_FEATURE_ID,
    SIMILARITY_HIGH_THRESHOLD as _public_SIMILARITY_HIGH_THRESHOLD,
    SIMILARITY_PROMOTION_THRESHOLD as _public_SIMILARITY_PROMOTION_THRESHOLD,
    SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID as _public_SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID,
    SIMILARITY_RUNTIME_LITE_AUTHORITY as _public_SIMILARITY_RUNTIME_LITE_AUTHORITY,
    SIMILARITY_RUNTIME_LITE_FEATURE_ID as _public_SIMILARITY_RUNTIME_LITE_FEATURE_ID,
    SIMILARITY_THRESHOLD_POLICY_FEATURE_ID as _public_SIMILARITY_THRESHOLD_POLICY_FEATURE_ID,
    SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID as _public_SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID,
    SIMILARITY_VISIBILITY_THRESHOLD as _public_SIMILARITY_VISIBILITY_THRESHOLD,
    SignalRule as _public_SignalRule,
)
from .scoring import (
    score_routing_signals as _public_score_routing_signals,
    summarize_signal_result as _public_summarize_signal_result,
)
from .shield import (
    build_similarity_box_shield_status as _public_build_similarity_box_shield_status,
    render_similarity_box_shield_status_text as _public_render_similarity_box_shield_status_text,
)
from .similarity_preview import (
    build_similarity_prompt_context_preview as _public_build_similarity_prompt_context_preview,
    build_similarity_ui_preview_adapter as _public_build_similarity_ui_preview_adapter,
    render_similarity_prompt_context_preview_text as _public_render_similarity_prompt_context_preview_text,
    render_similarity_ui_preview_text as _public_render_similarity_ui_preview_text,
)
from .similarity_runtime import (
    build_similarity_runtime_lite_advisory as _public_build_similarity_runtime_lite_advisory,
    summarize_similarity_runtime_lite_advisory as _public_summarize_similarity_runtime_lite_advisory,
)

ADVISORY_AUTHORITY = _public_ADVISORY_AUTHORITY
ADVISORY_FEATURE_ID = _public_ADVISORY_FEATURE_ID
AUTHORITY = _public_AUTHORITY
FEATURE_ID = _public_FEATURE_ID
PRE_OUTPUT_HOOK = _public_PRE_OUTPUT_HOOK
PRE_OUTPUT_TRIGGER_SIGNALS = _public_PRE_OUTPUT_TRIGGER_SIGNALS
SCHEMA_VERSION = _public_SCHEMA_VERSION
SIGNAL_NAMES = _public_SIGNAL_NAMES
SIMILARITY_BOX_SHIELD_FEATURE_ID = _public_SIMILARITY_BOX_SHIELD_FEATURE_ID
SIMILARITY_DECISION_REPORT_FEATURE_ID = _public_SIMILARITY_DECISION_REPORT_FEATURE_ID
SIMILARITY_EXPLAINABILITY_FEATURE_ID = _public_SIMILARITY_EXPLAINABILITY_FEATURE_ID
SIMILARITY_HIGH_THRESHOLD = _public_SIMILARITY_HIGH_THRESHOLD
SIMILARITY_PROMOTION_THRESHOLD = _public_SIMILARITY_PROMOTION_THRESHOLD
SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID = _public_SIMILARITY_PROMPT_CONTEXT_PREVIEW_FEATURE_ID
SIMILARITY_RUNTIME_LITE_AUTHORITY = _public_SIMILARITY_RUNTIME_LITE_AUTHORITY
SIMILARITY_RUNTIME_LITE_FEATURE_ID = _public_SIMILARITY_RUNTIME_LITE_FEATURE_ID
SIMILARITY_THRESHOLD_POLICY_FEATURE_ID = _public_SIMILARITY_THRESHOLD_POLICY_FEATURE_ID
SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID = _public_SIMILARITY_UI_PREVIEW_ADAPTER_FEATURE_ID
SIMILARITY_VISIBILITY_THRESHOLD = _public_SIMILARITY_VISIBILITY_THRESHOLD
SignalRule = _public_SignalRule
build_routing_advisory = _public_build_routing_advisory
summarize_advisory = _public_summarize_advisory
score_routing_signals = _public_score_routing_signals
summarize_signal_result = _public_summarize_signal_result
build_similarity_box_shield_status = _public_build_similarity_box_shield_status
render_similarity_box_shield_status_text = _public_render_similarity_box_shield_status_text
build_similarity_prompt_context_preview = _public_build_similarity_prompt_context_preview
build_similarity_ui_preview_adapter = _public_build_similarity_ui_preview_adapter
render_similarity_prompt_context_preview_text = _public_render_similarity_prompt_context_preview_text
render_similarity_ui_preview_text = _public_render_similarity_ui_preview_text
build_similarity_runtime_lite_advisory = _public_build_similarity_runtime_lite_advisory
summarize_similarity_runtime_lite_advisory = _public_summarize_similarity_runtime_lite_advisory

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
