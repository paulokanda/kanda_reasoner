"""Create or incrementally update Project Structure 3D complete JSON ZIPs."""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .complete_json_artifacts import (
    COMPLETE_JSON_PART_LIMIT_BYTES,
    COMPLETE_JSON_STREAM_ROTATE_BYTES,
    complete_json_artifact_dir,
    complete_json_building_dir,
    complete_json_manifest_path,
    complete_json_previous_dir,
    complete_json_state_db_path,
    inspect_complete_json_artifacts,
)
from .complete_json_index import CompleteJsonDiskIndex
from .complete_json_stream_writer import CompleteJsonZipStreamWriter

__all__ = ["build_project_structure_complete_json"]


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _json_load(text: str) -> Any:
    return json.loads(text)


def _write_mapping(writer: CompleteJsonZipStreamWriter, rows: Iterable, key: str, value: str) -> None:
    writer.write("{")
    first = True
    for row in rows:
        if not first:
            writer.write(",")
        writer.write_json(str(row[key]))
        writer.write(":")
        writer.write(str(row[value]))
        first = False
    writer.write("}")


def _write_array(writer: CompleteJsonZipStreamWriter, rows: Iterable, field: str) -> None:
    writer.write("[")
    first = True
    for row in rows:
        value = _json_load(str(row[field]))
        if isinstance(value, list):
            values = value
        else:
            values = [value]
        for item in values:
            if not first:
                writer.write(",")
            writer.write_json(item)
            first = False
    writer.write("]")


def _write_symbol_mapping(
    writer: CompleteJsonZipStreamWriter,
    rows: Iterable,
    *,
    web_variant: bool,
) -> None:
    writer.write("{")
    first = True
    for row in rows:
        symbols = _json_load(str(row["symbols_json"]))
        for symbol in symbols if isinstance(symbols, list) else []:
            if not isinstance(symbol, dict):
                continue
            key = str(symbol.get("key") or "")
            if not key:
                continue
            value = dict(symbol)
            value.pop("key", None)
            if web_variant:
                value = {
                    "symbol": value.get("name", ""),
                    "qualified_name": value.get("qualified_name", key),
                    "kind": value.get("kind", "unknown"),
                    "file": value.get("file", ""),
                    "module_name": value.get("module_name", ""),
                    "line_start": value.get("line_start", 0),
                    "line_end": value.get("line_end", 0),
                }
            if not first:
                writer.write(",")
            writer.write_json(key)
            writer.write(":")
            writer.write_json(value)
            first = False
    writer.write("}")


def _test_protection(index: CompleteJsonDiskIndex) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows = list(index.connection.execute("SELECT path, is_test FROM files ORDER BY path"))
    test_paths = [str(row["path"]) for row in rows if int(row["is_test"]) == 1]
    result: dict[str, Any] = {}
    links: list[dict[str, Any]] = []
    for row in rows:
        source = str(row["path"])
        if int(row["is_test"]) == 1:
            continue
        source_stem = Path(source).stem.lower()
        matched = [
            test_path
            for test_path in test_paths
            if source_stem and source_stem in Path(test_path).stem.lower()
        ]
        if not matched:
            continue
        linked = [
            {"test_file": test_path, "confidence": "filename_derived"}
            for test_path in matched[:20]
        ]
        result[source] = {
            "source_file": source,
            "linked_tests": linked,
        }
        links.append({"source_file": source, "linked_tests": linked})
    return result, links


def _write_document(
    index: CompleteJsonDiskIndex,
    writer: CompleteJsonZipStreamWriter,
    project_root: Path,
    mode: str,
    metrics: dict[str, int],
    progress=None,
) -> None:
    def section(name: str) -> None:
        writer.write_json(name)
        writer.write(":")

    writer.write("{")
    fixed = {
        "schema_version": "1.0",
        "artifact_type": "project_structure_3d_complete_json",
        "project_slug": project_root.name,
        "project_root": str(project_root),
        "generated_at_utc": _utc_now(),
        "generation_mode": mode,
        "authority": "project_source",
        "consumer": "Project Structure 3D",
        "collection_summary": metrics,
    }
    first = True
    for key, value in fixed.items():
        if not first:
            writer.write(",")
        section(key)
        writer.write_json(value)
        first = False

    writer.write(",")
    section("files")
    _write_array(writer, index.rows(), "record_json")
    if callable(progress):
        progress("Streaming source records directly into ZIP parts")

    writer.write(",")
    section("source_file_index")
    _write_mapping(writer, index.rows(), "path", "source_index_json")

    writer.write(",")
    section("symbol_index")
    _write_symbol_mapping(writer, index.rows(), web_variant=False)

    writer.write(",")
    section("primary_definition_index")
    _write_symbol_mapping(writer, index.rows(), web_variant=False)

    writer.write(",")
    section("web_ai_symbol_index")
    _write_symbol_mapping(writer, index.rows(), web_variant=True)

    writer.write(",")
    section("duplicate_symbols")
    writer.write("[]")

    writer.write(",")
    section("canonical_conflict_index")
    writer.write("{}")

    writer.write(",")
    section("import_graph")
    _write_mapping(writer, index.rows(), "module_name", "imports_json")

    writer.write(",")
    section("call_edges")
    _write_array(writer, index.rows(), "calls_json")

    writer.write(",")
    section("semantic_roles")
    _write_mapping(writer, index.rows(), "path", "semantic_json")

    writer.write(",")
    section("web_ai_file_responsibility_index")
    _write_mapping(writer, index.rows(), "path", "responsibility_json")

    protection, test_links = _test_protection(index)
    writer.write(",")
    section("web_ai_test_protection_index")
    writer.write_json(protection)

    writer.write(",")
    section("test_links")
    writer.write_json(test_links)

    writer.write(",")
    section("errors")
    writer.write("[")
    first_error = True
    for row in index.errors():
        if not first_error:
            writer.write(",")
        writer.write_json({"file": row["path"], "error": row["error_text"]})
        first_error = False
    writer.write("]}")


def _publish(project_root: Path, build_dir: Path) -> None:
    current = complete_json_artifact_dir(project_root)
    previous = complete_json_previous_dir(project_root)
    shutil.rmtree(previous, ignore_errors=True)
    if current.exists():
        os.replace(current, previous)
    try:
        os.replace(build_dir, current)
    except Exception:
        if previous.exists() and not current.exists():
            os.replace(previous, current)
        raise
    shutil.rmtree(previous, ignore_errors=True)


def build_project_structure_complete_json(
    project_root: str | Path,
    *,
    mode: str,
    progress=None,
) -> dict[str, Any]:
    """Build a fresh or incremental disk-indexed JSON ZIP family."""
    root = Path(project_root).expanduser().resolve()
    normalized_mode = str(mode).strip().lower()
    if normalized_mode not in {"create", "incremental"}:
        raise ValueError("mode must be create or incremental")
    current = inspect_complete_json_artifacts(root, verify_hashes=True)
    state_db = complete_json_state_db_path(root)
    if normalized_mode == "incremental":
        if not current.get("valid"):
            raise ValueError("Incremental update requires a valid created Project JSON.")
        if not state_db.is_file():
            raise ValueError("Incremental state is missing; run Create Project JSON once.")
    state_db.parent.mkdir(parents=True, exist_ok=True)
    index = CompleteJsonDiskIndex(state_db)
    build_dir = complete_json_building_dir(root)
    shutil.rmtree(build_dir, ignore_errors=True)
    build_dir.mkdir(parents=True, exist_ok=True)
    writer: CompleteJsonZipStreamWriter | None = None
    try:
        if callable(progress):
            progress("Scanning project files with a disk-backed incremental index")
        metrics = index.update_project(
            root,
            incremental=normalized_mode == "incremental",
            progress=progress,
        )
        writer = CompleteJsonZipStreamWriter(build_dir, root.name)
        _write_document(index, writer, root, normalized_mode, metrics, progress)
        stream_result = writer.finish()
        manifest = {
            "schema_version": "1.0",
            "artifact_type": "canonical_complete_json_zip_family",
            "project_slug": root.name,
            "producer": "project_structure_3d",
            "generation_mode": normalized_mode,
            "generated_at_utc": _utc_now(),
            "original_filename": stream_result["original_filename"],
            "original_size_bytes": stream_result["original_size_bytes"],
            "original_sha256": stream_result["original_sha256"],
            "part_limit_bytes": COMPLETE_JSON_PART_LIMIT_BYTES,
            "stream_rotate_bytes": COMPLETE_JSON_STREAM_ROTATE_BYTES,
            "reconstruction_mode": "ordered_chunks",
            "part_count": len(stream_result["parts"]),
            "parts": stream_result["parts"],
            "incremental_metrics": metrics,
        }
        manifest_path = build_dir / (root.name + "__complete_json_manifest.json")
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if callable(progress):
            progress("Validating ZIP part limits before publication")
        for record in manifest["parts"]:
            if int(record["size_bytes"]) > COMPLETE_JSON_PART_LIMIT_BYTES:
                raise ValueError("A complete JSON ZIP part exceeds 450 MB.")
        _publish(root, build_dir)
        published = inspect_complete_json_artifacts(root, verify_hashes=True)
        if not published.get("valid"):
            raise ValueError("Published Project JSON did not pass verification.")
        return {
            "ok": True,
            "mode": normalized_mode,
            "artifact_dir": str(complete_json_artifact_dir(root)),
            "manifest_path": str(complete_json_manifest_path(root)),
            "part_count": manifest["part_count"],
            "original_size_bytes": manifest["original_size_bytes"],
            "metrics": metrics,
        }
    except Exception:
        if writer is not None:
            writer.abort()
        shutil.rmtree(build_dir, ignore_errors=True)
        raise
    finally:
        index.close()
