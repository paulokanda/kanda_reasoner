# project-path: kanda_reasoner_app/engineering_diagnostics/_store_grouping_state.py
"""Private read model for persisted Engineering Diagnostics grouping state."""

from __future__ import annotations

from contextlib import closing
import sqlite3
from types import MappingProxyType

from ._store_database import connect
from .grouping_models import (
    DiagnosticGroupDecisionRecord,
    DiagnosticGroupRecord,
    DiagnosticManualGroupingState,
)
from .models import DiagnosticStateError

__all__: list[str] = []


def _run_row(connection: sqlite3.Connection, run_id: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM diagnostic_runs WHERE run_id = ?",
        (str(run_id),),
    ).fetchone()
    if row is None:
        raise DiagnosticStateError("GROUPING_RUN_NOT_FOUND")
    return row


def _scope_key(run: sqlite3.Row) -> tuple[str, str, str]:
    return (
        str(run["project_id"]),
        str(run["producer_id"]),
        str(run["scope_fingerprint"]),
    )


def _generation(connection: sqlite3.Connection, key: tuple[str, str, str]) -> int:
    row = connection.execute(
        """
        SELECT generation FROM diagnostic_group_heads
        WHERE project_id = ? AND producer_id = ? AND scope_fingerprint = ?
        """,
        key,
    ).fetchone()
    return int(row["generation"]) if row is not None else 0


def _group_row(connection: sqlite3.Connection, group_id: str) -> sqlite3.Row:
    row = connection.execute(
        "SELECT * FROM diagnostic_manual_groups WHERE group_id = ?",
        (str(group_id),),
    ).fetchone()
    if row is None:
        raise DiagnosticStateError("MANUAL_GROUP_NOT_FOUND")
    return row


def _require_group_scope(row: sqlite3.Row, key: tuple[str, str, str]) -> None:
    observed = (
        str(row["project_id"]),
        str(row["producer_id"]),
        str(row["scope_fingerprint"]),
    )
    if observed != key:
        raise DiagnosticStateError("MANUAL_GROUP_SCOPE_MISMATCH")


def _require_issue(
    connection: sqlite3.Connection,
    run_id: str,
    issue_fingerprint: str,
) -> str:
    fingerprint = str(issue_fingerprint or "").strip()
    if not fingerprint:
        raise DiagnosticStateError("ISSUE_FINGERPRINT_REQUIRED")
    row = connection.execute(
        """
        SELECT 1 FROM diagnostic_findings
        WHERE run_id = ? AND issue_fingerprint = ?
        """,
        (str(run_id), fingerprint),
    ).fetchone()
    if row is None:
        raise DiagnosticStateError("GROUPING_ISSUE_NOT_FOUND_IN_RUN")
    return fingerprint


def _decision_record(row: sqlite3.Row) -> DiagnosticGroupDecisionRecord:
    return DiagnosticGroupDecisionRecord(
        decision_id=str(row["decision_id"]),
        group_id=str(row["group_id"]),
        project_id=str(row["project_id"]),
        producer_id=str(row["producer_id"]),
        scope_fingerprint=str(row["scope_fingerprint"]),
        action=str(row["action"]),
        issue_fingerprint=str(row["issue_fingerprint"]),
        previous_group_id=str(row["previous_group_id"]),
        reason=str(row["reason"]),
        author=str(row["author"]),
        created_at_utc=str(row["created_at_utc"]),
        resulting_generation=int(row["resulting_generation"]),
    )


def _state_from_connection(
    connection: sqlite3.Connection,
    run: sqlite3.Row,
    decision_limit: int,
) -> DiagnosticManualGroupingState:
    key = _scope_key(run)
    generation = _generation(connection, key)
    group_rows = connection.execute(
        """
        SELECT * FROM diagnostic_manual_groups
        WHERE project_id = ? AND producer_id = ? AND scope_fingerprint = ?
        ORDER BY created_at_utc, group_id
        """,
        key,
    ).fetchall()
    member_rows = connection.execute(
        """
        SELECT group_id, issue_fingerprint
        FROM diagnostic_manual_group_members
        WHERE project_id = ? AND producer_id = ? AND scope_fingerprint = ?
        ORDER BY group_id, issue_fingerprint
        """,
        key,
    ).fetchall()
    members: dict[str, list[str]] = {}
    for row in member_rows:
        members.setdefault(str(row["group_id"]), []).append(
            str(row["issue_fingerprint"])
        )
    groups = tuple(
        DiagnosticGroupRecord(
            group_id=str(row["group_id"]),
            project_id=str(row["project_id"]),
            producer_id=str(row["producer_id"]),
            scope_fingerprint=str(row["scope_fingerprint"]),
            kind="MANUAL",
            recipe_id="manual.user_defined.v1",
            label=str(row["label"]),
            confidence="high",
            member_issue_fingerprints=tuple(members.get(str(row["group_id"]), ())),
            evidence=MappingProxyType(
                {
                    "decision_history_persisted": True,
                    "root_cause_claimed": False,
                }
            ),
            review_state=str(row["review_state"]),
            created_at_utc=str(row["created_at_utc"]),
            reviewed_at_utc=str(row["reviewed_at_utc"]),
            author=str(row["author"]),
            generation=generation,
        )
        for row in group_rows
    )
    bounded_limit = max(1, min(int(decision_limit), 1000))
    decision_rows = connection.execute(
        """
        SELECT * FROM diagnostic_group_decisions
        WHERE project_id = ? AND producer_id = ? AND scope_fingerprint = ?
        ORDER BY resulting_generation DESC, decision_id DESC LIMIT ?
        """,
        key + (bounded_limit,),
    ).fetchall()
    return DiagnosticManualGroupingState(
        project_id=key[0],
        producer_id=key[1],
        scope_fingerprint=key[2],
        generation=generation,
        groups=groups,
        decisions=tuple(_decision_record(row) for row in decision_rows),
    )


def _get_state(
    database_path,
    run_id: str,
    *,
    decision_limit: int = 200,
) -> DiagnosticManualGroupingState:
    with closing(connect(database_path)) as connection:
        run = _run_row(connection, run_id)
        return _state_from_connection(connection, run, decision_limit)
