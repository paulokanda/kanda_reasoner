"""Validate the exact Portable runtime allowlist renewal for one prompt."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

FEATURE_ID = "portable-runtime-allowlist-prompt-binding-v1"
TARGET_RELATIVE = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "patch_validate_freeze_error_memory_routine_blueprint.md"
)
EXPECTED_ROLE = "prompt_library"
EXPECTED_ARCHIVE_RELATIVE = "_internal/" + TARGET_RELATIVE
EXPECTED_PROMPT_SIZE = 11253
EXPECTED_PROMPT_SHA256 = (
    "f67cce917a22c6351d963672613a3d59fe6735bcebc6b43866d5a9bec658906b"
)
EXPECTED_ALLOWLIST_SHA256 = (
    "5b906e1beba9b055ce23a78a3848c76ff620540fb15eab978cbde561a15d8127"
)
EXPECTED_EXTERNAL_CONTROL_MANIFEST_SHA256 = (
    "c76d490dc94cc3dd5af0b1b1c3e8014369ad8b849eb262311b86fabd7fd6536a"
)


def require(condition: bool, code: str) -> None:
    """Raise one stable validation error when a contract is not met."""
    if not condition:
        raise RuntimeError(code)


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for one file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    """Load one JSON object from disk."""
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON_ROOT_NOT_OBJECT:" + str(path))
    return value


def validate(root: Path) -> None:
    """Validate the renewed prompt binding and dependent manifests."""
    root = root.resolve()
    sys.dont_write_bytecode = True
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    prompt_path = root / TARGET_RELATIVE
    allowlist_path = root / "portable" / "PORTABLE_RUNTIME_ALLOWLIST.json"
    builder_path = root / "portable" / "PORTABLE_BUILDER_MANIFEST.json"
    external_path = root / "portable" / "PORTABLE_EXTERNAL_BUILD_CONTROLS.json"

    require(prompt_path.is_file(), "TARGET_PROMPT_MISSING")
    require(allowlist_path.is_file(), "RUNTIME_ALLOWLIST_MISSING")
    require(builder_path.is_file(), "BUILDER_MANIFEST_MISSING")
    require(external_path.is_file(), "EXTERNAL_CONTROL_MANIFEST_MISSING")

    prompt_size = prompt_path.stat().st_size
    prompt_sha256 = sha256_file(prompt_path)
    require(prompt_size == EXPECTED_PROMPT_SIZE, "TARGET_PROMPT_SIZE_UNEXPECTED")
    require(prompt_sha256 == EXPECTED_PROMPT_SHA256, "TARGET_PROMPT_SHA256_UNEXPECTED")

    allowlist = load_json(allowlist_path)
    items = allowlist.get("items")
    require(isinstance(items, list), "RUNTIME_ALLOWLIST_ITEMS_MISSING")
    matches = [
        item
        for item in items
        if isinstance(item, dict)
        and item.get("source_relative") == TARGET_RELATIVE
    ]
    require(len(matches) == 1, "TARGET_ALLOWLIST_MATCH_COUNT_NOT_ONE")
    entry = matches[0]
    require(entry.get("archive_relative") == EXPECTED_ARCHIVE_RELATIVE,
            "TARGET_ARCHIVE_PATH_MISMATCH")
    require(entry.get("role") == EXPECTED_ROLE, "TARGET_ROLE_MISMATCH")
    require(int(entry.get("size_bytes", -1)) == prompt_size,
            "TARGET_ALLOWLIST_SIZE_MISMATCH")
    require(str(entry.get("sha256", "")) == prompt_sha256,
            "TARGET_ALLOWLIST_SHA256_MISMATCH")
    require(int(allowlist.get("item_count", -1)) == len(items),
            "RUNTIME_ALLOWLIST_ITEM_COUNT_MISMATCH")

    allowlist_sha256 = sha256_file(allowlist_path)
    require(allowlist_sha256 == EXPECTED_ALLOWLIST_SHA256,
            "RUNTIME_ALLOWLIST_SHA256_UNEXPECTED")

    builder = load_json(builder_path)
    files = builder.get("files")
    require(isinstance(files, dict), "BUILDER_FILE_HASH_MAP_MISSING")
    require(builder.get("runtime_allowlist_sha256") == allowlist_sha256,
            "BUILDER_RUNTIME_ALLOWLIST_HASH_MISMATCH")
    require(files.get("PORTABLE_RUNTIME_ALLOWLIST.json") == allowlist_sha256,
            "BUILDER_MEMBER_ALLOWLIST_HASH_MISMATCH")
    require(int(builder.get("runtime_allowlist_item_count", -1)) == len(items),
            "BUILDER_RUNTIME_ALLOWLIST_COUNT_MISMATCH")
    require(builder.get("production_portable_enabled") is False,
            "PORTABLE_PRODUCTION_GATE_OPEN")

    require(sha256_file(external_path) == EXPECTED_EXTERNAL_CONTROL_MANIFEST_SHA256,
            "EXTERNAL_CONTROL_MANIFEST_CHANGED")

    print("PORTABLE_PROMPT_CURRENT_SOURCE_IDENTITY: PASS")
    print("PORTABLE_PROMPT_ALLOWLIST_UNIQUE_ENTRY: PASS")
    print("PORTABLE_PROMPT_ALLOWLIST_SIZE_SHA256_RENEWED: PASS")
    print("PORTABLE_BUILDER_ALLOWLIST_HASH_BINDING: PASS")
    print("PORTABLE_EXTERNAL_CONTROL_MANIFEST_UNCHANGED: PASS")
    print("PORTABLE_PRODUCTION_BUILD_GATE_CLOSED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    """Run the validator from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    validate(args.project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
