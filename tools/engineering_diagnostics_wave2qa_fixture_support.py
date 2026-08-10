# project-path: tools/engineering_diagnostics_wave2qa_fixture_support.py
"""Neutral disposable fixtures for Engineering Diagnostics Wave 2Q-A."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import secrets
import tempfile
from typing import Iterator
from unittest.mock import patch

from kanda_reasoner_app.engineering_diagnostics import (
    RUFF_PRODUCER_ID,
    DiagnosticFindingInput,
    DiagnosticFindingRecord,
    DiagnosticRunInput,
    DiagnosticRunRecord,
    EngineeringDiagnosticsStore,
)
from kanda_reasoner_app.portable_smoke_isolation import (
    PORTABLE_SMOKE_ENABLED_ENV,
    PORTABLE_SMOKE_ROOT_ENV,
    PORTABLE_SMOKE_TOKEN_ENV,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectSelectionMode,
    ProjectToolBoundaryIdentity,
    canonical_project_support_root,
    canonical_transient_garbage_root,
)

__all__ = [
    "wave2qa_boundary_fixture",
    "wave2qa_disposable_boundary_fixture",
    "wave2qa_finding_fixture",
    "wave2qa_persisted_run_fixture",
    "wave2qa_run_record_fixture",
]

_SMOKE_MARKER_NAME = "KANDA_PORTABLE_SMOKE_ISOLATION.json"
_SMOKE_SCHEMA_VERSION = "1.0"


def _write_smoke_marker(root: Path, project_root: Path, token: str) -> None:
    """Write the exact token-bound marker consumed by the public resolver."""
    marker = {
        "schema_version": _SMOKE_SCHEMA_VERSION,
        "root": str(root.resolve(strict=False)),
        "runtime_root": str(project_root.resolve(strict=False)),
        "project_root": str(project_root.resolve(strict=False)),
        "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
    }
    marker_path = root / _SMOKE_MARKER_NAME
    marker_path.write_text(
        json.dumps(marker, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def wave2qa_boundary_fixture(root: Path) -> ProjectToolBoundaryIdentity:
    """Create an explicit self-hosting Tool/Project boundary fixture."""
    project_root = root.expanduser().resolve(strict=False)
    support = canonical_project_support_root(project_root)
    daily_work = canonical_transient_garbage_root(project_root)
    support.mkdir(parents=True, exist_ok=True)
    daily_work.mkdir(parents=True, exist_ok=True)
    return ProjectToolBoundaryIdentity(
        tool_project_slug="kanda_reasoner",
        tool_source_root=project_root,
        active_project_slug=project_root.name,
        active_project_root=project_root,
        active_project_support_root=support,
        active_project_daily_work_root=daily_work,
        active_project_id="project-id-2qa",
        active_project_root_fingerprint="a" * 64,
        same_canonical_resolved_root=True,
        self_hosting_mode=True,
        selection_mode=ProjectSelectionMode.EXPLICIT_SELF_HOSTING,
    )


@contextmanager
def wave2qa_disposable_boundary_fixture(
    ) -> Iterator[ProjectToolBoundaryIdentity]:
    """Yield one token-bound canonical boundary without drive-root leakage."""
    with tempfile.TemporaryDirectory() as temporary:
        isolation_root = Path(temporary).resolve(strict=False)
        project_root = isolation_root / "project"
        project_root.mkdir(parents=True, exist_ok=True)
        token = secrets.token_urlsafe(32)
        _write_smoke_marker(isolation_root, project_root, token)
        environment = {
            PORTABLE_SMOKE_ENABLED_ENV: "1",
            PORTABLE_SMOKE_ROOT_ENV: str(isolation_root),
            PORTABLE_SMOKE_TOKEN_ENV: token,
        }
        with patch.dict(os.environ, environment, clear=False):
            boundary = wave2qa_boundary_fixture(project_root)
            expected_support = canonical_project_support_root(project_root)
            expected_daily = canonical_transient_garbage_root(project_root)
            if boundary.active_project_support_root != expected_support:
                raise RuntimeError("WAVE2QA_FIXTURE_SUPPORT_ROOT_MISMATCH")
            if boundary.active_project_daily_work_root != expected_daily:
                raise RuntimeError("WAVE2QA_FIXTURE_DAILY_ROOT_MISMATCH")
            yield boundary


def wave2qa_run_record_fixture(
    producer_id: str,
    run_id: str = "run-2qa",
) -> DiagnosticRunRecord:
    """Create a stable completed diagnostic-run fixture."""
    return DiagnosticRunRecord(
        run_id=run_id,
        attempt_id="attempt-2qa",
        project_id="project-id-2qa",
        project_root_fingerprint="a" * 64,
        producer_id=producer_id,
        producer_version="1.0",
        scan_identity="scan-original",
        source_fingerprint="source-original",
        scope_fingerprint="scope-original",
        configuration_fingerprint="config-original",
        operation_generation=1,
        completion_status="COMPLETED",
        finding_count=0,
        content_digest="content-original",
        started_at_utc="2026-08-06T00:00:00Z",
        completed_at_utc="2026-08-06T00:00:01Z",
        provenance={},
    )


def wave2qa_finding_fixture(
    issue: str,
    code: str,
    path: str,
    *,
    symbol: str = "",
    evidence: dict[str, object] | None = None,
    run_id: str = "run-2qa",
) -> DiagnosticFindingRecord:
    """Create a stable diagnostic-finding fixture."""
    return DiagnosticFindingRecord(
        run_id=run_id,
        issue_fingerprint=issue,
        evidence_digest="evidence-" + issue,
        code=code,
        relative_path=path,
        message="message " + issue,
        severity="warning",
        confidence="high",
        semantic_key=code,
        symbol_id=symbol,
        location_key="location-" + issue,
        category="category",
        line=10,
        evidence=evidence or {},
        suggested_action="Review.",
    )


def wave2qa_persisted_run_fixture(
    store: EngineeringDiagnosticsStore,
    boundary: ProjectToolBoundaryIdentity,
) -> DiagnosticRunRecord:
    """Persist one read-only Ruff run through the canonical store owner."""
    findings = tuple(
        DiagnosticFindingInput(
            code="F401",
            relative_path="pkg/module.py",
            message="unused import " + str(index),
            severity="warning",
            confidence="high",
            semantic_key="F401|unused import " + str(index),
            symbol_id="Module.target",
            location_key="location-" + str(index),
            category="ruff_imports",
            line=index + 1,
            evidence={"tool": "ruff"},
        )
        for index in range(3)
    )
    run = DiagnosticRunInput(
        attempt_id="attempt-persisted",
        project_id=boundary.active_project_id,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        producer_id=RUFF_PRODUCER_ID,
        producer_version="1.0",
        source_fingerprint="source",
        scope_fingerprint="scope",
        configuration_fingerprint="config",
        operation_generation=1,
        findings=findings,
    )
    return store.record_completed_run(
        boundary,
        run,
        current_source_fingerprint="source",
        current_scope_fingerprint="scope",
        current_configuration_fingerprint="config",
        current_generation=1,
    )
