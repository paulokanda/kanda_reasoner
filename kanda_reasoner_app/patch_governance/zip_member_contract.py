\
# project-path: kanda_reasoner_app/patch_governance/zip_member_contract.py
"""Private ZIP member hardening for the canonical patch-governance validator."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import PurePosixPath
import re
import stat
from typing import Any, Mapping
import zipfile

__all__: list[str] = []

_INSTALL_MANIFEST = "INSTALL_MANIFEST.json"
_PAYLOAD_PREFIX = "payload/"
_DRIVE_PREFIX = re.compile(r"^[A-Za-z]:")
_WINDOWS_REPARSE_POINT = 0x0400


class ZipMemberContractError(ValueError):
    """Raised when an archive member violates the private ZIP safety contract."""


@dataclass(frozen=True)
class ZipMemberInventory:
    """Canonical, collision-checked member inventory for one patch ZIP."""

    names: tuple[str, ...]
    file_names: tuple[str, ...]
    directory_names: tuple[str, ...]
    declared_payload_members: tuple[str, ...]


def _fail(code: str, detail: str) -> None:
    raise ZipMemberContractError(f"{code}: {detail}")


def _canonical_member_name(raw_name: str, *, allow_directory: bool = True) -> str:
    raw = str(raw_name or "")
    if not raw:
        _fail("ZIP_MEMBER_EMPTY", "archive member name is empty")
    if "\x00" in raw:
        _fail("ZIP_MEMBER_NULL", repr(raw))
    if "\\" in raw:
        _fail("ZIP_MEMBER_BACKSLASH_SEPARATOR", raw)
    if raw.startswith("//"):
        _fail("ZIP_MEMBER_UNC_PATH", raw)
    if raw.startswith("/"):
        _fail("ZIP_MEMBER_ABSOLUTE_PATH", raw)
    if _DRIVE_PREFIX.match(raw):
        _fail("ZIP_MEMBER_DRIVE_QUALIFIED_PATH", raw)

    is_directory = raw.endswith("/")
    if is_directory and not allow_directory:
        _fail("ZIP_MEMBER_DIRECTORY_NOT_ALLOWED", raw)
    body = raw[:-1] if is_directory else raw
    parts = body.split("/")
    if any(part == "" for part in parts):
        _fail("ZIP_MEMBER_EMPTY_COMPONENT", raw)
    if any(part == "." for part in parts):
        _fail("ZIP_MEMBER_DOT_COMPONENT", raw)
    if any(part == ".." for part in parts):
        _fail("ZIP_MEMBER_TRAVERSAL", raw)
    if any(":" in part for part in parts):
        _fail("ZIP_MEMBER_COLON_COMPONENT", raw)

    canonical = "/".join(parts)
    return canonical + ("/" if is_directory else "")


def _relative_manifest_path(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("ZIP_INSTALL_MANIFEST_PATH_INVALID", field)
    canonical = _canonical_member_name(value, allow_directory=False)
    if canonical.startswith(_PAYLOAD_PREFIX):
        _fail("ZIP_INSTALL_MANIFEST_PROJECT_PATH_PREFIXED", canonical)
    return canonical


def _is_unexpected_link_or_special(info: zipfile.ZipInfo) -> bool:
    unix_mode = (int(info.external_attr) >> 16) & 0xFFFF
    file_type = stat.S_IFMT(unix_mode)
    if file_type == stat.S_IFLNK:
        return True
    if file_type not in (0, stat.S_IFREG, stat.S_IFDIR):
        return True
    dos_attributes = int(info.external_attr) & 0xFFFF
    return bool(dos_attributes & _WINDOWS_REPARSE_POINT)


def _validate_member_names(
    archive: zipfile.ZipFile,
) -> tuple[list[str], list[str], list[str], dict[str, zipfile.ZipInfo]]:
    names: list[str] = []
    files: list[str] = []
    directories: list[str] = []
    infos: dict[str, zipfile.ZipInfo] = {}
    exact_seen: set[str] = set()
    folded_seen: dict[str, str] = {}
    kind_by_path: dict[str, str] = {}

    for info in archive.infolist():
        # ZipInfo.filename is normalized by zipfile._sanitize_filename. On
        # Windows that converts raw backslashes from archive metadata to '/'.
        # orig_filename preserves the exact decoded archive member name and
        # must be the containment/collision authority.
        raw = info.orig_filename
        if raw in exact_seen:
            _fail("ZIP_MEMBER_DUPLICATE", raw)
        exact_seen.add(raw)
        canonical = _canonical_member_name(raw)
        path_key = canonical.rstrip("/")
        kind = "directory" if info.is_dir() or canonical.endswith("/") else "file"

        previous_kind = kind_by_path.get(path_key)
        if previous_kind is not None:
            if previous_kind != kind:
                _fail("ZIP_MEMBER_FILE_DIRECTORY_COLLISION", path_key)
            _fail("ZIP_MEMBER_DUPLICATE", path_key)
        kind_by_path[path_key] = kind

        folded = path_key.casefold()
        previous = folded_seen.get(folded)
        if previous is not None and previous != path_key:
            _fail("ZIP_MEMBER_WINDOWS_CASE_COLLISION", f"{previous} <> {path_key}")
        folded_seen[folded] = path_key

        if _is_unexpected_link_or_special(info):
            _fail("ZIP_MEMBER_UNEXPECTED_LINK", canonical)

        names.append(canonical)
        infos[canonical] = info
        if kind == "directory":
            directories.append(path_key)
        else:
            files.append(path_key)

    file_paths = set(files)
    folded_files = {item.casefold(): item for item in files}
    directory_paths = set(directories)
    for file_path in files:
        if file_path in directory_paths:
            _fail("ZIP_MEMBER_FILE_DIRECTORY_COLLISION", file_path)
        parts = PurePosixPath(file_path).parts
        for index in range(1, len(parts)):
            parent = "/".join(parts[:index])
            if parent in file_paths:
                _fail("ZIP_MEMBER_FILE_DIRECTORY_COLLISION", f"{parent} contains {file_path}")
            folded_parent = parent.casefold()
            if folded_parent in folded_files:
                owner = folded_files[folded_parent]
                _fail("ZIP_MEMBER_FILE_DIRECTORY_COLLISION", f"{owner} contains {file_path}")

    return names, files, directories, infos


def _load_install_manifest(
    archive: zipfile.ZipFile,
    infos: Mapping[str, zipfile.ZipInfo],
) -> Mapping[str, Any] | None:
    info = infos.get(_INSTALL_MANIFEST)
    if info is None:
        return None
    try:
        loaded = json.loads(archive.read(info).decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        _fail("ZIP_INSTALL_MANIFEST_INVALID", str(exc))
    if not isinstance(loaded, Mapping):
        _fail("ZIP_INSTALL_MANIFEST_INVALID", "root value must be an object")
    return loaded


def _declared_payload_members(manifest: Mapping[str, Any]) -> set[str]:
    declared: set[str] = set()
    folded: dict[str, str] = {}

    def add(member: str) -> None:
        canonical = _canonical_member_name(member, allow_directory=False)
        if not canonical.startswith(_PAYLOAD_PREFIX):
            _fail("ZIP_INSTALL_MANIFEST_PAYLOAD_OUTSIDE_NAMESPACE", canonical)
        key = canonical.casefold()
        previous = folded.get(key)
        if previous is not None:
            _fail("ZIP_INSTALL_MANIFEST_DUPLICATE_DECLARATION", f"{previous} <> {canonical}")
        folded[key] = canonical
        declared.add(canonical)

    files = manifest.get("files", [])
    if not isinstance(files, list):
        _fail("ZIP_INSTALL_MANIFEST_FILES_INVALID", "files must be a list")
    for index, item in enumerate(files):
        if not isinstance(item, Mapping):
            _fail("ZIP_INSTALL_MANIFEST_FILES_INVALID", f"files[{index}]")
        relative = _relative_manifest_path(item.get("path"), field=f"files[{index}].path")
        add(_PAYLOAD_PREFIX + relative)

    intake = manifest.get("error_memory_intake", [])
    if not isinstance(intake, list):
        _fail("ZIP_INSTALL_MANIFEST_INTAKE_INVALID", "error_memory_intake must be a list")
    for index, item in enumerate(intake):
        if not isinstance(item, Mapping):
            _fail("ZIP_INSTALL_MANIFEST_INTAKE_INVALID", f"error_memory_intake[{index}]")
        source = item.get("source_member")
        if not isinstance(source, str) or not source.strip():
            _fail("ZIP_INSTALL_MANIFEST_INTAKE_INVALID", f"error_memory_intake[{index}].source_member")
        add(source)

    extras = manifest.get("declared_payload_members", [])
    if not isinstance(extras, list):
        _fail("ZIP_INSTALL_MANIFEST_EXTRA_INVALID", "declared_payload_members must be a list")
    for index, member in enumerate(extras):
        if not isinstance(member, str) or not member.strip():
            _fail("ZIP_INSTALL_MANIFEST_EXTRA_INVALID", f"declared_payload_members[{index}]")
        add(member)

    return declared


def validate_zip_member_contract(archive: zipfile.ZipFile) -> ZipMemberInventory:
    """Validate member containment, collision, link, and manifest declaration rules."""
    names, files, directories, infos = _validate_member_names(archive)
    payload_files = {name for name in files if name.startswith(_PAYLOAD_PREFIX)}
    manifest = _load_install_manifest(archive, infos)
    if payload_files and manifest is None:
        _fail("ZIP_INSTALL_MANIFEST_MISSING", "payload members require root INSTALL_MANIFEST.json")

    declared: set[str] = set()
    if manifest is not None:
        declared = _declared_payload_members(manifest)
        undeclared = sorted(payload_files - declared)
        missing = sorted(declared - payload_files)
        if undeclared:
            _fail("ZIP_PAYLOAD_UNDECLARED", ", ".join(undeclared))
        if missing:
            _fail("ZIP_PAYLOAD_DECLARED_MISSING", ", ".join(missing))

    return ZipMemberInventory(
        names=tuple(names),
        file_names=tuple(files),
        directory_names=tuple(directories),
        declared_payload_members=tuple(sorted(declared)),
    )
