# project-path: kanda_prompt_workspace/prompt_tools/startup_kernel/prompt_library_zip.py
"""Prompt-library ZIP creation and validation compatibility surface."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

from startup_kernel.constants import (
    PROMPT_LIBRARY_MANIFEST_FILENAME,
    PROMPT_LIBRARY_ROOT_DIR_NAME,
    PROMPT_LIBRARY_ZIP_NAME,
    READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME,
    STARTUP_ARTIFACT_READ_ORDER_MARKER,
)
from startup_kernel.prompt_library_manifest import (
    _load_prompt_metadata_entries,
    build_prompt_library_manifest,
)
from startup_kernel.prompt_library_payload import (
    _is_prompt_library_payload_file,
    _prompt_library_relpath,
    iter_prompt_library_payload_files,
    prompt_library_source_fingerprint,
)
from startup_kernel.read_order import make_startup_artifact_read_order_notice

# Public ownership for payload and manifest helpers stays in their source modules.
# This compatibility module keeps explicit imports available, but only owns the
# ZIP creation and ZIP validation public surface.
__all__ = [
    "make_prompt_library_zip",
    "validate_prompt_library_zip_contract",
]


def make_prompt_library_zip(workspace_root: Path, output_dir: Path, generated_at: str, date_cert: str) -> Path:
    """Create first_prompt_files/prompt_library.zip for on-demand AI prompt retrieval."""
    library_root = workspace_root / PROMPT_LIBRARY_ROOT_DIR_NAME
    if not library_root.is_dir():
        raise FileNotFoundError("prompt_library folder not found: " + str(library_root))

    zip_path = output_dir / PROMPT_LIBRARY_ZIP_NAME
    files = iter_prompt_library_payload_files(workspace_root)
    manifest = build_prompt_library_manifest(workspace_root, generated_at, date_cert)
    manifest_bytes = json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(
            READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME,
            make_startup_artifact_read_order_notice(PROMPT_LIBRARY_ZIP_NAME).encode("utf-8"),
        )
        for path in files:
            z.write(path, arcname=_prompt_library_relpath(workspace_root, path))
        z.writestr(PROMPT_LIBRARY_MANIFEST_FILENAME, manifest_bytes)

    validate_prompt_library_zip_contract(zip_path, workspace_root)
    return zip_path


def validate_prompt_library_zip_contract(zip_path: Path, workspace_root: Path | None = None) -> None:
    """Validate prompt_library.zip contains direct-addressable prompt sources."""
    with zipfile.ZipFile(zip_path, "r") as z:
        names = set(z.namelist())
        required = {
            PROMPT_LIBRARY_MANIFEST_FILENAME,
            "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
            "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md",
            "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/chatgpt_kanda_routing_choice_output_protocol.md",
            READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME,
        }

        missing = sorted(required - names)
        if missing:
            raise ValueError("prompt_library.zip is missing required files: " + str(missing))
        if any(name.startswith("prompt_library/") for name in names):
            raise ValueError("prompt_library.zip must use direct roots such as ACTIVE_PROMPTS/, not prompt_library/ACTIVE_PROMPTS/.")
        notice_text = z.read(READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME).decode("utf-8-sig")
        if STARTUP_ARTIFACT_READ_ORDER_MARKER not in notice_text:
            raise ValueError("prompt_library.zip read-order notice is missing the tell_AI first instruction.")
        manifest = json.loads(z.read(PROMPT_LIBRARY_MANIFEST_FILENAME).decode("utf-8-sig"))

    if manifest.get("kind") != "prompt_library_zip_manifest":
        raise ValueError("prompt_library.zip manifest kind must be prompt_library_zip_manifest.")
    if not manifest.get("source_fingerprint"):
        raise ValueError("prompt_library.zip manifest is missing source_fingerprint.")
    if not isinstance(manifest.get("prompt_entries"), list):
        raise ValueError("prompt_library.zip manifest prompt_entries must be a list.")
    if workspace_root is not None:
        expected = prompt_library_source_fingerprint(workspace_root)
        if manifest.get("source_fingerprint") != expected:
            raise ValueError("prompt_library.zip source_fingerprint is stale.")
