# project-path: kanda_reasoner_app/freeze_hint_intake/consumed_hints.py
"""Consumed freeze hint bookkeeping helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .models import SCHEMA_VERSION, FreezeHintIntakePaths
from .paths_io import _atomic_write_json, _coerce_mapping, _utc_now, _safe_slug
from .frozen_matching import (
    _candidate_feature_slugs_from_record,
    _find_matching_frozen_feature_in_entry_files,
    _freeze_feature_tail_slug,
    _same_feature_id_alias,
)

def _load_consumed(path: Path) -> dict[str, Any]:
    """Support load consumed behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    if not path.exists():
        return {"schema_version": SCHEMA_VERSION, "kind": "kanda_consumed_freeze_hints", "items": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return {"schema_version": SCHEMA_VERSION, "kind": "kanda_consumed_freeze_hints", "items": []}
    if not isinstance(data, dict):
        return {"schema_version": SCHEMA_VERSION, "kind": "kanda_consumed_freeze_hints", "items": []}
    if not isinstance(data.get("items"), list):
        data["items"] = []
    return data

def _remember_consumed_hint(
    paths: FreezeHintIntakePaths,
    *,
    source_signature: Mapping[str, Any],
    hint: Mapping[str, Any],
    used_freeze_id: str,
) -> None:
    """Record an already-frozen staged hint as consumed.

    This prevents New Local Freeze Entry from repeatedly re-importing a staged
    patch ZIP for a feature that already exists in frozen_features_memory.
    """

    consumed = _load_consumed(paths.consumed_hints)
    used_at = _utc_now()
    consumed_item = {
        "consumed_at_utc": used_at,
        "used_freeze_id": str(used_freeze_id or "").strip(),
        "source": _coerce_mapping(source_signature),
        "feature_id": str(hint.get("feature_id") or "").strip(),
        "feature_title": str(hint.get("feature_title") or "").strip(),
    }
    consumed.setdefault("items", [])
    if not any(_same_consumed_source(item, consumed_item) for item in consumed["items"] if isinstance(item, Mapping)):
        consumed["items"].append(consumed_item)
    consumed["updated_at_utc"] = used_at
    _atomic_write_json(paths.consumed_hints, consumed)

def _remember_explicit_human_ignore(
    paths: FreezeHintIntakePaths,
    *,
    source_signature: Mapping[str, Any],
    hint: Mapping[str, Any],
) -> None:
    """Persist explicit human Ignore as authoritative consumed state.

    The visible candidate record/source may be deleted after this tombstone is
    written, but the exact ignored source must remain blocked on later rescans.
    This preserves the established Freeze consumption authority contract while
    still allowing a genuinely different newer repair source to remain eligible.
    """

    consumed = _load_consumed(paths.consumed_hints)
    ignored_at = _utc_now()
    ignored_item = {
        "consumed_at_utc": ignored_at,
        "used_freeze_id": "ignored-by-human",
        "source": _coerce_mapping(source_signature),
        "feature_id": str(hint.get("feature_id") or "").strip(),
        "feature_title": str(hint.get("feature_title") or "").strip(),
    }

    items = [
        item
        for item in consumed.get("items", [])
        if not (
            isinstance(item, Mapping)
            and _same_consumed_source(item, ignored_item)
        )
    ]
    items.append(ignored_item)
    consumed["items"] = items
    consumed["updated_at_utc"] = ignored_at
    _atomic_write_json(paths.consumed_hints, consumed)


def _is_consumed(
    consumed: Mapping[str, Any],
    signature: Mapping[str, Any],
    hint: Mapping[str, Any],
    *,
    project_root: Path | None = None,
) -> bool:
    """Return True only for consumed records that really belong to this feature.

    A prior false already-frozen match can leave a consumed_freeze_hints.json
    item for the current patch but with an unrelated used_freeze_id. That stale
    false-consumed item must not hide the current valid unconsumed patch forever.
    The consumed item is authoritative only when its source/feature matches and
    its used_freeze_id is absent/legacy or names the same feature identity.
    """

    probe = {
        "source": dict(signature),
        "feature_id": str(hint.get("feature_id") or ""),
        "feature_title": str(hint.get("feature_title") or ""),
    }
    for item in consumed.get("items", []):
        if not isinstance(item, Mapping):
            continue
        if not _same_consumed_source(item, probe):
            continue
        if not _consumed_freeze_id_confirms_hint(item, hint):
            continue
        if _consumed_record_is_authoritative(item, hint, project_root=project_root):
            return True
    return False


def _consumed_record_is_authoritative(
    item: Mapping[str, Any],
    hint: Mapping[str, Any],
    *,
    project_root: Path | None,
) -> bool:
    """Return True only when consumption has a valid authority source.

    Explicit human ignore remains authoritative. Legacy non-freeze markers remain
    authoritative for backward compatibility. A freeze-id consumption record is
    authoritative only when the selected project's canonical frozen entry files
    contain the matching feature and exact freeze ID. This prevents stale index
    artifacts or orphaned consumed records from permanently suppressing a valid
    current repair sidecar.
    """

    used_freeze_id = str(item.get("used_freeze_id") or "").strip()
    if used_freeze_id == "ignored-by-human":
        return True
    if not used_freeze_id or not used_freeze_id.startswith("freeze-"):
        return True
    if project_root is None:
        return True

    candidate_slugs = _candidate_feature_slugs_from_record({"hint": dict(hint)})
    matched = _find_matching_frozen_feature_in_entry_files(
        Path(project_root).resolve(),
        candidate_slugs,
    )
    if matched is None:
        return False

    matched_freeze_id = _safe_slug(str(matched.get("freeze_id") or ""))
    recorded_freeze_id = _safe_slug(used_freeze_id)
    return bool(matched_freeze_id and matched_freeze_id == recorded_freeze_id)

def _consumed_freeze_id_confirms_hint(item: Mapping[str, Any], hint: Mapping[str, Any]) -> bool:
    """Reject false-consumed records whose used_freeze_id names another feature.

    Do not infer consumed status from arbitrary old consumed records when the
    recorded used_freeze_id belongs to a different repair. This lets runtime-lite
    remain selectable after an earlier false-positive consumed it.
    """

    used_freeze_id = str(item.get("used_freeze_id") or "").strip()
    if not used_freeze_id:
        return True
    if not used_freeze_id.startswith("freeze-"):
        return True

    hint_slugs = {
        _safe_slug(str(hint.get("feature_id") or "")),
        _safe_slug(str(hint.get("feature_title") or "")),
    }
    hint_slugs.discard("")
    hint_slugs.discard("freeze-hint")
    if not hint_slugs:
        return True

    freeze_slugs = {_safe_slug(used_freeze_id)}
    freeze_tail = _freeze_feature_tail_slug(used_freeze_id)
    if freeze_tail:
        freeze_slugs.add(freeze_tail)
    freeze_slugs.discard("")
    freeze_slugs.discard("freeze-hint")

    return bool(hint_slugs.intersection(freeze_slugs))


def _source_name_for_compare(source: Mapping[str, Any]) -> str:
    """Return a stable source filename when legacy metadata permits comparison."""

    explicit = str(source.get("source_name") or "").strip()
    if explicit:
        return explicit.casefold()
    source_path = str(source.get("source_path") or "").strip()
    if not source_path:
        return ""
    return Path(source_path).name.casefold()

def _same_consumed_source(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    """Support same consumed source behavior.
    
    Parameters
    ----------
    left : Mapping[str, Any]
        The left value.
    right : Mapping[str, Any]
        The right value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    left_source = _coerce_mapping(left.get("source"))
    right_source = _coerce_mapping(right.get("source"))
    keys = ("source_path", "source_mtime_ns", "source_size_bytes")
    left_complete = all(str(left_source.get(key, "")) for key in keys)
    right_complete = all(str(right_source.get(key, "")) for key in keys)

    if left_complete and right_complete:
        return all(
            str(left_source.get(key, "")) == str(right_source.get(key, ""))
            for key in keys
        )

    left_name = _source_name_for_compare(left_source)
    right_name = _source_name_for_compare(right_source)
    used_freeze_id = str(left.get("used_freeze_id") or "").strip()

    # A complete current candidate must not be shadowed by an anonymous legacy
    # consumed item that has neither a comparable source name nor an authority
    # marker. Older versions could persist feature-only consumed rows; treating
    # those rows as every future repair source strands cumulative same-feature
    # releases forever. Preserve compatibility only when the legacy row can be
    # tied to the same source name or carries explicit ignore/freeze authority.
    if right_complete and not left_complete:
        if left_name and right_name and left_name != right_name:
            return False
        if not used_freeze_id and not (left_name and right_name):
            return False

    if left_complete and not right_complete:
        if left_name and right_name and left_name != right_name:
            return False

    # Legacy fallback is now bounded: it applies when source identity is the
    # same/compatible, or when explicit authority metadata exists. It no longer
    # lets an anonymous feature-only consumed row hide every future repair ZIP.
    left_id = str(left.get("feature_id") or "")
    right_id = str(right.get("feature_id") or "")
    if left_id and right_id and _same_feature_id_alias(left_id, right_id):
        return True
    left_title = str(left.get("feature_title") or "").strip()
    right_title = str(right.get("feature_title") or "").strip()
    return bool(left_title and right_title and left_title == right_title)
