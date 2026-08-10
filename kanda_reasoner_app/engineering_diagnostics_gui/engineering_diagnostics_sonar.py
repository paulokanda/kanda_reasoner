# project-path: kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_sonar.py
"""Public Engineering Diagnostics adapter for the canonical green sonar."""

from __future__ import annotations

from typing import Any

__all__ = ["create_engineering_diagnostics_sonar"]


class _EngineeringDiagnosticsSonar:
    """Bind Diagnostics activity to one reusable sonar monitor."""

    def __init__(self, monitor: Any) -> None:
        self._monitor = monitor
        self._active = False

    @property
    def active(self) -> bool:
        """Return whether Diagnostics currently owns the activity monitor."""
        return self._active

    def widget(self) -> Any:
        """Return the canonical floating sonar widget."""
        return self._monitor.widget()

    def start(self, collector_label: str) -> None:
        """Show the sonar while the selected collector is running."""
        label = str(collector_label or "Engineering").strip()
        self._active = True
        self._monitor.start(
            "Engineering Diagnostics running",
            (
                label + " collector is processing the selected Project",
                "Results remain read-only until store commit succeeds",
                "Cancel Diagnostics requests cooperative cancellation",
            ),
        )

    def stop(self) -> None:
        """Stop and hide the sonar on cancellation or worker settlement."""
        self._active = False
        self._monitor.set_idle()


def create_engineering_diagnostics_sonar(parent: object | None = None) -> object:
    """Create a Diagnostics adapter over the public green sonar template."""
    if parent is None:
        raise RuntimeError("Engineering Diagnostics sonar requires a QWidget host.")

    from kanda_reasoner_app.templates.green_sonar_monitor import (
        GreenSonarActivityMonitor,
    )

    monitor = GreenSonarActivityMonitor(
        parent,
        title="Engineering Diagnostics",
        host=parent,
    )
    monitor.setObjectName("engineeringDiagnosticsSonarMonitor")
    return _EngineeringDiagnosticsSonar(monitor)
