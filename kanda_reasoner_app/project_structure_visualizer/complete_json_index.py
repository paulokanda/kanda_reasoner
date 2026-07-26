"""Disk-backed incremental index for Project Structure 3D complete JSON."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

from kanda_reasoner_app.reasoner_context_collector.collector_ast import (
    parse_python_file,
)
from kanda_reasoner_app.reasoner_context_collector.collector_config import (
    CollectorConfig,
)
from kanda_reasoner_app.reasoner_context_collector.collector_roles import (
    summarize_file_semantics,
)
from kanda_reasoner_app.reasoner_context_collector.collector_walker import (
    walk_python_files_filtered,
)

__all__ = ["CompleteJsonDiskIndex"]


def _json_text(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _module_name(relative_path: str) -> str:
    path = PurePosixPath(relative_path)
    parts = list(path.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _is_test_path(relative_path: str) -> bool:
    normalized = relative_path.lower()
    name = PurePosixPath(normalized).name
    return (
        normalized.startswith("tests/")
        or "/tests/" in normalized
        or name.startswith("test_")
        or name.endswith("_test.py")
    )


def _line_count(source: str) -> int:
    return 0 if not source else source.count("\n") + 1


def _symbol_records(
    relative_path: str,
    module_name: str,
    classes: list[dict[str, Any]],
    functions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    def add(raw: dict[str, Any], kind: str, parent: str = "") -> None:
        name = str(raw.get("name") or "").strip()
        qualname = str(raw.get("qualname") or name).strip()
        if not name or not qualname:
            return
        qualified = module_name + "." + qualname if module_name else qualname
        records.append(
            {
                "key": qualified,
                "name": name,
                "qualified_name": qualified,
                "qualname": qualname,
                "kind": kind,
                "file": relative_path,
                "module_name": module_name,
                "line": int(raw.get("lineno") or raw.get("line") or 0),
                "line_start": int(raw.get("lineno") or raw.get("line") or 0),
                "line_end": int(raw.get("line_end") or raw.get("lineno") or 0),
                "parent_symbol": str(raw.get("parent_symbol") or parent),
            }
        )

    for raw_class in classes:
        if not isinstance(raw_class, dict):
            continue
        add(raw_class, "class")
        parent = str(raw_class.get("qualname") or raw_class.get("name") or "")
        for raw_method in raw_class.get("methods", []):
            if isinstance(raw_method, dict):
                add(raw_method, "method", parent)
    for raw_function in functions:
        if isinstance(raw_function, dict):
            add(raw_function, "function")
    return records


def _call_edges(
    relative_path: str,
    classes: list[dict[str, Any]],
    functions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []

    def collect(raw: dict[str, Any]) -> None:
        from_symbol = str(raw.get("qualname") or raw.get("name") or "").strip()
        if not from_symbol:
            return
        for call in raw.get("calls", []):
            if not isinstance(call, dict):
                continue
            to_call = str(call.get("call_name") or call.get("name") or "").strip()
            if not to_call:
                continue
            edges.append(
                {
                    "from_file": relative_path,
                    "from_symbol": from_symbol,
                    "to_call": to_call,
                    "line": int(call.get("lineno") or call.get("line") or 0),
                }
            )

    for raw_class in classes:
        if not isinstance(raw_class, dict):
            continue
        for raw_method in raw_class.get("methods", []):
            if isinstance(raw_method, dict):
                collect(raw_method)
    for raw_function in functions:
        if isinstance(raw_function, dict):
            collect(raw_function)
    return edges


class CompleteJsonDiskIndex:
    """Persist per-file analysis so incremental updates parse only changes."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def close(self) -> None:
        self.connection.close()

    def reset(self) -> None:
        self.connection.executescript(
            "DELETE FROM files; DELETE FROM errors; DELETE FROM metadata;"
        )
        self.connection.commit()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            PRAGMA journal_mode=WAL;
            PRAGMA synchronous=NORMAL;
            CREATE TABLE IF NOT EXISTS files (
                path TEXT PRIMARY KEY,
                size_bytes INTEGER NOT NULL,
                mtime_ns INTEGER NOT NULL,
                sha256 TEXT NOT NULL,
                module_name TEXT NOT NULL,
                is_test INTEGER NOT NULL,
                record_json TEXT NOT NULL,
                source_index_json TEXT NOT NULL,
                semantic_json TEXT NOT NULL,
                responsibility_json TEXT NOT NULL,
                imports_json TEXT NOT NULL,
                symbols_json TEXT NOT NULL,
                calls_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS errors (
                path TEXT PRIMARY KEY,
                error_text TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        self.connection.commit()

    def update_project(
        self,
        project_root: str | Path,
        *,
        incremental: bool,
        progress=None,
    ) -> dict[str, int]:
        root = Path(project_root).expanduser().resolve()
        if not incremental:
            self.reset()
        config = CollectorConfig()
        python_files = walk_python_files_filtered(root, config)
        current_paths = {
            path.relative_to(root).as_posix(): path
            for path in python_files
        }
        existing_paths = {
            str(row["path"])
            for row in self.connection.execute("SELECT path FROM files")
        }
        error_paths = {
            str(row["path"])
            for row in self.connection.execute("SELECT path FROM errors")
        }
        removed = sorted((existing_paths | error_paths) - set(current_paths))
        for relative_path in removed:
            self.connection.execute("DELETE FROM files WHERE path = ?", (relative_path,))
            self.connection.execute("DELETE FROM errors WHERE path = ?", (relative_path,))

        changed = 0
        unchanged = 0
        parsed_errors = 0
        total = len(current_paths)
        for index, relative_path in enumerate(sorted(current_paths), start=1):
            path = current_paths[relative_path]
            stat = path.stat()
            existing = self.connection.execute(
                "SELECT size_bytes, mtime_ns FROM files WHERE path = ?",
                (relative_path,),
            ).fetchone()
            if (
                incremental
                and existing is not None
                and int(existing["size_bytes"]) == stat.st_size
                and int(existing["mtime_ns"]) == stat.st_mtime_ns
            ):
                unchanged += 1
                if callable(progress) and (index == total or index % 50 == 0):
                    progress(f"Indexed {index}/{total} files; unchanged={unchanged}")
                continue
            parsed, error = parse_python_file(path)
            if error is not None or parsed is None:
                parsed_errors += 1
                self.connection.execute("DELETE FROM files WHERE path = ?", (relative_path,))
                self.connection.execute(
                    "INSERT OR REPLACE INTO errors(path, error_text) VALUES (?, ?)",
                    (relative_path, str(error or "unknown parse error")),
                )
                continue
            self.connection.execute("DELETE FROM errors WHERE path = ?", (relative_path,))
            record = self._build_record(root, path, relative_path, parsed)
            self.connection.execute(
                """
                INSERT OR REPLACE INTO files(
                    path, size_bytes, mtime_ns, sha256, module_name, is_test,
                    record_json, source_index_json, semantic_json,
                    responsibility_json, imports_json, symbols_json, calls_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    relative_path,
                    stat.st_size,
                    stat.st_mtime_ns,
                    record["sha256"],
                    record["module_name"],
                    int(record["is_test"]),
                    _json_text(record["file_record"]),
                    _json_text(record["source_index"]),
                    _json_text(record["semantic"]),
                    _json_text(record["responsibility"]),
                    _json_text(record["imports"]),
                    _json_text(record["symbols"]),
                    _json_text(record["calls"]),
                ),
            )
            changed += 1
            if callable(progress) and (index == total or index % 20 == 0):
                progress(f"Parsed {index}/{total} files; changed={changed}")
        self.connection.commit()
        return {
            "file_count": self.count_files(),
            "changed": changed,
            "unchanged": unchanged,
            "removed": len(removed),
            "errors": parsed_errors,
        }

    def _build_record(
        self,
        root: Path,
        path: Path,
        relative_path: str,
        parsed: dict[str, Any],
    ) -> dict[str, Any]:
        source = str(parsed.get("source") or "")
        module_name = _module_name(relative_path)
        classes = [item for item in parsed.get("classes", []) if isinstance(item, dict)]
        functions = [item for item in parsed.get("functions", []) if isinstance(item, dict)]
        semantic = summarize_file_semantics(
            {
                "imports": parsed.get("imports", []),
                "comments": parsed.get("comments", []),
                "strings": parsed.get("strings", []),
                "docstring": parsed.get("module_docstring", ""),
                "classes": classes,
                "functions": functions,
            }
        )
        file_hash = _file_sha256(path)
        symbol_count = len(functions) + sum(
            1 + len(item.get("methods", [])) for item in classes
        )
        primary_role = str(semantic.get("primary_role") or "")
        summary = (primary_role + " file") if primary_role else "general python module"
        file_record = {
            "path": relative_path,
            "module_name": module_name,
            "imports": parsed.get("imports", []),
            "classes": classes,
            "functions": functions,
            "docstring": parsed.get("module_docstring", ""),
            "comments": parsed.get("comments", []),
            "strings": parsed.get("strings", []),
            "semantic_hints": semantic.get("evidence_terms", []),
            "semantic_roles": semantic.get("roles", []),
            "primary_role": primary_role,
            "secondary_roles": semantic.get("secondary_roles", []),
            "role_confidence": semantic.get("confidence", 0.0),
            "summary": summary,
            "source": source,
            "file_sha256": file_hash,
        }
        source_index = {
            "file": relative_path,
            "module_name": module_name,
            "line_count": _line_count(source),
            "symbol_count": symbol_count,
            "size_bytes": path.stat().st_size,
            "sha256": file_hash,
        }
        responsibility = {
            "source_file": relative_path,
            "owner_box": relative_path.split("/", 1)[0],
            "primary_responsibility": summary,
            "confidence": semantic.get("confidence", 0.0),
        }
        return {
            "sha256": file_hash,
            "module_name": module_name,
            "is_test": _is_test_path(relative_path),
            "file_record": file_record,
            "source_index": source_index,
            "semantic": {
                "roles": semantic.get("roles", []),
                "primary_role": primary_role,
                "secondary_roles": semantic.get("secondary_roles", []),
                "confidence": semantic.get("confidence", 0.0),
                "evidence_terms": semantic.get("evidence_terms", []),
            },
            "responsibility": responsibility,
            "imports": parsed.get("imports", []),
            "symbols": _symbol_records(relative_path, module_name, classes, functions),
            "calls": _call_edges(relative_path, classes, functions),
        }

    def count_files(self) -> int:
        row = self.connection.execute("SELECT COUNT(*) AS count FROM files").fetchone()
        return int(row["count"] if row is not None else 0)

    def rows(self) -> Iterable[sqlite3.Row]:
        return self.connection.execute("SELECT * FROM files ORDER BY path")

    def errors(self) -> Iterable[sqlite3.Row]:
        return self.connection.execute("SELECT * FROM errors ORDER BY path")
