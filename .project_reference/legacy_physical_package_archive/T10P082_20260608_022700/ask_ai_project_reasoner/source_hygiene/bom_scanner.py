"""Dry-run scanner for UTF-8 BOM and text decoding hygiene."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .schemas import SourceHygieneFinding, SourceHygieneReport

UTF8_BOM_BYTES = b"\xef\xbb\xbf"

DEFAULT_BOM_SCAN_SUFFIXES = frozenset(
    {
        ".bat",
        ".cfg",
        ".cmd",
        ".css",
        ".csv",
        ".html",
        ".ini",
        ".js",
        ".json",
        ".jsonl",
        ".md",
        ".ps1",
        ".py",
        ".pyi",
        ".pyw",
        ".rst",
        ".toml",
        ".ts",
        ".txt",
        ".xml",
        ".yaml",
        ".yml",
    }
)

DEFAULT_SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)

__all__ = [
    "DEFAULT_BOM_SCAN_SUFFIXES",
    "DEFAULT_SKIP_DIR_NAMES",
    "UTF8_BOM_BYTES",
    "iter_bom_scan_files",
    "scan_file_for_bom",
    "scan_project_for_bom",
]


def iter_bom_scan_files(
    project_root: str | Path,
    suffixes: Iterable[str] | None = None,
) -> list[Path]:
    """Return candidate text files for a dry-run BOM scan."""
    root = Path(project_root).resolve()
    allowed_suffixes = _normalize_suffixes(suffixes)
    if not root.exists() or not root.is_dir():
        return []

    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if _is_in_skipped_dir(path, root):
            continue
        if path.suffix.lower() not in allowed_suffixes:
            continue
        files.append(path)
    return sorted(files, key=lambda item: str(item).lower())


def scan_file_for_bom(
    path: str | Path,
    project_root: str | Path | None = None,
    check_utf8: bool = True,
) -> tuple[SourceHygieneFinding, ...]:
    """Return dry-run BOM and UTF-8 findings for one file."""
    file_path = Path(path)
    root = Path(project_root).resolve() if project_root is not None else None
    display_path = _display_path(file_path, root)

    try:
        payload = file_path.read_bytes()
    except OSError as exc:
        return (
            SourceHygieneFinding(
                code="FILE_READ_ERROR",
                path=display_path,
                message="Could not read file during BOM scan: " + str(exc),
                severity="error",
                confidence="high",
                suggested_action="Inspect file permissions or path validity.",
            ),
        )

    findings: list[SourceHygieneFinding] = []
    if payload.startswith(UTF8_BOM_BYTES):
        findings.append(
            SourceHygieneFinding(
                code="UTF8_BOM_DETECTED",
                path=display_path,
                message="File starts with a UTF-8 byte order mark.",
                severity="warning",
                confidence="high",
                evidence={"bom_hex": UTF8_BOM_BYTES.hex(), "byte_count": len(payload)},
                suggested_action="Remove the UTF-8 BOM with backup and validation.",
            )
        )

    if check_utf8:
        try:
            payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            findings.append(
                SourceHygieneFinding(
                    code="UTF8_DECODE_ERROR",
                    path=display_path,
                    message="File could not be decoded as UTF-8: " + str(exc),
                    severity="warning",
                    confidence="high",
                    evidence={"encoding": "utf-8", "byte_count": len(payload)},
                    suggested_action="Review encoding before any automatic rewrite.",
                )
            )
    return tuple(findings)


def scan_project_for_bom(
    project_root: str | Path,
    suffixes: Iterable[str] | None = None,
    max_files: int | None = None,
) -> SourceHygieneReport:
    """Build a dry-run source hygiene report for BOM and UTF-8 issues."""
    root = Path(project_root).resolve()
    files = iter_bom_scan_files(root, suffixes=suffixes)
    if max_files is not None:
        files = files[:max(0, int(max_files))]

    findings: list[SourceHygieneFinding] = []
    for file_path in files:
        findings.extend(scan_file_for_bom(file_path, project_root=root))

    summary = (
        "BOM dry-run scan completed. "
        + "files_scanned="
        + str(len(files))
        + "; findings="
        + str(len(findings))
        + "."
    )
    return SourceHygieneReport(
        project_root=str(root),
        report_type="bom_scan",
        summary=summary,
        findings=tuple(findings),
        input_sources=("project_root",),
    )


def _normalize_suffixes(suffixes: Iterable[str] | None) -> set[str]:
    if suffixes is None:
        return set(DEFAULT_BOM_SCAN_SUFFIXES)
    normalized: set[str] = set()
    for suffix in suffixes:
        value = str(suffix).strip().lower()
        if not value:
            continue
        if not value.startswith("."):
            value = "." + value
        normalized.add(value)
    return normalized


def _is_in_skipped_dir(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts[:-1]
    except ValueError:
        parts = path.parts[:-1]
    return any(part in DEFAULT_SKIP_DIR_NAMES for part in parts)


def _display_path(path: Path, root: Path | None) -> str:
    if root is None:
        return str(path)
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)
