"""Exact Portable builder member governance."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path, PurePosixPath
from typing import Any


__all__ = [
    "BuilderMemberError",
    "validate_exact_builder_members",
]

MANIFEST_NAME = "PORTABLE_BUILDER_MANIFEST.json"
MEMBER_CONTRACT = "exact_builder_members_v1"
MANIFEST_SELF_CONTRACT = "structural_identity_and_install_receipt_sha256"


class BuilderMemberError(RuntimeError):
    """Raised when the Portable builder member set is not exact."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_relative(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise BuilderMemberError("BUILDER_MEMBER_PATH_EMPTY")
    if "\\" in value:
        raise BuilderMemberError("BUILDER_MEMBER_PATH_BACKSLASH")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise BuilderMemberError("BUILDER_MEMBER_PATH_UNSAFE")
    canonical = path.as_posix()
    if canonical != value:
        raise BuilderMemberError("BUILDER_MEMBER_PATH_NONCANONICAL")
    return canonical


def _has_reparse_attribute(path: Path) -> bool:
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return bool(flag and attributes & flag)


def _kind(path: Path) -> str:
    if path.is_symlink() or _has_reparse_attribute(path):
        return "link_or_reparse"
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    return "special"


def collect_builder_members(root: Path) -> dict[str, list[str]]:
    root = root.resolve()
    if root.name.casefold() != "portable":
        raise BuilderMemberError("BUILDER_MEMBER_ROOT_NAME_MISMATCH")
    files: list[str] = []
    directories: list[str] = []
    links_or_reparse: list[str] = []
    special: list[str] = []
    for parent, dir_names, file_names in os.walk(root, topdown=True, followlinks=False):
        parent_path = Path(parent)
        for name in sorted(dir_names, key=str.casefold):
            path = parent_path / name
            relative = path.relative_to(root).as_posix()
            kind = _kind(path)
            if kind == "directory":
                directories.append(relative)
            elif kind == "link_or_reparse":
                links_or_reparse.append(relative)
            else:
                special.append(relative)
        for name in sorted(file_names, key=str.casefold):
            path = parent_path / name
            relative = path.relative_to(root).as_posix()
            kind = _kind(path)
            if kind == "file":
                files.append(relative)
            elif kind == "link_or_reparse":
                links_or_reparse.append(relative)
            else:
                special.append(relative)
    return {
        "files": sorted(files),
        "directories": sorted(directories),
        "links_or_reparse": sorted(links_or_reparse),
        "special": sorted(special),
    }


def _require_case_unique(paths: set[str]) -> None:
    folded: dict[str, str] = {}
    for value in sorted(paths):
        key = value.casefold()
        previous = folded.get(key)
        if previous is not None and previous != value:
            raise BuilderMemberError("BUILDER_MEMBER_CASE_COLLISION")
        folded[key] = value


def validate_exact_builder_members(
    root: Path,
    manifest: dict[str, Any],
) -> dict[str, list[str]]:
    if manifest.get("builder_member_contract_version") != MEMBER_CONTRACT:
        raise BuilderMemberError("BUILDER_MEMBER_CONTRACT_VERSION_MISMATCH")
    if manifest.get("manifest_self_contract") != MANIFEST_SELF_CONTRACT:
        raise BuilderMemberError("BUILDER_MANIFEST_SELF_CONTRACT_MISMATCH")
    if manifest.get("exact_builder_member_contract_pending") is not False:
        raise BuilderMemberError("BUILDER_MEMBER_CONTRACT_STILL_PENDING")
    if manifest.get("exact_builder_member_governance") is not True:
        raise BuilderMemberError("BUILDER_MEMBER_GOVERNANCE_FLAG_MISSING")

    file_hashes = manifest.get("files")
    if not isinstance(file_hashes, dict) or not file_hashes:
        raise BuilderMemberError("BUILDER_MEMBER_HASH_MAP_MISSING")
    expected_files = {_canonical_relative(str(name)) for name in file_hashes}
    expected_files.add(MANIFEST_NAME)
    expected_directories_raw = manifest.get("directories")
    if not isinstance(expected_directories_raw, list):
        raise BuilderMemberError("BUILDER_DIRECTORY_SET_MISSING")
    expected_directories = {
        _canonical_relative(str(name)) for name in expected_directories_raw
    }
    _require_case_unique(expected_files | expected_directories)

    inventory = collect_builder_members(root)
    actual_files = set(inventory["files"])
    actual_directories = set(inventory["directories"])
    if inventory["links_or_reparse"]:
        raise BuilderMemberError(
            "BUILDER_LINK_OR_REPARSE_MEMBER:" + ",".join(inventory["links_or_reparse"])
        )
    if inventory["special"]:
        raise BuilderMemberError(
            "BUILDER_SPECIAL_MEMBER:" + ",".join(inventory["special"])
        )
    _require_case_unique(actual_files | actual_directories)
    if actual_files != expected_files:
        raise BuilderMemberError(
            "BUILDER_FILE_SET_MISMATCH:"
            f"missing={sorted(expected_files - actual_files)};"
            f"extra={sorted(actual_files - expected_files)}"
        )
    if actual_directories != expected_directories:
        raise BuilderMemberError(
            "BUILDER_DIRECTORY_SET_MISMATCH:"
            f"missing={sorted(expected_directories - actual_directories)};"
            f"extra={sorted(actual_directories - expected_directories)}"
        )
    for relative, expected_hash in sorted(file_hashes.items()):
        actual_hash = _sha256(root / relative)
        if actual_hash.casefold() != str(expected_hash).casefold():
            raise BuilderMemberError("BUILDER_MEMBER_HASH_MISMATCH:" + relative)
    total = len(actual_files) + len(actual_directories)
    if int(manifest.get("exact_builder_member_count", -1)) != total:
        raise BuilderMemberError("BUILDER_MEMBER_COUNT_MISMATCH")
    if int(manifest.get("exact_builder_file_count", -1)) != len(actual_files):
        raise BuilderMemberError("BUILDER_FILE_COUNT_MISMATCH")
    if int(manifest.get("exact_builder_directory_count", -1)) != len(actual_directories):
        raise BuilderMemberError("BUILDER_DIRECTORY_COUNT_MISMATCH")
    return inventory
