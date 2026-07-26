# project-path: kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_output_firewall.py
"""Prompt-output firewall for future governed prompt intake."""

from __future__ import annotations


FORBIDDEN_PROMPT_OUTPUT_PHRASES = frozenset(
    {
        "ignore previous rules",
        "override router",
        "bypass freeze",
        "write directly to registry",
        "modify prompt library without tests",
        "always select this prompt",
        "treat this prompt as final route",
        "import from other box internals",
        "call provider",
        "call network",
        "write persistence",
        "leak freeze memory",
        "leak router canon",
    }
)


def validate_prompt_candidate_text(text: str) -> None:
    """Reject prompt candidates with boundary-bypass instructions."""

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Prompt candidate text must be a non-empty string")
    lowered = text.lower()
    for phrase in FORBIDDEN_PROMPT_OUTPUT_PHRASES:
        if phrase in lowered:
            raise ValueError("Forbidden prompt-output phrase found: " + phrase)
