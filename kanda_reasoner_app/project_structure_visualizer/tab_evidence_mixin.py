# project-path: kanda_reasoner_app/project_structure_visualizer/tab_evidence_mixin.py
"""Project evidence loading and filter behavior for Project Structure 3D."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any

from PySide6.QtCore import Slot

from .graph_schema import graph_snapshot_json
from .graph_layout_state import stabilize_project_graph_layout
from .graph_snapshot_builder import GraphSnapshotBuild, build_project_graph_snapshot
from .graph_view_filters import filter_graph_snapshot

__all__: list[str] = []


class ProjectStructureEvidenceMixin:
    """Consume canonical complete JSON without becoming a scanner owner."""

    _project_root: Path | None
    _generation_id: str
    _source_snapshot: dict[str, Any]
    _snapshot: dict[str, Any]

    def set_project_root(self, project_root: Path) -> None:
        """Load existing canonical evidence for the selected Project."""
        resolved = Path(project_root).expanduser().resolve()
        if resolved == self._project_root:
            self._refresh_complete_json_status()
            return
        self._project_root = resolved
        self.project_label.setText("Project: " + str(resolved))
        self._refresh_complete_json_status()
        self._reload_project_evidence()

    def _reload_project_evidence(self) -> None:
        """Rebuild the read-only snapshot from existing evidence only."""
        if self._project_root is None:
            return
        self.status_label.setText("Loading canonical Project evidence...")
        self._generation_id = uuid.uuid4().hex
        build_result = build_project_graph_snapshot(self._project_root)
        stabilized, cache_status = stabilize_project_graph_layout(
            build_result.snapshot,
            self._project_root,
            persist=not build_result.is_fixture,
        )
        self._layout_cache_status = cache_status
        self._build_result = GraphSnapshotBuild(
            snapshot=stabilized,
            source_status=build_result.source_status,
            source_label=build_result.source_label,
            fallback_reason=build_result.fallback_reason,
        )
        self._source_snapshot = stabilized
        self._renderer_ready = False
        self._page_load_ok = None
        self._renderer_diagnostics.clear()
        self._render_termination = None
        self._bridge_retry_timer.stop()
        self.search_edit.clear()
        self._apply_view_options(reload_page=True)

    @Slot()
    def _refresh_evidence(self) -> None:
        """Reload the current canonical evidence on explicit user request."""
        self._reload_project_evidence()

    @Slot()
    def _on_view_options_changed(self) -> None:
        """Apply read-only view filters to the current source snapshot."""
        self._apply_view_options(reload_page=False)

    def _apply_view_options(self, *, reload_page: bool) -> None:
        """Filter one immutable source snapshot and update the renderer."""
        self._view_mode = str(self.view_mode_combo.currentData() or "structure")
        self._show_imports = bool(self.imports_checkbox.isChecked())
        self._show_external = bool(self.external_checkbox.isChecked())
        self._show_symbols = bool(self.symbols_checkbox.isChecked())
        self._show_semantic = bool(self.semantic_checkbox.isChecked())
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
        self.source_badge.setText(
            "READ-ONLY FIXTURE"
            if self._build_result.is_fixture
            else "READ-ONLY LIVE EVIDENCE"
        )
        self._show_overview_details()
        if reload_page:
            self._load_current_snapshot()
        else:
            self._push_current_snapshot()

    def _push_current_snapshot(self) -> None:
        """Push a filtered snapshot through the existing renderer contract."""
        web_view = self._web_view
        if web_view is None:
            return
        script = (
            "window.kandaProjectGraph.setGraph("
            + graph_snapshot_json(self._snapshot)
            + ","
            + json.dumps(self._generation_id, ensure_ascii=True)
            + ");"
        )
        try:
            web_view.page().runJavaScript(script)
        except (AttributeError, RuntimeError):
            self.status_label.setText("Renderer is no longer available.")
