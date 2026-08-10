# project-path: kanda_reasoner_app/engineering_diagnostics_gui/__init__.py
"""Public GUI contract for Engineering Diagnostics Wave 2O-B."""

from .bom_provider import BomReportProvider, SafetySuiteBomReportProvider
from .controller import EngineeringDiagnosticsController
from .engineering_diagnostics_tab import create_engineering_diagnostics_panel
from .engineering_diagnostics_workspace import create_engineering_diagnostics_workspace
from .full_engineering_diagnostics_tab import create_full_engineering_diagnostics_panel
from .full_audit_drillthrough_ui import install_full_audit_diagnostics_drillthrough_ui
from .navigation import (
    build_engineering_diagnostics_navigation_summary,
    request_engineering_diagnostics_navigation,
)
from .navigation_models import (
    EngineeringDiagnosticsNavigationRequest,
    EngineeringDiagnosticsNavigationSummary,
)
from .models import (
    DiagnosticFindingView,
    DiagnosticRunView,
    DiagnosticScanCandidate,
    EngineeringDiagnosticsGuiCancelled,
)
from .review_handoff import build_complete_review_ai_correction_handoff
from .source_identity import project_source_fingerprint

__all__ = [
    "BomReportProvider",
    "DiagnosticFindingView",
    "DiagnosticRunView",
    "DiagnosticScanCandidate",
    "EngineeringDiagnosticsController",
    "EngineeringDiagnosticsGuiCancelled",
    "EngineeringDiagnosticsNavigationRequest",
    "EngineeringDiagnosticsNavigationSummary",
    "SafetySuiteBomReportProvider",
    "build_complete_review_ai_correction_handoff",
    "build_engineering_diagnostics_navigation_summary",
    "create_engineering_diagnostics_panel",
    "create_engineering_diagnostics_workspace",
    "create_full_engineering_diagnostics_panel",
    "install_full_audit_diagnostics_drillthrough_ui",
    "request_engineering_diagnostics_navigation",
    "project_source_fingerprint",
]
