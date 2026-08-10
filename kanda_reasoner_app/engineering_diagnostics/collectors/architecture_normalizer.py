# project-path: kanda_reasoner_app/engineering_diagnostics/collectors/architecture_normalizer.py
"""Normalize public Architecture Review evidence into diagnostic runs."""

from __future__ import annotations

import hashlib
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

from ..models import DiagnosticFindingInput, DiagnosticRunInput, DiagnosticValidationError
from ..rules.architecture_rule_registry import architecture_rule_profile
from .architecture_collector import (
    ARCHITECTURE_COLLECTOR_CONTRACT_VERSION,
    ARCHITECTURE_PRODUCER_ID,
    ArchitectureCollectionResult,
)

__all__ = [
    "architecture_configuration_fingerprint",
    "architecture_scope_fingerprint",
    "build_architecture_diagnostic_run",
]


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def architecture_scope_fingerprint() -> str:
    """Return the fixed selected-Project architecture validation scope."""
    return _digest(
        "engineering-diagnostics-architecture-scope-v1|selected_project_root"
    )


def architecture_configuration_fingerprint(
    collection: ArchitectureCollectionResult,
) -> str:
    """Return validation-source and collector-contract configuration identity."""
    return _digest(
        "engineering-diagnostics-architecture-config-v1|"
        + collection.validation_source
        + "|"
        + collection.validation_source_sha256
        + "|collector="
        + ARCHITECTURE_COLLECTOR_CONTRACT_VERSION
    )


def _boundary_matches(
    collection: ArchitectureCollectionResult,
    boundary: ProjectToolBoundaryIdentity,
) -> None:
    observed = Path(collection.project_root).expanduser().resolve(strict=True)
    expected = Path(boundary.active_project_root).expanduser().resolve(strict=True)
    if observed != expected:
        raise DiagnosticValidationError("ARCHITECTURE_COLLECTION_PROJECT_MISMATCH")


def build_architecture_diagnostic_run(
    collection: ArchitectureCollectionResult,
    *,
    boundary: ProjectToolBoundaryIdentity,
    attempt_id: str,
    source_fingerprint: str,
    operation_generation: int,
) -> DiagnosticRunInput:
    """Build one immutable run from completed public Architecture Review evidence."""
    _boundary_matches(collection, boundary)
    findings: list[DiagnosticFindingInput] = []
    for item in collection.issues:
        profile = architecture_rule_profile(item.code, item.level)
        semantic = "|".join(
            (
                item.code,
                item.owner,
                item.boundary,
                item.symbol,
            )
        )
        findings.append(
            DiagnosticFindingInput(
                code=item.code,
                relative_path=item.relative_path,
                message=item.message,
                severity=profile.severity,
                confidence="high",
                semantic_key=semantic,
                symbol_id=item.symbol,
                location_key=item.owner + "|" + item.boundary,
                category="architecture_" + profile.category,
                evidence={
                    "validation_source": item.validation_source,
                    "validation_source_sha256": collection.validation_source_sha256,
                    "owner": item.owner,
                    "boundary": item.boundary,
                    "symbol": item.symbol,
                    "original_level": item.level,
                    "governance_impact": profile.governance_impact,
                    "priority_default": profile.priority,
                    "assessment": collection.assessment,
                    "coverage_valid": collection.coverage_valid,
                    "collector_contract": collection.collector_version,
                },
                suggested_action=profile.suggested_action,
            )
        )
    return DiagnosticRunInput(
        attempt_id=attempt_id,
        project_id=boundary.active_project_id,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        producer_id=ARCHITECTURE_PRODUCER_ID,
        producer_version=collection.collector_version,
        source_fingerprint=source_fingerprint,
        scope_fingerprint=architecture_scope_fingerprint(),
        configuration_fingerprint=architecture_configuration_fingerprint(collection),
        operation_generation=int(operation_generation),
        findings=tuple(findings),
        started_at_utc=collection.started_at_utc,
        completed_at_utc=collection.completed_at_utc,
        provenance={
            "collector": "architecture_review_public_facade",
            "validation_source": collection.validation_source,
            "validation_source_sha256": collection.validation_source_sha256,
            "raw_issue_count": int(collection.metadata.get("raw_issue_count", 0)),
            "normalized_issue_count": len(collection.issues),
            "canonical_issue_count": collection.canonical_issue_count,
            "assessment": collection.assessment,
            "coverage_valid": collection.coverage_valid,
        },
    )
