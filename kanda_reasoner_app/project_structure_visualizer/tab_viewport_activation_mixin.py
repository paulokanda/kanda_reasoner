# project-path: kanda_reasoner_app/project_structure_visualizer/tab_viewport_activation_mixin.py
"""Visibility recovery for the embedded Project Structure 3D WebGL viewport."""

from __future__ import annotations

import json
from typing import Any

from PySide6.QtCore import QTimer

__all__: list[str] = []


class ProjectStructureViewportActivationMixin:
    """Resize, resume, and refit WebGL after an inactive tab becomes visible."""

    def _initialize_viewport_activation(self) -> None:
        """Create one bounded activation timer owned by the widget."""
        self._viewport_activation_timer = QTimer(self)
        self._viewport_activation_timer.setSingleShot(True)
        self._viewport_activation_timer.timeout.connect(
            self._activate_renderer_viewport
        )
        self._viewport_activation_attempts = 0
        self._viewport_activation_generation = ""
        self._viewport_activation_force_fit = False
        self._last_viewport_diagnostics: dict[str, Any] = {}

    def _schedule_viewport_activation(self, *, force_fit: bool) -> None:
        """Schedule one post-layout renderer activation for the live page."""
        if self._web_view is None or not self.isVisible():
            return
        generation = str(self._generation_id)
        if generation != self._viewport_activation_generation:
            self._viewport_activation_generation = generation
            self._viewport_activation_attempts = 0
        self._viewport_activation_force_fit = (
            self._viewport_activation_force_fit or bool(force_fit)
        )
        self._viewport_activation_timer.start(60)

    def _activate_renderer_viewport(self) -> None:
        """Ask the page to recover from hidden or zero-sized initialization."""
        web_view = self._web_view
        generation = str(self._generation_id)
        if (
            web_view is None
            or not self.isVisible()
            or generation != self._viewport_activation_generation
        ):
            return
        self._viewport_activation_attempts += 1
        force_fit = "true" if self._viewport_activation_force_fit else "false"
        script = (
            "JSON.stringify(window.kandaProjectGraph && "
            "window.kandaProjectGraph.activateViewport("
            + force_fit
            + "))"
        )
        try:
            web_view.page().runJavaScript(
                script,
                self._on_viewport_activation_result,
            )
        except (AttributeError, RuntimeError):
            self.status_label.setText("Renderer is no longer available.")

    def _on_viewport_activation_result(self, result: Any) -> None:
        """Accept observable dimensions and retry while layout is still hidden."""
        try:
            payload = json.loads(result) if isinstance(result, str) else {}
        except (TypeError, ValueError):
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        if str(payload.get("generationId") or "") != str(
            self._viewport_activation_generation
        ):
            return
        self._last_viewport_diagnostics = payload
        if payload.get("ready") is True:
            self._viewport_activation_force_fit = False
            return
        if self._viewport_activation_attempts < 10 and self.isVisible():
            self._viewport_activation_timer.start(140)
            return
        self.status_label.setText(
            "Renderer viewport stayed unavailable after tab activation."
        )

    def _stop_viewport_activation(self) -> None:
        """Stop activation retries before widget teardown."""
        timer = getattr(self, "_viewport_activation_timer", None)
        if timer is not None:
            timer.stop()

    def showEvent(self, event: object) -> None:
        """Recover a renderer that was initialized while its tab was hidden."""
        super().showEvent(event)
        self._schedule_viewport_activation(force_fit=True)

    def resizeEvent(self, event: object) -> None:
        """Keep the WebGL drawing buffer aligned with the visible viewport."""
        super().resizeEvent(event)
        self._schedule_viewport_activation(force_fit=False)
