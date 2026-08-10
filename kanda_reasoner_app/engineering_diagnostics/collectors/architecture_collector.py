# project-path: kanda_reasoner_app/engineering_diagnostics/collectors/architecture_collector.py
"""Read-only public Architecture Review collector for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib
from pathlib import Path
import re
from threading import Event
from types import MappingProxyType
from typing import Any, Callable, Mapping

from ..models import EngineeringDiagnosticsError

__all__ = [
    "ARCHITECTURE_COLLECTOR_CONTRACT_VERSION",
    "ARCHITECTURE_PRODUCER_ID",
    "ArchitectureCollectionCancelled",
    "ArchitectureCollectionError",
    "ArchitectureCollectionResult",
    "ArchitectureIssueEvidence",
    "collect_architecture_findings",
]

ARCHITECTURE_PRODUCER_ID = "manage_architecture.validate"
ARCHITECTURE_COLLECTOR_CONTRACT_VERSION = "1.0"
_VALIDATION_SOURCE = (
    "kanda_reasoner_app.manage_architecture.manage_architecture.scan_project"
)
_MAX_FINDINGS = 100000
_SYMBOL_PATTERNS = (
    re.compile(r'Symbol [\'"]([^\'"]+)[\'"]'),
    re.compile(r'symbol [\'"]([^\'"]+)[\'"]', re.IGNORECASE),
    re.compile(r"symbol\(s\):\s*([^.;]+)", re.IGNORECASE),
)
_OWNER_PATTERNS = (
    re.compile(r"owned by multiple modules:\s*(\[[^\]]*\])", re.IGNORECASE),
    re.compile(r"owner(?: box| module)?[:=]\s*([^.;]+)", re.IGNORECASE),
)


class ArchitectureCollectionError(EngineeringDiagnosticsError):
    """Raised when Architecture Review evidence cannot be collected safely."""


class ArchitectureCollectionCancelled(ArchitectureCollectionError):
    """Raised when collection is cancelled before or after the public scan."""


@dataclass(frozen=True, slots=True)
class ArchitectureIssueEvidence:
    """One normalized public Architecture Review issue before persistence."""

    level: str
    code: str
    relative_path: str
    message: str
    owner: str
    boundary: str
    symbol: str
    validation_source: str


@dataclass(frozen=True, slots=True)
class ArchitectureCollectionResult:
    """Completed immutable Architecture Review collection."""

    project_root: str
    collector_version: str
    validation_source: str
    validation_source_sha256: str
    started_at_utc: str
    completed_at_utc: str
    issues: tuple[ArchitectureIssueEvidence, ...]
    canonical_issue_count: int
    assessment: str
    coverage_valid: bool
    metadata: Mapping[str, Any]


Scanner = Callable[[Path], tuple[dict[str, Any], list[Any], dict[str, Any], Any]]
BoundaryResolver = Callable[[Any], str]


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
        raise ArchitectureCollectionError(marker)
    return text


def _relative_path(value: object) -> str:
    text = str(value or "").strip().replace("\\", "/")
    if text in ("", "."):
        return "ARCHITECTURE.md"
    path = Path(text)
    if path.is_absolute() or ".." in path.parts:
        raise ArchitectureCollectionError("ARCHITECTURE_ISSUE_PATH_INVALID:" + text)
    return path.as_posix()


def _first_match(patterns: tuple[re.Pattern[str], ...], message: str) -> str:
    for pattern in patterns:
        match = pattern.search(message)
        if match:
            return " ".join(match.group(1).split())[:500]
    return ""


def _module_for_path(modules: Mapping[str, Any], relative_path: str) -> Any | None:
    normalized = relative_path.replace("\\", "/")
    for module in modules.values():
        if str(getattr(module, "path", "")).replace("\\", "/") == normalized:
            return module
    return None


def _default_public_scanner() -> tuple[Scanner, BoundaryResolver, Path]:
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    scanner = getattr(module, "scan_project", None)
    resolver = getattr(module, "architecture_box_for_module", None)
    source_path = Path(str(getattr(module, "__file__", ""))).resolve(strict=True)
    if not callable(scanner) or not callable(resolver):
        raise ArchitectureCollectionError(
            "ARCHITECTURE_PUBLIC_SCAN_CONTRACT_UNAVAILABLE"
        )
    return scanner, resolver, source_path


def collect_architecture_findings(
    project_root: str | Path,
    *,
    cancellation: Event | None = None,
    scanner: Scanner | None = None,
    boundary_resolver: BoundaryResolver | None = None,
    validation_source_path: str | Path | None = None,
) -> ArchitectureCollectionResult:
    """Collect Architecture Review findings through its public facade only."""
    root = Path(project_root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ArchitectureCollectionError("ARCHITECTURE_PROJECT_ROOT_NOT_DIRECTORY")
    if cancellation is not None and cancellation.is_set():
        raise ArchitectureCollectionCancelled("ARCHITECTURE_COLLECTION_CANCELLED")
    public_source = Path(validation_source_path).resolve(strict=True) if validation_source_path else None
    active_scanner = scanner
    active_boundary_resolver = boundary_resolver
    if active_scanner is None or active_boundary_resolver is None:
        default_scanner, default_resolver, default_source = _default_public_scanner()
        active_scanner = active_scanner or default_scanner
        active_boundary_resolver = active_boundary_resolver or default_resolver
        public_source = public_source or default_source
    if public_source is None or not public_source.is_file():
        raise ArchitectureCollectionError("ARCHITECTURE_VALIDATION_SOURCE_MISSING")
    started = _utc_now()
    try:
        modules, raw_issues, metadata, _sources = active_scanner(root)
    except ArchitectureCollectionError:
        raise
    except Exception as exc:
        raise ArchitectureCollectionError(
            "ARCHITECTURE_PUBLIC_SCAN_FAILED:" + str(exc)
        ) from exc
    if cancellation is not None and cancellation.is_set():
        raise ArchitectureCollectionCancelled("ARCHITECTURE_COLLECTION_CANCELLED")
    if not isinstance(modules, dict) or not isinstance(raw_issues, list):
        raise ArchitectureCollectionError("ARCHITECTURE_PUBLIC_SCAN_SHAPE_INVALID")
    if len(raw_issues) > _MAX_FINDINGS:
        raise ArchitectureCollectionError("ARCHITECTURE_FINDING_LIMIT_EXCEEDED")
    found: list[ArchitectureIssueEvidence] = []
    seen: set[tuple[str, str, str, str, str, str]] = set()
    canonical_issue_count = 0
    for raw in raw_issues:
        level = _required_text(getattr(raw, "level", ""), "ARCHITECTURE_LEVEL_MISSING").lower()
        code = _required_text(getattr(raw, "code", ""), "ARCHITECTURE_CODE_MISSING").upper()
        original_path = _relative_path(getattr(raw, "path", ""))
        message = _required_text(
            getattr(raw, "message", ""), "ARCHITECTURE_MESSAGE_MISSING"
        )
        module = _module_for_path(modules, original_path)
        boundary = "project"
        owner = ""
        if module is not None:
            boundary = str(active_boundary_resolver(module) or "project").strip()
            owner = str(getattr(module, "module_id", "") or "").strip()
        owner = _first_match(_OWNER_PATTERNS, message) or owner or boundary
        symbol = _first_match(_SYMBOL_PATTERNS, message)
        key = (level, code, original_path, owner, boundary, symbol)
        if key in seen:
            continue
        seen.add(key)
        if level == "error":
            canonical_issue_count += 1
        found.append(
            ArchitectureIssueEvidence(
                level=level,
                code=code,
                relative_path=original_path,
                message=message,
                owner=owner,
                boundary=boundary or "project",
                symbol=symbol,
                validation_source=_VALIDATION_SOURCE,
            )
        )
    assessment = "CLEAN" if canonical_issue_count == 0 else "ISSUES"
    evidence_metadata = {
        "collector_contract": ARCHITECTURE_COLLECTOR_CONTRACT_VERSION,
        "module_count": len(modules),
        "raw_issue_count": len(raw_issues),
        "normalized_issue_count": len(found),
        "canonical_issue_count": canonical_issue_count,
        "assessment": assessment,
        "coverage_valid": True,
        "public_metadata_keys": tuple(sorted(str(key) for key in metadata.keys()))
        if isinstance(metadata, dict)
        else (),
    }
    return ArchitectureCollectionResult(
        project_root=str(root),
        collector_version=ARCHITECTURE_COLLECTOR_CONTRACT_VERSION,
        validation_source=_VALIDATION_SOURCE,
        validation_source_sha256=_sha256(public_source),
        started_at_utc=started,
        completed_at_utc=_utc_now(),
        issues=tuple(found),
        canonical_issue_count=canonical_issue_count,
        assessment=assessment,
        coverage_valid=True,
        metadata=MappingProxyType(evidence_metadata),
    )
