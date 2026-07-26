# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_read_tools.py
"""Bounded read-only Project tools for Project Web AI agent requests.

This module owns local Project listing, text search, and source reads. It never
writes files, executes commands, reads Project Support, or exposes paths outside
the selected active Project root.
"""

from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path
from threading import Event
from typing import Iterable, Mapping

from kanda_reasoner_app.reasoner_engine.project_web_ai_boundary_context import (
    ProjectAgentBoundaryContext,
)

__all__ = [
    "ProjectReadToolBroker",
    "ProjectReadToolError",
    "ProjectReadToolResult",
]

MAX_TREE_ENTRIES = 240
MAX_SEARCH_RESULTS = 40
MAX_SEARCH_FILES = 3000
MAX_FILE_BYTES = 96 * 1024
MAX_FILE_LINES = 500
MAX_RESULT_CHARS = 120_000

_BLOCKED_PARTS = frozenset(
    {
        ".git",
        ".idea",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".svn",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "venv",
    }
)
_BLOCKED_NAMES = frozenset(
    {
        ".env",
        ".env.local",
        "id_rsa",
        "id_ed25519",
        "credentials.json",
        "secrets.json",
    }
)
_TEXT_SUFFIXES = frozenset(
    {
        ".c",
        ".cc",
        ".cfg",
        ".conf",
        ".cpp",
        ".css",
        ".csv",
        ".go",
        ".h",
        ".hpp",
        ".html",
        ".ini",
        ".java",
        ".js",
        ".json",
        ".jsx",
        ".md",
        ".ps1",
        ".py",
        ".pyi",
        ".rst",
        ".sh",
        ".sql",
        ".toml",
        ".ts",
        ".tsx",
        ".txt",
        ".xml",
        ".yaml",
        ".yml",
    }
)


class ProjectReadToolError(RuntimeError):
    """Raised when a read-only Project tool request is unsafe or invalid."""


@dataclass(frozen=True)
class ProjectReadToolResult:
    """Represent one bounded read-only Project tool result."""

    tool: str
    payload: Mapping[str, object]


class ProjectReadToolBroker:
    """Execute bounded read-only operations inside one active Project root."""

    def __init__(
        self,
        project_root: str | Path,
        *,
        boundary: ProjectAgentBoundaryContext,
        cancel_event: Event | None = None,
    ) -> None:
        """Bind the broker to one canonical existing Project root."""
        root = Path(project_root).expanduser()
        try:
            self._root = root.resolve(strict=True)
        except OSError as exc:
            raise ProjectReadToolError(
                "Active Project root could not be resolved: " + str(root)
            ) from exc
        if not self._root.is_dir():
            raise ProjectReadToolError(
                "Active Project root is not a directory: " + str(self._root)
            )
        if _path_key(self._root) != _path_key(boundary.active_project_root):
            raise ProjectReadToolError(
                "Project broker root does not match the request boundary identity."
            )
        self._boundary = boundary
        self._cancel_event = cancel_event

    def execute(self, tool: str, arguments: Mapping[str, object]) -> ProjectReadToolResult:
        """Execute one supported tool and return a bounded serializable payload."""
        self._check_cancelled()
        name = str(tool or "").strip()
        if name == "describe_project_boundaries":
            payload = self._boundary.tool_payload()
        elif name == "list_project_tree":
            payload = self._list_project_tree(arguments)
        elif name == "search_project_text":
            payload = self._search_project_text(arguments)
        elif name == "read_project_file":
            payload = self._read_project_file(arguments)
        elif name == "read_project_file_range":
            payload = self._read_project_file_range(arguments)
        else:
            raise ProjectReadToolError("Unsupported Project tool: " + name)
        return ProjectReadToolResult(tool=name, payload=_bounded_payload(payload))

    def _list_project_tree(self, arguments: Mapping[str, object]) -> Mapping[str, object]:
        """Return a bounded sorted tree rooted at one safe relative directory."""
        base = self._resolve_relative(arguments.get("path", "."), require_file=False)
        if not base.is_dir():
            raise ProjectReadToolError("Tree path is not a directory: " + _relative(base, self._root))
        maximum = _bounded_int(arguments.get("maximum_entries"), 1, MAX_TREE_ENTRIES, 160)
        entries: list[dict[str, object]] = []
        for path in self._walk_paths(base):
            self._check_cancelled()
            relative = _relative(path, self._root)
            if path.is_dir():
                kind = "directory"
                size = 0
            elif path.is_file():
                kind = "file"
                size = path.stat().st_size
            else:
                continue
            entries.append({"path": relative, "kind": kind, "size_bytes": size})
            if len(entries) >= maximum:
                break
        return {
            "root": _relative(base, self._root),
            "entry_count": len(entries),
            "truncated": len(entries) >= maximum,
            "entries": entries,
        }

    def _search_project_text(self, arguments: Mapping[str, object]) -> Mapping[str, object]:
        """Search bounded UTF-8 text files for one literal case-insensitive query."""
        query = str(arguments.get("query") or "").strip()
        if not query:
            raise ProjectReadToolError("search_project_text requires a non-empty query.")
        if len(query) > 240:
            raise ProjectReadToolError("Search query exceeds 240 characters.")
        includes = _string_list(arguments.get("include")) or ("*",)
        maximum = _bounded_int(arguments.get("maximum_results"), 1, MAX_SEARCH_RESULTS, 20)
        results: list[dict[str, object]] = []
        files_scanned = 0
        query_folded = query.casefold()
        for path in self._iter_text_files(includes):
            self._check_cancelled()
            files_scanned += 1
            if files_scanned > MAX_SEARCH_FILES:
                break
            text = self._read_text(path, maximum_bytes=MAX_FILE_BYTES)
            for line_number, line in enumerate(text.splitlines(), start=1):
                if query_folded not in line.casefold():
                    continue
                results.append(
                    {
                        "path": _relative(path, self._root),
                        "line": line_number,
                        "text": line.strip()[:360],
                    }
                )
                if len(results) >= maximum:
                    return {
                        "query": query,
                        "files_scanned": files_scanned,
                        "result_count": len(results),
                        "truncated": True,
                        "results": results,
                    }
        return {
            "query": query,
            "files_scanned": files_scanned,
            "result_count": len(results),
            "truncated": files_scanned > MAX_SEARCH_FILES,
            "results": results,
        }

    def _read_project_file(self, arguments: Mapping[str, object]) -> Mapping[str, object]:
        """Read one bounded UTF-8 text file from the active Project."""
        path = self._resolve_relative(arguments.get("path"), require_file=True)
        text = self._read_text(path, maximum_bytes=MAX_FILE_BYTES)
        lines = text.splitlines()
        if len(lines) > MAX_FILE_LINES:
            lines = lines[:MAX_FILE_LINES]
            truncated = True
        else:
            truncated = False
        return {
            "path": _relative(path, self._root),
            "size_bytes": path.stat().st_size,
            "line_count_returned": len(lines),
            "truncated": truncated,
            "content": "\n".join(lines),
        }

    def _read_project_file_range(self, arguments: Mapping[str, object]) -> Mapping[str, object]:
        """Read one bounded one-based line range from a UTF-8 text file."""
        path = self._resolve_relative(arguments.get("path"), require_file=True)
        start = _bounded_int(arguments.get("start_line"), 1, 2_000_000, 1)
        count = _bounded_int(arguments.get("line_count"), 1, MAX_FILE_LINES, 160)
        text = self._read_text(path, maximum_bytes=MAX_FILE_BYTES)
        lines = text.splitlines()
        selected = lines[start - 1 : start - 1 + count]
        return {
            "path": _relative(path, self._root),
            "start_line": start,
            "line_count_returned": len(selected),
            "end_line": start + len(selected) - 1 if selected else start - 1,
            "truncated": start - 1 + count < len(lines),
            "content": "\n".join(selected),
        }

    def _resolve_relative(self, raw_path: object, *, require_file: bool) -> Path:
        """Resolve one relative path and reject escapes, links, and blocked names."""
        text = str(raw_path or "").strip() or "."
        candidate = Path(text)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ProjectReadToolError("Project tool paths must be relative and contained.")
        unresolved = self._root / candidate
        self._assert_no_link_components(unresolved)
        try:
            resolved = unresolved.resolve(strict=True)
            resolved.relative_to(self._root)
        except (OSError, ValueError) as exc:
            raise ProjectReadToolError("Project path is missing or escaped: " + text) from exc
        if self._is_blocked(resolved):
            raise ProjectReadToolError("Project path is blocked: " + text)
        if require_file and not resolved.is_file():
            raise ProjectReadToolError("Project path is not a file: " + text)
        return resolved

    def _assert_no_link_components(self, path: Path) -> None:
        """Reject symlink and Windows reparse-point components before resolution."""
        current = self._root
        relative_parts = path.relative_to(self._root).parts
        for part in relative_parts:
            current = current / part
            if not current.exists():
                break
            if current.is_symlink() or _is_reparse_point(current):
                raise ProjectReadToolError(
                    "Project tool paths cannot traverse links or junctions: "
                    + _relative(current, self._root)
                )

    def _is_blocked(self, path: Path) -> bool:
        """Return whether one path is excluded from Project Web AI reads."""
        try:
            relative = path.relative_to(self._root)
        except ValueError:
            return True
        parts = tuple(part.casefold() for part in relative.parts)
        if any(part in _BLOCKED_PARTS for part in parts):
            return True
        if path.name.casefold() in _BLOCKED_NAMES:
            return True
        return any(part.endswith("_show_project_to_ai") for part in parts)


    def _walk_paths(self, base: Path) -> Iterable[Path]:
        """Yield sorted paths while pruning blocked and linked directories."""
        for current_text, directories, files in os.walk(
            base, topdown=True, followlinks=False
        ):
            self._check_cancelled()
            current = Path(current_text)
            kept_directories: list[str] = []
            for name in sorted(directories, key=str.casefold):
                candidate = current / name
                if self._is_blocked(candidate):
                    continue
                if candidate.is_symlink() or _is_reparse_point(candidate):
                    continue
                kept_directories.append(name)
                yield candidate
            directories[:] = kept_directories
            for name in sorted(files, key=str.casefold):
                candidate = current / name
                if self._is_blocked(candidate):
                    continue
                if candidate.is_symlink() or _is_reparse_point(candidate):
                    continue
                yield candidate

    def _iter_text_files(self, includes: Iterable[str]) -> Iterable[Path]:
        """Yield safe text files matching at least one bounded glob pattern."""
        patterns = tuple(str(item).strip() for item in includes if str(item).strip())
        for path in self._walk_paths(self._root):
            if not path.is_file():
                continue
            relative = _relative(path, self._root)
            if not any(fnmatch.fnmatch(relative, pattern) for pattern in patterns):
                continue
            if path.suffix.casefold() not in _TEXT_SUFFIXES:
                continue
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            yield path

    def _read_text(self, path: Path, *, maximum_bytes: int) -> str:
        """Read one bounded UTF-8 text file and reject binary content."""
        size = path.stat().st_size
        if size > maximum_bytes:
            raise ProjectReadToolError(
                "Project file exceeds the read limit: " + _relative(path, self._root)
            )
        raw = path.read_bytes()
        if b"\x00" in raw:
            raise ProjectReadToolError(
                "Binary files cannot be read by Project Web AI: "
                + _relative(path, self._root)
            )
        try:
            return raw.decode("utf-8-sig", errors="strict")
        except UnicodeDecodeError as exc:
            raise ProjectReadToolError(
                "Project file must be UTF-8 text: " + _relative(path, self._root)
            ) from exc

    def _check_cancelled(self) -> None:
        """Stop promptly when the active Project Web AI request is cancelled."""
        if self._cancel_event is not None and self._cancel_event.is_set():
            raise ProjectReadToolError("Project tool request was cancelled.")


def _relative(path: Path, root: Path) -> str:
    """Return one normalized relative path for remote evidence."""
    relative = path.relative_to(root).as_posix()
    return relative or "."


def _bounded_int(value: object, minimum: int, maximum: int, default: int) -> int:
    """Return one integer clamped to an explicit safe range."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, min(maximum, parsed))


def _string_list(value: object) -> tuple[str, ...]:
    """Return a small tuple of non-empty glob strings."""
    if isinstance(value, str):
        values = (value,)
    elif isinstance(value, (list, tuple)):
        values = tuple(str(item) for item in value)
    else:
        values = ()
    return tuple(item.strip()[:120] for item in values[:12] if item.strip())



def _path_key(path: str | Path) -> str:
    """Return one platform-aware canonical comparison key."""
    return os.path.normcase(str(Path(path).expanduser().resolve(strict=False)))

def _bounded_payload(payload: Mapping[str, object]) -> Mapping[str, object]:
    """Fail closed when one serialized tool result exceeds the agent budget."""
    text = repr(dict(payload))
    if len(text) > MAX_RESULT_CHARS:
        raise ProjectReadToolError("Project tool result exceeded the response budget.")
    return payload


def _is_reparse_point(path: Path) -> bool:
    """Return whether one existing Windows path has the reparse-point flag."""
    if os.name != "nt":
        return False
    try:
        attributes = path.stat().st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & 0x400)
