# project-path: kanda_reasoner_app/engineering_diagnostics_gui/full_audit_drillthrough_ui.py
"""Qt binding for Full Audit drill-through through public contracts."""

from __future__ import annotations

from collections.abc import Callable

from .navigation import (
    build_engineering_diagnostics_navigation_summary,
    request_engineering_diagnostics_navigation,
)
from .navigation_models import EngineeringDiagnosticsNavigationRequest

__all__ = ["install_full_audit_diagnostics_drillthrough_ui"]


def install_full_audit_diagnostics_drillthrough_ui(
    safety_panel: object,
    diagnostics_panel: object,
    *,
    project_root_provider: Callable[[], str],
    select_diagnostics_tab: Callable[[], None],
    diagnostic_links_provider: Callable[[str], tuple[object, ...]],
) -> object:
    """Install read-only summary rows over the frozen Full Audit report surface."""
    from PySide6.QtWidgets import (
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )

    full_page = getattr(safety_panel, "engineering_safety_full_audit_page", None)
    full_log = getattr(safety_panel, "engineering_safety_full_audit_log", None)
    if full_page is None or full_log is None or full_page.layout() is None:
        raise RuntimeError("ENGINEERING_SAFETY_FULL_AUDIT_PUBLIC_SURFACE_MISSING")
    controller = getattr(diagnostics_panel, "engineering_diagnostics_controller", None)
    if controller is None:
        raise RuntimeError("ENGINEERING_DIAGNOSTICS_PUBLIC_CONTROLLER_MISSING")

    group = QGroupBox("Engineering Diagnostics drill-through", full_page)
    group.setObjectName("full_audit_engineering_diagnostics_drillthrough")
    rows_layout = QVBoxLayout(group)
    rows_layout.setContentsMargins(8, 8, 8, 8)
    rows_layout.setSpacing(6)
    full_page.layout().insertWidget(1, group)
    state: dict[str, object] = {
        "report": "",
        "rows": [],
        "buttons": [],
        "refresh_generation": 0,
    }
    group.engineering_diagnostics_drillthrough_buttons = ()
    group.engineering_diagnostics_drillthrough_refresh_generation = 0

    def publish_projection() -> None:
        buttons = tuple(state["buttons"])
        generation = int(state["refresh_generation"])
        group.engineering_diagnostics_drillthrough_buttons = buttons
        group.engineering_diagnostics_drillthrough_refresh_generation = generation
        safety_panel.engineering_diagnostics_drillthrough_buttons = buttons
        safety_panel.engineering_diagnostics_drillthrough_refresh_generation = generation

    def clear_rows() -> None:
        for widget in state["rows"]:
            rows_layout.removeWidget(widget)
            widget.deleteLater()
        state["rows"] = []
        state["buttons"] = []

    def open_diagnostics(producer_id: str, run_id: str) -> None:
        request = EngineeringDiagnosticsNavigationRequest(
            producer_id=producer_id,
            compatible_run_id=run_id,
            baseline_state="current",
            severity="all",
            origin="full_audit",
        )
        if request_engineering_diagnostics_navigation(diagnostics_panel, request):
            select_diagnostics_tab()

    def refresh() -> None:
        report = str(full_log.toPlainText() or "")
        if report == state["report"]:
            return
        state["report"] = report
        state["refresh_generation"] = int(state["refresh_generation"]) + 1
        clear_rows()
        links = diagnostic_links_provider(report)
        if not links:
            label = QLabel(
                "Run Complete Enginneering Review to create collector drill-through rows.",
                group,
            )
            label.setWordWrap(True)
            rows_layout.addWidget(label)
            state["rows"] = [label]
            publish_projection()
            return
        row_widgets: list[object] = []
        row_buttons: list[object] = []
        for link in links:
            summary = build_engineering_diagnostics_navigation_summary(
                controller,
                project_root_provider(),
                link.producer_id,
            )
            row = QWidget(group)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            summary_text = link.label + " | Assessment: " + (link.assessment or "UNKNOWN")
            if summary.available:
                summary_text += (
                    " | raw: "
                    + str(summary.raw_finding_count)
                    + " | canonical: "
                    + str(summary.canonical_issue_count)
                    + " | groups: "
                    + str(summary.diagnostic_group_count)
                    + " | new errors: "
                    + str(summary.new_high_priority_count)
                )
            else:
                summary_text += " | no source-compatible diagnostic run"
            label = QLabel(summary_text, row)
            label.setWordWrap(True)
            button = QPushButton("Open in Engineering Diagnostics", row)
            button.setObjectName(
                "full_audit_engineering_diagnostics_open_button"
            )
            button.setEnabled(summary.available)
            if not summary.available:
                button.setToolTip(
                    "Run the matching Engineering Diagnostics collector for the current source first."
                )
            button.clicked.connect(
                lambda _checked=False, producer=link.producer_id, run_id=summary.compatible_run_id: open_diagnostics(
                    producer,
                    run_id,
                )
            )
            row_layout.addWidget(label, 1)
            row_layout.addWidget(button)
            rows_layout.addWidget(row)
            row_widgets.append(row)
            row_buttons.append(button)
        state["rows"] = row_widgets
        state["buttons"] = row_buttons
        publish_projection()

    safety_panel.refresh_engineering_diagnostics_drillthrough = refresh
    safety_panel.engineering_diagnostics_drillthrough_group = group
    full_log.textChanged.connect(
        safety_panel.refresh_engineering_diagnostics_drillthrough
    )
    refresh()
    return group
