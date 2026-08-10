# project-path: tools/validate_portable_runtime_allowlist_prompt_family_renewal_v1.py
"""Validate the consolidated Portable prompt-library allowlist renewal."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

FEATURE_ID = "portable-runtime-allowlist-prompt-family-renewal-v1"
EXPECTED = {
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_validate_freeze_error_memory_routine_blueprint.md": {
        "sha256": "f67cce917a22c6351d963672613a3d59fe6735bcebc6b43866d5a9bec658906b",
        "size_bytes": 11253
    },
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md": {
        "sha256": "6442cc9bd5b7e5d9e587489f06d9e5f04ed2cd1c51bf0b9bf9066489069d6e8b",
        "size_bytes": 14778
    },
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_startup_bridge.md": {
        "sha256": "201d158e7367d0974a573f0b836362c419bb34687514be494965eb80c5cdd9cf",
        "size_bytes": 8552
    },
    "kanda_prompt_workspace/prompt_library/METADATA/patch_validate_freeze_error_memory_routine_blueprint.meta.json": {
        "sha256": "eeca0929b4ed1f0c3f9ce778e4cb628dcc956b89243d2a8b2468743e6fd85cf6",
        "size_bytes": 4792
    },
    "kanda_prompt_workspace/prompt_library/ROUTING/PROMPT_NAVIGATION_INDEX.md": {
        "sha256": "bd5dc0b2545b24670d179be116d3e1e5a3df86ddbb3f5297c5ac386c5347ca18",
        "size_bytes": 71281
    },
    "kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json": {
        "sha256": "34f45ddd006a4af27fa5406714ab5b2cc628b44cd39281c6dcf5ee7b7fb35cda",
        "size_bytes": 139496
    }
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    project_root = args.project_root.resolve()
    _require(project_root.is_dir(), "PROJECT_ROOT_MISSING")
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    allowlist_path = project_root / "portable" / "PORTABLE_RUNTIME_ALLOWLIST.json"
    builder_path = project_root / "portable" / "PORTABLE_BUILDER_MANIFEST.json"
    allowlist = json.loads(allowlist_path.read_text(encoding="utf-8-sig"))
    builder = json.loads(builder_path.read_text(encoding="utf-8-sig"))
    items = allowlist.get("items")
    _require(isinstance(items, list), "ALLOWLIST_ITEMS_MISSING")
    by_source = {str(item.get("source_relative")): item for item in items}

    for relative, identity in EXPECTED.items():
        source = project_root / relative
        _require(source.is_file(), "PROMPT_SOURCE_MISSING:" + relative)
        _require(source.stat().st_size == identity["size_bytes"], "PROMPT_SOURCE_SIZE_MISMATCH:" + relative)
        _require(_sha256(source) == identity["sha256"], "PROMPT_SOURCE_SHA256_MISMATCH:" + relative)
        item = by_source.get(relative)
        _require(isinstance(item, dict), "ALLOWLIST_ENTRY_MISSING:" + relative)
        _require(int(item.get("size_bytes", -1)) == identity["size_bytes"], "ALLOWLIST_ENTRY_SIZE_MISMATCH:" + relative)
        _require(str(item.get("sha256", "")) == identity["sha256"], "ALLOWLIST_ENTRY_SHA256_MISMATCH:" + relative)
    print("PORTABLE_PROMPT_FAMILY_CURRENT_SOURCE_IDENTITY: PASS")
    print("PORTABLE_PROMPT_FAMILY_ALLOWLIST_BINDINGS: PASS")

    allowlist_sha = _sha256(allowlist_path)
    _require(builder.get("runtime_allowlist_sha256") == allowlist_sha, "BUILDER_RUNTIME_ALLOWLIST_SHA_MISMATCH")
    _require(builder.get("files", {}).get("PORTABLE_RUNTIME_ALLOWLIST.json") == allowlist_sha, "BUILDER_FILE_ALLOWLIST_SHA_MISMATCH")
    _require(int(builder.get("runtime_allowlist_item_count", -1)) == len(items), "BUILDER_ALLOWLIST_ITEM_COUNT_MISMATCH")
    print("PORTABLE_PROMPT_FAMILY_BUILDER_BINDING: PASS")

    from portable.physical_runtime import validate_runtime_allowlist_sources
    validate_runtime_allowlist_sources(project_root)
    print("PORTABLE_RUNTIME_ALLOWLIST_ALL_SOURCES: PASS")

    external = project_root / "portable" / "PORTABLE_EXTERNAL_BUILD_CONTROLS.json"
    _require(external.is_file(), "EXTERNAL_CONTROL_MANIFEST_MISSING")
    _require(_sha256(external) == "c76d490dc94cc3dd5af0b1b1c3e8014369ad8b849eb262311b86fabd7fd6536a", "EXTERNAL_CONTROL_MANIFEST_CHANGED")
    print("PORTABLE_EXTERNAL_CONTROL_MANIFEST_UNCHANGED: PASS")

    from portable.constants import PRODUCTION_PORTABLE_ENABLED
    _require(PRODUCTION_PORTABLE_ENABLED is False, "PRODUCTION_PORTABLE_GATE_OPEN")
    print("PORTABLE_PRODUCTION_BUILD_GATE_CLOSED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
