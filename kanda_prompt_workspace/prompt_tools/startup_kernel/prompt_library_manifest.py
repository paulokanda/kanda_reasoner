"""Prompt-library ZIP manifest and metadata catalog helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from startup_kernel.constants import (
    PROMPT_LIBRARY_ROOT_DIR_NAME,
    PROMPT_LIBRARY_ZIP_NAME,
    SCRIPT_NAME,
    TOOLS_DIR_NAME,
)
from startup_kernel.core_helpers import sha256_file
from startup_kernel.prompt_library_payload import (
    _prompt_library_relpath,
    iter_prompt_library_payload_files,
    prompt_library_source_fingerprint,
)


__all__ = [
    "build_prompt_library_manifest",
]


def _load_prompt_metadata_entries(workspace_root: Path) -> list[dict[str, Any]]:
    """Read prompt metadata into a compact address catalog for prompt_library.zip."""
    metadata_root = workspace_root / PROMPT_LIBRARY_ROOT_DIR_NAME / "METADATA"
    entries: list[dict[str, Any]] = []
    if not metadata_root.is_dir():
        return entries

    for meta_path in sorted(metadata_root.glob("*.json")):
        try:
            raw = json.loads(meta_path.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if not isinstance(raw, dict):
            continue
        entry = {
            "prompt_code": str(raw.get("prompt_code") or ""),
            "prompt_id": str(raw.get("prompt_id") or raw.get("id") or meta_path.stem),
            "title": str(raw.get("title") or raw.get("display_name") or ""),
            "load_type": str(raw.get("load_type") or raw.get("status") or ""),
            "folder": str(raw.get("folder") or raw.get("category") or ""),
            "path": str(raw.get("path") or raw.get("canonical_path") or "").replace("\\", "/"),
            "metadata_path": "METADATA/" + meta_path.name,
        }
        entries.append(entry)
    return entries


def build_prompt_library_manifest(workspace_root: Path, generated_at: str, date_cert: str) -> dict[str, Any]:
    """Build the prompt_library.zip manifest from the canonical prompt tree."""
    files = iter_prompt_library_payload_files(workspace_root)
    file_records = []
    for path in files:
        file_records.append({
            "path": _prompt_library_relpath(workspace_root, path),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })

    return {
        "manifest_version": "1.0",
        "kind": "prompt_library_zip_manifest",
        "zip_filename": PROMPT_LIBRARY_ZIP_NAME,
        "generated_at": generated_at,
        "date_certificate": date_cert,
        "generated_by": f"{TOOLS_DIR_NAME}/{SCRIPT_NAME}",
        "archive_root_rule": "Paths inside this ZIP are relative to kanda_prompt_workspace/prompt_library; use ACTIVE_PROMPTS/<folder>/<prompt>.md addresses directly.",
        "usage_rule": "Do not read every prompt at startup. Use startup routing/index files to select an address, then open only the selected prompt file from this ZIP when needed.",
        "source_fingerprint": prompt_library_source_fingerprint(workspace_root),
        "file_count": len(file_records),
        "files": file_records,
        "prompt_entries": _load_prompt_metadata_entries(workspace_root),
    }
