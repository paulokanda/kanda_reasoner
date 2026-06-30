# project-path: kanda_reasoner_app/live_source_verification/verifier.py
"""Verify and read live source files under PROJECT_ROOT.

This module is an isolated Project Reasoner box.

It exists so local AI can eventually use live source files as final
implementation truth without changing the canonical complete JSON or the
local-AI working JSON.

This first gate only provides safe path verification, file metadata, hashes,
and bounded snippet extraction.
"""

from __future__ import annotations

__all__ = [
    "LiveSourcePathResult",
    "LiveSourceSnippetResult",
    "batch_verify_sources",
    "extract_live_source_snippet",
    "read_live_source_text",
    "verify_live_source_path",
]

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_MAX_TEXT_FILE_SIZE_BYTES = 2 * 1024 * 1024
DEFAULT_CONTEXT_LINES = 20


@dataclass(frozen=True)
class LiveSourcePathResult:
    """Verification result for one candidate live source path."""

    requested_path: str
    project_root: str
    resolved_path: str
    relative_path: str
    status: str
    exists: bool
    is_file: bool
    size_bytes: int
    mtime_ns: int
    sha256: str
    message: str


@dataclass(frozen=True)
class LiveSourceSnippetResult:
    """Bounded live source snippet extracted from a verified file."""

    path_result: LiveSourcePathResult
    status: str
    line_start: int
    line_end: int
    anchor: str
    text: str
    message: str


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for path, or an empty string if unavailable."""
    if not path.exists() or not path.is_file():
        return ""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_resolve(project_root: str | Path, candidate_path: str | Path) -> tuple[Path, Path, bool]:
    """Resolve a candidate path and report whether it remains under root."""
    root = Path(project_root).resolve()
    candidate = Path(candidate_path)

    if not candidate.is_absolute():
        candidate = root / candidate

    resolved = candidate.resolve()

    try:
        resolved.relative_to(root)
        inside_root = True
    except ValueError:
        inside_root = False

    return root, resolved, inside_root


def _relative_path(root: Path, resolved: Path) -> str:
    """Return a project-relative path string when possible."""
    try:
        return str(resolved.relative_to(root))
    except ValueError:
        return ""


def verify_live_source_path(
    project_root: str | Path,
    candidate_path: str | Path,
    *,
    max_file_size_bytes: int = DEFAULT_MAX_TEXT_FILE_SIZE_BYTES,
) -> LiveSourcePathResult:
    """Verify one candidate live source file under project_root.

    The function never writes files. It only validates containment, existence,
    file type, size, mtime, and SHA-256.
    """
    root, resolved, inside_root = _safe_resolve(project_root, candidate_path)
    requested = str(candidate_path)

    if not inside_root:
        return LiveSourcePathResult(
            requested_path=requested,
            project_root=str(root),
            resolved_path=str(resolved),
            relative_path="",
            status="outside_project_root",
            exists=resolved.exists(),
            is_file=resolved.is_file(),
            size_bytes=0,
            mtime_ns=0,
            sha256="",
            message="Candidate path is outside PROJECT_ROOT.",
        )

    exists = resolved.exists()
    is_file = resolved.is_file()
    relative = _relative_path(root, resolved)

    if not exists:
        return LiveSourcePathResult(
            requested_path=requested,
            project_root=str(root),
            resolved_path=str(resolved),
            relative_path=relative,
            status="missing",
            exists=False,
            is_file=False,
            size_bytes=0,
            mtime_ns=0,
            sha256="",
            message="File does not exist.",
        )

    if not is_file:
        return LiveSourcePathResult(
            requested_path=requested,
            project_root=str(root),
            resolved_path=str(resolved),
            relative_path=relative,
            status="not_file",
            exists=True,
            is_file=False,
            size_bytes=0,
            mtime_ns=0,
            sha256="",
            message="Path exists but is not a file.",
        )

    stat = resolved.stat()
    size = int(stat.st_size)
    if size > max_file_size_bytes:
        return LiveSourcePathResult(
            requested_path=requested,
            project_root=str(root),
            resolved_path=str(resolved),
            relative_path=relative,
            status="too_large",
            exists=True,
            is_file=True,
            size_bytes=size,
            mtime_ns=int(stat.st_mtime_ns),
            sha256="",
            message="File exceeds max_file_size_bytes.",
        )

    return LiveSourcePathResult(
        requested_path=requested,
        project_root=str(root),
        resolved_path=str(resolved),
        relative_path=relative,
        status="ok",
        exists=True,
        is_file=True,
        size_bytes=size,
        mtime_ns=int(stat.st_mtime_ns),
        sha256=_sha256_file(resolved),
        message="File verified under PROJECT_ROOT.",
    )


def read_live_source_text(
    project_root: str | Path,
    candidate_path: str | Path,
    *,
    max_file_size_bytes: int = DEFAULT_MAX_TEXT_FILE_SIZE_BYTES,
    encoding: str = "utf-8",
) -> tuple[LiveSourcePathResult, str]:
    """Verify and read one live source file as text."""
    path_result = verify_live_source_path(
        project_root,
        candidate_path,
        max_file_size_bytes=max_file_size_bytes,
    )

    if path_result.status != "ok":
        return path_result, ""

    resolved = Path(path_result.resolved_path)
    text = resolved.read_text(encoding=encoding, errors="replace")
    return path_result, text


def _find_anchor_line(lines: list[str], anchor: str) -> int:
    """Find the best 1-based line for an anchor, or zero if absent.

    Definition lines are preferred over incidental mentions such as __all__,
    imports, comments, or prose. This improves live-source precision for
    questions about classes and functions such as PromptBuilder.
    """
    if not anchor:
        return 0

    lowered_anchor = anchor.lower()
    clean_anchor = anchor.split(".")[-1].strip()
    lowered_clean_anchor = clean_anchor.lower()

    definition_prefixes = (
        "class ",
        "def ",
        "async def ",
    )

    # First pass: prefer exact class/function definitions.
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        lowered = stripped.lower()
        for prefix in definition_prefixes:
            if lowered.startswith(prefix + lowered_clean_anchor.lower() + "("):
                return index
            if lowered.startswith(prefix + lowered_clean_anchor.lower() + ":"):
                return index

    # Second pass: prefer any definition-like line that contains the anchor.
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        lowered = stripped.lower()
        if any(lowered.startswith(prefix) for prefix in definition_prefixes):
            if lowered_clean_anchor in lowered:
                return index

    # Third pass: fallback to first occurrence anywhere.
    for index, line in enumerate(lines, start=1):
        if lowered_anchor in line.lower():
            return index
    return 0


def _bounded_line_range(
    total_lines: int,
    *,
    center_line: int,
    context_lines: int,
) -> tuple[int, int]:
    """Return a safe 1-based inclusive line range around center_line."""
    if total_lines <= 0:
        return 0, 0

    if center_line < 1:
        center_line = 1
    if center_line > total_lines:
        center_line = total_lines

    start = max(1, center_line - context_lines)
    end = min(total_lines, center_line + context_lines)
    return start, end


def extract_live_source_snippet(
    project_root: str | Path,
    candidate_path: str | Path,
    *,
    line_number: int | None = None,
    anchor: str = "",
    context_lines: int = DEFAULT_CONTEXT_LINES,
    max_file_size_bytes: int = DEFAULT_MAX_TEXT_FILE_SIZE_BYTES,
) -> LiveSourceSnippetResult:
    """Extract a bounded snippet from a verified live source file.

    If both anchor and line_number are provided, anchor takes priority when it
    is found. If neither is provided, the snippet starts near the top of file.
    """
    path_result, text = read_live_source_text(
        project_root,
        candidate_path,
        max_file_size_bytes=max_file_size_bytes,
    )

    if path_result.status != "ok":
        return LiveSourceSnippetResult(
            path_result=path_result,
            status=path_result.status,
            line_start=0,
            line_end=0,
            anchor=anchor,
            text="",
            message=path_result.message,
        )

    lines = text.splitlines()
    if not lines:
        return LiveSourceSnippetResult(
            path_result=path_result,
            status="empty",
            line_start=0,
            line_end=0,
            anchor=anchor,
            text="",
            message="File is empty.",
        )

    anchor_line = _find_anchor_line(lines, anchor)
    if anchor_line:
        center_line = anchor_line
    elif line_number is not None:
        center_line = int(line_number)
    else:
        center_line = 1

    start, end = _bounded_line_range(
        len(lines),
        center_line=center_line,
        context_lines=max(0, int(context_lines)),
    )
    snippet_lines = lines[start - 1:end]

    return LiveSourceSnippetResult(
        path_result=path_result,
        status="ok",
        line_start=start,
        line_end=end,
        anchor=anchor,
        text="\n".join(snippet_lines),
        message="Snippet extracted from live source.",
    )


def batch_verify_sources(
    project_root: str | Path,
    candidate_paths: Iterable[str | Path],
    *,
    max_file_size_bytes: int = DEFAULT_MAX_TEXT_FILE_SIZE_BYTES,
) -> list[LiveSourcePathResult]:
    """Verify multiple live source paths."""
    return [
        verify_live_source_path(
            project_root,
            candidate_path,
            max_file_size_bytes=max_file_size_bytes,
        )
        for candidate_path in candidate_paths
    ]


def _result_to_json(value: LiveSourcePathResult | LiveSourceSnippetResult) -> str:
    """Serialize a live source result as formatted JSON."""
    return json.dumps(asdict(value), indent=2, sort_keys=True)


def main(argv: list[str] | None = None) -> int:
    """Run live source verification from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, help="Selected PROJECT_ROOT.")
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Project-relative or absolute source path. May be repeated.",
    )
    parser.add_argument(
        "--snippet",
        action="store_true",
        help="Extract snippets instead of path verification only.",
    )
    parser.add_argument(
        "--line",
        type=int,
        default=None,
        help="1-based line number for snippet extraction.",
    )
    parser.add_argument(
        "--anchor",
        default="",
        help="Anchor text for snippet extraction.",
    )
    parser.add_argument(
        "--context-lines",
        type=int,
        default=DEFAULT_CONTEXT_LINES,
        help="Number of context lines around snippet center.",
    )
    parser.add_argument(
        "--max-file-size-bytes",
        type=int,
        default=DEFAULT_MAX_TEXT_FILE_SIZE_BYTES,
        help="Maximum file size allowed for hashing/reading.",
    )
    args = parser.parse_args(argv)

    try:
        for item in args.path:
            if args.snippet:
                result = extract_live_source_snippet(
                    args.project_root,
                    item,
                    line_number=args.line,
                    anchor=args.anchor,
                    context_lines=args.context_lines,
                    max_file_size_bytes=args.max_file_size_bytes,
                )
            else:
                result = verify_live_source_path(
                    args.project_root,
                    item,
                    max_file_size_bytes=args.max_file_size_bytes,
                )
            print(_result_to_json(result))
    except Exception as exc:
        print("LIVE SOURCE VERIFICATION ERROR")
        print(type(exc).__name__ + ": " + str(exc))
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
