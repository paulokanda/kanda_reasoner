# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_discovery.py
"""Candidate discovery and disposable-shadow execution for Ruff corrections."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

from .ruff_correction_errors import RuffCorrectionPreviewError
from .ruff_correction_storage import copy_file, ensure_project_relative_file
from .ruff_quality_runtime import _run_ruff_process

__all__: list[str] = []

_ALLOWED_SUFFIXES = frozenset({".py", ".pyi", ".pyw"})


def _resolve_scope_targets(
    root: Path,
    scope_paths: Sequence[str | Path] | None,
) -> tuple[tuple[Path, ...], tuple[str, ...]]:
    """Resolve project-owned files or directories selected for one preview."""
    if not scope_paths:
        return (root,), (".",)
    targets: list[Path] = []
    display: list[str] = []
    seen: set[str] = set()
    for value in scope_paths:
        candidate = Path(value)
        if not candidate.is_absolute():
            candidate = root / candidate
        resolved = candidate.expanduser().resolve()
        try:
            relative = resolved.relative_to(root)
        except ValueError as exc:
            raise RuffCorrectionPreviewError(
                "RUFF_CORRECTION_SCOPE_OUTSIDE_PROJECT_ROOT"
            ) from exc
        if not resolved.exists():
            raise RuffCorrectionPreviewError(
                "RUFF_CORRECTION_SCOPE_MISSING:" + relative.as_posix()
            )
        marker = str(resolved).casefold()
        if marker in seen:
            continue
        seen.add(marker)
        targets.append(resolved)
        display.append(relative.as_posix() or ".")
    return tuple(targets), tuple(display)


def _safe_lint_candidate_counts(text: str, root: Path) -> dict[str, int]:
    """Return per-file counts for Ruff findings with safe fixes."""
    try:
        payload = json.loads(text or "[]")
    except json.JSONDecodeError as exc:
        raise RuffCorrectionPreviewError("RUFF_CORRECTION_LINT_JSON_INVALID") from exc
    if not isinstance(payload, list):
        raise RuffCorrectionPreviewError("RUFF_CORRECTION_LINT_JSON_LIST_REQUIRED")
    counts: dict[str, int] = {}
    for item in payload:
        if not isinstance(item, dict):
            continue
        fix = item.get("fix")
        if not isinstance(fix, dict):
            continue
        if str(fix.get("applicability") or "").casefold() != "safe":
            continue
        relative = _relative_python_path(root, item.get("filename"))
        counts[relative] = counts.get(relative, 0) + 1
    return counts


def _format_candidate_paths(text: str, root: Path) -> set[str]:
    """Return project-relative paths from stable Ruff format-check output."""
    prefixes = ("would reformat:", "would format:")
    output: set[str] = set()
    for raw_line in str(text or "").splitlines():
        line = raw_line.strip()
        lowered = line.casefold()
        for prefix in prefixes:
            if lowered.startswith(prefix):
                value = line[len(prefix) :].strip()
                if value:
                    output.add(_relative_python_path(root, value))
                break
    return output


def _relative_python_path(root: Path, value: object) -> str:
    """Return a validated active-project Python path."""
    path, relative = ensure_project_relative_file(root, str(value or ""))
    if path.suffix.casefold() not in _ALLOWED_SUFFIXES:
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_NON_PYTHON_CANDIDATE:" + relative
        )
    return relative


def _load_source_payloads(
    root: Path,
    relatives: Iterable[str],
) -> dict[str, bytes]:
    """Read candidate source bytes and require strict UTF-8 text."""
    payloads: dict[str, bytes] = {}
    for relative in relatives:
        source = root / relative
        data = source.read_bytes()
        _decode_utf8(data, relative, "source")
        payloads[relative] = data
    return payloads


def _copy_candidates_to_shadow(
    root: Path,
    shadow_root: Path,
    relatives: Iterable[str],
) -> tuple[Path, ...]:
    """Copy candidate files into a disposable shadow tree."""
    output: list[Path] = []
    for relative in relatives:
        target = shadow_root / relative
        copy_file(root / relative, target)
        output.append(target)
    return tuple(output)


def _apply_safe_corrections_to_shadow(
    argv_prefix: Sequence[str],
    shadow_root: Path,
    shadow_files: Sequence[Path],
    timeout_seconds: float,
) -> None:
    """Apply safe lint fixes and formatting to shadow files only."""
    config_path = shadow_root / "ruff.toml"
    lint = _run_ruff_process(
        (
            *argv_prefix,
            "check",
            "--fix",
            "--no-unsafe-fixes",
            "--exit-zero",
            "--no-cache",
            "--no-preview",
            "--color",
            "never",
            "--config",
            str(config_path),
            *(str(path) for path in shadow_files),
        ),
        cwd=shadow_root,
        timeout_seconds=timeout_seconds,
    )
    if lint.returncode != 0:
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_SHADOW_LINT_FIX_FAILED:"
            + _bounded_text(lint.stderr or lint.stdout)
        )
    formatting = _run_ruff_process(
        (
            *argv_prefix,
            "format",
            "--no-cache",
            "--no-preview",
            "--color",
            "never",
            "--config",
            str(config_path),
            *(str(path) for path in shadow_files),
        ),
        cwd=shadow_root,
        timeout_seconds=timeout_seconds,
    )
    if formatting.returncode != 0:
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_SHADOW_FORMAT_FAILED:"
            + _bounded_text(formatting.stderr or formatting.stdout)
        )
    for file_path in shadow_files:
        _compile_python_text(file_path.read_bytes(), file_path.as_posix())


def _require_policy_version(actual: str, required: str) -> None:
    """Require the exact Ruff version pinned by the canonical policy."""
    expected = str(required or "").strip()
    if expected.startswith("=="):
        expected = expected[2:].strip()
    actual_version = str(actual or "").strip().split()[-1]
    if not expected or actual_version != expected:
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_RUFF_VERSION_MISMATCH:" + actual_version + ":" + expected
        )


def _decode_utf8(data: bytes, relative: str, phase: str) -> str:
    """Decode Python source strictly as UTF-8."""
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_NON_UTF8_" + phase.upper() + ":" + relative
        ) from exc


def _compile_python_text(data: bytes, display_path: str) -> None:
    """Compile Python text in memory without creating project cache files."""
    text = _decode_utf8(data, display_path, "preview")
    try:
        compile(text, display_path, "exec")
    except SyntaxError as exc:
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_PREVIEW_SYNTAX_FAILED:" + display_path + ":" + str(exc)
        ) from exc


def _bounded_text(value: object, limit: int = 1200) -> str:
    """Return one bounded single-line diagnostic string."""
    compact = " ".join(str(value or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
