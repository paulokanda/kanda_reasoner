#!/usr/bin/env python3
# project-path: tools/repair_frozen_memory_index_compatibility_v1.py
"""Rebuild the derived freeze index without editing frozen entry files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any

FEATURE_ID = "frozen-memory-integrity-compatibility-recovery-v1"
_ALLOWED_STATUSES = {"frozen", "superseded", "active", "validated"}
_BOM_COMPAT_ID = "freeze-20260613-freeze-after-update-bom-index-tolerance-v1"
_ALIAS_COMPAT_ID = (
    "freeze-20260616-freeze-formulary-current-feature-autofill-regression-v1"
)


def _sha256(path: Path) -> str:
    """Return one file digest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _entry_hashes(paths: list[Path]) -> dict[str, str]:
    """Return exact entry hashes keyed by resolved path."""
    return {str(path.resolve(strict=False)): _sha256(path) for path in paths}


def _validate_freezes(
    freezes: list[dict[str, Any]],
    *,
    entry_count: int,
) -> None:
    """Validate identity, status, supersession, and compatibility recovery."""
    if len(freezes) != entry_count:
        raise RuntimeError(
            "Freeze index entry count mismatch: "
            + str(len(freezes))
            + " versus "
            + str(entry_count)
        )

    ids = [str(item.get("freeze_id") or "") for item in freezes]
    if not all(ids) or len(ids) != len(set(ids)):
        raise RuntimeError("Freeze IDs are empty or duplicated.")
    id_set = set(ids)

    for item in freezes:
        freeze_id = str(item.get("freeze_id") or "")
        status = str(item.get("status") or "").strip().casefold()
        if status not in _ALLOWED_STATUSES:
            raise RuntimeError(
                "Unsupported freeze status for " + freeze_id + ": " + status
            )
        superseded_by = str(item.get("superseded_by") or "").strip()
        if superseded_by and superseded_by not in id_set:
            raise RuntimeError(
                "Missing superseding freeze for "
                + freeze_id
                + ": "
                + superseded_by
            )
        if not str(item.get("entry") or "").strip():
            raise RuntimeError("Freeze entry path is empty for " + freeze_id)

    by_id = {str(item["freeze_id"]): item for item in freezes}
    if _BOM_COMPAT_ID in by_id:
        item = by_id[_BOM_COMPAT_ID]
        if not item.get("protected_paths"):
            raise RuntimeError(
                "Historical BOM freeze protected paths were not recovered."
            )
        if not item.get("do_not_touch_summary"):
            raise RuntimeError(
                "Historical BOM freeze rules were not recovered."
            )
        print("HISTORICAL_BODY_PROTECTED_PATH_RECOVERY: PASS")
        print("HISTORICAL_BODY_RULE_RECOVERY: PASS")

    if _ALIAS_COMPAT_ID in by_id:
        item = by_id[_ALIAS_COMPAT_ID]
        if str(item.get("box") or "") != (
            "kanda_reasoner_app/freeze_after_update_gui"
        ):
            raise RuntimeError("Historical primary_box alias was not recovered.")
        if not item.get("do_not_touch_summary"):
            raise RuntimeError(
                "Historical do_not_regress_rules alias was not recovered."
            )
        print("HISTORICAL_FRONTMATTER_BOX_ALIAS: PASS")
        print("HISTORICAL_FRONTMATTER_RULE_ALIAS: PASS")

    print("FROZEN_MEMORY_UNIQUE_IDS: PASS")
    print("FROZEN_MEMORY_STATUS_VALUES: PASS")
    print("FROZEN_MEMORY_SUPERSESSION_REFERENCES: PASS")


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write one UTF-8 JSON object atomically without a BOM."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
        delete=False,
    ) as handle:
        temp_path = Path(handle.name)
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    try:
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _canonical_freezes(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the derived freezes list from an index payload."""
    freezes = payload.get("freezes")
    if not isinstance(freezes, list):
        raise RuntimeError("freeze_index.json must contain a freezes list.")
    return [dict(item) for item in freezes if isinstance(item, dict)]


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Rebuild or verify the generated index and preserve entry bytes."""
    args = parse_args()
    project_root = Path(args.project_root).expanduser().resolve(strict=False)

    from kanda_reasoner_app.freeze_after_update.freeze_state import (
        build_index_payload,
        entry_files,
        load_freeze_index,
    )
    from kanda_reasoner_app.freeze_after_update.paths import build_paths

    entries = entry_files(project_root)
    if not entries:
        raise RuntimeError("No frozen entry files were found.")
    before = _entry_hashes(entries)

    expected = build_index_payload(project_root)
    expected_freezes = _canonical_freezes(expected)
    _validate_freezes(expected_freezes, entry_count=len(entries))

    paths = build_paths(project_root)
    if args.write:
        _atomic_write_json(paths.freeze_index, expected)
        print("FREEZE_INDEX_REBUILT: PASS")
    else:
        current = load_freeze_index(project_root)
        current_freezes = _canonical_freezes(current)
        if current_freezes != expected_freezes:
            raise RuntimeError(
                "freeze_index.json is not in sync with compatible entry parsing."
            )
        print("FREEZE_INDEX_IN_SYNC: PASS")

    loaded = load_freeze_index(project_root)
    loaded_freezes = _canonical_freezes(loaded)
    if loaded_freezes != expected_freezes:
        raise RuntimeError("Rebuilt freeze index does not match expected entries.")
    if paths.freeze_index.read_bytes().startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Regenerated freeze_index.json contains a UTF-8 BOM.")
    print("FREEZE_INDEX_BOM_READ_COMPATIBILITY: PASS")
    print("FREEZE_INDEX_WRITTEN_WITHOUT_BOM: PASS")

    after = _entry_hashes(entries)
    if before != after:
        raise RuntimeError("Frozen entry files changed during index repair.")
    print("FROZEN_ENTRIES_READ_ONLY: PASS")
    print("FROZEN_MEMORY_ENTRY_COUNT: " + str(len(entries)))
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("FROZEN MEMORY INDEX REPAIR ERROR")
        print("ERROR TYPE: " + exc.__class__.__name__)
        print("ERROR MESSAGE: " + str(exc))
        raise SystemExit(1)
