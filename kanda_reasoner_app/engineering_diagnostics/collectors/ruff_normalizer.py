# project-path: kanda_reasoner_app/engineering_diagnostics/collectors/ruff_normalizer.py
"""Deterministic Ruff JSON normalization for Engineering Diagnostics."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any, Mapping

from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity

from ..models import (
    DiagnosticFindingInput,
    DiagnosticRunInput,
    DiagnosticValidationError,
)
from ..rules import ruff_rule_profile
from .ruff_collector import (
    RUFF_COLLECTOR_CONTRACT_VERSION,
    RUFF_PRODUCER_ID,
    RuffCollectionResult,
)

__all__ = [
    "build_ruff_diagnostic_run",
    "ruff_configuration_fingerprint",
    "ruff_scope_fingerprint",
]

_WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True, slots=True)
class _Candidate:
    code: str
    relative_path: str
    message: str
    row: int
    column: int
    end_row: int
    end_column: int
    symbol_id: str
    structural_hash: str
    fix_available: bool
    fix_applicability: str
    fix_message: str
    fix_edit_count: int


@dataclass(frozen=True, slots=True)
class _SourceFacts:
    lines: tuple[str, ...]
    tree: ast.AST | None


def _digest(label: str, value: object) -> str:
    payload = label + "|" + json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def ruff_scope_fingerprint() -> str:
    """Return the stable selected-Project Ruff scope contract identity."""
    return _digest(
        "engineering-diagnostics-ruff-scope-v1",
        {
            "producer_id": RUFF_PRODUCER_ID,
            "scope": "selected_project_root",
            "format": "ruff_native_json",
            "fix_execution": False,
        },
    )


def ruff_configuration_fingerprint(collection: RuffCollectionResult) -> str:
    """Return configuration identity including Ruff and collector versions."""
    return _digest(
        "engineering-diagnostics-ruff-configuration-v1",
        {
            "config_relative_path": collection.config_relative_path,
            "config_sha256": collection.config_sha256,
            "ruff_version": collection.ruff_version,
            "collector_contract": RUFF_COLLECTOR_CONTRACT_VERSION,
        },
    )


def _path_key(path: str | Path) -> str:
    return os.path.normcase(str(Path(path).expanduser().resolve(strict=False)))


def _positive_int(value: object, default: int = 1) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    return number if number > 0 else default


def _location(item: Mapping[str, Any], field: str) -> Mapping[str, Any]:
    value = item.get(field)
    return value if isinstance(value, Mapping) else {}


def _relative_filename(root: Path, value: object) -> str:
    text = str(value or "").strip()
    if not text:
        raise DiagnosticValidationError("Ruff finding filename is required.")
    path = Path(text)
    candidate = path if path.is_absolute() else root / path
    resolved = candidate.expanduser().resolve(strict=False)
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise DiagnosticValidationError(
            "Ruff finding path is outside the selected Project."
        ) from exc


def _source_facts(path: Path, cache: dict[Path, _SourceFacts]) -> _SourceFacts:
    existing = cache.get(path)
    if existing is not None:
        return existing
    if not path.is_file():
        facts = _SourceFacts((), None)
        cache[path] = facts
        return facts
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree: ast.AST | None = ast.parse(text, filename=str(path))
    except SyntaxError:
        tree = None
    facts = _SourceFacts(tuple(text.splitlines()), tree)
    cache[path] = facts
    return facts


def _contains_line(node: ast.AST, line: int) -> bool:
    start = getattr(node, "lineno", None)
    end = getattr(node, "end_lineno", start)
    return isinstance(start, int) and isinstance(end, int) and start <= line <= end


def _symbol_id(tree: ast.AST | None, line: int) -> str:
    if tree is None:
        return ""
    scopes: list[tuple[int, int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not _contains_line(node, line):
            continue
        start = int(getattr(node, "lineno", line))
        end = int(getattr(node, "end_lineno", start))
        scopes.append((start, -(end - start), str(node.name)))
    scopes.sort()
    return ".".join(item[2] for item in scopes)


def _structural_context(facts: _SourceFacts, line: int) -> str:
    candidates: list[tuple[int, int, ast.AST]] = []
    if facts.tree is not None:
        for node in ast.walk(facts.tree):
            if not _contains_line(node, line):
                continue
            start = int(getattr(node, "lineno", line))
            end = int(getattr(node, "end_lineno", start))
            span = end - start
            candidates.append((span, -start, node))
    if candidates:
        node = min(candidates, key=lambda item: (item[0], item[1]))[2]
        dumped = ast.dump(node, annotate_fields=True, include_attributes=False)
        return _digest("ruff-ast-context-v1", dumped)
    source_line = ""
    if facts.lines and 1 <= line <= len(facts.lines):
        source_line = _WHITESPACE.sub("", facts.lines[line - 1])
    return _digest("ruff-line-context-v1", source_line)


def _fix_metadata(item: Mapping[str, Any]) -> tuple[bool, str, str, int]:
    fix = item.get("fix")
    if not isinstance(fix, Mapping):
        return False, "none", "", 0
    applicability = str(fix.get("applicability") or "unknown").strip().lower()
    if applicability not in {"safe", "unsafe", "display", "unknown"}:
        applicability = "unknown"
    edits = fix.get("edits")
    edit_count = len(edits) if isinstance(edits, list) else 0
    return (
        True,
        applicability,
        str(fix.get("message") or "").strip(),
        edit_count,
    )


def _candidate(
    item: Mapping[str, Any],
    root: Path,
    cache: dict[Path, _SourceFacts],
) -> _Candidate:
    code = str(item.get("code") or "").strip().upper()
    message = " ".join(str(item.get("message") or "").split())
    if not code or not message:
        raise DiagnosticValidationError("Ruff finding code and message are required.")
    relative = _relative_filename(root, item.get("filename"))
    location = _location(item, "location")
    end_location = _location(item, "end_location")
    row = _positive_int(location.get("row"))
    column = _positive_int(location.get("column"))
    end_row = _positive_int(end_location.get("row"), row)
    end_column = _positive_int(end_location.get("column"), column)
    facts = _source_facts(root / Path(relative), cache)
    available, applicability, fix_message, edit_count = _fix_metadata(item)
    return _Candidate(
        code=code,
        relative_path=relative,
        message=message,
        row=row,
        column=column,
        end_row=end_row,
        end_column=end_column,
        symbol_id=_symbol_id(facts.tree, row),
        structural_hash=_structural_context(facts, row),
        fix_available=available,
        fix_applicability=applicability,
        fix_message=fix_message,
        fix_edit_count=edit_count,
    )


def _unique_candidates(
    collection: RuffCollectionResult,
    root: Path,
) -> tuple[tuple[_Candidate, ...], int]:
    cache: dict[Path, _SourceFacts] = {}
    values: dict[tuple[object, ...], _Candidate] = {}
    for raw in collection.raw_findings:
        candidate = _candidate(raw, root, cache)
        identity = (
            candidate.code,
            candidate.relative_path,
            candidate.message,
            candidate.row,
            candidate.column,
            candidate.end_row,
            candidate.end_column,
            candidate.fix_available,
            candidate.fix_applicability,
            candidate.fix_message,
            candidate.fix_edit_count,
        )
        values[identity] = candidate
    ordered = tuple(
        sorted(
            values.values(),
            key=lambda item: (
                item.relative_path,
                item.code,
                item.symbol_id,
                item.structural_hash,
                item.message,
                item.row,
                item.column,
            ),
        )
    )
    return ordered, len(collection.raw_findings) - len(ordered)


def _finding_inputs(
    collection: RuffCollectionResult,
    root: Path,
) -> tuple[tuple[DiagnosticFindingInput, ...], int]:
    candidates, duplicate_count = _unique_candidates(collection, root)
    occurrences: dict[tuple[str, ...], int] = {}
    findings: list[DiagnosticFindingInput] = []
    for item in candidates:
        group = (
            item.relative_path,
            item.code,
            item.symbol_id,
            item.structural_hash,
            item.message,
        )
        occurrence = occurrences.get(group, 0) + 1
        occurrences[group] = occurrence
        profile = ruff_rule_profile(item.code)
        fix_note = "No Ruff fix was reported."
        if item.fix_available:
            fix_note = (
                "Ruff reported a "
                + item.fix_applicability
                + " fix candidate; no fix was executed."
            )
        findings.append(
            DiagnosticFindingInput(
                code=item.code,
                relative_path=item.relative_path,
                message=item.message,
                severity=profile.severity,
                confidence="high",
                semantic_key=item.code + "|" + item.message,
                symbol_id=item.symbol_id,
                location_key=item.structural_hash[:32] + ":" + str(occurrence),
                category="ruff_" + profile.category,
                line=item.row,
                evidence={
                    "tool": "ruff",
                    "ruff_version": collection.ruff_version,
                    "command_source": collection.command_source,
                    "start_line": item.row,
                    "start_column": item.column,
                    "end_line": item.end_row,
                    "end_column": item.end_column,
                    "structural_context_sha256": item.structural_hash,
                    "priority_default": profile.priority,
                    "priority_rationale": profile.rationale,
                    "fix_available": item.fix_available,
                    "fix_applicability": item.fix_applicability,
                    "fix_message": item.fix_message,
                    "fix_edit_count": item.fix_edit_count,
                    "fix_executed": False,
                },
                suggested_action=(
                    "Review Ruff " + item.code + " evidence. " + fix_note
                ),
            )
        )
    return tuple(findings), duplicate_count


def build_ruff_diagnostic_run(
    collection: RuffCollectionResult,
    *,
    boundary: ProjectToolBoundaryIdentity,
    attempt_id: str,
    source_fingerprint: str,
    operation_generation: int,
) -> DiagnosticRunInput:
    """Normalize completed Ruff JSON into the frozen diagnostic run contract."""
    root = Path(boundary.active_project_root).resolve(strict=True)
    if _path_key(collection.project_root) != _path_key(root):
        raise DiagnosticValidationError("Ruff collection Project root does not match.")
    findings, duplicate_count = _finding_inputs(collection, root)
    return DiagnosticRunInput(
        attempt_id=attempt_id,
        project_id=boundary.active_project_id,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        producer_id=RUFF_PRODUCER_ID,
        producer_version=collection.ruff_version,
        source_fingerprint=source_fingerprint,
        scope_fingerprint=ruff_scope_fingerprint(),
        configuration_fingerprint=ruff_configuration_fingerprint(collection),
        operation_generation=int(operation_generation),
        findings=findings,
        completion_status="COMPLETED",
        started_at_utc=collection.started_at_utc,
        completed_at_utc=collection.completed_at_utc,
        provenance={
            "collector_contract": (
                "engineering_diagnostics.ruff_native_json."
                + RUFF_COLLECTOR_CONTRACT_VERSION
            ),
            "ruff_version": collection.ruff_version,
            "command_source": collection.command_source,
            "config_relative_path": collection.config_relative_path,
            "config_sha256": collection.config_sha256,
            "stdout_sha256": collection.stdout_sha256,
            "raw_finding_count": len(collection.raw_findings),
            "normalized_finding_count": len(findings),
            "duplicate_raw_findings_dropped": duplicate_count,
            "fix_execution": False,
        },
    )
