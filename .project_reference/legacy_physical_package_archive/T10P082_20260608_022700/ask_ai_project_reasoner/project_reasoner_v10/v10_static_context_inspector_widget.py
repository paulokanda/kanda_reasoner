"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

import json
from typing import Any

from PySide6.QtWidgets import (
    QPlainTextEdit,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
from .v10_static_context_evidence_formatter import (
    build_static_context_evidence_preview,
)
def _pretty_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def _join_preview(items: list[Any], limit: int = 5) -> str:
    cleaned = [str(item).strip() for item in items if str(item).strip()]
    if not cleaned:
        return "-"
    preview = cleaned[:limit]
    suffix = ""
    if len(cleaned) > limit:
        suffix = f" ... (+{len(cleaned) - limit} more)"
    return ", ".join(preview) + suffix


def _build_static_context_summary(
    packaging_metadata: dict[str, Any],
    documentation_intent: dict[str, Any],
) -> str:
    packaging_files = packaging_metadata.get("packaging_files_found", [])
    dependencies = packaging_metadata.get("declared_dependencies", [])
    entrypoints = packaging_metadata.get("declared_entrypoints", [])
    tooling = packaging_metadata.get("declared_tooling", {})

    doc_files = documentation_intent.get("documentation_files_found", [])
    workflows = documentation_intent.get("declared_workflows", [])
    run_instructions = documentation_intent.get("run_instructions", [])
    integrations = documentation_intent.get("external_integrations", [])

    entrypoint_preview: list[str] = []
    for item in entrypoints[:5]:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        target = str(item.get("target", "")).strip()
        if name or target:
            entrypoint_preview.append(f"{name} -> {target}".strip())

    tooling_names = sorted(
        str(key).strip() for key in tooling.keys() if str(key).strip()
    )

    lines = [
        "STATIC CONTEXT SUMMARY",
        "=" * 80,
        "",
        "[PACKAGING METADATA]",
        f"project_name: {str(packaging_metadata.get('project_name', '')).strip() or '-'}",
        f"declared_version: {str(packaging_metadata.get('declared_version', '')).strip() or '-'}",
        f"build_backend: {str(packaging_metadata.get('build_backend', '')).strip() or '-'}",
        f"packaging_files_found: {len(packaging_files)}",
        f"packaging_file_preview: {_join_preview(packaging_files, limit=8)}",
        f"declared_dependencies: {len(dependencies)}",
        f"dependency_preview: {_join_preview(dependencies, limit=8)}",
        f"declared_entrypoints: {len(entrypoints)}",
        f"entrypoint_preview: {_join_preview(entrypoint_preview, limit=5)}",
        f"declared_tooling: {len(tooling_names)}",
        f"tooling_preview: {_join_preview(tooling_names, limit=8)}",
        "",
        "[DOCUMENTATION INTENT]",
        (
            "project_purpose_summary: "
            f"{str(documentation_intent.get('project_purpose_summary', '')).strip() or '-'}"
        ),
        f"documentation_files_found: {len(doc_files)}",
        f"documentation_file_preview: {_join_preview(doc_files, limit=8)}",
        f"declared_workflows: {len(workflows)}",
        f"workflow_preview: {_join_preview(workflows, limit=8)}",
        f"run_instructions: {len(run_instructions)}",
        f"run_instruction_preview: {_join_preview(run_instructions, limit=5)}",
        f"external_integrations: {len(integrations)}",
        f"integration_preview: {_join_preview(integrations, limit=8)}",
    ]

    return "\n".join(lines)


class StaticContextInspectorWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._tabs = QTabWidget(self)

        self._summary_view = QPlainTextEdit(self)
        self._summary_view.setReadOnly(True)
        self._summary_view.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self._packaging_view = QPlainTextEdit(self)
        self._packaging_view.setReadOnly(True)
        self._evidence_view = QPlainTextEdit(self)
        self._evidence_view.setReadOnly(True)
        self._evidence_view.setLineWrapMode(QPlainTextEdit.WidgetWidth)

        self._documentation_view = QPlainTextEdit(self)
        self._documentation_view.setReadOnly(True)

        self._tabs.addTab(self._summary_view, "Summary")
        self._tabs.addTab(self._evidence_view, "Evidence")
        self._tabs.addTab(self._packaging_view, "Packaging Metadata")
        self._tabs.addTab(self._documentation_view, "Documentation Intent")

        layout = QVBoxLayout(self)
        layout.addWidget(self._tabs)
        self.setLayout(layout)

    def set_static_context(
        self,
        packaging_metadata: dict[str, Any] | None,
        documentation_intent: dict[str, Any] | None,
    ) -> None:
        packaging_payload = packaging_metadata or {}
        documentation_payload = documentation_intent or {}

        self._summary_view.setPlainText(
            _build_static_context_summary(
                packaging_metadata=packaging_payload,
                documentation_intent=documentation_payload,
            )
        )
        self._evidence_view.setPlainText(
            build_static_context_evidence_preview(
                packaging_metadata=packaging_payload,
                documentation_intent=documentation_payload,
            )
        )
        self._packaging_view.setPlainText(_pretty_json(packaging_payload))
        self._documentation_view.setPlainText(_pretty_json(documentation_payload))





