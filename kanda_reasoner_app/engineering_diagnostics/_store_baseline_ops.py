# project-path: kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py
"""Private baseline transactions used only by the public store owner."""

from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import sqlite3
from uuid import uuid4

from .baseline import compare_issue_fingerprints
from .fingerprinting import canonical_json
from .models import (
    DiagnosticBaselineRecord,
    DiagnosticComparison,
    DiagnosticConflictError,
    DiagnosticStateError,
    DiagnosticValidationError,
)
from ._store_database import (
    baseline_fingerprints,
    baseline_record,
    connect,
    finding_fingerprints,
)

__all__: list[str] = []


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _fingerprint_content_digest(fingerprints: tuple[str, ...]) -> str:
    if len(fingerprints) <= 10000:
        return hashlib.sha256(
            canonical_json(fingerprints).encode("utf-8")
        ).hexdigest()
    digest = hashlib.sha256()
    digest.update(b"engineering_diagnostics_baseline_stream_v1\0")
    digest.update(str(len(fingerprints)).encode("ascii"))
    digest.update(b"\0")
    for fingerprint in fingerprints:
        digest.update(str(fingerprint).encode("ascii", errors="strict"))
        digest.update(b"\n")
    return digest.hexdigest()


def create_draft(
    database_path,
    run_id: str,
    label: str,
) -> DiagnosticBaselineRecord:
    clean_label = str(label or "").strip()
    if not clean_label:
        raise DiagnosticValidationError("baseline label is required.")
    baseline_id = str(uuid4())
    created_at = _utc_now()
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            run = connection.execute(
                "SELECT * FROM diagnostic_runs WHERE run_id = ?",
                (str(run_id),),
            ).fetchone()
            if run is None:
                raise DiagnosticStateError("BASELINE_SOURCE_RUN_NOT_FOUND")
            fingerprints = finding_fingerprints(connection, str(run_id))
            content_digest = _fingerprint_content_digest(fingerprints)
            connection.execute(
                """
                INSERT INTO diagnostic_baselines (
                    baseline_id, project_id, producer_id,
                    scope_fingerprint, source_run_id, label, state,
                    content_digest, finding_count, created_at_utc,
                    activated_at_utc, superseded_at_utc, generation
                ) VALUES (?, ?, ?, ?, ?, ?, 'DRAFT', ?, ?, ?, '', '', 0)
                """,
                (
                    baseline_id,
                    run["project_id"],
                    run["producer_id"],
                    run["scope_fingerprint"],
                    run["run_id"],
                    clean_label,
                    content_digest,
                    len(fingerprints),
                    created_at,
                ),
            )
            for fingerprint in fingerprints:
                connection.execute(
                    """
                    INSERT INTO diagnostic_baseline_findings (
                        baseline_id, issue_fingerprint
                    ) VALUES (?, ?)
                    """,
                    (baseline_id, fingerprint),
                )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
    return get(database_path, baseline_id)


def activate(
    database_path,
    baseline_id: str,
    expected_generation: int,
) -> DiagnosticBaselineRecord:
    now = _utc_now()
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            baseline = connection.execute(
                "SELECT * FROM diagnostic_baselines WHERE baseline_id = ?",
                (str(baseline_id),),
            ).fetchone()
            if baseline is None:
                raise DiagnosticStateError("BASELINE_NOT_FOUND")
            key = (
                baseline["project_id"],
                baseline["producer_id"],
                baseline["scope_fingerprint"],
            )
            head = connection.execute(
                """
                SELECT * FROM diagnostic_baseline_heads
                WHERE project_id = ? AND producer_id = ?
                  AND scope_fingerprint = ?
                """,
                key,
            ).fetchone()
            current_generation = int(head["generation"]) if head else 0
            if current_generation != int(expected_generation):
                raise DiagnosticConflictError(
                    "BASELINE_GENERATION_COMPARE_AND_SWAP_FAILED"
                )
            if str(baseline["state"]) == "ACTIVE":
                if head and str(head["active_baseline_id"]) == str(baseline_id):
                    connection.rollback()
                    return baseline_record(baseline, current_generation)
                raise DiagnosticStateError("BASELINE_ACTIVE_HEAD_MISMATCH")
            if str(baseline["state"]) != "DRAFT":
                raise DiagnosticStateError(
                    "BASELINE_ACTIVATION_REQUIRES_DRAFT_STATE"
                )
            if head and head["active_baseline_id"]:
                connection.execute(
                    """
                    UPDATE diagnostic_baselines
                    SET state = 'SUPERSEDED', superseded_at_utc = ?
                    WHERE baseline_id = ? AND state = 'ACTIVE'
                    """,
                    (now, head["active_baseline_id"]),
                )
            next_generation = current_generation + 1
            connection.execute(
                """
                UPDATE diagnostic_baselines
                SET state = 'ACTIVE', activated_at_utc = ?, generation = ?
                WHERE baseline_id = ?
                """,
                (now, next_generation, str(baseline_id)),
            )
            connection.execute(
                """
                INSERT INTO diagnostic_baseline_heads (
                    project_id, producer_id, scope_fingerprint,
                    active_baseline_id, generation, updated_at_utc
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(project_id, producer_id, scope_fingerprint)
                DO UPDATE SET
                    active_baseline_id = excluded.active_baseline_id,
                    generation = excluded.generation,
                    updated_at_utc = excluded.updated_at_utc
                """,
                key + (str(baseline_id), next_generation, now),
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
    return get(database_path, str(baseline_id))


def get(database_path, baseline_id: str) -> DiagnosticBaselineRecord | None:
    with closing(connect(database_path)) as connection:
        row = connection.execute(
            "SELECT * FROM diagnostic_baselines WHERE baseline_id = ?",
            (str(baseline_id),),
        ).fetchone()
    return baseline_record(row) if row is not None else None


def get_active(
    database_path,
    project_id: str,
    producer_id: str,
    scope_fingerprint: str,
) -> DiagnosticBaselineRecord | None:
    with closing(connect(database_path)) as connection:
        row = connection.execute(
            """
            SELECT b.* FROM diagnostic_baselines AS b
            JOIN diagnostic_baseline_heads AS h
              ON h.active_baseline_id = b.baseline_id
            WHERE h.project_id = ? AND h.producer_id = ?
              AND h.scope_fingerprint = ?
            """,
            (project_id, str(producer_id).strip(), str(scope_fingerprint).strip()),
        ).fetchone()
    return baseline_record(row) if row is not None else None


def compare(database_path, run_id: str) -> DiagnosticComparison:
    with closing(connect(database_path)) as connection:
        run = connection.execute(
            "SELECT * FROM diagnostic_runs WHERE run_id = ?",
            (str(run_id),),
        ).fetchone()
        if run is None:
            raise DiagnosticStateError("COMPARISON_RUN_NOT_FOUND")
        current = finding_fingerprints(connection, str(run_id))
        baseline = connection.execute(
            """
            SELECT b.* FROM diagnostic_baselines AS b
            JOIN diagnostic_baseline_heads AS h
              ON h.active_baseline_id = b.baseline_id
            WHERE h.project_id = ? AND h.producer_id = ?
              AND h.scope_fingerprint = ?
            """,
            (
                run["project_id"],
                run["producer_id"],
                run["scope_fingerprint"],
            ),
        ).fetchone()
        if baseline is None:
            return DiagnosticComparison(
                run_id=str(run_id),
                baseline_id=None,
                status="NO_ACTIVE_BASELINE",
                new_issue_fingerprints=tuple(current),
                persistent_issue_fingerprints=(),
                resolved_issue_fingerprints=(),
            )
        baseline_items = baseline_fingerprints(
            connection,
            str(baseline["baseline_id"]),
        )
    new_items, persistent, resolved = compare_issue_fingerprints(
        current,
        baseline_items,
    )
    return DiagnosticComparison(
        run_id=str(run_id),
        baseline_id=str(baseline["baseline_id"]),
        status="COMPARED",
        new_issue_fingerprints=new_items,
        persistent_issue_fingerprints=persistent,
        resolved_issue_fingerprints=resolved,
    )
