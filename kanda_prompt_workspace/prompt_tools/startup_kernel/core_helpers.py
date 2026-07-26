"""Core startup delivery path and status helpers.

This module remains the public compatibility surface for helpers that were
historically exported by sync_startup_routing_kernel_pack.py.  Pure generic
helpers and source-map resolution now live in focused modules, but are
re-exported here so existing imports keep working.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from startup_kernel.constants import (
    FIRST_PROMPT_FILES_DIR_NAME,
    LEGACY_MODIFY_STARTUP_DELIVERY_FILENAME,
    LEGACY_PASTE_AFTER_FIRST_PROMPTS_FILENAME,
    MODIFY_STARTUP_DELIVERY_FILENAME,
    OLD_PASTE_AFTER_UPLOAD_FILENAME,
    PASTE_AFTER_UPLOAD_FILENAME,
    SourceEntry,
)
from startup_kernel.generic_helpers import (
    _safe_slug_for_delivery,
    date_certificate,
    generated_header,
    now_utc,
    read_text_utf8,
    sha256_bytes,
    sha256_file,
)
from startup_kernel.source_resolution import load_source_map, resolve_source

__all__ = [
    "clean_delivery_folder",
    "collect_status",
    "date_certificate",
    "default_first_prompt_output_dir",
    "detect_workspace_root",
    "generated_header",
    "load_source_map",
    "now_utc",
    "read_text_utf8",
    "resolve_source",
    "sha256_bytes",
    "sha256_file",
]


def detect_workspace_root(script_path: Path, explicit_workspace: Path | None) -> Path:
    """Return the prompt workspace root containing prompt_library/.

    The startup generator can be launched through the thin public entrypoint in
    prompt_tools or through helper modules inside prompt_tools/startup_kernel.
    After the train-car refactor, looking only one or two parents above
    __file__ is not enough. Walk upward from both the script path and current
    working directory so the helper package does not mistake startup_kernel for
    the workspace root.
    """
    if explicit_workspace is not None:
        return explicit_workspace.expanduser().resolve(strict=False)

    candidates: list[Path] = []
    anchors = [script_path.expanduser().resolve(strict=False), Path.cwd().resolve(strict=False)]
    for anchor in anchors:
        start = anchor if anchor.is_dir() else anchor.parent
        for candidate in (start, *start.parents):
            if candidate not in candidates:
                candidates.append(candidate)

    for candidate in candidates:
        if (candidate / "prompt_library").exists():
            return candidate.resolve(strict=False)
    return script_path.parent.resolve(strict=False)


def default_first_prompt_output_dir(active_project_root: Path) -> Path:
    """Return <project_drive>/<project>_show_project_to_AI/first_prompt_files."""
    root = Path(active_project_root).expanduser().resolve(strict=False)
    anchor = root.anchor or str(root.parent)
    slug = _safe_slug_for_delivery(root)
    if anchor.endswith(":\\") or anchor.endswith(":/"):
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    elif anchor.endswith(":"):
        base = Path(f"{anchor}\\{slug}_show_project_to_AI")
    else:
        base = Path(anchor) / f"{slug}_show_project_to_AI"
    return base / FIRST_PROMPT_FILES_DIR_NAME


def collect_status(workspace_root: Path, entries: list[SourceEntry]) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    for entry in entries:
        source_path, resolution = resolve_source(workspace_root, entry)
        record: dict[str, Any] = {
            "load_order": entry.load_order,
            "prompt_id": entry.prompt_id,
            "load_mode": entry.load_mode,
            "role": entry.role,
            "canonical_source": entry.canonical_source,
            "generated_filename": entry.generated_filename,
            "resolution": resolution,
            "exists": source_path is not None,
        }
        if source_path is None:
            failures.append(f"{entry.generated_filename}: {resolution} ({entry.canonical_source})")
        else:
            try:
                resolved_source = str(source_path.relative_to(workspace_root)).replace("\\", "/")
            except ValueError:
                resolved_source = str(source_path)
            record["resolved_source"] = resolved_source
            record["canonical_sha256_current"] = sha256_file(source_path)
            record["size_bytes"] = source_path.stat().st_size
        records.append(record)
    return records, failures


def clean_delivery_folder(output_dir: Path) -> None:
    """Clear approved first_prompt_files or remove legacy generated files only."""
    if not output_dir.exists():
        return
    resolved_dir = output_dir.expanduser().resolve(strict=False)
    if (
        resolved_dir.name == FIRST_PROMPT_FILES_DIR_NAME
        and resolved_dir.parent.name.endswith("_show_project_to_AI")
    ):
        for child in list(resolved_dir.iterdir()):
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        return
    patterns = [
        "first_prompts_to_ai*.zip",
        "prompt_library*.zip",
        "startup_prompt_request_kernel_upload_pack*.zip",
        "send" + "_this_first__CERT_" + "*.md",  # obsolete pre-rename boot command files
        "send_ai" + "_just_if_modify" + "_startup_delivery.md",  # obsolete pre-rename maintenance file
        PASTE_AFTER_UPLOAD_FILENAME,
        OLD_PASTE_AFTER_UPLOAD_FILENAME,
        LEGACY_PASTE_AFTER_FIRST_PROMPTS_FILENAME,
        LEGACY_MODIFY_STARTUP_DELIVERY_FILENAME,
        MODIFY_STARTUP_DELIVERY_FILENAME,
    ]
    for pattern in patterns:
        for path in output_dir.glob(pattern):
            if path.is_file():
                path.unlink()
