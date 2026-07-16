"""
Symbol Churn Analyzer - v1.0
============================

Deterministic semantic delta layer.

Compares previous and current symbol index files.

Outputs:
- added symbols
- removed symbols
- churn_count
- churn_ratio

Pure set comparison.
No inference.
No mutation.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Set


def _load_symbol_index(path: Path) -> Set[str]:
    if not path.exists():
        return set()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return set()

    symbols = data.get("symbols", [])
    return {
        f"{s['module']}::{s['type']}::{s['name']}"
        for s in symbols
    }


def analyze_symbol_churn(previous_path: Path, current_path: Path, output_path: Path, prefix: str) -> Dict[str, Any]:
    previous_symbols = _load_symbol_index(previous_path)
    current_symbols = _load_symbol_index(current_path)

    added = sorted(list(current_symbols - previous_symbols))
    removed = sorted(list(previous_symbols - current_symbols))

    churn_count = len(added) + len(removed)

    total_base = len(previous_symbols) if previous_symbols else 1
    churn_ratio = round(churn_count / total_base, 4)

    result = {
        "churn_version": "1.0",
        "domain_prefix": prefix,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "previous_symbol_count": len(previous_symbols),
        "current_symbol_count": len(current_symbols),
        "added_count": len(added),
        "removed_count": len(removed),
        "churn_count": churn_count,
        "churn_ratio": churn_ratio,
        "added_symbols": added,
        "removed_symbols": removed
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, sort_keys=True)

    return result