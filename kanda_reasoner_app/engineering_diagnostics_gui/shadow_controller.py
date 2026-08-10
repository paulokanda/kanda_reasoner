# project-path: kanda_reasoner_app/engineering_diagnostics_gui/shadow_controller.py
"""Shadow collector bridge for the Engineering Diagnostics GUI controller."""

from __future__ import annotations

from pathlib import Path
from threading import Event
from typing import Callable
from uuid import uuid4

from kanda_reasoner_app.engineering_diagnostics import (
    ShadowCollectionCancelled,
    build_shadow_diagnostic_run,
    collect_shadow_findings,
)
from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

from .models import DiagnosticScanCandidate, EngineeringDiagnosticsGuiCancelled
from .source_identity import project_source_fingerprint

__all__ = ["build_shadow_scan_candidate"]

BoundaryResolver = Callable[[Path], ProjectToolBoundaryIdentity]
CancellationCheck = Callable[[Event], None]
SourceIdentityCheck = Callable[[str, str], None]


def build_shadow_scan_candidate(
    project_root: str | Path,
    operation_generation: int,
    cancellation: Event,
    *,
    boundary_resolver: BoundaryResolver,
    require_not_cancelled: CancellationCheck,
    require_unchanged_source: SourceIdentityCheck,
) -> DiagnosticScanCandidate:
    """Collect one read-only Shadow candidate through explicit dependencies."""
    root = Path(project_root).expanduser().resolve(strict=True)
    boundary = boundary_resolver(root)
    require_not_cancelled(cancellation)
    source_before = project_source_fingerprint(root)
    try:
        collection = collect_shadow_findings(root, cancellation=cancellation)
    except ShadowCollectionCancelled as exc:
        raise EngineeringDiagnosticsGuiCancelled(str(exc)) from exc
    require_not_cancelled(cancellation)
    source_after = project_source_fingerprint(root)
    require_unchanged_source(source_before, source_after)
    run = build_shadow_diagnostic_run(
        collection,
        boundary=boundary,
        attempt_id="gui-shadow-" + uuid4().hex,
        source_fingerprint=source_after,
        operation_generation=int(operation_generation),
    )
    return DiagnosticScanCandidate(
        project_root=root,
        boundary=boundary,
        run_input=run,
        source_fingerprint=source_after,
        scope_fingerprint=run.scope_fingerprint,
        configuration_fingerprint=run.configuration_fingerprint,
        operation_generation=int(operation_generation),
        report_payload={
            "report_type": "shadow_conflict_audit",
            "audit_source": collection.audit_source,
            "issue_count": len(collection.issues),
            "assessment": collection.assessment,
            "coverage_valid": collection.coverage_valid,
        },
    )
