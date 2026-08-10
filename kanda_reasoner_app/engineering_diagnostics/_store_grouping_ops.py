# project-path: kanda_reasoner_app/engineering_diagnostics/_store_grouping_ops.py
"""Private manual grouping transactions for EngineeringDiagnosticsStore."""

from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import sqlite3
from uuid import uuid4

from ._store_database import connect
from .grouping_models import DiagnosticManualGroupingState
from ._store_grouping_state import (
    _generation,
    _get_state,
    _group_row,
    _require_group_scope,
    _require_issue,
    _run_row,
    _scope_key,
)
from .models import DiagnosticConflictError, DiagnosticStateError

__all__: list[str] = []


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise DiagnosticStateError(field_name.upper() + "_REQUIRED")
    return text


def _require_generation(current: int, expected: int) -> None:
    if current != int(expected):
        raise DiagnosticConflictError(
            "GROUPING_GENERATION_COMPARE_AND_SWAP_FAILED"
        )


def _next_generation(
    connection: sqlite3.Connection,
    key: tuple[str, str, str],
    current: int,
    now: str,
) -> int:
    next_value = current + 1
    connection.execute(
        """
        INSERT INTO diagnostic_group_heads (
            project_id, producer_id, scope_fingerprint, generation, updated_at_utc
        ) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(project_id, producer_id, scope_fingerprint)
        DO UPDATE SET
            generation = excluded.generation,
            updated_at_utc = excluded.updated_at_utc
        """,
        key + (next_value, now),
    )
    return next_value


def _insert_decision(
    connection: sqlite3.Connection,
    *,
    group_id: str,
    key: tuple[str, str, str],
    action: str,
    issue_fingerprint: str,
    previous_group_id: str,
    reason: str,
    author: str,
    now: str,
    generation: int,
) -> None:
    connection.execute(
        """
        INSERT INTO diagnostic_group_decisions (
            decision_id, group_id, project_id, producer_id, scope_fingerprint,
            action, issue_fingerprint, previous_group_id, reason, author,
            created_at_utc, resulting_generation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            uuid4().hex,
            group_id,
            key[0],
            key[1],
            key[2],
            action,
            issue_fingerprint,
            previous_group_id,
            reason,
            author,
            now,
            generation,
        ),
    )


def _invalidate_review(
    connection: sqlite3.Connection,
    group_ids: set[str],
) -> None:
    for group_id in sorted(group_ids):
        if not group_id:
            continue
        connection.execute(
            """
            UPDATE diagnostic_manual_groups
            SET review_state = 'UNREVIEWED', reviewed_at_utc = ''
            WHERE group_id = ? AND review_state != 'UNREVIEWED'
            """,
            (group_id,),
        )


def get_state(
    database_path,
    run_id: str,
    *,
    decision_limit: int = 200,
) -> DiagnosticManualGroupingState:
    return _get_state(
        database_path,
        run_id,
        decision_limit=decision_limit,
    )


def create_group(
    database_path,
    run_id: str,
    *,
    label: str,
    author: str,
    reason: str,
    expected_generation: int,
) -> DiagnosticManualGroupingState:
    clean_label = _required_text(label, "group_label")
    clean_author = _required_text(author, "author")
    clean_reason = _required_text(reason, "reason")
    now = _utc_now()
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            run = _run_row(connection, run_id)
            key = _scope_key(run)
            current = _generation(connection, key)
            _require_generation(current, expected_generation)
            group_id = "manual-group-" + uuid4().hex
            connection.execute(
                """
                INSERT INTO diagnostic_manual_groups (
                    group_id, project_id, producer_id, scope_fingerprint,
                    label, review_state, created_at_utc, reviewed_at_utc, author
                ) VALUES (?, ?, ?, ?, ?, 'UNREVIEWED', ?, '', ?)
                """,
                (group_id,) + key + (clean_label, now, clean_author),
            )
            next_value = _next_generation(connection, key, current, now)
            _insert_decision(
                connection,
                group_id=group_id,
                key=key,
                action="CREATE_GROUP",
                issue_fingerprint="",
                previous_group_id="",
                reason=clean_reason,
                author=clean_author,
                now=now,
                generation=next_value,
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
    return get_state(database_path, run_id)


def assign_issue(
    database_path,
    run_id: str,
    issue_fingerprint: str,
    group_id: str,
    *,
    author: str,
    reason: str,
    expected_generation: int,
) -> DiagnosticManualGroupingState:
    clean_author = _required_text(author, "author")
    clean_reason = _required_text(reason, "reason")
    now = _utc_now()
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            run = _run_row(connection, run_id)
            key = _scope_key(run)
            current = _generation(connection, key)
            _require_generation(current, expected_generation)
            fingerprint = _require_issue(connection, run_id, issue_fingerprint)
            group = _group_row(connection, group_id)
            _require_group_scope(group, key)
            existing = connection.execute(
                """
                SELECT group_id FROM diagnostic_manual_group_members
                WHERE project_id = ? AND producer_id = ?
                  AND scope_fingerprint = ? AND issue_fingerprint = ?
                """,
                key + (fingerprint,),
            ).fetchone()
            previous = str(existing["group_id"]) if existing is not None else ""
            if previous == str(group_id):
                connection.rollback()
                return get_state(database_path, run_id)
            connection.execute(
                """
                INSERT INTO diagnostic_manual_group_members (
                    project_id, producer_id, scope_fingerprint,
                    issue_fingerprint, group_id, assigned_at_utc
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(
                    project_id, producer_id, scope_fingerprint, issue_fingerprint
                ) DO UPDATE SET
                    group_id = excluded.group_id,
                    assigned_at_utc = excluded.assigned_at_utc
                """,
                key + (fingerprint, str(group_id), now),
            )
            _invalidate_review(connection, {previous, str(group_id)})
            next_value = _next_generation(connection, key, current, now)
            _insert_decision(
                connection,
                group_id=str(group_id),
                key=key,
                action="ASSIGN_ISSUE",
                issue_fingerprint=fingerprint,
                previous_group_id=previous,
                reason=clean_reason,
                author=clean_author,
                now=now,
                generation=next_value,
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
    return get_state(database_path, run_id)


def ungroup_issue(
    database_path,
    run_id: str,
    issue_fingerprint: str,
    *,
    author: str,
    reason: str,
    expected_generation: int,
) -> DiagnosticManualGroupingState:
    clean_author = _required_text(author, "author")
    clean_reason = _required_text(reason, "reason")
    now = _utc_now()
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            run = _run_row(connection, run_id)
            key = _scope_key(run)
            current = _generation(connection, key)
            _require_generation(current, expected_generation)
            fingerprint = _require_issue(connection, run_id, issue_fingerprint)
            existing = connection.execute(
                """
                SELECT group_id FROM diagnostic_manual_group_members
                WHERE project_id = ? AND producer_id = ?
                  AND scope_fingerprint = ? AND issue_fingerprint = ?
                """,
                key + (fingerprint,),
            ).fetchone()
            if existing is None:
                connection.rollback()
                return get_state(database_path, run_id)
            group_id = str(existing["group_id"])
            connection.execute(
                """
                DELETE FROM diagnostic_manual_group_members
                WHERE project_id = ? AND producer_id = ?
                  AND scope_fingerprint = ? AND issue_fingerprint = ?
                """,
                key + (fingerprint,),
            )
            _invalidate_review(connection, {group_id})
            next_value = _next_generation(connection, key, current, now)
            _insert_decision(
                connection,
                group_id=group_id,
                key=key,
                action="UNGROUP_ISSUE",
                issue_fingerprint=fingerprint,
                previous_group_id=group_id,
                reason=clean_reason,
                author=clean_author,
                now=now,
                generation=next_value,
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
    return get_state(database_path, run_id)


def mark_reviewed(
    database_path,
    run_id: str,
    group_id: str,
    *,
    author: str,
    reason: str,
    expected_generation: int,
) -> DiagnosticManualGroupingState:
    clean_author = _required_text(author, "author")
    clean_reason = _required_text(reason, "reason")
    now = _utc_now()
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            run = _run_row(connection, run_id)
            key = _scope_key(run)
            current = _generation(connection, key)
            _require_generation(current, expected_generation)
            group = _group_row(connection, group_id)
            _require_group_scope(group, key)
            if str(group["review_state"]) == "REVIEWED":
                connection.rollback()
                return get_state(database_path, run_id)
            connection.execute(
                """
                UPDATE diagnostic_manual_groups
                SET review_state = 'REVIEWED', reviewed_at_utc = ?
                WHERE group_id = ?
                """,
                (now, str(group_id)),
            )
            next_value = _next_generation(connection, key, current, now)
            _insert_decision(
                connection,
                group_id=str(group_id),
                key=key,
                action="MARK_REVIEWED",
                issue_fingerprint="",
                previous_group_id="",
                reason=clean_reason,
                author=clean_author,
                now=now,
                generation=next_value,
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
    return get_state(database_path, run_id)
