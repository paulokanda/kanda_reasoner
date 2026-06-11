"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help
# PURPOSE       : Retrieve packaging and documentation evidence sections from static index metadata.
# EXPORTS       : retrieve_packaging_metadata, retrieve_documentation_intent
# DEPENDS ON    : query_text.py, query_intents.py
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_intents import detect_query_intents
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import norm_text
from kanda_reasoner_app.reasoner_engine.v10_models import EvidenceItem

__all__ = ["retrieve_packaging_metadata", "retrieve_documentation_intent"]


def retrieve_packaging_metadata(project_index, question: str) -> list[EvidenceItem]:
    q = norm_text(question)
    intents = detect_query_intents(q)

    if not intents["packaging_metadata"]:
        return []

    packaging = project_index.packaging_metadata
    if not isinstance(packaging, dict) or not packaging:
        return []

    lines: list[str] = []

    project_name = str(packaging.get("project_name", "")).strip()
    declared_version = str(packaging.get("declared_version", "")).strip()
    build_backend = str(packaging.get("build_backend", "")).strip()

    if project_name:
        lines.append("project_name: " + project_name)
    if declared_version:
        lines.append("declared_version: " + declared_version)
    if build_backend:
        lines.append("build_backend: " + build_backend)

    package_manager_signals = packaging.get("package_manager_signals", [])
    if isinstance(package_manager_signals, list) and package_manager_signals:
        lines.append(
            "package_manager_signals: "
            + ", ".join(str(x).strip() for x in package_manager_signals[:20] if str(x).strip())
        )

    declared_dependencies = packaging.get("declared_dependencies", [])
    if isinstance(declared_dependencies, list) and declared_dependencies:
        lines.append(
            "declared_dependencies: "
            + ", ".join(str(x).strip() for x in declared_dependencies[:30] if str(x).strip())
        )

    declared_optional_dependencies = packaging.get("declared_optional_dependencies", {})
    if isinstance(declared_optional_dependencies, dict) and declared_optional_dependencies:
        optional_parts: list[str] = []
        for group_name, values in list(declared_optional_dependencies.items())[:12]:
            cleaned_values = []
            if isinstance(values, list):
                cleaned_values = [
                    str(value).strip()
                    for value in values[:12]
                    if str(value).strip()
                ]
            if cleaned_values:
                optional_parts.append(
                    str(group_name).strip() + ": " + ", ".join(cleaned_values)
                )
        if optional_parts:
            lines.append(
                "declared_optional_dependencies: " + " | ".join(optional_parts)
            )

    declared_entrypoints = packaging.get("declared_entrypoints", [])
    if isinstance(declared_entrypoints, list) and declared_entrypoints:
        entry_parts: list[str] = []

        for item in declared_entrypoints[:12]:
            if not isinstance(item, dict):
                continue
            group = str(item.get("group", "")).strip()
            name = str(item.get("name", "")).strip()
            target = str(item.get("target", "")).strip()
            if name or target:
                entry_parts.append(f"{group}:{name}->{target}".strip(":"))
        if entry_parts:
            lines.append("declared_entrypoints: " + " | ".join(entry_parts))

    declared_tooling = packaging.get("declared_tooling", {})
    if isinstance(declared_tooling, dict) and declared_tooling:
        lines.append(
            "declared_tooling: " + ", ".join(sorted(str(k).strip() for k in declared_tooling.keys())[:20])
        )

    packaging_files_found = packaging.get("packaging_files_found", [])
    detail_lines: list[str] = []
    if isinstance(packaging_files_found, list) and packaging_files_found:
        detail_lines.append(
            "Packaging files: "
            + " | ".join(str(x).strip() for x in packaging_files_found[:12] if str(x).strip())
        )

    packaging_evidence = packaging.get("packaging_evidence", [])
    if isinstance(packaging_evidence, list) and packaging_evidence:
        preview_parts: list[str] = []
        for item in packaging_evidence[:8]:
            if not isinstance(item, dict):
                continue
            source_file = str(item.get("source_file", "")).strip()
            field_name = str(item.get("field", "")).strip()
            value_excerpt = str(item.get("value_excerpt", "")).strip()
            if source_file or field_name or value_excerpt:
                preview_parts.append(f"{source_file} | {field_name} | {value_excerpt}")
        if preview_parts:
            detail_lines.append("Evidence: " + " || ".join(preview_parts))

    if not lines and not detail_lines:
        return []

    return [
        EvidenceItem(
            evidence_id="",
            score=950,
            path="packaging_metadata",
            module_name="packaging_metadata",
            reason="packaging-metadata-section",
            detail="\n".join(lines + detail_lines),
        )
    ]


def retrieve_documentation_intent(project_index, question: str) -> list[EvidenceItem]:
    q = norm_text(question)
    intents = detect_query_intents(q)

    if not intents["documentation_intent"]:
        return []

    docs = project_index.documentation_intent
    if not isinstance(docs, dict) or not docs:
        return []

    lines: list[str] = []

    project_purpose_summary = str(docs.get("project_purpose_summary", "")).strip()
    if project_purpose_summary:
        lines.append("project_purpose_summary: " + project_purpose_summary)

    for key in (
        "declared_workflows",
        "architecture_terms",
        "run_instructions",
        "named_features",
        "external_integrations",
    ):
        values = docs.get(key, [])
        if isinstance(values, list) and values:
            cleaned = [str(x).strip() for x in values[:20] if str(x).strip()]
            if cleaned:
                lines.append(f"{key}: " + " | ".join(cleaned))

    detail_lines: list[str] = []

    documentation_files_found = docs.get("documentation_files_found", [])
    if isinstance(documentation_files_found, list) and documentation_files_found:
        detail_lines.append(
            "Documentation files: "
            + " | ".join(str(x).strip() for x in documentation_files_found[:12] if str(x).strip())
        )

    documentation_evidence = docs.get("documentation_evidence", [])
    if isinstance(documentation_evidence, list) and documentation_evidence:
        preview_parts: list[str] = []
        for item in documentation_evidence[:8]:
            if not isinstance(item, dict):
                continue
            source_file = str(item.get("source_file", "")).strip()
            field_name = str(item.get("field", "")).strip()
            value_excerpt = str(item.get("value_excerpt", "")).strip()
            if source_file or field_name or value_excerpt:
                preview_parts.append(f"{source_file} | {field_name} | {value_excerpt}")
        if preview_parts:
            detail_lines.append("Evidence: " + " || ".join(preview_parts))

    if not lines and not detail_lines:
        return []

    return [
        EvidenceItem(
            evidence_id="",
            score=950,
            path="documentation_intent",
            module_name="documentation_intent",
            reason="documentation-intent-section",
            detail="\n".join(lines + detail_lines),
        )
    ]






