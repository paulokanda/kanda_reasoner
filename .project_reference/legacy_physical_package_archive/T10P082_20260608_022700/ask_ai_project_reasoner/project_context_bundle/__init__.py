"""Closed-box helpers for additive AI context bundle generation.

This package is intentionally project-agnostic. It resolves paths from the
active project root and writes companion JSON artifacts without changing the
existing complete JSON contract.
"""

from __future__ import annotations

from .exclusion_engine import decide_path_exclusion
from .exclusion_provider import load_bundle_exclusion_rules
from .exclusion_rules_exporter import (
    build_exclusion_rules_payload,
    write_exclusion_rules_json,
)
from .active_snapshot_builder import (
    SNAPSHOT_TEXT_EXTENSIONS,
    build_active_snapshot_payload,
    write_active_snapshot_json,
)
from .file_manifest_builder import (
    GENERATED_EVIDENCE_PREFIXES,
    TEXT_FILE_EXTENSIONS,
    build_file_manifest_payload,
    iter_active_project_files,
    write_file_manifest_json,
)

from .reconstruction_payload_builder import (
    build_reconstruction_payload,
    write_reconstruction_payload_json,
)

from .validation_state_builder import (
    DEFAULT_VALIDATION_COMMANDS,
    build_validation_state_payload,
    run_validation_commands,
    write_validation_state_json,
)

from .bundle_manifest_builder import (
    BUNDLE_ARTIFACT_ORDER,
    build_bundle_manifest_payload,
    write_bundle_manifest_json,
)
from .bundle_checker import (
    check_ai_context_bundle,
    raise_for_ai_context_bundle_errors,
)
from .bundle_orchestrator import generate_ai_context_bundle
from .bundle_zipper import zip_ai_context_bundle

from .handoff_zip_exporter import (
    CONSERVATIVE_PART_SIZE_MB,
    DEFAULT_PART_SIZE_MB,
    export_json_handoff_zip_parts,
    is_destination_inside_project_root,
)
from .cli import main as run_project_context_bundle_cli
from .hashing import sha256_bytes, sha256_file, sha256_text_normalized
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .path_normalization import relative_posix_path, safe_resolve, to_posix_path
from .project_context import resolve_project_context
from .schema_models import (
    BundleArtifactPaths,
    ExclusionDecision,
    ExclusionRules,
    ProjectContext,
)

__all__ = [
    "run_project_context_bundle_cli",
    "generate_ai_context_bundle",
    "zip_ai_context_bundle",
    "export_json_handoff_zip_parts",
    "is_destination_inside_project_root",
    "DEFAULT_PART_SIZE_MB",
    "CONSERVATIVE_PART_SIZE_MB",
    "SNAPSHOT_TEXT_EXTENSIONS",
    "TEXT_FILE_EXTENSIONS",
    "GENERATED_EVIDENCE_PREFIXES",
    "DEFAULT_VALIDATION_COMMANDS",
    "run_validation_commands",
    "raise_for_ai_context_bundle_errors",
    "check_ai_context_bundle",
    "write_bundle_manifest_json",
    "build_bundle_manifest_payload",
    "BUNDLE_ARTIFACT_ORDER",
    "build_reconstruction_payload",
    "write_reconstruction_payload_json",
    "build_validation_state_payload",
    "write_validation_state_json",
    "BundleArtifactPaths",
    "ExclusionDecision",
    "ExclusionRules",
    "ProjectContext",
    "build_exclusion_rules_payload",
    "build_active_snapshot_payload",
    "build_file_manifest_payload",
    "bundle_artifact_paths",
    "decide_path_exclusion",
    "relative_posix_path",
    "iter_active_project_files",
    "load_bundle_exclusion_rules",
    "resolve_project_context",
    "safe_resolve",
    "sha256_bytes",
    "sha256_file",
    "sha256_text_normalized",
    "to_posix_path",
    "write_exclusion_rules_json",
    "write_active_snapshot_json",
    "write_file_manifest_json",
    "write_json_atomic",
]
