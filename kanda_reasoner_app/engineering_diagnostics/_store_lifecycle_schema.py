# project-path: kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_schema.py
"""Private atomic lifecycle-schema migration for Engineering Diagnostics."""

from __future__ import annotations

import sqlite3

from .lifecycle_models import DIAGNOSTIC_LIFECYCLE_SCHEMA_VERSION
from .models import DiagnosticStateError

_LIFECYCLE_SCHEMA_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS diagnostic_lifecycle_metadata (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS diagnostic_lifecycle_heads (
        project_id TEXT NOT NULL,
        producer_id TEXT NOT NULL,
        scope_fingerprint TEXT NOT NULL,
        target_kind TEXT NOT NULL,
        target_id TEXT NOT NULL,
        target_label TEXT NOT NULL,
        current_state TEXT NOT NULL,
        generation INTEGER NOT NULL,
        last_decision_id TEXT NOT NULL,
        updated_at_utc TEXT NOT NULL,
        last_run_id TEXT NOT NULL,
        member_digest TEXT NOT NULL,
        PRIMARY KEY (
            project_id, producer_id, scope_fingerprint,
            target_kind, target_id
        )
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS diagnostic_lifecycle_decisions (
        decision_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        producer_id TEXT NOT NULL,
        scope_fingerprint TEXT NOT NULL,
        run_id TEXT NOT NULL,
        target_kind TEXT NOT NULL,
        target_id TEXT NOT NULL,
        target_label TEXT NOT NULL,
        member_issue_fingerprints_json TEXT NOT NULL,
        action TEXT NOT NULL,
        previous_state TEXT NOT NULL,
        resulting_state TEXT NOT NULL,
        reason_code TEXT NOT NULL,
        rationale TEXT NOT NULL,
        author TEXT NOT NULL,
        decided_at_utc TEXT NOT NULL,
        expires_at_utc TEXT NOT NULL,
        revisit_condition TEXT NOT NULL,
        related_ticket TEXT NOT NULL,
        related_wave TEXT NOT NULL,
        explicit_confirmation INTEGER NOT NULL,
        resulting_generation INTEGER NOT NULL,
        FOREIGN KEY (run_id) REFERENCES diagnostic_runs(run_id)
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS diagnostic_lifecycle_decisions_scope_idx
    ON diagnostic_lifecycle_decisions (
        project_id, producer_id, scope_fingerprint,
        decided_at_utc, decision_id
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS diagnostic_lifecycle_decisions_target_idx
    ON diagnostic_lifecycle_decisions (
        project_id, producer_id, scope_fingerprint,
        target_kind, target_id, resulting_generation
    )
    """,
)

_LIFECYCLE_REQUIRED_COLUMNS = {
    "diagnostic_lifecycle_metadata": frozenset({"key", "value"}),
    "diagnostic_lifecycle_heads": frozenset(
        {
            "project_id",
            "producer_id",
            "scope_fingerprint",
            "target_kind",
            "target_id",
            "target_label",
            "current_state",
            "generation",
            "last_decision_id",
            "updated_at_utc",
            "last_run_id",
            "member_digest",
        }
    ),
    "diagnostic_lifecycle_decisions": frozenset(
        {
            "decision_id",
            "project_id",
            "producer_id",
            "scope_fingerprint",
            "run_id",
            "target_kind",
            "target_id",
            "target_label",
            "member_issue_fingerprints_json",
            "action",
            "previous_state",
            "resulting_state",
            "reason_code",
            "rationale",
            "author",
            "decided_at_utc",
            "expires_at_utc",
            "revisit_condition",
            "related_ticket",
            "related_wave",
            "explicit_confirmation",
            "resulting_generation",
        }
    ),
}


def _validate_lifecycle_table_contract(connection: sqlite3.Connection) -> None:
    for table_name, required in _LIFECYCLE_REQUIRED_COLUMNS.items():
        rows = connection.execute("PRAGMA table_info(" + table_name + ")").fetchall()
        observed = {str(row["name"]) for row in rows}
        if observed != set(required):
            raise DiagnosticStateError(
                "ENGINEERING_DIAGNOSTICS_LIFECYCLE_TABLE_CONTRACT_MISMATCH:"
                + table_name
                + ":"
                + ",".join(sorted(observed))
            )


def _initialize_lifecycle_schema(connection: sqlite3.Connection) -> None:
    connection.execute("BEGIN IMMEDIATE")
    try:
        for statement in _LIFECYCLE_SCHEMA_STATEMENTS:
            connection.execute(statement)
        _validate_lifecycle_table_contract(connection)
        row = connection.execute(
            """
            SELECT value FROM diagnostic_lifecycle_metadata
            WHERE key = 'schema_version'
            """
        ).fetchone()
        if row is None:
            connection.execute(
                """
                INSERT INTO diagnostic_lifecycle_metadata (key, value)
                VALUES ('schema_version', ?)
                """,
                (DIAGNOSTIC_LIFECYCLE_SCHEMA_VERSION,),
            )
        elif str(row["value"]) != DIAGNOSTIC_LIFECYCLE_SCHEMA_VERSION:
            raise DiagnosticStateError(
                "ENGINEERING_DIAGNOSTICS_LIFECYCLE_SCHEMA_UNSUPPORTED:"
                + str(row["value"])
            )
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
