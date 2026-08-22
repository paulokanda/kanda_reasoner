# project-path: kanda_reasoner_app/project_structure_visualizer/project_structure_3d_tab.py
"""Read-only Project Structure 3D PySide6 tab."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QMessageBox,
    QTextEdit,
    QWidget,
)

from .details_presenter import node_details_html, overview_details_html
from .fixture_graph import build_fixture_graph
from .graph_snapshot_builder import GraphSnapshotBuild
from .graph_schema import graph_snapshot_json
from .graph_view_filters import filter_graph_snapshot
from .tab_evidence_mixin import ProjectStructureEvidenceMixin
from .tab_json_controls_mixin import ProjectStructureJsonControlsMixin
from .tab_ui_builder import build_project_structure_3d_ui
from .tab_navigation_mixin import ProjectStructureNavigationMixin
from .tab_style import project_structure_3d_style
from .tab_viewport_activation_mixin import (
    ProjectStructureViewportActivationMixin,
)
from .web_assets import asset_root
from .web_bridge import create_bridge_bundle
from .web_runtime import (
    LocalVisualizerDocuments,
    configure_web_settings,
)

__all__ = ["ProjectStructure3DWidget"]


class ProjectStructure3DWidget(
    ProjectStructureJsonControlsMixin,
    ProjectStructureNavigationMixin,
    ProjectStructureEvidenceMixin,
    ProjectStructureViewportActivationMixin,
    QWidget,
):
    """Display an immutable Project graph from existing KANDA evidence."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("projectStructure3DWidget")
        self._project_root: Path | None = None
        self._generation_id = uuid.uuid4().hex
        initial_snapshot = build_fixture_graph()
        self._build_result = GraphSnapshotBuild(
            snapshot=initial_snapshot,
            source_status="fixture_unselected",
            source_label="Fixture fallback",
            fallback_reason="No Project has been selected yet.",
        )
        self._source_snapshot = initial_snapshot
        self._view_mode = "structure"
        self._show_imports = True
        self._show_external = True
        self._show_symbols = True
        self._show_semantic = True
        self._snapshot = filter_graph_snapshot(
            self._source_snapshot,
            mode=self._view_mode,
            show_imports=self._show_imports,
            show_external=self._show_external,
            show_symbols=self._show_symbols,
            show_semantic=self._show_semantic,
        )
        self._nodes_by_id = {
            node["id"]: node for node in self._snapshot["nodes"]
        }
        self._renderer_ready = False
        self._page_load_ok: bool | None = None
        self._renderer_diagnostics: list[str] = []
        self._render_termination: tuple[str, int] | None = None
        self._documents = LocalVisualizerDocuments()
        self._web_view: QWidget | None = None
        self._bridge_bundle: object | None = None
        self._bridge_retry_timer = QTimer(self)
        self._bridge_retry_timer.setInterval(250)
        self._bridge_retry_timer.timeout.connect(
            self._request_renderer_handshake
        )
        self._initialize_viewport_activation()
        self._initialize_complete_json_controls()
        self._build_ui()
        self._create_renderer()

    def _build_ui(self) -> None:
        """Build the Project Structure 3D interface."""
        build_project_structure_3d_ui(self)


    def _open_project_structure_3d_help(self) -> None:
        """Open the local Project Structure 3D help document."""
        try:
            from ..reasoner_tools_gui_shell.help_docs.renderer import (
                open_help_document_for_legacy_catalog,
            )

            rich_dialog = open_help_document_for_legacy_catalog(
                self,
                "project_structure_3d.json",
                window_title="Help - Project Structure 3D",
            )
        except Exception:
            rich_dialog = None

        if rich_dialog is not None:
            self._project_structure_help_dialog = rich_dialog
            return

        try:
            from ..reasoner_tools_gui_shell.gui_support import (
                _format_help_catalog_text,
                _help_catalog_path,
            )

            catalog_path = _help_catalog_path("project_structure_3d.json")
            if not catalog_path.is_file():
                QMessageBox.warning(
                    self,
                    "Help catalog not found",
                    "Expected Project Structure 3D help was not found:\n"
                    f"{catalog_path}",
                )
                return

            dialog = QMainWindow(self)
            dialog.setWindowTitle("Help - Project Structure 3D")
            dialog.resize(1080, 800)

            editor = QTextEdit(dialog)
            editor.setReadOnly(True)
            editor.setPlainText(_format_help_catalog_text(catalog_path))
            dialog.setCentralWidget(editor)
            dialog.show()
            self._project_structure_help_dialog = dialog
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Help could not be opened",
                "Failed to open Project Structure 3D help.\n\n"
                f"Details: {exc}",
            )

    def _apply_style(self) -> None:
        """Apply restrained local styling without changing global palette."""
        self.setStyleSheet(project_structure_3d_style())

    def _create_renderer(self) -> None:
        """Create QWebEngineView or a clear browser-only fallback."""
        try:
            from PySide6.QtWebEngineCore import QWebEngineSettings
            from PySide6.QtWebEngineWidgets import QWebEngineView

            from .safe_web_page import LocalVisualizerPage
        except ImportError as exc:
            self._install_webengine_fallback(str(exc))
            return

        web_view = QWebEngineView()
        web_view.setObjectName("projectStructure3DWebView")
        web_view.setContextMenuPolicy(Qt.NoContextMenu)
        page = LocalVisualizerPage(
            (asset_root(), self._documents.embedded_root),
            web_view,
        )
        web_view.setPage(page)
        configure_web_settings(page.settings(), QWebEngineSettings)
        bridge_bundle = create_bridge_bundle(web_view)
        bridge_bundle.connect_to_page(page)
        bridge_bundle.bridge.node_selected.connect(self._on_node_selected)
        bridge_bundle.bridge.background_selected.connect(
            self._on_background_selected
        )
        bridge_bundle.bridge.renderer_ready.connect(self._on_renderer_ready)
        bridge_bundle.bridge.renderer_error.connect(self._on_renderer_error)
        page.navigation_blocked.connect(self._on_navigation_blocked)
        page.console_message.connect(self._on_console_message)
        page.renderProcessTerminated.connect(
            self._on_render_process_terminated
        )
        web_view.loadFinished.connect(self._on_page_load_finished)

        self._web_view = web_view
        self._bridge_bundle = bridge_bundle
        setattr(web_view, "_project_structure_3d_bridge_bundle", bridge_bundle)
        setattr(self, "_project_structure_3d_bridge_bundle", bridge_bundle)
        self._viewport_layout.addWidget(web_view)
        self._load_current_snapshot()

    def _install_webengine_fallback(self, reason: str) -> None:
        """Show a contained fallback when Qt WebEngine is unavailable."""
        message = QLabel(
            "Qt WebEngine is unavailable, so the embedded 3D viewport could "
            "not be created. The standalone browser preview remains available."
        )
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignCenter)
        message.setProperty("kanda_preserve_across_project_switch", True)
        self._viewport_layout.addWidget(message)
        self.status_label.setText("Embedded renderer unavailable: " + reason[:180])

    def _load_current_snapshot(self) -> None:
        """Load a cache-busted local graph document into the current page."""
        web_view = self._web_view
        if web_view is None:
            return
        try:
            document_url = self._documents.write_embedded(
                graph_snapshot_json(self._snapshot),
                self._generation_id,
            )
        except (OSError, RuntimeError, ValueError) as exc:
            self._renderer_ready = False
            self._page_load_ok = False
            self.status_label.setText(
                "Embedded document preparation failed: " + str(exc)[:180]
            )
            return
        self._renderer_ready = False
        self._page_load_ok = None
        self._renderer_diagnostics.clear()
        self._render_termination = None
        self._bridge_retry_timer.stop()
        self.status_label.setText("Loading local Project graph...")
        web_view.setUrl(document_url)

    @Slot(bool)
    def _on_page_load_finished(self, success: bool) -> None:
        """Start a bounded bridge handshake after the local page loads."""
        self._page_load_ok = bool(success)
        if not success:
            self.status_label.setText("Renderer page load failed.")
            return
        self.status_label.setText("Renderer page loaded; connecting bridge...")
        self._bridge_retry_timer.start()
        self._request_renderer_handshake()

    @Slot()
    def _request_renderer_handshake(self) -> None:
        """Ask the loaded page to connect its narrow QWebChannel bridge."""
        if self._renderer_ready:
            self._bridge_retry_timer.stop()
            return
        web_view = self._web_view
        if web_view is None:
            self._bridge_retry_timer.stop()
            return
        script = (
            "Boolean(window.kandaProjectGraph && "
            "window.kandaProjectGraph.ensureBridge())"
        )
        try:
            web_view.page().runJavaScript(script, self._on_handshake_probe)
        except (AttributeError, RuntimeError) as exc:
            self._bridge_retry_timer.stop()
            self.status_label.setText("Renderer handshake failed: " + str(exc)[:180])

    def _on_handshake_probe(self, available: Any) -> None:
        """Retain a useful status while the bridge is still connecting."""
        if self._renderer_ready:
            return
        if not bool(available):
            self.status_label.setText("Renderer loaded; bridge bootstrap pending...")

    def _is_live_generation(self, generation_id: str) -> bool:
        """Reject stale callbacks and callbacks to a deleted Qt wrapper."""
        if str(generation_id) != self._generation_id:
            return False
        try:
            from shiboken6 import isValid

            return bool(isValid(self))
        except (ImportError, RuntimeError):
            return True

    @Slot(str, str)
    def _on_node_selected(self, generation_id: str, node_id: str) -> None:
        """Display only a node from the current immutable snapshot."""
        if not self._is_live_generation(generation_id):
            return
        node = self._nodes_by_id.get(str(node_id))
        if node is None:
            self.status_label.setText("Rejected unknown renderer node ID.")
            return
        self._show_node_details(node)
        self.status_label.setText("Selected: " + str(node["label"]))

    @Slot(str)
    def _on_background_selected(self, generation_id: str) -> None:
        """Clear details only for the active renderer generation."""
        if not self._is_live_generation(generation_id):
            return
        self._show_overview_details()
        self.status_label.setText("Selection cleared.")

    @Slot(str)
    def _on_renderer_ready(self, generation_id: str) -> None:
        """Accept readiness only from the active graph generation."""
        if not self._is_live_generation(generation_id):
            return
        self._renderer_ready = True
        self._bridge_retry_timer.stop()
        statistics = self._snapshot["statistics"]
        source_text = (
            "fixture fallback"
            if self._build_result.is_fixture
            else self._build_result.source_label
        )
        self.status_label.setText(
            f"Renderer ready: {statistics['node_count']} nodes, "
            f"{statistics['edge_count']} edges | {source_text}."
        )
        self._schedule_viewport_activation(force_fit=True)

    @Slot(str, str)
    def _on_renderer_error(self, generation_id: str, message: str) -> None:
        """Contain renderer errors without affecting other KANDA tabs."""
        if not self._is_live_generation(generation_id):
            return
        self._renderer_ready = False
        diagnostic = str(message)[:500]
        self._renderer_diagnostics.append(diagnostic)
        self._renderer_diagnostics[:] = self._renderer_diagnostics[-8:]
        self.status_label.setText("Renderer error: " + diagnostic[:240])

    @Slot(str)
    def _on_navigation_blocked(self, target: str) -> None:
        """Report blocked browser navigation without opening it."""
        self.status_label.setText("Blocked external navigation: " + target[:160])

    @Slot(str)
    def _on_console_message(self, message: str) -> None:
        """Surface only renderer console errors in the local status line."""
        bounded = str(message)[:800]
        self._renderer_diagnostics.append(bounded)
        self._renderer_diagnostics[:] = self._renderer_diagnostics[-8:]
        if "error" in bounded.lower() or "uncaught" in bounded.lower():
            self.status_label.setText("Renderer diagnostic: " + bounded[:220])

    @Slot(object, int)
    def _on_render_process_terminated(
        self,
        termination_status: object,
        exit_code: int,
    ) -> None:
        """Record a bounded renderer-process failure for diagnostics."""
        status_name = getattr(termination_status, "name", str(termination_status))
        self._render_termination = (str(status_name), int(exit_code))
        message = f"render process terminated: {status_name}; exit={int(exit_code)}"
        self._renderer_diagnostics.append(message)
        self._renderer_diagnostics[:] = self._renderer_diagnostics[-8:]
        self._renderer_ready = False
        self._bridge_retry_timer.stop()
        self.status_label.setText("Embedded renderer unavailable: " + message[:180])

    def _run_renderer_command(self, command_name: str) -> None:
        """Run one allowlisted read-only renderer command."""
        if command_name not in {"fitGraph", "resetCamera"}:
            return
        web_view = self._web_view
        if web_view is None:
            return
        try:
            web_view.page().runJavaScript(
                f"window.kandaProjectGraph.{command_name}();"
            )
        except (AttributeError, RuntimeError):
            self.status_label.setText("Renderer is no longer available.")

    @Slot()
    def _search_graph(self) -> None:
        """Focus the first visible node matching the current query."""
        query = self.search_edit.text().strip()
        if not query:
            return
        web_view = self._web_view
        if web_view is None:
            self.status_label.setText("Search requires the embedded renderer.")
            return
        script = (
            "window.kandaProjectGraph.focusByQuery("
            + json.dumps(query, ensure_ascii=True)
            + ");"
        )
        try:
            web_view.page().runJavaScript(script, self._on_search_result)
        except (AttributeError, RuntimeError):
            self.status_label.setText("Renderer is no longer available.")

    def _on_search_result(self, found: Any) -> None:
        """Report one bounded search result."""
        if not bool(found):
            self.status_label.setText("No visible graph node matched the search.")

    @Slot()
    def _open_in_browser(self) -> None:
        """Open a temporary self-contained preview in the default browser."""
        try:
            self._documents.open_browser(
                graph_snapshot_json(self._snapshot),
                self._generation_id,
            )
            self.status_label.setText("Opened local read-only browser preview.")
        except (OSError, RuntimeError, ValueError) as exc:
            QMessageBox.warning(
                self,
                "Browser preview unavailable",
                "The local preview could not be opened.\n\n" + str(exc),
            )

    def _show_overview_details(self) -> None:
        """Display current evidence provenance and graph limitations."""
        self.details.setHtml(overview_details_html(self._build_result))

    def _show_node_details(self, node: dict[str, Any]) -> None:
        """Render escaped current-snapshot node metadata."""
        self.details.setHtml(node_details_html(node, self._build_result))

    def closeEvent(self, event: object) -> None:
        """Invalidate late renderer events before Qt teardown."""
        self._generation_id = uuid.uuid4().hex
        self._renderer_ready = False
        self._bridge_retry_timer.stop()
        self._stop_viewport_activation()
        self._documents.close()
        super().closeEvent(event)
