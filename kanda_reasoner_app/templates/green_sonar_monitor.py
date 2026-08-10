# project-path: kanda_reasoner_app/templates/green_sonar_monitor.py
"""Public facade for the reusable green sonar activity monitor."""

from __future__ import annotations

from ._green_sonar_activity_monitor import _GreenSonarActivityMonitor

__all__ = ["GreenSonarActivityMonitor"]


class GreenSonarActivityMonitor(_GreenSonarActivityMonitor):
    """Public facade class for the reusable green sonar activity monitor."""
