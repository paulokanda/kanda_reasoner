# project-path: kanda_reasoner_app/engineering_diagnostics/collectors/shadow_collector.py
"""Read-only public Shadow audit collector for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib
from pathlib import Path
from threading import Event
from types import MappingProxyType
from typing import Any, Callable, Mapping

from ..models import EngineeringDiagnosticsError

__all__ = [
    "SHADOW_COLLECTOR_CONTRACT_VERSION",
    "SHADOW_PRODUCER_ID",
    "ShadowCollectionCancelled",
    "ShadowCollectionError",
    "ShadowCollectionResult",
    "ShadowIssueEvidence",
    "collect_shadow_findings",
]

SHADOW_PRODUCER_ID = "source_hygiene.shadow_conflict_audit"
SHADOW_COLLECTOR_CONTRACT_VERSION = "1.0"
_SHADOW_PUBLIC_SOURCE = (
    "kanda_reasoner_app.source_hygiene.shadow_audit."
    "audit_project_for_shadow_conflicts"
)
_MAX_FINDINGS = 100000
_INVALID_COVERAGE_CODES = frozenset(
    {"SHADOW_AUDIT_READ_ERROR", "SHADOW_AUDIT_PARSE_ERROR"}
)


class ShadowCollectionError(EngineeringDiagnosticsError):
    """Raised when public Shadow evidence cannot be collected safely."""


class ShadowCollectionCancelled(ShadowCollectionError):
    """Raised when Shadow collection is cancelled."""


@dataclass(frozen=True, slots=True)
class ShadowIssueEvidence:
    """One copied public Shadow issue before diagnostic normalization."""

    code: str
    relative_path: str
    message: str
    severity: str
    confidence: str
    line: int | None
    evidence: Mapping[str, Any]
    suggested_action: str


@dataclass(frozen=True, slots=True)
class ShadowCollectionResult:
    """Completed immutable Shadow audit collection."""

    project_root: str
    collector_version: str
    audit_source: str
    audit_source_sha256: str
    started_at_utc: str
    completed_at_utc: str
    issues: tuple[ShadowIssueEvidence, ...]
    assessment: str
    coverage_valid: bool
    metadata: Mapping[str, Any]


ShadowAuditor = Callable[..., object]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _required_text(value: object, marker: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ShadowCollectionError(marker)
    return text


def _normalized_relative_path(value: object) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if text in ("", ".", "<project>"):
        return "ARCHITECTURE.md"
    path = Path(text)
    if path.is_absolute() or ".." in path.parts:
        raise ShadowCollectionError("SHADOW_ISSUE_PATH_INVALID:" + text)
    return path.as_posix()


def _mapping(value: object) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ShadowCollectionError("SHADOW_ISSUE_EVIDENCE_INVALID")
    return {str(key): item for key, item in value.items()}


def _report_dict(report: object) -> dict[str, Any]:
    if isinstance(report, Mapping):
        return dict(report)
    serializer = getattr(report, "to_dict", None)
    if not callable(serializer):
        raise ShadowCollectionError("SHADOW_PUBLIC_REPORT_CONTRACT_INVALID")
    payload = serializer()
    if not isinstance(payload, Mapping):
        raise ShadowCollectionError("SHADOW_PUBLIC_REPORT_PAYLOAD_INVALID")
    return dict(payload)


def _default_public_auditor() -> tuple[ShadowAuditor, Path]:
    module = importlib.import_module(
        "kanda_reasoner_app.source_hygiene.shadow_audit"
    )
    auditor = getattr(module, "audit_project_for_shadow_conflicts", None)
    source_path = Path(str(getattr(module, "__file__", ""))).resolve(strict=True)
    if not callable(auditor):
        raise ShadowCollectionError("SHADOW_PUBLIC_AUDIT_CONTRACT_UNAVAILABLE")
    return auditor, source_path


def _issue_from_payload(raw: object) -> ShadowIssueEvidence:
    if not isinstance(raw, Mapping):
        raise ShadowCollectionError("SHADOW_PUBLIC_FINDING_INVALID")
    evidence = _mapping(raw.get("evidence"))
    original_path = str(raw.get("path") or "").strip()
    if original_path:
        evidence.setdefault("shadow_original_path", original_path)
    line_value = raw.get("line")
    line = None if line_value in (None, "") else int(line_value)
    if line is not None and line < 1:
        raise ShadowCollectionError("SHADOW_ISSUE_LINE_INVALID")
    return ShadowIssueEvidence(
        code=_required_text(raw.get("code"), "SHADOW_ISSUE_CODE_MISSING").upper(),
        relative_path=_normalized_relative_path(raw.get("path")),
        message=_required_text(raw.get("message"), "SHADOW_ISSUE_MESSAGE_MISSING"),
        severity=_required_text(
            raw.get("severity") or "warning", "SHADOW_ISSUE_SEVERITY_MISSING"
        ).lower(),
        confidence=_required_text(
            raw.get("confidence") or "medium", "SHADOW_ISSUE_CONFIDENCE_MISSING"
        ).lower(),
        line=line,
        evidence=MappingProxyType(evidence),
        suggested_action=str(raw.get("suggested_action") or "").strip(),
    )


def collect_shadow_findings(
    project_root: str | Path,
    *,
    cancellation: Event | None = None,
    auditor: ShadowAuditor | None = None,
    audit_source_path: str | Path | None = None,
    max_files: int | None = None,
) -> ShadowCollectionResult:
    """Collect structured Shadow findings through its public audit contract."""
    root = Path(project_root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ShadowCollectionError("SHADOW_PROJECT_ROOT_NOT_DIRECTORY")
    if cancellation is not None and cancellation.is_set():
        raise ShadowCollectionCancelled("SHADOW_COLLECTION_CANCELLED")

    active_auditor = auditor
    public_source = (
        Path(audit_source_path).resolve(strict=True)
        if audit_source_path is not None
        else None
    )
    if active_auditor is None:
        active_auditor, default_source = _default_public_auditor()
        public_source = public_source or default_source
    if public_source is None or not public_source.is_file():
        raise ShadowCollectionError("SHADOW_AUDIT_SOURCE_MISSING")

    started = _utc_now()
    try:
        report = active_auditor(root, max_files=max_files)
    except ShadowCollectionError:
        raise
    except Exception as exc:
        raise ShadowCollectionError("SHADOW_PUBLIC_AUDIT_FAILED:" + str(exc)) from exc
    if cancellation is not None and cancellation.is_set():
        raise ShadowCollectionCancelled("SHADOW_COLLECTION_CANCELLED")

    payload = _report_dict(report)
    report_type = str(payload.get("report_type") or "").strip().lower()
    if report_type != "shadow_conflict_audit":
        raise ShadowCollectionError("SHADOW_PUBLIC_REPORT_TYPE_INVALID")
    report_root = Path(str(payload.get("project_root") or "")).resolve(strict=False)
    if report_root != root:
        raise ShadowCollectionError("SHADOW_PUBLIC_REPORT_PROJECT_MISMATCH")
    raw_findings = payload.get("findings")
    if not isinstance(raw_findings, list):
        raise ShadowCollectionError("SHADOW_PUBLIC_FINDINGS_INVALID")
    if len(raw_findings) > _MAX_FINDINGS:
        raise ShadowCollectionError("SHADOW_FINDING_LIMIT_EXCEEDED")

    unique: dict[tuple[object, ...], ShadowIssueEvidence] = {}
    for raw in raw_findings:
        issue = _issue_from_payload(raw)
        key = (
            issue.code,
            issue.relative_path,
            issue.line,
            str(issue.evidence.get("symbol") or ""),
            str(issue.evidence.get("exported_name") or ""),
            tuple(str(item) for item in issue.evidence.get("owners", ()) or ()),
        )
        unique[key] = issue
    issues = tuple(
        sorted(
            unique.values(),
            key=lambda item: (
                item.relative_path,
                item.code,
                item.line or 0,
                item.message,
            ),
        )
    )
    invalid_codes = sorted(
        {item.code for item in issues if item.code in _INVALID_COVERAGE_CODES}
    )
    coverage_valid = not invalid_codes
    return ShadowCollectionResult(
        project_root=str(root),
        collector_version=SHADOW_COLLECTOR_CONTRACT_VERSION,
        audit_source=_SHADOW_PUBLIC_SOURCE,
        audit_source_sha256=_sha256(public_source),
        started_at_utc=started,
        completed_at_utc=_utc_now(),
        issues=issues,
        assessment="CLEAN" if not issues else "ISSUES",
        coverage_valid=coverage_valid,
        metadata=MappingProxyType(
            {
                "collector_contract": SHADOW_COLLECTOR_CONTRACT_VERSION,
                "raw_finding_count": len(raw_findings),
                "normalized_finding_count": len(issues),
                "duplicate_count": len(raw_findings) - len(issues),
                "invalid_coverage_codes": tuple(invalid_codes),
                "max_files": None if max_files is None else int(max_files),
            }
        ),
    )
