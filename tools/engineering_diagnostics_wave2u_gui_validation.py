# project-path: tools/engineering_diagnostics_wave2u_gui_validation.py
"""Real Qt validation for Wave 2U governed Patch Preview controls."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.engineering_diagnostics import (
    BOM_PRODUCER_ID,
    DiagnosticFindingEnrichment,
    DiagnosticFindingRecord,
    DiagnosticFrozenPathEnrichment,
    DiagnosticOwnerEnrichment,
    DiagnosticRemediationIntent,
    DiagnosticScopeEnrichment,
    DiagnosticValidationPlan,
)
from kanda_reasoner_app.engineering_diagnostics_gui.models import DiagnosticFindingView

__all__ = ["validate_wave2u_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _finding_view() -> DiagnosticFindingView:
    finding = DiagnosticFindingRecord(
        run_id="wave2u-run",
        issue_fingerprint="1" * 64,
        evidence_digest="2" * 64,
        code="BOM",
        relative_path="sample.py",
        message="UTF-8 BOM",
        severity="warning",
        confidence="high",
        semantic_key="bom|sample.py",
        symbol_id="",
        location_key="file",
        category="source_hygiene",
        line=1,
        evidence={},
        suggested_action="Remove only the exact UTF-8 BOM.",
    )
    intent = DiagnosticRemediationIntent(
        intent_id="remediation-" + "3" * 64,
        target_issue_fingerprint=finding.issue_fingerprint,
        action_class="SAFE_MECHANICAL_FIX_AVAILABLE",
        likely_correction="Remove only the exact UTF-8 BOM.",
        reason="Exact active unfrozen file.",
        canonical_owner="sample.py",
        expected_affected_files=("sample.py",),
        frozen_path_impact="UNFROZEN",
        governing_freeze_ids=(),
        required_governed_wave="",
        fix_applicability="EXACT_FILE",
        mechanical_safety="SAFE_MECHANICAL",
        semantic_review_requirement="NOT_REQUIRED",
        validation_plan=DiagnosticValidationPlan(
            focused_tests=("focused",),
            validation_commands=("validate",),
            rollback_expectation="restore exact bytes",
            evidence_required=("evidence",),
        ),
        uncertainty="low",
        primary_trust_source="KANDA_RULE_TEMPLATE",
        rule_template_id="kanda.remediation.bom.exact_file.v1",
        deterministic_evidence=("evidence",),
        project_governance_rules=("governance",),
    )
    enrichment = DiagnosticFindingEnrichment(
        scope=DiagnosticScopeEnrichment(
            classification="ACTIVE",
            confidence="high",
            method="wave2u_real_qt_fixture",
            evidence=("Wave 2U real-Qt validation fixture.",),
        ),
        frozen_path=DiagnosticFrozenPathEnrichment(
            status="UNFROZEN",
            governing_freeze_ids=(),
            matched_protected_paths=(),
            evidence=("Fixture path is explicitly unfrozen.",),
        ),
        owner=DiagnosticOwnerEnrichment(
            status="READY",
            confidence="high",
            canonical_owner="sample.py",
            active_candidates=("sample.py",),
            historical_candidates=(),
            selection_method="wave2u_real_qt_fixture",
            evidence=("Fixture owner is exact and active.",),
        ),
    )
    return DiagnosticFindingView(
        record=finding,
        lifecycle_state="current",
        enrichment=enrichment,
        decision_state="PATCH_PREPARED",
        remediation_intent=intent,
    )


def validate_wave2u_gui(root: Path) -> tuple[float, float, float]:
    """Prove the real Patch Preview button projection and inherited GUI gates."""
    from PySide6.QtCore import QCoreApplication
    from PySide6.QtWidgets import QApplication, QPushButton

    from kanda_reasoner_app.engineering_diagnostics_gui import (
        create_engineering_diagnostics_panel,
    )
    from tools.engineering_diagnostics_wave2t_gui_validation import validate_wave2t_gui

    fixture = _finding_view()
    _require(
        isinstance(fixture.enrichment, DiagnosticFindingEnrichment),
        "WAVE2U_REAL_QT_FIXTURE_ENRICHMENT_TYPE_INVALID",
    )
    _require(
        fixture.enrichment.owner.active_candidates == ("sample.py",),
        "WAVE2U_REAL_QT_FIXTURE_ACTIVE_CANDIDATES_INVALID",
    )
    _require(
        fixture.enrichment.owner.historical_candidates == (),
        "WAVE2U_REAL_QT_FIXTURE_HISTORICAL_CANDIDATES_INVALID",
    )
    print("WAVE2U REAL QT PUBLIC ENRICHMENT FIXTURE: PASS")
    print("WAVE2U REAL QT OWNER CANDIDATE FIELDS: PASS")
    panel_ms, rows_ms, filter_ms = validate_wave2t_gui(root)
    app = QApplication.instance() or QApplication([])
    run = SimpleNamespace(
        run_id="wave2u-run",
        producer_id=BOM_PRODUCER_ID,
        completion_status="COMPLETED",
        source_fingerprint="source",
        provenance={},
        finding_count=1,
        completed_at_utc="2026-08-06T00:00:00Z",
    )
    comparison = SimpleNamespace(
        status="NO_BASELINE",
        new_issue_fingerprints=(),
        persistent_issue_fingerprints=(),
        resolved_issue_fingerprints=(),
    )
    view = SimpleNamespace(
        run=run,
        comparison=comparison,
        findings=(_finding_view(),),
        groups=(),
        lifecycle=None,
    )
    controller = SimpleNamespace(
        list_runs=lambda *_args, **_kwargs: (run,),
        load_run_view=lambda *_args, **_kwargs: view,
        source_excerpt=lambda *_args, **_kwargs: "sample",
    )
    panel = create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        controller=controller,
        defer_initial_refresh=True,
    )
    panel.refresh_engineering_diagnostics("wave2u-run")
    table = panel.engineering_diagnostics_table
    table.selectRow(0)
    QCoreApplication.processEvents()
    button = panel.engineering_diagnostics_patch_preview_button
    _require(isinstance(button, QPushButton), "WAVE2U_REAL_QT_BUTTON_TYPE_INVALID")
    _require(
        button.objectName() == "engineeringDiagnosticsPatchPreviewButton",
        "WAVE2U_REAL_QT_BUTTON_IDENTITY_MISMATCH",
    )
    _require(button.text() == "Create Patch Preview", "WAVE2U_REAL_QT_BUTTON_TEXT_MISMATCH")
    _require(button.isEnabled(), "WAVE2U_REAL_QT_ELIGIBLE_BUTTON_DISABLED")
    _require(
        not hasattr(panel, "engineering_diagnostics_patch_apply_button"),
        "WAVE2U_REAL_QT_APPLY_LANE_EXPOSED",
    )
    panel.deleteLater()
    app.processEvents()
    print("WAVE2U REAL QT PATCH PREVIEW BUTTON: PASS")
    print("WAVE2U REAL QT ELIGIBILITY PROJECTION: PASS")
    print("WAVE2U GUI SOURCE APPLY CONTROL: ABSENT")
    print("WAVE2U GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms
