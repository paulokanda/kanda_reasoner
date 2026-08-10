"""Hybrid source-tree export for Show Project to AI.

This module owns the public compatibility contract for exact project
reconstruction export. Runtime/source logic lives in cohesive helper modules
under :mod:`kanda_reasoner_app.reasoner_context_bundle`.
"""

from __future__ import annotations

from .source_tree_exporter_inventory import (
    gather_source_archive_inventory as _gather_source_archive_inventory,
)
from .source_tree_exporter_shared import (
    SOURCE_ARCHIVE_MANIFEST_SUFFIX as _SOURCE_ARCHIVE_MANIFEST_SUFFIX,
    build_source_archive_manifest_path as _build_source_archive_manifest_path,
)
from .source_tree_exporter_writer import write_source_archive_parts as _write_source_archive_parts

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
