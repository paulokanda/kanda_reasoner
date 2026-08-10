# project-path: kanda_reasoner_app/engineering_diagnostics_gui/models.py
"""Immutable GUI-facing contracts for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from kanda_reasoner_app.engineering_diagnostics import (
    DiagnosticComparison,
    DiagnosticFindingEnrichment,
    DiagnosticFindingRecord,
    DiagnosticGroupRecord,
    DiagnosticLifecycleHead,
    DiagnosticLifecycleState,
    DiagnosticOwnerEnrichment,
    DiagnosticRemediationIntent,
    DiagnosticFrozenPathEnrichment,
    DiagnosticScopeEnrichment,
    DiagnosticRunInput,
    DiagnosticRunRecord,
)
from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

__all__ = [
    "DiagnosticFindingView",
    "DiagnosticRunView",
    "DiagnosticScanCandidate",
    "EngineeringDiagnosticsGuiCancelled",
]


class EngineeringDiagnosticsGuiCancelled(RuntimeError):
    """Raised when a cooperative GUI diagnostic operation is cancelled."""


def _unknown_enrichment() -> DiagnosticFindingEnrichment:
    return DiagnosticFindingEnrichment(
        scope=DiagnosticScopeEnrichment(
            "UNKNOWN",
            "low",
            "not_evaluated",
            (),
        ),
        frozen_path=DiagnosticFrozenPathEnrichment(
            "UNKNOWN",
            evidence=("not_evaluated",),
        ),
        owner=DiagnosticOwnerEnrichment(
            "NOT_EVALUATED",
            "none",
            selection_method="not_evaluated",
            evidence=("not_evaluated",),
        ),
    )


@dataclass(frozen=True, slots=True)
class DiagnosticScanCandidate:
    """Completed read-only producer output awaiting guarded persistence."""

    project_root: Path
    boundary: ProjectToolBoundaryIdentity
    run_input: DiagnosticRunInput
    source_fingerprint: str
    scope_fingerprint: str
    configuration_fingerprint: str
    operation_generation: int
    report_payload: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class DiagnosticFindingView:
    """Presentation finding row with baseline and deterministic enrichment."""

    record: DiagnosticFindingRecord
    lifecycle_state: str
    enrichment: DiagnosticFindingEnrichment = field(
        default_factory=_unknown_enrichment
    )
    groups: tuple[DiagnosticGroupRecord, ...] = ()
    decision_state: str = "OPEN"
    decision_generation: int = 0
    decision_head: DiagnosticLifecycleHead | None = None
    group_decision_heads: tuple[DiagnosticLifecycleHead, ...] = ()
    remediation_intent: DiagnosticRemediationIntent | None = None

    def group_decision_generation(self, group_id: str) -> int:
        """Return current CAS generation for one visible group target."""
        head = next(
            (item for item in self.group_decision_heads if item.target_id == group_id),
            None,
        )
        return head.generation if head is not None else 0

    @property
    def scope_classification(self) -> str:
        """Return the deterministic Project scope classification."""
        return self.enrichment.scope.classification

    @property
    def scope_confidence(self) -> str:
        """Return scope-classification confidence."""
        return self.enrichment.scope.confidence

    @property
    def frozen_status(self) -> str:
        """Return the active Project Freeze path status."""
        return self.enrichment.frozen_path.status

    @property
    def governing_freeze_ids(self) -> str:
        """Return a compact display value for governing Freeze IDs."""
        return ", ".join(self.enrichment.frozen_path.governing_freeze_ids)

    @property
    def owner_status(self) -> str:
        """Return the deterministic owner-enrichment status."""
        return self.enrichment.owner.status

    @property
    def owner_confidence(self) -> str:
        """Return owner-enrichment confidence."""
        return self.enrichment.owner.confidence

    @property
    def canonical_owner(self) -> str:
        """Return the canonical owner only when status is READY."""
        return self.enrichment.owner.canonical_owner

    @property
    def group_label(self) -> str:
        """Return the selected display group label without hiding memberships."""
        return self.groups[0].label if self.groups else ""

    @property
    def group_kind(self) -> str:
        """Return MANUAL, DETERMINISTIC, or UNGROUPED for filtering."""
        return self.groups[0].kind if self.groups else "UNGROUPED"

    @property
    def group_confidence(self) -> str:
        """Return confidence for the selected display group."""
        return self.groups[0].confidence if self.groups else ""

    @property
    def group_count(self) -> int:
        """Return the number of visible deterministic and manual memberships."""
        return len(self.groups)

    @property
    def remediation_action_class(self) -> str:
        """Return the current non-mutating remediation action class."""
        return (
            self.remediation_intent.action_class
            if self.remediation_intent is not None
            else "EVIDENCE_REQUIRED"
        )

    @property
    def manual_group(self) -> DiagnosticGroupRecord | None:
        """Return the current manual group assignment when present."""
        return next((group for group in self.groups if group.kind == "MANUAL"), None)


@dataclass(frozen=True, slots=True)
class DiagnosticRunView:
    """One persisted run with findings, groups, and baseline comparison."""

    run: DiagnosticRunRecord
    findings: tuple[DiagnosticFindingView, ...]
    comparison: DiagnosticComparison
    groups: tuple[DiagnosticGroupRecord, ...] = ()
    grouping_generation: int = 0
    lifecycle: DiagnosticLifecycleState | None = None
