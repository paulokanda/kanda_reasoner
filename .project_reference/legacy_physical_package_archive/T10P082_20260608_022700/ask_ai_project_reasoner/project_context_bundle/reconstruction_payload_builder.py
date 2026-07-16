"""Build a lossless active-project reconstruction payload."""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from .exclusion_engine import decide_path_exclusion
from .exclusion_provider import load_bundle_exclusion_rules
from .file_manifest_builder import build_file_manifest_payload
from .hashing import sha256_bytes
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .path_normalization import relative_posix_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ExclusionRules, ProjectContext

__all__ = [
    "build_reconstruction_payload",
    "write_reconstruction_payload_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "reconstruction_payload"
GENERATOR_NAME = "project_context_bundle.reconstruction_payload_builder"
GENERATOR_VERSION = "1.0.0"

_GENERATED_EVIDENCE_PREFIXES = (
    "project_analysis_evidence/json_complete/",
    "project_analysis_evidence/json_splitted/",
)


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _utc_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _is_generated_evidence_path(path: Path, context: ProjectContext) -> bool:
    relative = relative_posix_path(path, context.root).replace("\\", "/").lower().lstrip("/")
    return any(relative.startswith(prefix) for prefix in _GENERATED_EVIDENCE_PREFIXES)


def _iter_project_entries(root: Path) -> Iterator[Path]:
    try:
        entries = sorted(root.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
    except OSError:
        return
    for entry in entries:
        yield entry


def _active_directories(context: ProjectContext, rules: ExclusionRules) -> list[dict[str, Any]]:
    root = safe_resolve(context.root)
    directories: list[dict[str, Any]] = []

    def walk(current: Path) -> None:
        for entry in _iter_project_entries(current):
            if entry.is_symlink():
                continue
            if _is_generated_evidence_path(entry, context):
                continue
            decision = decide_path_exclusion(entry, context, rules)
            if decision.excluded:
                continue
            if entry.is_dir():
                stat = entry.stat()
                directories.append(
                    {
                        "path": relative_posix_path(entry, context.root),
                        "mtime_ns": stat.st_mtime_ns,
                    }
                )
                walk(entry)

    walk(root)
    directories.sort(key=lambda item: str(item.get("path", "")).lower())
    return directories


def _file_payload_record(record: dict[str, Any], context: ProjectContext) -> dict[str, Any]:
    relative_path = str(record["path"])
    source_path = context.root / Path(relative_path)
    raw = source_path.read_bytes()
    raw_hash = sha256_bytes(raw)
    expected_hash = str(record.get("sha256_raw", ""))
    if expected_hash and expected_hash != raw_hash:
        raise ValueError("Raw hash changed while building reconstruction payload: " + relative_path)
    return {
        "path": relative_path,
        "kind": str(record.get("kind", "unknown")),
        "extension": str(record.get("extension", "")),
        "size_bytes": len(raw),
        "mtime_ns": int(record.get("mtime_ns", 0)),
        "sha256_raw": raw_hash,
        "content_encoding": "base64_raw_bytes",
        "content_base64": base64.b64encode(raw).decode("ascii"),
    }


def _payload_files(manifest: dict[str, Any], context: ProjectContext) -> list[dict[str, Any]]:
    manifest_files = manifest.get("files", [])
    if not isinstance(manifest_files, list):
        raise ValueError("file_manifest.files must be a list")
    files: list[dict[str, Any]] = []
    for item in manifest_files:
        if not isinstance(item, dict):
            continue
        files.append(_file_payload_record(item, context))
    files.sort(key=lambda item: str(item.get("path", "")).lower())
    return files


def _counts(files: list[dict[str, Any]], directories: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "directories": len(directories),
        "files": len(files),
        "binary_files": sum(1 for item in files if item.get("kind") == "binary"),
        "text_files": sum(1 for item in files if item.get("kind") == "text"),
        "unreadable_files": sum(1 for item in files if item.get("kind") == "unreadable"),
        "embedded_files": len(files),
        "embedded_binary_files": sum(1 for item in files if item.get("kind") == "binary"),
    }


def build_reconstruction_payload(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Build a lossless raw-byte payload for active project reconstruction."""
    context = _context(project)
    rules = load_bundle_exclusion_rules(context)
    manifest = build_file_manifest_payload(context)
    files = _payload_files(manifest, context)
    directories = _active_directories(context, rules)
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": _utc_now(),
        "project": {
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "project_analysis_evidence",
            "json_complete_relative": "project_analysis_evidence/json_complete",
        },
        "reconstruction_policy": {
            "scope": "active_project_files_after_project_exclusion_rules",
            "excluded_content": "not_project_content_by_active_exclusion_policy",
            "content_encoding": "base64_raw_bytes",
            "binary_policy": "embed_binary_files_as_base64_raw_bytes",
            "text_policy": "embed_text_files_as_base64_raw_bytes",
            "exact_file_bytes": True,
            "exact_binary_reconstruction": True,
            "exact_active_project_file_reconstruction": True,
            "internet_or_ai_contact": False,
            "hardcoded_project_root": False,
        },
        "counts": _counts(files, directories),
        "directories": directories,
        "files": files,
    }


def write_reconstruction_payload_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__reconstruction_payload.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_reconstruction_payload(context)
    return write_json_atomic(paths.reconstruction_payload_json, payload)
