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
from .schema_models import ProjectContext

DEFAULT_PART_SIZE_MB = 40
CONSERVATIVE_PART_SIZE_MB = 25

__all__ = [
    "DEFAULT_PART_SIZE_MB",
    "CONSERVATIVE_PART_SIZE_MB",
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
        if part_size_mb not in (CONSERVATIVE_PART_SIZE_MB, DEFAULT_PART_SIZE_MB):
            return None, _part_size_error(context, "part_size_mb must be 25 or 40")
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


def export_json_handoff_zip_parts(
    project: str | Path | ProjectContext,
    destination_folder: str | Path,
    *,
    part_size_mb: int = DEFAULT_PART_SIZE_MB,
    part_size_bytes: int | None = None,
    timestamp: str | None = None,
    include_runtime_trace: bool = True,
    check_bundle: bool = True,
) -> dict[str, Any]:
    """Export generated JSON handoff artifacts as three ZIP profiles plus TXT README."""
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

    temp_root = Path(tempfile.mkdtemp(prefix="json_handoff_zip_export_", dir=str(destination)))
    created_paths: list[Path] = []
    try:
        timestamp_value(timestamp)
        artifacts = ordered_export_paths(context, include_runtime_trace)
        specs = package_specs(context, artifacts)
        warnings: list[str] = []
        zip_records: list[dict[str, Any]] = []
        packages: list[dict[str, Any]] = []

        for spec in specs:
            records, package_warnings, package_paths = write_package_parts(
                spec,
                context,
                destination,
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
            "packages": packages,
            "zip_parts": zip_records,
            "readme_file": write_external_readme(destination, context, part_size_mb),
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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export JSON handoff artifacts as ZIP profiles.")
    parser.add_argument("--root", required=True, help="Active project root.")
    parser.add_argument("--destination", required=True, help="Destination folder outside project root.")
    parser.add_argument("--part-size-mb", type=int, choices=[25, 40], default=DEFAULT_PART_SIZE_MB)
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
