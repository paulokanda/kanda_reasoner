# project-path: kanda_reasoner_app/engineering_diagnostics/collectors/shadow_normalizer.py
"""Normalize public Shadow evidence into Engineering Diagnostics runs."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

from ..fingerprinting import canonical_json
from ..models import DiagnosticFindingInput, DiagnosticRunInput, DiagnosticValidationError
from .shadow_collector import (
    SHADOW_COLLECTOR_CONTRACT_VERSION,
    SHADOW_PRODUCER_ID,
    ShadowCollectionResult,
    ShadowIssueEvidence,
)

__all__ = [
    "build_shadow_diagnostic_run",
    "shadow_configuration_fingerprint",
    "shadow_scope_fingerprint",
]

_FACADE_CODES = frozenset(
    {
        "BEHAVIOR_DEFINED_IN_FACADE",
        "FACADE_WITHOUT_ALL",
        "RUNTIME_LOGIC_IN_FACADE",
        "WILDCARD_IMPORT_IN_FACADE",
    }
)


def _digest(label: str, payload: object) -> str:
    text = label + "|" + canonical_json(payload)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def shadow_scope_fingerprint(collection: ShadowCollectionResult) -> str:
    """Return deterministic Shadow scope identity."""
    return _digest(
        "engineering-diagnostics-shadow-scope-v1",
        {
            "producer_id": SHADOW_PRODUCER_ID,
            "collector_contract": SHADOW_COLLECTOR_CONTRACT_VERSION,
            "scope": "active_production_python_without_tests",
            "max_files": collection.metadata.get("max_files"),
        },
    )


def shadow_configuration_fingerprint(collection: ShadowCollectionResult) -> str:
    """Return deterministic public-audit configuration identity."""
    return _digest(
        "engineering-diagnostics-shadow-configuration-v1",
        {
            "audit_source": collection.audit_source,
            "audit_source_sha256": collection.audit_source_sha256,
            "collector_contract": collection.collector_version,
        },
    )


def _tuple_text(value: object) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple, set, frozenset)):
        return ()
    return tuple(sorted({str(item).strip() for item in value if str(item).strip()}))


def _semantic_parts(issue: ShadowIssueEvidence) -> tuple[str, str, str, str]:
    symbol = str(issue.evidence.get("symbol") or "").strip()
    exported = str(issue.evidence.get("exported_name") or "").strip()
    owners = _tuple_text(issue.evidence.get("owners"))
    owner_key = _digest("shadow-owner-set-v1", owners)[:24] if owners else ""
    statement_fingerprint = str(
        issue.evidence.get("runtime_statement_fingerprint") or ""
    ).strip()
    statement_ordinal = str(
        issue.evidence.get("runtime_statement_ordinal") or ""
    ).strip()
    statement_key = ""
    if statement_fingerprint:
        statement_key = statement_fingerprint + ":" + (statement_ordinal or "1")
    return symbol, exported, owner_key, statement_key


def _category(code: str) -> str:
    if code in _FACADE_CODES:
        return "shadow_facade"
    if code in {"DUPLICATE_PUBLIC_SYMBOL", "UNBOUND_ALL_EXPORT", "DYNAMIC_ALL_EXPORT"}:
        return "shadow_public_surface"
    return "shadow_audit"


def _finding_input(issue: ShadowIssueEvidence) -> DiagnosticFindingInput:
    symbol, exported, owner_key, statement_key = _semantic_parts(issue)
    semantic_subject = symbol or exported or owner_key or statement_key or issue.code
    evidence: dict[str, Any] = dict(issue.evidence)
    evidence.update(
        {
            "tool": "source_hygiene.shadow_audit",
            "shadow_code": issue.code,
            "relational_evidence_available": bool(symbol or exported or evidence.get("owners")),
            "source_mutated": False,
        }
    )
    location_key = "|".join(
        part for part in (symbol, exported, owner_key, statement_key) if part
    ) or issue.relative_path
    return DiagnosticFindingInput(
        code=issue.code,
        relative_path=issue.relative_path,
        message=issue.message,
        severity=issue.severity,
        confidence=issue.confidence,
        semantic_key=issue.code + "|" + semantic_subject,
        symbol_id=symbol or exported,
        location_key=location_key,
        category=_category(issue.code),
        line=issue.line,
        evidence=evidence,
        suggested_action=issue.suggested_action,
    )


def build_shadow_diagnostic_run(
    collection: ShadowCollectionResult,
    *,
    boundary: ProjectToolBoundaryIdentity,
    attempt_id: str,
    source_fingerprint: str,
    operation_generation: int,
) -> DiagnosticRunInput:
    """Normalize a complete public Shadow audit into one diagnostic run."""
    root = Path(boundary.active_project_root).resolve(strict=True)
    if Path(collection.project_root).resolve(strict=False) != root:
        raise DiagnosticValidationError("Shadow collection Project root does not match.")
    if not collection.coverage_valid:
        raise DiagnosticValidationError("SHADOW_COLLECTION_COVERAGE_INVALID")
    findings = tuple(_finding_input(issue) for issue in collection.issues)
    return DiagnosticRunInput(
        attempt_id=attempt_id,
        project_id=boundary.active_project_id,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        producer_id=SHADOW_PRODUCER_ID,
        producer_version=collection.collector_version,
        source_fingerprint=str(source_fingerprint),
        scope_fingerprint=shadow_scope_fingerprint(collection),
        configuration_fingerprint=shadow_configuration_fingerprint(collection),
        operation_generation=int(operation_generation),
        findings=findings,
        started_at_utc=collection.started_at_utc,
        completed_at_utc=collection.completed_at_utc,
        provenance={
            "collector_contract": collection.collector_version,
            "audit_source": collection.audit_source,
            "audit_source_sha256": collection.audit_source_sha256,
            "assessment": collection.assessment,
            "coverage_valid": collection.coverage_valid,
            "metadata": dict(collection.metadata),
            "source_mutated": False,
            "ai_grouping_used": False,
        },
    )
