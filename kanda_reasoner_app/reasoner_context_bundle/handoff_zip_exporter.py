# project-path: kanda_reasoner_app/reasoner_context_bundle/handoff_zip_exporter.py
"""Standalone ZIP export for JSON handoff artifacts.

The exporter writes ChatGPT-friendly standalone ZIP files from the generated
JSON bundle. Destination folders inside the active project root are rejected so
exports do not become active project content.
"""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .file_manifest_builder import build_file_manifest_payload
from .handoff_zip_exporter_paths_private import (
    _assert_no_forbidden_outputs,
    _cleanup_created_paths,
    _finalize_ai_context_artifacts_for_handoff,
    _previous_second_prompt_files_for_reuse,
    _publish_stage_outputs,
    _remove_obsolete_all_in_one_outputs,
    _retarget_record_paths,
)
from .handoff_zip_exporter_validation_private import (
    _check_bundle_if_requested,
    _part_size_error,
    _resolve_part_size,
    _validate_destination,
)
from .handoff_zip_exporter_support import (
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
from .source_tree_exporter import write_source_archive_parts
from .schema_models import ProjectContext
from .output_paths import bundle_artifact_paths
from .source_state_identity import (
    load_source_state_identity,
    require_archive_projection_matches_file_manifest,
    require_matching_source_states,
    source_state_from_payload,
)

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




def is_destination_inside_project_root(project_root: str | Path, destination: str | Path) -> bool:
    """Return True when destination is the project root or any child folder."""
    return _is_destination_inside_project_root(project_root, destination)





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

    Normal hybrid export never creates, uploads, or requires the heavy
    complete/active-snapshot JSON artifacts. Exact reconstruction is provided
    by standalone source_archive_part ZIPs and source_archive_manifest.json.
    """
    context = context_from_project(project)
    destination = Path(destination_folder).expanduser()
    destination_error = _validate_destination(context, destination)
    if destination_error is not None:
        return destination_error

    resolved_part_size_bytes, size_error = _resolve_part_size(context, part_size_mb, part_size_bytes, ALLOWED_PART_SIZE_MB_OPTIONS)
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
            "ok": True,
            "status": "tool_owned_separate_workflow",
            "reason": (
                "Reusable Error Memory is Tool-owned and is supplied "
                "separately from the Project handoff workflow."
            ),
            "compact_files_in_upload_package": [],
            "full_zip_policy": "tool_owned_separate_workflow",
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
        archive_state = dict(source_archive.get("source_state", {}))
        file_manifest_state: dict[str, Any] = {}
        if archive_state:
            bundle_paths = bundle_artifact_paths(context)
            file_manifest_state = load_source_state_identity(
                bundle_paths.file_manifest_json
            )
            source_manifest_state = load_source_state_identity(source_manifest_path)
            bundle_manifest_state = load_source_state_identity(
                bundle_paths.bundle_manifest_json
            )
            require_matching_source_states(
                archive_state,
                source_manifest_state,
                expected_label="source_archive_inventory",
                observed_label="source_archive_manifest",
            )
            require_matching_source_states(
                file_manifest_state,
                bundle_manifest_state,
                expected_label="file_manifest",
                observed_label="bundle_manifest",
            )
            file_manifest_payload = json.loads(
                bundle_paths.file_manifest_json.read_text(encoding="utf-8-sig")
            )
            source_manifest_payload = json.loads(
                source_manifest_path.read_text(encoding="utf-8-sig")
            )
            require_archive_projection_matches_file_manifest(
                list(file_manifest_payload.get("files", [])),
                list(source_manifest_payload.get("included_files", [])),
            )
        elif check_bundle:
            raise RuntimeError("SOURCE_ARCHIVE_STATE_MISSING")

        artifacts = ordered_export_paths(context, include_runtime_trace)
        if source_manifest_path.exists():
            artifacts.append(source_manifest_path)

        # Reusable Error Memory is Tool-owned. Show Project exports only
        # Project handoff/source artifacts; Tool Error Memory is supplied by
        # the separate Error Memory workflow when an AI session needs it.

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

        if archive_state:
            live_payload = build_file_manifest_payload(context)
            live_state = source_state_from_payload(live_payload)
            require_matching_source_states(
                file_manifest_state,
                live_state,
                expected_label="handoff_snapshot",
                observed_label="live_source_before_publish",
            )

        removed_obsolete_outputs = _remove_obsolete_all_in_one_outputs(
            destination,
            context.project_slug,
        )
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
            "png_assets_reused": bool(source_archive.get("png_assets_reused", False)),
            "png_assets_reuse_method": str(
                source_archive.get("png_assets_reuse_method", "")
            ),
            "source_state": file_manifest_state,
            "source_archive_state": archive_state,
            "source_archive_projection_status": (
                "VERIFIED_SUBSET" if archive_state else "NOT_AVAILABLE"
            ),
            "source_state_status": (
                "FRESH_AT_PUBLICATION" if archive_state else "NOT_AVAILABLE"
            ),
            "packages": retargeted_packages,
            "zip_parts": retargeted_zip_records,
            "readme_file": retargeted_readme,
            "published_paths": [str(path) for path in published_paths],
            "removed_obsolete_outputs": [
                str(path) for path in removed_obsolete_outputs
            ],
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
    """Support build parser behavior.
    
    Returns
    -------
    argparse.ArgumentParser
        The argument parser result.
    """
    
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
    """Support main behavior.
    
    Parameters
    ----------
    argv : list[str] | None, optional
        The optional argv value.
    
    Returns
    -------
    int
        The integer status code.
    """
    
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
