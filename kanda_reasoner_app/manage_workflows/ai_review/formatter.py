# project-path: kanda_reasoner_app/manage_workflows/ai_review/formatter.py
"""Format Tab 2 advisory AI review output safely."""

from __future__ import annotations

from .models import CHECK_ADVISORY_BANNER, CORRECTION_ADVISORY_BANNER

__all__ = ["format_tab2_advisory_review_text"]


def _banner_for_kind(review_kind: str) -> str:
    """Return the forced banner for one review kind."""
    if str(review_kind or "").strip().lower() == "correction_plan":
        return CORRECTION_ADVISORY_BANNER
    return CHECK_ADVISORY_BANNER


def format_tab2_advisory_review_text(
    response_text: str,
    model_name: str,
    review_kind: str = "check",
) -> str:
    """Return advisory output with a forced authority reminder."""
    banner = _banner_for_kind(review_kind)
    body = str(response_text or "").strip()
    model = str(model_name or "").strip() or "unknown local model"
    return (
        banner
        + "\n"
        + "Model: "
        + model
        + "\n\n"
        + body
        + "\n\n"
        + "Deterministic Tab 2 Check/Correct remain the pass/fail and write "
        + "authorities. This AI review is read-only guidance."
    )
