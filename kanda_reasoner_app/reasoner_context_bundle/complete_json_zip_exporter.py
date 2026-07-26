"""Dedicated ZIP-family export for canonical complete JSON evidence."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from .hashing import sha256_file
from .output_paths import bundle_artifact_paths
from .schema_models import ProjectContext

COMPLETE_JSON_PART_LIMIT_BYTES = 450 * 1024 * 1024
_COMPLETE_JSON_CHUNK_BYTES = 400 * 1024 * 1024
_SCHEMA_VERSION = "1.0"

__all__ = ["COMPLETE_JSON_PART_LIMIT_BYTES", "write_complete_json_zip_family"]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def _part_record(path: Path, member_name: str, member_size: int, member_hash: str) -> dict[str, Any]:
    return {
        "package": "complete_json",
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "member_name": member_name,
        "member_size_bytes": member_size,
        "member_sha256": member_hash,
    }


def _zip_single_file(source: Path, destination: Path) -> dict[str, Any]:
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        allowZip64=True,
    ) as archive:
        archive.write(source, arcname=source.name)
    return _part_record(
        destination,
        source.name,
        source.stat().st_size,
        sha256_file(source),
    )


def _zip_chunk(
    chunk_path: Path,
    destination: Path,
    member_name: str,
) -> dict[str, Any]:
    with zipfile.ZipFile(
        destination,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        allowZip64=True,
    ) as archive:
        archive.write(chunk_path, arcname=member_name)
    record = _part_record(
        destination,
        member_name,
        chunk_path.stat().st_size,
        sha256_file(chunk_path),
    )
    if int(record["size_bytes"]) > COMPLETE_JSON_PART_LIMIT_BYTES:
        raise ValueError(
            "Complete JSON ZIP part exceeds 450 MB: " + destination.name
        )
    return record


def _write_chunk_parts(
    complete_json: Path,
    output_dir: Path,
    project_slug: str,
    temp_root: Path,
) -> list[dict[str, Any]]:
    chunks: list[tuple[Path, str]] = []
    with complete_json.open("rb") as source:
        index = 1
        while True:
            data = source.read(_COMPLETE_JSON_CHUNK_BYTES)
            if not data:
                break
            member_name = complete_json.name + ".part" + str(index).zfill(4)
            chunk_path = temp_root / member_name
            chunk_path.write_bytes(data)
            chunks.append((chunk_path, member_name))
            index += 1

    total = len(chunks)
    records: list[dict[str, Any]] = []
    for index, (chunk_path, member_name) in enumerate(chunks, start=1):
        zip_name = (
            project_slug
            + "__complete_json_part"
            + str(index).zfill(2)
            + "_of_"
            + str(total).zfill(2)
            + ".zip"
        )
        records.append(
            _zip_chunk(chunk_path, output_dir / zip_name, member_name)
        )
    return records


def write_complete_json_zip_family(
    context: ProjectContext,
    output_dir: str | Path,
) -> dict[str, Any]:
    """Write canonical complete JSON as standalone ZIP part(s) plus manifest."""
    destination = Path(output_dir).expanduser().resolve(strict=False)
    destination.mkdir(parents=True, exist_ok=True)
    complete_json = bundle_artifact_paths(context).complete_json.resolve(strict=True)
    original_size = complete_json.stat().st_size
    original_hash = sha256_file(complete_json)
    temp_root = Path(tempfile.mkdtemp(prefix=".complete_json_zip_", dir=str(destination.parent)))
    created: list[Path] = []
    try:
        provisional = temp_root / (context.project_slug + "__complete_json_probe.zip")
        probe_record = _zip_single_file(complete_json, provisional)
        records: list[dict[str, Any]]
        mode: str
        if int(probe_record["size_bytes"]) <= COMPLETE_JSON_PART_LIMIT_BYTES:
            final_name = context.project_slug + "__complete_json_part01_of_01.zip"
            final_path = destination / final_name
            shutil.move(str(provisional), str(final_path))
            records = [_part_record(final_path, complete_json.name, original_size, original_hash)]
            created.append(final_path)
            mode = "single_member"
        else:
            provisional.unlink(missing_ok=True)
            records = _write_chunk_parts(
                complete_json,
                destination,
                context.project_slug,
                temp_root,
            )
            created.extend(destination / str(item["filename"]) for item in records)
            mode = "ordered_chunks"

        manifest = {
            "schema_version": _SCHEMA_VERSION,
            "artifact_type": "canonical_complete_json_zip_family",
            "project_slug": context.project_slug,
            "original_filename": complete_json.name,
            "original_size_bytes": original_size,
            "original_sha256": original_hash,
            "part_limit_bytes": COMPLETE_JSON_PART_LIMIT_BYTES,
            "reconstruction_mode": mode,
            "part_count": len(records),
            "parts": records,
        }
        manifest_path = destination / (
            context.project_slug + "__complete_json_manifest.json"
        )
        _write_json(manifest_path, manifest)
        created.append(manifest_path)
        return {
            "ok": True,
            "package": "complete_json",
            "manifest_path": str(manifest_path),
            "zip_parts": records,
            "created_paths": [str(path) for path in created],
        }
    except Exception:
        for path in created:
            try:
                path.unlink()
            except OSError:
                pass
        raise
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
