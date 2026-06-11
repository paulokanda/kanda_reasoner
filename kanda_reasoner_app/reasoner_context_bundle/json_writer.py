"""Atomic JSON writing helpers for reasoner context bundle files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

__all__ = ["write_json_atomic"]


def write_json_atomic(path: str | Path, payload: Any) -> Path:
    """Write JSON atomically and verify that the result can be loaded.

    The write is staged through a temporary sibling file before replacement.
    This avoids leaving a half-written JSON artifact if generation is
    interrupted.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")

    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=True, indent=2, sort_keys=True)
            handle.write("\n")

        with temporary.open("r", encoding="utf-8") as handle:
            json.load(handle)

        temporary.replace(destination)
        return destination
    finally:
        if temporary.exists():
            temporary.unlink()
