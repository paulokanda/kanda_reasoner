# project-path: kanda_reasoner_app/storage_policy/evidence_output_writer_shortlist.py
"""Report-only shortlist for evidence output writer candidates.

This module narrows the broad evidence output integration audit into a smaller
manual review list. It does not change output paths, create folders, move files,
or write reports unless a caller explicitly invokes a write function.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.evidence_output_integration_audit import (
    EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE,
    EvidenceOutputIntegrationAuditReport,
    EvidenceOutputReference,
    scan_evidence_output_integration_references,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path

EVIDENCE_OUTPUT_WRITER_SHORTLIST_ACTION = "report_only"
EVIDENCE_OUTPUT_WRITER_SHORTLIST_SCHEMA_VERSION = 1
EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CLEAN = "clean"
EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CANDIDATES_FOUND = "candidates_found"
EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_LIKELY_WRITER = "likely_writer"
EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_NEEDS_REVIEW = "needs_review"

_RUNTIME_SUFFIXES = (".py", ".pyw")
_EXCLUDED_PREFIXES = (
    "tests/",
    "workbench/",
    "patch_metadata/",
    "docs/",
)
_EXCLUDED_PARTS = (
    "/tests/",
    "/__pycache__/",
    "/storage_policy/",
    "/bundle_manifest/",
)
_WRITER_LINE_HINTS = (
    "write_text",
    "write_bytes",
    ".write(",
    "json.dump",
    "open(",
    "mkdir",
    "makedirs",
    "copyfile",
    "copy2",
    "shutil.copy",
)
_PATH_HINTS = (
    "collector",
    "context",
    "bundle",
    "complete",
    "evidence",
    "snapshot",
    "manifest",
    "export",
    "json",
)


@dataclass(frozen=True)
class EvidenceOutputWriterShortlistItem:
    """One aggregated writer-candidate file for manual review."""

    relative_path: str
    reference_count: int
    score: int
    risk: str
    first_line_number: int
    first_line_preview: str
    recommendation: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "reference_count": self.reference_count,
            "score": self.score,
            "risk": self.risk,
            "first_line_number": self.first_line_number,
            "first_line_preview": self.first_line_preview,
            "recommendation": self.recommendation,
        }


@dataclass(frozen=True)
class EvidenceOutputWriterShortlistReport:
    """Report-only shortlist of likely evidence output writer files."""

    source_root: str
    action: str = EVIDENCE_OUTPUT_WRITER_SHORTLIST_ACTION
    schema_version: int = EVIDENCE_OUTPUT_WRITER_SHORTLIST_SCHEMA_VERSION
    source_reference_count: int = 0
    source_writer_candidate_count: int = 0
    items: tuple[EvidenceOutputWriterShortlistItem, ...] = field(default_factory=tuple)

    @property
    def total_items(self) -> int:
        """Return the number of shortlisted files."""
        return len(self.items)

    @property
    def likely_writer_items(self) -> int:
        """Return the number of likely writer files."""
        return sum(
            1
            for item in self.items
            if item.risk == EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_LIKELY_WRITER
        )

    @property
    def review_items(self) -> int:
        """Return the number of review-only files."""
        return sum(
            1
            for item in self.items
            if item.risk == EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_NEEDS_REVIEW
        )

    def status(self) -> str:
        """Return the shortlist status."""
        if self.items:
            return EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CANDIDATES_FOUND
        return EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CLEAN

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "action": self.action,
            "schema_version": self.schema_version,
            "status": self.status(),
            "source_root": self.source_root,
            "source_reference_count": self.source_reference_count,
            "source_writer_candidate_count": self.source_writer_candidate_count,
            "total_items": self.total_items,
            "likely_writer_items": self.likely_writer_items,
            "review_items": self.review_items,
            "items": [item.to_dict() for item in self.items],
        }


__all__ = [
    "EVIDENCE_OUTPUT_WRITER_SHORTLIST_ACTION",
    "EVIDENCE_OUTPUT_WRITER_SHORTLIST_SCHEMA_VERSION",
    "EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CLEAN",
    "EVIDENCE_OUTPUT_WRITER_SHORTLIST_STATUS_CANDIDATES_FOUND",
    "EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_LIKELY_WRITER",
    "EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_NEEDS_REVIEW",
    "EvidenceOutputWriterShortlistItem",
    "EvidenceOutputWriterShortlistReport",
    "build_evidence_output_writer_shortlist",
    "build_evidence_output_writer_shortlist_from_audit",
    "render_evidence_output_writer_shortlist_json",
    "render_evidence_output_writer_shortlist_text",
    "write_evidence_output_writer_shortlist_json",
    "write_evidence_output_writer_shortlist_text",
]


def _is_runtime_candidate(relative_path: str) -> bool:
    """Return True if relative_path can be a runtime writer file."""
    lowered = relative_path.lower().replace("\\", "/")
    if not lowered.endswith(_RUNTIME_SUFFIXES):
        return False
    if any(lowered.startswith(prefix) for prefix in _EXCLUDED_PREFIXES):
        return False
    if any(part in lowered for part in _EXCLUDED_PARTS):
        return False
    return True


def _score_reference(reference: EvidenceOutputReference) -> int:
    """Score one reference for writer likelihood."""
    score = 1
    line = reference.line_preview.lower()
    path = reference.relative_path.lower()
    if reference.matched_token == "project_analysis" + "_evidence":
        score += 10
    if reference.matched_token == "json_complete":
        score += 5
    if reference.matched_token == "architecture_audit":
        score += 2
    score += sum(3 for hint in _WRITER_LINE_HINTS if hint in line)
    score += sum(2 for hint in _PATH_HINTS if hint in path)
    return score


def _recommendation(item_score: int, risk: str) -> str:
    """Return the manual review recommendation."""
    if risk == EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_LIKELY_WRITER:
        return "inspect this file first and route output through architecture audit resolver"
    if item_score >= 8:
        return "inspect as possible writer before changing generation behavior"
    return "review only after likely writer files are handled"


def build_evidence_output_writer_shortlist_from_audit(
    audit_report: EvidenceOutputIntegrationAuditReport,
    *,
    max_items: int = 50,
) -> EvidenceOutputWriterShortlistReport:
    """Build a reduced writer-candidate shortlist from an audit report."""
    if max_items < 1:
        raise ValueError("max_items must be greater than zero")

    grouped: dict[str, list[EvidenceOutputReference]] = {}
    writer_candidates = 0
    for reference in audit_report.references:
        if reference.risk != EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE:
            continue
        writer_candidates += 1
        if not _is_runtime_candidate(reference.relative_path):
            continue
        grouped.setdefault(reference.relative_path, []).append(reference)

    items: list[EvidenceOutputWriterShortlistItem] = []
    for relative_path, references in grouped.items():
        score = sum(_score_reference(reference) for reference in references)
        first = sorted(references, key=lambda item: item.line_number)[0]
        risk = EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_NEEDS_REVIEW
        if score >= 12 or len(references) >= 3:
            risk = EVIDENCE_OUTPUT_WRITER_SHORTLIST_RISK_LIKELY_WRITER
        items.append(
            EvidenceOutputWriterShortlistItem(
                relative_path=relative_path,
                reference_count=len(references),
                score=score,
                risk=risk,
                first_line_number=first.line_number,
                first_line_preview=first.line_preview,
                recommendation=_recommendation(score, risk),
            )
        )

    items.sort(key=lambda item: (-item.score, -item.reference_count, item.relative_path))
    return EvidenceOutputWriterShortlistReport(
        source_root=audit_report.source_root,
        source_reference_count=audit_report.total_references,
        source_writer_candidate_count=writer_candidates,
        items=tuple(items[:max_items]),
    )


def build_evidence_output_writer_shortlist(
    source_root: str | Path,
    *,
    max_items: int = 50,
) -> EvidenceOutputWriterShortlistReport:
    """Scan source_root and build a reduced writer-candidate shortlist."""
    audit_report = scan_evidence_output_integration_references(source_root)
    return build_evidence_output_writer_shortlist_from_audit(
        audit_report,
        max_items=max_items,
    )


def render_evidence_output_writer_shortlist_json(
    report: EvidenceOutputWriterShortlistReport,
) -> str:
    """Render a stable JSON shortlist report."""
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"


def render_evidence_output_writer_shortlist_text(
    report: EvidenceOutputWriterShortlistReport,
) -> str:
    """Render a human-readable shortlist report."""
    lines = [
        "Kanda Reasoner evidence output writer shortlist",
        f"Action: {report.action}",
        f"Status: {report.status()}",
        f"Source root: {report.source_root}",
        f"Source references: {report.source_reference_count}",
        f"Source writer candidates: {report.source_writer_candidate_count}",
        f"Shortlisted files: {report.total_items}",
        f"Likely writers: {report.likely_writer_items}",
        f"Review-only files: {report.review_items}",
    ]
    if report.items:
        lines.append("Items:")
        for item in report.items:
            lines.append(
                f"  - {item.relative_path}:{item.first_line_number} "
                f"[{item.risk}] score={item.score} refs={item.reference_count}"
            )
    return "\n".join(lines)


def _write_text(output_path: str | Path, content: str, overwrite: bool) -> None:
    """Write content only to an explicit path."""
    target = normalize_path(output_path)
    if not target.parent.exists():
        raise ValueError(f"Output parent does not exist: {target.parent}")
    if target.exists() and not overwrite:
        raise FileExistsError(f"Output file already exists: {target}")
    target.write_text(content, encoding="utf-8")


def write_evidence_output_writer_shortlist_json(
    report: EvidenceOutputWriterShortlistReport,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> None:
    """Write the JSON shortlist to an explicit output path."""
    _write_text(output_path, render_evidence_output_writer_shortlist_json(report), overwrite)


def write_evidence_output_writer_shortlist_text(
    report: EvidenceOutputWriterShortlistReport,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> None:
    """Write the text shortlist to an explicit output path."""
    _write_text(output_path, render_evidence_output_writer_shortlist_text(report), overwrite)
