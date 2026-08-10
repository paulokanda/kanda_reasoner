# project-path: kanda_reasoner_app/engineering_diagnostics/_store_grouping_schema.py
"""Private atomic grouping-schema migration for Engineering Diagnostics."""

from __future__ import annotations

import sqlite3

from .grouping_models import DIAGNOSTIC_GROUPING_SCHEMA_VERSION
from .models import DiagnosticStateError

__all__: list[str] = []

_GROUPING_SCHEMA_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS diagnostic_group_heads (
        project_id TEXT NOT NULL,
        producer_id TEXT NOT NULL,
        scope_fingerprint TEXT NOT NULL,
        generation INTEGER NOT NULL,
        updated_at_utc TEXT NOT NULL,
        PRIMARY KEY (project_id, producer_id, scope_fingerprint)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS diagnostic_manual_groups (
        group_id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        producer_id TEXT NOT NULL,
        scope_fingerprint TEXT NOT NULL,
        label TEXT NOT NULL,
        review_state TEXT NOT NULL,
        created_at_utc TEXT NOT NULL,
        reviewed_at_utc TEXT NOT NULL,
        author TEXT NOT NULL
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS diagnostic_manual_groups_scope_idx
        ON diagnostic_manual_groups (
            project_id, producer_id, scope_fingerprint
        )
    """,
    """
    CREATE TABLE IF NOT EXISTS diagnostic_manual_group_members (
        project_id TEXT NOT NULL,
        producer_id TEXT NOT NULL,
        scope_fingerprint TEXT NOT NULL,
        issue_fingerprint TEXT NOT NULL,
        group_id TEXT NOT NULL,
        assigned_at_utc TEXT NOT NULL,
        PRIMARY KEY (
            project_id, producer_id, scope_fingerprint, issue_fingerprint
        ),
        FOREIGN KEY (group_id)
            REFERENCES diagnostic_manual_groups(group_id)
            ON DELETE CASCADE
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS diagnostic_manual_group_members_group_idx
        ON diagnostic_manual_group_members (group_id)
    """,
    """
    CREATE TABLE IF NOT EXISTS diagnostic_group_decisions (
        decision_id TEXT PRIMARY KEY,
        group_id TEXT NOT NULL,
        project_id TEXT NOT NULL,
        producer_id TEXT NOT NULL,
        scope_fingerprint TEXT NOT NULL,
        action TEXT NOT NULL,
        issue_fingerprint TEXT NOT NULL,
        previous_group_id TEXT NOT NULL,
        reason TEXT NOT NULL,
        author TEXT NOT NULL,
        created_at_utc TEXT NOT NULL,
        resulting_generation INTEGER NOT NULL,
        FOREIGN KEY (group_id)
            REFERENCES diagnostic_manual_groups(group_id)
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS diagnostic_group_decisions_scope_idx
        ON diagnostic_group_decisions (
            project_id, producer_id, scope_fingerprint, resulting_generation
        )
    """,
)


def _initialize_grouping_schema(connection: sqlite3.Connection) -> None:
    """Apply the grouping schema atomically without changing core identity schema."""
    connection.execute("BEGIN IMMEDIATE")
    try:
        for statement in _GROUPING_SCHEMA_STATEMENTS:
            connection.execute(statement)
        row = connection.execute(
            "SELECT value FROM diagnostics_metadata "
            "WHERE key = 'grouping_schema_version'"
        ).fetchone()
        if row is None:
            connection.execute(
                "INSERT INTO diagnostics_metadata (key, value) VALUES (?, ?)",
                ("grouping_schema_version", DIAGNOSTIC_GROUPING_SCHEMA_VERSION),
            )
        elif str(row["value"]) != DIAGNOSTIC_GROUPING_SCHEMA_VERSION:
            raise DiagnosticStateError(
                "ENGINEERING_DIAGNOSTICS_GROUPING_SCHEMA_UNSUPPORTED:"
                + str(row["value"])
            )
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
