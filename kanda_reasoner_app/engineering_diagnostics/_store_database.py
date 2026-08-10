# project-path: kanda_reasoner_app/engineering_diagnostics/_store_database.py
"""Private SQLite mechanics for the Engineering Diagnostics store."""

from __future__ import annotations

from contextlib import closing
import json
from pathlib import Path
import sqlite3
from types import MappingProxyType

from ._store_grouping_schema import _initialize_grouping_schema
from ._store_lifecycle_schema import _initialize_lifecycle_schema
from .models import (
    DIAGNOSTIC_SCHEMA_VERSION,
    DiagnosticBaselineRecord,
    DiagnosticFindingRecord,
    DiagnosticRunRecord,
    DiagnosticStateError,
)

__all__: list[str] = []


def connect(database_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(
        database_path,
        timeout=5.0,
        isolation_level=None,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 5000")
    return connection


def initialize(database_path: Path) -> None:
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS diagnostics_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS diagnostic_runs (
                    run_id TEXT PRIMARY KEY,
                    attempt_id TEXT NOT NULL UNIQUE,
                    project_id TEXT NOT NULL,
                    project_root_fingerprint TEXT NOT NULL,
                    producer_id TEXT NOT NULL,
                    producer_version TEXT NOT NULL,
                    scan_identity TEXT NOT NULL,
                    source_fingerprint TEXT NOT NULL,
                    scope_fingerprint TEXT NOT NULL,
                    configuration_fingerprint TEXT NOT NULL,
                    operation_generation INTEGER NOT NULL,
                    completion_status TEXT NOT NULL,
                    finding_count INTEGER NOT NULL,
                    content_digest TEXT NOT NULL,
                    started_at_utc TEXT NOT NULL,
                    completed_at_utc TEXT NOT NULL,
                    provenance_json TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS diagnostic_runs_lookup_idx
                    ON diagnostic_runs (
                        project_id, producer_id, scope_fingerprint
                    );
                CREATE TABLE IF NOT EXISTS diagnostic_findings (
                    run_id TEXT NOT NULL,
                    issue_fingerprint TEXT NOT NULL,
                    evidence_digest TEXT NOT NULL,
                    code TEXT NOT NULL,
                    relative_path TEXT NOT NULL,
                    message TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    confidence TEXT NOT NULL,
                    semantic_key TEXT NOT NULL,
                    symbol_id TEXT NOT NULL,
                    location_key TEXT NOT NULL,
                    category TEXT NOT NULL,
                    line INTEGER,
                    evidence_json TEXT NOT NULL,
                    suggested_action TEXT NOT NULL,
                    PRIMARY KEY (run_id, issue_fingerprint),
                    FOREIGN KEY (run_id) REFERENCES diagnostic_runs(run_id)
                        ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS diagnostic_baselines (
                    baseline_id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    producer_id TEXT NOT NULL,
                    scope_fingerprint TEXT NOT NULL,
                    source_run_id TEXT NOT NULL,
                    label TEXT NOT NULL,
                    state TEXT NOT NULL,
                    content_digest TEXT NOT NULL,
                    finding_count INTEGER NOT NULL,
                    created_at_utc TEXT NOT NULL,
                    activated_at_utc TEXT NOT NULL,
                    superseded_at_utc TEXT NOT NULL,
                    generation INTEGER NOT NULL,
                    FOREIGN KEY (source_run_id) REFERENCES diagnostic_runs(run_id)
                );
                CREATE TABLE IF NOT EXISTS diagnostic_baseline_findings (
                    baseline_id TEXT NOT NULL,
                    issue_fingerprint TEXT NOT NULL,
                    PRIMARY KEY (baseline_id, issue_fingerprint),
                    FOREIGN KEY (baseline_id)
                        REFERENCES diagnostic_baselines(baseline_id)
                        ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS diagnostic_baseline_heads (
                    project_id TEXT NOT NULL,
                    producer_id TEXT NOT NULL,
                    scope_fingerprint TEXT NOT NULL,
                    active_baseline_id TEXT NOT NULL,
                    generation INTEGER NOT NULL,
                    updated_at_utc TEXT NOT NULL,
                    PRIMARY KEY (project_id, producer_id, scope_fingerprint),
                    FOREIGN KEY (active_baseline_id)
                        REFERENCES diagnostic_baselines(baseline_id)
                );
                """
            )
            row = connection.execute(
                "SELECT value FROM diagnostics_metadata WHERE key = 'schema_version'"
            ).fetchone()
            if row is None:
                connection.execute(
                    "INSERT INTO diagnostics_metadata (key, value) VALUES (?, ?)",
                    ("schema_version", DIAGNOSTIC_SCHEMA_VERSION),
                )
            elif str(row["value"]) != DIAGNOSTIC_SCHEMA_VERSION:
                raise DiagnosticStateError(
                    "ENGINEERING_DIAGNOSTICS_SCHEMA_UNSUPPORTED:"
                    + str(row["value"])
                )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        _initialize_grouping_schema(connection)
        _initialize_lifecycle_schema(connection)


def finding_fingerprints(
    connection: sqlite3.Connection,
    run_id: str,
) -> tuple[str, ...]:
    rows = connection.execute(
        """
        SELECT issue_fingerprint FROM diagnostic_findings
        WHERE run_id = ? ORDER BY issue_fingerprint
        """,
        (run_id,),
    ).fetchall()
    return tuple(str(row["issue_fingerprint"]) for row in rows)


def baseline_fingerprints(
    connection: sqlite3.Connection,
    baseline_id: str,
) -> tuple[str, ...]:
    rows = connection.execute(
        """
        SELECT issue_fingerprint FROM diagnostic_baseline_findings
        WHERE baseline_id = ? ORDER BY issue_fingerprint
        """,
        (baseline_id,),
    ).fetchall()
    return tuple(str(row["issue_fingerprint"]) for row in rows)


def run_record(row: sqlite3.Row) -> DiagnosticRunRecord:
    return DiagnosticRunRecord(
        run_id=str(row["run_id"]),
        attempt_id=str(row["attempt_id"]),
        project_id=str(row["project_id"]),
        project_root_fingerprint=str(row["project_root_fingerprint"]),
        producer_id=str(row["producer_id"]),
        producer_version=str(row["producer_version"]),
        scan_identity=str(row["scan_identity"]),
        source_fingerprint=str(row["source_fingerprint"]),
        scope_fingerprint=str(row["scope_fingerprint"]),
        configuration_fingerprint=str(row["configuration_fingerprint"]),
        operation_generation=int(row["operation_generation"]),
        completion_status=str(row["completion_status"]),
        finding_count=int(row["finding_count"]),
        content_digest=str(row["content_digest"]),
        started_at_utc=str(row["started_at_utc"]),
        completed_at_utc=str(row["completed_at_utc"]),
        provenance=MappingProxyType(json.loads(str(row["provenance_json"]))),
    )


def finding_record(row: sqlite3.Row) -> DiagnosticFindingRecord:
    return DiagnosticFindingRecord(
        run_id=str(row["run_id"]),
        issue_fingerprint=str(row["issue_fingerprint"]),
        evidence_digest=str(row["evidence_digest"]),
        code=str(row["code"]),
        relative_path=str(row["relative_path"]),
        message=str(row["message"]),
        severity=str(row["severity"]),
        confidence=str(row["confidence"]),
        semantic_key=str(row["semantic_key"]),
        symbol_id=str(row["symbol_id"]),
        location_key=str(row["location_key"]),
        category=str(row["category"]),
        line=int(row["line"]) if row["line"] is not None else None,
        evidence=MappingProxyType(json.loads(str(row["evidence_json"]))),
        suggested_action=str(row["suggested_action"]),
    )


def baseline_record(
    row: sqlite3.Row,
    generation_override: int | None = None,
) -> DiagnosticBaselineRecord:
    generation = (
        int(generation_override)
        if generation_override is not None
        else int(row["generation"])
    )
    return DiagnosticBaselineRecord(
        baseline_id=str(row["baseline_id"]),
        project_id=str(row["project_id"]),
        producer_id=str(row["producer_id"]),
        scope_fingerprint=str(row["scope_fingerprint"]),
        source_run_id=str(row["source_run_id"]),
        label=str(row["label"]),
        state=str(row["state"]),
        content_digest=str(row["content_digest"]),
        finding_count=int(row["finding_count"]),
        created_at_utc=str(row["created_at_utc"]),
        activated_at_utc=str(row["activated_at_utc"]),
        superseded_at_utc=str(row["superseded_at_utc"]),
        generation=generation,
    )
