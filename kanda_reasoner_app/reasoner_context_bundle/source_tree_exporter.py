"""Hybrid source-tree export for Show Project to AI.

This module owns the public compatibility contract for exact project
reconstruction export. Runtime/source logic lives in cohesive helper modules
under :mod:`kanda_reasoner_app.reasoner_context_bundle`.
"""

from __future__ import annotations

from .source_tree_exporter_archive_io import (
    _reuse_previous_png_asset_parts,
    _write_archive_groups,
    _write_zip,
)
from .source_tree_exporter_inventory import (
    _can_reuse_previous_png_assets,
    _current_png_signature,
    _excluded_by_builtin_policy,
    _file_record,
    _iter_sorted_entries,
    _load_previous_source_archive_manifest,
    _previous_png_record_map,
    _previous_png_signature,
    gather_source_archive_inventory as _gather_source_archive_inventory,
)
from .source_tree_exporter_planning import (
    _candidate_zip_size,
    _enforce_group_caps,
    _estimate_record_size,
    _initial_groups,
    _part_filename,
    _png_asset_part_filename,
    _rebalance_tiny_final_group,
    _single_record_fits,
)
from .source_tree_exporter_shared import (
    GENERATOR_NAME,
    GENERATOR_VERSION,
    PLANNING_TARGET_RATIO,
    SCHEMA_VERSION,
    SOURCE_ARCHIVE_MANIFEST_SUFFIX as _SOURCE_ARCHIVE_MANIFEST_SUFFIX,
    _ALWAYS_EXCLUDED_DIRS,
    _ALWAYS_EXCLUDED_EXTENSIONS,
    _ALWAYS_EXCLUDED_FILES,
    _BYTES_PER_MB,
    _GENERATED_OUTPUT_NAMES,
    _PNG_ASSET_EXTENSIONS,
    _REBALANCE_LAST_PART_MIN_RATIO,
    _REBALANCE_PREVIOUS_PART_MIN_RATIO,
    _ZIP_OVERHEAD_ESTIMATE_BYTES,
    _context,
    _excluded_by_project_rules,
    _exclusion_record,
    _is_generated_output_path,
    _is_generated_project_archive,
    _is_path_same_or_inside,
    _is_png_asset_record,
    _posix_rel,
    _split_png_asset_records,
    build_source_archive_manifest_path as _build_source_archive_manifest_path,
)
from .source_tree_exporter_writer import _write_manifest, write_source_archive_parts as _write_source_archive_parts

SOURCE_ARCHIVE_MANIFEST_SUFFIX = _SOURCE_ARCHIVE_MANIFEST_SUFFIX
build_source_archive_manifest_path = _build_source_archive_manifest_path
gather_source_archive_inventory = _gather_source_archive_inventory
write_source_archive_parts = _write_source_archive_parts

__all__ = [
    "SOURCE_ARCHIVE_MANIFEST_SUFFIX",
    "build_source_archive_manifest_path",
    "gather_source_archive_inventory",
    "write_source_archive_parts",
]
