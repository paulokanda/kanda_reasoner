"""Generic time, hashing, text, and generated-header helpers."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from startup_kernel.startup_source_map import SourceEntry


__all__ = []


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def date_certificate(dt: datetime) -> str:
    return dt.strftime("%Y%m%d_%H%M%SZ")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_text_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def generated_header(entry: SourceEntry, source_path: Path, workspace_root: Path, generated_at: str, source_hash: str) -> str:
    canonical_relative = entry.canonical_source.replace("\\", "/")
    try:
        resolved_relative = str(source_path.relative_to(workspace_root)).replace("\\", "/")
    except ValueError:
        resolved_relative = str(source_path).replace("\\", "/")
    return (
        "<!---\n"
        "GENERATED FILE - DO NOT EDIT DIRECTLY\n"
        f"Canonical source: {canonical_relative}\n"
        f"Resolved source path: {resolved_relative}\n"
        f"Generated: {generated_at}\n"
        f"SHA-256 source: {source_hash}\n"
        "Edit the canonical source and re-run prompt_tools/sync_startup_routing_kernel_pack.py --sync.\n"
        "--->\n\n"
    )


def _safe_slug_for_delivery(path: Path) -> str:
    raw = str(path.name or "project").strip().lower()
    cleaned = "".join(ch if ch.isalnum() or ch in "_.-" else "_" for ch in raw).strip("._-")
    return cleaned or "project"
