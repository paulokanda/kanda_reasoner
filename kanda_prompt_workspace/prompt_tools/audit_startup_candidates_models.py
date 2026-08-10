"""Data models and shared constants for startup prompt candidate audits."""

from __future__ import annotations
__all__: list[str] = []


import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any



TOOLS_DIR_NAME = "prompt_tools"
PROMPT_LIBRARY_DIR_NAME = "prompt_library"
SOURCE_MAP_FILENAME = "STARTUP_ROUTING_KERNEL_SOURCES.json"
REPORT_FILENAME = "STARTUP_ROUTING_KERNEL_SOURCES_UPDATE_CANDIDATE.md"
SYNC_SCRIPT_FILENAME = "sync_startup_routing_kernel_pack.py"

ALLOWED_SCAN_DIRS = (
    "prompt_library/ACTIVE_PROMPTS",
    "prompt_library/ROUTING",
)

MAX_CANDIDATE_SIZE_BYTES = 100 * 1024
MAX_NEW_CANDIDATES_WARNING = 5
MAX_STARTUP_SOURCES_WARNING = 20

GENERATED_FILENAME_RE = re.compile(r"^[0-9]{2}_[^\\/]+\.md$")
PROMPT_ID_RE = re.compile(r"^[a-z0-9_]+$")

REQUIRED_SOURCE_MAP_KEYS = {
    "load_order",
    "canonical_source",
    "generated_filename",
    "prompt_id",
    "load_mode",
    "role",
}

ALLOWED_SOURCE_MAP_KEYS = REQUIRED_SOURCE_MAP_KEYS

REQUIRED_SIDECAR_KEYS = {
    "startup_kernel_include",
    "startup_load_mode",
    "startup_generated_filename",
    "prompt_id",
    "startup_role",
}

ALLOWED_SIDECAR_KEYS = REQUIRED_SIDECAR_KEYS | {"canonical_source", "load_order"}


@dataclass(frozen=True)
class SourceMapEntry:
    load_order: int
    canonical_source: str
    generated_filename: str
    prompt_id: str
    load_mode: str
    role: str
    raw: dict[str, Any]
@dataclass(frozen=True)
class StartupCandidate:
    canonical_source: str
    generated_filename: str
    prompt_id: str
    load_mode: str
    role: str
    md_path: Path
    sidecar_path: Path
    size_bytes: int
    optional_load_order: int | None
@dataclass
class AuditResult:
    source_map_errors: list[str]
    source_map_warnings: list[str]
    sidecar_warnings: list[str]
    candidate_errors: list[str]
    candidate_warnings: list[str]
    stale_entries: list[str]
    existing_candidates: list[StartupCandidate]
    missing_candidates: list[StartupCandidate]
    ignored_sidecars: list[str]
    source_map_sha256: str
    report_path: Path

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
def read_text_utf8_strict(path: Path) -> str:
    # Accept UTF-8 with or without BOM. Windows PowerShell 5.1 and
    # some editors can write UTF-8 files with a BOM; that is still
    # valid UTF-8 for this workflow and should not break JSON parsing.
    return path.read_text(encoding="utf-8-sig")
def write_text_utf8(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")
def read_json_file(path: Path) -> Any:
    return json.loads(read_text_utf8_strict(path))
def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
