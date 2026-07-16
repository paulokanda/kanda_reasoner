"""Core helpers for json_splitter_split_reassemble_validation."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

__all__ = [
    "CHUNK_SCHEMA",
    "stable_hash",
]

CHUNK_SCHEMA = "chatgpt-json-chunk/v1"
ROUTE_MANIFEST_SCHEMA = "project-reasoner-web-ai-route-manifest/v1"


def stable_hash(value: Any) -> str:
    """Return the canonical stable hash used by the splitter."""
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _load_json(path: Path) -> Any:
    """Load JSON from path."""
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return json.load(handle)


def _safe_text(value: Any) -> str:
    """Return stripped text."""
    return str(value or "").strip()


def _safe_int(value: Any) -> int:
    """Return int(value), or zero if conversion fails."""
    try:
        return int(value)
    except Exception:
        return 0


def _get_entries(node: Any, entry_keys: list[Any] | None = None) -> list[tuple[Any, Any]]:
    """Return entries for a dict or list chunk payload.

    For list chunks, prefer manifest entry_keys because they preserve the
    original absolute source indexes. Falling back to enumerate(node) is only a
    legacy compatibility path.
    """
    if isinstance(node, dict):
        return list(node.items())

    if isinstance(node, list):
        if entry_keys is not None and len(entry_keys) == len(node):
            return list(zip(entry_keys, node))
        return list(enumerate(node))

    raise TypeError("Chunk payload must be a dict or list.")


def _sort_key_for_entry(entry: tuple[Any, Any]) -> tuple[int, Any]:
    """Return stable sort key for reconstructed list entries."""
    key = entry[0]
    if isinstance(key, int):
        return (0, key)
    try:
        return (0, int(key))
    except Exception:
        return (1, str(key))


def _rebuild_container(entries: list[tuple[Any, Any]], is_list: bool) -> Any:
    """Rebuild a dict or list from part entries."""
    if is_list:
        return [
            value
            for _key, value in sorted(entries, key=_sort_key_for_entry)
        ]
    return {key: value for key, value in entries}


def _set_nested_value(root: Any, path_parts: list[str], new_value: Any) -> Any:
    """Return a copy of root with a nested path replaced by new_value."""
    cloned = copy.deepcopy(root)
    if not path_parts:
        return new_value

    cur = cloned
    for part in path_parts[:-1]:
        cur = cur[part]
    cur[path_parts[-1]] = new_value
    return cloned


def _get_nested_value(root: Any, path_parts: list[str]) -> Any:
    """Read a nested value from root."""
    cur = root
    for part in path_parts:
        if not isinstance(cur, dict):
            raise KeyError("'" + part + "' is not inside a dict.")
        cur = cur[part]
    return cur


def _resolve_source_file(manifest: dict[str, Any], manifest_dir: Path) -> Path | None:
    """Resolve source_file from a split manifest."""
    source_text = _safe_text(manifest.get("source_file", ""))
    if not source_text:
        return None

    source_path = Path(source_text)
    if source_path.exists() and source_path.is_file():
        return source_path.resolve()

    candidate = (manifest_dir / source_text).resolve()
    if candidate.exists() and candidate.is_file():
        return candidate

    return None


def _expected_chunk_from_source(
    source_payload: Any,
    path_parts: list[str],
    entry_keys: list[Any],
    is_list: bool,
) -> Any:
    """Build the expected chunk payload from the canonical source JSON."""
    container = _get_nested_value(source_payload, path_parts) if path_parts else source_payload

    if is_list:
        if not isinstance(container, list):
            raise TypeError("Expected source container at path to be a list.")
        return [container[int(key)] for key in entry_keys]

    if not isinstance(container, dict):
        raise TypeError("Expected source container at path to be a dict.")
    return {str(key): container[str(key)] for key in entry_keys}


def _expected_coverage_keys(
    source_payload: Any,
    path_parts: list[str],
    is_list: bool,
    nested_split_top_keys: set[str],
) -> set[Any]:
    """Return expected covered keys for a split path."""
    container = _get_nested_value(source_payload, path_parts) if path_parts else source_payload

    if is_list:
        if not isinstance(container, list):
            return set()
        return set(range(len(container)))

    if not isinstance(container, dict):
        return set()

    keys = set(container.keys())
    if not path_parts:
        keys = keys - nested_split_top_keys
    return keys


def _sorted_key_sample(values: set[Any], limit: int = 12) -> list[str]:
    """Return a stable printable key sample."""
    return [str(item) for item in sorted(values, key=lambda item: str(item))[:limit]]


def _validate_partitions_against_source(
    *,
    manifest: dict[str, Any],
    manifest_dir: Path,
) -> dict[str, Any]:
    """Validate every part directly against the source JSON slice it represents."""
    source_path = _resolve_source_file(manifest, manifest_dir)
    if source_path is None:
        return {
            "available": False,
            "ok": False,
            "message": "Source JSON file is not available for partition validation.",
            "source_path": "",
            "part_mismatch_count": 0,
            "coverage_mismatch_count": 0,
        }

    source_payload = _load_json(source_path)
    source_hash = stable_hash(source_payload)
    manifest_source_hash = _safe_text(manifest.get("source_sha256", ""))
    if manifest_source_hash and source_hash != manifest_source_hash:
        return {
            "available": True,
            "ok": False,
            "message": "Source JSON hash does not match split manifest source hash.",
            "source_path": str(source_path),
            "part_mismatch_count": 0,
            "coverage_mismatch_count": 0,
        }

    parts = manifest.get("parts", [])
    if not isinstance(parts, list):
        parts = []

    nested_split_top_keys = {
        str(part.get("path_parts", [""])[0])
        for part in parts
        if isinstance(part, dict)
        and isinstance(part.get("path_parts", []), list)
        and part.get("path_parts", [])
    }

    part_mismatches: list[dict[str, Any]] = []
    coverage_by_path: dict[tuple[str, ...], set[Any]] = {}
    path_is_list: dict[tuple[str, ...], bool] = {}

    for part_info in parts:
        if not isinstance(part_info, dict):
            continue

        filename = _safe_text(part_info.get("filename", ""))
        part_path = manifest_dir / filename
        if not part_path.exists():
            part_mismatches.append({
                "filename": filename,
                "reason": "missing_chunk_file",
            })
            continue

        part_doc = _load_json(part_path)
        path_parts = [str(item) for item in part_info.get("path_parts", [])]
        path_tuple = tuple(path_parts)
        is_list = bool(part_info.get("is_list", False))
        path_is_list[path_tuple] = is_list
        entry_keys = part_info.get("entry_keys", [])
        if not isinstance(entry_keys, list):
            entry_keys = []

        chunk_value = _chunk_value_from_doc(
            part_doc=part_doc,
            part_info=part_info,
            root_skeleton_present=True,
        )
        expected_value = _expected_chunk_from_source(
            source_payload,
            path_parts,
            entry_keys,
            is_list,
        )

        if stable_hash(chunk_value) != stable_hash(expected_value):
            part_mismatches.append({
                "filename": filename,
                "reason": "chunk_payload_does_not_match_source_slice",
                "path_parts": path_parts,
            })

        key_set = coverage_by_path.setdefault(path_tuple, set())
        for key in entry_keys:
            if is_list:
                try:
                    key_set.add(int(key))
                except Exception:
                    key_set.add(str(key))
            else:
                key_set.add(str(key))

    coverage_mismatches: list[dict[str, Any]] = []
    for path_tuple, actual_keys in coverage_by_path.items():
        is_list = path_is_list.get(path_tuple, False)
        expected_keys = _expected_coverage_keys(
            source_payload,
            list(path_tuple),
            is_list,
            nested_split_top_keys,
        )
        if actual_keys != expected_keys:
            missing = expected_keys - actual_keys
            extra = actual_keys - expected_keys
            coverage_mismatches.append({
                "path_parts": list(path_tuple),
                "expected_count": len(expected_keys),
                "actual_count": len(actual_keys),
                "missing_count": len(missing),
                "extra_count": len(extra),
                "missing_key_sample": _sorted_key_sample(missing),
                "extra_key_sample": _sorted_key_sample(extra),
            })

    slice_integrity_ok = not part_mismatches
    strict_coverage_ok = not coverage_mismatches
    ok = slice_integrity_ok and strict_coverage_ok
    return {
        "available": True,
        "ok": ok,
        "slice_integrity_ok": slice_integrity_ok,
        "strict_coverage_ok": strict_coverage_ok,
        "message": (
            "Every split part matches its source JSON slice and strict coverage passed."
            if ok
            else "Source slice integrity and strict coverage produced different results."
        ),
        "source_path": str(source_path),
        "part_mismatch_count": len(part_mismatches),
        "coverage_mismatch_count": len(coverage_mismatches),
        "part_mismatch_examples": part_mismatches[:5],
        "coverage_mismatch_examples": coverage_mismatches[:10],
    }


def _find_single_manifest(split_dir: Path) -> Path:
    """Find a single split manifest in split_dir."""
    candidates = sorted(split_dir.glob("*__split_manifest.json"))
    if not candidates:
        raise FileNotFoundError("No *__split_manifest.json found in split directory.")
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise ValueError("Multiple split manifests found: " + names)
    return candidates[0]


def _chunk_value_from_doc(
    *,
    part_doc: Any,
    part_info: dict[str, Any],
    root_skeleton_present: bool,
) -> Any:
    """Return chunk payload from a chunk document."""
    if (
        isinstance(part_doc, dict)
        and isinstance(part_doc.get("meta"), dict)
        and part_doc["meta"].get("schema") == CHUNK_SCHEMA
        and "payload" in part_doc
    ):
        return part_doc["payload"]

    if root_skeleton_present:
        return part_doc

    path_parts = [str(item) for item in part_info.get("path_parts", [])]
    return _get_nested_value(part_doc, path_parts) if path_parts else part_doc


def _validate_route_manifest(
    *,
    manifest: dict[str, Any],
    manifest_dir: Path,
) -> dict[str, Any]:
    """Validate route manifest presence and basic shape."""
    route_name = _safe_text(manifest.get("web_ai_route_manifest_filename", ""))
    if not route_name:
        return {
            "ok": False,
            "present": False,
            "filename": "",
            "message": "Split manifest does not reference web_ai_route_manifest_filename.",
            "question_route_count": 0,
            "section_count": 0,
        }

    route_path = manifest_dir / route_name
    if not route_path.exists():
        return {
            "ok": False,
            "present": False,
            "filename": route_name,
            "message": "Referenced route manifest file does not exist.",
            "question_route_count": 0,
            "section_count": 0,
        }

    route_data = _load_json(route_path)
    if not isinstance(route_data, dict):
        return {
            "ok": False,
            "present": True,
            "filename": route_name,
            "message": "Route manifest top level is not an object.",
            "question_route_count": 0,
            "section_count": 0,
        }

    schema_ok = route_data.get("schema") == ROUTE_MANIFEST_SCHEMA
    routes = route_data.get("question_routes", {})
    sections = route_data.get("section_index", {})
    route_count = len(routes) if isinstance(routes, dict) else 0
    section_count = len(sections) if isinstance(sections, dict) else 0

    return {
        "ok": bool(schema_ok and route_count > 0 and section_count > 0),
        "present": True,
        "filename": route_name,
        "message": (
            "Route manifest is present and has route metadata."
            if schema_ok and route_count > 0 and section_count > 0
            else "Route manifest is present but missing required route metadata."
        ),
        "question_route_count": route_count,
        "section_count": section_count,
    }


def _reassemble_from_manifest(
    *,
    manifest: dict[str, Any],
    manifest_dir: Path,
) -> tuple[Any, list[dict[str, Any]]]:
    """Reassemble chunks from a split manifest and return hash warnings."""
    parts = manifest.get("parts", [])
    if not isinstance(parts, list) or not parts:
        raise ValueError("Manifest has no parts.")

    root_skeleton = manifest.get("root_skeleton")
    root_skeleton_present = "root_skeleton" in manifest

    path_entries: dict[tuple[str, ...], list[tuple[Any, Any]]] = defaultdict(list)
    path_is_list: dict[tuple[str, ...], bool] = {}
    hash_checks: list[dict[str, Any]] = []

    fallback_root: Any = None

    for part_info in parts:
        if not isinstance(part_info, dict):
            raise TypeError("Manifest part entry must be an object.")

        filename = _safe_text(part_info.get("filename", ""))
        if not filename:
            raise ValueError("Manifest part entry is missing filename.")

        part_path = manifest_dir / filename
        if not part_path.exists():
            raise FileNotFoundError("Missing chunk file: " + filename)

        part_doc = _load_json(part_path)
        path_tuple = tuple(str(item) for item in part_info.get("path_parts", []))
        is_list = bool(part_info.get("is_list", False))
        path_is_list[path_tuple] = is_list

        chunk_value = _chunk_value_from_doc(
            part_doc=part_doc,
            part_info=part_info,
            root_skeleton_present=root_skeleton_present,
        )

        if not root_skeleton_present and fallback_root is None:
            fallback_root = copy.deepcopy(part_doc)

        expected_hash = _safe_text(part_info.get("payload_sha256", ""))
        actual_hash = stable_hash(chunk_value)
        hash_checks.append(
            {
                "filename": filename,
                "expected_payload_sha256": expected_hash,
                "actual_payload_sha256": actual_hash,
                "ok": bool(not expected_hash or expected_hash == actual_hash),
            }
        )

        entry_keys = part_info.get("entry_keys", [])
        if not isinstance(entry_keys, list):
            entry_keys = []
        path_entries[path_tuple].extend(_get_entries(chunk_value, entry_keys))

    if root_skeleton_present:
        reconstructed = copy.deepcopy(root_skeleton)
    else:
        if fallback_root is None:
            raise RuntimeError("No chunk files could be read.")
        reconstructed = copy.deepcopy(fallback_root)

    # Apply root chunks first, then nested chunks. The splitter can store large
    # sections such as files, call_edges, source_file_index, and
    # stable_evidence_id_index as nested chunks while root chunks store the rest
    # of the top-level object. If nested chunks are applied first and then the
    # root chunk is applied last, the root replacement discards those nested
    # sections and produces a false source_hash_ok failure.
    for path_tuple in sorted(path_entries.keys(), key=len):
        merged = _rebuild_container(path_entries[path_tuple], path_is_list[path_tuple])
        reconstructed = _set_nested_value(reconstructed, list(path_tuple), merged)

    return reconstructed, hash_checks
