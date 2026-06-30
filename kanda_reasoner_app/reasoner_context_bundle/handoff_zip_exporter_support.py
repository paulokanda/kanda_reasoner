# project-path: kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter_support.py
"""Internal support helpers for JSON handoff ZIP export."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .hashing import sha256_file
from .output_paths import bundle_artifact_paths
from .path_normalization import artifact_logical_posix_path, resolve_logical_artifact_path, safe_resolve
from .project_context import resolve_project_context
from .schema_models import ProjectContext

_EXPORT_KIND = "json_handoff_zip_parts"
_EXPORT_GENERATOR = "reasoner_context_bundle.handoff_zip_exporter"
_EXPORT_GENERATOR_VERSION = "2.2.0"
_DEFAULT_PART_SIZE_MB = 500
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
    """Resolve a bundle artifact path from project or architecture-audit roots."""
    return resolve_logical_artifact_path(context, relative_path)


def _final_delivery_logical_path(logical_path: str) -> str:
    """Return a stable final-delivery logical path for handoff members."""
    text = logical_path.replace("\\", "/")
    text = text.replace(
        "show_project_to_AI/second_prompt_files_building/",
        "show_project_to_AI/second_prompt_files/",
    )
    if "/.json_handoff_zip_stage_" in text:
        return "show_project_to_AI/second_prompt_files/" + Path(text).name
    if "/.json_handoff_zip_work_" in text:
        return "show_project_to_AI/second_prompt_files/" + Path(text).name
    return text


def _handoff_artifact_logical_path(path: Path, context: ProjectContext) -> str:
    """Return a final-delivery logical path for handoff artifacts.

    ZIPs are often assembled while artifacts live in ``second_prompt_files_building``
    or in a temporary staging folder.  The delivered ZIP must never expose those
    transactional paths.  It always reports members under the final
    ``show_project_to_AI/second_prompt_files`` contract.
    """
    try:
        return _final_delivery_logical_path(artifact_logical_posix_path(path, context))
    except ValueError:
        return "show_project_to_AI/second_prompt_files/" + path.name


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
            "__exclusion_rules.json",
            "__file_manifest.json",
            "__validation_state.json",
            "__bundle_manifest.json",
        ]
        for index, suffix in enumerate(order):
            if name.endswith(suffix):
                return index
        return len(order)

    forbidden_suffixes = ("__complete.json", "__active_snapshot.json", "__reconstruction_payload.json")
    combined = [path for path in required_paths if not path.name.endswith(forbidden_suffixes)]
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
    relative = _handoff_artifact_logical_path(path, context)
    if relative.startswith("../") or relative == ".." or Path(relative).is_absolute():
        raise ValueError("ZIP artifact path escapes allowed roots: " + str(path))
    return base_folder + "/" + relative


def external_readme_text(context: ProjectContext, part_size_mb: int) -> str:
    """Return the plain-text external upload README."""
    slug = context.project_slug
    return "\n".join(
        [
            "Kanda Reasoner second upload group - read this first",
            "Project slug: " + slug,
            "Project root marker: <PROJECT_ROOT>",
            "Target standalone ZIP part size: " + str(part_size_mb) + " MB",
            "The AI-readable JSON handoff is delivered as ZIP package(s) that respect the selected Show Project to AI size cap.",
            "Loose JSON files are packaged into the JSON handoff ZIP and are normally removed from second_prompt_files after successful ZIP export.",
            "",
            "Second-upload reading order:",
            "1. _RUN_COLLECTOR_STATUS.txt, if present, to confirm generation status.",
            "2. " + slug + "__ai_handoff_upload_readme.txt, this file.",
            "3. Read compact Error Memory files when present: " + slug + "__error_memory_ai_prompt.md, " + slug + "__error_lessons_compact.json, and " + slug + "__error_memory_manifest.json.",
            "4. " + slug + "__ai_handoff_upload*.zip, in numeric order if split. This is the zipped JSON handoff package and includes compact Error Memory files.",
            "5. Inside the JSON handoff ZIP, read UPLOAD_README.txt first, then ai_briefing, routing_manifest, bundle_manifest, patch_safety_routes, file_manifest, source_archive_manifest, validation_state, and compact Error Memory files.",
            "6. " + slug + "__error_memory_full.zip is always generated separately; open it only when compact Error Memory says full context is needed, repeated-error debugging is the task, or the user asks for Error Memory audit.",
            "7. " + slug + "__source_archive_partXX_of_YY.zip only when exact source inspection or reconstruction is needed. Use source_archive_manifest to choose needed parts.",
            "8. " + slug + "__png_assets_partXX_of_YY.zip when exact reconstruction needs PNG assets. These are ZIP_STORED asset parts listed in source_archive_manifest.",
            "9. " + slug + "__ai_handoff_all_in_one*.zip only as convenience/archive fallback if the upload ZIP package is missing.",
            "",
            "Created package families:",
            "1. " + slug + "__ai_handoff_upload*.zip",
            "   Upload/read this JSON handoff package before source archive parts. It may be split to respect the selected size cap.",
            "2. " + slug + "__source_archive_partXX_of_YY.zip",
            "   Upload only when exact source-tree reconstruction is needed.",
            "3. " + slug + "__png_assets_partXX_of_YY.zip",
            "   Upload with source_archive parts when exact source-tree reconstruction needs PNG assets; parts use ZIP_STORED and split by the selected size cap.",
            "4. " + slug + "__error_memory_full.zip",
            "   Full project Error Memory archive. Always generated; open only when needed.",
            "5. " + slug + "__ai_handoff_all_in_one*.zip",
            "   Archive/convenience package containing AI-readable handoff artifacts, not nested source ZIPs.",
            "",
            "Each part is a normal standalone ZIP file. Source archive and PNG asset parts are independent ZIPs with disjoint file subsets.",
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
            "Kanda Reasoner AI handoff ZIP package",
            "Project slug: " + context.project_slug,
            "Project root marker: <PROJECT_ROOT>",
            "Package: " + package_name,
            "Purpose: " + package_purpose,
            "Part: " + part_label + " of " + str(total_parts),
            "Target standalone ZIP part size: " + str(part_size_mb) + " MB",
            "",
            "Each part is a normal standalone ZIP file.",
            "If this package is split, read/upload parts in numeric order.",
            "For ai_handoff_upload packages, read UPLOAD_README.txt first, then ai_briefing, routing_manifest, bundle_manifest, patch_safety_routes, file_manifest, source_archive_manifest, validation_state, and compact Error Memory files when present.",
            "The separate full Error Memory ZIP should be opened only when compact lessons are insufficient or the task is repeated-error debugging.",
            "Source archive and PNG asset part ZIPs should be opened only when exact source inspection or reconstruction is needed.",
            "Excluded folders are intentionally omitted according to Tab 8 project exclusion rules.",
            "No internet or AI service is contacted during ZIP creation.",
            "",
        ]
    )


def artifact_record(path: Path, context: ProjectContext) -> dict[str, Any]:
    """Return stable metadata for one handoff artifact."""
    return {
        "path": _handoff_artifact_logical_path(path, context),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def package_specs(context: ProjectContext, artifacts: list[Path]) -> list[dict[str, Any]]:
    """Return AI-readable handoff package specifications.

    Exact source reconstruction is exported separately as standalone source
    archive ZIP parts plus a source_archive_manifest JSON file.  Do not place
    source archive ZIPs inside these AI context packages.
    """
    return [
        {
            "name": "upload",
            "stem": context.project_slug + "__ai_handoff_upload",
            "purpose": "AI-readable project context plus source-archive manifest for first ChatGPT upload.",
            "artifacts": artifacts,
            "readme_name": "UPLOAD_README.txt",
        },
        {
            "name": "all_in_one",
            "stem": context.project_slug + "__ai_handoff_all_in_one",
            "purpose": "Archive convenience package containing AI-readable handoff artifacts and source-archive manifest.",
            "artifacts": artifacts,
            "readme_name": "UPLOAD_README.txt",
        },
    ]
