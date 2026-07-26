# project-path: kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_lifecycle_contract.py
"""Prompt lifecycle states for governed prompt intake."""

from __future__ import annotations

from enum import Enum


class PromptLifecycleState(str, Enum):
    """Lifecycle states for prompt artifacts."""

    PROPOSED = "PROPOSED"
    CLASSIFIED = "CLASSIFIED"
    DRAFTED = "DRAFTED"
    TESTED = "TESTED"
    VALIDATED = "VALIDATED"
    ROUTER_BOUND = "ROUTER_BOUND"
    FROZEN = "FROZEN"
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    RETIRED = "RETIRED"
    REJECTED = "REJECTED"


def prompt_can_bind_to_router(
    *,
    validated: bool,
    router_bound: bool,
    frozen: bool,
    active: bool,
    superseded: bool,
) -> bool:
    """Return True only for validated, router-bound, frozen active prompts."""

    return validated and router_bound and frozen and active and not superseded
