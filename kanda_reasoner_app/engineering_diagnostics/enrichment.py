# project-path: kanda_reasoner_app/engineering_diagnostics/enrichment.py
"""Batch deterministic scope and frozen-path enrichment public service."""

from __future__ import annotations

from pathlib import Path

from .enrichment_models import (
    DiagnosticFindingEnrichment,
    DiagnosticFrozenPathEnrichment,
    DiagnosticScopeEnrichment,
)
from .frozen_path_enrichment import (
    DiagnosticFreezeSnapshot,
    build_diagnostic_freeze_snapshot,
    classify_diagnostic_frozen_path,
    related_project_paths_from_evidence,
)
from .models import DiagnosticFindingRecord
from .owner_enrichment import (
    DiagnosticOwnerSnapshot,
    build_diagnostic_owner_snapshot,
    classify_diagnostic_owner,
)
from .owner_enrichment_models import DiagnosticOwnerEnrichment
from .scope_enrichment import (
    DiagnosticScopePolicy,
    build_diagnostic_scope_policy,
    classify_diagnostic_scope,
)

__all__ = ["EngineeringDiagnosticsEnricher"]


class EngineeringDiagnosticsEnricher:
    """Prepared read-only batch enrichment service for one selected Project."""

    def __init__(
        self,
        project_root: str | Path,
        *,
        owner_snapshot: DiagnosticOwnerSnapshot | None = None,
    ) -> None:
        self._scope_policy: DiagnosticScopePolicy = build_diagnostic_scope_policy(
            project_root
        )
        self._freeze_snapshot: DiagnosticFreezeSnapshot = (
            build_diagnostic_freeze_snapshot(project_root)
        )
        self._owner_snapshot = owner_snapshot or build_diagnostic_owner_snapshot(
            project_root
        )

    @property
    def project_root(self) -> Path:
        """Return the selected Project root bound to this enrichment service."""
        return self._scope_policy.project_root

    def enrich(
        self,
        finding: DiagnosticFindingRecord,
    ) -> DiagnosticFindingEnrichment:
        """Return deterministic context without changing finding identity."""
        scope = classify_diagnostic_scope(
            self._scope_policy,
            finding.relative_path,
        )
        related = related_project_paths_from_evidence(finding.evidence)
        frozen = classify_diagnostic_frozen_path(
            self._freeze_snapshot,
            finding.relative_path,
            related_paths=related,
        )
        owner = classify_diagnostic_owner(self._owner_snapshot, finding)
        return DiagnosticFindingEnrichment(
            scope=scope,
            frozen_path=frozen,
            owner=owner,
        )

    def enrich_many(
        self,
        findings: tuple[DiagnosticFindingRecord, ...],
    ) -> tuple[DiagnosticFindingEnrichment, ...]:
        """Return ordered enrichment while reusing identical batch decisions."""
        scope_cache: dict[str, DiagnosticScopeEnrichment] = {}
        freeze_cache: dict[
            tuple[str, tuple[str, ...]], DiagnosticFrozenPathEnrichment
        ] = {}
        owner_cache: dict[tuple[str, str], DiagnosticOwnerEnrichment] = {}
        output: list[DiagnosticFindingEnrichment] = []

        for finding in findings:
            path_key = str(finding.relative_path)
            scope = scope_cache.get(path_key)
            if scope is None:
                scope = classify_diagnostic_scope(
                    self._scope_policy,
                    finding.relative_path,
                )
                scope_cache[path_key] = scope

            related = related_project_paths_from_evidence(finding.evidence)
            freeze_key = (path_key, related)
            frozen = freeze_cache.get(freeze_key)
            if frozen is None:
                frozen = classify_diagnostic_frozen_path(
                    self._freeze_snapshot,
                    finding.relative_path,
                    related_paths=related,
                )
                freeze_cache[freeze_key] = frozen

            owner_key = (path_key, str(finding.symbol_id))
            owner = owner_cache.get(owner_key)
            if owner is None:
                owner = classify_diagnostic_owner(self._owner_snapshot, finding)
                owner_cache[owner_key] = owner

            output.append(
                DiagnosticFindingEnrichment(
                    scope=scope,
                    frozen_path=frozen,
                    owner=owner,
                )
            )

        return tuple(output)
