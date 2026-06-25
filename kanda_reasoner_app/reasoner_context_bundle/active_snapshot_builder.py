"""Build an active source snapshot for one reasoner context bundle."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .file_manifest_builder import build_file_manifest_payload
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .project_context import resolve_project_context
from .schema_models import ProjectContext

__all__ = [
    "SNAPSHOT_TEXT_EXTENSIONS",
    "build_active_snapshot_payload",
    "write_active_snapshot_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "active_snapshot"
GENERATOR_NAME = "reasoner_context_bundle.active_snapshot_builder"
GENERATOR_VERSION = "1.0.1"

SNAPSHOT_TEXT_EXTENSIONS = (
    ".bat",
    ".cmd",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".qss",
    ".toml",
    ".txt",
    ".ui",
    ".xml",
    ".yaml",
    ".yml",
)

_GENERATED_ARTIFACT_PREFIXES = (
    "show_project_to_AI/",
    "show_project_to_AI/second_prompt_files/",
    "show_project_to_AI/json_splitted/",
)


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _is_generated_bundle_artifact(relative_path: str) -> bool:
    rel = relative_path.replace("\\", "/").lower().lstrip("/")
    return any(rel.startswith(prefix) for prefix in _GENERATED_ARTIFACT_PREFIXES)


def _omission_reason(record: dict[str, Any]) -> str:
    path = str(record.get("path", ""))
    if _is_generated_bundle_artifact(path):
        return "generated_context_bundle_artifact"
    kind = str(record.get("kind", ""))
    if kind == "binary":
        return "binary_file_omitted"
    if kind == "unreadable":
        return "unreadable_file_omitted"
    extension = str(record.get("extension", "")).lower()
    if extension not in SNAPSHOT_TEXT_EXTENSIONS:
        return "extension_not_in_snapshot_text_policy"
    if not record.get("included_in_active_snapshot"):
        return "manifest_marked_not_in_snapshot"
    return ""


def _read_snapshot_text(path: Path, encoding: str) -> str:
    selected_encoding = "utf-8-sig" if encoding == "utf-8-sig" else "utf-8"
    with path.open("r", encoding=selected_encoding, errors="replace", newline="") as handle:
        return handle.read()


def _snapshot_file_record(
    record: dict[str, Any],
    context: ProjectContext,
) -> dict[str, Any]:
    relative_path = str(record["path"])
    source_path = context.root / Path(relative_path)
    encoding = str(record.get("encoding") or "utf-8")
    content = _read_snapshot_text(source_path, encoding)
    return {
        "path": relative_path,
        "kind": "text",
        "extension": str(record.get("extension", "")),
        "encoding": encoding,
        "newline": str(record.get("newline", "unknown")),
        "size_bytes": int(record.get("size_bytes", 0)),
        "sha256_raw": str(record.get("sha256_raw", "")),
        "sha256_normalized": str(record.get("sha256_normalized", "")),
        "content": content,
    }


def _omitted_file_record(record: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "path": str(record.get("path", "")),
        "kind": str(record.get("kind", "unknown")),
        "extension": str(record.get("extension", "")),
        "size_bytes": int(record.get("size_bytes", 0)),
        "sha256_raw": str(record.get("sha256_raw", "")),
        "sha256_normalized": str(record.get("sha256_normalized", "")),
        "reason": reason,
    }


def _split_snapshot_records(
    manifest_files: list[dict[str, Any]],
    context: ProjectContext,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    files: list[dict[str, Any]] = []
    omitted_files: list[dict[str, Any]] = []
    for record in manifest_files:
        reason = _omission_reason(record)
        if reason:
            omitted_files.append(_omitted_file_record(record, reason))
            continue
        try:
            files.append(_snapshot_file_record(record, context))
        except OSError as exc:
            omitted = _omitted_file_record(record, "read_error")
            omitted["error"] = str(exc)
            omitted_files.append(omitted)
    return files, omitted_files


def _counts(files: list[dict[str, Any]], omitted_files: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "snapshot_files": len(files),
        "omitted_files": len(omitted_files),
        "text_files": len(files),
        "generated_artifact_omissions": sum(
            1 for item in omitted_files if item.get("reason") == "generated_context_bundle_artifact"
        ),
        "binary_omissions": sum(
            1 for item in omitted_files if item.get("reason") == "binary_file_omitted"
        ),
    }


def build_active_snapshot_payload(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Build a reconstructable text snapshot for one active project."""
    context = _context(project)
    manifest = build_file_manifest_payload(context)
    manifest_files = list(manifest.get("files", []))
    files, omitted_files = _split_snapshot_records(manifest_files, context)
    files.sort(key=lambda item: str(item.get("path", "")).lower())
    omitted_files.sort(key=lambda item: str(item.get("path", "")).lower())
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "project": {
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
        },
        "source": {
            "file_manifest_builder": "reasoner_context_bundle.file_manifest_builder",
            "contract": "project_specific_dynamic_rules",
        },
        "snapshot_policy": {
            "text_extensions": list(SNAPSHOT_TEXT_EXTENSIONS),
            "generated_artifact_prefixes_omitted": list(_GENERATED_ARTIFACT_PREFIXES),
            "binary_policy": "omit_binary_files_in_v1",
            "content_fidelity": "text_content_preserves_original_newline_sequences",
            "exact_reconstruction_scope": (
                "raw text reconstruction is supported for UTF-8 text files without "
                "external filesystem metadata; binary files remain hash-only omissions"
            ),
        },
        "counts": _counts(files, omitted_files),
        "files": files,
        "omitted_files": omitted_files,
    }


def write_active_snapshot_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__active_snapshot.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_active_snapshot_payload(context)
    return write_json_atomic(paths.active_snapshot_json, payload)
