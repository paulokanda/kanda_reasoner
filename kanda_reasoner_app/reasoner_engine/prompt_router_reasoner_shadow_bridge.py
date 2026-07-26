# project-path: kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_shadow_bridge.py
"""Shadow bridge for Prompt Router Reasoner review capture.

This module connects a heuristic prompt selection and an ML advisory prompt
selection to the Prompt Router Reasoner review store. It never changes the
returned router or prompt-selection output. It is intentionally callable by
future runtime wiring, but it performs no provider calls, no router mutation,
no prompt-library mutation, and no freeze-memory writes.
"""

from __future__ import annotations


__all__ = [
    'bridge_result_keeps_authoritative_output',
    'build_prompt_snapshot_from_candidate',
    'capture_shadow_prompt_selection',
    'PromptRouterReasonerShadowBridgeError',
    'ShadowBridgeCaptureResult',
]
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    AGREEMENT_AGREE,
    AGREEMENT_DISAGREE,
    PromptRouterReasonerReviewStore,
    PromptRouterReasonerStoreError,
    PromptSnapshot,
    ROUTER_WITH_HEURISTICS,
    compact_generator_text,
    normalize_router_mode,
)

SHADOW_BRIDGE_SCHEMA_VERSION = "1.0"
SHADOW_STATUS_CAPTURED = "captured"
SHADOW_STATUS_SKIPPED = "skipped"
SHADOW_REASON_CAPTURED = "shadow_review_item_captured"
SHADOW_REASON_DISABLED = "shadow_bridge_disabled"
SHADOW_REASON_NO_STORE = "review_store_unavailable"
SHADOW_REASON_NO_GENERATOR_TEXT = "generator_text_missing"
SHADOW_REASON_NO_HEURISTIC_PROMPT = "heuristic_prompt_missing"
SHADOW_REASON_NO_ML_PROMPT = "ml_prompt_missing"

FORBIDDEN_BRIDGE_PATH_FRAGMENTS = (
    "project_freeze_after_update",
    "project_freeze_ledger",
    "frozen_features_memory",
    "freeze_hint_intake",
)


@dataclass(frozen=True)
class ShadowBridgeCaptureResult:
    """Result of one shadow bridge capture attempt."""

    schema_version: str
    shadow_status: str
    reason: str
    review_item_id: str
    agreement_status: str
    router_mode_at_capture: str
    final_router_output: Any
    final_router_output_unchanged: bool
    review_store_dir: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable summary except for final_router_output."""
        return {
            "schema_version": self.schema_version,
            "shadow_status": self.shadow_status,
            "reason": self.reason,
            "review_item_id": self.review_item_id,
            "agreement_status": self.agreement_status,
            "router_mode_at_capture": self.router_mode_at_capture,
            "final_router_output_unchanged": self.final_router_output_unchanged,
            "review_store_dir": self.review_store_dir,
        }


class PromptRouterReasonerShadowBridgeError(RuntimeError):
    """Raised when the shadow bridge configuration is unsafe."""


def capture_shadow_prompt_selection(
    *,
    full_generator_text: str,
    heuristic_prompt: PromptSnapshot | Mapping[str, Any] | None,
    ml_prompt: PromptSnapshot | Mapping[str, Any] | None,
    final_router_output: Any = None,
    project_root: str | Path | None = None,
    review_store: PromptRouterReasonerReviewStore | None = None,
    enabled: bool = True,
    generator_text_id: str | None = None,
    short_generator_text: str | None = None,
    router_mode_at_capture: str | None = None,
    app_version: str = "",
    router_version: str = "",
    retriever_version: str = "",
    ml_version: str = "",
    prompt_library_version: str = "",
    safety_violation: bool = False,
    notes: str = "",
) -> ShadowBridgeCaptureResult:
    """Capture one heuristic-vs-ML prompt comparison for later human review.

    The authoritative router or prompt-selection result is passed through as
    final_router_output and returned unchanged. The function records only a
    pending review item. If the bridge is disabled, the store is unavailable,
    or a required candidate is missing, it fails open and returns a skipped
    result without mutating router behavior.
    """
    mode = normalize_router_mode(router_mode_at_capture or ROUTER_WITH_HEURISTICS)

    if not enabled:
        return _skipped_result(
            reason=SHADOW_REASON_DISABLED,
            router_mode_at_capture=mode,
            final_router_output=final_router_output,
            review_store_dir=_store_dir_text(review_store),
        )

    if not str(full_generator_text or "").strip():
        return _skipped_result(
            reason=SHADOW_REASON_NO_GENERATOR_TEXT,
            router_mode_at_capture=mode,
            final_router_output=final_router_output,
            review_store_dir=_store_dir_text(review_store),
        )

    if heuristic_prompt is None:
        return _skipped_result(
            reason=SHADOW_REASON_NO_HEURISTIC_PROMPT,
            router_mode_at_capture=mode,
            final_router_output=final_router_output,
            review_store_dir=_store_dir_text(review_store),
        )

    if ml_prompt is None:
        return _skipped_result(
            reason=SHADOW_REASON_NO_ML_PROMPT,
            router_mode_at_capture=mode,
            final_router_output=final_router_output,
            review_store_dir=_store_dir_text(review_store),
        )

    store = _resolve_review_store(project_root=project_root, review_store=review_store)
    review_id = store.create_pending_review(
        full_generator_text=full_generator_text,
        short_generator_text=short_generator_text or compact_generator_text(full_generator_text),
        generator_text_id=generator_text_id,
        heuristic_prompt=heuristic_prompt,
        ml_prompt=ml_prompt,
        router_mode_at_capture=mode,
        app_version=app_version,
        router_version=router_version,
        retriever_version=retriever_version,
        ml_version=ml_version,
        prompt_library_version=prompt_library_version,
        safety_violation=safety_violation,
        notes=notes,
    )
    item = store.get_review_item(review_id)
    return ShadowBridgeCaptureResult(
        schema_version=SHADOW_BRIDGE_SCHEMA_VERSION,
        shadow_status=SHADOW_STATUS_CAPTURED,
        reason=SHADOW_REASON_CAPTURED,
        review_item_id=review_id,
        agreement_status=str(item.get("agreement_status", "")),
        router_mode_at_capture=mode,
        final_router_output=final_router_output,
        final_router_output_unchanged=True,
        review_store_dir=str(store.review_dir),
    )


def build_prompt_snapshot_from_candidate(
    candidate: Mapping[str, Any],
    *,
    role: str,
) -> PromptSnapshot:
    """Normalize a candidate mapping into a PromptSnapshot.

    This helper is intentionally pure. It lets future bridge wiring adapt
    existing heuristic and ML candidate dictionaries without importing router,
    prompt-library writer, or provider code into this module.
    """
    if not isinstance(candidate, Mapping):
        raise PromptRouterReasonerShadowBridgeError(role + " candidate must be a mapping")
    snapshot = PromptSnapshot.from_mapping(candidate)
    snapshot.validate(field_name=role)
    return snapshot


def bridge_result_keeps_authoritative_output(
    result: ShadowBridgeCaptureResult,
    expected_output: Any,
) -> bool:
    """Return True only when the bridge returned the exact authoritative object."""
    return result.final_router_output is expected_output


def _resolve_review_store(
    *,
    project_root: str | Path | None,
    review_store: PromptRouterReasonerReviewStore | None,
) -> PromptRouterReasonerReviewStore:
    """Support resolve review store behavior.
    
    Parameters
    ----------
    project_root : str | Path | None
        The project root path.
    review_store : PromptRouterReasonerReviewStore | None
        The review store value.
    
    Returns
    -------
    PromptRouterReasonerReviewStore
        The prompt router reasoner review store result.
    """
    
    if review_store is not None:
        _validate_store_boundary(review_store)
        return review_store
    if project_root is None:
        raise PromptRouterReasonerStoreError(SHADOW_REASON_NO_STORE)
    store = PromptRouterReasonerReviewStore(project_root)
    _validate_store_boundary(store)
    return store


def _validate_store_boundary(store: PromptRouterReasonerReviewStore) -> None:
    """Support validate store boundary behavior.
    
    Parameters
    ----------
    store : PromptRouterReasonerReviewStore
        The store value.
    """
    
    review_dir = Path(store.review_dir)
    lowered = str(review_dir).replace("\\", "/").lower()
    for fragment in FORBIDDEN_BRIDGE_PATH_FRAGMENTS:
        if fragment.lower() in lowered:
            raise PromptRouterReasonerShadowBridgeError(
                "Shadow bridge review store must not point at: " + fragment
            )


def _store_dir_text(review_store: PromptRouterReasonerReviewStore | None) -> str:
    """Support store dir text behavior.
    
    Parameters
    ----------
    review_store : PromptRouterReasonerReviewStore | None
        The review store value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if review_store is None:
        return ""
    return str(review_store.review_dir)


def _skipped_result(
    *,
    reason: str,
    router_mode_at_capture: str,
    final_router_output: Any,
    review_store_dir: str,
) -> ShadowBridgeCaptureResult:
    """Support skipped result behavior.
    
    Parameters
    ----------
    reason : str
        The reason value.
    router_mode_at_capture : str
        The router mode at capture value.
    final_router_output : Any
        The final router output value.
    review_store_dir : str
        The review store dir value.
    
    Returns
    -------
    ShadowBridgeCaptureResult
        The shadow bridge capture result result.
    """
    
    return ShadowBridgeCaptureResult(
        schema_version=SHADOW_BRIDGE_SCHEMA_VERSION,
        shadow_status=SHADOW_STATUS_SKIPPED,
        reason=reason,
        review_item_id="",
        agreement_status="",
        router_mode_at_capture=router_mode_at_capture,
        final_router_output=final_router_output,
        final_router_output_unchanged=True,
        review_store_dir=review_store_dir,
    )
