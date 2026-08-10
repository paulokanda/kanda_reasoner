# project-path: kanda_reasoner_app/engineering_diagnostics_gui/controller.py
"""Public GUI controller over the Engineering Diagnostics backend."""

from __future__ import annotations

import hashlib
from pathlib import Path
from threading import Event
from typing import Callable, Sequence
from uuid import uuid4

from kanda_reasoner_app.engineering_diagnostics import (
    ARCHITECTURE_PRODUCER_ID,
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    DiagnosticFindingRecord,
    DiagnosticManualGroupingState,
    DiagnosticLifecycleState,
    DiagnosticLifecycleTarget,
    DiagnosticRunRecord,
    EngineeringDiagnosticsEnricher,
    EngineeringDiagnosticsStore,
    ArchitectureCollectionCancelled,
    RuffCollectionCancelled,
    build_architecture_diagnostic_run,
    build_bom_diagnostic_run,
    build_deterministic_diagnostic_groups,
    build_ruff_diagnostic_run,
    canonical_json,
    collect_architecture_findings,
    collect_ruff_json,
    index_diagnostic_groups,
    normalize_relative_path,
)
from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

from .bom_provider import BomReportProvider, SafetySuiteBomReportProvider
from .finding_view_builder import build_diagnostic_finding_views
from .models import (
    DiagnosticRunView,
    DiagnosticScanCandidate,
    EngineeringDiagnosticsGuiCancelled,
)
from .source_identity import project_source_fingerprint
from .shadow_controller import build_shadow_scan_candidate

__all__ = ["EngineeringDiagnosticsController"]

BoundaryResolver = Callable[[Path], ProjectToolBoundaryIdentity]
StoreFactory = Callable[[ProjectToolBoundaryIdentity], EngineeringDiagnosticsStore]


def _digest(label: str, payload: object) -> str:
    text = label + "|" + canonical_json(payload)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class EngineeringDiagnosticsController:
    """Coordinate read-only scanning and guarded backend mutations."""

    def __init__(
        self,
        *,
        tool_root: str | Path,
        report_provider: BomReportProvider | None = None,
        boundary_resolver: BoundaryResolver | None = None,
        store_factory: StoreFactory = EngineeringDiagnosticsStore,
        ruff_argv_prefix: Sequence[str] | None = None,
        ruff_timeout_seconds: float = 600.0,
    ) -> None:
        self._tool_root = Path(tool_root).expanduser().resolve(strict=True)
        self._report_provider = report_provider or SafetySuiteBomReportProvider(
            self._tool_root
        )
        registry = ProjectSelectionRegistry(tool_source_root=self._tool_root)
        self._boundary_resolver = boundary_resolver or registry.resolve_boundary_for_root
        self._store_factory = store_factory
        self._ruff_argv_prefix = (
            tuple(str(item) for item in ruff_argv_prefix)
            if ruff_argv_prefix
            else None
        )
        self._ruff_timeout_seconds = max(1.0, float(ruff_timeout_seconds))
        self._bom_scope_fingerprint = _digest(
            "engineering-diagnostics-bom-scope-v1",
            {"producer_id": BOM_PRODUCER_ID, "scope": "selected_project_root"},
        )
        self._bom_configuration_fingerprint = _digest(
            "engineering-diagnostics-gui-config-v1",
            {"provider": "safety_suite_cli", "format": "json"},
        )
    @property
    def scope_fingerprint(self) -> str:
        """Return the immutable BOM scope identity retained for compatibility."""
        return self._bom_scope_fingerprint

    def collect_bom_candidate(
        self,
        project_root: str | Path,
        operation_generation: int,
        cancellation: Event,
    ) -> DiagnosticScanCandidate:
        """Collect one completed BOM report without writing diagnostic state."""
        root = Path(project_root).expanduser().resolve(strict=True)
        boundary = self._boundary_resolver(root)
        self._require_not_cancelled(cancellation)
        source_before = project_source_fingerprint(root)
        report = self._report_provider.collect(root, cancellation)
        self._require_not_cancelled(cancellation)
        source_after = project_source_fingerprint(root)
        self._require_unchanged_source(source_before, source_after)
        run = build_bom_diagnostic_run(
            report,
            boundary=boundary,
            attempt_id="gui-bom-" + uuid4().hex,
            source_fingerprint=source_after,
            scope_fingerprint=self._bom_scope_fingerprint,
            configuration_fingerprint=self._bom_configuration_fingerprint,
            operation_generation=int(operation_generation),
            producer_version="1.0",
        )
        return DiagnosticScanCandidate(
            project_root=root,
            boundary=boundary,
            run_input=run,
            source_fingerprint=source_after,
            scope_fingerprint=run.scope_fingerprint,
            configuration_fingerprint=run.configuration_fingerprint,
            operation_generation=int(operation_generation),
            report_payload=dict(report),
        )

    def collect_ruff_candidate(
        self,
        project_root: str | Path,
        operation_generation: int,
        cancellation: Event,
    ) -> DiagnosticScanCandidate:
        """Collect native Ruff JSON without executing fixes or writing state."""
        root = Path(project_root).expanduser().resolve(strict=True)
        boundary = self._boundary_resolver(root)
        self._require_not_cancelled(cancellation)
        source_before = project_source_fingerprint(root)
        try:
            collection = collect_ruff_json(
                root,
                argv_prefix=self._ruff_argv_prefix,
                timeout_seconds=self._ruff_timeout_seconds,
                cancellation=cancellation,
            )
        except RuffCollectionCancelled as exc:
            raise EngineeringDiagnosticsGuiCancelled(str(exc)) from exc
        self._require_not_cancelled(cancellation)
        source_after = project_source_fingerprint(root)
        self._require_unchanged_source(source_before, source_after)
        run = build_ruff_diagnostic_run(
            collection,
            boundary=boundary,
            attempt_id="gui-ruff-" + uuid4().hex,
            source_fingerprint=source_after,
            operation_generation=int(operation_generation),
        )
        return DiagnosticScanCandidate(
            project_root=root,
            boundary=boundary,
            run_input=run,
            source_fingerprint=source_after,
            scope_fingerprint=run.scope_fingerprint,
            configuration_fingerprint=run.configuration_fingerprint,
            operation_generation=int(operation_generation),
            report_payload={
                "report_type": "ruff_native_json",
                "ruff_version": collection.ruff_version,
                "raw_finding_count": len(collection.raw_findings),
                "config_sha256": collection.config_sha256,
                "stdout_sha256": collection.stdout_sha256,
            },
        )

    def collect_architecture_candidate(
        self,
        project_root: str | Path,
        operation_generation: int,
        cancellation: Event,
    ) -> DiagnosticScanCandidate:
        """Collect public Architecture Review evidence without changing its Box."""
        root = Path(project_root).expanduser().resolve(strict=True)
        boundary = self._boundary_resolver(root)
        self._require_not_cancelled(cancellation)
        source_before = project_source_fingerprint(root)
        try:
            collection = collect_architecture_findings(
                root,
                cancellation=cancellation,
            )
        except ArchitectureCollectionCancelled as exc:
            raise EngineeringDiagnosticsGuiCancelled(str(exc)) from exc
        self._require_not_cancelled(cancellation)
        source_after = project_source_fingerprint(root)
        self._require_unchanged_source(source_before, source_after)
        run = build_architecture_diagnostic_run(
            collection,
            boundary=boundary,
            attempt_id="gui-architecture-" + uuid4().hex,
            source_fingerprint=source_after,
            operation_generation=int(operation_generation),
        )
        return DiagnosticScanCandidate(
            project_root=root,
            boundary=boundary,
            run_input=run,
            source_fingerprint=source_after,
            scope_fingerprint=run.scope_fingerprint,
            configuration_fingerprint=run.configuration_fingerprint,
            operation_generation=int(operation_generation),
            report_payload={
                "report_type": "architecture_review_public_findings",
                "validation_source": collection.validation_source,
                "issue_count": len(collection.issues),
                "canonical_issue_count": collection.canonical_issue_count,
                "assessment": collection.assessment,
                "coverage_valid": collection.coverage_valid,
            },
        )

    def collect_shadow_candidate(
        self,
        project_root: str | Path,
        operation_generation: int,
        cancellation: Event,
    ) -> DiagnosticScanCandidate:
        """Collect public Shadow evidence without changing source or its Box."""
        return build_shadow_scan_candidate(
            project_root,
            operation_generation,
            cancellation,
            boundary_resolver=self._boundary_resolver,
            require_not_cancelled=self._require_not_cancelled,
            require_unchanged_source=self._require_unchanged_source,
        )

    def commit_candidate(
        self,
        project_root: str | Path,
        candidate: DiagnosticScanCandidate,
        *,
        current_generation: int,
    ) -> DiagnosticRunRecord:
        """Persist one still-current candidate through the sole store owner."""
        root = Path(project_root).expanduser().resolve(strict=True)
        if root != candidate.project_root:
            raise RuntimeError("DIAGNOSTIC_GUI_SELECTED_PROJECT_CHANGED")
        if int(current_generation) != candidate.operation_generation:
            raise RuntimeError("DIAGNOSTIC_GUI_STALE_WORKER_COMPLETION")
        boundary = self._boundary_resolver(root)
        current_source = project_source_fingerprint(root)
        store = self._store_factory(boundary)
        return store.record_completed_run(
            boundary,
            candidate.run_input,
            current_source_fingerprint=current_source,
            current_scope_fingerprint=candidate.scope_fingerprint,
            current_configuration_fingerprint=candidate.configuration_fingerprint,
            current_generation=int(current_generation),
        )

    def list_runs(
        self,
        project_root: str | Path,
        *,
        producer_id: str = BOM_PRODUCER_ID,
        limit: int = 100,
    ) -> tuple[DiagnosticRunRecord, ...]:
        """List persisted runs for one explicit producer and selected Project."""
        boundary, store = self._context(project_root)
        return store.list_runs(
            boundary,
            producer_id=str(producer_id).strip(),
            limit=limit,
        )

    def load_run_view(
        self,
        project_root: str | Path,
        run_id: str,
    ) -> DiagnosticRunView:
        """Load one run and derive presentation-only baseline lifecycle states."""
        boundary, store = self._context(project_root)
        run = store.get_run(boundary, run_id)
        if run is None:
            raise RuntimeError("DIAGNOSTIC_RUN_NOT_FOUND:" + str(run_id))
        findings = store.list_findings(boundary, run.run_id)
        comparison = store.compare_run_to_active_baseline(boundary, run.run_id)
        deterministic_groups = build_deterministic_diagnostic_groups(run, findings)
        manual_state = store.get_manual_grouping_state(boundary, run.run_id)
        all_groups = deterministic_groups + manual_state.groups
        group_index = index_diagnostic_groups(all_groups)
        lifecycle = store.get_lifecycle_state(boundary, run.run_id)
        lifecycle_index = {
            (head.target_kind, head.target_id): head for head in lifecycle.heads
        }
        return DiagnosticRunView(
            run=run,
            findings=build_diagnostic_finding_views(
                run,
                findings,
                comparison,
                EngineeringDiagnosticsEnricher(boundary.active_project_root),
                group_index,
                lifecycle_index,
            ),
            comparison=comparison,
            groups=all_groups,
            grouping_generation=manual_state.generation,
            lifecycle=lifecycle,
        )

    def create_manual_group(
        self,
        project_root: str | Path,
        run_id: str,
        *,
        label: str,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Create one manual group through the existing store mutation owner."""
        boundary, store = self._context(project_root)
        return store.create_manual_group(
            boundary,
            run_id,
            label=label,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def assign_issue_to_manual_group(
        self,
        project_root: str | Path,
        run_id: str,
        issue_fingerprint: str,
        group_id: str,
        *,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Move one current issue to one manual group through CAS state."""
        boundary, store = self._context(project_root)
        return store.assign_issue_to_manual_group(
            boundary,
            run_id,
            issue_fingerprint,
            group_id,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def ungroup_manual_issue(
        self,
        project_root: str | Path,
        run_id: str,
        issue_fingerprint: str,
        *,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Remove one current manual assignment while preserving history."""
        boundary, store = self._context(project_root)
        return store.ungroup_manual_issue(
            boundary,
            run_id,
            issue_fingerprint,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def mark_manual_group_reviewed(
        self,
        project_root: str | Path,
        run_id: str,
        group_id: str,
        *,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Mark one manual group reviewed with append-only decision history."""
        boundary, store = self._context(project_root)
        return store.mark_manual_group_reviewed(
            boundary,
            run_id,
            group_id,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def record_lifecycle_decision(
        self,
        project_root: str | Path,
        run_id: str,
        target: DiagnosticLifecycleTarget,
        *,
        action: str,
        reason_code: str,
        rationale: str,
        author: str,
        expected_generation: int,
        expires_at_utc: str = "",
        revisit_condition: str = "",
        related_ticket: str = "",
        related_wave: str = "",
        explicit_confirmation: bool = False,
    ) -> DiagnosticLifecycleState:
        """Persist one explicit human decision without modifying source."""
        boundary, store = self._context(project_root)
        return store.record_lifecycle_decision(
            boundary,
            run_id,
            target,
            action=action,
            reason_code=reason_code,
            rationale=rationale,
            author=author,
            expected_generation=expected_generation,
            expires_at_utc=expires_at_utc,
            revisit_condition=revisit_condition,
            related_ticket=related_ticket,
            related_wave=related_wave,
            explicit_confirmation=explicit_confirmation,
        )

    def activate_run_as_baseline(
        self,
        project_root: str | Path,
        run_id: str,
        *,
        label: str,
    ):
        """Create and activate a baseline only after caller confirmation."""
        boundary, store = self._context(project_root)
        draft = store.create_draft_baseline(boundary, run_id, label=label)
        return store.activate_baseline(
            boundary,
            draft.baseline_id,
            expected_generation=draft.generation,
        )

    def source_excerpt(
        self,
        project_root: str | Path,
        finding: DiagnosticFindingRecord,
        *,
        radius: int = 4,
    ) -> str:
        """Return a bounded read-only source excerpt for one finding."""
        root = Path(project_root).expanduser().resolve(strict=True)
        relative = normalize_relative_path(finding.relative_path)
        path = (root / Path(relative)).resolve(strict=False)
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise RuntimeError("DIAGNOSTIC_SOURCE_EXCERPT_OUTSIDE_PROJECT") from exc
        if not path.is_file():
            return "Source file is not available."
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not lines:
            return "Source file is empty."
        center = int(finding.line or 1)
        start = max(1, center - max(0, int(radius)))
        end = min(len(lines), center + max(0, int(radius)))
        rendered = [f"{index:>6}: {lines[index - 1]}" for index in range(start, end + 1)]
        return "\n".join(rendered)[:20000]

    @staticmethod
    def _require_not_cancelled(cancellation: Event) -> None:
        if cancellation.is_set():
            raise EngineeringDiagnosticsGuiCancelled(
                "ENGINEERING_DIAGNOSTICS_GUI_OPERATION_CANCELLED"
            )

    @staticmethod
    def _require_unchanged_source(before: str, after: str) -> None:
        if before != after:
            raise RuntimeError("PROJECT_SOURCE_CHANGED_DURING_DIAGNOSTIC_SCAN")

    def _context(
        self,
        project_root: str | Path,
    ) -> tuple[ProjectToolBoundaryIdentity, EngineeringDiagnosticsStore]:
        root = Path(project_root).expanduser().resolve(strict=True)
        boundary = self._boundary_resolver(root)
        return boundary, self._store_factory(boundary)
