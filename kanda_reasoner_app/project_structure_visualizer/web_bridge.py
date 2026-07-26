# project-path: kanda_reasoner_app/project_structure_visualizer/web_bridge.py
"""Narrow QWebChannel bridge for the read-only 3D visualizer."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWebChannel import QWebChannel

__all__ = ["ProjectStructure3DBridge", "ProjectStructure3DBridgeBundle"]


class ProjectStructure3DBridge(QObject):
    """Receive only renderer selection and lifecycle events."""

    node_selected = Signal(str, str)
    background_selected = Signal(str)
    renderer_ready = Signal(str)
    renderer_error = Signal(str, str)

    @Slot(str, str)
    def onNodeSelected(self, generation_id: str, node_id: str) -> None:
        """Forward one node selection without granting object access."""
        self.node_selected.emit(str(generation_id), str(node_id))

    @Slot(str)
    def onBackgroundSelected(self, generation_id: str) -> None:
        """Forward one read-only background selection."""
        self.background_selected.emit(str(generation_id))

    @Slot(str)
    def onRendererReady(self, generation_id: str) -> None:
        """Forward renderer readiness for the active generation."""
        self.renderer_ready.emit(str(generation_id))

    @Slot(str, str)
    def onRendererError(self, generation_id: str, message: str) -> None:
        """Forward a bounded renderer error message."""
        self.renderer_error.emit(str(generation_id), str(message)[:1000])


@dataclass(frozen=True)
class ProjectStructure3DBridgeBundle:
    """Keep the QWebChannel and its registered bridge together."""

    channel: QWebChannel
    bridge: ProjectStructure3DBridge
    object_name: str = "projectGraphBridge"

    def connect_to_page(self, page: object) -> None:
        """Attach the narrow channel to one QWebEngine page."""
        page.setWebChannel(self.channel)


def create_bridge_bundle(parent: QObject) -> ProjectStructure3DBridgeBundle:
    """Create one parent-owned channel and bridge bundle."""
    channel = QWebChannel(parent)
    bridge = ProjectStructure3DBridge(parent)
    channel.registerObject("projectGraphBridge", bridge)
    return ProjectStructure3DBridgeBundle(channel=channel, bridge=bridge)
