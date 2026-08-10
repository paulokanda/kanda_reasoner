# project-path: kanda_reasoner_app/engineering_diagnostics/_store_run_ops.py
"""Private immutable-run normalization and insertion mechanics."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from .fingerprinting import (
    canonical_json,
    evidence_digest,
    issue_fingerprint as calculate_issue_fingerprint,
    normalize_relative_path,
    scan_identity,
)
from .models import (
    DiagnosticConflictError,
    DiagnosticFindingInput,
    DiagnosticRunInput,
)


def _path_key(path: str | Path) -> str:
    return os.path.normcase(str(Path(path).expanduser().resolve(strict=False)))


def _run_id(project_id: str, attempt_id: str) -> str:
    payload = "run-v1|" + project_id + "|" + attempt_id
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _finding_row(
    fingerprint: str,
    finding: DiagnosticFindingInput,
) -> dict[str, Any]:
    return {
        "issue_fingerprint": fingerprint,
        "evidence_digest": evidence_digest(finding),
        "code": finding.code,
        "relative_path": normalize_relative_path(finding.relative_path),
        "message": finding.message,
        "severity": finding.severity,
        "confidence": finding.confidence,
        "semantic_key": finding.semantic_key,
        "symbol_id": finding.symbol_id,
        "location_key": finding.location_key,
        "category": finding.category,
        "line": finding.line,
        "evidence_json": canonical_json(finding.evidence),
        "suggested_action": finding.suggested_action,
    }


def _normalize_findings(
    run: DiagnosticRunInput,
) -> tuple[dict[str, Any], ...]:
    rows: dict[str, dict[str, Any]] = {}
    for finding in run.findings:
        fingerprint = calculate_issue_fingerprint(run.producer_id, finding)
        row = _finding_row(fingerprint, finding)
        existing = rows.get(fingerprint)
        if existing is not None and existing != row:
            raise DiagnosticConflictError(
                "DUPLICATE_ISSUE_FINGERPRINT_WITH_DIFFERENT_EVIDENCE"
            )
        rows[fingerprint] = row
    return tuple(rows[key] for key in sorted(rows))


def _insert_run(
    connection,
    run_id: str,
    run: DiagnosticRunInput,
    content_digest: str,
    finding_rows: tuple[dict[str, Any], ...],
) -> None:
    connection.execute(
        """
        INSERT INTO diagnostic_runs (
            run_id, attempt_id, project_id, project_root_fingerprint,
            producer_id, producer_version, scan_identity,
            source_fingerprint, scope_fingerprint,
            configuration_fingerprint, operation_generation,
            completion_status, finding_count, content_digest,
            started_at_utc, completed_at_utc, provenance_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            run.attempt_id,
            run.project_id,
            run.project_root_fingerprint,
            run.producer_id,
            run.producer_version,
            scan_identity(run),
            run.source_fingerprint,
            run.scope_fingerprint,
            run.configuration_fingerprint,
            run.operation_generation,
            run.completion_status,
            len(finding_rows),
            content_digest,
            run.started_at_utc,
            run.completed_at_utc,
            canonical_json(run.provenance),
        ),
    )
    for row in finding_rows:
        connection.execute(
            """
            INSERT INTO diagnostic_findings (
                run_id, issue_fingerprint, evidence_digest, code,
                relative_path, message, severity, confidence,
                semantic_key, symbol_id, location_key, category,
                line, evidence_json, suggested_action
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                row["issue_fingerprint"],
                row["evidence_digest"],
                row["code"],
                row["relative_path"],
                row["message"],
                row["severity"],
                row["confidence"],
                row["semantic_key"],
                row["symbol_id"],
                row["location_key"],
                row["category"],
                row["line"],
                row["evidence_json"],
                row["suggested_action"],
            ),
        )
