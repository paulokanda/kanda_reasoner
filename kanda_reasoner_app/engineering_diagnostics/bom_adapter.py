# project-path: kanda_reasoner_app/engineering_diagnostics/bom_adapter.py
"""Public-data adapter for Source Hygiene BOM report payloads."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

from .models import (
    DiagnosticFindingInput,
    DiagnosticRunInput,
    DiagnosticValidationError,
)

__all__ = ["BOM_PRODUCER_ID", "build_bom_diagnostic_run"]

BOM_PRODUCER_ID = "source_hygiene.bom_scan"


def _path_key(path: str | Path) -> str:
    return os.path.normcase(str(Path(path).expanduser().resolve(strict=False)))


def _required_mapping(value: object, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DiagnosticValidationError(field_name + " must be an object.")
    return value


def _required_list(value: object, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise DiagnosticValidationError(field_name + " must be a list.")
    if len(value) > 100000:
        raise DiagnosticValidationError(field_name + " exceeds 100000 items.")
    return value


def build_bom_diagnostic_run(
    report_payload: Mapping[str, Any],
    *,
    boundary: ProjectToolBoundaryIdentity,
    attempt_id: str,
    source_fingerprint: str,
    scope_fingerprint: str,
    configuration_fingerprint: str,
    operation_generation: int,
    producer_version: str = "1.0",
) -> DiagnosticRunInput:
    """Translate one completed public BOM report payload into a run input."""
    report = _required_mapping(report_payload, "report_payload")
    if str(report.get("report_type", "")).strip() != "bom_scan":
        raise DiagnosticValidationError("BOM report_type must be bom_scan.")
    report_root = str(report.get("project_root", "")).strip()
    if not report_root:
        raise DiagnosticValidationError("BOM report project_root is required.")
    if _path_key(report_root) != _path_key(boundary.active_project_root):
        raise DiagnosticValidationError("BOM report Project root does not match.")

    findings: list[DiagnosticFindingInput] = []
    for index, raw in enumerate(_required_list(report.get("findings"), "findings")):
        item = _required_mapping(raw, "findings[" + str(index) + "]")
        evidence = item.get("evidence", {})
        if not isinstance(evidence, Mapping):
            raise DiagnosticValidationError(
                "findings[" + str(index) + "].evidence must be an object."
            )
        findings.append(
            DiagnosticFindingInput(
                code=str(item.get("code", "")),
                relative_path=str(item.get("path", "")),
                message=str(item.get("message", "")),
                severity=str(item.get("severity", "warning")),
                confidence=str(item.get("confidence", "medium")),
                semantic_key=str(item.get("code", "")),
                category="source_hygiene_bom",
                line=item.get("line"),
                evidence=dict(evidence),
                suggested_action=str(item.get("suggested_action", "")),
            )
        )

    provenance = {
        "adapter_contract": "engineering_diagnostics.bom_adapter.v1",
        "source_report_id": str(report.get("report_id", "")),
        "source_created_at": str(report.get("created_at", "")),
        "source_summary": str(report.get("summary", "")),
        "source_input_sources": list(report.get("input_sources", []) or []),
    }
    return DiagnosticRunInput(
        attempt_id=attempt_id,
        project_id=boundary.active_project_id,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        producer_id=BOM_PRODUCER_ID,
        producer_version=producer_version,
        source_fingerprint=source_fingerprint,
        scope_fingerprint=scope_fingerprint,
        configuration_fingerprint=configuration_fingerprint,
        operation_generation=operation_generation,
        findings=tuple(findings),
        completion_status="COMPLETED",
        started_at_utc=str(report.get("created_at", "")),
        completed_at_utc=str(report.get("created_at", "")),
        provenance=provenance,
    )
