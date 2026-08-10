# project-path: tools/engineering_diagnostics_wave2w_gui_validation.py
"""Real Qt validation for Full and Pontual Diagnostics hierarchy Wave 2W."""

from __future__ import annotations

from pathlib import Path
import time

from kanda_reasoner_app.engineering_diagnostics_gui.models import (
    EngineeringDiagnosticsGuiCancelled,
)

__all__ = ["validate_wave2w_gui"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


class _FullRunController:
    """Public controller fixture that waits for cooperative cancellation."""

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
    raise RuntimeError("WAVE2W_REAL_QT_SETTLEMENT_TIMEOUT")


def validate_wave2w_gui(root: Path) -> tuple[float, float, float]:
    """Validate Full Diagnostics controls after preserving Pontual behavior."""
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

    from kanda_reasoner_app.engineering_diagnostics_gui import (
        create_full_engineering_diagnostics_panel,
    )
    from tools.engineering_diagnostics_wave2v_gui_validation import validate_wave2v_gui

    panel_ms, rows_ms, filter_ms = validate_wave2v_gui(root)
    app = QApplication.instance() or QApplication([])
    host = QWidget()
    host.resize(1000, 700)
    layout = QVBoxLayout(host)
    full = create_full_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        controller=_FullRunController(),
    )
    layout.addWidget(full)
    host.show()
    app.processEvents()

    run_button = full.full_engineering_diagnostics_run_button
    cancel_button = full.full_engineering_diagnostics_cancel_button
    sonar = full.full_engineering_diagnostics_sonar
    sonar_widget = full.full_engineering_diagnostics_sonar_widget
    _require(
        full.full_engineering_diagnostics_collectors
        == ("BOM", "Ruff", "Architecture", "Shadow"),
        "WAVE2W_REAL_QT_COLLECTOR_SET_INVALID",
    )
    _require(
        run_button.text() == "Run All Engineering Diagnostics",
        "WAVE2W_REAL_QT_FULL_RUN_BUTTON_TEXT",
    )
    _require(
        cancel_button.text() == "Cancel Diagnostics",
        "WAVE2W_REAL_QT_FULL_CANCEL_BUTTON_TEXT",
    )
    _require(
        run_button.isEnabled() and not cancel_button.isEnabled(),
        "WAVE2W_REAL_QT_FULL_IDLE_STATE",
    )
    _require(
        not sonar.active and not sonar_widget.isVisible(),
        "WAVE2W_REAL_QT_FULL_IDLE_SONAR_VISIBLE",
    )
    print("FULL ENGINEERING DIAGNOSTICS REAL QT RUN BUTTON: PASS")
    print("FULL ENGINEERING DIAGNOSTICS REAL QT CANCEL BUTTON: PASS")
    print("FULL ENGINEERING DIAGNOSTICS REAL QT COLLECTOR SET: PASS")

    run_button.click()
    _process_until(app, lambda: sonar.active and sonar_widget.isVisible())
    _require(
        not run_button.isEnabled() and cancel_button.isEnabled(),
        "WAVE2W_REAL_QT_FULL_ACTIVE_STATE",
    )
    print("FULL ENGINEERING DIAGNOSTICS REAL QT SONAR START: PASS")

    cancel_button.click()
    app.processEvents()
    _require(
        not sonar.active and not sonar_widget.isVisible(),
        "WAVE2W_REAL_QT_FULL_CANCEL_SONAR_ACTIVE",
    )
    _require(
        not run_button.isEnabled() and not cancel_button.isEnabled(),
        "WAVE2W_REAL_QT_FULL_CANCEL_PREMATURE_IDLE",
    )
    print("FULL ENGINEERING DIAGNOSTICS REAL QT SONAR CANCEL STATE: PASS")
    _process_until(app, lambda: run_button.isEnabled())
    _require(
        not cancel_button.isEnabled(),
        "WAVE2W_REAL_QT_FULL_CANCEL_BUTTON_REENABLED",
    )
    _require(
        "cancel" in full.full_engineering_diagnostics_status_label.text().lower(),
        "WAVE2W_REAL_QT_FULL_CANCEL_STATUS_MISSING",
    )
    print("FULL ENGINEERING DIAGNOSTICS REAL QT COOPERATIVE CANCEL: PASS")
    print("FULL ENGINEERING DIAGNOSTICS REAL QT SONAR TERMINAL STOP: PASS")

    full.deleteLater()
    host.deleteLater()
    app.processEvents()
    return panel_ms, rows_ms, filter_ms
