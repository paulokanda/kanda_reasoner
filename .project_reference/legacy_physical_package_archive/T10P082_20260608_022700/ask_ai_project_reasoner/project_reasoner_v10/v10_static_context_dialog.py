"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QFrame, QLabel, QVBoxLayout, QWidget

from .index_loader import JsonProjectIndex
from .v10_static_context_inspector_widget import StaticContextInspectorWidget


class StaticContextDialog(QDialog):
    def __init__(
        self,
        index: JsonProjectIndex | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Static Context Inspector")
        self.resize(900, 700)

        self._detected_profile_label = QLabel("Detected profile: unknown")
        self._active_profile_label = QLabel("Active profile: unknown")
        self._static_context_status_label = QLabel("Static context: unknown")
        self._inspector = StaticContextInspectorWidget(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self._detected_profile_label)
        layout.addWidget(self._active_profile_label)
        layout.addWidget(self._static_context_status_label)

        divider = QFrame(self)
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)

        layout.addWidget(self._inspector)

        if index is not None:
            self.set_context(index)

    def set_context(
        self,
        index: JsonProjectIndex,
        detected_profile_name: str = "",
        active_profile_name: str = "",
    ) -> None:
        packaging_metadata = index.packaging_metadata
        documentation_intent = index.documentation_intent

        has_packaging = bool(packaging_metadata)
        has_documentation = bool(documentation_intent)

        if has_packaging and has_documentation:
            status_text = "Static context: available"
        elif has_packaging or has_documentation:
            status_text = "Static context: partial"
        else:
            status_text = "Static context: missing"

        self._detected_profile_label.setText(
            "Detected profile: " + (detected_profile_name or "unknown")
        )
        self._active_profile_label.setText(
            "Active profile: " + (active_profile_name or "unknown")
        )
        self._static_context_status_label.setText(status_text)

        self._inspector.set_static_context(
            packaging_metadata=packaging_metadata,
            documentation_intent=documentation_intent,
        )

    def set_index(self, index: JsonProjectIndex) -> None:
        self.set_context(index)






