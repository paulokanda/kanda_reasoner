"""Internal support helpers for JSON handoff ZIP export."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .hashing import sha256_file
from .output_paths import bundle_artifact_paths
from .path_normalization import relative_posix_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ProjectContext

_EXPORT_KIND = "json_handoff_zip_parts"
_EXPORT_GENERATOR = "reasoner_context_bundle.handoff_zip_exporter"
_EXPORT_GENERATOR_VERSION = "1.1.0"
_DEFAULT_PART_SIZE_MB = 40
_CONSERVATIVE_PART_SIZE_MB = 25
_BYTES_PER_MB = 1024 * 1024
_RECONSTRUCTION_SUFFIX = "__reconstruction_payload.json"
_RUNTIME_TRACE_SUFFIX = "__complete_runtime_trace.json"

__all__ = [
    "artifact_record",
    "context_from_project",
    "external_readme_text",
    "load_json_object",
    "manifest_artifact_paths",
    "optional_runtime_trace_path",
    "ordered_export_paths",
    "package_readme_text",
    "package_specs",
    "resolve_project_artifact",
    "safe_zip_member_name",
    "timestamp_value",
]


def context_from_project(project: str | Path | ProjectContext) -> ProjectContext:
    """Return a project context from an existing context, path, or string."""
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def load_json_object(path: Path) -> dict[str, Any]:
    """Read a JSON object from path."""
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Expected JSON object: " + str(path))
    return payload


def resolve_project_artifact(context: ProjectContext, relative_path: str) -> Path:
    """Resolve an artifact and reject paths that escape the project root."""
    artifact = safe_resolve(context.root / relative_path)
    root = safe_resolve(context.root)
    try:
        artifact.relative_to(root)
    except ValueError as exc:
        raise ValueError("Artifact path escapes project root: " + relative_path) from exc
    return artifact


def _is_destination_inside_project_root(project_root: str | Path, destination: str | Path) -> bool:
    """Return True when destination is the project root or any child folder."""
    root = safe_resolve(Path(project_root).expanduser())
    target = safe_resolve(Path(destination).expanduser())
    try:
        target.relative_to(root)
        return True
    except ValueError:
        return False


def manifest_artifact_paths(context: ProjectContext) -> list[Path]:
    """Return verified artifact paths recorded in bundle_manifest.json."""
    paths = bundle_artifact_paths(context)
    if not paths.bundle_manifest_json.exists():
        raise ValueError("Bundle manifest is missing: " + str(paths.bundle_manifest_json))

    manifest = load_json_object(paths.bundle_manifest_json)
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
        artifact = resolve_project_artifact(context, relative_path)
        if not artifact.exists():
            if required:
                raise ValueError("Required artifact is missing: " + relative_path)
            continue
        if expected_hash and sha256_file(artifact) != expected_hash:
            raise ValueError("Artifact hash mismatch before ZIP: " + relative_path)
        result.append(artifact)
    return result


def optional_runtime_trace_path(context: ProjectContext) -> Path | None:
    """Return runtime trace path when it exists next to complete.json."""
    paths = bundle_artifact_paths(context)
    complete_json = paths.complete_json
    suffix = "__complete.json"
    if not complete_json.name.endswith(suffix):
        return None
    trace_name = complete_json.name[: -len(suffix)] + _RUNTIME_TRACE_SUFFIX
    trace_path = complete_json.with_name(trace_name)
    if trace_path.exists() and trace_path.is_file():
        return trace_path
    return None


def ordered_export_paths(context: ProjectContext, include_runtime_trace: bool) -> list[Path]:
    """Return handoff artifact paths in stable reading order."""
    required_paths = manifest_artifact_paths(context)
    runtime_trace = optional_runtime_trace_path(context) if include_runtime_trace else None

    def rank(path: Path) -> int:
        name = path.name
        order = [
            "__complete.json",
            _RUNTIME_TRACE_SUFFIX,
            "__exclusion_rules.json",
            "__file_manifest.json",
            "__active_snapshot.json",
            "__validation_state.json",
            _RECONSTRUCTION_SUFFIX,
            "__bundle_manifest.json",
        ]
        for index, suffix in enumerate(order):
            if name.endswith(suffix):
                return index
        return len(order)

    combined = list(required_paths)
    if runtime_trace is not None and runtime_trace not in combined:
        combined.append(runtime_trace)
    return sorted(combined, key=lambda item: (rank(item), item.name))


def timestamp_value(timestamp: str | None) -> str:
    """Return a provided timestamp or current timestamp."""
    if timestamp is None:
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    cleaned = timestamp.strip()
    if not cleaned:
        raise ValueError("timestamp must not be empty")
    return cleaned


def safe_zip_member_name(base_folder: str, path: Path, context: ProjectContext) -> str:
    """Return a ZIP member name scoped under base_folder."""
    relative = relative_posix_path(path, context.root)
    if relative.startswith("../") or relative == "..":
        raise ValueError("ZIP artifact path escapes project root: " + str(path))
    return base_folder + "/" + relative


def external_readme_text(context: ProjectContext, part_size_mb: int) -> str:
    """Return the plain-text external upload README."""
    return "\n".join(
        [
            "Kanda Reasoner JSON handoff export",
            "Project slug: " + context.project_slug,
            "Project root marker: <PROJECT_ROOT>",
            "Target standalone ZIP part size: " + str(part_size_mb) + " MB",
            "",
            "Created packages:",
            "1. " + context.project_slug + "__ai_handoff_upload.zip",
            "   Upload this first to ChatGPT. It contains AI-readable project context.",
            "2. " + context.project_slug + "__ai_handoff_reconstruction.zip",
            "   Upload only when exact active-project reconstruction is needed.",
            "3. " + context.project_slug + "__ai_handoff_all_in_one.zip",
            "   Archive/convenience package containing every handoff artifact.",
            "",
            "If a package is split, upload its part files in numeric order.",
            "Each part is a normal standalone ZIP file.",
            "Excluded folders are intentionally omitted according to Tab 8 project exclusion rules.",
            "No internet or AI service is contacted during ZIP creation.",
            "",
        ]
    )


def package_readme_text(
    context: ProjectContext,
    package_name: str,
    package_purpose: str,
    part_label: str,
    total_parts: int,
    part_size_mb: int,
) -> str:
    """Return the per-package README text stored inside each ZIP."""
    return "\n".join(
        [
            "Kanda Reasoner JSON handoff ZIP package",
            "Project slug: " + context.project_slug,
            "Project root marker: <PROJECT_ROOT>",
            "Package: " + package_name,
            "Purpose: " + package_purpose,
            "Part: " + part_label + " of " + str(total_parts),
            "Target standalone ZIP part size: " + str(part_size_mb) + " MB",
            "",
            "Each part is a normal standalone ZIP file.",
            "Excluded folders are intentionally omitted according to Tab 8 project exclusion rules.",
            "No internet or AI service is contacted during ZIP creation.",
            "",
        ]
    )


def artifact_record(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Return stable metadata for one handoff artifact."""
    return {
        "path": relative_posix_path(path, context.root),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def package_specs(context: ProjectContext, artifacts: list[Path]) -> list[dict[str, Any]]:
    """Return the three handoff package specifications."""
    reconstruction = [path for path in artifacts if path.name.endswith(_RECONSTRUCTION_SUFFIX)]
    if not reconstruction:
        raise ValueError("reconstruction_payload artifact is missing from handoff bundle")

    upload_artifacts = [path for path in artifacts if not path.name.endswith(_RECONSTRUCTION_SUFFIX)]
    return [
        {
            "name": "upload",
            "stem": context.project_slug + "__ai_handoff_upload",
            "purpose": "AI-readable project context for first ChatGPT upload.",
            "artifacts": upload_artifacts,
            "readme_name": "UPLOAD_README.txt",
        },
        {
            "name": "reconstruction",
            "stem": context.project_slug + "__ai_handoff_reconstruction",
            "purpose": "Lossless active-project raw-byte reconstruction payload.",
            "artifacts": reconstruction,
            "readme_name": "RECONSTRUCTION_README.txt",
        },
        {
            "name": "all_in_one",
            "stem": context.project_slug + "__ai_handoff_all_in_one",
            "purpose": "Archive convenience package containing every handoff artifact.",
            "artifacts": artifacts,
            "readme_name": "UPLOAD_README.txt",
        },
    ]
