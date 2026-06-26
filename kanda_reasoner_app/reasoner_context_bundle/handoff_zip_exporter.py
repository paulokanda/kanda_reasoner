"""Standalone multi-profile ZIP export for JSON handoff artifacts.

The exporter writes ChatGPT-friendly standalone ZIP files from the generated
JSON bundle. Destination folders inside the active project root are rejected so
exports do not become active project content.
"""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import os
from pathlib import Path
from typing import Any

from .bundle_checker import check_ai_context_bundle
from .handoff_zip_exporter_support import (
    _BYTES_PER_MB,
    _EXPORT_GENERATOR,
    _EXPORT_GENERATOR_VERSION,
    _EXPORT_KIND,
    _is_destination_inside_project_root,
    context_from_project,
    ordered_export_paths,
    package_specs,
    timestamp_value,
)
from .handoff_zip_exporter_writer import write_external_readme, write_package_parts
from .source_archive_exporter import write_source_archive_parts
from .schema_models import ProjectContext

DEFAULT_PART_SIZE_MB = 500
EXTENDED_PART_SIZE_MB_OPTIONS = (100, 200, 300, 400, 500)
ALLOWED_PART_SIZE_MB_OPTIONS = EXTENDED_PART_SIZE_MB_OPTIONS

__all__ = [
    "DEFAULT_PART_SIZE_MB",
    "EXTENDED_PART_SIZE_MB_OPTIONS",
    "ALLOWED_PART_SIZE_MB_OPTIONS",
    "export_json_handoff_zip_parts",
    "is_destination_inside_project_root",
    "main",
]


def _part_size_error(context: ProjectContext, message: str) -> dict[str, Any]:
    return {
        "ok": False,
        "kind": _EXPORT_KIND,
        "project_slug": context.project_slug,
        "failures": [message],
    }


def is_destination_inside_project_root(project_root: str | Path, destination: str | Path) -> bool:
    """Return True when destination is the project root or any child folder."""
    return _is_destination_inside_project_root(project_root, destination)


def _validate_destination(context: ProjectContext, destination: Path) -> dict[str, Any] | None:
    if not destination.exists() or not destination.is_dir():
        return _part_size_error(context, "Destination folder does not exist: " + str(destination))
    if is_destination_inside_project_root(context.root, destination):
        return _part_size_error(
            context,
            "Destination folder is inside the active project root. "
            "Choose a folder outside: " + str(context.root),
        )
    return None


def _resolve_part_size(
    context: ProjectContext,
    part_size_mb: int,
    part_size_bytes: int | None,
) -> tuple[int | None, dict[str, Any] | None]:
    if part_size_bytes is None:
        if part_size_mb not in ALLOWED_PART_SIZE_MB_OPTIONS:
            return None, _part_size_error(
                context,
                "part_size_mb must be one of " + ", ".join(str(item) for item in ALLOWED_PART_SIZE_MB_OPTIONS),
            )
        part_size_bytes = part_size_mb * _BYTES_PER_MB
    if part_size_bytes <= 0:
        return None, _part_size_error(context, "part_size_bytes must be positive")
    return int(part_size_bytes), None


def _check_bundle_if_requested(context: ProjectContext, check_bundle: bool) -> dict[str, Any] | None:
    if not check_bundle:
        return None
    check_result = check_ai_context_bundle(context)
    if bool(check_result.get("ok", False)):
        return None
    failures = check_result.get("failures", [])
    if not isinstance(failures, list):
        failures = ["Unknown bundle checker failure"]
    return {
        "ok": False,
        "kind": _EXPORT_KIND,
        "project_slug": context.project_slug,
        "failures": [str(item) for item in failures],
        "check_result": check_result,
    }


def _cleanup_created_paths(created_paths: list[Path]) -> None:
    for created_path in created_paths:
        try:
            created_path.unlink()
        except Exception:
            pass


def _retarget_path_string(value: Any, stage: Path, destination: Path) -> Any:
    if not isinstance(value, str):
        return value
    stage_text = str(stage)
    dest_text = str(destination)
    return value.replace(stage_text, dest_text).replace(
        stage_text.replace("\\", "/"), dest_text.replace("\\", "/")
    )


def _retarget_record_paths(value: Any, stage: Path, destination: Path) -> Any:
    if isinstance(value, dict):
        return {key: _retarget_record_paths(item, stage, destination) for key, item in value.items()}
    if isinstance(value, list):
        return [_retarget_record_paths(item, stage, destination) for item in value]
    return _retarget_path_string(value, stage, destination)


def _publish_stage_outputs(stage: Path, destination: Path) -> list[Path]:
    published: list[Path] = []
    destination.mkdir(parents=True, exist_ok=True)
    for child in sorted(stage.iterdir(), key=lambda item: item.name.lower()):
        target = destination / child.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.move(str(child), str(target))
        published.append(target)
    return published


def _assert_no_forbidden_outputs(output_dir: Path) -> None:
    forbidden_names = {"CHUNK_MANIFEST.json", "json_splitted"}
    for child in output_dir.rglob("*"):
        if child.name in forbidden_names or child.name == "chunks":
            raise ValueError("Forbidden legacy split artifact generated: " + str(child))
        if child.name.endswith("__reconstruction_payload.json"):
            raise ValueError("Forbidden normal reconstruction payload generated: " + str(child))



def _delivery_folder_for_metadata(destination: Path) -> Path:
    """Return the final public folder to write inside artifact metadata."""
    if destination.name == "second_prompt_files_building":
        return destination.with_name("second_prompt_files")
    return destination


def _previous_second_prompt_files_for_reuse(destination: Path) -> Path:
    """Return the selected project's previous final second_prompt_files folder.

    Show Project to AI may build new artifacts in a temporary sibling named
    ``second_prompt_files_building``.  Reusable artifact families, such as
    PNG assets, must be read from the same selected project's previously
    published ``second_prompt_files`` folder, not from the tool installation
    and not from a hard-coded project name.
    """
    if destination.name == "second_prompt_files_building":
        return destination.with_name("second_prompt_files")
    return destination


def _rewrite_text_references(folder: Path, delivery_folder: Path) -> int:
    """Rewrite build/stage folder references to the public delivery folder."""
    replacements = (
        (str(folder), str(delivery_folder)),
        (str(folder).replace("\\", "/"), str(delivery_folder).replace("\\", "/")),
        ("show_project_to_AI/second_prompt_files_building", "show_project_to_AI/second_prompt_files"),
        ("show_project_to_AI\\second_prompt_files_building", "show_project_to_AI\\second_prompt_files"),
        ("second_prompt_files_building", "second_prompt_files"),
    )
    changed = 0
    if not folder.exists():
        return changed
    for path in folder.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".txt", ".md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        original = text
        for old, new in replacements:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def _finalize_ai_context_artifacts_for_handoff(context: ProjectContext, destination: Path) -> None:
    """Refresh JSON artifacts before they are copied into upload ZIPs.

    The GUI builds in ``second_prompt_files_building`` and publishes later.
    Upload ZIPs are created before that publish step, so this function rewrites
    metadata to the final delivery folder and refreshes the mutually linked
    briefing/manifest pair before packaging.
    """
    from .ai_briefing_builder import write_ai_briefing_json
    from .bundle_manifest_builder import write_bundle_manifest_json

    delivery_folder = _delivery_folder_for_metadata(destination)
    _rewrite_text_references(destination, delivery_folder)
    write_ai_briefing_json(context)
    _rewrite_text_references(destination, delivery_folder)
    write_bundle_manifest_json(context)
    _rewrite_text_references(destination, delivery_folder)
    write_ai_briefing_json(context)
    _rewrite_text_references(destination, delivery_folder)
    write_bundle_manifest_json(context)
    _rewrite_text_references(destination, delivery_folder)

def export_json_handoff_zip_parts(
    project: str | Path | ProjectContext,
    destination_folder: str | Path,
    *,
    part_size_mb: int = DEFAULT_PART_SIZE_MB,
    part_size_bytes: int | None = None,
    timestamp: str | None = None,
    include_runtime_trace: bool = False,
    check_bundle: bool = True,
) -> dict[str, Any]:
    """Export lightweight JSON map artifacts plus source archive ZIP parts.

    Normal hybrid export must not upload or require the old heavy
    complete/active-snapshot JSON artifacts. Exact reconstruction is provided
    by standalone source_archive_part ZIPs and source_archive_manifest.json.
    """
    context = context_from_project(project)
    destination = Path(destination_folder).expanduser()
    destination_error = _validate_destination(context, destination)
    if destination_error is not None:
        return destination_error

    resolved_part_size_bytes, size_error = _resolve_part_size(context, part_size_mb, part_size_bytes)
    if size_error is not None:
        return size_error
    if resolved_part_size_bytes is None:
        return _part_size_error(context, "part_size_bytes resolution failed")

    bundle_error = _check_bundle_if_requested(context, check_bundle)
    if bundle_error is not None:
        return bundle_error

    temp_parent = destination.parent if destination.parent != Path("") else destination
    temp_root = Path(tempfile.mkdtemp(prefix=".json_handoff_zip_work_", dir=str(temp_parent)))
    output_stage = Path(tempfile.mkdtemp(prefix=".json_handoff_zip_stage_", dir=str(temp_parent)))
    created_paths: list[Path] = []
    try:
        timestamp_value(timestamp)
        warnings: list[str] = []
        zip_records: list[dict[str, Any]] = []
        packages: list[dict[str, Any]] = []
        error_memory_export_result: dict[str, Any] = {
            "ok": False,
            "status": "not_attempted",
            "reason": "Error Memory export has not run yet.",
        }

        previous_reuse_folder = _previous_second_prompt_files_for_reuse(destination)
        source_archive = write_source_archive_parts(
            context,
            output_stage,
            temp_root,
            part_size_mb=part_size_mb,
            part_size_bytes=resolved_part_size_bytes,
            reuse_png_assets_from=previous_reuse_folder,
        )
        created_paths.extend(Path(str(path)) for path in source_archive.get("created_paths", []))
        source_manifest_path = Path(str(source_archive.get("manifest_path", "")))
        source_zip_records = list(source_archive.get("source_zip_parts", []))
        if not source_zip_records:
            source_zip_records = [
                item
                for item in list(source_archive.get("zip_parts", []))
                if str(item.get("package", "")) == "source_archive"
            ]
        png_asset_zip_records = list(source_archive.get("png_asset_zip_parts", []))
        zip_records.extend(source_zip_records)
        zip_records.extend(png_asset_zip_records)
        packages.append(
            {
                "name": "source_archive",
                "stem": context.project_slug + "__source_archive",
                "purpose": "Exact non-PNG source-tree reconstruction as standalone ZIP parts for the selected Project root.",
                "zip_count": len(source_zip_records),
                "artifact_count": sum(int(item.get("artifact_count", 0)) for item in source_zip_records),
                "zip_parts": source_zip_records,
            }
        )
        if png_asset_zip_records:
            packages.append(
                {
                    "name": "png_assets",
                    "stem": context.project_slug + "__png_assets",
                    "purpose": "Exact PNG asset reconstruction as standalone ZIP_STORED parts for the selected Project root.",
                    "zip_count": len(png_asset_zip_records),
                    "artifact_count": sum(int(item.get("artifact_count", 0)) for item in png_asset_zip_records),
                    "zip_parts": png_asset_zip_records,
                }
            )

        _finalize_ai_context_artifacts_for_handoff(context, destination)
        artifacts = ordered_export_paths(context, include_runtime_trace)
        if source_manifest_path.exists():
            artifacts.append(source_manifest_path)

        # Error Memory canon: compact files are always included in the main
        # AI-readable upload package, while the full Error Memory ZIP is
        # generated as a separate sibling in second_prompt_files and opened
        # only when needed.
        try:
            from kanda_reasoner_app.error_memory.exporter import (
                write_error_memory_ai_send_files,
            )

            error_memory_export_result = write_error_memory_ai_send_files(context.root, destination)
            error_memory_export_result["status"] = "included"
            error_memory_export_result["compact_files_in_upload_package"] = []
            error_memory_export_result["full_zip_policy"] = "sibling_file_open_only_when_needed"
            for key in ("compact_json", "prompt_md", "manifest_json"):
                value = str(error_memory_export_result.get(key, "") or "")
                if value:
                    candidate = Path(value)
                    if candidate.exists() and candidate.is_file():
                        artifacts.append(candidate)
                        error_memory_export_result["compact_files_in_upload_package"].append(candidate.name)
            full_zip = str(error_memory_export_result.get("full_zip", "") or "")
            if full_zip:
                full_zip_path = Path(full_zip)
                error_memory_export_result["full_zip_name"] = full_zip_path.name
                error_memory_export_result["full_zip_in_upload_package"] = False
                created_paths.append(full_zip_path)
        except Exception as exc:
            error_memory_export_result = {
                "ok": False,
                "status": "skipped",
                "reason": str(exc),
            }
            warnings.append("Error Memory export skipped: " + str(exc))

        specs = package_specs(context, artifacts)

        for spec in specs:
            records, package_warnings, package_paths = write_package_parts(
                spec,
                context,
                output_stage,
                temp_root,
                part_size_mb,
                resolved_part_size_bytes,
            )
            created_paths.extend(package_paths)
            warnings.extend(package_warnings)
            zip_records.extend(records)
            packages.append(
                {
                    "name": spec["name"],
                    "stem": spec["stem"],
                    "purpose": spec["purpose"],
                    "zip_count": len(records),
                    "artifact_count": sum(int(item.get("artifact_count", 0)) for item in records),
                    "zip_parts": records,
                }
            )

        readme_file = write_external_readme(output_stage, context, part_size_mb)
        _assert_no_forbidden_outputs(output_stage)
        published_paths = _publish_stage_outputs(output_stage, destination)
        retargeted_packages = _retarget_record_paths(packages, output_stage, destination)
        retargeted_zip_records = _retarget_record_paths(zip_records, output_stage, destination)
        retargeted_readme = _retarget_record_paths(readme_file, output_stage, destination)
        return {
            "ok": True,
            "kind": _EXPORT_KIND,
            "generator": {"name": _EXPORT_GENERATOR, "version": _EXPORT_GENERATOR_VERSION},
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "destination_folder": str(destination),
            "part_size_mb": part_size_mb,
            "part_size_bytes": resolved_part_size_bytes,
            "zip_count": len(zip_records),
            "artifact_count": len(artifacts),
            "package_count": len(packages),
            "packages": retargeted_packages,
            "zip_parts": retargeted_zip_records,
            "readme_file": retargeted_readme,
            "published_paths": [str(path) for path in published_paths],
            "error_memory_export": _retarget_record_paths(error_memory_export_result, output_stage, destination),
            "warnings": warnings,
            "failures": [],
        }
    except Exception as exc:
        _cleanup_created_paths(created_paths)
        return {
            "ok": False,
            "kind": _EXPORT_KIND,
            "project_slug": context.project_slug,
            "failures": [str(exc)],
        }
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)
        shutil.rmtree(output_stage, ignore_errors=True)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export JSON handoff artifacts as ZIP profiles.")
    parser.add_argument("--root", required=True, help="Active project root.")
    parser.add_argument("--destination", required=True, help="Destination folder outside project root.")
    parser.add_argument("--part-size-mb", type=int, choices=list(ALLOWED_PART_SIZE_MB_OPTIONS), default=DEFAULT_PART_SIZE_MB)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--no-runtime-trace", action="store_true")
    parser.add_argument("--no-check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    result = export_json_handoff_zip_parts(
        args.root,
        args.destination,
        part_size_mb=int(args.part_size_mb),
        timestamp=args.timestamp,
        include_runtime_trace=not bool(args.no_runtime_trace),
        check_bundle=not bool(args.no_check),
    )
    indent = None if bool(args.compact) else 2
    print(json.dumps(result, indent=indent, ensure_ascii=True), flush=True)
    return 0 if bool(result.get("ok", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
