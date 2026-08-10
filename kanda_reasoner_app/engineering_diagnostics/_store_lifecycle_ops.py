# project-path: kanda_reasoner_app/engineering_diagnostics/_store_lifecycle_ops.py
"""Private lifecycle transactions for EngineeringDiagnosticsStore."""

from __future__ import annotations

from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import re
from uuid import uuid4

from ._store_database import connect
from ._store_lifecycle_state import _run_row, _scope_key, get_state
from .lifecycle import validate_lifecycle_transition
from .lifecycle_models import DiagnosticLifecycleState, DiagnosticLifecycleTarget
from .models import DiagnosticConflictError, DiagnosticStateError

_REASON_CODE = re.compile(r"^[A-Z][A-Z0-9_]{1,63}$")


def _required_text(value: object, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise DiagnosticStateError(field_name.upper() + "_REQUIRED")
    return text


def _optional_text(value: object) -> str:
    return str(value or "").strip()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _member_digest(members: tuple[str, ...]) -> str:
    payload = "lifecycle-members-v1|" + "\n".join(sorted(members))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _require_current_members(connection, run_id: str, target: DiagnosticLifecycleTarget) -> None:
    placeholders = ",".join("?" for _ in target.member_issue_fingerprints)
    rows = connection.execute(
        f"""
        SELECT issue_fingerprint FROM diagnostic_findings
        WHERE run_id = ? AND issue_fingerprint IN ({placeholders})
        """,
        (str(run_id),) + target.member_issue_fingerprints,
    ).fetchall()
    observed = {str(row["issue_fingerprint"]) for row in rows}
    expected = set(target.member_issue_fingerprints)
    if observed != expected:
        raise DiagnosticStateError("LIFECYCLE_TARGET_MEMBERS_NOT_CURRENT")


def _head_row(connection, key, target: DiagnosticLifecycleTarget):
    return connection.execute(
        """
        SELECT * FROM diagnostic_lifecycle_heads
        WHERE project_id = ? AND producer_id = ? AND scope_fingerprint = ?
          AND target_kind = ? AND target_id = ?
        """,
        key + (target.target_kind, target.target_id),
    ).fetchone()


def record_decision(
    database_path,
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
    """Append one human decision and atomically advance its target head."""
    clean_reason_code = _required_text(reason_code, "reason_code").upper()
    if _REASON_CODE.fullmatch(clean_reason_code) is None:
        raise DiagnosticStateError("LIFECYCLE_REASON_CODE_INVALID")
    clean_rationale = _required_text(rationale, "rationale")
    clean_author = _required_text(author, "author")
    clean_expiration = _optional_text(expires_at_utc)
    clean_revisit = _optional_text(revisit_condition)
    clean_ticket = _optional_text(related_ticket)
    clean_wave = _optional_text(related_wave)
    if not clean_expiration and not clean_revisit:
        raise DiagnosticStateError(
            "LIFECYCLE_EXPIRATION_OR_REVISIT_CONDITION_REQUIRED"
        )
    normalized_action = str(action or "").strip().upper()
    if normalized_action == "ACCEPT_RISK" and not bool(explicit_confirmation):
        raise DiagnosticStateError(
            "ACCEPTED_RISK_EXPLICIT_CONFIRMATION_REQUIRED"
        )
    if normalized_action == "DEFER" and not clean_wave:
        raise DiagnosticStateError("DEFERRED_RELATED_WAVE_REQUIRED")
    now = _utc_now()
    members_json = json.dumps(
        list(target.member_issue_fingerprints),
        ensure_ascii=True,
        separators=(",", ":"),
    )
    digest = _member_digest(target.member_issue_fingerprints)
    with closing(connect(database_path)) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            run = _run_row(connection, run_id)
            key = _scope_key(run)
            _require_current_members(connection, run_id, target)
            head = _head_row(connection, key, target)
            previous_state = str(head["current_state"]) if head is not None else "OPEN"
            current_generation = int(head["generation"]) if head is not None else 0
            if current_generation != int(expected_generation):
                raise DiagnosticConflictError(
                    "STALE_LIFECYCLE_GENERATION:"
                    + str(current_generation)
                    + "!="
                    + str(expected_generation)
                )
            resulting_state = validate_lifecycle_transition(
                previous_state,
                normalized_action,
            )
            next_generation = current_generation + 1
            decision_id = "lifecycle-decision-" + uuid4().hex
            connection.execute(
                """
                INSERT INTO diagnostic_lifecycle_decisions (
                    decision_id, project_id, producer_id, scope_fingerprint,
                    run_id, target_kind, target_id, target_label,
                    member_issue_fingerprints_json, action, previous_state,
                    resulting_state, reason_code, rationale, author,
                    decided_at_utc, expires_at_utc, revisit_condition,
                    related_ticket, related_wave, explicit_confirmation,
                    resulting_generation
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?
                )
                """,
                (
                    decision_id,
                    key[0],
                    key[1],
                    key[2],
                    str(run_id),
                    target.target_kind,
                    target.target_id,
                    target.label,
                    members_json,
                    normalized_action,
                    previous_state,
                    resulting_state,
                    clean_reason_code,
                    clean_rationale,
                    clean_author,
                    now,
                    clean_expiration,
                    clean_revisit,
                    clean_ticket,
                    clean_wave,
                    int(bool(explicit_confirmation)),
                    next_generation,
                ),
            )
            connection.execute(
                """
                INSERT INTO diagnostic_lifecycle_heads (
                    project_id, producer_id, scope_fingerprint,
                    target_kind, target_id, target_label, current_state,
                    generation, last_decision_id, updated_at_utc,
                    last_run_id, member_digest
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(
                    project_id, producer_id, scope_fingerprint,
                    target_kind, target_id
                ) DO UPDATE SET
                    target_label = excluded.target_label,
                    current_state = excluded.current_state,
                    generation = excluded.generation,
                    last_decision_id = excluded.last_decision_id,
                    updated_at_utc = excluded.updated_at_utc,
                    last_run_id = excluded.last_run_id,
                    member_digest = excluded.member_digest
                """,
                key
                + (
                    target.target_kind,
                    target.target_id,
                    target.label,
                    resulting_state,
                    next_generation,
                    decision_id,
                    now,
                    str(run_id),
                    digest,
                ),
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
    return get_state(database_path, run_id)
