# project-path: kanda_reasoner_app/source_hygiene/ruff_quality.py
"""Read-only Ruff lint and format checks for Source Hygiene."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

from .ruff_quality_runtime import (
    _DEFAULT_RUFF_TIMEOUT_SECONDS,
    _RuffCommandIdentity,
    _RuffProcessResult,
    _resolve_ruff_command,
    _run_ruff_process,
)
from .ruff_quality_scope import _build_ruff_quality_scope
from .schemas import SourceHygieneFinding, SourceHygieneReport

__all__ = [
    "RUFF_QUALITY_FEATURE_ID",
    "build_ruff_quality_report",
]

RUFF_QUALITY_FEATURE_ID = "engineering-safety-source-hygiene-ruff-quality-v1"


def build_ruff_quality_report(
    project_root: str | Path,
    *,
    ruff_argv_prefix: Sequence[str] | None = None,
    timeout_seconds: float = _DEFAULT_RUFF_TIMEOUT_SECONDS,
) -> SourceHygieneReport:
    """Run read-only Ruff lint and format checks for one project root."""
    root = Path(project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        return _blocked_report(root, "PROJECT_ROOT_NOT_DIRECTORY")
    if float(timeout_seconds) <= 0:
        return _blocked_report(root, "RUFF_TIMEOUT_NOT_POSITIVE")

    try:
        identity = _resolve_ruff_command(
            ruff_argv_prefix,
            timeout_seconds=timeout_seconds,
        )
    except RuntimeError as exc:
        return _blocked_report(root, str(exc))

    scope = _build_ruff_quality_scope(root)

    lint_result = _run_ruff_process(
        (
            *identity.argv_prefix,
            *scope.global_argv,
            "check",
            "--output-format",
            "json",
            "--exit-zero",
            "--no-cache",
            "--color",
            "never",
            *scope.command_argv,
            str(root),
        ),
        cwd=root,
        timeout_seconds=timeout_seconds,
    )
    format_result = _run_ruff_process(
        (
            *identity.argv_prefix,
            *scope.global_argv,
            "format",
            "--check",
            "--no-cache",
            "--color",
            "never",
            *scope.command_argv,
            str(root),
        ),
        cwd=root,
        timeout_seconds=timeout_seconds,
    )

    findings: list[SourceHygieneFinding] = []
    findings.extend(_lint_findings(lint_result, root, identity))
    findings.extend(_format_findings(format_result, root, identity))
    findings.extend(_process_blockers(lint_result, format_result, identity))

    summary = (
        "Read-only Ruff quality check completed. "
        + "ruff_version="
        + identity.version
        + "; command_source="
        + identity.source
        + "; lint_status="
        + str(lint_result.returncode)
        + "; format_status="
        + str(format_result.returncode)
        + "; scope_exclusions="
        + str(len(scope.exclusion_patterns))
        + "; findings="
        + str(len(findings))
        + "."
    )
    return SourceHygieneReport(
        project_root=str(root),
        report_type="ruff_quality",
        summary=summary,
        findings=tuple(findings),
        input_sources=(
            "ruff_version:" + identity.version,
            "ruff_command_source:" + identity.source,
            "ruff_check_json",
            "ruff_format_check_text",
            "ruff_scope_policy:project_exclusion_policy",
            "ruff_scope_exclusion_count:" + str(len(scope.exclusion_patterns)),
            "ruff_scope_fingerprint:" + scope.fingerprint,
        ),
    )


def _lint_findings(
    result: _RuffProcessResult,
    root: Path,
    identity: _RuffCommandIdentity,
) -> list[SourceHygieneFinding]:
    """Convert Ruff lint JSON into source-hygiene findings."""
    if result.returncode != 0:
        return []
    payload = _load_json_list(result.stdout)
    findings: list[SourceHygieneFinding] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "RUFF_LINT").strip()
        message = str(item.get("message") or "Ruff lint finding.").strip()
        location = (
            item.get("location") if isinstance(item.get("location"), dict) else {}
        )
        fix = item.get("fix")
        findings.append(
            SourceHygieneFinding(
                code=code,
                path=_display_path(item.get("filename"), root),
                line=_positive_int(location.get("row")),
                message=message,
                severity="warning",
                confidence="high",
                evidence={
                    "phase": "lint",
                    "ruff_version": identity.version,
                    "fix_available": bool(fix),
                },
                suggested_action=(
                    "Review the finding before any correction. "
                    "No source file was modified by this command."
                ),
            )
        )
    return findings


def _format_findings(
    result: _RuffProcessResult,
    root: Path,
    identity: _RuffCommandIdentity,
) -> list[SourceHygieneFinding]:
    """Convert Ruff format-check output into source-hygiene findings."""
    if result.returncode == 0:
        return []
    findings: list[SourceHygieneFinding] = []
    for path_value in _format_required_paths(result.stdout):
        findings.append(
            SourceHygieneFinding(
                code="RUFF_FORMAT_REQUIRED",
                path=_display_path(path_value, root),
                message="File would be reformatted by Ruff.",
                severity="warning",
                confidence="high",
                evidence={
                    "phase": "format_check",
                    "ruff_version": identity.version,
                },
                suggested_action=(
                    "Preview formatting in a disposable copy before applying it "
                    "to active project source."
                ),
            )
        )
    if findings:
        return findings
    return [
        SourceHygieneFinding(
            code="RUFF_FORMAT_CHECK_BLOCKED",
            path=".",
            message="Ruff format check did not pass: "
            + _bounded_text(result.stderr or result.stdout),
            severity="warning",
            confidence="high",
            evidence={
                "phase": "format_check",
                "ruff_version": identity.version,
                "returncode": result.returncode,
            },
            suggested_action="Inspect Ruff output before any formatting action.",
        )
    ]


def _format_required_paths(text: str) -> list[str]:
    """Return paths from stable Ruff formatter check output."""
    prefixes = (
        "would reformat:",
        "would format:",
    )
    paths: list[str] = []
    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        lowered = line.casefold()
        for prefix in prefixes:
            if lowered.startswith(prefix):
                path_value = line[len(prefix) :].strip()
                if path_value:
                    paths.append(path_value)
                break
    return paths


def _process_blockers(
    lint_result: _RuffProcessResult,
    format_result: _RuffProcessResult,
    identity: _RuffCommandIdentity,
) -> list[SourceHygieneFinding]:
    """Return process-level failures that could invalidate Ruff evidence."""
    findings: list[SourceHygieneFinding] = []
    if lint_result.returncode != 0:
        findings.append(
            _process_finding("RUFF_LINT_EXECUTION_FAILED", lint_result, identity)
        )
    if format_result.returncode not in (0, 1):
        findings.append(
            _process_finding("RUFF_FORMAT_EXECUTION_FAILED", format_result, identity)
        )
    return findings


def _process_finding(
    code: str,
    result: _RuffProcessResult,
    identity: _RuffCommandIdentity,
) -> SourceHygieneFinding:
    """Build one process-level Ruff blocker finding."""
    detail = _bounded_text(result.stderr or result.stdout)
    if result.timed_out:
        detail = "Ruff command timed out. " + detail
    return SourceHygieneFinding(
        code=code,
        path=".",
        message=detail or "Ruff command failed without diagnostic output.",
        severity="error",
        confidence="high",
        evidence={
            "ruff_version": identity.version,
            "returncode": result.returncode,
            "timed_out": result.timed_out,
        },
        suggested_action="Resolve Ruff execution before treating the report as quality evidence.",
    )


def _blocked_report(root: Path, blocker: str) -> SourceHygieneReport:
    """Return a structured report when Ruff cannot be executed safely."""
    finding = SourceHygieneFinding(
        code="RUFF_QUALITY_BLOCKED",
        path=".",
        message=blocker,
        severity="error",
        confidence="high",
        suggested_action=(
            "Install or configure Ruff, then rerun the read-only quality check."
        ),
    )
    return SourceHygieneReport(
        project_root=str(root),
        report_type="ruff_quality",
        summary="Read-only Ruff quality check was blocked.",
        findings=(finding,),
        input_sources=("ruff_availability_probe",),
    )


def _load_json_list(text: str) -> list[Any]:
    """Return a JSON list, or an empty list for malformed or absent output."""
    try:
        payload = json.loads(text or "[]")
    except json.JSONDecodeError:
        return []
    return payload if isinstance(payload, list) else []


def _display_path(value: object, root: Path) -> str:
    """Return a project-relative path when Ruff reports one inside the root."""
    text = str(value or "").strip()
    if not text:
        return "."
    candidate = Path(text)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        return candidate.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return text


def _positive_int(value: object) -> int | None:
    """Return a positive integer or None."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def _bounded_text(value: object, limit: int = 1200) -> str:
    """Return one bounded, whitespace-normalized diagnostic string."""
    compact = " ".join(str(value or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
