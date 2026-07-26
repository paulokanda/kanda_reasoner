"""Prompt-library payload file selection and fingerprint helpers."""

from __future__ import annotations

import json
from pathlib import Path

from startup_kernel.constants import PROMPT_LIBRARY_ROOT_DIR_NAME
from startup_kernel.core_helpers import sha256_bytes, sha256_file


__all__ = [
    "iter_prompt_library_payload_files",
    "prompt_library_source_fingerprint",
]


def _is_prompt_library_payload_file(path: Path) -> bool:
    """Return True when a prompt_library file should be packaged for AI lookup.

    The on-demand prompt-library ZIP must contain canonical prompt sources and
    metadata only. It must not recursively carry generated ZIPs, historical
    bundle scratch folders, bytecode, or backup/temp files because those stale
    artifacts can reintroduce obsolete startup names into fresh AI sessions.
    """
    if not path.is_file():
        return False
    parts = {part.lower() for part in path.parts}
    if "__pycache__" in parts or "_bundle_temp" in parts:
        return False
    if path.name.lower() in {".ds_store", "thumbs.db"}:
        return False
    if path.suffix.lower() in {".zip", ".pyc", ".pyo", ".tmp", ".bak"}:
        return False
    return True


def iter_prompt_library_payload_files(workspace_root: Path) -> list[Path]:
    """List canonical prompt_library files included in prompt_library.zip."""
    library_root = workspace_root / PROMPT_LIBRARY_ROOT_DIR_NAME
    if not library_root.is_dir():
        raise FileNotFoundError("prompt_library folder not found: " + str(library_root))
    return sorted(
        path for path in library_root.rglob("*")
        if _is_prompt_library_payload_file(path)
    )


def _prompt_library_relpath(workspace_root: Path, path: Path) -> str:
    library_root = workspace_root / PROMPT_LIBRARY_ROOT_DIR_NAME
    return str(path.relative_to(library_root)).replace("\\", "/")


def prompt_library_source_fingerprint(workspace_root: Path) -> str:
    """Return a stable fingerprint for the canonical prompt_library source tree."""
    records = []
    for path in iter_prompt_library_payload_files(workspace_root):
        records.append({
            "path": _prompt_library_relpath(workspace_root, path),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })
    payload = json.dumps(records, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return sha256_bytes(payload)
