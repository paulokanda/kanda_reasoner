# project-path: kanda_reasoner_app/project_structure_visualizer/tab_navigation_mixin.py
"""Read-only focus controls and renderer command routing for v1D."""

from __future__ import annotations

import json
from typing import Any, Callable

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

__all__: list[str] = []


class ProjectStructureNavigationMixin:
    """Add visual navigation without changing graph or Project evidence."""

    def _install_navigation_bar(self, root_layout: Any) -> None:
        """Install a second compact row to avoid toolbar width pressure."""
        frame = QFrame()
        frame.setObjectName("projectStructure3DNavigation")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(7)
        label = QLabel("Focus tools")
        label.setObjectName("projectStructure3DNavigationLabel")
        layout.addWidget(label)

        controls = (
            ("Back", self._navigate_back, "Return to the previous focused node."),
            ("Forward", self._navigate_forward, "Move to the next focused node."),
            ("Overview", self._show_graph_overview, "Show the full visible graph."),
            (
                "Isolate selected",
                self._isolate_selected_node,
                "Show the selected node and its direct neighborhood.",
            ),
            (
                "Expand / collapse",
                self._toggle_selected_expansion,
                "Toggle descendants of the selected package or module.",
            ),
            (
                "Path to search",
                self._trace_dependency_path,
                "Trace a relationship path from the selected node to the search target.",
            ),
        )
        for text, callback, tooltip in controls:
            button = QPushButton(text)
            button.setToolTip(tooltip)
            button.clicked.connect(callback)
            layout.addWidget(button)
        layout.addStretch(1)
        root_layout.addWidget(frame)
        self.navigation_frame = frame

    def _run_navigation_command(
        self,
        command_name: str,
        *arguments: object,
        callback: Callable[[Any], None] | None = None,
    ) -> None:
        """Run one allowlisted read-only navigation command."""
        allowed = {
            "goBack",
            "goForward",
            "showOverview",
            "isolateSelected",
            "toggleSelectedExpansion",
            "tracePathToQuery",
        }
        if command_name not in allowed:
            return
        web_view = self._web_view
        if web_view is None:
            self.status_label.setText("Navigation requires the embedded renderer.")
            return
        encoded_arguments = ",".join(
            json.dumps(value, ensure_ascii=True) for value in arguments
        )
        script = (
            "window.kandaProjectGraph && "
            f"window.kandaProjectGraph.{command_name}({encoded_arguments});"
        )
        try:
            web_view.page().runJavaScript(
                script,
                callback or self._on_navigation_result,
            )
        except (AttributeError, RuntimeError):
            self.status_label.setText("Renderer is no longer available.")

    def _on_navigation_result(self, result: Any) -> None:
        """Display one bounded renderer navigation result."""
        if not isinstance(result, dict):
            self.status_label.setText("Navigation action returned no result.")
            return
        message = str(result.get("message") or "Navigation updated.")[:240]
        self.status_label.setText(message)

    @Slot()
    def _navigate_back(self) -> None:
        """Return to the previous visual focus."""
        self._run_navigation_command("goBack")

    @Slot()
    def _navigate_forward(self) -> None:
        """Move to the next visual focus."""
        self._run_navigation_command("goForward")

    @Slot()
    def _show_graph_overview(self) -> None:
        """Clear temporary focus state and fit the visible graph."""
        self._run_navigation_command("showOverview")

    @Slot()
    def _isolate_selected_node(self) -> None:
        """Show only the selected node and its direct neighborhood."""
        self._run_navigation_command("isolateSelected")

    @Slot()
    def _toggle_selected_expansion(self) -> None:
        """Toggle descendants of the selected package or module."""
        self._run_navigation_command("toggleSelectedExpansion")

    @Slot()
    def _trace_dependency_path(self) -> None:
        """Trace a relationship path to the current search target."""
        query = self.search_edit.text().strip()
        if not query:
            self.status_label.setText(
                "Enter the target node in Search before tracing a path."
            )
            return
        self._run_navigation_command("tracePathToQuery", query)
