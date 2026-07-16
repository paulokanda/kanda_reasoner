"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

__all__ = [
    "ProjectProfile",
]

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProjectProfile:
    """
    Canonical optional profile for project-specific retrieval behavior.

    This object is a passive data container only.
    It must not execute retrieval logic.
    It must not call collector code.
    It must not import runtime collector code.
    """

    name: str = "generic"
    description: str = "Generic profile with no project-specific boosts."
    domain_scope: str = "generic"

    path_priority_terms: tuple[str, ...] = field(default_factory=tuple)
    path_penalty_terms: tuple[str, ...] = field(default_factory=tuple)
    owner_path_boosts: dict[str, int] = field(default_factory=dict)

    symbol_priority_terms: tuple[str, ...] = field(default_factory=tuple)
    symbol_penalty_terms: tuple[str, ...] = field(default_factory=tuple)
    symbol_boosts: dict[str, int] = field(default_factory=dict)

    question_aliases: dict[str, tuple[str, ...]] = field(default_factory=dict)
    chain_aliases: dict[str, tuple[str, ...]] = field(default_factory=dict)
    feature_flags: dict[str, bool] = field(default_factory=dict)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "domain_scope": self.domain_scope,
            "path_priority_terms": list(self.path_priority_terms),
            "path_penalty_terms": list(self.path_penalty_terms),
            "owner_path_boosts": dict(self.owner_path_boosts),
            "symbol_priority_terms": list(self.symbol_priority_terms),
            "symbol_penalty_terms": list(self.symbol_penalty_terms),
            "symbol_boosts": dict(self.symbol_boosts),
            "question_aliases": {
                key: list(value) for key, value in self.question_aliases.items()
            },
            "chain_aliases": {
                key: list(value) for key, value in self.chain_aliases.items()
            },
            "feature_flags": dict(self.feature_flags),
            "notes": list(self.notes),
        }
