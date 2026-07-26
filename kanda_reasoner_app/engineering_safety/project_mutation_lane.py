# project-path: kanda_reasoner_app/engineering_safety/project_mutation_lane.py
"""Durable per-project serial mutation lane shared by independently boxed tabs."""
from __future__ import annotations

from contextlib import closing
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterable

__all__ = [
    "PROJECT_MUTATION_LANE_FEATURE_ID",
    "MutationRequest",
    "MutationPort",
    "ProjectMutationLaneStore",
    "build_mutation_request",
    "default_project_mutation_lane_database",
    "physical_project_id",
]

PROJECT_MUTATION_LANE_FEATURE_ID = "engineering-safety-project-mutation-lane-v1"
_TERMINAL_STATES = {"COMPLETED", "ROLLED_BACK", "CANCELLED", "ABANDONED"}
_ACTIVE_STATES = {"RESERVED", "EXECUTING", "VALIDATING", "ROLLBACK_PENDING", "RECOVERY_PENDING"}
_ALLOWED_TRANSITIONS = {
    "QUEUED": {"RESERVED", "CANCELLED"},
    "RESERVED": {"EXECUTING", "CANCELLED", "RECOVERY_PENDING"},
    "EXECUTING": {"VALIDATING", "ROLLBACK_PENDING", "RECOVERY_PENDING"},
    "VALIDATING": {"COMPLETED", "ROLLBACK_PENDING", "RECOVERY_PENDING"},
    "ROLLBACK_PENDING": {"ROLLED_BACK", "RECOVERY_PENDING"},
    "RECOVERY_PENDING": {"EXECUTING", "ROLLBACK_PENDING", "ABANDONED", "COMPLETED", "ROLLED_BACK"},
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class MutationRequest:
    """Serializable mutation intent crossing one tab box boundary."""

    schema_version: str
    feature_id: str
    request_id: str
    physical_project_id: str
    project_root: str
    owner_box: str
    operation_family: str
    transaction_id: str
    mutation_paths: tuple[str, ...]
    basis_paths: tuple[str, ...]
    created_at: str
    request_hash: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["mutation_paths"] = list(self.mutation_paths)
        data["basis_paths"] = list(self.basis_paths)
        return data

    def integrity_valid(self) -> bool:
        return self.request_hash == _request_hash(
            physical_project_id=self.physical_project_id,
            project_root=self.project_root,
            owner_box=self.owner_box,
            operation_family=self.operation_family,
            transaction_id=self.transaction_id,
            mutation_paths=self.mutation_paths,
            basis_paths=self.basis_paths,
            created_at=self.created_at,
        )


class MutationPort:
    """Small public port exposed to one independently boxed source-mutating tab."""

    def __init__(self, store: "ProjectMutationLaneStore", owner_box: str) -> None:
        self._store = store
        self._owner_box = str(owner_box).strip()
        if not self._owner_box:
            raise ValueError("MUTATION_PORT_OWNER_BOX_REQUIRED")

    @property
    def owner_box(self) -> str:
        return self._owner_box

    def submit(self, request: MutationRequest) -> int:
        if request.owner_box != self._owner_box:
            raise ValueError("MUTATION_REQUEST_OWNER_BOX_MISMATCH")
        return self._store.enqueue(request)


class ProjectMutationLaneStore:
    """SQLite-backed queue and one-active-owner lane per physical project."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = Path(database_path).resolve()
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def port(self, owner_box: str) -> MutationPort:
        return MutationPort(self, owner_box)

    def enqueue(self, request: MutationRequest) -> int:
        self._require_request(request)
        with closing(self._connect()) as connection:
            cursor = connection.execute(
                """
                INSERT INTO mutation_requests (
                    request_id, physical_project_id, project_root, owner_box,
                    operation_family, transaction_id, mutation_paths_json,
                    basis_paths_json, request_hash, state, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'QUEUED', ?, ?)
                """,
                (
                    request.request_id,
                    request.physical_project_id,
                    request.project_root,
                    request.owner_box,
                    request.operation_family,
                    request.transaction_id,
                    json.dumps(list(request.mutation_paths), separators=(",", ":")),
                    json.dumps(list(request.basis_paths), separators=(",", ":")),
                    request.request_hash,
                    request.created_at,
                    request.created_at,
                ),
            )
            return int(cursor.lastrowid)

    def reserve_next(self, project_id: str) -> dict[str, Any] | None:
        """Reserve the oldest queued request only when the project lane is free."""
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            active = connection.execute(
                "SELECT active_request_id FROM project_mutation_lanes WHERE physical_project_id = ?",
                (project_id,),
            ).fetchone()
            if active and active[0]:
                connection.rollback()
                return None
            row = connection.execute(
                """
                SELECT queue_sequence, request_id FROM mutation_requests
                WHERE physical_project_id = ? AND state = 'QUEUED'
                ORDER BY queue_sequence ASC LIMIT 1
                """,
                (project_id,),
            ).fetchone()
            if row is None:
                connection.rollback()
                return None
            now = _utc_now()
            request_id = str(row[1])
            connection.execute(
                "UPDATE mutation_requests SET state = 'RESERVED', updated_at = ? WHERE request_id = ?",
                (now, request_id),
            )
            connection.execute(
                """
                INSERT INTO project_mutation_lanes (
                    physical_project_id, active_request_id, lane_state,
                    owner_box, transaction_id, generation, updated_at
                )
                SELECT physical_project_id, request_id, 'RESERVED', owner_box,
                       transaction_id, 1, ?
                FROM mutation_requests WHERE request_id = ?
                ON CONFLICT(physical_project_id) DO UPDATE SET
                    active_request_id = excluded.active_request_id,
                    lane_state = excluded.lane_state,
                    owner_box = excluded.owner_box,
                    transaction_id = excluded.transaction_id,
                    generation = project_mutation_lanes.generation + 1,
                    updated_at = excluded.updated_at
                """,
                (now, request_id),
            )
            connection.commit()
        return self.get_request(request_id)

    def transition(self, request_id: str, new_state: str, *, reason: str = "") -> dict[str, Any]:
        new_state = str(new_state).strip().upper()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT state, physical_project_id FROM mutation_requests WHERE request_id = ?",
                (request_id,),
            ).fetchone()
            if row is None:
                connection.rollback()
                raise KeyError("MUTATION_REQUEST_NOT_FOUND")
            old_state = str(row[0])
            if new_state not in _ALLOWED_TRANSITIONS.get(old_state, set()):
                connection.rollback()
                raise ValueError(f"INVALID_MUTATION_STATE_TRANSITION:{old_state}->{new_state}")
            now = _utc_now()
            connection.execute(
                "UPDATE mutation_requests SET state = ?, last_reason = ?, updated_at = ? WHERE request_id = ?",
                (new_state, reason, now, request_id),
            )
            if new_state in _ACTIVE_STATES:
                connection.execute(
                    "UPDATE project_mutation_lanes SET lane_state = ?, updated_at = ? WHERE active_request_id = ?",
                    (new_state, now, request_id),
                )
            elif new_state in _TERMINAL_STATES:
                connection.execute(
                    """
                    UPDATE project_mutation_lanes
                    SET active_request_id = NULL, lane_state = 'FREE', owner_box = '',
                        transaction_id = '', updated_at = ?
                    WHERE active_request_id = ?
                    """,
                    (now, request_id),
                )
            connection.commit()
        result = self.get_request(request_id)
        if result is None:
            raise RuntimeError("MUTATION_REQUEST_DISAPPEARED")
        return result

    def get_request(self, request_id: str) -> dict[str, Any] | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT * FROM mutation_requests WHERE request_id = ?",
                (request_id,),
            ).fetchone()
            return dict(row) if row else None

    def active_owner(self, project_id: str) -> dict[str, Any] | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT * FROM project_mutation_lanes WHERE physical_project_id = ?",
                (project_id,),
            ).fetchone()
            if row is None or not row["active_request_id"]:
                return None
            return dict(row)

    def pending_requests(self, project_id: str) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT * FROM mutation_requests
                WHERE physical_project_id = ? AND state NOT IN ('COMPLETED','ROLLED_BACK','CANCELLED','ABANDONED')
                ORDER BY queue_sequence ASC
                """,
                (project_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def recovery_pending(self, project_id: str) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT * FROM mutation_requests WHERE physical_project_id = ? AND state = 'RECOVERY_PENDING' ORDER BY queue_sequence",
                (project_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def _require_request(self, request: MutationRequest) -> None:
        if not request.integrity_valid():
            raise ValueError("MUTATION_REQUEST_HASH_MISMATCH")
        root = Path(request.project_root).resolve()
        for raw in (*request.mutation_paths, *request.basis_paths):
            path = Path(raw).resolve()
            if not _is_relative_to(path, root):
                raise ValueError("MUTATION_REQUEST_PATH_OUTSIDE_PROJECT_ROOT:" + str(path))

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
                CREATE TABLE IF NOT EXISTS mutation_requests (
                    queue_sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    request_id TEXT NOT NULL UNIQUE,
                    physical_project_id TEXT NOT NULL,
                    project_root TEXT NOT NULL,
                    owner_box TEXT NOT NULL,
                    operation_family TEXT NOT NULL,
                    transaction_id TEXT NOT NULL,
                    mutation_paths_json TEXT NOT NULL,
                    basis_paths_json TEXT NOT NULL,
                    request_hash TEXT NOT NULL,
                    state TEXT NOT NULL,
                    last_reason TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS mutation_requests_project_queue_idx
                    ON mutation_requests(physical_project_id, state, queue_sequence);
                CREATE TABLE IF NOT EXISTS project_mutation_lanes (
                    physical_project_id TEXT PRIMARY KEY,
                    active_request_id TEXT,
                    lane_state TEXT NOT NULL DEFAULT 'FREE',
                    owner_box TEXT NOT NULL DEFAULT '',
                    transaction_id TEXT NOT NULL DEFAULT '',
                    generation INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                );
                """
            )



def default_project_mutation_lane_database(project_root: str | Path) -> Path:
    """Return durable sibling storage shared by source-mutating tab boxes."""
    root = Path(project_root).resolve()
    durable_root = root.parent / f"{root.name}_workbench_transactions"
    return durable_root / "project_mutation_lane.sqlite3"

def build_mutation_request(
    *,
    request_id: str,
    project_root: str | Path,
    owner_box: str,
    operation_family: str,
    transaction_id: str,
    mutation_paths: Iterable[str | Path],
    basis_paths: Iterable[str | Path],
) -> MutationRequest:
    root = Path(project_root).resolve()
    mutation = _canonical_paths(root, mutation_paths)
    basis = _canonical_paths(root, basis_paths)
    created_at = _utc_now()
    project_id = physical_project_id(root)
    digest = _request_hash(
        physical_project_id=project_id,
        project_root=str(root),
        owner_box=owner_box,
        operation_family=operation_family,
        transaction_id=transaction_id,
        mutation_paths=mutation,
        basis_paths=basis,
        created_at=created_at,
    )
    return MutationRequest(
        schema_version="1.0",
        feature_id=PROJECT_MUTATION_LANE_FEATURE_ID,
        request_id=str(request_id),
        physical_project_id=project_id,
        project_root=str(root),
        owner_box=str(owner_box),
        operation_family=str(operation_family),
        transaction_id=str(transaction_id),
        mutation_paths=mutation,
        basis_paths=basis,
        created_at=created_at,
        request_hash=digest,
    )


def physical_project_id(project_root: str | Path) -> str:
    normalized = str(Path(project_root).resolve()).casefold()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _canonical_paths(root: Path, paths: Iterable[str | Path]) -> tuple[str, ...]:
    values: set[str] = set()
    for raw in paths:
        path = Path(raw).resolve()
        if not _is_relative_to(path, root):
            raise ValueError("MUTATION_REQUEST_PATH_OUTSIDE_PROJECT_ROOT:" + str(path))
        values.add(str(path))
    return tuple(sorted(values, key=str.casefold))


def _request_hash(
    *,
    physical_project_id: str,
    project_root: str,
    owner_box: str,
    operation_family: str,
    transaction_id: str,
    mutation_paths: tuple[str, ...],
    basis_paths: tuple[str, ...],
    created_at: str,
) -> str:
    payload = json.dumps(
        {
            "physical_project_id": physical_project_id,
            "project_root": project_root,
            "owner_box": owner_box,
            "operation_family": operation_family,
            "transaction_id": transaction_id,
            "mutation_paths": list(mutation_paths),
            "basis_paths": list(basis_paths),
            "created_at": created_at,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
