"""Report writer helpers for Project Symbol Atlas outputs."""

from __future__ import annotations
from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import sanitize_atlas_markdown_text

import json
from pathlib import Path

from .schemas import ProjectAtlasWriteResult, ProjectSymbolAtlasReport

__all__ = [
    "default_reasoner_symbol_atlas_report_dir",
    "format_reasoner_symbol_atlas_markdown",
    "reasoner_symbol_atlas_report_stem",
    "write_reasoner_symbol_atlas_report",
]


def default_reasoner_symbol_atlas_report_dir(project_root: str | Path) -> Path:
    """Return the default output folder for Project Symbol Atlas reports."""
    return Path(project_root) / "workbench" / "reasoner_symbol_atlas_reports"


def reasoner_symbol_atlas_report_stem(report: ProjectSymbolAtlasReport) -> str:
    """Return a filesystem-safe report stem."""
    data = report.to_dict()
    created_at = str(data["created_at"])
    timestamp = created_at.replace(":", "").replace("+", "_")
    timestamp = timestamp.replace("-", "").replace("T", "_")
    return timestamp + "_" + str(data["report_type"]) + "_" + str(data["report_id"])[-12:]


def _format_lines(title: str, values: list[str]) -> list[str]:
    lines = ["## " + title, ""]
    if values:
        lines.extend("- " + value for value in values)
    else:
        lines.append("- none")
    lines.append("")
    return lines


def format_reasoner_symbol_atlas_markdown(report: ProjectSymbolAtlasReport) -> str:
    """Format a Project Symbol Atlas report as Markdown."""
    data = report.to_dict()
    lines = [
        "# Project Symbol Atlas Report",
        "",
        "Report ID: " + str(data["report_id"]),
        "Report type: " + str(data["report_type"]),
        "Created at: " + str(data["created_at"]),
        "Project root: " + str(data["project_root"]),
        "Module count: " + str(data["module_count"]),
        "Symbol count: " + str(data["symbol_count"]),
        "Query result count: " + str(data["query_result_count"]),
        "",
    ]
    summary = str(data.get("summary", "")).strip()
    if summary:
        lines.extend(["## Summary", "", summary, ""])

    input_sources = [str(item) for item in data.get("input_sources", []) if str(item)]
    if input_sources:
        lines.extend(_format_lines("Input Sources", input_sources))

    decision_lines = _decision_lines(data)
    if decision_lines:
        lines.extend(_format_lines("Decision Details", decision_lines))

    query_lines = _query_result_lines(data)
    if query_lines:
        lines.extend(_format_lines("Query Results", query_lines))

    module_lines: list[str] = []
    for module in data.get("modules", []):
        if not isinstance(module, dict):
            continue
        module_lines.append(
            str(module.get("module", ""))
            + " -> "
            + str(module.get("path", ""))
            + " ["
            + str(module.get("owner_role", "unknown"))
            + "]"
        )
    lines.extend(_format_lines("Modules", module_lines))

    symbol_lines: list[str] = []
    for symbol in data.get("symbols", []):
        if not isinstance(symbol, dict):
            continue
        path = str(symbol.get("path", ""))
        path_suffix = ""
        if path:
            path_suffix = " -> " + path
        symbol_lines.append(
            str(symbol.get("name", ""))
            + " ("
            + str(symbol.get("kind", "unknown"))
            + ") in "
            + str(symbol.get("module", ""))
            + path_suffix
        )
    lines.extend(_format_lines("Symbols", symbol_lines))

    evidence_lines = _symbol_evidence_lines(data, max_items=40)
    if evidence_lines:
        lines.extend(_format_lines("Symbol Evidence", evidence_lines))
    return sanitize_atlas_markdown_text("\n".join(lines))


def _decision_lines(data: dict[str, object]) -> list[str]:
    lines: list[str] = []
    for symbol in data.get("symbols", []):
        if not isinstance(symbol, dict):
            continue
        if str(symbol.get("name", "")) != "existing_code_finder_decision":
            continue
        for item in symbol.get("evidence", []):
            text = str(item).strip()
            if _is_decision_evidence(text):
                lines.append(text)
    return lines


def _is_decision_evidence(text: str) -> bool:
    prefixes = (
        "query_type=",
        "status=",
        "confidence=",
        "owner_path=",
        "duplicate_symbol=",
        "facade_owner_path=",
        "main_path=",
        "helper_path=",
        "related_file=",
        "test_to_run=",
        "primary_edit_target=",
        "file_not_to_touch=",
        "pre_patch_status=",
    )
    return text.startswith(prefixes)


def _query_result_lines(data: dict[str, object]) -> list[str]:
    lines: list[str] = []
    for result in data.get("query_results", []):
        if not isinstance(result, dict):
            continue
        query = result.get("query", {})
        query_name = ""
        if isinstance(query, dict):
            query_name = str(query.get("name", ""))
        lines.append(
            "query="
            + query_name
            + "; status="
            + str(result.get("status", ""))
            + "; matches="
            + str(result.get("match_count", 0))
        )
    return lines


def _symbol_evidence_lines(data: dict[str, object], max_items: int) -> list[str]:
    lines: list[str] = []
    for symbol in data.get("symbols", []):
        if not isinstance(symbol, dict):
            continue
        name = str(symbol.get("name", ""))
        for evidence in symbol.get("evidence", []):
            text = str(evidence).strip()
            if text and not _is_decision_evidence(text):
                lines.append(name + ": " + text)
            if len(lines) >= max_items:
                lines.append("truncated at " + str(max_items) + " evidence lines")
                return lines
    return lines

def write_reasoner_symbol_atlas_report(
    report: ProjectSymbolAtlasReport,
    output_dir: str | Path | None = None,
) -> ProjectAtlasWriteResult:
    """Write a Project Symbol Atlas report as JSON and Markdown."""
    target_dir = Path(output_dir) if output_dir is not None else (
        default_reasoner_symbol_atlas_report_dir(report.project_root)
    )
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = reasoner_symbol_atlas_report_stem(report)
    json_path = target_dir / (stem + ".json")
    markdown_path = target_dir / (stem + ".md")
    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
        newline="\n",
    )
    markdown_path.write_text(
        format_reasoner_symbol_atlas_markdown(report),
        encoding="utf-8",
        newline="\n",
    )
    return ProjectAtlasWriteResult(json_path=json_path, markdown_path=markdown_path)
