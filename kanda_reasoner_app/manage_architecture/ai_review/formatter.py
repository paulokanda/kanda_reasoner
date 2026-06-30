# project-path: kanda_reasoner_app/manage_architecture/ai_review/formatter.py
"""Format Tab 1 AI review output as advisory text."""

from __future__ import annotations

from .models import ADVISORY_BANNER

__all__ = ["format_advisory_review_text"]


def format_advisory_review_text(model_text: str, model_name: str = "") -> str:
    """Return advisory review text with a forced authority banner."""
    body = str(model_text or "").strip()
    lines = [ADVISORY_BANNER]
    if model_name:
        lines.append("Model: " + str(model_name))
    lines.append("")
    if body.startswith(ADVISORY_BANNER):
        body = body[len(ADVISORY_BANNER):].lstrip()
    lines.append(body or "The model returned an empty advisory response.")
    lines.append("")
    lines.append(
        "Deterministic First Check remains the pass/fail authority. "
        "This AI review is read-only guidance."
    )
    return "\n".join(lines)
