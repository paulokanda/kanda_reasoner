# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/fixture_catalog_contract.py
"""Contracts for Phase 3 offline fixture catalog.

The catalog is still non-runtime and non-authoritative. It defines immutable,
caller-supplied-style synthetic fixtures for exercising the Phase 2 offline
harness. It does not load prompt text, scan prompt libraries, read freeze
memory, read router canon, call providers, persist reports, or select routes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from .offline_evaluation_contract import (
    OfflineEvaluationFixture,
    OfflineEvaluationStatus,
)


FEATURE_ID = "rss_ml_adv_phase3_offline_fixture_catalog_contract_v1"


class OfflineFixtureIntent(str, Enum):
    """Finite synthetic fixture intents for offline-only evaluation."""

    LOW_SIGNAL_CONTROL = "LOW_SIGNAL_CONTROL"
    AMBIGUITY_SIGNAL = "AMBIGUITY_SIGNAL"
    CONFLICT_SIGNAL = "CONFLICT_SIGNAL"
    PROMPT_GAP_SIGNAL = "PROMPT_GAP_SIGNAL"
    ROUTE_VARIANCE_REJECTION = "ROUTE_VARIANCE_REJECTION"


@dataclass(frozen=True)
class OfflineFixtureCatalogEntry:
    """One cataloged synthetic fixture and its expected harness behavior."""

    catalog_entry_id: str
    intent: OfflineFixtureIntent
    fixture: OfflineEvaluationFixture
    expected_status: OfflineEvaluationStatus
    expected_route_invariant: bool
    safety_scope_codes: Tuple[str, ...]

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("catalog_entry_id", self.catalog_entry_id)
        if not isinstance(self.intent, OfflineFixtureIntent):
            raise TypeError("intent must be OfflineFixtureIntent")
        if not isinstance(self.fixture, OfflineEvaluationFixture):
            raise TypeError("fixture must be OfflineEvaluationFixture")
        if not isinstance(self.expected_status, OfflineEvaluationStatus):
            raise TypeError("expected_status must be OfflineEvaluationStatus")
        if not isinstance(self.expected_route_invariant, bool):
            raise TypeError("expected_route_invariant must be bool")
        _require_tuple_of_text("safety_scope_codes", self.safety_scope_codes)


@dataclass(frozen=True)
class OfflineFixtureCatalog:
    """Immutable synthetic catalog for Phase 3 offline evaluation."""

    catalog_id: str
    feature_id: str
    entries: Tuple[OfflineFixtureCatalogEntry, ...]
    catalog_scope: str
    non_runtime: bool = True
    non_authoritative: bool = True

    def __post_init__(self) -> None:
        """Support post init behavior.
        """
        
        _require_text("catalog_id", self.catalog_id)
        _require_text("feature_id", self.feature_id)
        if self.feature_id != FEATURE_ID:
            raise ValueError("feature_id must match Phase 3 fixture catalog")
        if not isinstance(self.entries, tuple):
            raise TypeError("entries must be tuple")
        if not self.entries:
            raise ValueError("entries must not be empty")
        seen = set()
        for entry in self.entries:
            if not isinstance(entry, OfflineFixtureCatalogEntry):
                raise TypeError("entries contains invalid item")
            if entry.catalog_entry_id in seen:
                raise ValueError("catalog_entry_id values must be unique")
            seen.add(entry.catalog_entry_id)
        _require_text("catalog_scope", self.catalog_scope)
        if self.non_runtime is not True:
            raise ValueError("non_runtime must remain True")
        if self.non_authoritative is not True:
            raise ValueError("non_authoritative must remain True")


def catalog_fixtures(catalog: OfflineFixtureCatalog) -> Tuple[OfflineEvaluationFixture, ...]:
    """Return immutable fixtures for the Phase 2 offline harness."""

    if not isinstance(catalog, OfflineFixtureCatalog):
        raise TypeError("catalog must be OfflineFixtureCatalog")
    return tuple(entry.fixture for entry in catalog.entries)


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


def _require_tuple_of_text(name: str, value: Tuple[str, ...]) -> None:
    """Support require tuple of text behavior.
    
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
