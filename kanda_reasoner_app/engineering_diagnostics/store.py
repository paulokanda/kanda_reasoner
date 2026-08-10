# project-path: kanda_reasoner_app/engineering_diagnostics/store.py
"""Sole public SQLite mutation owner for Engineering Diagnostics."""

from __future__ import annotations

from contextlib import closing
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

from ._store_baseline_ops import (
    activate as _activate_baseline,
    compare as _compare_baseline,
    create_draft as _create_draft_baseline,
    get as _get_baseline,
    get_active as _get_active_baseline,
)
from ._store_database import (
    connect,
    finding_record,
    initialize,
    run_record,
)
from ._store_grouping_ops import (
    assign_issue as _assign_issue_to_manual_group,
    create_group as _create_manual_group,
    get_state as _get_manual_grouping_state,
    mark_reviewed as _mark_manual_group_reviewed,
    ungroup_issue as _ungroup_manual_issue,
)
from ._store_lifecycle_ops import record_decision as _record_lifecycle_decision
from ._store_lifecycle_state import get_state as _get_lifecycle_state
from .fingerprinting import run_content_digest
from ._store_run_ops import (
    _insert_run,
    _normalize_findings,
    _path_key,
    _run_id,
)
from .grouping_models import DiagnosticManualGroupingState
from .lifecycle_models import (
    DiagnosticLifecycleState,
    DiagnosticLifecycleTarget,
)
from .models import (
    DiagnosticBaselineRecord,
    DiagnosticBoundaryError,
    DiagnosticComparison,
    DiagnosticConflictError,
    DiagnosticFindingInput,
    DiagnosticFindingRecord,
    DiagnosticRunInput,
    DiagnosticRunRecord,
)
from .paths import engineering_diagnostics_database_path

__all__ = ["EngineeringDiagnosticsStore"]


class EngineeringDiagnosticsStore:
    """Persist completed runs and baselines for one selected Project."""

    def __init__(
        self,
        boundary: ProjectToolBoundaryIdentity,
        database_path: str | Path | None = None,
    ) -> None:
        self._project_id = boundary.active_project_id
        self._root_fingerprint = boundary.active_project_root_fingerprint
        self._project_root_key = _path_key(boundary.active_project_root)
        self._support_root_key = _path_key(boundary.active_project_support_root)
        default_path = engineering_diagnostics_database_path(boundary)
        self.database_path = Path(database_path or default_path).resolve(strict=False)
        owner_root = default_path.parent.resolve(strict=False)
        try:
            self.database_path.relative_to(owner_root)
        except ValueError as exc:
            raise DiagnosticBoundaryError(
                "ENGINEERING_DIAGNOSTICS_DATABASE_OUTSIDE_OWNER_ROOT"
            ) from exc
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        initialize(self.database_path)

    def record_completed_run(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run: DiagnosticRunInput,
        *,
        current_source_fingerprint: str,
        current_scope_fingerprint: str,
        current_configuration_fingerprint: str,
        current_generation: int,
    ) -> DiagnosticRunRecord:
        """Atomically persist one completed, current, immutable run."""
        self._require_boundary(boundary)
        self._require_run_current(
            run,
            current_source_fingerprint=current_source_fingerprint,
            current_scope_fingerprint=current_scope_fingerprint,
            current_configuration_fingerprint=current_configuration_fingerprint,
            current_generation=current_generation,
        )
        finding_rows = _normalize_findings(run)
        content_digest = run_content_digest(
            run,
            tuple(
                (row["issue_fingerprint"], row["evidence_digest"])
                for row in finding_rows
            ),
        )
        run_id = _run_id(run.project_id, run.attempt_id)
        with closing(connect(self.database_path)) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                existing = connection.execute(
                    "SELECT * FROM diagnostic_runs WHERE attempt_id = ?",
                    (run.attempt_id,),
                ).fetchone()
                if existing is not None:
                    if str(existing["content_digest"]) != content_digest:
                        raise DiagnosticConflictError(
                            "DIAGNOSTIC_ATTEMPT_ID_CONTENT_CONFLICT"
                        )
                    connection.rollback()
                    return run_record(existing)
                _insert_run(connection, run_id, run, content_digest, finding_rows)
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
        record = self.get_run(boundary, run_id)
        if record is None:
            raise RuntimeError("DIAGNOSTIC_RUN_DISAPPEARED_AFTER_COMMIT")
        return record

    def get_run(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
    ) -> DiagnosticRunRecord | None:
        """Return one completed run through the public record contract."""
        self._require_boundary(boundary)
        with closing(connect(self.database_path)) as connection:
            row = connection.execute(
                "SELECT * FROM diagnostic_runs WHERE run_id = ?",
                (str(run_id),),
            ).fetchone()
        return run_record(row) if row is not None else None

    def list_runs(
        self,
        boundary: ProjectToolBoundaryIdentity,
        *,
        producer_id: str | None = None,
        limit: int = 100,
    ) -> tuple[DiagnosticRunRecord, ...]:
        """List recent completed runs without exposing persistence objects."""
        self._require_boundary(boundary)
        bounded_limit = max(1, min(int(limit), 1000))
        query = "SELECT * FROM diagnostic_runs"
        parameters: tuple[Any, ...] = ()
        if producer_id is not None:
            query += " WHERE producer_id = ?"
            parameters = (str(producer_id).strip(),)
        query += " ORDER BY rowid DESC LIMIT ?"
        parameters += (bounded_limit,)
        with closing(connect(self.database_path)) as connection:
            rows = connection.execute(query, parameters).fetchall()
        return tuple(run_record(row) for row in rows)

    def list_findings(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
    ) -> tuple[DiagnosticFindingRecord, ...]:
        """Return normalized findings for one completed run."""
        self._require_boundary(boundary)
        with closing(connect(self.database_path)) as connection:
            rows = connection.execute(
                """
                SELECT * FROM diagnostic_findings
                WHERE run_id = ? ORDER BY issue_fingerprint
                """,
                (str(run_id),),
            ).fetchall()
        return tuple(finding_record(row) for row in rows)

    def create_draft_baseline(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
        *,
        label: str,
    ) -> DiagnosticBaselineRecord:
        """Create an immutable draft from one completed compatible run."""
        self._require_boundary(boundary)
        return _create_draft_baseline(self.database_path, run_id, label)

    def activate_baseline(
        self,
        boundary: ProjectToolBoundaryIdentity,
        baseline_id: str,
        *,
        expected_generation: int,
    ) -> DiagnosticBaselineRecord:
        """Atomically activate one draft through compare-and-swap generation."""
        self._require_boundary(boundary)
        return _activate_baseline(
            self.database_path,
            baseline_id,
            expected_generation,
        )

    def get_baseline(
        self,
        boundary: ProjectToolBoundaryIdentity,
        baseline_id: str,
    ) -> DiagnosticBaselineRecord | None:
        """Return one baseline without exposing SQL state."""
        self._require_boundary(boundary)
        return _get_baseline(self.database_path, baseline_id)

    def get_active_baseline(
        self,
        boundary: ProjectToolBoundaryIdentity,
        *,
        producer_id: str,
        scope_fingerprint: str,
    ) -> DiagnosticBaselineRecord | None:
        """Return the sole active baseline for one producer and scope."""
        self._require_boundary(boundary)
        return _get_active_baseline(
            self.database_path,
            self._project_id,
            producer_id,
            scope_fingerprint,
        )

    def compare_run_to_active_baseline(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
    ) -> DiagnosticComparison:
        """Compare one completed run with its compatible active baseline."""
        self._require_boundary(boundary)
        return _compare_baseline(self.database_path, run_id)

    def get_manual_grouping_state(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
        *,
        decision_limit: int = 200,
    ) -> DiagnosticManualGroupingState:
        """Return manual groups and append-only decisions for one run scope."""
        self._require_boundary(boundary)
        return _get_manual_grouping_state(
            self.database_path,
            run_id,
            decision_limit=decision_limit,
        )

    def create_manual_group(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
        *,
        label: str,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Create one human group and append its decision history atomically."""
        self._require_boundary(boundary)
        return _create_manual_group(
            self.database_path,
            run_id,
            label=label,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def assign_issue_to_manual_group(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
        issue_fingerprint: str,
        group_id: str,
        *,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Move one current issue into one manual group through CAS state."""
        self._require_boundary(boundary)
        return _assign_issue_to_manual_group(
            self.database_path,
            run_id,
            issue_fingerprint,
            group_id,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def ungroup_manual_issue(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
        issue_fingerprint: str,
        *,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Remove one current manual assignment while retaining history."""
        self._require_boundary(boundary)
        return _ungroup_manual_issue(
            self.database_path,
            run_id,
            issue_fingerprint,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def mark_manual_group_reviewed(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
        group_id: str,
        *,
        author: str,
        reason: str,
        expected_generation: int,
    ) -> DiagnosticManualGroupingState:
        """Mark one manual group reviewed and append the human decision."""
        self._require_boundary(boundary)
        return _mark_manual_group_reviewed(
            self.database_path,
            run_id,
            group_id,
            author=author,
            reason=reason,
            expected_generation=expected_generation,
        )

    def get_lifecycle_state(
        self,
        boundary: ProjectToolBoundaryIdentity,
        run_id: str,
        *,
        decision_limit: int = 500,
    ) -> DiagnosticLifecycleState:
        """Return current lifecycle heads and searchable decision history."""
        self._require_boundary(boundary)
        return _get_lifecycle_state(
            self.database_path,
            run_id,
            decision_limit=decision_limit,
        )

    def record_lifecycle_decision(
        self,
        boundary: ProjectToolBoundaryIdentity,
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
        """Append one human decision through the sole persistence owner."""
        self._require_boundary(boundary)
        return _record_lifecycle_decision(
            self.database_path,
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

    def _require_boundary(self, boundary: ProjectToolBoundaryIdentity) -> None:
        if boundary.active_project_id != self._project_id:
            raise DiagnosticBoundaryError("ACTIVE_PROJECT_ID_CHANGED")
        if boundary.active_project_root_fingerprint != self._root_fingerprint:
            raise DiagnosticBoundaryError("ACTIVE_PROJECT_ROOT_FINGERPRINT_CHANGED")
        if _path_key(boundary.active_project_root) != self._project_root_key:
            raise DiagnosticBoundaryError("ACTIVE_PROJECT_ROOT_CHANGED")
        if _path_key(boundary.active_project_support_root) != self._support_root_key:
            raise DiagnosticBoundaryError("ACTIVE_PROJECT_SUPPORT_ROOT_CHANGED")

    def _require_run_current(
        self,
        run: DiagnosticRunInput,
        *,
        current_source_fingerprint: str,
        current_scope_fingerprint: str,
        current_configuration_fingerprint: str,
        current_generation: int,
    ) -> None:
        if run.project_id != self._project_id:
            raise DiagnosticBoundaryError("RUN_PROJECT_ID_MISMATCH")
        if run.project_root_fingerprint != self._root_fingerprint:
            raise DiagnosticBoundaryError("RUN_PROJECT_ROOT_FINGERPRINT_MISMATCH")
        comparisons = (
            (run.source_fingerprint, current_source_fingerprint, "SOURCE"),
            (run.scope_fingerprint, current_scope_fingerprint, "SCOPE"),
            (
                run.configuration_fingerprint,
                current_configuration_fingerprint,
                "CONFIGURATION",
            ),
        )
        for observed, current, label in comparisons:
            if str(observed) != str(current):
                raise DiagnosticBoundaryError("STALE_DIAGNOSTIC_" + label)
        if run.operation_generation != int(current_generation):
            raise DiagnosticBoundaryError("STALE_DIAGNOSTIC_GENERATION")
