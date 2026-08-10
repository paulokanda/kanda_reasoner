# project-path: kanda_reasoner_app/engineering_diagnostics/owner_enrichment.py
"""Read-only Symbol Atlas owner enrichment for diagnostic findings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

from kanda_reasoner_app.reasoner_symbol_atlas import (
    ProjectModuleRecord,
    ProjectSymbol,
    classify_reasoner_symbol_atlas_owners,
)
from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
    is_active_owner_candidate,
)

from .models import DiagnosticFindingRecord
from .owner_enrichment_models import DiagnosticOwnerEnrichment

__all__ = [
    "DiagnosticOwnerSnapshot",
    "build_diagnostic_owner_snapshot",
    "classify_diagnostic_owner",
]

_OWNER_CLASSIFIER = Callable[[str | Path], tuple[ProjectModuleRecord, ...]]
_CANONICAL_ROLE = "canonical_owner"


def _path(value: object) -> str:
    text = str(value or "").replace("\\", "/").strip()
    while text.startswith("./"):
        text = text[2:]
    return text.strip("/")


def _symbol_keys(value: object) -> tuple[str, ...]:
    text = str(value or "").strip()
    if not text:
        return ()
    keys = [text]
    for separator in ("::", ":"):
        if separator in text:
            keys.append(text.rsplit(separator, 1)[-1])
    if "." in text:
        keys.append(text.rsplit(".", 1)[-1])
    return tuple(dict.fromkeys(key for key in keys if key))


def _candidate_label(
    record: ProjectModuleRecord,
    symbol: ProjectSymbol | None = None,
) -> str:
    base = _path(record.path)
    if symbol is not None and symbol.name:
        return base + "::" + symbol.name
    return base


def _record_is_active(record: ProjectModuleRecord) -> bool:
    return is_active_owner_candidate(
        record.path,
        record.owner_role,
        record.is_test_file,
    )


@dataclass(frozen=True, slots=True)
class DiagnosticOwnerSnapshot:
    """One read-only Symbol Atlas snapshot prepared for batch enrichment."""

    modules_by_path: Mapping[str, tuple[ProjectModuleRecord, ...]]
    symbols_by_name: Mapping[str, tuple[tuple[ProjectModuleRecord, ProjectSymbol], ...]]
    module_count: int
    degraded_reason: str = ""

    @property
    def degraded(self) -> bool:
        """Return whether Symbol Atlas owner classification failed closed."""
        return bool(self.degraded_reason)


def build_diagnostic_owner_snapshot(
    project_root: str | Path,
    *,
    records: Sequence[ProjectModuleRecord] | None = None,
    classifier: _OWNER_CLASSIFIER = classify_reasoner_symbol_atlas_owners,
) -> DiagnosticOwnerSnapshot:
    """Build one reusable owner lookup without mutating Symbol Atlas state."""
    try:
        classified = tuple(records) if records is not None else tuple(
            classifier(Path(project_root).expanduser().resolve(strict=True))
        )
    except Exception as exc:  # noqa: BLE001
        return DiagnosticOwnerSnapshot(
            MappingProxyType({}),
            MappingProxyType({}),
            0,
            degraded_reason=type(exc).__name__ + ": " + str(exc),
        )

    modules: dict[str, list[ProjectModuleRecord]] = {}
    symbols: dict[str, list[tuple[ProjectModuleRecord, ProjectSymbol]]] = {}
    for record in classified:
        modules.setdefault(_path(record.path), []).append(record)
        for symbol in record.symbols:
            if symbol.name:
                symbols.setdefault(symbol.name, []).append((record, symbol))

    module_map = {
        key: tuple(sorted(values, key=lambda item: (item.path, item.module)))
        for key, values in modules.items()
    }
    symbol_map = {
        key: tuple(
            sorted(
                values,
                key=lambda item: (
                    item[0].path,
                    item[1].line or 0,
                    item[1].name,
                ),
            )
        )
        for key, values in symbols.items()
    }
    return DiagnosticOwnerSnapshot(
        MappingProxyType(module_map),
        MappingProxyType(symbol_map),
        len(classified),
    )


def _matching_candidates(
    snapshot: DiagnosticOwnerSnapshot,
    finding: DiagnosticFindingRecord,
) -> tuple[
    tuple[tuple[ProjectModuleRecord, ProjectSymbol | None], ...],
    str,
]:
    matches: list[tuple[ProjectModuleRecord, ProjectSymbol | None]] = []
    path_key = _path(finding.relative_path)
    for record in snapshot.modules_by_path.get(path_key, ()):
        matches.append((record, None))

    symbol_match_count = 0
    symbol_records: list[ProjectModuleRecord] = []
    for key in _symbol_keys(finding.symbol_id):
        for record, symbol in snapshot.symbols_by_name.get(key, ()):
            pair = (record, symbol)
            if pair not in matches:
                matches.append(pair)
                symbol_match_count += 1
                symbol_records.append(record)
    if symbol_records:
        matches = [
            pair
            for pair in matches
            if pair[1] is not None or pair[0] not in symbol_records
        ]

    method = "exact_path"
    if symbol_match_count and path_key:
        method = "exact_path_and_symbol"
    elif symbol_match_count:
        method = "exact_symbol"
    return tuple(matches), method


def classify_diagnostic_owner(
    snapshot: DiagnosticOwnerSnapshot,
    finding: DiagnosticFindingRecord,
) -> DiagnosticOwnerEnrichment:
    """Classify owner context without inventing certainty or writing state."""
    if snapshot.degraded:
        return DiagnosticOwnerEnrichment(
            "DEGRADED",
            "none",
            selection_method="symbol_atlas_classifier_failed",
            evidence=(snapshot.degraded_reason,),
        )

    if not _path(finding.relative_path) and not _symbol_keys(finding.symbol_id):
        return DiagnosticOwnerEnrichment(
            "NOT_EVALUATED",
            "none",
            selection_method="missing_finding_identity",
            evidence=("No Project-relative path or symbol ID was available.",),
        )

    matches, method = _matching_candidates(snapshot, finding)
    active: list[tuple[ProjectModuleRecord, ProjectSymbol | None]] = []
    historical: list[tuple[ProjectModuleRecord, ProjectSymbol | None]] = []
    for record, symbol in matches:
        if _record_is_active(record):
            active.append((record, symbol))
        else:
            historical.append((record, symbol))

    active_labels = tuple(
        dict.fromkeys(_candidate_label(record, symbol) for record, symbol in active)
    )
    historical_labels = tuple(
        dict.fromkeys(
            _candidate_label(record, symbol) for record, symbol in historical
        )
    )
    canonical = [
        (record, symbol)
        for record, symbol in active
        if (symbol.owner_role if symbol is not None else record.owner_role)
        == _CANONICAL_ROLE
    ]
    canonical_labels = tuple(
        dict.fromkeys(
            _candidate_label(record, symbol) for record, symbol in canonical
        )
    )
    evidence = (
        "symbol_atlas_module_count: " + str(snapshot.module_count),
        "matching_candidates: " + str(len(matches)),
        "active_candidates: " + str(len(active_labels)),
        "historical_candidates: " + str(len(historical_labels)),
        "canonical_candidates: " + str(len(canonical_labels)),
    )

    if len(canonical_labels) == 1:
        return DiagnosticOwnerEnrichment(
            "READY",
            "high" if method == "exact_path_and_symbol" else "medium",
            canonical_owner=canonical_labels[0],
            active_candidates=active_labels,
            historical_candidates=historical_labels,
            selection_method=method + ":single_active_canonical_owner",
            evidence=evidence,
        )
    if active_labels:
        return DiagnosticOwnerEnrichment(
            "NEEDS_REVIEW",
            "medium" if len(canonical_labels) > 1 else "low",
            active_candidates=active_labels,
            historical_candidates=historical_labels,
            selection_method=method + ":competing_or_noncanonical_active_owners",
            evidence=evidence,
        )
    return DiagnosticOwnerEnrichment(
        "NO_OWNER",
        "none",
        active_candidates=(),
        historical_candidates=historical_labels,
        selection_method=method + ":no_active_owner_candidate",
        evidence=evidence,
    )
