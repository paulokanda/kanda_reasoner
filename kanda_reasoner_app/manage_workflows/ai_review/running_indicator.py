"""Floating green sonar activity monitor for Workflow Review work."""

from __future__ import annotations

from typing import Any

from kanda_reasoner_app.templates.green_sonar_monitor import GreenSonarActivityMonitor

__all__ = ["Tab2ActivityIndicator", "install_tab2_activity_indicator"]


_DETERMINISTIC_CONTEXT = {
    "check": (
        "Checking workflow manifest contracts",
        "Comparing routes, tools, and workflow evidence",
        "Results stay in the Workflow Review output panel",
    ),
    "correct": (
        "Preparing governed workflow corrections",
        "Preserving review gates before any write action",
        "Correction evidence remains visible for audit",
    ),
    "validate": (
        "Validating workflow ownership and routing",
        "Scanning workflow helpers for contract drift",
        "No confirmation gates are bypassed",
    ),
}


def _workflow_details(mode: str) -> tuple[str, str, str]:
    normalized = str(mode or "check").strip().lower()
    return _DETERMINISTIC_CONTEXT.get(normalized, (
        "Running deterministic Workflow Review work",
        "Checking workflow evidence and routing contracts",
        "Review the output panel before continuing",
    ))


class Tab2ActivityIndicator:
    """Compatibility facade backed by a floating green sonar monitor."""

    def __init__(self, window: Any) -> None:
        self._monitor = GreenSonarActivityMonitor(
            window,
            title="Workflow Review",
        )

    def widget(self) -> Any:
        """Return the floating panel for legacy layout insertion compatibility."""
        return self._monitor.widget()

    def start_deterministic(self, mode: str) -> None:
        """Show deterministic Tab 2 work context."""
        normalized = str(mode or "check").strip().lower()
        self._monitor.start(
            "Running " + normalized + " mode",
            _workflow_details(normalized),
        )

    def start_ai_review(self, label: str) -> None:
        """Show advisory AI review context."""
        model_label = str(label or "local model").strip()
        self._monitor.start(
            "Advisory AI review running",
            (
                "Reading the latest deterministic workflow output",
                "Model: " + model_label,
                "AI output remains advisory, not authoritative",
            ),
        )

    def finish_success(self, message: str) -> None:
        """Show a brief success state, then hide."""
        self._monitor.finish_success(
            "Complete: " + str(message or "work finished"),
            (
                "Workflow Review process finished",
                "Review the workflow output panel if needed",
                "Ready for the next governed action",
            ),
        )

    def finish_error(self, message: str) -> None:
        """Show a brief attention state, then hide."""
        self._monitor.finish_error(
            "Needs review: " + str(message or "work finished"),
            (
                "Workflow Review process finished with issues",
                "Check the output panel before continuing",
                "No automatic write is performed by this monitor",
            ),
        )

    def set_idle(self) -> None:
        """Hide the monitor and stop animation."""
        self._monitor.set_idle()


def install_tab2_activity_indicator(window: Any, layout: Any) -> Tab2ActivityIndicator:
    """Install and return the Tab 2 floating green sonar activity monitor."""
    indicator = Tab2ActivityIndicator(window)
    window._tab2_activity_indicator = indicator
    return indicator
