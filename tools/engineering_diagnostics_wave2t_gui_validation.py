# project-path: tools/engineering_diagnostics_wave2t_gui_validation.py
"""Real Qt validation for Wave 2T Full Audit drill-through."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.engineering_diagnostics import RUFF_PRODUCER_ID
from kanda_reasoner_app.engineering_diagnostics_gui.source_identity import (
    project_source_fingerprint,
)

__all__ = ["validate_wave2t_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _report() -> str:
    return "\n".join(
        (
            "COMPLETE ENGINEERING REVIEW",
            "[01/01] Source Hygiene - Ruff Quality",
            "Command: ruff-quality",
            "Outcome: PASS",
            "Execution: PASS",
            "Assessment: PASS_WITH_FINDINGS",
            "Assessment reason: Ruff findings were retained.",
            "-" * 72,
        )
    )


def validate_wave2t_gui(root: Path) -> tuple[float, float, float]:
    """Prove the real sibling-tab bridge and retain inherited scale gates."""
    from PySide6.QtCore import QCoreApplication
    from PySide6.QtWidgets import QApplication, QPushButton, QTabWidget
    from reasoner_tools_gui_engineering_safety_panel import create_engineering_safety_panel

    from kanda_reasoner_app.engineering_diagnostics_gui import (
        create_engineering_diagnostics_panel,
        install_full_audit_diagnostics_drillthrough_ui,
    )
    from kanda_reasoner_app.engineering_diagnostics_gui.wave2s_validation import (
        validate_wave2s_gui,
    )

    panel_ms, rows_ms, filter_ms = validate_wave2s_gui(root)
    app = QApplication.instance() or QApplication([])
    source = project_source_fingerprint(root)
    run = SimpleNamespace(
        run_id="wave2t-compatible-run",
        producer_id=RUFF_PRODUCER_ID,
        completion_status="COMPLETED",
        source_fingerprint=source,
        provenance={"raw_finding_count": 19},
        finding_count=17,
        completed_at_utc="2026-08-06T00:00:00Z",
    )
    comparison = SimpleNamespace(
        status="COMPARED",
        new_issue_fingerprints=(),
        persistent_issue_fingerprints=(),
        resolved_issue_fingerprints=(),
    )
    view = SimpleNamespace(run=run, comparison=comparison, findings=(), groups=())
    controller = SimpleNamespace(
        list_runs=lambda *_args, **_kwargs: (run,),
        load_run_view=lambda *_args, **_kwargs: view,
    )
    root_provider = lambda: str(root)
    safety = create_engineering_safety_panel(project_root_provider=root_provider)
    diagnostics = create_engineering_diagnostics_panel(
        project_root_provider=root_provider,
        controller=controller,
        defer_initial_refresh=True,
    )
    tabs = QTabWidget()
    tabs.addTab(safety, "Engineering Safety")
    tabs.addTab(diagnostics, "Engineering Diagnostics")
    link = SimpleNamespace(
        label="Ruff Quality",
        assessment="PASS_WITH_FINDINGS",
        producer_id=RUFF_PRODUCER_ID,
    )
    group = install_full_audit_diagnostics_drillthrough_ui(
        safety,
        diagnostics,
        project_root_provider=root_provider,
        select_diagnostics_tab=lambda: tabs.setCurrentWidget(diagnostics),
        diagnostic_links_provider=lambda _report: (link,),
    )
    generation_before = int(
        getattr(
            group,
            "engineering_diagnostics_drillthrough_refresh_generation",
            0,
        )
    )
    safety.engineering_safety_full_audit_log.setPlainText(_report())
    QCoreApplication.processEvents()
    generation_after = int(
        getattr(
            group,
            "engineering_diagnostics_drillthrough_refresh_generation",
            0,
        )
    )
    _require(
        generation_after > generation_before,
        "WAVE2T_REAL_QT_DRILLTHROUGH_SIGNAL_REFRESH_MISSING",
    )
    buttons = tuple(
        getattr(group, "engineering_diagnostics_drillthrough_buttons", ())
    )
    _require(len(buttons) == 1, "WAVE2T_REAL_QT_DRILLTHROUGH_BUTTON_MISSING")
    _require(
        isinstance(buttons[0], QPushButton),
        "WAVE2T_REAL_QT_DRILLTHROUGH_BUTTON_TYPE_INVALID",
    )
    _require(
        buttons[0].objectName()
        == "full_audit_engineering_diagnostics_open_button",
        "WAVE2T_REAL_QT_DRILLTHROUGH_BUTTON_IDENTITY_MISMATCH",
    )
    _require(
        buttons[0].text() == "Open in Engineering Diagnostics",
        "WAVE2T_REAL_QT_DRILLTHROUGH_BUTTON_TEXT_MISMATCH",
    )
    _require(buttons[0].isEnabled(), "WAVE2T_REAL_QT_DRILLTHROUGH_BUTTON_DISABLED")
    _require(
        "Assessment: PASS_WITH_FINDINGS"
        in safety.engineering_safety_full_audit_log.toPlainText(),
        "WAVE2M_ASSESSMENT_TEXT_CHANGED",
    )
    buttons[0].click()
    QCoreApplication.processEvents()
    request = getattr(diagnostics, "engineering_diagnostics_last_navigation", None)
    _require(request is not None, "WAVE2T_NAVIGATION_REQUEST_NOT_APPLIED")
    _require(request.producer_id == RUFF_PRODUCER_ID, "WAVE2T_PRODUCER_FILTER_MISMATCH")
    _require(request.compatible_run_id == run.run_id, "WAVE2T_COMPATIBLE_RUN_FILTER_MISMATCH")
    _require(request.baseline_state == "current", "WAVE2T_BASELINE_FILTER_MISMATCH")
    _require(tabs.currentWidget() is diagnostics, "WAVE2T_SIBLING_TAB_NOT_SELECTED")
    tabs.deleteLater()
    app.processEvents()
    print("WAVE2T REAL QT DRILL-THROUGH SIGNAL REFRESH: PASS")
    print("WAVE2T REAL QT DRILL-THROUGH PUBLIC BUTTON PROJECTION: PASS")
    print("WAVE2T FULL AUDIT DRILL-THROUGH ROW: PASS")
    print("WAVE2T EXACT COMPATIBLE RUN NAVIGATION: PASS")
    print("WAVE2M ASSESSMENT SEMANTICS PRESERVED: PASS")
    print("WAVE2T GUI HIGH-VOLUME PERFORMANCE: PASS")
    return panel_ms, rows_ms, filter_ms
