"""Enforce Tool-source classification and allowlisted release resources.

This module is the single policy owner for Release 3 source and archive
hygiene.  It classifies paths relative to the KANDA Reasoner Tool root,
validates synthetic fixture provenance, blocks Project captures, and provides
the explicit data-file list consumed by the PyInstaller specification.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any

from .kilo_workspace_policy import classify_verified_kilo_workspace

__all__ = [
    "ToolArchiveDecision",
    "ToolArchivePolicyError",
    "ToolPathClassification",
    "classify_tool_source_path",
    "inspect_tool_archive_candidate",
    "is_kanda_reasoner_tool_root",
    "is_project_capture_forbidden_relative",
    "iter_known_capture_records",
    "iter_packaged_resource_files",
    "load_source_classification_manifest",
    "validate_registered_synthetic_fixtures",
]

_CLASSIFICATION_FILE = "TOOL_SOURCE_CLASSIFICATION.json"
_FIXTURE_MANIFEST_FILE = "SYNTHETIC_FIXTURE_MANIFEST.json"
_SOURCE_HYGIENE_RELATIVE = Path("kanda_reasoner_app") / "source_hygiene"
_PROTECTED_MLRT_RESOURCE_RELATIVE = (
    Path("kanda_reasoner_app")
    / "routing_signal_scorer"
    / "mlrt_non_runtime_candidate_reliability"
)
_PROTECTED_MLRT_PACKAGED_DESTINATION = "mlrt"
_COMPILED_SUFFIXES = {".py", ".pyi", ".pyc", ".pyo"}
_WINDOWS_ABSOLUTE_RE = re.compile(
    rb"(?i)(?:[a-z]:[\\/](?:[^\x00\r\n\"']{1,240}))"
)
_PROJECT_SUPPORT_MARKERS = (
    b"_show_project_to_AI",
    b"project_error_memory",
    b"project_freeze_after_update",
)

_PACKAGING_CACHE_FOLDER_NAMES = frozenset(
    {
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
    }
)

_PACKAGING_BACKUP_NAME_RE = re.compile(
    r"(?i)(?:\.bak|\.backup|\.orig|\.old)(?:$|[._-])"
)


class ToolArchivePolicyError(RuntimeError):
    """Raised when a Tool path lacks safe packaging provenance."""


class ToolPathClassification(str, Enum):
    """Canonical Tool-source classifications required by Release 3."""

    CANONICAL_TOOL_SOURCE = "CANONICAL_TOOL_SOURCE"
    PACKAGED_TOOL_RESOURCE = "PACKAGED_TOOL_RESOURCE"
    REGISTERED_SYNTHETIC_FIXTURE = "REGISTERED_SYNTHETIC_FIXTURE"
    GENERATED_TOOL_EVIDENCE = "GENERATED_TOOL_EVIDENCE"
    PROJECT_CAPTURE_FORBIDDEN = "PROJECT_CAPTURE_FORBIDDEN"
    CACHE = "CACHE"
    TRANSIENT = "TRANSIENT"


@dataclass(frozen=True)
class ToolArchiveDecision:
    """Describe one path classification and archive inclusion decision."""

    relative_path: str
    classification: ToolPathClassification
    include_in_tool_archive: bool
    reason: str
    matched_rule: str


def _source_hygiene_root(tool_root: Path) -> Path:
    return tool_root / _SOURCE_HYGIENE_RELATIVE


def _normalized_relative(path: str | Path) -> str:
    text = str(path).replace("\\", "/").strip("/")
    while text.startswith("./"):
        text = text[2:]
    return text


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_kanda_reasoner_tool_root(root: str | Path) -> bool:
    """Return whether *root* is the canonical KANDA Reasoner source shape."""
    candidate = Path(root).expanduser().resolve(strict=False)
    return (
        (candidate / "reasoner_tools_gui.py").is_file()
        and (candidate / "KandaReasonerWindows.spec").is_file()
        and (candidate / "kanda_reasoner_app" / "__init__.py").is_file()
        and _source_hygiene_root(candidate).is_dir()
    )


@lru_cache(maxsize=8)
def _load_manifest_cached(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ToolArchivePolicyError(
            "TOOL_SOURCE_CLASSIFICATION_MANIFEST_UNREADABLE:" + str(path)
        ) from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0":
        raise ToolArchivePolicyError(
            "TOOL_SOURCE_CLASSIFICATION_MANIFEST_INVALID:" + str(path)
        )
    return payload


def load_source_classification_manifest(
    tool_root: str | Path,
) -> dict[str, Any]:
    """Load the immutable Tool-source classification manifest."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    path = _source_hygiene_root(root) / _CLASSIFICATION_FILE
    return _load_manifest_cached(str(path))


def _rule_matches(rule: dict[str, Any], relative_path: str) -> tuple[bool, str]:
    if "exact" in rule:
        expected = _normalized_relative(rule["exact"])
        return relative_path == expected, "exact:" + expected
    if "path_prefix" in rule:
        prefix = _normalized_relative(rule["path_prefix"])
        matched = relative_path == prefix or relative_path.startswith(prefix + "/")
        return matched, "path_prefix:" + prefix
    if "glob" in rule:
        pattern = _normalized_relative(rule["glob"])
        return fnmatch.fnmatchcase(relative_path, pattern), "glob:" + pattern
    return False, "invalid_rule"


def classify_tool_source_path(
    tool_root: str | Path,
    path_or_relative: str | Path,
) -> ToolArchiveDecision:
    """Classify one Tool path and fail closed when no rule owns it."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    raw = Path(path_or_relative)
    if raw.is_absolute():
        try:
            relative = raw.resolve(strict=False).relative_to(root).as_posix()
        except ValueError as exc:
            raise ToolArchivePolicyError(
                "TOOL_SOURCE_PATH_OUTSIDE_TOOL_ROOT:" + str(raw)
            ) from exc
    else:
        relative = _normalized_relative(raw)
    if not relative:
        raise ToolArchivePolicyError("TOOL_SOURCE_ROOT_NOT_ARCHIVE_MEMBER")

    manifest = load_source_classification_manifest(root)
    included = {
        ToolPathClassification(item)
        for item in manifest.get("archive_included_classifications", [])
    }
    for raw_rule in manifest.get("rules", []):
        if not isinstance(raw_rule, dict):
            continue
        matched, marker = _rule_matches(raw_rule, relative)
        if not matched:
            continue
        try:
            classification = ToolPathClassification(
                str(raw_rule.get("classification", ""))
            )
        except ValueError as exc:
            raise ToolArchivePolicyError(
                "TOOL_SOURCE_CLASSIFICATION_UNKNOWN:" + relative
            ) from exc
        return ToolArchiveDecision(
            relative_path=relative,
            classification=classification,
            include_in_tool_archive=classification in included,
            reason=str(raw_rule.get("reason", "")),
            matched_rule=marker,
        )
    kilo_record = classify_verified_kilo_workspace(
        root, relative, manifest.get("kilo_workspace_policy", {})
    )
    if kilo_record is not None:
        classification = ToolPathClassification(kilo_record.classification)
        return ToolArchiveDecision(
            relative_path=relative,
            classification=classification,
            include_in_tool_archive=classification in included,
            reason=kilo_record.reason,
            matched_rule=kilo_record.matched_rule,
        )
    hidden_decision = _root_hidden_metadata_decision(root, relative, manifest, included)
    if hidden_decision is not None:
        return hidden_decision
    raise ToolArchivePolicyError("UNCLASSIFIED_TOOL_SOURCE_PATH:" + relative)



def _root_hidden_metadata_decision(
    root: Path,
    relative: str,
    manifest: dict[str, Any],
    included: set[ToolPathClassification],
) -> ToolArchiveDecision | None:
    """Classify bounded root-level hidden tooling metadata by contents.

    Source-bearing hidden directories remain unclassified and therefore fail
    closed. This avoids an endless editor-name allowlist without turning every
    dot-directory into trusted non-source metadata.
    """
    policy = manifest.get("root_hidden_metadata_policy", {})
    if not isinstance(policy, dict) or policy.get("enabled") is not True:
        return None
    head = relative.split("/", 1)[0]
    if not head.startswith(".") or head in {".", ".."}:
        return None
    hidden_root = root / head
    if not hidden_root.is_dir() or hidden_root.is_symlink():
        return None
    reserved = {
        str(item).casefold()
        for item in policy.get("source_bearing_directory_names", [])
    }
    if head.casefold() in reserved:
        return None
    source_names = {
        str(item).casefold()
        for item in policy.get("source_bearing_file_names", [])
    }
    source_suffixes = {
        str(item).casefold()
        for item in policy.get("source_bearing_suffixes", [])
    }
    maximum = int(policy.get("maximum_files_inspected", 4096))
    inspected = 0
    try:
        for candidate in hidden_root.rglob("*"):
            if candidate.is_symlink():
                return None
            if not candidate.is_file():
                continue
            inspected += 1
            if inspected > maximum:
                return None
            if (
                candidate.name.casefold() in source_names
                or candidate.suffix.casefold() in source_suffixes
            ):
                return None
    except OSError:
        return None
    classification = ToolPathClassification(
        str(policy.get("classification", "GENERATED_TOOL_EVIDENCE"))
    )
    return ToolArchiveDecision(
        relative_path=relative,
        classification=classification,
        include_in_tool_archive=classification in included,
        reason=str(policy.get("reason", "Root hidden tooling metadata.")),
        matched_rule="root_hidden_metadata_policy:" + head,
    )

def _contains_suspicious_external_capture(tool_root: Path, path: Path) -> bool:
    """Inspect a bounded large text candidate for external Project roots."""
    manifest = load_source_classification_manifest(tool_root)
    threshold = int(
        manifest.get("suspicious_large_text_threshold_bytes", 8 * 1024 * 1024)
    )
    suffixes = {
        str(item).casefold()
        for item in manifest.get("suspicious_text_suffixes", [])
    }
    try:
        size = path.stat().st_size
    except OSError:
        return True
    if size < threshold or path.suffix.casefold() not in suffixes:
        return False

    overlap = b""
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                sample = overlap + block
                if _WINDOWS_ABSOLUTE_RE.search(sample):
                    return True
                if any(marker in sample for marker in _PROJECT_SUPPORT_MARKERS):
                    return True
                overlap = sample[-512:]
    except OSError:
        return True
    return False


def inspect_tool_archive_candidate(
    tool_root: str | Path,
    path: str | Path,
) -> ToolArchiveDecision:
    """Classify and inspect one source-archive or release candidate."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    candidate = Path(path).expanduser().resolve(strict=False)
    decision = classify_tool_source_path(root, candidate)
    if candidate.is_symlink():
        raise ToolArchivePolicyError(
            "TOOL_ARCHIVE_SYMLINK_REJECTED:" + decision.relative_path
        )
    if (
        candidate.is_file()
        and decision.include_in_tool_archive
        and _contains_suspicious_external_capture(root, candidate)
    ):
        raise ToolArchivePolicyError(
            "TOOL_ARCHIVE_SUSPICIOUS_EXTERNAL_PROJECT_CAPTURE:"
            + decision.relative_path
        )
    return decision


def _load_fixture_manifest(tool_root: Path) -> dict[str, Any]:
    path = _source_hygiene_root(tool_root) / _FIXTURE_MANIFEST_FILE
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ToolArchivePolicyError(
            "SYNTHETIC_FIXTURE_MANIFEST_UNREADABLE:" + str(path)
        ) from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0":
        raise ToolArchivePolicyError(
            "SYNTHETIC_FIXTURE_MANIFEST_INVALID:" + str(path)
        )
    return payload


def validate_registered_synthetic_fixtures(
    tool_root: str | Path,
) -> tuple[dict[str, Any], ...]:
    """Validate every registered synthetic fixture and exact content hash."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    manifest = _load_fixture_manifest(root)
    validated: list[dict[str, Any]] = []
    for raw in manifest.get("fixtures", []):
        if not isinstance(raw, dict):
            raise ToolArchivePolicyError("SYNTHETIC_FIXTURE_RECORD_INVALID")
        required = (
            "fixture_id",
            "path",
            "synthetic",
            "source_owner",
            "contains_real_project_data",
            "purpose",
            "maintainer",
            "sha256",
        )
        if any(key not in raw for key in required):
            raise ToolArchivePolicyError(
                "SYNTHETIC_FIXTURE_REQUIRED_FIELD_MISSING"
            )
        if raw["synthetic"] is not True:
            raise ToolArchivePolicyError("SYNTHETIC_FIXTURE_FLAG_REQUIRED")
        if str(raw["source_owner"]).upper() != "TOOL":
            raise ToolArchivePolicyError("SYNTHETIC_FIXTURE_TOOL_OWNER_REQUIRED")
        if raw["contains_real_project_data"] is not False:
            raise ToolArchivePolicyError(
                "SYNTHETIC_FIXTURE_REAL_PROJECT_DATA_REJECTED"
            )
        fixture = root / _normalized_relative(raw["path"])
        decision = classify_tool_source_path(root, fixture)
        if decision.classification is not ToolPathClassification.REGISTERED_SYNTHETIC_FIXTURE:
            raise ToolArchivePolicyError(
                "SYNTHETIC_FIXTURE_CLASSIFICATION_MISMATCH:" + str(fixture)
            )
        if not fixture.is_file() or _sha256_file(fixture) != str(raw["sha256"]):
            raise ToolArchivePolicyError(
                "SYNTHETIC_FIXTURE_HASH_MISMATCH:" + str(fixture)
            )
        validated.append(dict(raw))
    if not validated:
        raise ToolArchivePolicyError("SYNTHETIC_FIXTURE_MANIFEST_EMPTY")
    return tuple(validated)


def iter_known_capture_records(tool_root: str | Path) -> tuple[dict[str, Any], ...]:
    """Return immutable known-capture records from the Tool policy manifest."""
    manifest = load_source_classification_manifest(tool_root)
    records = manifest.get("known_capture_records", [])
    if not isinstance(records, list):
        raise ToolArchivePolicyError("KNOWN_CAPTURE_RECORDS_INVALID")
    return tuple(dict(item) for item in records if isinstance(item, dict))


def is_project_capture_forbidden_relative(relative_path: str | Path) -> bool:
    """Detect forbidden Tool capture paths inside source or packaged layouts."""
    parts = tuple(
        part.casefold()
        for part in Path(_normalized_relative(relative_path)).parts
        if part not in {"", "."}
    )
    sequence = ("kanda_reasoner_app", "outputs")
    width = len(sequence)
    return any(
        parts[index : index + width] == sequence
        for index in range(max(0, len(parts) - width + 1))
    )


def _is_packaging_cache_path(root: Path, path: Path) -> bool:
    """Return whether *path* is inside a non-runtime packaging cache."""

    relative = path.relative_to(root)
    return any(
        part.casefold() in _PACKAGING_CACHE_FOLDER_NAMES
        for part in relative.parts
    )


def _is_packaging_backup_path(path: Path) -> bool:
    """Return whether *path* uses a known non-runtime backup filename."""

    name = path.name
    return bool(
        name.endswith("~")
        or _PACKAGING_BACKUP_NAME_RE.search(name)
    )


def iter_packaged_resource_files(
    tool_root: str | Path,
) -> list[tuple[str, str]]:
    """Return explicit PyInstaller data files from the classification allowlist."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    if not is_kanda_reasoner_tool_root(root):
        raise ToolArchivePolicyError("PYINSTALLER_TOOL_ROOT_INVALID:" + str(root))
    validate_registered_synthetic_fixtures(root)
    package_root = root / "kanda_reasoner_app"
    resources: list[tuple[str, str]] = []
    for path in sorted(package_root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if not path.is_file() or path.suffix.casefold() in _COMPILED_SUFFIXES:
            continue
        if _is_packaging_cache_path(root, path):
            continue
        if _is_packaging_backup_path(path):
            continue
        decision = inspect_tool_archive_candidate(root, path)
        if not decision.include_in_tool_archive:
            continue
        relative = path.relative_to(root)
        if (
            relative.parent == _PROTECTED_MLRT_RESOURCE_RELATIVE
            and path.suffix.casefold() == ".md"
        ):
            destination = _PROTECTED_MLRT_PACKAGED_DESTINATION
        else:
            destination = relative.parent.as_posix()
        resources.append((str(path), destination))
    if not resources:
        raise ToolArchivePolicyError("PYINSTALLER_DATA_ALLOWLIST_EMPTY")
    return resources
