# project-path: kanda_reasoner_app/reasoner_symbol_atlas/evidence_freshness.py
"""Read-only freshness checks for Project Analysis Evidence JSON."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .schemas import (
    ProjectSymbolAtlasReport,
    normalize_project_atlas_text,
)

from .evidence_freshness_helpers_private import (
    _collect_live_files,
    _classify_freshness,
    _load_snapshot,
    _modified_after_generation,
    _same_project_root,
    _select_json_path,
)

PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH = "fresh"
PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE = "probably_stale"
PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL = "json_canonical"
PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE = "stale"
PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT = "wrong_project"
PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE = "missing_evidence"
PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE = "invalid_evidence"

__all__ = [
    "PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH",
    "PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL",
    "PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE",
    "PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_PROBABLY_STALE",
    "PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE",
    "PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT",
    "ProjectSymbolAtlasEvidenceFreshnessOptions",
    "ProjectSymbolAtlasEvidenceFreshnessSummary",
    "build_reasoner_symbol_atlas_evidence_freshness_report",
    "check_reasoner_symbol_atlas_evidence_freshness",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasEvidenceFreshnessOptions:
    """Options for read-only evidence freshness checks."""

    project_root: str
    json_path: str = ""
    max_items: int = 50
    include_non_python_files: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "max_items": int(self.max_items),
            "include_non_python_files": bool(self.include_non_python_files),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasEvidenceFreshnessSummary:
    """Freshness result for generated Project Analysis Evidence."""

    project_root: str
    json_path: str = ""
    status: str = PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE
    generated_at: str = ""
    evidence_project_root: str = ""
    checked_file_count: int = 0
    evidence_file_count: int = 0
    missing_source_file_count: int = 0
    new_source_file_count: int = 0
    modified_after_generation_count: int = 0
    missing_source_files: tuple[str, ...] = field(default_factory=tuple)
    new_source_files: tuple[str, ...] = field(default_factory=tuple)
    modified_after_generation: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible summary dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "status": normalize_project_atlas_text(self.status),
            "generated_at": normalize_project_atlas_text(self.generated_at),
            "evidence_project_root": str(Path(self.evidence_project_root))
            if self.evidence_project_root else "",
            "checked_file_count": int(self.checked_file_count),
            "evidence_file_count": int(self.evidence_file_count),
            "missing_source_file_count": int(self.missing_source_file_count),
            "new_source_file_count": int(self.new_source_file_count),
            "modified_after_generation_count": int(self.modified_after_generation_count),
            "missing_source_files": list(self.missing_source_files),
            "new_source_files": list(self.new_source_files),
            "modified_after_generation": list(self.modified_after_generation),
            "notes": list(self.notes),
        }




def check_reasoner_symbol_atlas_evidence_freshness(
    options: ProjectSymbolAtlasEvidenceFreshnessOptions,
) -> ProjectSymbolAtlasEvidenceFreshnessSummary:
    """Check whether generated JSON evidence still matches live source files.

    This function never imports analyzed project modules and never edits files.
    """

    project_root = Path(options.project_root).expanduser().resolve(strict=False)
    json_path = _select_json_path(project_root, options.json_path)
    if json_path is None:
        return ProjectSymbolAtlasEvidenceFreshnessSummary(
            project_root=str(project_root),
            status=PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_MISSING_EVIDENCE,
            notes=("No complete JSON evidence file was found.",),
        )

    try:
        snapshot = _load_snapshot(project_root, json_path)
    except ValueError as exc:
        return ProjectSymbolAtlasEvidenceFreshnessSummary(
            project_root=str(project_root),
            json_path=str(json_path),
            status=PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_INVALID_EVIDENCE,
            notes=(str(exc),),
        )

    if snapshot.project_root and not _same_project_root(project_root, snapshot.project_root):
        return ProjectSymbolAtlasEvidenceFreshnessSummary(
            project_root=str(project_root),
            json_path=str(json_path),
            status=PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_WRONG_PROJECT,
            generated_at=snapshot.generated_at,
            evidence_project_root=snapshot.project_root,
            evidence_file_count=len(snapshot.evidence_files),
            notes=("Evidence project_root does not match the supplied project root.",),
        )

    live_files = _collect_live_files(
        project_root=project_root,
        include_non_python_files=options.include_non_python_files,
    )
    evidence_set = set(snapshot.evidence_files)
    live_set = set(live_files.keys())
    missing_all = tuple(sorted(evidence_set - live_set))
    new_files_all = tuple(sorted(live_set - evidence_set))
    modified_all = _modified_after_generation(
        live_files=live_files,
        evidence_files=evidence_set,
        generated_dt=snapshot.generated_dt,
        limit=None,
        project_root=project_root,
        evidence_hashes=snapshot.evidence_hashes,
    )
    max_items = max(0, int(options.max_items))
    missing = missing_all[:max_items]
    new_files = new_files_all[:max_items]
    modified = modified_all[:max_items]
    status, notes = _classify_freshness(
        generated_dt=snapshot.generated_dt,
        missing=missing_all,
        new_files=new_files_all,
        modified=modified_all,
    )

    return ProjectSymbolAtlasEvidenceFreshnessSummary(
        project_root=str(project_root),
        json_path=str(json_path),
        status=status,
        generated_at=snapshot.generated_at,
        evidence_project_root=snapshot.project_root,
        checked_file_count=len(live_files),
        evidence_file_count=len(snapshot.evidence_files),
        missing_source_file_count=len(missing_all),
        new_source_file_count=len(new_files_all),
        modified_after_generation_count=len(modified_all),
        missing_source_files=missing,
        new_source_files=new_files,
        modified_after_generation=modified,
        notes=notes,
    )


def build_reasoner_symbol_atlas_evidence_freshness_report(
    options: ProjectSymbolAtlasEvidenceFreshnessOptions,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas report for evidence freshness."""

    summary = check_reasoner_symbol_atlas_evidence_freshness(options)
    data = summary.to_dict()
    summary_line = (
        "Evidence freshness status="
        + str(data["status"])
        + "; canonical_policy=json_is_authoritative"
        + "; checked_files="
        + str(data["checked_file_count"])
        + "; evidence_files="
        + str(data["evidence_file_count"])
        + "; missing="
        + str(data["missing_source_file_count"])
        + "; post_evidence_new="
        + str(data["new_source_file_count"])
        + "; modified="
        + str(data["modified_after_generation_count"])
        + "; json_path="
        + str(data["json_path"])
    )
    return ProjectSymbolAtlasReport(
        project_root=options.project_root,
        report_type="reasoner_symbol_atlas",
        summary=summary_line,
        input_sources=("complete_json", data["json_path"], "live_source_tree"),
    )


