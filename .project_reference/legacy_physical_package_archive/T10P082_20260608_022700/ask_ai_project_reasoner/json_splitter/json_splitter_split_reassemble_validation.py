"""Validate Project Reasoner JSON split/reassemble output.

This module audits an existing JSON Splitter output folder. It reconstructs the
JSON payload from chunk files in memory, verifies payload hashes, compares the
stable hash to the source hash stored in the split manifest, and checks that the
web-AI route manifest exists.

It does not modify chunk files, the split manifest, the route manifest, or the
canonical complete JSON.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from .json_splitter_split_reassemble_validation_help.core import (
    CHUNK_SCHEMA,
    ROUTE_MANIFEST_SCHEMA,
    stable_hash,
    _load_json,
    _safe_text,
    _safe_int,
    _get_entries,
    _sort_key_for_entry,
    _rebuild_container,
    _set_nested_value,
    _get_nested_value,
    _resolve_source_file,
    _expected_chunk_from_source,
    _expected_coverage_keys,
    _sorted_key_sample,
    _validate_partitions_against_source,
    _find_single_manifest,
    _chunk_value_from_doc,
    _validate_route_manifest,
    _reassemble_from_manifest,
)

__all__ = [
    "CHUNK_SCHEMA",
    "stable_hash",
    "validate_split_reassemble_output",
    "main",
]

def validate_split_reassemble_output(
    split_dir: str | Path,
    manifest_filename: str | None = None,
) -> dict[str, Any]:
    """Validate split output folder and route manifest."""
    split_path = Path(split_dir).resolve()
    if not split_path.exists():
        return {
            "ok": False,
            "message": "Split directory does not exist.",
            "split_dir": str(split_path),
        }

    try:
        manifest_path = (
            split_path / manifest_filename
            if manifest_filename
            else _find_single_manifest(split_path)
        )
        manifest = _load_json(manifest_path)
        if not isinstance(manifest, dict):
            raise ValueError("Split manifest top level must be an object.")

        reconstructed, hash_checks = _reassemble_from_manifest(
            manifest=manifest,
            manifest_dir=manifest_path.parent,
        )

        source_hash = _safe_text(manifest.get("source_sha256", ""))
        reconstructed_hash = stable_hash(reconstructed)
        source_file_path = Path(_safe_text(manifest.get("source_file", "")))
        current_source_hash = ""
        current_source_hash_ok = False
        if source_file_path.exists() and source_file_path.is_file():
            current_source_payload = _load_json(source_file_path)
            current_source_hash = stable_hash(current_source_payload)
            current_source_hash_ok = current_source_hash == source_hash

        route_result = _validate_route_manifest(
            manifest=manifest,
            manifest_dir=manifest_path.parent,
        )
        source_partition_result = _validate_partitions_against_source(
            manifest=manifest,
            manifest_dir=manifest_path.parent,
        )

        payload_hash_failures = [
            item for item in hash_checks if not item.get("ok", False)
        ]
        reconstructed_hash_ok = bool(source_hash and source_hash == reconstructed_hash)
        source_partition_ok = bool(source_partition_result.get("ok", False))
        source_slice_integrity_ok = bool(
            source_partition_result.get("slice_integrity_ok", False)
        )
        strict_coverage_ok = bool(
            source_partition_result.get("strict_coverage_ok", False)
        )
        source_hash_ok = bool(reconstructed_hash_ok or source_partition_ok)

        # A full PASS still requires strict coverage or reconstructed hash. When
        # every emitted chunk matches the source, but strict coverage disagrees,
        # return a diagnostic status instead of hiding details.
        ok = bool(
            source_hash_ok
            and not payload_hash_failures
            and route_result.get("ok", False)
        )
        diagnostic_ok = bool(
            source_slice_integrity_ok
            and not payload_hash_failures
            and route_result.get("ok", False)
            and current_source_hash_ok
        )

        return {
            "ok": ok,
            "diagnostic_ok": diagnostic_ok,
            "message": (
                "Split output is lossless and route manifest is valid."
                if ok
                else (
                    "Chunk hashes and source slices are valid, but strict coverage needs review."
                    if diagnostic_ok
                    else "Split output validation failed."
                )
            ),
            "split_dir": str(split_path),
            "manifest_path": str(manifest_path),
            "part_count": _safe_int(manifest.get("part_count", len(hash_checks))),
            "payload_hash_failure_count": len(payload_hash_failures),
            "source_sha256": source_hash,
            "reconstructed_sha256": reconstructed_hash,
            "source_hash_ok": source_hash_ok,
            "reconstructed_hash_ok": reconstructed_hash_ok,
            "source_partition_ok": source_partition_ok,
            "source_slice_integrity_ok": source_slice_integrity_ok,
            "strict_coverage_ok": strict_coverage_ok,
            "source_partition": source_partition_result,
            "current_source_sha256": current_source_hash,
            "current_source_hash_matches_manifest": current_source_hash_ok,
            "route_manifest": route_result,
        }
    except Exception as exc:
        return {
            "ok": False,
            "message": type(exc).__name__ + ": " + str(exc),
            "split_dir": str(split_path),
        }


def _print_result(result: dict[str, Any]) -> None:
    """Print readable validation result."""
    print("JSON SPLIT REASSEMBLE VALIDATION")
    print("status:", "PASS" if result.get("ok") else "FAIL")
    print("message:", result.get("message", ""))
    print("split_dir:", result.get("split_dir", ""))
    print("manifest_path:", result.get("manifest_path", ""))
    print("part_count:", result.get("part_count", 0))
    print("payload_hash_failure_count:", result.get("payload_hash_failure_count", 0))
    print("source_hash_ok:", result.get("source_hash_ok", False))
    print("reconstructed_hash_ok:", result.get("reconstructed_hash_ok", False))
    print("source_partition_ok:", result.get("source_partition_ok", False))
    print("source_slice_integrity_ok:", result.get("source_slice_integrity_ok", False))
    print("strict_coverage_ok:", result.get("strict_coverage_ok", False))
    print("diagnostic_ok:", result.get("diagnostic_ok", False))
    if result.get("current_source_sha256", ""):
        print(
            "current_source_hash_matches_manifest:",
            result.get("current_source_hash_matches_manifest", False),
        )

    source_partition = result.get("source_partition", {})
    if isinstance(source_partition, dict):
        print("")
        print("source partition validation:")
        print("available:", source_partition.get("available", False))
        print("ok:", source_partition.get("ok", False))
        print("part_mismatch_count:", source_partition.get("part_mismatch_count", 0))
        print(
            "coverage_mismatch_count:",
            source_partition.get("coverage_mismatch_count", 0),
        )
        print("message:", source_partition.get("message", ""))
        examples = source_partition.get("coverage_mismatch_examples", [])
        if examples:
            print("coverage mismatch examples:")
            for item in examples:
                print("- path_parts:", item.get("path_parts", []))
                print("  expected_count:", item.get("expected_count", 0))
                print("  actual_count:", item.get("actual_count", 0))
                print("  missing_count:", item.get("missing_count", 0))
                print("  extra_count:", item.get("extra_count", 0))
                print("  missing_key_sample:", item.get("missing_key_sample", []))
                print("  extra_key_sample:", item.get("extra_key_sample", []))

    route = result.get("route_manifest", {})
    if isinstance(route, dict):
        print("")
        print("web-AI route manifest:")
        print("present:", route.get("present", False))
        print("filename:", route.get("filename", ""))
        print("ok:", route.get("ok", False))
        print("question_route_count:", route.get("question_route_count", 0))
        print("section_count:", route.get("section_count", 0))
        print("message:", route.get("message", ""))


def main(argv: list[str] | None = None) -> int:
    """Run split/reassemble validation CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--split-dir",
        required=True,
        help="Folder containing split chunks and split manifest.",
    )
    parser.add_argument(
        "--manifest-filename",
        default=None,
        help="Optional explicit split manifest filename.",
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Print machine-readable JSON.",
    )
    args = parser.parse_args(argv)

    result = validate_split_reassemble_output(
        split_dir=args.split_dir,
        manifest_filename=args.manifest_filename,
    )

    if args.json_output:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        _print_result(result)

    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
