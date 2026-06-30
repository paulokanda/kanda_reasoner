
# project-path: kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/hash_utils.py
"""Deterministic hash helpers for offline Adviser registry records.

The functions in this module hash values that are explicitly supplied by the
caller. They do not read files, scan source trees, access git state, or write
anything. This keeps M6 safe as registry-record infrastructure only.
"""

from __future__ import annotations


__all__ = [
    'canonical_json',
    'hash_mapping',
    'hash_record_without_field',
    'hash_sequence',
    'hash_value',
]
import hashlib
import json
from typing import Any, Mapping, Sequence

FEATURE_ID = "routing_signal_scorer_v3_adviser_gold_manifest_run_registry_v1"
SCHEMA_VERSION = "3.45-adviser-gold-manifest-run-registry"
AUTHORITY_STATEMENT = "advisory_only"


def canonical_json(value: Any) -> str:
    """Return deterministic JSON for supplied values only."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    """Return sha256 hex for supplied text."""

    if not isinstance(text, str):
        raise TypeError("sha256_text expects str")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_value(value: Any) -> str:
    """Hash any JSON-serializable supplied value using canonical JSON."""

    return sha256_text(canonical_json(value))


def hash_mapping(mapping: Mapping[str, Any]) -> str:
    """Hash a supplied mapping."""

    if not isinstance(mapping, Mapping):
        raise TypeError("hash_mapping expects a mapping")
    return hash_value(dict(mapping))


def hash_sequence(items: Sequence[Any]) -> str:
    """Hash a supplied sequence."""

    if isinstance(items, (str, bytes, bytearray)) or not isinstance(items, Sequence):
        raise TypeError("hash_sequence expects a non-string sequence")
    return hash_value(list(items))


def hash_record_without_field(record: Mapping[str, Any], field_name: str) -> str:
    """Hash a supplied record after removing one field such as record_hash."""

    if not isinstance(record, Mapping):
        raise TypeError("hash_record_without_field expects a mapping")
    clone = dict(record)
    clone.pop(field_name, None)
    return hash_mapping(clone)
