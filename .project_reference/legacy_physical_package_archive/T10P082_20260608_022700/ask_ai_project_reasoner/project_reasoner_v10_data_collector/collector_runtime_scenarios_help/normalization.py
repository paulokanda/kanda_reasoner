"""Normalization helpers for collector_runtime_scenarios."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

def _safe_text(value: Any) -> str:
    return str(value or "").strip()

def _safe_lower(value: Any) -> str:
    return _safe_text(value).lower()

def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0

def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return {}

def _normalize_path_text(value: Any) -> str:
    return _safe_text(value).replace("\\", "/")
