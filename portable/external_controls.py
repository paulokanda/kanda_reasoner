"""Exact hash binding for external Portable build-control files."""

from __future__ import annotations

import hashlib
import json
import stat
from pathlib import Path, PurePosixPath
from typing import Any

from portable.constants import (
    BUILDER_VERSION,
    EXTERNAL_CONTROL_FEATURE_ID,
    FEATURE_ID,
    PORTABLE_HARDENING_FEATURES,
)

__all__ = [
    "REQUIRED_EXTERNAL_CONTROLS",
    "ExternalControlError",
    "validate_external_build_controls",
]

EXTERNAL_CONTROL_MANIFEST_NAME = "PORTABLE_EXTERNAL_BUILD_CONTROLS.json"
EXTERNAL_CONTROL_CONTRACT = "exact_external_build_controls_v1"
REQUIRED_EXTERNAL_CONTROLS = (
    ("KandaReasonerWindows.spec", "pyinstaller_spec"),
    ("kanda_reasoner_app/__init__.py", "application_package_initializer"),
    (
        "kanda_reasoner_app/source_hygiene/__init__.py",
        "archive_policy_package_initializer",
    ),
    (
        "kanda_reasoner_app/source_hygiene/tool_archive_policy.py",
        "archive_policy_owner",
    ),
    (
        "kanda_reasoner_app/source_hygiene/kilo_workspace_policy.py",
        "archive_policy_dependency",
    ),
    (
        "kanda_reasoner_app/source_hygiene/TOOL_SOURCE_CLASSIFICATION.json",
        "source_classification_manifest",
    ),
    (
        "kanda_reasoner_app/source_hygiene/SYNTHETIC_FIXTURE_MANIFEST.json",
        "synthetic_fixture_manifest",
    ),
)


class ExternalControlError(RuntimeError):
    """Raised when external build-control identity is not exact."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_relative(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ExternalControlError("EXTERNAL_CONTROL_PATH_EMPTY")
    if "\\" in value:
        raise ExternalControlError("EXTERNAL_CONTROL_PATH_BACKSLASH")
    path = PurePosixPath(value)
    if path.is_absolute() or "." in path.parts or ".." in path.parts:
        raise ExternalControlError("EXTERNAL_CONTROL_PATH_UNSAFE")
    canonical = path.as_posix()
    if canonical != value:
        raise ExternalControlError("EXTERNAL_CONTROL_PATH_NONCANONICAL")
    return canonical


def _has_reparse_attribute(path: Path) -> bool:
    attributes = getattr(path.lstat(), "st_file_attributes", 0)
    flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return bool(flag and attributes & flag)


def _canonical_control_set_sha(items: list[dict[str, Any]]) -> str:
    encoded = json.dumps(
        {"items": items}, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_external_control_manifest(portable_root: Path) -> dict[str, Any]:
    path = portable_root / EXTERNAL_CONTROL_MANIFEST_NAME
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalControlError("EXTERNAL_CONTROL_MANIFEST_UNREADABLE") from exc
    if not isinstance(payload, dict):
        raise ExternalControlError("EXTERNAL_CONTROL_MANIFEST_NOT_OBJECT")
    return payload


def validate_external_build_controls(
    project_root: Path,
    portable_root: Path | None = None,
) -> dict[str, Any]:
    root = project_root.resolve()
    if root.name.casefold() != "kanda_reasoner":
        raise ExternalControlError("EXTERNAL_CONTROL_TOOL_ROOT_MISMATCH")
    portable = (portable_root or (root / "portable")).resolve()
    try:
        portable.relative_to(root)
    except ValueError as exc:
        raise ExternalControlError("EXTERNAL_CONTROL_PORTABLE_OUTSIDE_TOOL") from exc
    manifest = load_external_control_manifest(portable)
    if manifest.get("schema_version") != "1.0":
        raise ExternalControlError("EXTERNAL_CONTROL_SCHEMA_MISMATCH")
    if manifest.get("artifact_type") != "portable_external_build_control_manifest":
        raise ExternalControlError("EXTERNAL_CONTROL_ARTIFACT_TYPE_MISMATCH")
    if manifest.get("contract_version") != EXTERNAL_CONTROL_CONTRACT:
        raise ExternalControlError("EXTERNAL_CONTROL_CONTRACT_MISMATCH")
    if manifest.get("feature_id") != EXTERNAL_CONTROL_FEATURE_ID:
        raise ExternalControlError("EXTERNAL_CONTROL_FEATURE_ID_MISMATCH")
    if manifest.get("builder_feature_id") != FEATURE_ID:
        raise ExternalControlError("EXTERNAL_CONTROL_BUILDER_FEATURE_MISMATCH")
    if manifest.get("builder_version") != BUILDER_VERSION:
        raise ExternalControlError("EXTERNAL_CONTROL_BUILDER_VERSION_MISMATCH")
    if manifest.get("hardening_features") != list(PORTABLE_HARDENING_FEATURES):
        raise ExternalControlError("EXTERNAL_CONTROL_CAPABILITY_SET_MISMATCH")
    raw_items = manifest.get("items")
    if not isinstance(raw_items, list):
        raise ExternalControlError("EXTERNAL_CONTROL_ITEMS_MISSING")
    if int(manifest.get("item_count", -1)) != len(REQUIRED_EXTERNAL_CONTROLS):
        raise ExternalControlError("EXTERNAL_CONTROL_ITEM_COUNT_MISMATCH")
    if len(raw_items) != len(REQUIRED_EXTERNAL_CONTROLS):
        raise ExternalControlError("EXTERNAL_CONTROL_ITEM_SET_LENGTH_MISMATCH")
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            raise ExternalControlError("EXTERNAL_CONTROL_ITEM_INVALID")
        relative = _canonical_relative(raw.get("source_relative"))
        expected_relative, expected_role = REQUIRED_EXTERNAL_CONTROLS[index]
        if relative != expected_relative:
            raise ExternalControlError("EXTERNAL_CONTROL_ORDER_OR_PATH_MISMATCH")
        if str(raw.get("role") or "") != expected_role:
            raise ExternalControlError("EXTERNAL_CONTROL_ROLE_MISMATCH")
        folded = relative.casefold()
        if folded in seen:
            raise ExternalControlError("EXTERNAL_CONTROL_DUPLICATE_PATH")
        seen.add(folded)
        try:
            expected_size = int(raw.get("size_bytes", -1))
        except (TypeError, ValueError) as exc:
            raise ExternalControlError("EXTERNAL_CONTROL_SIZE_INVALID") from exc
        expected_hash = str(raw.get("sha256") or "").casefold()
        if len(expected_hash) != 64 or any(ch not in "0123456789abcdef" for ch in expected_hash):
            raise ExternalControlError("EXTERNAL_CONTROL_SHA256_INVALID")
        path = root / relative
        if path.is_symlink() or (path.exists() and _has_reparse_attribute(path)):
            raise ExternalControlError("EXTERNAL_CONTROL_LINK_OR_REPARSE_REJECTED")
        if not path.is_file():
            raise ExternalControlError("EXTERNAL_CONTROL_FILE_MISSING:" + relative)
        resolved = path.resolve()
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ExternalControlError("EXTERNAL_CONTROL_RESOLVES_OUTSIDE_TOOL") from exc
        if path.stat().st_size != expected_size:
            raise ExternalControlError("EXTERNAL_CONTROL_SIZE_MISMATCH:" + relative)
        if _sha256(path).casefold() != expected_hash:
            raise ExternalControlError("EXTERNAL_CONTROL_SHA256_MISMATCH:" + relative)
        items.append(
            {
                "role": expected_role,
                "source_relative": relative,
                "size_bytes": expected_size,
                "sha256": expected_hash,
            }
        )
    control_set_hash = _canonical_control_set_sha(items)
    if manifest.get("control_set_sha256") != control_set_hash:
        raise ExternalControlError("EXTERNAL_CONTROL_SET_SHA256_MISMATCH")
    return {
        "feature_id": EXTERNAL_CONTROL_FEATURE_ID,
        "item_count": len(items),
        "control_set_sha256": control_set_hash,
        "manifest_sha256": _sha256(portable / EXTERNAL_CONTROL_MANIFEST_NAME),
        "items": items,
    }
