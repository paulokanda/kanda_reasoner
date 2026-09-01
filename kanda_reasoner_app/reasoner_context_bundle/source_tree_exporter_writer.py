"""Manifest and top-level source archive writer for Show Project to AI."""

from __future__ import annotations

__all__: list[str] = []


import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

from .json_writer import write_json_atomic
from .schema_models import ProjectContext
from .source_state_identity import build_source_state_identity
from .source_tree_exporter_archive_io import (
    _reuse_previous_png_asset_parts,
    _verify_archive_parts_content,
    _write_archive_groups,
)
from .source_tree_exporter_inventory import (
    _can_reuse_previous_png_assets,
    _load_previous_source_archive_manifest,
    _png_signature_sha256,
    gather_source_archive_inventory,
)
from .source_tree_exporter_planning import (
    _enforce_group_caps,
    _initial_groups,
    _part_filename,
    _png_asset_part_filename,
    _rebalance_tiny_final_group,
)
from .source_tree_exporter_shared import (
    GENERATOR_NAME,
    GENERATOR_VERSION,
    PLANNING_TARGET_RATIO,
    SCHEMA_VERSION,
    _PNG_ASSET_EXTENSIONS,
    _context,
    _split_png_asset_records,
    build_source_archive_manifest_path,
)

def _write_manifest(
    context: ProjectContext,
    destination: Path,
    part_size_mb: int,
    hard_cap: int,
    planning_target: int,
    included_files: list[dict[str, Any]],
    excluded_paths: list[dict[str, Any]],
    part_records: list[dict[str, Any]],
    png_asset_part_records: list[dict[str, Any]],
    source_state: dict[str, Any],
) -> Path:
    manifest_path = build_source_archive_manifest_path(destination, context)
    included_manifest = []
    for record in included_files:
        included_manifest.append(
            {
                "path": record["path"],
                "size_bytes": record["size_bytes"],
                "mtime_ns": record.get("mtime_ns", 0),
                "sha256": record["sha256"],
                "archive_family": record.get("archive_family", "source_archive"),
                "part": record.get("part", 0),
                "part_filename": record.get("part_filename", ""),
            }
        )
    payload = {
        "manifest_version": SCHEMA_VERSION,
        "bundle_kind": "source_archive_manifest",
        "generator": {"name": GENERATOR_NAME, "version": GENERATOR_VERSION},
        "generated_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "project": {
            "project_slug": context.project_slug,
            "active_project_id": context.active_project_id,
            "active_project_root_fingerprint": context.active_project_root_fingerprint,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
            "dynamic_output_contract": "<project_drive>:\\<project_slug>_show_project_to_AI\\second_prompt_files",
        },
        "source_state": source_state,
        "source_state_contract": {
            "canonical_owner": "source_archive_inventory",
            "this_manifest_owns_archive_projection_identity": True,
            "archive_members_verified_against_inventory": True,
            "publication_requires_projection_binding_to_file_manifest": True,
        },
        "archive_contract": {
            "selected_size_cap_mb": part_size_mb,
            "selected_size_cap_bytes": hard_cap,
            "planning_target_ratio": PLANNING_TARGET_RATIO,
            "planning_target_bytes": planning_target,
            "compression_method": "ZIP_DEFLATED",
            "compresslevel": 9,
            "parts_are_standalone_zip_files": True,
            "file_level_packing_only": True,
            "byte_chunking_allowed": False,
            "chunk_manifest_allowed": False,
            "chunks_folder_allowed": False,
        },
        "png_asset_archive_contract": {
            "enabled": True,
            "extensions": sorted(_PNG_ASSET_EXTENSIONS),
            "selected_size_cap_mb": part_size_mb,
            "selected_size_cap_bytes": hard_cap,
            "compression_method": "ZIP_STORED",
            "compresslevel": None,
            "parts_are_standalone_zip_files": True,
            "file_level_packing_only": True,
            "split_if_over_selected_size_cap": True,
            "reuse_if_signature_unchanged": True,
            "no_png_files_creates_no_png_zip": True,
            "signature_fields": [
                "path",
                "size_bytes",
                "mtime_ns",
                "sha256",
            ],
            "content_signature_fields": ["path", "size_bytes", "sha256"],
            "content_signature_sha256": _png_signature_sha256(included_files),
            "fast_reuse_identity_fields": [
                "filename",
                "actual_size_bytes",
                "file_mtime_ns",
            ],
            "fallback_verification": "sha256_and_full_crc",
            "preferred_reuse_method": "same_volume_hardlink",
        },
        "counts": {
            "included_files": len(included_manifest),
            "excluded_paths": len(excluded_paths),
            "archive_parts": len(part_records),
            "png_asset_archive_parts": len(png_asset_part_records),
            "png_asset_files": sum(1 for item in included_manifest if item.get("archive_family") == "png_assets"),
            "total_included_source_bytes": sum(int(item.get("size_bytes", 0)) for item in included_manifest),
            "total_archive_bytes": sum(int(item.get("actual_size_bytes", 0)) for item in part_records),
            "total_png_asset_archive_bytes": sum(int(item.get("actual_size_bytes", 0)) for item in png_asset_part_records),
        },
        "parts": part_records,
        "png_asset_parts": png_asset_part_records,
        "included_files": included_manifest,
        "excluded_paths": excluded_paths,
        "reconstruction_instructions": (
            "Extract every standalone source_archive_part ZIP into the same empty target directory. "
            "Then extract every standalone png_assets_part ZIP into that same target directory. "
            "The merged tree reconstructs exactly the manifest included_files set."
        ),
    }
    return write_json_atomic(manifest_path, payload)

def write_source_archive_parts(
    project: str | Path | ProjectContext,
    destination: str | Path,
    temp_root: str | Path,
    *,
    part_size_mb: int,
    part_size_bytes: int,
    reuse_png_assets_from: str | Path | None = None,
) -> dict[str, Any]:
    """Write standalone source archive ZIP parts for the selected project root.

    The source archive always uses the selected project root from ``project``.
    The Kanda Reasoner app may be the tool executing this function, but it is
    never assumed to be the project being exported.
    """
    context = _context(project)
    destination_path = Path(destination).expanduser().resolve(strict=False)
    temp_path = Path(temp_root).expanduser().resolve(strict=False)
    destination_path.mkdir(parents=True, exist_ok=True)
    temp_path.mkdir(parents=True, exist_ok=True)
    hard_cap = int(part_size_bytes)
    planning_target = int(hard_cap * PLANNING_TARGET_RATIO)
    if hard_cap <= 0:
        raise ValueError("part_size_bytes must be positive")
    if planning_target <= 0:
        planning_target = hard_cap

    previous_manifest = _load_previous_source_archive_manifest(reuse_png_assets_from, context)
    inventory = gather_source_archive_inventory(context, destination_path, previous_manifest)
    included_files: list[dict[str, Any]] = list(inventory["included_files"])
    excluded_paths: list[dict[str, Any]] = list(inventory["excluded_paths"])
    source_state = build_source_state_identity(
        included_files,
        hash_field="sha256",
    )
    if source_state.get("identity_status") != "VERIFIED":
        raise RuntimeError("SOURCE_ARCHIVE_STATE_UNVERIFIABLE")

    source_files, png_asset_files = _split_png_asset_records(included_files)

    source_groups = _initial_groups(
        source_files,
        hard_cap,
        planning_target,
        temp_path,
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    )
    source_groups = _enforce_group_caps(
        source_groups,
        hard_cap,
        temp_path,
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    )
    source_groups = _rebalance_tiny_final_group(
        source_groups,
        hard_cap,
        temp_path,
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    )
    source_groups = _enforce_group_caps(
        source_groups,
        hard_cap,
        temp_path,
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    )

    png_reuse_allowed = _can_reuse_previous_png_assets(
        context=context,
        previous_output_dir=reuse_png_assets_from,
        previous_manifest=previous_manifest,
        png_asset_files=png_asset_files,
        part_size_mb=part_size_mb,
        hard_cap=hard_cap,
    )
    png_groups: list[list[dict[str, Any]]] = []
    if not png_reuse_allowed:
        png_groups = _initial_groups(
            png_asset_files,
            hard_cap,
            hard_cap,
            temp_path,
            compression=zipfile.ZIP_STORED,
            compresslevel=None,
        )
        png_groups = _enforce_group_caps(
            png_groups,
            hard_cap,
            temp_path,
            compression=zipfile.ZIP_STORED,
            compresslevel=None,
        )

    created_paths: list[Path] = []
    part_records, source_created_paths = _write_archive_groups(
        context=context,
        destination_path=destination_path,
        temp_path=temp_path,
        groups=source_groups,
        hard_cap=hard_cap,
        filename_builder=_part_filename,
        archive_family="source_archive",
        package_name="Source archive",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    )
    created_paths.extend(source_created_paths)

    if png_reuse_allowed and reuse_png_assets_from is not None and previous_manifest is not None:
        (
            png_asset_part_records,
            png_created_paths,
            png_assets_reuse_method,
        ) = _reuse_previous_png_asset_parts(
            context=context,
            destination_path=destination_path,
            previous_output_dir=reuse_png_assets_from,
            previous_manifest=previous_manifest,
            png_asset_files=png_asset_files,
        )
        png_assets_reused = True
    else:
        png_asset_part_records, png_created_paths = _write_archive_groups(
            context=context,
            destination_path=destination_path,
            temp_path=temp_path,
            groups=png_groups,
            hard_cap=hard_cap,
            filename_builder=_png_asset_part_filename,
            archive_family="png_assets",
            package_name="PNG asset archive",
            compression=zipfile.ZIP_STORED,
            compresslevel=None,
        )
        png_assets_reused = False
        png_assets_reuse_method = "created"
    created_paths.extend(png_created_paths)

    _verify_archive_parts_content(
        destination_path,
        part_records + png_asset_part_records,
        included_files,
    )

    manifest_path = _write_manifest(
        context,
        destination_path,
        part_size_mb,
        hard_cap,
        planning_target,
        included_files,
        excluded_paths,
        part_records,
        png_asset_part_records,
        source_state,
    )
    created_paths.append(manifest_path)

    source_zip_parts = [
        {
            "package": "source_archive",
            "filename": item["filename"],
            "path": item["path"],
            "size_bytes": item["actual_size_bytes"],
            "sha256": item["sha256"],
            "artifact_count": item["file_count"],
            "artifacts": [],
            "source_archive_part": True,
        }
        for item in part_records
    ]
    png_zip_parts = [
        {
            "package": "png_assets",
            "filename": item["filename"],
            "path": item["path"],
            "size_bytes": item["actual_size_bytes"],
            "sha256": item["sha256"],
            "artifact_count": item["file_count"],
            "artifacts": [],
            "png_asset_part": True,
        }
        for item in png_asset_part_records
    ]
    return {
        "ok": True,
        "project_slug": context.project_slug,
        "manifest_path": str(manifest_path),
        "created_paths": created_paths,
        "zip_parts": source_zip_parts + png_zip_parts,
        "source_zip_parts": source_zip_parts,
        "png_asset_zip_parts": png_zip_parts,
        "part_records": part_records,
        "png_asset_part_records": png_asset_part_records,
        "png_assets_reused": png_assets_reused,
        "png_assets_reuse_method": png_assets_reuse_method,
        "source_state": source_state,
        "warnings": [],
    }
