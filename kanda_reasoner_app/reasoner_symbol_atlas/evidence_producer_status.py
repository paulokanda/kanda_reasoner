# project-path: kanda_reasoner_app/reasoner_symbol_atlas/evidence_producer_status.py
"""Status reporting for Project Analysis Evidence producers.

This module verifies the active evidence path contract used by the project
structure collector and JSON splitter. It does not collect source structure,
split JSON, migrate files, or modify project source.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_symbol_atlas.reference_folder_policy import (
    is_reasoner_symbol_atlas_reference_path,
)
from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
    analysis_json_parts_dir,
    parts_index_file_path,
    parts_manifest_file_path,
    primary_evidence_json_path,
    project_analysis_evidence_root,
    relative_parts_index_file_path,
    relative_parts_manifest_file_path,
    relative_primary_evidence_json_path,
    relative_route_manifest_file_path,
    relative_secondary_evidence_json_path,
    route_manifest_file_path,
    secondary_evidence_json_path,
)

PROJECT_ANALYSIS_EVIDENCE_STATUS_OK = "ok"
PROJECT_ANALYSIS_EVIDENCE_STATUS_WARN = "warn"
PROJECT_ANALYSIS_EVIDENCE_STATUS_FAIL = "fail"


@dataclass(frozen=True)
class ProjectAnalysisEvidenceProducerStatus:
    """Read-only status for complete and split evidence producer paths."""

    project_root: str
    status: str
    canonical_evidence_root: str
    json_complete_dir: str
    json_splitted_dir: str
    primary_complete_json: str
    runtime_trace_json: str
    split_manifest_json: str
    split_index_json: str
    route_manifest_json: str
    canonical_paths_ok: bool
    tab4_outputs_canonical: bool
    tab5_outputs_canonical: bool
    tab5_window_helpers_detected: bool
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable status dictionary."""

        return {
            "project_root": self.project_root,
            "status": self.status,
            "canonical_evidence_root": self.canonical_evidence_root,
            "json_complete_dir": self.json_complete_dir,
            "json_splitted_dir": self.json_splitted_dir,
            "primary_complete_json": self.primary_complete_json,
            "runtime_trace_json": self.runtime_trace_json,
            "split_manifest_json": self.split_manifest_json,
            "split_index_json": self.split_index_json,
            "route_manifest_json": self.route_manifest_json,
            "canonical_paths_ok": self.canonical_paths_ok,
            "tab4_outputs_canonical": self.tab4_outputs_canonical,
            "tab5_outputs_canonical": self.tab5_outputs_canonical,
            "tab5_window_helpers_detected": self.tab5_window_helpers_detected,
            "notes": list(self.notes),
        }


def _normalize_root(project_root: str | Path) -> Path:
    """Support normalize root behavior.
    
    Parameters
    ----------
    project_root : str | Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    if project_root is None:
        raise ValueError("project_root is required")
    root_text = str(project_root).strip()
    if not root_text:
        raise ValueError("project_root must not be empty")
    return Path(root_text).expanduser().resolve(strict=False)


def _is_canonical_project_evidence_path(path: Path, project_root: Path) -> bool:
    """Support is canonical project evidence path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    text = str(path).replace("\\", "/")
    root_text = str(project_root).replace("\\", "/").rstrip("/")
    return (
        text.startswith(root_text + "/project_analysis_evidence/")
        or text == root_text + "/project_analysis_evidence"
    ) and not is_reasoner_symbol_atlas_reference_path(text)


def _relative_paths_are_canonical() -> bool:
    """Support relative paths are canonical behavior.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    expected_prefix = "project_analysis_evidence/"
    relative_paths = (
        relative_primary_evidence_json_path("project"),
        relative_secondary_evidence_json_path("project"),
        relative_parts_manifest_file_path("project"),
        relative_parts_index_file_path("project"),
        relative_route_manifest_file_path("project"),
    )
    return all(
        path.startswith(expected_prefix)
        and not is_reasoner_symbol_atlas_reference_path(path)
        for path in relative_paths
    )


def _current_product_package_root(project_root: Path) -> Path:
    """Return the product package root that owns this module."""
    module_path = Path(__file__).resolve()
    try:
        relative_module = module_path.relative_to(project_root.resolve())
    except ValueError:
        return project_root / "kanda_reasoner_app"
    if not relative_module.parts:
        return project_root / "kanda_reasoner_app"
    return project_root / relative_module.parts[0]


def _tab5_window_helpers_detected(project_root: Path) -> bool:
    """Support tab5 window helpers detected behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    source_path = (
        _current_product_package_root(project_root)
        / "reasoner_tools_gui_shell"
        / "main_window_help"
        / "window_output_paths.py"
    )
    if not source_path.is_file():
        return False
    source = source_path.read_text(encoding="utf-8", errors="replace")
    required_tokens = (
        "analysis_json_parts_dir",
        "parts_manifest_file_path",
        "parts_index_file_path",
    )
    return all(token in source for token in required_tokens)


def collect_project_analysis_evidence_producer_status(
    project_root: str | Path,
) -> ProjectAnalysisEvidenceProducerStatus:
    """Collect a read-only status report for evidence producer path outputs."""

    root = _normalize_root(project_root)
    canonical_root = project_analysis_evidence_root(root)
    complete_dir = analysis_json_complete_dir(root)
    parts_dir = analysis_json_parts_dir(root)
    primary_json = primary_evidence_json_path(root)
    trace_json = secondary_evidence_json_path(root)
    manifest_json = parts_manifest_file_path(root)
    index_json = parts_index_file_path(root)
    route_json = route_manifest_file_path(root)

    tab4_paths = (complete_dir, primary_json, trace_json)
    tab5_paths = (parts_dir, manifest_json, index_json, route_json)
    all_paths = (canonical_root,) + tab4_paths + tab5_paths

    canonical_paths_ok = all(
        _is_canonical_project_evidence_path(path, root)
        for path in all_paths
    ) and _relative_paths_are_canonical()
    tab4_outputs_canonical = all(
        _is_canonical_project_evidence_path(path, root)
        for path in tab4_paths
    )
    tab5_outputs_canonical = all(
        _is_canonical_project_evidence_path(path, root)
        for path in tab5_paths
    )
    tab5_helpers = _tab5_window_helpers_detected(root)

    notes: list[str] = []
    if canonical_paths_ok:
        notes.append("Canonical project_analysis_evidence path contract is active.")
    else:
        notes.append("One or more evidence paths are not canonical.")
    if tab4_outputs_canonical:
        notes.append("Tab 4 complete JSON output helpers resolve to canonical paths.")
    if tab5_outputs_canonical:
        notes.append("Tab 5 split JSON output helpers resolve to canonical paths.")
    if tab5_helpers:
        notes.append("Tab 5 window output owner references canonical split helpers.")
    else:
        notes.append("Tab 5 window output helper evidence was not detected.")

    if canonical_paths_ok and tab4_outputs_canonical and tab5_outputs_canonical:
        status = PROJECT_ANALYSIS_EVIDENCE_STATUS_OK
    elif tab4_outputs_canonical or tab5_outputs_canonical:
        status = PROJECT_ANALYSIS_EVIDENCE_STATUS_WARN
    else:
        status = PROJECT_ANALYSIS_EVIDENCE_STATUS_FAIL

    return ProjectAnalysisEvidenceProducerStatus(
        project_root=str(root),
        status=status,
        canonical_evidence_root=str(canonical_root),
        json_complete_dir=str(complete_dir),
        json_splitted_dir=str(parts_dir),
        primary_complete_json=str(primary_json),
        runtime_trace_json=str(trace_json),
        split_manifest_json=str(manifest_json),
        split_index_json=str(index_json),
        route_manifest_json=str(route_json),
        canonical_paths_ok=canonical_paths_ok,
        tab4_outputs_canonical=tab4_outputs_canonical,
        tab5_outputs_canonical=tab5_outputs_canonical,
        tab5_window_helpers_detected=tab5_helpers,
        notes=tuple(notes),
    )


def format_project_analysis_evidence_producer_status_markdown(
    status: ProjectAnalysisEvidenceProducerStatus,
) -> str:
    """Return a Markdown status report."""

    lines = [
        "# Project Analysis Evidence Producer Status",
        "",
        f"Project root: {status.project_root}",
        f"Status: {status.status}",
        "",
        "## Canonical paths",
        f"Evidence root: {status.canonical_evidence_root}",
        f"Complete JSON dir: {status.json_complete_dir}",
        f"Split JSON dir: {status.json_splitted_dir}",
        "",
        "## Tab 4 complete JSON",
        f"Primary complete JSON: {status.primary_complete_json}",
        f"Runtime trace JSON: {status.runtime_trace_json}",
        f"Tab 4 outputs canonical: {status.tab4_outputs_canonical}",
        "",
        "## Tab 5 split JSON",
        f"Split manifest JSON: {status.split_manifest_json}",
        f"Split index JSON: {status.split_index_json}",
        f"Route manifest JSON: {status.route_manifest_json}",
        f"Tab 5 outputs canonical: {status.tab5_outputs_canonical}",
        f"Tab 5 helper evidence detected: {status.tab5_window_helpers_detected}",
        "",
        "## Notes",
    ]
    for note in status.notes:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def write_project_analysis_evidence_producer_status_report(
    project_root: str | Path,
    output_dir: str | Path | None = None,
) -> tuple[Path, Path]:
    """Write JSON and Markdown evidence producer status reports."""

    root = _normalize_root(project_root)
    if output_dir is None:
        report_dir = root / "workbench" / "_bundle_temp"
    else:
        report_dir = Path(output_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    status = collect_project_analysis_evidence_producer_status(root)
    json_path = report_dir / "PA007E_project_analysis_evidence_status.json"
    markdown_path = report_dir / "PA007E_project_analysis_evidence_status.md"
    json_path.write_text(
        json.dumps(status.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    markdown_path.write_text(
        format_project_analysis_evidence_producer_status_markdown(status),
        encoding="utf-8",
    )
    return json_path, markdown_path


__all__ = [
    "PROJECT_ANALYSIS_EVIDENCE_STATUS_FAIL",
    "PROJECT_ANALYSIS_EVIDENCE_STATUS_OK",
    "PROJECT_ANALYSIS_EVIDENCE_STATUS_WARN",
    "ProjectAnalysisEvidenceProducerStatus",
    "collect_project_analysis_evidence_producer_status",
    "format_project_analysis_evidence_producer_status_markdown",
    "write_project_analysis_evidence_producer_status_report",
]
