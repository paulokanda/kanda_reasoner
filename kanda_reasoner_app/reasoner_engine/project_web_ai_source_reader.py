# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_source_reader.py
"""Read explicitly selected Project source files for bounded Web AI review.

This module owns exact, read-only source selection and containment checks. It
never writes Project source, Project Support, Error Memory, or Freeze state.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

__all__ = [
    "ExactProjectSourceFile",
    "ProjectSourceReadError",
    "read_exact_project_sources",
]

MAX_SOURCE_FILE_COUNT = 6
MAX_SOURCE_FILE_BYTES = 256 * 1024
MAX_TOTAL_SOURCE_BYTES = 640 * 1024


class ProjectSourceReadError(RuntimeError):
    """Raised when selected source cannot be read safely and exactly."""


@dataclass(frozen=True)
class ExactProjectSourceFile:
    """Represent one exact UTF-8 Project file selected by the human."""

    relative_path: str
    sha256: str
    size_bytes: int
    text: str
    had_utf8_bom: bool
    newline: str

    def prompt_block(self) -> str:
        """Return one bounded source block for the remote proposal request."""
        return (
            "PROJECT_SOURCE_FILE_BEGIN\n"
            + "relative_path: "
            + self.relative_path
            + "\nsha256: "
            + self.sha256
            + "\nsize_bytes: "
            + str(self.size_bytes)
            + "\ncontent_begin\n"
            + self.text
            + ("" if self.text.endswith(("\n", "\r")) else "\n")
            + "content_end\nPROJECT_SOURCE_FILE_END"
        )


def read_exact_project_sources(
    project_root: str | Path,
    selected_paths: Iterable[str | Path],
) -> tuple[ExactProjectSourceFile, ...]:
    """Return exact selected files after strict Project containment checks."""
    root = _canonical_existing_directory(project_root)
    raw_paths = tuple(selected_paths)
    if not raw_paths:
        raise ProjectSourceReadError("Select at least one Project source file.")
    if len(raw_paths) > MAX_SOURCE_FILE_COUNT:
        raise ProjectSourceReadError(
            "Select at most " + str(MAX_SOURCE_FILE_COUNT) + " source files."
        )

    sources: list[ExactProjectSourceFile] = []
    seen: set[str] = set()
    total_bytes = 0
    for raw_path in raw_paths:
        source = _read_one(root, raw_path)
        key = source.relative_path.casefold()
        if key in seen:
            raise ProjectSourceReadError(
                "The same source file was selected more than once: "
                + source.relative_path
            )
        seen.add(key)
        total_bytes += source.size_bytes
        if total_bytes > MAX_TOTAL_SOURCE_BYTES:
            raise ProjectSourceReadError(
                "Selected source exceeds the total exact-source byte limit of "
                + str(MAX_TOTAL_SOURCE_BYTES)
                + "."
            )
        sources.append(source)
    return tuple(sources)


def _canonical_existing_directory(path_value: str | Path) -> Path:
    """Return one existing canonical directory."""
    path = Path(path_value).expanduser()
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise ProjectSourceReadError(
            "Project root could not be resolved: " + str(path)
        ) from exc
    if not resolved.is_dir():
        raise ProjectSourceReadError("Project root is not a directory: " + str(path))
    return resolved


def _read_one(root: Path, raw_path: str | Path) -> ExactProjectSourceFile:
    """Read one exact file and reject escapes, binaries, and unsupported text."""
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise ProjectSourceReadError(
            "Selected source file could not be resolved: " + str(candidate)
        ) from exc
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ProjectSourceReadError(
            "Selected source must remain inside the active Project root: "
            + str(candidate)
        ) from exc
    if not resolved.is_file():
        raise ProjectSourceReadError(
            "Selected source is not a regular file: " + relative.as_posix()
        )
    size_bytes = resolved.stat().st_size
    if size_bytes > MAX_SOURCE_FILE_BYTES:
        raise ProjectSourceReadError(
            "Selected source exceeds the per-file byte limit: "
            + relative.as_posix()
        )
    raw = resolved.read_bytes()
    if b"\x00" in raw:
        raise ProjectSourceReadError(
            "Binary source files cannot be sent to Project Web AI: "
            + relative.as_posix()
        )
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    try:
        text = raw.decode("utf-8-sig" if had_bom else "utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ProjectSourceReadError(
            "Selected source must be valid UTF-8 text: " + relative.as_posix()
        ) from exc
    return ExactProjectSourceFile(
        relative_path=relative.as_posix(),
        sha256=hashlib.sha256(raw).hexdigest(),
        size_bytes=len(raw),
        text=text,
        had_utf8_bom=had_bom,
        newline=_detect_newline(raw),
    )


def _detect_newline(raw: bytes) -> str:
    """Return the dominant source newline sequence."""
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    return "\r\n" if crlf > lf else "\n"
