# project-path: kanda_reasoner_app/engineering_diagnostics/fingerprinting.py
"""Deterministic identity functions for Engineering Diagnostics."""

from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
import re
from typing import Any, Mapping, Sequence

from .models import (
    DIAGNOSTIC_SCHEMA_VERSION,
    DiagnosticFindingInput,
    DiagnosticRunInput,
    DiagnosticValidationError,
)

__all__ = [
    "canonical_json",
    "evidence_digest",
    "issue_fingerprint",
    "normalize_relative_path",
    "run_content_digest",
    "scan_identity",
]

_DRIVE_PREFIX = re.compile(r"^[A-Za-z]:")


def _json_value(value: Any, *, depth: int = 0) -> Any:
    if depth > 20:
        raise DiagnosticValidationError("JSON boundary depth exceeds 20 levels.")
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, Mapping):
        if len(value) > 1000:
            raise DiagnosticValidationError("JSON mapping exceeds 1000 items.")
        result: dict[str, Any] = {}
        for key, item in value.items():
            text = str(key)
            if text in result:
                raise DiagnosticValidationError("Duplicate JSON key after normalization.")
            result[text] = _json_value(item, depth=depth + 1)
        return result
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray, str)):
        if len(value) > 10000:
            raise DiagnosticValidationError("JSON sequence exceeds 10000 items.")
        return [_json_value(item, depth=depth + 1) for item in value]
    raise DiagnosticValidationError(
        "Unsupported JSON boundary value type: " + type(value).__name__
    )


def canonical_json(value: Any) -> str:
    """Return strict deterministic JSON for persisted boundary data."""
    normalized = _json_value(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def normalize_relative_path(value: object) -> str:
    """Return a canonical project-relative POSIX path or fail closed."""
    text = str(value or "").strip().replace("\\", "/")
    if not text:
        raise DiagnosticValidationError("relative_path is required.")
    if text.startswith("/") or text.startswith("//") or _DRIVE_PREFIX.match(text):
        raise DiagnosticValidationError("Absolute diagnostic paths are forbidden.")
    raw_parts = PurePosixPath(text).parts
    parts: list[str] = []
    for part in raw_parts:
        if part in ("", "."):
            continue
        if part == "..":
            raise DiagnosticValidationError("Parent traversal is forbidden.")
        if ":" in part:
            raise DiagnosticValidationError("Colon path components are forbidden.")
        parts.append(part)
    if not parts:
        raise DiagnosticValidationError("relative_path resolves to an empty path.")
    return "/".join(parts)


def issue_fingerprint(producer_id: str, finding: DiagnosticFindingInput) -> str:
    """Return stable semantic identity for one finding."""
    payload = {
        "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "producer_id": str(producer_id).strip(),
        "code": finding.code,
        "relative_path": normalize_relative_path(finding.relative_path),
        "semantic_key": finding.semantic_key or finding.code,
        "symbol_id": finding.symbol_id,
        "location_key": finding.location_key,
        "category": finding.category,
    }
    return _digest(payload)


def evidence_digest(finding: DiagnosticFindingInput) -> str:
    """Return a digest for evidence that does not define issue identity."""
    payload = {
        "message": finding.message,
        "severity": finding.severity,
        "confidence": finding.confidence,
        "line": finding.line,
        "evidence": finding.evidence,
        "suggested_action": finding.suggested_action,
    }
    return _digest(payload)


def scan_identity(run: DiagnosticRunInput) -> str:
    """Return deterministic scan identity independent of attempt time."""
    payload = {
        "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "project_id": run.project_id,
        "project_root_fingerprint": run.project_root_fingerprint,
        "producer_id": run.producer_id,
        "producer_version": run.producer_version,
        "source_fingerprint": run.source_fingerprint,
        "scope_fingerprint": run.scope_fingerprint,
        "configuration_fingerprint": run.configuration_fingerprint,
    }
    return _digest(payload)


def run_content_digest(
    run: DiagnosticRunInput,
    finding_rows: Sequence[tuple[str, str]],
) -> str:
    """Return immutable content identity for conflict and idempotency checks."""
    ordered = sorted(finding_rows)
    if len(ordered) <= 10000:
        payload = {
            "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
            "attempt_id": run.attempt_id,
            "scan_identity": scan_identity(run),
            "completion_status": run.completion_status,
            "operation_generation": run.operation_generation,
            "findings": ordered,
            "provenance": run.provenance,
        }
        return _digest(payload)
    digest = hashlib.sha256()
    header = {
        "digest_contract": "engineering_diagnostics_run_content_stream_v1",
        "schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "attempt_id": run.attempt_id,
        "scan_identity": scan_identity(run),
        "completion_status": run.completion_status,
        "operation_generation": run.operation_generation,
        "finding_count": len(ordered),
        "provenance": run.provenance,
    }
    digest.update(canonical_json(header).encode("utf-8"))
    digest.update(b"\0")
    for issue_identity, evidence_identity in ordered:
        digest.update(str(issue_identity).encode("ascii", errors="strict"))
        digest.update(b":")
        digest.update(str(evidence_identity).encode("ascii", errors="strict"))
        digest.update(b"\n")
    return digest.hexdigest()
