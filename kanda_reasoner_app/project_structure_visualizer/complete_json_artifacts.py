"""Project Structure 3D complete-JSON artifact paths and validation."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_analysis_evidence_root,
)

PROJECT_STRUCTURE_3D_JSON_DIR = "project_structure_3d_json"
PROJECT_STRUCTURE_3D_JSON_BUILDING_DIR = "project_structure_3d_json_building"
PROJECT_STRUCTURE_3D_JSON_PREVIOUS_DIR = "project_structure_3d_json_previous"
PROJECT_STRUCTURE_3D_STATE_DB = "complete_json_index.sqlite3"
COMPLETE_JSON_PART_LIMIT_BYTES = 450 * 1024 * 1024
COMPLETE_JSON_STREAM_ROTATE_BYTES = 400 * 1024 * 1024

__all__ = [
    "COMPLETE_JSON_PART_LIMIT_BYTES",
    "COMPLETE_JSON_STREAM_ROTATE_BYTES",
    "PROJECT_STRUCTURE_3D_JSON_DIR",
    "complete_json_artifact_dir",
    "complete_json_building_dir",
    "complete_json_manifest_path",
    "complete_json_previous_dir",
    "complete_json_state_db_path",
    "inspect_complete_json_artifacts",
]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def complete_json_artifact_dir(project_root: str | Path) -> Path:
    """Return the persistent Project Structure 3D JSON artifact folder."""
    root = Path(project_root).expanduser().resolve(strict=False)
    return project_analysis_evidence_root(root) / PROJECT_STRUCTURE_3D_JSON_DIR


def complete_json_building_dir(project_root: str | Path) -> Path:
    """Return the transactional build folder for a new JSON ZIP family."""
    root = Path(project_root).expanduser().resolve(strict=False)
    return project_analysis_evidence_root(root) / PROJECT_STRUCTURE_3D_JSON_BUILDING_DIR


def complete_json_previous_dir(project_root: str | Path) -> Path:
    """Return the temporary rollback folder used during atomic publication."""
    root = Path(project_root).expanduser().resolve(strict=False)
    return project_analysis_evidence_root(root) / PROJECT_STRUCTURE_3D_JSON_PREVIOUS_DIR


def complete_json_state_db_path(project_root: str | Path) -> Path:
    """Return the disk-backed incremental state database path."""
    root = Path(project_root).expanduser().resolve(strict=False)
    state_root = project_analysis_evidence_root(root) / "project_structure_3d_state"
    return state_root / PROJECT_STRUCTURE_3D_STATE_DB


def complete_json_manifest_path(project_root: str | Path) -> Path:
    """Return the canonical Project Structure 3D complete-JSON manifest path."""
    root = Path(project_root).expanduser().resolve(strict=False)
    return complete_json_artifact_dir(root) / (
        root.name + "__complete_json_manifest.json"
    )


def _load_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Complete JSON manifest must contain an object.")
    return payload


def inspect_complete_json_artifacts(
    project_root: str | Path,
    *,
    verify_hashes: bool = False,
) -> dict[str, Any]:
    """Validate published ZIP metadata, optionally including full SHA-256."""
    root = Path(project_root).expanduser().resolve(strict=False)
    artifact_dir = complete_json_artifact_dir(root)
    manifest_path = complete_json_manifest_path(root)
    result: dict[str, Any] = {
        "exists": False,
        "valid": False,
        "incremental_ready": False,
        "artifact_dir": str(artifact_dir),
        "manifest_path": str(manifest_path),
        "part_count": 0,
        "reason": "missing",
    }
    if not manifest_path.is_file():
        return result
    try:
        manifest = _load_manifest(manifest_path)
        if manifest.get("artifact_type") != "canonical_complete_json_zip_family":
            raise ValueError("Unsupported complete JSON artifact type.")
        if str(manifest.get("project_slug") or "") != root.name:
            raise ValueError("Complete JSON project slug mismatch.")
        parts = manifest.get("parts")
        if not isinstance(parts, list) or not parts:
            raise ValueError("Complete JSON manifest has no ZIP parts.")
        for record in parts:
            if not isinstance(record, dict):
                raise ValueError("Complete JSON part record is invalid.")
            filename = str(record.get("filename") or "")
            if not filename or Path(filename).name != filename:
                raise ValueError("Unsafe complete JSON part filename.")
            part_path = artifact_dir / filename
            if not part_path.is_file():
                raise ValueError("Missing complete JSON ZIP part: " + filename)
            if part_path.stat().st_size != int(record.get("size_bytes") or -1):
                raise ValueError("Complete JSON ZIP size mismatch: " + filename)
            if part_path.stat().st_size > COMPLETE_JSON_PART_LIMIT_BYTES:
                raise ValueError("Complete JSON ZIP exceeds 450 MB: " + filename)
            if verify_hashes and _sha256_file(part_path) != str(record.get("sha256") or ""):
                raise ValueError("Complete JSON ZIP hash mismatch: " + filename)
            member_name = str(record.get("member_name") or "")
            with zipfile.ZipFile(part_path, "r") as archive:
                if archive.namelist() != [member_name]:
                    raise ValueError("Complete JSON ZIP member mismatch: " + filename)
        result.update(
            {
                "exists": True,
                "valid": True,
                "incremental_ready": complete_json_state_db_path(root).is_file(),
                "part_count": len(parts),
                "reason": "ready",
                "manifest": manifest,
            }
        )
    except Exception as exc:
        result.update(
            {
                "exists": True,
                "valid": False,
                "incremental_ready": False,
                "reason": str(exc),
            }
        )
    return result
