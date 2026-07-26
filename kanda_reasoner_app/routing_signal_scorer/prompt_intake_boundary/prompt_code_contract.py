# project-path: kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_code_contract.py
"""Prompt code namespace contract for governed prompt intake."""

from __future__ import annotations

import re
from dataclasses import dataclass


PROMPT_CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{4,6}$")
RESERVED_UNSCOPED_PATTERN = re.compile(r"^[0-9]{4,6}$")


@dataclass(frozen=True)
class PromptCode:
    """Namespaced prompt code reference.

    A code is a reference and classification hint. It is not a route
    command and not prompt execution authority.
    """

    value: str

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        validate_prompt_code(self.value)


def validate_prompt_code(code: str) -> None:
    """Validate a namespaced prompt code and reject plain numeric codes."""

    if not isinstance(code, str) or not code.strip():
        raise ValueError("Prompt code must be a non-empty string")
    stripped = code.strip()
    if stripped != stripped.upper():
        raise ValueError("Prompt code must already use uppercase namespace syntax")
    normalized = stripped
    if RESERVED_UNSCOPED_PATTERN.fullmatch(normalized):
        raise ValueError("Prompt code must be namespaced, not plain digits")
    if not PROMPT_CODE_PATTERN.fullmatch(normalized):
        raise ValueError("Prompt code must use an uppercase namespace and digits")
