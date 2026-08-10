# project-path: kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_state.py
"""Private read model for Engineering Diagnostics lifecycle governance."""

from __future__ import annotations

from contextlib import closing
import json
import sqlite3

from ._store_database import connect
from .lifecycle_models import (
    DiagnosticLifecycleDecisionRecord,
    DiagnosticLifecycleHead,
    DiagnosticLifecycleState,
)
from .models import DiagnosticStateError


def _run_row(connection: sqlite3.Connection, run_id: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM diagnostic_runs WHERE run_id = ?",
        (str(run_id),),
    ).fetchone()
    if row is None:
        raise DiagnosticStateError("LIFECYCLE_RUN_NOT_FOUND")
    return row


def _scope_key(run: sqlite3.Row) -> tuple[str, str, str]:
    return (
        str(run["project_id"]),
        str(run["producer_id"]),
        str(run["scope_fingerprint"]),
    )


def _head_record(row: sqlite3.Row) -> DiagnosticLifecycleHead:
    return DiagnosticLifecycleHead(
        project_id=str(row["project_id"]),
        producer_id=str(row["producer_id"]),
        scope_fingerprint=str(row["scope_fingerprint"]),
        target_kind=str(row["target_kind"]),
        target_id=str(row["target_id"]),
        target_label=str(row["target_label"]),
        current_state=str(row["current_state"]),
        generation=int(row["generation"]),
        last_decision_id=str(row["last_decision_id"]),
        updated_at_utc=str(row["updated_at_utc"]),
        last_run_id=str(row["last_run_id"]),
        member_digest=str(row["member_digest"]),
    )


def _decision_record(row: sqlite3.Row) -> DiagnosticLifecycleDecisionRecord:
    return DiagnosticLifecycleDecisionRecord(
        decision_id=str(row["decision_id"]),
        project_id=str(row["project_id"]),
        producer_id=str(row["producer_id"]),
        scope_fingerprint=str(row["scope_fingerprint"]),
        run_id=str(row["run_id"]),
        target_kind=str(row["target_kind"]),
        target_id=str(row["target_id"]),
        target_label=str(row["target_label"]),
        member_issue_fingerprints=tuple(
            json.loads(str(row["member_issue_fingerprints_json"]))
        ),
        action=str(row["action"]),
        previous_state=str(row["previous_state"]),
        resulting_state=str(row["resulting_state"]),
        reason_code=str(row["reason_code"]),
        rationale=str(row["rationale"]),
        author=str(row["author"]),
        decided_at_utc=str(row["decided_at_utc"]),
        expires_at_utc=str(row["expires_at_utc"]),
        revisit_condition=str(row["revisit_condition"]),
        related_ticket=str(row["related_ticket"]),
        related_wave=str(row["related_wave"]),
        explicit_confirmation=bool(int(row["explicit_confirmation"])),
        resulting_generation=int(row["resulting_generation"]),
    )


def get_state(
    database_path,
    run_id: str,
    *,
    decision_limit: int = 500,
) -> DiagnosticLifecycleState:
    """Return searchable lifecycle state for one compatible producer scope."""
    bounded_limit = max(1, min(int(decision_limit), 5000))
    with closing(connect(database_path)) as connection:
        run = _run_row(connection, run_id)
        key = _scope_key(run)
        head_rows = connection.execute(
            """
            SELECT * FROM diagnostic_lifecycle_heads
            WHERE project_id = ? AND producer_id = ? AND scope_fingerprint = ?
            ORDER BY target_kind, target_id
            """,
            key,
        ).fetchall()
        decision_rows = connection.execute(
            """
            SELECT * FROM diagnostic_lifecycle_decisions
            WHERE project_id = ? AND producer_id = ? AND scope_fingerprint = ?
            ORDER BY rowid DESC LIMIT ?
            """,
            key + (bounded_limit,),
        ).fetchall()
    return DiagnosticLifecycleState(
        project_id=key[0],
        producer_id=key[1],
        scope_fingerprint=key[2],
        heads=tuple(_head_record(row) for row in head_rows),
        decisions=tuple(_decision_record(row) for row in decision_rows),
    )
