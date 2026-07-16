"""ZIP export helpers for the additive AI context bundle."""

from __future__ import annotations

import json
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from .bundle_checker import check_ai_context_bundle
from .hashing import sha256_file
from .output_paths import bundle_artifact_paths
from .path_normalization import relative_posix_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ProjectContext

__all__ = ["zip_ai_context_bundle"]

ZIP_KIND = "ai_context_bundle_zip"
ZIP_GENERATOR = "project_context_bundle.bundle_zipper"
ZIP_GENERATOR_VERSION = "1.0.0"


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _load_json_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Expected JSON object: " + str(path))
    return payload


def _resolve_project_artifact(context: ProjectContext, relative_path: str) -> Path:
    artifact = safe_resolve(context.root / relative_path)
    root = safe_resolve(context.root)
    try:
        artifact.relative_to(root)
    except ValueError as exc:
        raise ValueError("Artifact path escapes project root: " + relative_path) from exc
    return artifact


def _manifest_artifact_paths(context: ProjectContext) -> list[Path]:
    paths = bundle_artifact_paths(context)
    if not paths.bundle_manifest_json.exists():
        raise ValueError("Bundle manifest is missing: " + str(paths.bundle_manifest_json))

    manifest = _load_json_object(paths.bundle_manifest_json)
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("bundle_manifest.artifacts must be a list")

    result: list[Path] = []
    for item in artifacts:
        if not isinstance(item, dict):
            raise ValueError("bundle_manifest artifact entry is not an object")
        relative_path = str(item.get("path", ""))
        expected_hash = str(item.get("sha256", ""))
        required = bool(item.get("required", False))
        if not relative_path:
            raise ValueError("bundle_manifest artifact entry is missing path")
        artifact = _resolve_project_artifact(context, relative_path)
        if not artifact.exists():
            if required:
                raise ValueError("Required artifact is missing: " + relative_path)
            continue
        if expected_hash and sha256_file(artifact) != expected_hash:
            raise ValueError("Artifact hash mismatch before ZIP: " + relative_path)
        result.append(artifact)
    return result


def _optional_runtime_trace_path(context: ProjectContext) -> Path | None:
    paths = bundle_artifact_paths(context)
    complete_json = paths.complete_json
    suffix = "__complete.json"
    if not complete_json.name.endswith(suffix):
        return None
    trace_name = complete_json.name[: -len(suffix)] + "__complete_runtime_trace.json"
    trace_path = complete_json.with_name(trace_name)
    if trace_path.exists() and trace_path.is_file():
        return trace_path
    return None


def _artifact_records(paths: list[Path], context: ProjectContext) -> list[dict[str, Any]]:
    records = []
    for path in paths:
        records.append(
            {
                "path": relative_posix_path(path, context.root),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return records


def _safe_zip_member_name(base_folder: str, path: Path, context: ProjectContext) -> str:
    relative = relative_posix_path(path, context.root)
    if relative.startswith("../") or relative == "..":
        raise ValueError("ZIP artifact path escapes project root: " + str(path))
    return base_folder + "/" + relative


def _timestamp_value(timestamp: str | None) -> str:
    if timestamp is not None:
        cleaned = timestamp.strip()
        if not cleaned:
            raise ValueError("timestamp must not be empty")
        return cleaned
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def zip_ai_context_bundle(
    project: str | Path | ProjectContext,
    destination_folder: str | Path,
    *,
    timestamp: str | None = None,
    include_runtime_trace: bool = True,
    check_bundle: bool = True,
) -> dict[str, Any]:
    """Create a ZIP containing the current project's AI context bundle.

    The destination folder is supplied by the caller, normally a GUI folder
    picker. This helper does not hardcode any project root or export location.
    """
    context = _context(project)
    destination = Path(destination_folder).expanduser()
    if not destination.exists() or not destination.is_dir():
        return {
            "ok": False,
            "kind": ZIP_KIND,
            "project_slug": context.project_slug,
            "failures": ["Destination folder does not exist: " + str(destination)],
        }

    if check_bundle:
        check_result = check_ai_context_bundle(context)
        if not bool(check_result.get("ok", False)):
            failures = check_result.get("failures", [])
            if not isinstance(failures, list):
                failures = ["Unknown bundle checker failure"]
            return {
                "ok": False,
                "kind": ZIP_KIND,
                "project_slug": context.project_slug,
                "failures": [str(item) for item in failures],
                "check_result": check_result,
            }

    try:
        required_paths = _manifest_artifact_paths(context)
        optional_paths: list[Path] = []
        if include_runtime_trace:
            runtime_trace = _optional_runtime_trace_path(context)
            if runtime_trace is not None:
                optional_paths.append(runtime_trace)

        stamp = _timestamp_value(timestamp)
        zip_stem = context.project_slug + "__ai_context_bundle__" + stamp
        zip_path = destination / (zip_stem + ".zip")
        base_folder = zip_stem

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for artifact in required_paths + optional_paths:
                archive.write(
                    artifact,
                    arcname=_safe_zip_member_name(base_folder, artifact, context),
                )

        zipped_paths = required_paths + optional_paths
        return {
            "ok": True,
            "kind": ZIP_KIND,
            "generator": {
                "name": ZIP_GENERATOR,
                "version": ZIP_GENERATOR_VERSION,
            },
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "destination_folder": str(destination),
            "zip_path": str(zip_path),
            "zip_filename": zip_path.name,
            "zip_sha256": sha256_file(zip_path),
            "zip_size_bytes": zip_path.stat().st_size,
            "artifact_count": len(zipped_paths),
            "required_artifact_count": len(required_paths),
            "optional_artifact_count": len(optional_paths),
            "artifacts": _artifact_records(zipped_paths, context),
            "failures": [],
        }
    except Exception as exc:
        return {
            "ok": False,
            "kind": ZIP_KIND,
            "project_slug": context.project_slug,
            "failures": [str(exc)],
        }
