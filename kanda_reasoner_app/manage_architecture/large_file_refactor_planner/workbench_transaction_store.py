# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_transaction_store.py
"""Durable SQLite metadata store for Workbench refactor transactions and recovery."""
from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
from typing import Any

from .workbench_project_support_paths import workbench_support_root

__all__ = [
    "WORKBENCH_TRANSACTION_STORE_FEATURE_ID",
    "WorkbenchTransactionStore",
    "default_workbench_transaction_root",
    "legacy_workbench_transaction_root",
    "migrate_legacy_workbench_transaction_state",
]

WORKBENCH_TRANSACTION_STORE_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-transaction-store-v1"
)
_NONTERMINAL_STATES = {
    "PREPARED",
    "LANE_RESERVED",
    "EXECUTING",
    "VALIDATING",
    "ROLLBACK_PENDING",
    "RECOVERY_PENDING",
}
_TERMINAL_STATES = {
    "COMPLETED_VALIDATED",
    "COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED",
    "ROLLBACK_VERIFIED",
    "STALE_AFTER_EXTERNAL_SOURCE_MUTATION",
    "ABANDONED",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_workbench_transaction_root(project_root: str | Path) -> Path:
    """Return canonical durable transaction root under active project support."""
    root = Path(project_root).resolve()
    return workbench_support_root(root) / "transactions"


def legacy_workbench_transaction_root(project_root: str | Path) -> Path:
    """Return the pre-canon sibling transaction root for bounded migration only."""
    root = Path(project_root).resolve()
    return root.parent / f"{root.name}_workbench_transactions" / "large_file_refactor_workbench"


def migrate_legacy_workbench_transaction_state(project_root: str | Path) -> Path:
    """Move legacy Workbench transaction state into project support without merging."""
    root = Path(project_root).resolve()
    canonical = default_workbench_transaction_root(root)
    legacy = legacy_workbench_transaction_root(root)
    legacy_lane = legacy.parent / "project_mutation_lane.sqlite3"
    canonical_lane = canonical.parent / "project_mutation_lane.sqlite3"
    if not legacy.exists() and not legacy_lane.exists():
        return canonical
    canonical_has_state = canonical.exists() and any(canonical.iterdir())
    legacy_has_state = legacy.exists() and any(legacy.iterdir())
    if canonical_has_state and legacy_has_state:
        raise RuntimeError("WORKBENCH_TRANSACTION_ROOT_MIGRATION_CONFLICT")
    canonical.parent.mkdir(parents=True, exist_ok=True)
    if legacy_has_state:
        if canonical.exists():
            canonical.rmdir()
        shutil.move(str(legacy), str(canonical))
    elif legacy.exists():
        legacy.rmdir()
    if legacy_lane.exists():
        if canonical_lane.exists():
            raise RuntimeError("PROJECT_MUTATION_LANE_MIGRATION_CONFLICT")
        shutil.move(str(legacy_lane), str(canonical_lane))
    try:
        legacy.parent.rmdir()
    except OSError:
        pass
    return canonical


class WorkbenchTransactionStore:
    """Persist transaction truth separately from GUI state and live source files."""

    def __init__(self, transaction_root: str | Path) -> None:
        self.transaction_root = Path(transaction_root).resolve()
        self.transaction_root.mkdir(parents=True, exist_ok=True)
        self.database_path = self.transaction_root / "workbench_transactions.sqlite3"
        self._initialize()

    def create_transaction(
        self,
        *,
        transaction_id: str,
        contract_hash: str,
        snapshot_hash: str,
        baseline_hash: str,
        physical_project_id: str,
        project_root: str,
        owner_box: str,
        mutation_request_id: str,
    ) -> Path:
        tx_root = self.transaction_root / "transactions" / transaction_id
        tx_root.mkdir(parents=True, exist_ok=True)
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                """
                INSERT INTO transactions (
                    transaction_id, contract_hash, snapshot_hash, baseline_hash,
                    physical_project_id, project_root, owner_box,
                    mutation_request_id, transaction_root, state,
                    recovery_state, rollback_state, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'PREPARED', 'NONE', 'NOT_REQUIRED', ?, ?)
                """,
                (
                    transaction_id,
                    contract_hash,
                    snapshot_hash,
                    baseline_hash,
                    physical_project_id,
                    str(Path(project_root).resolve()),
                    owner_box,
                    mutation_request_id,
                    str(tx_root),
                    now,
                    now,
                ),
            )
            connection.commit()
        return tx_root

    def store_artifact(
        self,
        transaction_id: str,
        artifact_kind: str,
        payload: dict[str, Any],
    ) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute(
                """
                INSERT INTO transaction_artifacts (
                    transaction_id, artifact_kind, payload_hash, payload_json, created_at
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(transaction_id, artifact_kind) DO UPDATE SET
                    payload_hash = excluded.payload_hash,
                    payload_json = excluded.payload_json,
                    created_at = excluded.created_at
                """,
                (transaction_id, artifact_kind, digest, canonical, now),
            )
        return digest

    def load_artifact(self, transaction_id: str, artifact_kind: str) -> dict[str, Any] | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                """
                SELECT payload_json, payload_hash FROM transaction_artifacts
                WHERE transaction_id = ? AND artifact_kind = ?
                """,
                (transaction_id, artifact_kind),
            ).fetchone()
            if row is None:
                return None
            payload_json = str(row["payload_json"])
            digest = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
            if digest != row["payload_hash"]:
                raise ValueError("TRANSACTION_ARTIFACT_HASH_MISMATCH")
            value = json.loads(payload_json)
            if not isinstance(value, dict):
                raise ValueError("TRANSACTION_ARTIFACT_NOT_OBJECT")
            return value

    def register_operation(
        self,
        *,
        transaction_id: str,
        sequence_no: int,
        operation_type: str,
        target_path: str,
        precondition_hash: str,
        payload_hash: str,
        backup_path: str,
    ) -> str:
        operation_id = f"{transaction_id}-op-{sequence_no:04d}"
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute(
                """
                INSERT INTO transaction_operations (
                    operation_id, transaction_id, sequence_no, operation_type,
                    target_path, precondition_hash, payload_hash, backup_path,
                    state, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?)
                """,
                (
                    operation_id,
                    transaction_id,
                    int(sequence_no),
                    operation_type,
                    str(Path(target_path).resolve()),
                    precondition_hash,
                    payload_hash,
                    backup_path,
                    now,
                    now,
                ),
            )
        return operation_id

    def record_operation_intent(self, operation_id: str) -> None:
        self._transition_operation(operation_id, expected="PENDING", new_state="INTENT_RECORDED")

    def record_operation_applied(self, operation_id: str) -> None:
        self._transition_operation(operation_id, expected="INTENT_RECORDED", new_state="APPLIED")

    def record_operation_verified(self, operation_id: str) -> None:
        self._transition_operation(operation_id, expected="APPLIED", new_state="VERIFIED")

    def record_operation_failed(self, operation_id: str, error: str) -> None:
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute(
                "UPDATE transaction_operations SET state = 'FAILED', error = ?, updated_at = ? WHERE operation_id = ?",
                (error, now, operation_id),
            )

    def transition_transaction(
        self,
        transaction_id: str,
        new_state: str,
        *,
        recovery_state: str | None = None,
        rollback_state: str | None = None,
    ) -> None:
        new_state = str(new_state).strip().upper()
        now = _utc_now()
        updates = ["state = ?", "updated_at = ?"]
        values: list[Any] = [new_state, now]
        if recovery_state is not None:
            updates.append("recovery_state = ?")
            values.append(str(recovery_state))
        if rollback_state is not None:
            updates.append("rollback_state = ?")
            values.append(str(rollback_state))
        values.append(transaction_id)
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                f"UPDATE transactions SET {', '.join(updates)} WHERE transaction_id = ?",
                tuple(values),
            )
            if cursor.rowcount != 1:
                raise KeyError("WORKBENCH_TRANSACTION_NOT_FOUND")

    def get_transaction(self, transaction_id: str) -> dict[str, Any] | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT * FROM transactions WHERE transaction_id = ?",
                (transaction_id,),
            ).fetchone()
            return dict(row) if row else None

    def list_operations(self, transaction_id: str) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT * FROM transaction_operations WHERE transaction_id = ? ORDER BY sequence_no",
                (transaction_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def discover_recovery_pending(self, *, project_root: str | Path | None = None) -> list[dict[str, Any]]:
        query = "SELECT * FROM transactions WHERE state IN ({})".format(
            ",".join("?" for _ in _NONTERMINAL_STATES)
        )
        params: list[Any] = sorted(_NONTERMINAL_STATES)
        if project_root is not None:
            query += " AND project_root = ?"
            params.append(str(Path(project_root).resolve()))
        query += " ORDER BY created_at"
        with closing(self._connect()) as connection:
            rows = connection.execute(query, tuple(params)).fetchall()
            return [dict(row) for row in rows]

    def transaction_is_terminal(self, transaction_id: str) -> bool:
        record = self.get_transaction(transaction_id)
        return bool(record and record["state"] in _TERMINAL_STATES)

    def _transition_operation(self, operation_id: str, *, expected: str, new_state: str) -> None:
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT state FROM transaction_operations WHERE operation_id = ?",
                (operation_id,),
            ).fetchone()
            if row is None:
                connection.rollback()
                raise KeyError("TRANSACTION_OPERATION_NOT_FOUND")
            if row[0] != expected:
                connection.rollback()
                raise ValueError(f"INVALID_OPERATION_STATE_TRANSITION:{row[0]}->{new_state}")
            connection.execute(
                "UPDATE transaction_operations SET state = ?, updated_at = ? WHERE operation_id = ?",
                (new_state, now, operation_id),
            )
            connection.commit()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=5.0, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    contract_hash TEXT NOT NULL,
                    snapshot_hash TEXT NOT NULL,
                    baseline_hash TEXT NOT NULL,
                    physical_project_id TEXT NOT NULL,
                    project_root TEXT NOT NULL,
                    owner_box TEXT NOT NULL,
                    mutation_request_id TEXT NOT NULL,
                    transaction_root TEXT NOT NULL,
                    state TEXT NOT NULL,
                    recovery_state TEXT NOT NULL,
                    rollback_state TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS transactions_project_state_idx
                    ON transactions(project_root, state, created_at);
                CREATE TABLE IF NOT EXISTS transaction_artifacts (
                    transaction_id TEXT NOT NULL,
                    artifact_kind TEXT NOT NULL,
                    payload_hash TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY(transaction_id, artifact_kind),
                    FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id)
                );
                CREATE TABLE IF NOT EXISTS transaction_operations (
                    operation_id TEXT PRIMARY KEY,
                    transaction_id TEXT NOT NULL,
                    sequence_no INTEGER NOT NULL,
                    operation_type TEXT NOT NULL,
                    target_path TEXT NOT NULL,
                    precondition_hash TEXT NOT NULL,
                    payload_hash TEXT NOT NULL,
                    backup_path TEXT NOT NULL,
                    state TEXT NOT NULL,
                    error TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(transaction_id, sequence_no),
                    FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id)
                );
                """
            )
