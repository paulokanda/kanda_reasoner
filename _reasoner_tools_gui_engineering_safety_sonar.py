# project-path: _reasoner_tools_gui_engineering_safety_sonar.py
"""Engineering Safety adapter for KANDA's canonical green sonar monitor."""

from __future__ import annotations

from typing import Any

__all__: list[str] = []


class _EngineeringSafetySonarAdapter:
    """Expose the Full Audit lifecycle through the shared sonar template."""

    def __init__(self, monitor: Any) -> None:
        self._monitor = monitor
        self._active = False

    @property
    def active(self) -> bool:
        """Return whether Full Audit currently owns the activity monitor."""
        return self._active

    def widget(self) -> Any:
        """Return the canonical floating sonar panel widget."""
        return self._monitor.widget()

    def isVisible(self) -> bool:  # noqa: N802
        """Return whether the canonical sonar panel is visible."""
        return bool(self.widget().isVisible())

    def isVisibleTo(self, ancestor: Any) -> bool:  # noqa: N802
        """Return whether the canonical panel is visible to ``ancestor``."""
        return bool(self.widget().isVisibleTo(ancestor))

    def start(self) -> None:
        """Start KANDA's canonical green sonar for Full Audit."""
        self._active = True
        self._monitor.start(
            "Engineering review running",
            (
                "Complete Engineering Review is processing the catalog",
                "Results are written to the discriminated Full Audit log",
                "Cancel Review remains cooperative between catalog items",
            ),
        )

    def stop(self) -> None:
        """Stop and hide the canonical sonar on cancel or settlement."""
        self._active = False
        self._monitor.set_idle()


def create_engineering_safety_sonar(parent: object | None = None) -> object:
    """Create a Full Audit adapter over the reusable KANDA sonar template."""
    if parent is None:
        raise RuntimeError("Engineering Safety sonar requires a QWidget host.")

    from kanda_reasoner_app.templates.green_sonar_monitor import (
        GreenSonarActivityMonitor,
    )

    monitor = GreenSonarActivityMonitor(
        parent,
        title="Engineering Safety Full Audit",
        host=parent,
    )
    monitor.setObjectName("engineeringSafetyFullAuditSonarMonitor")
    return _EngineeringSafetySonarAdapter(monitor)
