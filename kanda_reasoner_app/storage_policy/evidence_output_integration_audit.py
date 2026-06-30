# project-path: kanda_reasoner_app/storage_policy/evidence_output_integration_audit.py
"""Report-only audit for evidence output integration references.

This module helps prepare the output-path integration step after evidence has
been relocated out of the source tree. It scans source files for references that
may still recreate old in-source evidence output folders or write generated
architecture evidence into the app source tree.

Import is side-effect free: no scan, folder creation, move, delete, or write is
performed unless a caller explicitly invokes a scan or write function.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.path_resolver import normalize_path

EVIDENCE_OUTPUT_INTEGRATION_AUDIT_ACTION = "report_only"
EVIDENCE_OUTPUT_INTEGRATION_AUDIT_SCHEMA_VERSION = 1
EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE = "writer_candidate"
EVIDENCE_OUTPUT_RISK_REFERENCE_ONLY = "reference_only"
EVIDENCE_OUTPUT_RISK_TEST_REFERENCE = "test_reference"
EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE = "policy_reference"
EVIDENCE_OUTPUT_STATUS_CLEAN = "clean"
EVIDENCE_OUTPUT_STATUS_REVIEW_REQUIRED = "review_required"
EVIDENCE_OUTPUT_STATUS_WRITERS_FOUND = "writers_found"

_OLD_EVIDENCE_TOKEN = "project_analysis" + "_evidence"
_ARCHITECTURE_AUDIT_TOKEN = "architecture_audit"
_JSON_COMPLETE_TOKEN = "json_complete"

_TEXT_SUFFIXES = (
    ".py",
    ".pyw",
    ".ps1",
    ".bat",
    ".cmd",
    ".txt",
    ".md",
    ".json",
    ".toml",
    ".yaml",
    ".yml",
)
_EXCLUDED_DIR_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
    }
)
_WRITER_HINTS = (
    "write",
    "writetext",
    "write_text",
    "open(",
    "mkdir",
    "makedirs",
    "copy",
    "copy2",
    "copyfile",
    "destination",
    "output",
    "json_complete",
)


@dataclass(frozen=True)
class EvidenceOutputReference:
    """One source reference related to evidence output path integration."""

    relative_path: str
    line_number: int
    matched_token: str
    risk: str
    line_preview: str
    recommendation: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "line_number": self.line_number,
            "matched_token": self.matched_token,
            "risk": self.risk,
            "line_preview": self.line_preview,
            "recommendation": self.recommendation,
        }


@dataclass(frozen=True)
class EvidenceOutputIntegrationAuditReport:
    """Report-only result for evidence output integration references."""

    source_root: str
    action: str = EVIDENCE_OUTPUT_INTEGRATION_AUDIT_ACTION
    schema_version: int = EVIDENCE_OUTPUT_INTEGRATION_AUDIT_SCHEMA_VERSION
    references: tuple[EvidenceOutputReference, ...] = field(default_factory=tuple)

    @property
    def total_references(self) -> int:
        """Return the total number of references."""
        return len(self.references)

    @property
    def writer_candidates(self) -> int:
        """Return the number of writer-candidate references."""
        return sum(
            1
            for item in self.references
            if item.risk == EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE
        )

    @property
    def test_references(self) -> int:
        """Return the number of test references."""
        return sum(
            1
            for item in self.references
            if item.risk == EVIDENCE_OUTPUT_RISK_TEST_REFERENCE
        )

    @property
    def policy_references(self) -> int:
        """Return the number of storage-policy references."""
        return sum(
            1
            for item in self.references
            if item.risk == EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE
        )

    @property
    def reference_only_items(self) -> int:
        """Return the number of reference-only items."""
        return sum(
            1
            for item in self.references
            if item.risk == EVIDENCE_OUTPUT_RISK_REFERENCE_ONLY
        )

    def status(self) -> str:
        """Return the audit status."""
        if self.writer_candidates:
            return EVIDENCE_OUTPUT_STATUS_WRITERS_FOUND
        if self.total_references:
            return EVIDENCE_OUTPUT_STATUS_REVIEW_REQUIRED
        return EVIDENCE_OUTPUT_STATUS_CLEAN

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "action": self.action,
            "schema_version": self.schema_version,
            "status": self.status(),
            "source_root": self.source_root,
            "total_references": self.total_references,
            "writer_candidates": self.writer_candidates,
            "test_references": self.test_references,
            "policy_references": self.policy_references,
            "reference_only_items": self.reference_only_items,
            "references": [item.to_dict() for item in self.references],
        }


__all__ = [
    "EVIDENCE_OUTPUT_INTEGRATION_AUDIT_ACTION",
    "EVIDENCE_OUTPUT_INTEGRATION_AUDIT_SCHEMA_VERSION",
    "EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE",
    "EVIDENCE_OUTPUT_RISK_REFERENCE_ONLY",
    "EVIDENCE_OUTPUT_RISK_TEST_REFERENCE",
    "EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE",
    "EVIDENCE_OUTPUT_STATUS_CLEAN",
    "EVIDENCE_OUTPUT_STATUS_REVIEW_REQUIRED",
    "EVIDENCE_OUTPUT_STATUS_WRITERS_FOUND",
    "EvidenceOutputIntegrationAuditReport",
    "EvidenceOutputReference",
    "render_evidence_output_integration_audit_json",
    "render_evidence_output_integration_audit_text",
    "scan_evidence_output_integration_references",
    "write_evidence_output_integration_audit_json",
    "write_evidence_output_integration_audit_text",
]


def _iter_text_files(source_root: Path) -> list[Path]:
    """Return candidate text files below source_root."""
    files: list[Path] = []
    for path in source_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in _EXCLUDED_DIR_NAMES for part in path.parts):
            continue
        if path.suffix.lower() not in _TEXT_SUFFIXES:
            continue
        files.append(path)
    return sorted(files)


def _relative_path(source_root: Path, path: Path) -> str:
    """Return a stable slash-separated relative path."""
    return path.relative_to(source_root).as_posix()


def _classify_reference(relative_path: str, line_text: str) -> str:
    """Classify one evidence output reference."""
    lowered_path = relative_path.lower()
    lowered_line = line_text.lower()
    if lowered_path.startswith("tests/") or "/tests/" in lowered_path:
        return EVIDENCE_OUTPUT_RISK_TEST_REFERENCE
    if "/storage_policy/" in lowered_path or lowered_path.startswith(
        "kanda_reasoner_app/storage_policy/"
    ):
        return EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE
    if any(hint in lowered_line for hint in _WRITER_HINTS):
        return EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE
    return EVIDENCE_OUTPUT_RISK_REFERENCE_ONLY


def _recommendation_for_risk(risk: str) -> str:
    """Return a remediation recommendation for a reference risk."""
    if risk == EVIDENCE_OUTPUT_RISK_WRITER_CANDIDATE:
        return "replace writer path with architecture audit resolver"
    if risk == EVIDENCE_OUTPUT_RISK_TEST_REFERENCE:
        return "update tests after output integration patch"
    if risk == EVIDENCE_OUTPUT_RISK_POLICY_REFERENCE:
        return "allowed policy reference; review for public API accuracy"
    return "review reference and keep only if it is documentation or migration logic"


def _matched_token(line_text: str) -> str:
    """Return the matched output-related token for one line."""
    if _OLD_EVIDENCE_TOKEN in line_text:
        return _OLD_EVIDENCE_TOKEN
    if _ARCHITECTURE_AUDIT_TOKEN in line_text:
        return _ARCHITECTURE_AUDIT_TOKEN
    return _JSON_COMPLETE_TOKEN


def _preview(line_text: str, limit: int = 160) -> str:
    """Return a safe compact one-line preview."""
    clean = " ".join(line_text.strip().split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."


def scan_evidence_output_integration_references(
    source_root: str | Path,
) -> EvidenceOutputIntegrationAuditReport:
    """Scan source files for evidence output path integration references."""
    root = normalize_path(source_root)
    if not root.exists():
        raise FileNotFoundError(f"Source root not found: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Source root is not a directory: {root}")

    references: list[EvidenceOutputReference] = []
    tokens = (_OLD_EVIDENCE_TOKEN, _ARCHITECTURE_AUDIT_TOKEN, _JSON_COMPLETE_TOKEN)
    for path in _iter_text_files(root):
        relative = _relative_path(root, path)
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for index, line in enumerate(lines, start=1):
            if not any(token in line for token in tokens):
                continue
            risk = _classify_reference(relative, line)
            references.append(
                EvidenceOutputReference(
                    relative_path=relative,
                    line_number=index,
                    matched_token=_matched_token(line),
                    risk=risk,
                    line_preview=_preview(line),
                    recommendation=_recommendation_for_risk(risk),
                )
            )

    return EvidenceOutputIntegrationAuditReport(
        source_root=str(root),
        references=tuple(references),
    )


def render_evidence_output_integration_audit_json(
    report: EvidenceOutputIntegrationAuditReport,
) -> str:
    """Render a stable JSON audit report."""
    return json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n"


def render_evidence_output_integration_audit_text(
    report: EvidenceOutputIntegrationAuditReport,
) -> str:
    """Render a human-readable audit report."""
    lines = [
        "Kanda Reasoner evidence output integration audit",
        f"Action: {report.action}",
        f"Status: {report.status()}",
        f"Source root: {report.source_root}",
        f"References: {report.total_references}",
        f"Writer candidates: {report.writer_candidates}",
        f"Test references: {report.test_references}",
        f"Policy references: {report.policy_references}",
        f"Reference-only items: {report.reference_only_items}",
    ]
    if report.references:
        lines.append("Items:")
        for item in report.references:
            lines.append(
                f"  - {item.relative_path}:{item.line_number} "
                f"[{item.risk}] {item.matched_token}"
            )
    return "\n".join(lines)


def _write_text(output_path: str | Path, content: str, overwrite: bool) -> None:
    """Write text only when explicitly requested."""
    target = normalize_path(output_path)
    if not target.parent.exists():
        raise ValueError(f"Output parent does not exist: {target.parent}")
    if target.exists() and not overwrite:
        raise FileExistsError(f"Output file already exists: {target}")
    target.write_text(content, encoding="utf-8")


def write_evidence_output_integration_audit_json(
    report: EvidenceOutputIntegrationAuditReport,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> None:
    """Write the JSON audit report to an explicit output path."""
    _write_text(output_path, render_evidence_output_integration_audit_json(report), overwrite)


def write_evidence_output_integration_audit_text(
    report: EvidenceOutputIntegrationAuditReport,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> None:
    """Write the text audit report to an explicit output path."""
    _write_text(output_path, render_evidence_output_integration_audit_text(report), overwrite)
