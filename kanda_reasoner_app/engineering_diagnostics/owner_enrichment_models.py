# project-path: kanda_reasoner_app/engineering_diagnostics/owner_enrichment_models.py
"""Immutable Symbol Atlas owner enrichment contracts."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "OWNER_CONFIDENCE_LEVELS",
    "OWNER_ENRICHMENT_STATUSES",
    "DiagnosticOwnerEnrichment",
]

OWNER_ENRICHMENT_STATUSES = frozenset(
    {
        "READY",
        "NEEDS_REVIEW",
        "NO_OWNER",
        "DEGRADED",
        "NOT_EVALUATED",
    }
)
OWNER_CONFIDENCE_LEVELS = frozenset({"high", "medium", "low", "none"})


def _normalized_choice(value: object, allowed: frozenset[str], field: str) -> str:
    text = str(value or "").strip().upper()
    if text not in allowed:
        raise ValueError("Unsupported " + field + ": " + text)
    return text


def _confidence(value: object) -> str:
    text = str(value or "").strip().lower()
    if text not in OWNER_CONFIDENCE_LEVELS:
        raise ValueError("Unsupported owner confidence: " + text)
    return text


def _text(value: object) -> str:
    return str(value or "").strip()


def _tuple_text(values: object) -> tuple[str, ...]:
    if values is None:
        return ()
    result: list[str] = []
    for value in tuple(values):
        text = _text(value)
        if text and text not in result:
            result.append(text)
    return tuple(result)


@dataclass(frozen=True, slots=True)
class DiagnosticOwnerEnrichment:
    """Regenerable read-only owner context for one diagnostic finding."""

    status: str
    confidence: str
    canonical_owner: str = ""
    active_candidates: tuple[str, ...] = ()
    historical_candidates: tuple[str, ...] = ()
    selection_method: str = ""
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "status",
            _normalized_choice(
                self.status,
                OWNER_ENRICHMENT_STATUSES,
                "owner status",
            ),
        )
        object.__setattr__(self, "confidence", _confidence(self.confidence))
        object.__setattr__(
            self,
            "canonical_owner",
            _text(self.canonical_owner),
        )
        object.__setattr__(
            self,
            "active_candidates",
            _tuple_text(self.active_candidates),
        )
        object.__setattr__(
            self,
            "historical_candidates",
            _tuple_text(self.historical_candidates),
        )
        object.__setattr__(
            self,
            "selection_method",
            _text(self.selection_method),
        )
        object.__setattr__(self, "evidence", _tuple_text(self.evidence))

        if self.status == "READY" and not self.canonical_owner:
            raise ValueError("READY owner enrichment requires canonical_owner.")
        if self.status != "READY" and self.canonical_owner:
            raise ValueError(
                "Only READY owner enrichment may declare canonical_owner."
            )
