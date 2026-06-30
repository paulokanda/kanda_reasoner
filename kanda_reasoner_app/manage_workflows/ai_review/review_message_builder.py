# project-path: kanda_reasoner_app/manage_workflows/ai_review/review_message_builder.py
"""Prompt builders for Tab 2 advisory AI review."""

from __future__ import annotations

from .models import Tab2AIReviewRequest

__all__ = [
    "build_tab2_ai_review_messages",
    "limit_text_for_model",
]

TRUNCATION_NOTICE = "\n\n[Input truncated for local model context.]\n"


def limit_text_for_model(text: str, max_chars: int) -> str:
    """Return bounded text with an explicit truncation notice."""
    normalized = str(text or "")
    limit = max(1000, int(max_chars or 12000))
    if len(normalized) <= limit:
        return normalized
    keep = max(0, limit - len(TRUNCATION_NOTICE))
    return normalized[:keep] + TRUNCATION_NOTICE


def _system_message() -> dict[str, str]:
    """Return the common system message for Tab 2 review."""
    return {
        "role": "system",
        "content": (
            "You are an advisory reviewer for Kanda Reasoner Tab 2. "
            "Tab 2 deterministic Check and Correct remain authoritative. "
            "You must not claim to validate, write files, apply corrections, "
            "run Correct, freeze patches, or replace deterministic validation. "
            "Give concise, practical guidance for safe surgical engineering."
        ),
    }


def _check_prompt(request: Tab2AIReviewRequest) -> str:
    """Build the user prompt for AI Review Check."""
    audit_text = limit_text_for_model(
        request.check_output_text,
        request.max_chars,
    )
    return (
        "Review the latest Tab 2 deterministic Check output.\n\n"
        "Return these sections:\n"
        "1. Advisory summary\n"
        "2. Highest risks first\n"
        "3. Suggested next inspection files\n"
        "4. Safest correction strategy\n"
        "5. Tests to run before any correction\n"
        "6. What deterministic Tab 2 Check still decides\n\n"
        "Constraints:\n"
        "- Do not suggest automatic writes.\n"
        "- Do not say the AI result is a pass/fail authority.\n"
        "- Respect feature boxes and narrow surgical repairs.\n\n"
        "Project root marker: <PROJECT_ROOT>\n"
        "Selected mode: " + str(request.mode_label or "unknown") + "\n\n"
        "Tab 2 deterministic Check output:\n"
        + audit_text
    )


def _correction_prompt(request: Tab2AIReviewRequest) -> str:
    """Build the user prompt for AI Review Correction Plan."""
    audit_text = limit_text_for_model(
        request.check_output_text,
        request.max_chars,
    )
    return (
        "Create a read-only advisory correction plan from the latest Tab 2 "
        "output. Do not apply corrections.\n\n"
        "Return these sections:\n"
        "1. Advisory correction summary\n"
        "2. Correction risks and box boundaries\n"
        "3. Files or contracts to inspect before Correct\n"
        "4. Safest deterministic Correct workflow\n"
        "5. Tests and validations required after Correct\n"
        "6. What deterministic Tab 2 Correct still decides\n\n"
        "Hard rule:\n"
        "- This is read-only advice. Do not write files, do not run Correct, "
        "and do not create a patch.\n\n"
        "Project root marker: <PROJECT_ROOT>\n"
        "Selected mode: " + str(request.mode_label or "unknown") + "\n\n"
        "Latest Tab 2 output/context:\n"
        + audit_text
    )


def build_tab2_ai_review_messages(
    request: Tab2AIReviewRequest,
) -> list[dict[str, str]]:
    """Build chat messages for one Tab 2 AI review request."""
    review_kind = str(request.review_kind or "check").strip().lower()
    if review_kind == "correction_plan":
        prompt = _correction_prompt(request)
    else:
        prompt = _check_prompt(request)
    return [_system_message(), {"role": "user", "content": prompt}]
