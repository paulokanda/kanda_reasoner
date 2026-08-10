# project-path: kanda_reasoner_app/engineering_diagnostics_gui/_navigation_ui.py
"""Private Qt binding for the public Engineering Diagnostics navigation request."""

from __future__ import annotations

from collections.abc import Callable

from .navigation_models import EngineeringDiagnosticsNavigationRequest

__all__: list[str] = []


def _set_combo_text(combo: object, value: str) -> None:
    index = combo.findText(value)
    if index < 0:
        raise RuntimeError("ENGINEERING_DIAGNOSTICS_NAVIGATION_FILTER_UNSUPPORTED:" + value)
    combo.setCurrentIndex(index)


def _bind_engineering_diagnostics_navigation(
    panel: object,
    controller: object,
    current_project_root: Callable[[], str],
    producer_combo: object,
    run_combo: object,
    severity_combo: object,
    baseline_combo: object,
    search_edit: object,
    refresh_history: Callable[[str], None],
    update_run_button: Callable[[], None],
    apply_filters: Callable[[], None],
    status_label: object,
) -> None:
    """Bind a fail-closed public request without exposing widget internals."""

    def apply_request(request: EngineeringDiagnosticsNavigationRequest) -> bool:
        if not isinstance(request, EngineeringDiagnosticsNavigationRequest):
            raise TypeError("EngineeringDiagnosticsNavigationRequest is required.")
        root = current_project_root()
        runs = controller.list_runs(root, producer_id=request.producer_id, limit=200)
        if request.compatible_run_id and not any(
            run.run_id == request.compatible_run_id for run in runs
        ):
            status_label.setText(
                "Full Audit drill-through blocked: compatible run is unavailable."
            )
            return False
        producer_index = producer_combo.findData(request.producer_id)
        if producer_index < 0:
            status_label.setText(
                "Full Audit drill-through blocked: collector is unavailable."
            )
            return False
        previous = producer_combo.blockSignals(True)
        producer_combo.setCurrentIndex(producer_index)
        producer_combo.blockSignals(previous)
        update_run_button()
        refresh_history(request.compatible_run_id)
        if request.compatible_run_id and str(run_combo.currentData() or "") != request.compatible_run_id:
            status_label.setText(
                "Full Audit drill-through blocked: exact run was not selected."
            )
            return False
        _set_combo_text(severity_combo, request.severity)
        _set_combo_text(baseline_combo, request.baseline_state)
        search_edit.setText(request.rule_family)
        apply_filters()
        panel.engineering_diagnostics_last_navigation = request
        status_label.setText(
            "Full Audit drill-through applied: " + request.producer_id
        )
        return True

    panel.apply_engineering_diagnostics_navigation = apply_request
    panel.engineering_diagnostics_navigation_contract_version = "1.0"
