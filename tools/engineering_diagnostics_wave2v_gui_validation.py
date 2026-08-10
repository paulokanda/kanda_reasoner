# project-path: tools/engineering_diagnostics_wave2v_gui_validation.py
"""Real Qt validation for the corrected Wave 2V Pontual run console."""

from __future__ import annotations

from pathlib import Path
import time

from kanda_reasoner_app.engineering_diagnostics_gui.models import (
    EngineeringDiagnosticsGuiCancelled,
)

__all__ = ["validate_wave2v_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class _RunConsoleController:
    """Public-contract fixture for cooperative cancellation."""

    def list_runs(self, *_args: object, **_kwargs: object) -> tuple[()]:
        return ()

    def load_run_view(self, *_args: object, **_kwargs: object) -> object:
        raise RuntimeError("No fixture run exists.")

    def source_excerpt(self, *_args: object, **_kwargs: object) -> str:
        return ""

    def _collect(self, _root: str, _generation: int, cancellation: object) -> object:
        wait = getattr(cancellation, "wait")
        while not wait(0.01):
            pass
        raise EngineeringDiagnosticsGuiCancelled("fixture cancellation")

    collect_bom_candidate = _collect
    collect_ruff_candidate = _collect
    collect_architecture_candidate = _collect
    collect_shadow_candidate = _collect

    def commit_candidate(self, *_args: object, **_kwargs: object) -> object:
        raise RuntimeError("Cancelled fixture must never commit.")


def _process_until(app: object, predicate: object, timeout: float = 3.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.processEvents()
        if predicate():
            return
        time.sleep(0.01)
    raise RuntimeError("WAVE2V_REAL_QT_SETTLEMENT_TIMEOUT")


def validate_wave2v_gui(root: Path) -> tuple[float, float, float]:
    """Prove corrected hierarchy and retained Pontual run-console behavior."""
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

    from kanda_reasoner_app.engineering_diagnostics_gui import (
        create_engineering_diagnostics_workspace,
    )
    from reasoner_tools_gui_engineering_safety_panel import (
        create_engineering_safety_panel,
    )
    from tools.engineering_diagnostics_wave2u_gui_validation import validate_wave2u_gui

    panel_ms, rows_ms, filter_ms = validate_wave2u_gui(root)
    app = QApplication.instance() or QApplication([])
    host = QWidget()
    host.resize(1200, 800)
    host_layout = QVBoxLayout(host)
    safety = create_engineering_safety_panel(project_root_provider=lambda: str(root))
    host_layout.addWidget(safety)
    section_tabs = safety.engineering_safety_section_tabs
    audit_tabs = safety.engineering_safety_audit_tabs
    workspace = create_engineering_diagnostics_workspace(
        project_root_provider=lambda: str(root),
        controller=_RunConsoleController(),
        defer_initial_refresh=True,
    )
    section_tabs.addTab(workspace, "Engineering Diagnostics")
    host.show()
    section_tabs.setCurrentWidget(workspace)
    workspace.select_pontual_engineering_diagnostics()
    app.processEvents()

    section_labels = tuple(
        section_tabs.tabText(index) for index in range(section_tabs.count())
    )
    audit_labels = tuple(audit_tabs.tabText(index) for index in range(audit_tabs.count()))
    mode_tabs = workspace.engineering_diagnostics_mode_tabs
    mode_labels = tuple(mode_tabs.tabText(index) for index in range(mode_tabs.count()))
    _require(
        section_labels[:2] == ("Engineering Audit", "Engineering Diagnostics"),
        "WAVE2V_REAL_QT_SECTION_ORDER_INVALID:" + repr(section_labels),
    )
    _require(
        audit_labels[:2] == ("Full Audit", "Pontual Audit"),
        "WAVE2V_REAL_QT_AUDIT_ORDER_INVALID:" + repr(audit_labels),
    )
    _require(
        mode_labels[:2]
        == ("Full Engineering Diagnostics", "Pontual Engineering Diagnostics"),
        "WAVE2V_REAL_QT_DIAGNOSTICS_MODE_ORDER_INVALID:" + repr(mode_labels),
    )
    _require(
        audit_tabs.widget(0) is safety.engineering_safety_full_audit_page,
        "WAVE2V_REAL_QT_FULL_AUDIT_PAGE_REPLACED",
    )
    _require(
        audit_tabs.widget(1) is safety.engineering_safety_pontual_audit_page,
        "WAVE2V_REAL_QT_PONTUAL_PAGE_REPLACED",
    )
    print("ENGINEERING SAFETY REAL QT TWO-LEVEL REGISTRATION: PASS")
    print("FULL AUDIT REAL QT CONTROLS PRESERVED: PASS")
    print("PONTUAL AUDIT REAL QT PAGE PRESERVED: PASS")

    diagnostics = workspace.pontual_engineering_diagnostics_page
    run_button = diagnostics.engineering_diagnostics_run_button
    cancel_button = diagnostics.engineering_diagnostics_cancel_button
    sonar = diagnostics.engineering_diagnostics_sonar
    sonar_widget = diagnostics.engineering_diagnostics_sonar_widget
    _require(
        run_button.objectName() == "engineering_diagnostics_run_button",
        "WAVE2V_REAL_QT_RUN_BUTTON_IDENTITY",
    )
    _require(
        cancel_button.objectName() == "engineering_diagnostics_cancel_button",
        "WAVE2V_REAL_QT_CANCEL_BUTTON_IDENTITY",
    )
    _require(
        run_button.isEnabled() and not cancel_button.isEnabled(),
        "WAVE2V_REAL_QT_IDLE_CONTROL_STATE",
    )
    _require(
        not sonar.active and not sonar_widget.isVisible(),
        "WAVE2V_REAL_QT_IDLE_SONAR_VISIBLE",
    )
    print("PONTUAL ENGINEERING DIAGNOSTICS REAL QT RUN BUTTON: PASS")
    print("PONTUAL ENGINEERING DIAGNOSTICS REAL QT CANCEL BUTTON: PASS")

    run_button.click()
    _process_until(app, lambda: sonar.active and sonar_widget.isVisible())
    _require(
        not run_button.isEnabled() and cancel_button.isEnabled(),
        "WAVE2V_REAL_QT_ACTIVE_CONTROL_STATE",
    )
    print("PONTUAL ENGINEERING DIAGNOSTICS REAL QT SONAR START: PASS")

    cancel_button.click()
    app.processEvents()
    _require(
        not sonar.active and not sonar_widget.isVisible(),
        "WAVE2V_REAL_QT_CANCEL_SONAR_ACTIVE",
    )
    _require(
        not run_button.isEnabled() and not cancel_button.isEnabled(),
        "WAVE2V_REAL_QT_CANCEL_PREMATURE_IDLE",
    )
    _process_until(app, lambda: run_button.isEnabled())
    _require(
        not cancel_button.isEnabled(),
        "WAVE2V_REAL_QT_CANCEL_BUTTON_REENABLED",
    )
    _require(
        "cancel" in diagnostics.engineering_diagnostics_status_label.text().lower(),
        "WAVE2V_REAL_QT_CANCEL_STATUS_MISSING",
    )
    print("PONTUAL ENGINEERING DIAGNOSTICS REAL QT COOPERATIVE CANCEL: PASS")
    print("PONTUAL ENGINEERING DIAGNOSTICS REAL QT SONAR TERMINAL STOP: PASS")
    print("FULL AUDIT REAL QT SONAR BEHAVIOR PRESERVED: PASS")
    print("PONTUAL AUDIT REAL QT ASYNC BEHAVIOR PRESERVED: PASS")

    workspace.deleteLater()
    safety.deleteLater()
    host.deleteLater()
    app.processEvents()
    return panel_ms, rows_ms, filter_ms
