# project-path: kanda_reasoner_app/engineering_diagnostics/enrichment_models.py
"""Immutable deterministic enrichment contracts for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .owner_enrichment_models import DiagnosticOwnerEnrichment

__all__ = [
    "FROZEN_PATH_STATUSES",
    "SCOPE_CLASSIFICATIONS",
    "DiagnosticFindingEnrichment",
    "DiagnosticFrozenPathEnrichment",
    "DiagnosticScopeEnrichment",
]

SCOPE_CLASSIFICATIONS = frozenset(
    {
        "ACTIVE",
        "TEST",
        "FIXTURE",
        "PROTOTYPE",
        "GENERATED",
        "REFERENCE",
        "DEPRECATED",
        "WORKBENCH",
        "SNIPPET",
        "TEMPORARY",
        "UNKNOWN",
    }
)
FROZEN_PATH_STATUSES = frozenset(
    {
        "UNFROZEN",
        "FROZEN",
        "TOUCHES_FROZEN",
        "HISTORICAL_FROZEN",
        "UNKNOWN",
    }
)
_VALID_CONFIDENCE = frozenset({"low", "medium", "high"})


def _normalized_choice(
    value: object,
    allowed: frozenset[str],
    field_name: str,
) -> str:
    text = str(value or "").strip().upper()
    if text not in allowed:
        raise ValueError("Unsupported " + field_name + ": " + text)
    return text


def _confidence(value: object) -> str:
    text = str(value or "").strip().lower()
    if text not in _VALID_CONFIDENCE:
        raise ValueError("Unsupported enrichment confidence: " + text)
    return text


def _text(value: object) -> str:
    return str(value or "").strip()


def _tuple_text(values: object) -> tuple[str, ...]:
    if values is None:
        return ()
    output: list[str] = []
    for value in tuple(values):
        text = _text(value)
        if text and text not in output:
            output.append(text)
    return tuple(output)


@dataclass(frozen=True, slots=True)
class DiagnosticScopeEnrichment:
    """Regenerable deterministic scope context for one finding path."""

    classification: str
    confidence: str
    method: str
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "classification",
            _normalized_choice(
                self.classification,
                SCOPE_CLASSIFICATIONS,
                "scope classification",
            ),
        )
        object.__setattr__(self, "confidence", _confidence(self.confidence))
        object.__setattr__(self, "method", _text(self.method))
        object.__setattr__(self, "evidence", _tuple_text(self.evidence))


@dataclass(frozen=True, slots=True)
class DiagnosticFrozenPathEnrichment:
    """Regenerable read-only Freeze context for one finding and related paths."""

    status: str
    governing_freeze_ids: tuple[str, ...] = ()
    matched_protected_paths: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "status",
            _normalized_choice(
                self.status,
                FROZEN_PATH_STATUSES,
                "frozen-path status",
            ),
        )
        object.__setattr__(
            self,
            "governing_freeze_ids",
            _tuple_text(self.governing_freeze_ids),
        )
        object.__setattr__(
            self,
            "matched_protected_paths",
            _tuple_text(self.matched_protected_paths),
        )
        object.__setattr__(self, "evidence", _tuple_text(self.evidence))


def _not_evaluated_owner() -> "DiagnosticOwnerEnrichment":
    from .owner_enrichment_models import DiagnosticOwnerEnrichment

    return DiagnosticOwnerEnrichment(
        "NOT_EVALUATED",
        "none",
        selection_method="not_evaluated",
        evidence=("Owner enrichment was not evaluated.",),
    )


@dataclass(frozen=True, slots=True)
class DiagnosticFindingEnrichment:
    """Combined scope, Freeze, and owner context for one finding."""

    scope: DiagnosticScopeEnrichment
    frozen_path: DiagnosticFrozenPathEnrichment
    owner: "DiagnosticOwnerEnrichment" = field(
        default_factory=_not_evaluated_owner
    )
