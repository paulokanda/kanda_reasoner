# project-path: kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_artifact_contract.py
"""Prompt artifact contract for future governed prompt intake."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .prompt_code_contract import PromptCode
from .prompt_lifecycle_contract import PromptLifecycleState, prompt_can_bind_to_router


@dataclass(frozen=True)
class PromptArtifactContract:
    """First-class prompt artifact metadata.

    This is a contract only. It does not write to a prompt library, bind the
    router, or mutate any registry.
    """

    prompt_id: str
    prompt_code: PromptCode
    prompt_title: str
    box_owner: str
    scope: str
    allowed_use_cases: Tuple[str, ...]
    forbidden_use_cases: Tuple[str, ...]
    lifecycle_state: PromptLifecycleState
    version: str
    validated: bool
    router_bound: bool
    frozen: bool
    active: bool
    superseded: bool = False

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("prompt_id", self.prompt_id)
        _require_text("prompt_title", self.prompt_title)
        _require_text("box_owner", self.box_owner)
        _require_text("scope", self.scope)
        _require_text("version", self.version)
        _require_tuple_text("allowed_use_cases", self.allowed_use_cases)
        _require_tuple_text("forbidden_use_cases", self.forbidden_use_cases)
        if not isinstance(self.prompt_code, PromptCode):
            raise TypeError("prompt_code must be PromptCode")
        if not isinstance(self.lifecycle_state, PromptLifecycleState):
            raise TypeError("lifecycle_state must be PromptLifecycleState")
        for name in ("validated", "router_bound", "frozen", "active", "superseded"):
            if not isinstance(getattr(self, name), bool):
                raise TypeError(f"{name} must be bool")

    def can_be_considered_by_router(self) -> bool:
        """Return True only when all router-binding gates are satisfied."""

        return prompt_can_bind_to_router(
            validated=self.validated,
            router_bound=self.router_bound,
            frozen=self.frozen,
            active=self.active,
            superseded=self.superseded,
        )


def _require_text(name: str, value: str) -> None:
    """Support require text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : str
        The input value.
    """
    
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")


def _require_tuple_text(name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple text behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    value : Tuple[str, ...]
        The input value.
    """
    
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be a tuple")
    for item in value:
        _require_text(name, item)
